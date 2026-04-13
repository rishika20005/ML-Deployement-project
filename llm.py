import google.generativeai as genai
import streamlit as st
import os

class GeminiClient:
    """Free LLM Client using Google Gemini API"""
    
    def __init__(self):
        # Get API key from Streamlit secrets (cloud) or environment (local)
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("✅ API key loaded from Streamlit secrets")
        except Exception as e:
            # Fallback to environment variable for local testing
            api_key = os.getenv("GEMINI_API_KEY")
            st.warning("⚠️ Using API key from environment variable")
        
        if not api_key:
            st.error("❌ GEMINI_API_KEY not found!")
            raise ValueError(
                "❌ GEMINI_API_KEY not found!\n"
                "Please add it to Streamlit Secrets (Manage App → Settings → Secrets)\n"
                "Format: GEMINI_API_KEY = \"your_key_here\""
            )
        
        # Configure Gemini
        try:
            genai.configure(api_key=api_key)
            
            # List available models to debug
            models = genai.list_models()
            model_names = [model.name for model in models]
            
            # Try different model names in order
            model_options = [
                "models/gemini-pro",
                "gemini-pro",
                "models/gemini-1.5-flash",
                "gemini-1.5-flash"
            ]
            
            self.model = None
            for model_name in model_options:
                try:
                    if model_name in model_names or any(model_name in m for m in model_names):
                        self.model = genai.GenerativeModel(model_name)
                        st.success(f"🤖 Using model: {model_name}")
                        break
                except:
                    continue
            
            # If no model found, use default
            if self.model is None:
                self.model = genai.GenerativeModel("gemini-pro")
                st.info("ℹ️ Using default gemini-pro model")
                
        except Exception as e:
            st.error(f"❌ Error configuring Gemini: {str(e)}")
            raise
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text using Google Gemini"""
        
        try:
            # Build full prompt with system instruction
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
            else:
                full_prompt = prompt
            
            # Call Gemini API with retry logic
            try:
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=1000,
                        temperature=0.7,
                        top_p=0.9
                    )
                )
                return response.text
            except Exception as api_error:
                # Try with simpler config if first attempt fails
                st.warning("⚠️ Retrying with simpler configuration...")
                response = self.model.generate_content(full_prompt)
                return response.text
        
        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ Generation error: {error_msg}")
            
            # Helpful error messages
            if "API_KEY" in error_msg.upper():
                return "Error: Invalid API key. Please check your Streamlit Secrets."
            elif "quota" in error_msg.lower():
                return "Error: API quota exceeded. Please wait a few minutes."
            elif "model" in error_msg.lower():
                return "Error: Model not available. Please check API access."
            else:
                return f"Error: {error_msg}"

# ============================================
# Create global instance
# ============================================
llm = GeminiClient()