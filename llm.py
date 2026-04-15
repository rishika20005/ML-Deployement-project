from groq import Groq
import streamlit as st
import os

class GroqClient:
    """Free Cloud LLM Client using Groq + Llama 3"""
    
    def __init__(self):
        # Get API key from Streamlit secrets (cloud) or environment (local)
        try:
            api_key = st.secrets["GROQ_API_KEY"]
            st.success("✅ API key loaded from Streamlit secrets")
        except Exception as e:
            api_key = os.getenv("GROQ_API_KEY")
            st.warning("⚠️ Using API key from environment variable")
        
        if not api_key:
            st.error("❌ GROQ_API_KEY not found!")
            raise ValueError("Please add GROQ_API_KEY to Streamlit Secrets")
        
        # Initialize Groq client
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192"  # Fast & Free
        st.success(f"🤖 Groq client initialized with {self.model}")
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text using Groq Cloud"""
        
        try:
            # Build messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=0.9
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ Generation error: {error_msg}")
            
            if "api_key" in error_msg.lower():
                return "Error: Invalid API key. Check Streamlit Secrets."
            elif "rate limit" in error_msg.lower():
                return "Error: Rate limit exceeded. Wait 1 minute and try again."
            else:
                return f"Error: {error_msg}"

# Create global instance
llm = GroqClient()