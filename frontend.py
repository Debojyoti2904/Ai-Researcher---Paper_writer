import streamlit as st
from ai_researcher_2 import INITIAL_PROMPT, graph, config
from langchain_core.messages import AIMessage
import logging
from pathlib import Path

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Research AI Agent",
    page_icon="📄",
    layout="wide",
)

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown("## 🧠 Research AI Agent")
    st.markdown(
        """
        **Capabilities**
        - Search arXiv papers
        - Analyze multiple papers
        - Draft a research paper
        - Generate LaTeX & PDF
        
        **Model**
        - Gemini 2.5 Flash
        
        **Tip**
        - Ask step-by-step for best results
        """
    )

# ----------------------------
# Session State
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

# ----------------------------
# Header
# ----------------------------
st.title("📄 Research AI Agent")
st.caption("An agentic AI system for research discovery and paper generation")

st.divider()

# ----------------------------
# Display Chat History
# ----------------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ----------------------------
# Chat Input
# ----------------------------
user_input = st.chat_input("What research topic would you like to explore?")

if user_input:
    # ---- Display user message
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.write(user_input)

    # ---- Prepare agent input
    chat_input = {
        "messages": [
            {"role": "system", "content": INITIAL_PROMPT},
            *st.session_state.chat_history,
        ]
    }

    # ---- Status indicator
    status = st.status("🤖 Agent is thinking...", expanded=True)

    assistant_placeholder = st.empty()
    full_response = ""

    # ---- Stream agent output
    for step in graph.stream(chat_input, config, stream_mode="values"):
        message = step["messages"][-1]

        # ---- Tool call logging (no UI spam)
        if getattr(message, "tool_calls", None):
            for tool_call in message.tool_calls:
                status.update(
                    label=f"🔧 Using tool: {tool_call['name']}",
                    state="running",
                )

        # ---- Assistant text handling
        if isinstance(message, AIMessage) and message.content:
            clean_text = ""

            # Structured Gemini output
            if isinstance(message.content, list):
                for block in message.content:
                    text = ""
                    
                    #Handle Dictionary Blocks    
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            text = block.get("text", "").strip()
                            
                    elif isinstance(block, str):
                        text = block.strip()
                            
                    # Hide and process LaTeX / internal content
                    if text:
                        if (
                            text.startswith("latex")
                            or text.startswith("\\documentclass")
                        ):
                            continue

                        clean_text += text + "\n"

            # Simple string
            elif isinstance(message.content, str):
                clean_text = message.content.strip()

            if clean_text:
                full_response += clean_text + "\n"
                assistant_placeholder.markdown(full_response)

    status.update(label="✅ Done", state="complete")

    # ---- Save assistant response
    if full_response.strip():
        st.session_state.chat_history.append(
            {"role": "assistant", "content": full_response.strip()}
        )

# ----------------------------
# PDF Section
# ----------------------------
if st.session_state.pdf_path:
    st.divider()
    st.subheader("📑 Generated Research Paper")

    pdf_file = Path(st.session_state.pdf_path)
    if pdf_file.exists():
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name=pdf_file.name,
                mime="application/pdf",
            )
    else:
        st.warning("PDF file not found.")
