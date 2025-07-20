import streamlit as st
import sys
import json
from datetime import datetime
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from core.chat_agent import TripForgeChatAgent

# Page configuration
st.set_page_config(
    page_title="TripForge - AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load external CSS file
def load_css():
    """Load external CSS file for styling"""
    css_file_path = Path(__file__).parent / "static" / "styles.css"
    try:
        with open(css_file_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("CSS file not found. Please ensure static/styles.css exists.")
    except Exception as e:
        st.error(f"Error loading CSS: {str(e)}")

# Load the external CSS
load_css()

def initialize_session():
    """Initialize session state variables"""
    if 'chat_agent' not in st.session_state:
        st.session_state.chat_agent = TripForgeChatAgent()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'agent_state' not in st.session_state:
        st.session_state.agent_state = {}
    
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False


def create_sidebar():
    """Create a narrow sidebar with essential features"""
    with st.sidebar:
        st.markdown("### 🛠️ Tools")
        
        # New Chat Button
        if st.button("🔄 New Chat", use_container_width=True, help="Start a new conversation"):
            # Reset the chat agent
            st.session_state.chat_agent.reset_conversation()
            
            # Clear session state
            st.session_state.chat_history = []
            st.session_state.agent_state = {}
            st.session_state.initialized = False
            st.rerun()
        
        st.markdown("---")
        
        # Download Itinerary Button
        itinerary_content = generate_itinerary_file()
        if itinerary_content:
            st.download_button(
                label="📄📥 Download Itinerary",
                data=itinerary_content,
                file_name=f"tripforge_itinerary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
                help="Download your travel itinerary"
            )
        else:
            st.button("📄📥 Download Itinerary", use_container_width=True, disabled=True, help="No itinerary available. Please complete your trip planning first.")
        
        # Download Preferences Button
        preferences_content = generate_preferences_file()
        if preferences_content:
            st.download_button(
                label="📋📥 Download Preferences",
                data=preferences_content,
                file_name=f"tripforge_preferences_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
                help="Download your travel preferences"
            )
        else:
            st.button("📋📥 Download Preferences", use_container_width=True, disabled=True, help="No preferences available. Please start planning your trip first.")
        
        st.markdown("---")
        
        # Export Chat History
        chat_content = generate_chat_export()
        if chat_content:
            st.download_button(
                label="💬📥 Export Chat",
                data=chat_content,
                file_name=f"tripforge_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
                help="Export your conversation"
            )
        else:
            st.button("💬📥 Export Chat", use_container_width=True, disabled=True, help="No chat history to export.")

def generate_itinerary_file():
    """Generate downloadable itinerary file in formatted text"""
    if hasattr(st.session_state, 'agent_state') and st.session_state.agent_state:
        itinerary = st.session_state.agent_state.get('itinerary', '')
        preferences = st.session_state.agent_state.get('preferences', {})
        
        if itinerary:
            # Create formatted text content
            content = "🌍 TRIPFORGE TRAVEL ITINERARY\n"
            content += "=" * 50 + "\n\n"
            content += f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n"
            
            # Add preferences summary if available
            if preferences:
                content += "📋 TRIP PREFERENCES:\n"
                content += "-" * 25 + "\n"
                for key, value in preferences.items():
                    if value:
                        # Format key names to be more readable
                        formatted_key = key.replace('_', ' ').title()
                        if isinstance(value, list):
                            content += f"{formatted_key}: {', '.join(value)}\n"
                        else:
                            content += f"{formatted_key}: {value}\n"
                content += "\n"
            
            # Add the main itinerary
            content += "🗓️ DETAILED ITINERARY:\n"
            content += "-" * 25 + "\n"
            content += itinerary
            
            # Add footer
            content += "\n\n" + "=" * 50 + "\n"
            content += "Generated by TripForge AI Travel Assistant\n"
            content += "Visit us at: https://tripforge.ai\n"
            
            return content
    
    return None

def generate_preferences_file():
    """Generate downloadable preferences file"""
    if hasattr(st.session_state, 'agent_state') and st.session_state.agent_state:
        preferences_data = {
            "tripforge_export": {
                "type": "preferences",
                "generated_at": datetime.now().isoformat(),
                "preferences": st.session_state.agent_state.get('preferences', {}),
                "version": "1.0"
            }
        }
        
        if preferences_data["tripforge_export"]["preferences"]:
            return json.dumps(preferences_data, indent=2, ensure_ascii=False)
    
    return None

def generate_chat_export():
    """Generate downloadable chat history"""
    if st.session_state.chat_history:
        chat_content = f"TripForge Chat Export\n"
        chat_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        chat_content += "=" * 50 + "\n\n"
        
        for i, message in enumerate(st.session_state.chat_history, 1):
            role = "You" if message['role'] == 'user' else "TripForge AI"
            chat_content += f"[{i:03d}] {role}:\n"
            chat_content += f"{message['content']}\n\n"
            chat_content += "-" * 30 + "\n\n"
        
        return chat_content
    
    return None

def display_chat_history():
    """Display the chat history with user bubbles on right and assistant markdown on left"""
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            # User message in bubble on the right
            st.markdown(f"""
            <div class="user-message-container">
                <div class="user-message">
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Assistant message as plain markdown on the left
            st.markdown(f"""
            <div class="assistant-message-container">
                <div class="assistant-message">
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

def handle_user_input():
    """Handle user input and get agent response"""
    # Chat input at the bottom
    user_input = st.chat_input("Type your message here...", key="user_input")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({
            'role': 'user', 
            'content': user_input
        })
        
        # Get agent response
        try:
            response, updated_state = st.session_state.chat_agent.process_message(user_input)
            
            # Update agent state
            st.session_state.agent_state = updated_state
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({
                'role': 'assistant', 
                'content': response
            })
            
            # Rerun to update the display
            st.rerun()
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}. Please try again."
            st.session_state.chat_history.append({
                'role': 'assistant', 
                'content': error_msg
            })
            st.rerun()

def main():
    """Main application function"""
    # Initialize session
    initialize_session()
    
    # Create sidebar with tools
    create_sidebar()
    
    # Add TripForge logo at the top of chat container
    st.markdown("""
    <div class="chat-header">
        <h1 class="tripforge-logo">🌍 TripForge</h1>
        <p class="tripforge-subtitle">AI Travel Planning Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show welcome message only if no chat history (startup state)
    if len(st.session_state.chat_history) == 0:
        st.markdown("""
        <div class="assistant-message">
            👋 Hey there! I'm TripForge, your AI travel planning assistant. Ready to plan your perfect trip?
        </div>
        """, unsafe_allow_html=True)
    
    # Mark as initialized without auto-starting
    if not st.session_state.initialized:
        st.session_state.initialized = True
    
    # Display chat history
    display_chat_history()
    
    # Handle user input (always at the bottom)
    handle_user_input()

if __name__ == "__main__":
    main()
