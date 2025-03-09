import json
import uvicorn
import redis
from fastapi import FastAPI, Request
from src.graph.graph_builder import GraphBuilder
from src.llms.groq_llm import GroqLLM
from src.state.project_state import ProjectState
from langchain_core.messages import HumanMessage

app = FastAPI()

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

@app.post("/generate")
async def gnerate(request: Request):
    data = await request.json()
    usecase_name = data.get('usecase_name', '')
    action = data.get('action', 'start')
    thread_id = data.get('thread_id', 1)
    project_path = data.get('project_path', '') # Only needed for 'Continue'

    # get the llm object 
    llm = GroqLLM().get_llm()

    # get the Graph
    graph_builder = GraphBuilder(llm)
    graph = graph_builder.setup_graph()

    # Prepare thread context
    thread = {"configurable": {"thread_id": thread_id}}
   
    if action == "start":
        return await start_graph_execution(graph, thread, usecase_name, thread_id)   
    elif action == "resume":
        return await resume_graph_execution(graph, thread, thread_id, project_path)
    return {"error": "Invalid action"}


async def start_graph_execution(graph, thread, usecase_name, thread_id):
    """
    Starts the graph execution.

    Args:
        graph: The graph object.
        thread: The thread context.
        usecase_name: The name of the use case.
        thread_id: The ID of the thread.

    Returns:
        dict: The result of the graph execution.
    """
    initial_input = {"usecase_name": usecase_name}

    # Stream through graph events
    for event in graph.stream(initial_input, thread, stream_mode="values"):
        print(f"Event Received: {event}")

    # Check if we hit an interruption
    current_state = graph.get_state(thread)

    # If we are stuck at the 'human' node, we need to return the state for user input
    if "human" in current_state.next:
        # Save interrupted state in redis cache
        redis_client.set(f"state:{thread_id}", json.dumps(current_state))

        return {
            "status": "interrupted",
            "message": "User input required",
            "node": "human",
            "state": current_state
        }

    return {"status": "completed"}

async def resume_graph_execution(graph, thread, thread_id, project_path):
    """
    Resumes the graph execution from a saved state.

    Args:
        graph: The graph object.
        thread: The thread context.
        thread_id: The ID of the thread.
        project_path: The project path to be added to the state.

    Returns:
        dict: The result of the graph execution.
    """
    if not project_path:
        return {"error": "project_path is required to resume execution"}

    # saves the project_path in redis cache and returns the updated state
    new_dict = update_state_with_project_path(
        thread_id = thread_id, 
        project_path = project_path
    )

    # update the graph with thread
    graph.update_state(thread, new_dict, as_node="human")

    # Resume the graph
    for event in graph.stream(None, thread, stream_mode="values"):
        print(f"Event Received: {event}")
        state = event

    # clear from redis cache 
    redis_client.delete(f"state:{thread_id}")

    return {"status": "resumed", "data": state}


def update_state_with_project_path(thread_id: str, project_path: str):
    """
    Updates the saved state with the provided project path.

    Args:
        thread_id (str): The ID of the thread whose state needs to be updated.
        project_path (str): The project path to be added to the state.

    Returns:
        dict: The updated state dictionary or an error message if no state is found.
    """

    saved_state_json = redis_client.get(f"state:{thread_id}")
    if not saved_state_json:
        return {"error": f"No state found for thread ID {thread_id}"}

    # Load state from Redis
    saved_state = json.loads(saved_state_json)

    # Update the state with user input (project_path)
    # Check if any dictionary in saved_state already contains the key "project_path"
    key_present = any("project_path" in item for item in saved_state if isinstance(item, dict))

    if not key_present:
        # Append a new dictionary with the key-value pair
        saved_state.append({"project_path": project_path})

    # Initialize an empty dictionary to store the extracted values
    new_dict = {}

    # Loop through saved_state to find and merge dictionaries
    for item in saved_state:
        if isinstance(item, dict):
            new_dict.update(item)

    return new_dict


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)