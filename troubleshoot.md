lsof -i :8000
kill -9 27869  or direct fuser -k 8000/tcp


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
cd ~/claude/api && python main.py

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

# questions
can we use rag in this case?
voice
handwritten note
