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
                "Please add it to Streamlit Secrets or create a .env file"
            )
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Use correct model name
        try:
            self.model = genai.GenerativeModel("gemini-pro")
            print("🤖 Gemini client initialized with gemini-pro")
        except Exception as e:
            # Fallback to alternative model
            print(f"⚠️ Using alternative model: {e}")
            self.model = genai.GenerativeModel("models/gemini-pro")
    
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
            error_msg = str(e)
            print(f"❌ Error generating content: {error_msg}")
            
            # If gemini-pro fails, try with explicit model path
            if "not found" in error_msg.lower():
                try:
                    # Try alternative model
                    alt_model = genai.GenerativeModel("gemini-1.5-flash-latest")
                    response = alt_model.generate_content(full_prompt)
                    return response.text
                except:
                    return f"Error: Model not available. Please check your API key and model access."
            
            return f"Error: {error_msg}"

# ============================================
# Create global instance
# ============================================
llm = GeminiClient()