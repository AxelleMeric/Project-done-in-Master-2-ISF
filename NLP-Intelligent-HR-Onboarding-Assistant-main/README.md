# Intelligent HR Onboarding Assistant with RAG and LangChain

**NLP Project — Master M2**  
*Authors: Arthur DANJOU, Axelle MERIC, Moritz von SIEMENS*

## Description

Intelligent conversational assistant designed to support new employees at **Editions Divulgâche** during their first week. The system uses advanced NLP techniques (RAG, embeddings, agents) to answer HR questions, access employee data, schedule meetings, and manage leave requests.

## Features

- 🔍 **Semantic search** in the HR knowledge base via RAG
- 👤 **Employee directory access** (structured JSON data)
- 📅 **Meeting scheduling** via LangChain tools
- 🏖️ **Automated leave requests**
- 🧠 **Conversational memory** with sliding window (multi-turn context)
- 💬 **Interactive Gradio interface** with tool call visualization

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│      HR Onboarding Assistant — Editions Divulgâche       │
│                                                          │
│  📝 System prompts (LangChain LCEL)                      │
│  🧠 Sliding window conversational memory                 │
│  🔧 Tools:                                               │
│     ├── 🔍 Knowledge base search (RAG)                   │
│     ├── 👤 Employee directory                            │
│     ├── 📅 Meeting scheduling                            │
│     ├── 🏖️ Leave request submission                      │
│     └── 🕐 Current date and time                         │
│  🔄 ReAct loop: reason → act → observe                   │
│  📊 MistralAI Embeddings + Qdrant Vector Store           │
└──────────────────────────────────────────────────────────┘
```

## Prerequisites

- Python ≥ 3.13
- MistralAI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NLP-Intelligent-HR-Onboarding-Assistant-with-RAG-and-LangChain
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure MistralAI API key**
   
   Set the environment variable:
   ```bash
   export MISTRAL_API_KEY="your_api_key"
   ```

## Usage

### Run the Jupyter notebook

```bash
jupyter notebook projet.ipynb
```

Execute cells sequentially to:
1. Analyse tokenisation of HR documents
2. Create the Qdrant vector database
3. Initialise the ReAct agent
4. Run demonstrations
5. Launch the Gradio interface (runs on `http://127.0.0.1:7860`)

### Data structure

```
data/
├── entreprise.md    # HR knowledge base (leave policy, remote work, etc.)
└── employés.json    # Editions Divulgâche employee directory
```

## Project content

|    TP   |      Concept     |                         Usage                         |
|:--------|:-----------------|:------------------------------------------------------|
| **TP1** | Embeddings       | Vector representation of documents, cosine similarity |
| **TP2** | BPE Tokenization | Token cost analysis, FR/EN comparison                 |
| **TP3** | LLM + LangChain  | ChatMistralAI configuration, messages, LCEL chains    |
| **TP4** | Agents + Memory  | `@tool` decorators, ReAct loop, sliding window        |
| **TP5** | RAG + Gradio     | Qdrant vector store, semantic search, interface       |

## Technologies

- **LangChain**: LLM orchestration framework
- **MistralAI**: LLM model and embeddings (mistral-embed)
- **Qdrant**: In-memory vector database
- **Gradio**: Interactive web interface
- **tiktoken**: BPE tokenization analysis
- **pandas**: Employee data manipulation

## Main dependencies

```
langchain>=1.2.12
langchain-mistralai>=1.1.1
langchain-qdrant>=1.1.0
gradio>=6.9.0
tiktoken>=0.12.0
pandas>=3.0.1
```

## Supported question examples

- "How many days of annual leave do I have?"
- "What is the remote work policy?"
- "Give me Flore d'Anjou's contact information"
- "Schedule a meeting with the editorial team tomorrow at 2pm"
- "I want to request leave from January 15th to 20th"

## Authors

- **Arthur DANJOU**
- **Axelle MERIC**
- **Moritz von SIEMENS**

*Project completed as part of the Natural Language Processing course — Master M2*
