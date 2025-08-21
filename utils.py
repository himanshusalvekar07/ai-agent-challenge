"""
Utility functions for Karbon AI Agent
"""
import json
import base64
import streamlit as st
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd

def export_chat_history(chat_history: List[Dict], agent_type: str) -> str:
    """Export chat history as JSON"""
    export_data = {
        "export_timestamp": datetime.now().isoformat(),
        "agent_type": agent_type,
        "total_messages": len(chat_history),
        "chat_history": chat_history
    }
    
    return json.dumps(export_data, indent=2)

def create_download_link(data: str, filename: str, link_text: str) -> str:
    """Create a download link for data"""
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def format_timestamp(timestamp: str = None) -> str:
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return timestamp

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def validate_api_key(api_key: str) -> bool:
    """Validate Groq API key format"""
    if not api_key:
        return False
    if len(api_key) < 10:
        return False
    return True

def get_conversation_summary(chat_history: List[Dict]) -> Dict[str, Any]:
    """Get summary statistics of conversation"""
    if not chat_history:
        return {
            "total_messages": 0,
            "user_messages": 0,
            "agent_messages": 0,
            "first_message_time": None,
            "last_message_time": None,
            "average_message_length": 0
        }
    
    user_messages = [msg for msg in chat_history if msg["role"] == "user"]
    agent_messages = [msg for msg in chat_history if msg["role"] == "assistant"]
    
    message_lengths = [len(msg["content"]) for msg in chat_history]
    avg_length = sum(message_lengths) / len(message_lengths) if message_lengths else 0
    
    timestamps = [msg.get("timestamp") for msg in chat_history if msg.get("timestamp")]
    
    return {
        "total_messages": len(chat_history),
        "user_messages": len(user_messages),
        "agent_messages": len(agent_messages),
        "first_message_time": min(timestamps) if timestamps else None,
        "last_message_time": max(timestamps) if timestamps else None,
        "average_message_length": round(avg_length, 2)
    }

def create_agent_card(agent_name: str, config: Dict) -> str:
    """Create HTML card for agent display"""
    return f"""
    <div class="agent-card">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 24px; margin-right: 10px;">{config['icon']}</span>
            <h3 style="margin: 0;">{agent_name}</h3>
        </div>
        <p style="margin: 5px 0; color: #666;">{config['description']}</p>
        <small style="color: #888;"><strong>Model:</strong> {config.get('model', 'mixtral-8x7b-32768')}</small>
    </div>
    """

def format_code_block(code: str, language: str = "") -> str:
    """Format code block for display"""
    return f"```{language}\n{code}\n```"

def extract_code_from_response(response: str) -> List[Dict]:
    """Extract code blocks from AI response"""
    import re
    
    code_blocks = []
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, response, re.DOTALL)
    
    for i, (language, code) in enumerate(matches):
        code_blocks.append({
            "id": i,
            "language": language or "text",
            "code": code.strip()
        })
    
    return code_blocks

class SessionManager:
    """Manage Streamlit session state"""
    
    @staticmethod
    def initialize_session():
        """Initialize session state variables"""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        if "selected_agent" not in st.session_state:
            st.session_state.selected_agent = "General Assistant"
        
        if "conversation_count" not in st.session_state:
            st.session_state.conversation_count = 0
        
        if "total_tokens_used" not in st.session_state:
            st.session_state.total_tokens_used = 0
    
    @staticmethod
    def add_message(role: str, content: str, timestamp: str = None):
        """Add message to chat history"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
        
        st.session_state.chat_history.append(message)
        
        if role == "user":
            st.session_state.conversation_count += 1
    
    @staticmethod
    def clear_history():
        """Clear chat history"""
        st.session_state.chat_history = []
        st.session_state.conversation_count = 0
    
    @staticmethod
    def get_recent_messages(count: int = 10) -> List[Dict]:
        """Get recent messages from history"""
        return st.session_state.chat_history[-count:] if st.session_state.chat_history else []