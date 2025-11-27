import tkinter as tk
from tkinter import scrolledtext
import requests
#from langchain.llms import Ollama
from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM

#llm = Ollama(model="llama3")
llm = OllamaLLM(model="llama3")

def run_agent():
    query = user_input.get()
    if not query:
        return

    # Call your local API (still offline)
    try:
        api_response = requests.get(
            "http://localhost:9000/search",
            params={"q": query}
        ).json()["result"]
    except:
        api_response = "Local API unavailable."

    prompt = f"""
    You are a local AI agent. No internet.
    User asked: {query}
    
    Local API says: {api_response}

    Combine your knowledge + API result to give final answer.
    """

    #answer = llm(prompt)
    answer = llm.invoke(prompt)

    output_box.insert(tk.END, f"User: {query}\n", "user")
    output_box.insert(tk.END, f"Agent: {answer}\n\n", "agent")
    user_input.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Pure Local AI Agent")
root.geometry("650x520")

title = tk.Label(root, text="Local Agent Search App (100% Offline)", font=("Arial", 16))
title.pack(pady=10)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
output_box.pack(pady=10)
output_box.tag_config("user", foreground="blue")
output_box.tag_config("agent", foreground="green")

user_input = tk.Entry(root, width=60, font=("Arial", 12))
user_input.pack(pady=5)

run_button = tk.Button(root, text="Search", command=run_agent, width=10)
run_button.pack(pady=5)

root.mainloop()
