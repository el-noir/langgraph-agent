from dotenv import  load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

llm = ChatGroq(model="openai/gpt-oss-120b")

response = llm.invoke("How are you?")

print(response.content)