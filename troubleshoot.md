lsof -i :8000
kill -9 27869  or direct fuser -k 8000/tcp

# questions
can we use rag in this case?
voice
handwritten note

# prompt
------------
what is the total amount due on the electricity bill for march 2026
list all unpaid bills
which bill has the highest amount
what is the Jio fiber bill amount
summarise all bills
total GST across all bills
which vendor has sent the most bills

total orders
show all orders
total amount of all orders



what is the total sales revenue in Q1 2026
which region had the highest sales in Q1 2026
did we achieve our sales target in Q1 2026
how much did we exceed the sales target by
who are the top 5 customers by revenue
which product category generated the most revenue
what is the month wise sales breakdown for Q1 2026
what was the sales growth from January to March 2026
how many orders were placed in Q1 2026
what is the average order value in Q1 2026
what are the key challenges mentioned in the sales report
what is the sales forecast for Q2 2026
which region underperformed and why



-----------


curl -X POST http://localhost:8000/api/agent/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "total orders in year 2014", "source": "db"}'

  curl -X POST http://localhost:8000/api/db/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT EXTRACT(YEAR FROM order_date) AS year, COUNT(*) AS total FROM orders GROUP BY year ORDER BY year;"}'

##Restart Ollama cleanly
bash# Kill Ollama completely
sudo pkill ollama
sleep 3

# Start fresh
sudo ollama serve &
sleep 5

# Try the smallest possible test
ollama run llama3.2:latest "say hi"

#Restart API with the working model
fuser -k 8000/tcp
cd ~/Agent-AI/api && python main.py





----------orders

cat > ~/Agent-AI/data/uploads/orders/order_ORD001_acme_corp.txt << 'EOF'
================================================
             ORDER CONFIRMATION
================================================
Order No     : ORD-2026-001
Order Date   : 01-Mar-2026
Delivery Date: 10-Mar-2026
Status       : Delivered

CUSTOMER DETAILS
----------------
Name         : Acme Corp
Contact      : Mr. Rajesh Sharma
Phone        : +91-9876543210
Email        : rajesh@acmecorp.com
Address      : 101 Industrial Area, Pune - 411001

ITEMS ORDERED
------------------------------------------------
Sr  Item Description        Qty   Rate    Amount
------------------------------------------------
1   Industrial Bolts M10    500   Rs. 12  Rs.  6,000
2   Steel Pipe 2inch        100   Rs. 85  Rs.  8,500
3   Welding Rods Box         20   Rs.450  Rs.  9,000
4   Safety Gloves Pair       50   Rs. 95  Rs.  4,750
5   Grease Cartridge         30   Rs.120  Rs.  3,600
------------------------------------------------
                    Subtotal     Rs. 31,850
                    GST 18%      Rs.  5,733
                    Freight      Rs.    500
------------------------------------------------
                    TOTAL        Rs. 38,083
================================================
Payment Terms : Net 30 days
Payment Status: PAID
Delivered By  : BlueDart Express
Tracking No   : BD-2026-887432
================================================
EOF

cat > ~/Agent-AI/data/uploads/orders/order_ORD002_beta_solutions.txt << 'EOF'
================================================
             ORDER CONFIRMATION
================================================
Order No     : ORD-2026-002
Order Date   : 05-Mar-2026
Expected Date: 20-Mar-2026
Status       : Pending

CUSTOMER DETAILS
----------------
Name         : Beta Solutions Pvt Ltd
Contact      : Ms. Priya Mehta
Phone        : +91-9823456789
Email        : priya@betasolutions.in
Address      : 45 Tech Park, Hinjewadi, Pune - 411057

ITEMS ORDERED
------------------------------------------------
Sr  Item Description        Qty   Rate    Amount
------------------------------------------------
1   Laptop Stand Aluminium   10   Rs.899  Rs.  8,990
2   USB Hub 7-Port           10   Rs.599  Rs.  5,990
3   Wireless Mouse           15   Rs.449  Rs.  6,735
4   HDMI Cable 2m            20   Rs.199  Rs.  3,980
------------------------------------------------
                    Subtotal     Rs. 25,695
                    GST 18%      Rs.  4,625
                    Freight      Rs.    250
