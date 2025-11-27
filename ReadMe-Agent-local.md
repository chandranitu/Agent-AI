## Agentic AI 

##python3.10
# python3.10 -m venv /home/hadoop/venv-agentic
# source /home/hadoop/venv-agentic/bin/activate
# deactivate

#complete local setup

A local GUI app
✔ A local AI agent
✔ A local API endpoint (localhost only)
✔ No cloud access
✔ Everything runs offline

#install in python3.10
pip uninstall -y langchain langchain-core langchain-community langchain-openai langchain-text-splitters langsmith langchain-ollama
pip list | grep langchain

pip install langchain==0.3.7   
pip install langchain-community
pip install langchain-ollama
pip install langgraph
pip3 install fastapi
pip3 install "uvicorn[standard]"

sudo apt purge python3-tk
#tkinter
sudo apt install python3.10-tk
 
(venv-agentic) hadoop@chandra-ThinkPad:~$ ollama pull llama3


#Run
python local_api.py
uvicorn local_api:app --port 9000

python local_agent_gui.py


# #

✅  Knowledge base
Your own offline database
Load documents, code, logs
Ask questions over your local data

✅  Memory
Save past conversations locally
Add vector storage (Chroma)
Let the agent "remember" data

✅  More local tools
File search agent
Log analyzer agent
PDF reader agent
System control agent

✅  Better GUI
PyQt5
Electron + Python
Streamlit local web app

✅ 5. Multi-agent system
One agent for search
One for analysis
One for actions


#

##

https://github.com/jim-schwoebel/awesome_ai_agents

Agentic AI Accelerator:
OpenAI
ollamma2

crewai==0.26.8 is not available for Python 3.9

sudo apt install python3.10 python3.10-venv python3.10-distutils python3.10-dev -y

##python3.10
# python3.10 -m venv /home/hadoop/venv-agentic
# source /home/hadoop/venv-agentic/bin/activate
# deactivate

pip install --upgrade pip setuptools

pip install -r /home/hadoop/1.tutorial/hadoop_working/5.0_DataScience/5.Generative-AI-chat-GPT/Agent/requirements.txt

pip show pydantic crewai langchain
pip uninstall crewai langchain -y
pip freeze | grep langchain


#🔑 Steps to Get Your OpenAI API Key
Go to the OpenAI platform:
https://platform.openai.com/

Log in to your OpenAI account.

Go to the API keys page:
👉 https://platform.openai.com/api-keys

Click the “+ Create new secret key” button.

python /home/hadoop/1.tutorial/hadoop_working/5.0_DataScience/5.Generative-AI-chat-GPT/Agent/agentic_accelerator.py


#hugging Face
Read and monitor logs (Python + watchdog)

#: Custom classification labels
You can fine-tune your own model with labels like:
FAIL_PAYMENT
FAIL_OTP
FAIL_CARD_ADD
SUCCESS
INFO

/home/hadoop/workspace/payment/payment.log

python /home/hadoop/1.tutorial/hadoop_working/5.0_DataScience/5.Generative-AI-chat-GPT/Agent/HuggingFace/log_agent.py

#test
echo "Payment failed due to insufficient balance" >> /home/hadoop/workspace/payment/payment.log

