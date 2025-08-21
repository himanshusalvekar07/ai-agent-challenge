import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import json
from datetime import datetime
import pandas as pd
import time
from typing import List, Dict, Any
import base64

# Import configuration
try:
    from config import (
        AVAILABLE_MODELS, AGENT_TYPES, APP_TITLE, APP_ICON, 
        ERROR_MESSAGES, SUCCESS_MESSAGES, get_model_info, 
        validate_config, GROQ_API_KEY
    )
except ImportError:
    st.error("❌ Could not import config.py. Make sure config.py is in the same directory as app.py")
    st.stop()

# Load environment variables
load_dotenv()

# Validate configuration
if not validate_config():
    st.stop()

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .agent-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .agent-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .status-online {
        color: #4caf50;
        font-weight: bold;
    }
    
    .status-offline {
        color: #f44336;
        font-weight: bold;
    }
    
    .model-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #667eea;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client with proper error handling
@st.cache_resource
def init_groq_client():
    if not GROQ_API_KEY:
        st.error(ERROR_MESSAGES["api_key_missing"])
        st.info("💡 Make sure your .env file is in the same directory and contains: GROQ_API_KEY=your_api_key_here")
        st.stop()
    
    try:
        # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY)
        
        # Test connection with fastest available model
        test_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=1
        )
        
        st.success(SUCCESS_MESSAGES["connection_established"])
        return client
        
    except Exception as e:
        st.error(f"❌ Failed to initialize Groq client: {str(e)}")
        st.info("💡 Try the following solutions:")
        st.info("1. Update the Groq library: `pip install --upgrade groq`")
        st.info("2. Check if your API key is valid at https://console.groq.com/")
        st.info("3. Verify your internet connection")
        st.stop()

class KarbonAgent:
    def __init__(self, client: Groq):
        self.client = client
        self.conversation_history = []
        
    def get_response(self, message: str, agent_type: str, model: str = None, temperature: float = None) -> str:
        """Get response from Groq API with improved error handling"""
        try:
            config = AGENT_TYPES[agent_type]
            
            # Use provided model or default from config
            selected_model = model or config["model"]
            selected_temperature = temperature if temperature is not None else config.get("temperature", 0.7)
            max_tokens = config.get("max_tokens", 1024)
            
            messages = [
                {"role": "system", "content": config["system_prompt"]}
            ]
            
            # Add conversation history (last 10 messages to manage context length)
            messages.extend(self.conversation_history[-10:])
            messages.append({"role": "user", "content": message})
            
            with st.spinner(f"🤔 {agent_type} is thinking..."):
                response = self.client.chat.completions.create(
                    model=selected_model,
                    messages=messages,
                    temperature=selected_temperature,
                    max_tokens=max_tokens,
                    top_p=1,
                    stream=False
                )
            
            ai_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": ai_response}
            ])
            
            return ai_response
            
        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ Error getting response: {error_msg}")
            
            # Provide specific error guidance using config
            if "rate_limit" in error_msg.lower():
                return ERROR_MESSAGES["rate_limit"]
            elif "api_key" in error_msg.lower():
                return "⚠️ API key issue. Please check your Groq API key configuration."
            elif "model" in error_msg.lower():
                return ERROR_MESSAGES["model_error"]
            else:
                return f"{ERROR_MESSAGES['general_error']} Details: {error_msg}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

