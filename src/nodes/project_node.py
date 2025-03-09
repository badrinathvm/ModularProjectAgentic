from src.state.project_state import ProjectState
import os

class ProjectNode:

    def __init__(self, llm):
        self.llm = llm 

    def set_project_path(self, state: ProjectState):
        """
        Sets the project path and persists the usecase name in the state variable.
        """
        pass

    def create_project_structure(self, state: ProjectState):
        """
        Creates the project structure based on the use case name.
        """
        folder_name = state['usecase_name'] # 
        project_path = f"{state['project_path']}/{folder_name}"
        # Define structure
        structure = {
            "directories": [
                os.path.join(project_path, "src"),
                os.path.join(project_path, "src", "graph"),
                os.path.join(project_path, "src", "nodes"),
                os.path.join(project_path, "src", "tools"),
                os.path.join(project_path, "src", "state")
            ],
            "files": [
                {
                    "path": os.path.join(project_path, ".env"),
                    "content": "# Environemtn variables for the {} project\n\n# APIKeys"
                },
                {
                    "path": os.path.join(project_path, "README.md"),
                    "content": f"# {state['usecase_name']}\n\nThis project was generated using a LangGraph project structure generator.\n\n## Structure\n\n- `src/`: Source code\n  - `graphs/`: LangGraph graph definitions\n  - `nodes/`: Custom LangGraph nodes\n- `tools/`: Custom Tools\n - `state/`: Graph Satte \n`.env`: Environment variables configuration\n"
                },
                {
                    "path": os.path.join(project_path, "requirements.txt"),
                    "content": """
                            langchain
                            langgraph
                            langchain_community
                            langchain_core
                            langchain_groq
                            langchain_openai
                            fastapi
                            uvicorn
                            watchdog
                            youtube-transcript-api
                            huggingface_hub
                            transformers
                            langgraph-cli[inmem]
                            redis
                    """
                },
                {
                    "path": os.path.join(project_path, "src", "__init__.py"),
                    "content": ""
                },
                {
                    "path": os.path.join(project_path, "src", "graph", "__init__.py"),
                    "content": ""
                },
                {
                    "path": os.path.join(project_path, "src", "nodes", "__init__.py"),
                    "content": ""
                },
                {
                    "path": os.path.join(project_path, "src", "tools", "__init__.py"),
                    "content": ""
                },
                {
                    "path": os.path.join(project_path, "src", "state", "__init__.py"),
                    "content": ""
                }
            ]
        }

        created_paths = []

        # created directories
        for directory in structure["directories"]:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True) 
                created_paths.append(f"created directory: {directory}")

        for file_info in structure["files"]:
            path = file_info["path"]
            content = file_info["content"]

            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write(content)
                created_paths.append(f"Created file: {path}")

        # Generate structure summary
        structure_summary = f"""
        
        Structure:
        {folder_name}/
        ├── .env
        ├── README.md
        ├── requirements.txt
        └── src/
            ├── __init__.py
            ├── graphs/
            │   └── __init__.py
            └── nodes/
            │    └── __init__.py
            └── state/
            │    └── __init__.py
            │    
            └── tools/
                └── __init__.py
        """
        return {
            "usecase_name": folder_name, 
            "created_paths": created_paths, 
            "structure_summary": structure_summary
        }
