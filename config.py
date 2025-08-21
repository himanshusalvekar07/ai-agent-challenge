"""
Configuration settings for Karbon AI Agent
Updated with current Groq API models (August 2024)
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Available Groq models (Production models - stable and reliable)
AVAILABLE_MODELS = {
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B Versatile",
        "developer": "Meta",
        "context": 131072,
        "max_tokens": 32768,
        "description": "Meta's latest and most capable model for complex tasks",
        "recommended_for": ["complex reasoning", "code generation", "creative writing"]
    },
    "llama-3.1-8b-instant": {
        "name": "Llama 3.1 8B Instant", 
        "developer": "Meta",
        "context": 131072,
        "max_tokens": 131072,
        "description": "Fast and efficient model for quick responses",
        "recommended_for": ["general chat", "quick queries", "simple tasks"]
    },
    "gemma2-9b-it": {
        "name": "Gemma 2 9B IT",
        "developer": "Google",
        "context": 8192,
        "max_tokens": 8192,
        "description": "Google's efficient instruction-tuned model",
        "recommended_for": ["instruction following", "general assistance"]
    }
}

# Preview models (for testing only - not recommended for production)
PREVIEW_MODELS = {
    "deepseek-r1-distill-llama-70b": {
        "name": "DeepSeek R1 Distill Llama 70B",
        "developer": "DeepSeek/Meta",
        "context": 131072,
        "max_tokens": 131072,
        "description": "Advanced reasoning model (Preview)",
        "warning": "Preview model - may be discontinued"
    },
    "qwen/qwen3-32b": {
        "name": "Qwen 3 32B",
        "developer": "Alibaba Cloud",
        "context": 131072,
        "max_tokens": 40960,
        "description": "Latest Qwen model with advanced reasoning (Preview)",
        "warning": "Preview model - may be discontinued"
    }
}

# Default model parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1024
DEFAULT_TOP_P = 1

# App Configuration
APP_TITLE = "Karbon AI Agent"
APP_ICON = "🤖"
MAX_CONVERSATION_HISTORY = 20

# UI Configuration
THEME_COLOR = "#667eea"
SECONDARY_COLOR = "#764ba2"

# Agent Types Configuration with optimized model selection
AGENT_TYPES = {
    "Code Assistant": {
        "model": "llama-3.3-70b-versatile",  # Best for complex coding tasks
        "description": "Expert in programming and software development",
        "system_prompt": """You are an expert code assistant with deep knowledge in multiple programming languages, 
        software architecture, debugging, and best practices. Help users with coding tasks, code review, 
        optimization, and technical problem-solving. Always provide clear, well-commented code examples 
        and explain your reasoning step by step. Focus on writing clean, efficient, and maintainable code.""",
        "icon": "💻",
        "temperature": 0.3,  # Lower temperature for more consistent code
        "max_tokens": 2048   # More tokens for detailed code explanations
    },
    "Research Analyst": {
        "model": "llama-3.3-70b-versatile",  # Best for complex analysis
        "description": "Specialized in data analysis and research",
        "system_prompt": """You are a professional research analyst with expertise in data analysis, 
        market research, academic research, and statistical analysis. Provide well-researched, 
        evidence-based insights and help users analyze complex information. Always structure your 
        analysis clearly with: 1) Key findings, 2) Supporting evidence, 3) Implications, and 4) Recommendations.""",
        "icon": "📊",
        "temperature": 0.5,  # Balanced for analytical tasks
        "max_tokens": 2048
    },
    "Creative Writer": {
        "model": "llama-3.3-70b-versatile",  # Best for creative tasks
        "description": "Creative writing and content creation specialist",
        "system_prompt": """You are a creative writing assistant with expertise in storytelling, 
        content creation, copywriting, and literary analysis. Help users create engaging content, 
        improve their writing, and explore creative ideas. Focus on narrative flow, character development, 
        vivid descriptions, and engaging dialogue. Adapt your writing style to match the user's needs.""",
        "icon": "✍️",
        "temperature": 0.8,  # Higher temperature for creativity
        "max_tokens": 2048
    },
    "General Assistant": {
        "model": "llama-3.1-8b-instant",  # Fast for general queries
        "description": "Versatile AI assistant for general queries",
        "system_prompt": """You are a helpful, knowledgeable AI assistant. Provide accurate, 
        detailed, and helpful responses across a wide range of topics. Be conversational, 
        clear, and adapt your communication style to the user's needs. Always aim to be 
        informative yet accessible, and ask clarifying questions when needed.""",
        "icon": "🤖",
        "temperature": 0.7,  # Standard temperature
        "max_tokens": 1024
    }
}

# File upload settings
ALLOWED_FILE_TYPES = ['txt', 'pdf', 'docx', 'py', 'js', 'html', 'css', 'json', 'md', 'csv']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Conversation settings
MAX_CONVERSATION_LENGTH = 50  # Maximum number of messages to keep in memory
CONTEXT_WINDOW_BUFFER = 1000  # Reserve tokens for system prompt and response

# Error messages
ERROR_MESSAGES = {
    "api_key_missing": "❌ Groq API key not found. Please check your .env file.",
    "model_error": "❌ Model error. The selected model may be temporarily unavailable.",
    "rate_limit": "⚠️ Rate limit exceeded. Please wait a moment before sending another message.",
    "network_error": "❌ Network error. Please check your internet connection.",
    "general_error": "❌ An unexpected error occurred. Please try again."
}

# Success messages
SUCCESS_MESSAGES = {
    "connection_established": "✅ Successfully connected to Groq API",
    "history_cleared": "✅ Conversation history cleared",
    "file_uploaded": "✅ File uploaded successfully"
}

# Model selection guidelines
MODEL_SELECTION_GUIDE = {
    "complex_tasks": "llama-3.3-70b-versatile",
    "quick_responses": "llama-3.1-8b-instant", 
    "general_use": "llama-3.1-8b-instant",
    "code_generation": "llama-3.3-70b-versatile",
    "creative_writing": "llama-3.3-70b-versatile",
    "data_analysis": "llama-3.3-70b-versatile"
}

# Feature flags
ENABLE_FILE_UPLOAD = True
ENABLE_CONVERSATION_EXPORT = True
ENABLE_MODEL_SWITCHING = True
ENABLE_TEMPERATURE_ADJUSTMENT = True

def get_model_info(model_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific model"""
    if model_id in AVAILABLE_MODELS:
        return AVAILABLE_MODELS[model_id]
    elif model_id in PREVIEW_MODELS:
        return PREVIEW_MODELS[model_id]
    else:
        return {"error": f"Model {model_id} not found"}

def get_recommended_model(task_type: str) -> str:
    """Get recommended model for a specific task type"""
    return MODEL_SELECTION_GUIDE.get(task_type, "llama-3.1-8b-instant")

def validate_config() -> bool:
    """Validate configuration settings"""
    if not GROQ_API_KEY:
        print(ERROR_MESSAGES["api_key_missing"])
        return False
    return True