------------------------------------------------
                    TOTAL        Rs. 30,570
================================================
Payment Terms : Advance 50% + 50% on delivery
Payment Status: PARTIALLY PAID (Rs. 15,285 received)
Balance Due   : Rs. 15,285
================================================
EOF

cat > ~/Agent-AI/data/uploads/orders/order_ORD003_gamma_ltd.txt << 'EOF'
================================================
             ORDER CONFIRMATION
================================================
Order No     : ORD-2026-003
Order Date   : 08-Mar-2026
Expected Date: 18-Mar-2026
Status       : Shipped

CUSTOMER DETAILS
----------------
Name         : Gamma Ltd
Contact      : Mr. Vikram Nair
Phone        : +91-9765432100
Email        : vikram@gammaltd.com
Address      : Plot 7, MIDC Chinchwad, Pimpri - 411019

ITEMS ORDERED
------------------------------------------------
Sr  Item Description        Qty   Rate    Amount
------------------------------------------------
1   Office Chair Ergonomic    5  Rs.4500  Rs. 22,500
2   Standing Desk             2  Rs.8999  Rs. 17,998
3   Monitor Arm               5  Rs.1299  Rs.  6,495
------------------------------------------------
                    Subtotal     Rs. 46,993
                    GST 18%      Rs.  8,459
                    Freight      Rs.    800
------------------------------------------------
                    TOTAL        Rs. 56,252
================================================
Payment Terms : Net 15 days
Payment Status: UNPAID
Shipped Via   : DTDC Courier
Tracking No   : DTDC-2026-334421
================================================
EOF

cat > ~/Agent-AI/data/uploads/orders/order_ORD004_delta_pvt.txt << 'EOF'
================================================
             ORDER CONFIRMATION
================================================
Order No     : ORD-2026-004
Order Date   : 10-Mar-2026
Cancelled On : 11-Mar-2026
Status       : Cancelled

CUSTOMER DETAILS
----------------
Name         : Delta Pvt Ltd
Contact      : Mr. Anil Desai
Phone        : +91-9988776655
Email        : anil@deltapvt.com
Address      : 22 Commerce Zone, Nashik - 422001

CANCELLATION REASON
-------------------
Customer requested cancellation due to budget freeze.
Refund of advance Rs. 5,000 initiated on 11-Mar-2026.
Refund Reference : REF-2026-00234

ITEMS (CANCELLED)
------------------------------------------------
Sr  Item Description        Qty   Rate    Amount
------------------------------------------------
1   Printer LaserJet          2  Rs.8500  Rs. 17,000
2   Ink Cartridge Set (5)    10  Rs.1200  Rs. 12,000
------------------------------------------------
                    TOTAL (Cancelled) Rs. 29,000
================================================
EOF

cat > ~/Agent-AI/data/uploads/orders/order_ORD005_sigma_traders.txt << 'EOF'
================================================
             ORDER CONFIRMATION
================================================
Order No     : ORD-2026-005
Order Date   : 11-Mar-2026
Expected Date: 25-Mar-2026
Status       : Pending

CUSTOMER DETAILS
----------------
Name         : Sigma Traders
Contact      : Ms. Sunita Kulkarni
Phone        : +91-9871234560
Email        : sunita@sigmatraders.in
Address      : Shop 12, Market Yard, Solapur - 413001

ITEMS ORDERED
------------------------------------------------
Sr  Item Description        Qty   Rate    Amount
------------------------------------------------
1   Cotton Fabric (metres)  200   Rs.180  Rs. 36,000
2   Polyester Blend (metres)150   Rs.220  Rs. 33,000
3   Thread Spools (box)      10   Rs.350  Rs.  3,500
4   Packaging Material        5  Rs.1200  Rs.  6,000
------------------------------------------------
                    Subtotal     Rs. 78,500
                    GST 5%       Rs.  3,925
                    Freight      Rs.  1,200
------------------------------------------------
                    TOTAL        Rs. 83,625
================================================
Payment Terms : Net 30 days
Payment Status: UNPAID
Special Note  : Customer requested delivery before 25-Mar-2026
================================================
EOF

echo "✅ 5 sample orders created"
ls -lh ~/Agent-AI/data/uploads/orders/
