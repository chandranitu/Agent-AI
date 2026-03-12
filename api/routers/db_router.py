"""
routers/db_router.py
────────────────────
All PostgreSQL 18.1 interactions.
Uses psycopg3 (the modern async-capable driver, fully open-source).
Returns ONLY data that actually exists in the database — no fabrication.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import psycopg
import json

from config import settings

router = APIRouter()


def get_connection():
    """Return a synchronous psycopg3 connection."""
    return psycopg.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        connect_timeout=10,
    )


# ─── Schema discovery ────────────────────────────────────────────────────────

@router.get("/schema")
def get_schema():
    """
    Return all table names and their columns from the connected database.
    The AI agent calls this first so it knows what tables exist before
    constructing any query — preventing hallucinated table/column names.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        t.table_name,
                        array_agg(c.column_name || ' ' || c.data_type ORDER BY c.ordinal_position) AS columns
                    FROM information_schema.tables t
                    JOIN information_schema.columns c
                      ON t.table_name = c.table_name AND t.table_schema = c.table_schema
                    WHERE t.table_schema = 'public'
                      AND t.table_type = 'BASE TABLE'
                    GROUP BY t.table_name
                    ORDER BY t.table_name;
                """)
                rows = cur.fetchall()
                return {
                    "tables": [
                        {"table": r[0], "columns": r[1]} for r in rows
                    ]
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB connection error: {str(e)}")


# ─── Safe parameterised query runner ─────────────────────────────────────────

@router.post("/query")
def run_query(payload: dict):
    """
    Execute a READ-ONLY SQL query.
    Body: { "sql": "SELECT ...", "params": [] }

    Only SELECT statements are permitted — all others are rejected
    to prevent data modification through the agent.
    """
    sql: str = payload.get("sql", "").strip()
    params: list = payload.get("params", [])

    if not sql.lower().startswith("select"):
        raise HTTPException(
            status_code=400,
            detail="Only SELECT statements are permitted through this endpoint."
        )

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                cols = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return {
                    "columns": cols,
                    "rows": [dict(zip(cols, row)) for row in rows],
                    "row_count": len(rows),
                }
    except psycopg.errors.UndefinedTable as e:
        raise HTTPException(status_code=400, detail=f"Table not found: {str(e)}")
    except psycopg.errors.UndefinedColumn as e:
        raise HTTPException(status_code=400, detail=f"Column not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Convenience endpoints ────────────────────────────────────────────────────

@router.get("/reports")
def list_reports(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: Optional[str] = None,
):
    """
    List rows from the 'reports' table.
    Assumes schema: reports(id, title, category, created_at, summary)
    Adjust column names to match your actual schema.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if search:
                    cur.execute(
                        """
                        SELECT id, title, category, created_at, summary
                        FROM reports
                        WHERE title ILIKE %s OR summary ILIKE %s
                        ORDER BY created_at DESC
                        LIMIT %s OFFSET %s
                        """,
                        (f"%{search}%", f"%{search}%", limit, offset),
                    )
                else:
                    cur.execute(
                        """
                        SELECT id, title, category, created_at, summary
                        FROM reports
                        ORDER BY created_at DESC
                        LIMIT %s OFFSET %s
                        """,
                        (limit, offset),
                    )
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
                return {"reports": [dict(zip(cols, r)) for r in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/{report_id}")
def get_report(report_id: int):
    """Fetch a single report by primary key."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM reports WHERE id = %s", (report_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Report not found")
                cols = [d[0] for d in cur.description]
                return dict(zip(cols, row))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
