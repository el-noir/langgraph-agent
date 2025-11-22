from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from agent.prompt import planner_prompt, architect_prompt, coder_system_prompt
from agent.state import Plan, TaskPlan
from agent.tools import read_file, write_file

load_dotenv()

# set_debug(True)
# set_verbose(True)

llm = ChatGroq(model="openai/gpt-oss-120b")

from pydantic import BaseModel
from typing import Optional

class GraphState(BaseModel):
    user_prompt: str
    plan: Optional[Plan] = None
    task_plan: Optional[dict] = None  # Add task_plan field to store architect output
    code: Optional[str] = None  # Add code field to store coder output
    coder_state: Optional[dict] = None  # Add coder_state to track coder progress
    status: Optional[str] = None  # Add status field for workflow control


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

    # Initialize or get coder_state
    if state.coder_state is None:
        # First time running - initialize with task plan
        task_plan_dict = state.task_plan
        if task_plan_dict is None:
            raise ValueError("coder_agent received no task_plan in state")

        coder_state_dict = {
            "current_step_idx": 0,
            "task_plan": task_plan_dict
        }
    else:
        coder_state_dict = state.coder_state

    # Get the steps from task_plan
    steps = coder_state_dict["task_plan"].get('implementation_steps', [])
    current_idx = coder_state_dict.get("current_step_idx", 0)

    # Check if we're done with all steps
    if current_idx >= len(steps):
        print(f"\n=== All {len(steps)} tasks completed ===")
        return {"status": "DONE"}

    current_task = steps[current_idx]
    print(f"\n--- Processing task {current_idx + 1}/{len(steps)}: {current_task['filepath']} ---")

    system_prompt = coder_system_prompt()

    # Read existing content using the tool directly
    existing_content = read_file.invoke({"path": current_task['filepath']})

    # Build a comprehensive prompt for direct code generation (avoiding tool calling size limits)
    use_prompt = f"""Task: {current_task['task_description']}

Filepath: {current_task['filepath']}

Existing content:
{existing_content if existing_content else '(empty file)'}

Instructions:
- Generate ONLY the complete file content, no explanations or markdown
- Make sure the code is complete, functional, and follows best practices
- Include all necessary imports, functions, styles, or markup
- If the file has existing content, enhance or complete it as needed

Generate the complete file content now:"""

    # Use direct LLM invocation to avoid Groq tool calling size limits
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=use_prompt)
    ]

    response = llm.invoke(messages)
    generated_code = response.content

    # Write the generated code directly using the write_file tool
    write_result = write_file.invoke({
        "path": current_task['filepath'],
        "content": generated_code
    })

    print(f"✓ Completed task for {current_task['filepath']}")
    print(f"  {write_result}")

    # Update coder state for next iteration
    coder_state_dict["current_step_idx"] = current_idx + 1

    return {"coder_state": coder_state_dict}

graph = StateGraph(GraphState)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

def should_continue(state: GraphState) -> str:
    """Decide whether to continue coding or end."""
    if state.status == "DONE":
        return "end"
    return "continue"

graph.add_conditional_edges(
    "coder",
    should_continue,
    {
        "continue": "coder",  # Loop back to coder for next task
        "end": END  # Finish the workflow
    }
)

graph.set_entry_point("planner")


if __name__ == "__main__":
    agent = graph.compile()
    result = agent.invoke(GraphState(user_prompt="create a calculator web application"))
    print(result)
