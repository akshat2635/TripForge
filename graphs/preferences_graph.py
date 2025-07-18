from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
import sys
from pathlib import Path

# Add parent directory to import original modules
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from utils.schema import AgentState
from utils.prompts import system_prompt_phase_1, initialize_prompt
from datetime import datetime


def get_preferences_graph(llm):
    """
    Modified preferences graph for Streamlit compatibility.
    Removes console I/O operations.
    """
    parser = JsonOutputParser()

    current_date = datetime.now()
    current_date_str = current_date.strftime('%Y-%m-%d')
    current_year = current_date.year
    
    def init_node(state: AgentState) -> AgentState:
        """Initialize the state for the preferences graph."""
        state['next_action'] = "start" if not state.get('next_action') else state['next_action']
        return state

    def start_node(state: AgentState) -> AgentState:
        """Initial state of the graph, setting up the conversation."""
        
        system_prompt = system_prompt_phase_1.invoke({
            "date": current_date_str,
            "day": current_date.strftime('%A')
        })
        
        # Check if this is first user message
        
        if state.get('first_message') and state.get('user_input'):
            # Initialize with system prompt and actual user input
            state['messages'] = [
                SystemMessage(content=system_prompt.text),
                HumanMessage(content=state['user_input']),
            ]
        else:
            # Original behavior for other cases
            initialize_message = initialize_prompt.invoke({
                "year": current_year
            })
            
            state['messages'] = [
                SystemMessage(content=system_prompt.text),
                HumanMessage(content=initialize_message.text),
            ]
        state['next_action'] = 'invoke_llm'
        state['llm_response'] = ''
        state['preferences'] = {}
        state['preferences_file'] = f"trip-preferences-{current_date.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        return state

    def invoke_llm(state: AgentState) -> AgentState:
        """Invoke the LLM to generate a response based on the current state."""
        response = llm.invoke(state['messages'])
        state['messages'].append(AIMessage(content=response.content))
        
        try:
            parsed_response = parser.parse(response.content)
            if parsed_response.get('state') == 'continue':
                state['next_action'] = 'user_input'
                state['llm_response'] = parsed_response.get('question', 'Tell me more about your trip.')
            elif parsed_response.get('state') == 'confirm':
                state['next_action'] = 'user_input'
                state['llm_response'] = parsed_response.get('question', 'Does this look good?')
            elif parsed_response.get('state') == 'end':
                state['next_action'] = 'start_itinerary'
                state['preferences_file'] = parsed_response.get('filename', state['preferences_file'])
                state['preferences'] = parsed_response.get('preferences', {})
        except Exception as e:
            state['next_action'] = 'user_input'
            state['llm_response'] = f"I encountered an issue processing your response: {str(e)}. Could you please try again?"
        
        return state

    def router(state: AgentState) -> str:
        return state['next_action']

    graph = StateGraph(AgentState)
    graph.add_node("init", init_node)
    graph.add_node("start", start_node)
    graph.add_node("invoke_llm", invoke_llm)

    graph.add_edge(START, "init")
    
    graph.add_conditional_edges("init", router, {
        "start": "start",
        "invoke_llm": "invoke_llm",
    })
    
    graph.add_edge("start", "invoke_llm")
    
    graph.add_edge("invoke_llm", END)
    
    preferences_graph = graph.compile()
    
    return preferences_graph

