import sys
from pathlib import Path

# Add parent directory to path to import from original modules
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from langchain_google_genai import ChatGoogleGenerativeAI
from graphs.preferences_graph import get_preferences_graph
from graphs.itinerary_graph import create_itinerary_graph
from utils.tools import tools
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class TripForgeChatAgent:
    """
    Streamlit-compatible wrapper for the TripForge LangGraph agent.
    Uses the original separate graphs with proper state management.
    """
    
    def __init__(self):
        """Initialize the chat agent with LLM and separate graphs"""
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.preferences_graph = get_preferences_graph(self.llm)
        self.itinerary_graph = create_itinerary_graph(self.llm.bind_tools(tools))
        self.agent_state = {}
        self.is_initialized = False
        self.current_phase = "preferences"
    
    def process_message(self, user_input: str) -> tuple[str, dict]:
        """
        Process a user message through the appropriate LangGraph workflow.
        
        Args:
            user_input: The user's message (empty string for initialization)
            
        Returns:
            tuple: (agent_response, updated_state)
        """
        try:
            # If we have user input, process it
            if user_input and user_input.strip():
                # Initialize the preferences graph if this is the first user input
                if not self.is_initialized:
                    # Start with preferences graph using the actual user input
                    result = self.preferences_graph.invoke({
                        'user_input': user_input,
                        'first_message': True
                    })
                    self.agent_state = result
                    self.is_initialized = True
                    self.current_phase = "preferences"
                    
                    # Return the llm_response from the graph
                    return self.agent_state.get('llm_response', 'Please tell me about your trip!'), self.agent_state
                
                # Continue with subsequent user input
                # Add user message to the agent state
                if 'messages' not in self.agent_state:
                    self.agent_state['messages'] = []
                
                self.agent_state['messages'].append(HumanMessage(content=user_input))
                self.agent_state['user_input'] = user_input
                
                if self.current_phase == "preferences":
                    # Set next_action to invoke_llm to continue processing
                    self.agent_state['next_action'] = 'invoke_llm'
                    
                    # Continue with preferences graph
                    result = self.preferences_graph.invoke(self.agent_state)
                    self.agent_state = result
                    
                    # Check if preferences are complete
                    if self.agent_state.get('preferences') and self.agent_state.get('next_action') == 'start_itinerary':
                        # Transition to itinerary phase
                        self.current_phase = "itinerary"
                        
                        # Start itinerary graph with preferences
                        self.agent_state['next_action'] = 'start'
                        itinerary_result = self.itinerary_graph.invoke(self.agent_state)
                        self.agent_state.update(itinerary_result)
                        
                        return self.agent_state.get('llm_response', 'Here is your itinerary!'), self.agent_state
                    
                    # Still in preferences phase
                    return self.agent_state.get('llm_response', 'Please tell me more.'), self.agent_state
                
                elif self.current_phase == "itinerary":
                    # Set next_action to invoke_llm to continue processing
                    self.agent_state['next_action'] = 'invoke_llm'
                    
                    # Continue with itinerary graph - user can ask further questions
                    result = self.itinerary_graph.invoke(self.agent_state, config={"recursion_limit": 100})
                    self.agent_state.update(result)
                    
                    # Return the response - no completion check, keep it open-ended
                    return self.agent_state.get('llm_response', 'How can I help you further?'), self.agent_state
            
            # If no input and already initialized, return current state response
            if self.is_initialized:
                return self.agent_state.get('llm_response', 'How can I help you?'), self.agent_state
            
            return "Please tell me about your trip!", self.agent_state
                
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try again.", self.agent_state
    
    @property 
    def current_phase_property(self) -> str:
        """Get current phase"""
        return self.current_phase
    
    def reset_conversation(self):
        """Reset the conversation state"""
        self.agent_state = {}
        self.is_initialized = False
        self.current_phase = "preferences"
