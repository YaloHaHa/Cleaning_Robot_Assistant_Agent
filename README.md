# 🤖 Cleaning Robot Q&A Assistant

A modern AI-powered chatbot demo showcasing **LangChain ReAct agents**, **Retrieval-Augmented Generation (RAG)**, and **tool-use capabilities** for intelligent robot vacuum and mop combo Q&A. Built with Streamlit for an intuitive, interactive interface.

## ✨ Features

- **ReAct Agent Architecture**: Autonomous reasoning with "Think → Act → Observe → Re-think" workflow
- **Retrieval-Augmented Generation (RAG)**: Intelligent semantic search across knowledge base using Chroma vector store
- **7 Integrated Tools**:
  - `rag_summarize`: Semantic search for robot-related knowledge
  - `get_weather`: Real-time weather & environment info
  - `get_user_location`: User geolocation detection
  - `get_user_id`: User identification
  - `get_current_month`: Current date/time
  - `fetch_external_data`: User usage records & statistics
  - `fill_context_for_report`: Report generation setup
- **Streaming Response**: Real-time chat responses with character-by-character streaming
- **Modern UI**: Clean, professional Streamlit interface with Material Design icons
- **Middleware Pipeline**: Tool monitoring, logging, and report prompt switching
- **Multi-language Knowledge Base**: 8 comprehensive English documents (~1000+ Q&A entries)

## 📋 Project Structure

```
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── Plan.md                         # Project roadmap
│
├── agent/
│   ├── react_agent.py             # ReAct agent orchestrator
│   └── tools/
│       ├── agent_tools.py         # 7 tool implementations
│       └── middleware.py          # Tool monitoring & logging
│
├── rag/
│   ├── rag_service.py             # RAG pipeline orchestrator
│   └── vector_store.py            # Chroma integration & MD5 deduplication
│
├── model/
│   └── factory.py                 # LLM model factory
│
├── config/
│   ├── agent.yaml                 # Agent configuration
│   ├── chroma.yaml                # Vector store settings
│   ├── rag.yaml                   # RAG pipeline config
│   └── prompts.yaml               # Prompt management
│
├── prompts/
│   ├── main_prompt.txt            # System prompt for agent
│   ├── report_prompt.txt          # Report generation prompt
│   └── rag_summarize.txt          # RAG query prompt
│
├── data_bot/                      # Knowledge base
│   ├── size_recommendation.txt    # Size selection guide
│   ├── color_selection.txt        # Color/appearance info
│   ├── laundry_care.txt          # Cleaning & care instructions
│   ├── troubleshooting.txt        # Fault diagnosis (200 entries)
│   ├── robot_vacuum_faq.txt       # Single-robot FAQ (100 Q&A)
│   ├── vacuum_mop_combo_faq.txt   # Combo-robot FAQ (100 Q&A)
│   ├── maintenance.txt            # Maintenance guide (200+ entries)
│   ├── buying_guide.txt           # Purchase recommendations
│   └── external/
│       └── records.csv            # User usage data (120 records)
│
├── utils/
│   ├── config_handler.py          # YAML config loader
│   ├── file_handler.py            # File I/O utilities
│   ├── logger_handler.py          # Logging setup
│   ├── path_tool.py               # Dynamic path resolution
│   ├── prompt_uploader.py         # Prompt loading
│   └── restart_chunk.py           # Text chunking
│
├── logs/                          # Application logs
├── chroma_db/                     # Vector store (auto-generated)
├── .streamlit/
│   └── config.toml               # Streamlit theme configuration
└── md5.text                       # MD5 dedup tracking
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (gpt-5-nano + text-embedding-3-small)

### 1. Clone & Setup

```bash
cd 1_Project_LangChain_RobotAssistantAgent

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy the environment template
cp .env.example .env

# Add your OpenAI API key to .env
# OPENAI_API_KEY=sk-...
```

Or export directly:
```bash
export OPENAI_API_KEY=sk-...
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 💬 Usage

1. **Ask Questions** about robot vacuums/mops:
   - "How do I clean the side brush?"
   - "What vacuum is best for pet hair?"
   - "My robot won't dock. How do I fix it?"
   - "Generate my usage report for March"

