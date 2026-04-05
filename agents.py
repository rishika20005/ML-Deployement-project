from llm import bedrock

class Agent:
    """Base Agent Class"""
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
    
    def run(self, user_input: str) -> str:
        """Execute the agent with given input"""
        print(f"🤖 {self.name}: Working...")
        response = bedrock.generate(
            prompt=user_input,
            system_prompt=self.system_prompt
        )
        print(f"✅ {self.name}: Done")
        return response

# Define Agent 1: Researcher
researcher = Agent(
    name="Researcher",
    system_prompt="""You are an expert research assistant. 
    When given a topic, provide:
    1. 3-5 key bullet points with important facts
    2. A suggested outline for a blog post (Introduction, 3-4 sections, Conclusion)
    Be factual, concise, and informative."""
)

# Define Agent 2: Writer
writer = Agent(
    name="Writer",
    system_prompt="""You are a professional blog writer.
    When given an outline, write a comprehensive 400-500 word blog post.
    - Use engaging language
    - Include clear headings
    - Write in short, readable paragraphs
    - Add a compelling introduction and conclusion
    - Use a friendly, conversational tone"""
)

# Define Agent 3: Editor
editor = Agent(
    name="Editor",
    system_prompt="""You are a helpful and encouraging editor.
    Review the draft for:
    - Clarity and flow
    - Grammar and spelling
    - Completeness
    
    If the draft is reasonably good, respond with exactly: "✅ APPROVED - Good quality content ready for publication."
    Only reject if there are major issues."""
)

# ============================================
# THESE ARE THE FUNCTIONS THAT app.py IMPORTS
# ============================================

def research_topic(topic: str) -> str:
    """Research a topic and return outline"""
    return researcher.run(f"Research this topic thoroughly: {topic}")

def write_blog_post(outline: str) -> str:
    """Write a blog post from outline"""
    return writer.run(f"Write a blog post based on this outline:\n\n{outline}")

def edit_content(draft: str) -> str:
    """Edit and review a draft"""
    return editor.run(f"Review and edit this draft:\n\n{draft}")