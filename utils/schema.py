from typing import TypedDict, Annotated, List, Dict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_input: str
    first_message: bool
    next_action: str
    llm_response: str
    preferences: Dict[str, str]
    preferences_file: str
    itinerary_file: str
    itinerary: str