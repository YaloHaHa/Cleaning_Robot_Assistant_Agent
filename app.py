import streamlit as st
from agent.react_agent import ReactAgent
import time

# Page configuration
st.set_page_config(
    page_title="Robot Assistant",
    page_icon=":material/smart_toy:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar: App info and quick help
with st.sidebar:
    st.markdown("### :material/info: About")
    st.markdown("""
    **Cleaning Robot Assistant** — Your intelligent Q&A companion for robot vacuum and mop combo guidance.
    
    Ask questions about:
    - :material/help: Usage & operation
    - :material/build: Maintenance & care
    - :material/trending_up: Purchase recommendations
    - :material/warning: Troubleshooting
    """)
    
    st.divider()
    
    st.markdown("### :material/history: Session")
    if st.button(":material/delete: Clear History", use_container_width=True):
        st.session_state["message"] = []
        st.rerun()
    
    msg_count = len(st.session_state.get("message", []))
    if msg_count > 0:
        st.caption(f":material/chat: {msg_count // 2} conversations")
    
    st.divider()
    st.caption(":material/shield: Powered by LangChain ReAct Agent")

# Main header
col1, col2 = st.columns([1, 5], vertical_alignment="center")
with col1:
    st.markdown("# :material/smart_toy:")
with col2:
    st.markdown("## Cleaning Robot Assistant")
    st.markdown("*Intelligent answers to all your robot cleaning questions*", help="Powered by advanced RAG and tool-use capabilities")

# Initialize the agent
if "agent" not in st.session_state:
    st.session_state.agent = ReactAgent()

# Message history
if "message" not in st.session_state:
    st.session_state["message"] = []

# Display message history with better styling
for message in st.session_state["message"]:
    with st.chat_message(message["role"], avatar=":material/smart_toy:" if message["role"] == "assistant" else ":material/person:"):
        st.markdown(message["content"])

# User input with better prompt
prompt = st.chat_input(
    placeholder="Ask me anything about robot vacuums, maintenance, or troubleshooting...",
    key="user_input"
)

if prompt:
    # User message
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    # Assistant response with streaming
    response_messages = []
    with st.chat_message("assistant", avatar=":material/smart_toy:"):
        with st.spinner(":material/psychology: Agent is thinking..."):
            res_stream = st.session_state.agent.execute_stream(prompt)
            
            def capture(generator, cache_list):
                for chunk in generator:
                    cache_list.append(chunk)
                    for char in chunk:
                        time.sleep(0.01)
                        yield char
            
            st.write_stream(capture(res_stream, response_messages))
    
    st.session_state["message"].append({
        "role": "assistant",
        "content": "".join(response_messages[-1]) if response_messages else ""
    })

