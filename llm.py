import google.generativeai as genai
import streamlit as st
import os

class GeminiClient:
    """Free LLM Client using Google Gemini API"""
    
    def __init__(self):
        # Get API key from Streamlit secrets (cloud) or environment (local)
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            print("✅ Loaded API key from Streamlit secrets")
        except Exception as e:
            # Fallback to environment variable for local testing
            api_key = os.getenv("GEMINI_API_KEY")
            print("🔄 Loaded API key from environment variable")
        
        if not api_key:
            raise ValueError(
                "❌ GEMINI_API_KEY not found!\n"
                "Please add it to GitHub Secrets or create a .env file"
            )
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        print("🤖 Gemini client initialized successfully")
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text using Google Gemini"""
        
        try:
            # Build full prompt with system instruction
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
            else:
                full_prompt = prompt
            
            # Call Gemini API
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.7,
                    top_p=0.9
                )
            )
            
            return response.text
        
        except Exception as e:
            print(f"❌ Error generating content: {e}")
            return f"Error: {str(e)}"

# ============================================
# Create global instance (this is what agents.py imports)
# ============================================
llm = GeminiClient()