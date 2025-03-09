from langgraph.graph import StateGraph, START, END
from src.llms.groq_llm import GroqLLM
from src.nodes.project_node import ProjectNode
from src.state.project_state import ProjectState
from langgraph.checkpoint.memory import MemorySaver

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.builder = StateGraph(ProjectState)
        self.memory = MemorySaver()

    def build_graph(self):
        self.project_node = ProjectNode(self.llm)

        # Nodes
        self.builder.add_node("human", self.project_node.set_project_path)
        self.builder.add_node("create_project_folder", self.project_node.create_project_structure)
               
        # Edges 
        self.builder.add_edge(START, "human")
        self.builder.add_edge("human", "create_project_folder")
        self.builder.add_edge("create_project_folder", END)

        return self.builder
    
    def setup_graph(self):
        self.build_graph()
        return self.builder.compile(interrupt_before=["human"],checkpointer=self.memory)
    
# Add nodes 
# ask user to enter the keys in the env file? 
# ask user to generate the langsmith debiug file?
    
# Below code is to debug langsmith
llm = GroqLLM().get_llm()
graph_builder = GraphBuilder(llm)
project_agent = graph_builder.build_graph().compile(checkpointer=MemorySaver())