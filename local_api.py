from fastapi import FastAPI
import json

app = FastAPI()

# Load JSON file once at startup
with open("data.json", "r") as file:
    local_data = json.load(file)

@app.get("/search")
def search_data(q: str):
    # Dummy offline data source
    
    # Simple offline search
    return {"result": local_data.get(q.lower(), "No data found locally.")}
