from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from agent.prompt import planner_prompt, architect_prompt
from agent.state import Plan, TaskPlan

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile")

from pydantic import BaseModel
from typing import Optional

class GraphState(BaseModel):
    user_prompt: str
    plan: Optional[Plan] = None
    task_plan: Optional[dict] = None  # Add task_plan field to store architect output

def planner_agent(state: GraphState) -> dict:
    response: Plan = llm.with_structured_output(Plan).invoke(planner_prompt(state.user_prompt))
    print("planner_agent got response:", repr(response))
    print("response type:", type(response))
    return {"plan": response.model_dump()}

def architect_agent(state: GraphState) -> dict:
    print("architect_agent starting...")
    plan_value = state.plan
    if plan_value is None:
        raise ValueError("architect_agent received no plan in state")
    if isinstance(plan_value, dict):
        plan_obj = Plan.model_validate(plan_value)
    else:
        plan_obj = plan_value

    response: TaskPlan = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan_obj.model_dump()))
    print("architect_agent got response:", repr(response))
    print("response type:", type(response))
    if response is None:
        raise ValueError("architect_agent received no response from LLM")

    task_plan_dict = response.model_dump()
    task_plan_dict["plan"] = plan_obj.model_dump()
    print("architect_agent returning task_plan with", len(task_plan_dict.get('implementation_steps', [])), "steps")
    return {"task_plan": task_plan_dict}


graph = StateGraph(GraphState)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_edge("planner", "architect")
graph.add_edge("architect", END)
graph.set_entry_point("planner")
if __name__ == "__main__":
    agent = graph.compile()
    result = agent.invoke(GraphState(user_prompt="create a simple calculator web application"))
    print(result)
