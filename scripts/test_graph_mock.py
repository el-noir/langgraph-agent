# Small test harness that patches agent.graph.llm with a mock LLM to exercise planner and architect nodes
from agent import graph as g
from agent.state import Plan, TaskPlan, ImplementationTask, File

class MockInvoker:
    def __init__(self, model):
        self.model = model

    def invoke(self, prompt):
        # Return deterministic instances depending on requested model
        if self.model is Plan:
            return Plan(
                name="Mocked Simple Calculator Web Application",
                description="A mocked plan for calculator",
                techstack="javascript, html, css",
                features=["addition", "subtraction", "multiplication", "division"],
                files=[
                    File(path="index.html", purpose="main page"),
                    File(path="script.js", purpose="logic"),
                    File(path="style.css", purpose="styles"),
                ],
            )
        if self.model is TaskPlan:
            task = ImplementationTask(filepath="script.js", task_description="Implement calculator logic")
            return TaskPlan(implementation_steps=[task])
        # Fallback: return None
        return None

class MockLLM:
    def with_structured_output(self, model):
        return MockInvoker(model)

# Patch the module-level llm
g.llm = MockLLM()

if __name__ == '__main__':
    agent = g.graph.compile()
    result = agent.invoke(g.GraphState(user_prompt="create a simple calculator web application"))
    print("Mock run result:\n", result)

