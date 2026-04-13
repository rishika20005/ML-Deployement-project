import streamlit as st
from agents import research_topic, write_blog_post, edit_content

# ============================================
# Page Configuration
# ============================================
st.set_page_config(
    page_title="AutoScribe - AI Content Generator",
    page_icon="🤖",
    layout="wide"
)

# ============================================
# Title & Header
# ============================================
st.title("🤖 AutoScribe")
st.subheader("Multi-Agent AI Content Generation System")
st.markdown("---")

# ============================================
# Sidebar - Project Info
# ============================================
with st.sidebar:
    st.header("ℹ️ About AutoScribe")
    st.write("""
    **AutoScribe** is a cloud-native, multi-agent AI system that automates content research, writing, and editing.
    
    **Workflow:**
    1. 🤖 Researcher → Gathers facts & creates outline
    2. 🤖 Writer → Composes full article
    3. 🤖 Editor → Reviews & approves
    
    **Tech Stack:**
    - Python 3.11
    - Google Gemini API (Free)
    - Streamlit Cloud
    - Git/GitHub
    """)
    
    st.markdown("---")
    st.write("**Developed by:** Rishika Ravi")
    st.write("**Internship:** IBM")
    st.write("**Roll No:** 22BBCACD457")

# ============================================
# Main Content Area
# ============================================

# Topic Input
st.header("📝 Generate Your Article")
topic = st.text_input(
    "Enter your topic:",
    placeholder="e.g., The Future of Artificial Intelligence in Healthcare",
    help="Enter a clear, specific topic for best results"
)

# Generate Button
if st.button("🚀 Start Multi-Agent Workflow", type="primary"):
    if not topic:
        st.warning("⚠️ Please enter a topic first!")
    else:
        # Create containers for each agent's output
        research_container = st.container()
        writer_container = st.container()
        editor_container = st.container()
        final_container = st.container()
        
        # ============================================
        # Agent 1: Researcher
        # ============================================
        with research_container:
            st.subheader("🤖 Step 1: Researcher Agent")
            with st.spinner("Researching topic and gathering facts..."):
                research_output = research_topic(topic)
                st.success("✅ Research Complete!")
                st.markdown(research_output)
        
        # ============================================
        # Agent 2: Writer
        # ============================================
        with writer_container:
            st.subheader("🤖 Step 2: Writer Agent")
            with st.spinner("Writing article based on research..."):
                writer_output = write_blog_post(research_output)
                st.success("✅ Writing Complete!")
                st.markdown(writer_output)
        
        # ============================================
        # Agent 3: Editor
        # ============================================
        with editor_container:
            st.subheader("🤖 Step 3: Editor Agent")
            with st.spinner("Reviewing and editing content..."):
                editor_output = edit_content(writer_output)
                st.success("✅ Editing Complete!")
                st.markdown(editor_output)
        
        # ============================================
        # Final Output + Download
        # ============================================
        with final_container:
            st.markdown("---")
            st.subheader("🎉 Final Article")
            
            # Combine all outputs for download
            full_article = f"""
AUTOSCRIBE - AI GENERATED ARTICLE
==================================

Topic: {topic}

---

RESEARCH OUTPUT:
{research_output}

---

WRITTEN ARTICLE:
{writer_output}

---

EDITOR REVIEW:
{editor_output}
"""
            
            st.markdown(writer_output)
            
            # Download Button
            st.download_button(
                label="📥 Download Article (.txt)",
                data=full_article,
                file_name=f"autoscribe_{topic.replace(' ', '_')[:30]}.txt",
                mime="text/plain",
                type="primary"
            )
            
            st.success("✅ Article generation complete! Download or copy your content.")

# ============================================
# Footer
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p><b>AutoScribe</b> | Multi-Agent AI Content Generation System</p>
    <p>Developed with ❤️ using Python, Gemini API, and Streamlit</p>
    <p>GitHub: <a href='https://github.com/rishika2005/ML-Deployement-project'>View Repository</a></p>
</div>
""", unsafe_allow_html=True)