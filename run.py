#!/usr/bin/env python3
"""
Quick launcher for the Karbon AI Agent application
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import streamlit
        import groq
        import pandas
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e.name}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has API key"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found")
        print("Please copy .env.example to .env and add your Groq API key")
        return False
    
    with open(env_file) as f:
        content = f.read()
        if "your_groq_api_key_here" in content:
            print("❌ Please update your Groq API key in the .env file")
            return False
        
        if "GROQ_API_KEY=" not in content:
            print("❌ GROQ_API_KEY not found in .env file")
            return False
    
    print("✅ Environment configuration looks good")
    return True

def main():
    """Main launcher function"""
    print("🤖 Karbon AI Agent Launcher")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    print("\n🚀 Starting Streamlit application...")
    print("The app will open in your browser automatically")
    print("Press Ctrl+C to stop the application")
    print("-" * 40)
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()