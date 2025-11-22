from dotenv import load_dotenv
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from agent.prompt import planner_prompt
from agent.state import Plan  # explicit import

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile")

from pydantic import BaseModel
from typing import Optional

class GraphState(BaseModel):
    user_prompt: str
    plan: Optional[Plan] = None

def planner_agent(state: GraphState) -> dict:
    response: Plan = llm.with_structured_output(Plan).invoke(planner_prompt(state.user_prompt))
    print("planner_agent got response:", repr(response))
    print("response type:", type(response))
    return {"plan": response.dict()}

graph = StateGraph(GraphState)
graph.add_node("planner", planner_agent)
graph.set_entry_point("planner")

if __name__ == "__main__":
    agent = graph.compile()
    result = agent.invoke(GraphState(user_prompt="create a simple calculator web application"))
    print(result)
