from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from agent.prompt import planner_prompt, architect_prompt, coder_system_prompt
from agent.state import Plan, TaskPlan

load_dotenv()

# set_debug(True)
# set_verbose(True)

llm = ChatGroq(model="llama-3.3-70b-versatile")

from pydantic import BaseModel
from typing import Optional

class GraphState(BaseModel):
    user_prompt: str
    plan: Optional[Plan] = None
    task_plan: Optional[dict] = None  # Add task_plan field to store architect output
    code: Optional[str] = None  # Add code field to store coder output


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

def coder_agent(state: GraphState) -> dict:
    print("coder_agent starting...")
    task_plan_dict = state.task_plan
    if task_plan_dict is None:
        raise ValueError("coder_agent received no task_plan in state")

    steps = task_plan_dict.get('implementation_steps', [])
    if not steps:
        raise ValueError("coder_agent received empty implementation_steps")

    current_step_idx = 0
    current_task = steps[current_step_idx]

    use_prompt = f"Task: {current_task['task_description']}\nFile: {current_task['filepath']}"

    system_prompt = coder_system_prompt()
    # response = llm.invoke(system_prompt + "\n" + use_prompt)
    # print(f"coder_agent generated code for {current_task['filepath']}")

    coder_tools = ["read_file", "write_file", "list_files", "get_current_directory"]
    react_agent = create_react_agent(llm, coder_tools)
    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                       {"role": "user", "content": use_prompt}]})


    return {}

graph = StateGraph(GraphState)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_edge("planner", "architect")
graph.add_node("coder", coder_agent)
graph.add_edge("architect", "coder")
graph.add_edge("coder", END)
graph.set_entry_point("planner")


if __name__ == "__main__":
    agent = graph.compile()
    result = agent.invoke(GraphState(user_prompt="create a simple calculator web application"))
    print(result)
