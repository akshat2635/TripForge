from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
import sys
from datetime import datetime
from pathlib import Path
import json

# Add parent directory to import original modules
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from utils.schema import AgentState
from utils.prompts import system_prompt_phase_2, itinerary_prompt
from utils.tools import  tools_dict
from dotenv import load_dotenv

load_dotenv()

def create_itinerary_graph(llm) -> StateGraph:
    """
    Modified itinerary graph for Streamlit compatibility.
    Removes console I/O operations.
    """
    
    def init_node(state: AgentState) -> AgentState:
        state['next_action'] = "start" if not state.get('next_action') else state['next_action']
        return state

    def start_itinerary(state: AgentState) -> AgentState:
        """Start the itinerary creation process."""
        # Use preferences from the state passed from the main graph
        preferences = state.get('preferences', {})
        
        system_prompt = system_prompt_phase_2.invoke({
            "preferences": json.dumps(preferences, indent=2)
        })
        
        state['messages'] = [SystemMessage(content=system_prompt.text)]
        
        prompt = itinerary_prompt.invoke({
            "preferences": json.dumps(preferences, indent=2)
        }) 
        state['messages'].append(HumanMessage(content=prompt.text))
        state['next_action'] = 'invoke_llm'
        state['llm_response'] = ''
        state['itinerary'] = ''
        state['itinerary_file'] = f"trip-itinerary-{preferences.get('departure_city', 'unknown')}-{preferences.get('arrival_city', 'unknown')}-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        return state

    def invoke_llm(state: AgentState) -> AgentState:
        """Invoke the LLM to generate the itinerary based on the preferences."""
        response = llm.invoke(state['messages'])
        state['messages'].append(response)
        
        try: 
            if hasattr(response, 'tool_calls') and response.tool_calls:
                state['next_action'] = "tool_node"
            else:
                state['next_action'] = 'user_input'
                state['itinerary'] = response.content
                state['llm_response'] = response.content
        except Exception as e:
            state['next_action'] = 'user_input'
            state['llm_response'] = f"I encountered an issue processing your request: {str(e)}. Could you please rephrase or provide more details?"
        
        return state


    def tool_node(state: AgentState) -> AgentState:
        """Execute tool calls from the LLM's response."""
        # Set a processing message
        state['llm_response'] = "Let me gather some additional information for you..."

        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            if t['name'] not in tools_dict:
                result = f"Tool not available: {t['name']}. Available tools: {list(tools_dict.keys())}"
            else:
                try:
                    result = tools_dict[t['name']].func(**t['args'])
                except Exception as e:
                    result = f"Error executing tool {t['name']}: {str(e)}"

            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

        state['messages'].extend(results)
        state['next_action'] = 'invoke_llm'
        return state

    def router(state: AgentState) -> str:
        return state['next_action']

    graph = StateGraph(AgentState)
    
    graph.add_node("init", init_node)
    graph.add_node("start_itinerary", start_itinerary)
    graph.add_node("invoke_llm", invoke_llm)
    graph.add_node("tool_node", tool_node)

    graph.add_edge(START, "init")
    graph.add_edge("start_itinerary", "invoke_llm")
    graph.add_edge("tool_node", "invoke_llm")
    
    graph.add_conditional_edges("init", router, {
        "start": "start_itinerary",
        "invoke_llm": "invoke_llm",
        "user_input": END
    })
    
    graph.add_conditional_edges("invoke_llm", router, {
        "tool_node": "tool_node",
        "user_input": END
    })

    app = graph.compile()

    return app