2. **View Sidebar** for:
   - Quick help on supported topics
   - Session management & history clearing
   - Conversation counter

3. **Streaming Responses** appear character-by-character in real-time

## 🏗️ Architecture

### Agent Workflow

```
User Query
    ↓
[ReAct Agent]
    ├→ Think: Analyze query, decide which tools needed
    ├→ Act: Call 0-5 tools in sequence
    ├→ Observe: Integrate tool results
    └→ Respond: Generate natural language answer
    ↓
Streaming Response
```

### Tool Integration

Tools are dynamically called based on agent reasoning:

```python
# Tool definitions (agent_tools.py)
- rag_summarize(query: str) → knowledge base content
- get_weather(city: str) → weather/humidity info
- get_user_location() → user's city
- get_user_id() → user ID (e.g., "1001")
- get_current_month() → current month (YYYY-MM format)
- fetch_external_data(user_id: str, month: str) → usage records
- fill_context_for_report() → prepare report context
```

### RAG Pipeline

```
Data Files (.txt, .pdf)
    ↓
[Vector Store - Chroma]
    ├→ Text Chunking (200 chars, 20 overlap)
    ├→ Embedding (text-embedding-3-small)
    ├→ Vector Storage with MD5 dedup
    └→ Semantic Search (k=4 results)
    ↓
rag_summarize Tool
```

## ⚙️ Configuration

All settings are in `config/` YAML files:

- **agent.yaml**: Agent behavior, model params, temperature
- **chroma.yaml**: Vector store path, chunk size, k-retrieval
- **rag.yaml**: Text splitting strategy, embedding params
- **prompts.yaml**: Prompt file paths

Modify these to customize agent behavior without code changes.

## 📊 Knowledge Base

**8 documents** covering:
- Size recommendations, color selection, care instructions
- Troubleshooting (200+ fault diagnosis entries)
- FAQ for single robots (100 Q&A) & combo robots (100 Q&A)
- Maintenance guide (200+ entries across 7 sections)
- Buying guide with recommendations
- User usage data (120 records × 12 months)


## 🔧 Customization

### Add Knowledge Documents

1. Place new `.txt` or `.pdf` files in `data_bot/`
2. Clear `md5.text` to force vector store rebuild
3. Restart the app
4. Vector store automatically rebuilds on next run

### Modify System Prompt

Edit `prompts/main_prompt.txt` to change agent behavior, guidelines, or tool descriptions.

### Change Theme

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#0066cc"
backgroundColor = "#ffffff"
# ... other theme settings
```

### Adjust Tool Behavior

Modify functions in `agent/tools/agent_tools.py`:
- Change weather API source
- Customize location detection
- Adjust data fetching logic

## 📦 Dependencies

- **langchain** - Agent orchestration
- **langchain-openai** - OpenAI integration
- **langchain-chroma** - Vector store integration
- **streamlit** - Web UI framework
- **pyyaml** - Configuration management
- **pypdf** - PDF document processing
- **chromadb** - Vector database

See `requirements.txt` for versions.

## 🎯 Demo Highlights

This project demonstrates:

✅ **LangChain ReAct Agent** - Autonomous reasoning and tool use  
✅ **Retrieval-Augmented Generation** - Semantic search + LLM  
✅ **Tool-Use Workflow** - Multi-step reasoning with external data  
✅ **Streaming Responses** - Real-time chat UX  
✅ **Middleware Pipeline** - Tool monitoring, logging, prompt switching  
✅ **Modular Architecture** - Easy to extend and customize  
✅ **Production-Ready Streamlit UI** - Modern, professional interface  

## 🔍 What You Can Try

1. **Q&A Demo**: Ask specific robot questions and watch the agent reason
2. **Tool Observation**: Ask about weather/location to trigger `get_weather` tool
3. **Report Generation**: Say "Generate my usage report" to see report pipeline
4. **Multi-step Reasoning**: Ask complex questions requiring tool chaining
5. **Streaming**: Watch responses appear character-by-character in real-time

## 🤝 License

This is a demo project created for educational purposes.

