import streamlit as st
from agents import research_topic, write_blog_post, edit_content

# Page configuration
st.set_page_config(
    page_title="🤖 Multi-Agent Workflow",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 Autonomous Multi-Agent Workflow")
st.markdown("### AI-Powered Business Process Automation")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("This system uses 3 AI agents working together:\n\n1. 🔍 **Researcher** - Gathers information\n2. ✍️ **Writer** - Creates content\n3. 🧐 **Editor** - Reviews and approves")
    st.markdown("---")
    st.caption("Built with AWS Bedrock & Streamlit")

# Main input
st.header("📝 Create a Blog Post")
topic = st.text_input(
    "Enter your blog topic:",
    placeholder="e.g., The Future of Renewable Energy",
    value="The Impact of AI on Healthcare"
)

# Workflow execution
if st.button("🚀 Start Multi-Agent Workflow", type="primary", use_container_width=True):
    if not topic.strip():
        st.error("Please enter a topic!")
    else:
        with st.spinner("🤖 Agents are collaborating..."):
            
            # Step 1: Research
            st.subheader("🔍 Step 1: Research Phase")
            with st.status("Researcher is gathering information...", expanded=True) as status:
                outline = research_topic(topic)
                st.markdown(outline)
                status.update(label="✅ Research complete!", state="complete")
            
            # Step 2: Write
            st.subheader("✍️ Step 2: Writing Phase")
            with st.status("Writer is creating content...", expanded=True) as status:
                draft = write_blog_post(outline)
                st.markdown(draft)
                status.update(label="✅ Draft complete!", state="complete")
            
            # Step 3: Edit
            st.subheader("🧐 Step 3: Editing Phase")
            with st.status("Editor is reviewing...", expanded=True) as status:
                review = edit_content(draft)
                st.markdown(review)
                
                if "✅ APPROVED" in review:
                    status.update(label="✅ Approved by Editor!", state="complete")
                else:
                    status.update(label="⚠️ Revisions suggested", state="running")
            
            # ==========================================
            # FINAL RESULT & DOWNLOAD BUTTON (ALWAYS SHOWS)
            # ==========================================
            st.markdown("---")
            if "✅ APPROVED" in review:
                st.balloons()
                st.success("🎉 Article Complete and Approved!")
            else:
                st.warning("⚠️ Editor suggested revisions (see Step 3 above)")
                st.info("💡 You can still download the draft below!")
            
            # DOWNLOAD BUTTON (Outside the if/else block)
            st.download_button(
                label="📥 Download Article",
                data=draft,
                file_name=f"{topic.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
            # ==========================================

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>Final Year Project | Multi-Agent AI System | Powered by AWS Bedrock</p>
    </div>
    """,
    unsafe_allow_html=True
)