from typing import NotRequired, TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ProjectState(TypedDict):
    usecase_name: str
    project_path: NotRequired[str]
    created_paths: NotRequired[list[str]]
    structure_summary: NotRequired[str]
