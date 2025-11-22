from pydantic import BaseModel, Field, ConfigDict


class File(BaseModel):
    path: str = Field(description="The path of the file to be created or modified")
    purpose: str = Field(
        description="The purpose of the file to be created or modified, e.g. 'main application logic', 'data processing module', etc."
    )


class Plan(BaseModel):
    name: str = Field(description="The name of the app to be built")
    description: str = Field(
        description="The online description of the app to be built, e.g. 'A web application for managing persons'.")
    techstack: str = Field(
        description="The tech stack to be used for the app, e.g. 'python', 'javascript', 'react', 'flask', etc.")
    features: list[str] = Field(
        description="A list of features that the app should have, e.g. 'user authentication', 'data visualization', etc."
    )
    files: list[File] = Field(description="A list of files to be created, each with a 'path' and 'purpose'.")

class ImplementationTask(BaseModel):
    filepath: str = Field(description="The path of the file to be created or modified")
    task_description: str = Field(
        description="A detailed description of the implementation task, including what to implement, variable and function names, dependencies, and integration details."
    )

class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(description="A list of implementation tasks derived from the project plan.")
    model_config = ConfigDict(extra="allow")
