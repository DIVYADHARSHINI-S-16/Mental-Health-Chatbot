#!/usr/bin/env python3
"""
Quick Start Script for Mental Health Companion Chatbot
Run this to set up the application quickly
"""

import os
import sys

def main():
    print("🧠 Mental Health Companion Chatbot - Setup Guide\n")
    print("=" * 50)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("\n⚠️  .env file not found!")
        print("\nTo run the chatbot, you need to:")
        print("\n1. Get a Groq API key:")
        print("   - Visit: https://console.groq.com")
        print("   - Sign up for free")
        print("   - Create an API key")
        print("\n2. Create a .env file with:")
        print("   GROQ_API_KEY=your_api_key_here")
        print("\n3. Run the app:")
        print("   streamlit run main.py")
        print("\n" + "=" * 50)
        return False
    
    print("\n✅ Setup looks good!")
    print("\n📝 To start the chatbot:")
    print("   streamlit run main.py")
    print("\n" + "=" * 50)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
