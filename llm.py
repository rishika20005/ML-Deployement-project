from groq import Groq
import streamlit as st
import os

class GroqClient:
    def __init__(self):
        try:
            api_key = st.secrets["GROQ_API_KEY"]
            st.success("✅ API key loaded from Streamlit secrets")
        except:
            api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            st.error("❌ GROQ_API_KEY not found!")
            raise ValueError("Add GROQ_API_KEY to Streamlit Secrets")
        
        self.client = Groq(api_key=api_key)
        # Updated to currently available model
        self.model = "llama-3.1-8b-instant"
        st.success(f"🤖 Groq client initialized with {self.model}")
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

llm = GroqClient()