from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

load_dotenv()

# Replace the decommissioned model with a supported one
llm = ChatGroq(model="llama-3.3-70b-versatile")

user_prompt = 'create a simple calculator web application'

prompt = f"""
    You are a Planner agent, Convert the user prompt into a complete engineering project plan

    User request: {user_prompt}
"""

class File(BaseModel):
    path: str = Field(description="The path of the file to be created or modified")
    purpose: str = Field(
        description="The purpose of the file to be created or modified, e.g. 'main application logic', 'data processing module', etc."
    )


class Schema(BaseModel):
    name: str = Field(description="The name of the app to be built")
    description: str = Field(
        description="The online description of the app to be built, e.g. 'A web application for managing persons'.")
    techstack: str = Field(
        description="The tech stack to be used for the app, e.g. 'python', 'javascript', 'react', 'flask', etc.")
    features: list[str] = Field(
        description="A list of features that the app should have, e.g. 'user authentication', 'data visualization', etc."
    )
    files: list[File] = Field(description="A list of files to be created, each with a 'path' and 'purpose'.")


response = llm.with_structured_output(Schema).invoke(prompt)

print(response)