def test_groq_connection(client, model):
    """Test Groq API connection"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        return True, "Connection successful"
    except Exception as e:
        return False, str(e)

def main():
    # Initialize session state
    if "groq_client" not in st.session_state:
        st.session_state.groq_client = init_groq_client()
    
    if "agent" not in st.session_state:
        st.session_state.agent = KarbonAgent(st.session_state.groq_client)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "selected_agent" not in st.session_state:
        st.session_state.selected_agent = "General Assistant"
    
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None

    # Main header
    st.markdown(f"""
    <div class="main-header">
        <h1>{APP_ICON} {APP_TITLE}</h1>
        <p>Advanced AI Agent System powered by Groq API</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        st.header("🛠️ Agent Configuration")
        
        # Agent selection
        selected_agent = st.selectbox(
            "Select Agent Type:",
            list(AGENT_TYPES.keys()),
            index=list(AGENT_TYPES.keys()).index(st.session_state.selected_agent)
        )
        
        if selected_agent != st.session_state.selected_agent:
            st.session_state.selected_agent = selected_agent
            st.session_state.selected_model = None  # Reset model selection
            st.rerun()
        
        # Display agent info
        config = AGENT_TYPES[selected_agent]
        st.markdown(f"""
        <div class="agent-card">
            <h3>{config['icon']} {selected_agent}</h3>
            <p>{config['description']}</p>
            <small><strong>Default Model:</strong> {config['model']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Model parameters
        st.subheader("⚙️ Model Parameters")
        
        # Model selection
        available_models = list(AVAILABLE_MODELS.keys())
        default_model = config["model"]
        current_model = st.session_state.selected_model or default_model
        
        selected_model = st.selectbox(
            "Select Model:",
            available_models,
            index=available_models.index(current_model) if current_model in available_models else 0,
            help="Choose the AI model for this agent"
        )
        
        # Update session state
        st.session_state.selected_model = selected_model
        
        # Display model info
        model_info = get_model_info(selected_model)
        if "error" not in model_info:
            st.markdown(f"""
            <div class="model-info">
                <strong>📋 {model_info['name']}</strong><br>
                <small>by {model_info['developer']}</small><br><br>
                📝 {model_info['description']}<br><br>
                🔧 <strong>Context:</strong> {model_info['context']:,} tokens<br>
                📤 <strong>Max output:</strong> {model_info['max_tokens']:,} tokens<br>
                💡 <strong>Best for:</strong> {', '.join(model_info['recommended_for'])}
            </div>
            """, unsafe_allow_html=True)
            
            # Show warning for preview models
            if "warning" in model_info:
                st.markdown(f"""
                <div class="warning-box">
                    ⚠️ <strong>Warning:</strong> {model_info['warning']}
                </div>
                """, unsafe_allow_html=True)
        
        # Temperature slider with agent-specific defaults
        default_temp = config.get("temperature", 0.7)
        temperature = st.slider(
            "Temperature", 
            0.0, 2.0, 
            default_temp, 
            0.1,
            help="Higher values make output more random, lower values more focused"
        )
        
        # Agent status
        st.subheader("📡 Agent Status")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Test", use_container_width=True):
                with st.spinner("Testing..."):
                    is_connected, status_msg = test_groq_connection(
                        st.session_state.groq_client, 
                        selected_model
                    )
                    if is_connected:
                        st.success("🟢 Online")
                    else:
                        st.error("🔴 Failed")
                        st.caption(status_msg)
        
        with col2:
            # Show current status
            try:
                # Quick status check
                test_response = st.session_state.groq_client.chat.completions.create(
                    model=selected_model,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
                st.markdown('<p class="status-online">🟢 Ready</p>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown('<p class="status-offline">🔴 Error</p>', unsafe_allow_html=True)
        
        # Conversation controls
        st.subheader("🎛️ Conversation Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.agent.clear_history()
                st.session_state.chat_history = []
                st.success("✅ Cleared!")
                st.rerun()
        
        with col2:
            if st.session_state.chat_history and st.button("📄 Export", use_container_width=True):
                chat_data = {
                    "timestamp": datetime.now().isoformat(),
                    "agent_type": selected_agent,
                    "model": selected_model,
                    "temperature": temperature,
                    "chat_history": st.session_state.chat_history
                }
                
                json_string = json.dumps(chat_data, indent=2)
                b64 = base64.b64encode(json_string.encode()).decode()
                href = f'<a href="data:application/json;base64,{b64}" download="karbon_chat_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json">📥 Download</a>'
                st.markdown(href, unsafe_allow_html=True)

    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"💬 Chat with {config['icon']} {selected_agent}")
        
        # Model indicator
        model_name = get_model_info(selected_model).get('name', selected_model)
        st.caption(f"Using: {model_name} (Temperature: {temperature})")
        
        # Display welcome message if no chat history
        if not st.session_state.chat_history:
            st.info(f"👋 Hi! I'm your {selected_agent}. {config['description']}. How can I help you today?")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for chat in st.session_state.chat_history:
                if chat["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>👤 You:</strong><br>
                        {chat["content"]}
                        <br><small>📅 {chat.get("timestamp", "")}</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message agent-message">
                        <strong>{config['icon']} {selected_agent}:</strong><br>
                        {chat["content"]}
                        <br><small>📅 {chat.get("timestamp", "")}</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Your message:",
                placeholder=f"Ask {selected_agent} anything...",
                height=100,
                key="user_input"
            )
            
            col_send, col_example = st.columns([1, 1])
            
            with col_send:
                send_button = st.form_submit_button("🚀 Send", use_container_width=True)
            
            with col_example:
                example_button = st.form_submit_button("💡 Example", use_container_width=True)
        
        # Handle example button
        if example_button:
            examples = {
                "Code Assistant": "Can you help me optimize this Python function for better performance?",
                "Research Analyst": "What are the current trends in artificial intelligence adoption?",
                "Creative Writer": "Help me write a short story about time travel.",
                "General Assistant": "Explain the concept of quantum computing in simple terms."
            }
            user_input = examples[selected_agent]
            send_button = True
        
        # Process user input
        if send_button and user_input and user_input.strip():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": timestamp
            })
            
            # Get AI response
            ai_response = st.session_state.agent.get_response(
                user_input, 
                selected_agent,
                selected_model,
                temperature
            )
            
            # Add AI response to history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": timestamp,
                "model": selected_model,
                "temperature": temperature
            })
            
            st.rerun()
    
    with col2:
        st.subheader("📊 Statistics")
        
        # Chat statistics
        total_messages = len(st.session_state.chat_history)
        user_messages = len([msg for msg in st.session_state.chat_history if msg["role"] == "user"])
        agent_messages = len([msg for msg in st.session_state.chat_history if msg["role"] == "assistant"])
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_messages}</h3>
            <p>Total Messages</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>{user_messages}</h3>
            <p>Your Messages</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>{agent_messages}</h3>
            <p>Agent Responses</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        quick_actions = {
            "📝 Code Review": "Please review this code and suggest improvements:",
            "🧠 Explain Concept": "Can you explain the following concept in detail:",
            "🔧 Problem Solving": "Help me solve this problem step by step:",
            "💡 Creative Ideas": "Give me creative ideas for:",
        }
        
        for action, prompt in quick_actions.items():
            if st.button(action, use_container_width=True, key=f"quick_{action}"):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Add quick action to chat
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": prompt,
                    "timestamp": timestamp
                })
                
                # Get AI response
                ai_response = st.session_state.agent.get_response(
                    prompt, 
                    selected_agent,
                    selected_model,
                    temperature
                )
                
                # Add AI response to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": ai_response,
                    "timestamp": timestamp,
                    "model": selected_model,
                    "temperature": temperature
                })
                
                st.rerun()
        
        # Recent topics
        if st.session_state.chat_history:
            st.subheader("📝 Recent Topics")
            recent_topics = [
                msg["content"][:40] + "..." if len(msg["content"]) > 40 else msg["content"]
                for msg in st.session_state.chat_history[-5:]
                if msg["role"] == "user"
            ]
            
            for i, topic in enumerate(recent_topics):
                st.caption(f"{i+1}. {topic}")

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption("**Karbon AI Agent**")
    
    with col2:
        st.caption("Powered by Groq API")
    
    with col3:
        st.caption("Built with ❤️ using Streamlit")

if __name__ == "__main__":
    main()