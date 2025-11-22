from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from prompt import *
from state import *
load_dotenv()

# Replace the decommissioned model with a supported one
llm = ChatGroq(model="llama-3.3-70b-versatile")

user_prompt = 'create a simple calculator web application'

prompt = planner_prompt(user_prompt)

response = llm.with_structured_output(Plan).invoke(prompt)

print(response)
