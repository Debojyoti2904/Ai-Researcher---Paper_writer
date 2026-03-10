<div align="center">

# 🧬 AI Researcher: The Autonomous Scholar
### *Browse, Analyze, Visualize, and Author Research Papers in 2-3 Minutes.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Agentic-LangGraph-FF6F00?style=for-the-badge&logo=python&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Gemini](https://img.shields.io/badge/LLM-Gemini_2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![UI](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-setup-and-installation">Setup</a> •
  <a href="#-usage">Usage</a>
</p>

</div>

---

## 📖 Overview

**AI Researcher** is a cutting-edge **Agentic AI Workflow** designed to automate the heavy lifting of academic research. Unlike simple summarizers, this agent acts as an end-to-end research assistant that can autonomously browse the latest findings on **arXiv**, read complex PDF documents, generate data-driven charts, identify promising research directions, and compile a formatted **LaTeX** research paper—complete with mathematical equations, visual data, and citations.

Built using **LangGraph** for sophisticated state management, the system allows the agent to maintain context over long research cycles, dynamically choosing which tools to use until the final publication-ready PDF is generated.

---

## ✨ Key Features

* **🧠 Agentic Workflow:** Uses **LangGraph** nodes and edges to coordinate searching, reading, charting, and writing phases.
* **📚 Deep Literature Review:** Autonomously queries the **arXiv API** to find recently published papers on any specified topic.
* **👁️ PDF Comprehension:** Integrated `read_pdf` tool extracts full-text content from academic papers for in-depth analysis.
* **📊 Data Visualization:** Autonomously writes Python code to generate **Matplotlib** charts and seamlessly embeds them into the final document.
* **📝 Ready-to-Publish Output:** Generates professional research papers with mathematical rigor, rendered via **Tectonic** into high-quality LaTeX PDFs.
* **💬 Interactive Research:** A **Streamlit-powered** frontend allows you to guide the agent through the discovery and writing process.

---

## 🏗️ Technical Architecture

The system operates as a **ReAct Agent** cycle, where the Gemini 2.5 Flash "Brain" decides which tool to use based on the research stage.

```mermaid
graph TD
    User((User)) -->|Mention Topic| Streamlit["Streamlit UI"]
    Streamlit -->|Input| Agent{"AI Agent<br>(Gemini 2.5 Flash)"}
    
    subgraph Tools
        Agent -->|Search| arXiv["arXiv Tool"]
        Agent -->|Read| PyPDF2["PDF Reader"]
        Agent -->|Visualize| Matplotlib["Chart Generator"]
        Agent -->|Export| Tectonic["LaTeX Renderer"]
    end
    
    Agent -.->|State Tracking| Memory["Memory Store<br>(thread_id)"]
    Tectonic -->|Final Paper| User

```

---

## 🛠️ Technology Stack

| Component | Technology | Role |
| --- | --- | --- |
| **Orchestration** | **LangGraph** | Node-based agentic workflow management |
| **LLM Core** | **Gemini 2.5 Flash** | High-speed reasoning model for research analysis |
| **Data Retrieval** | **arXiv API** | Access to 2M+ scholarly articles |
| **PDF Extraction** | **PyPDF2** | Parsing complex academic documents |
| **Data Visualization** | **Matplotlib** | Generating analytical charts and graphs |
| **PDF Generation** | **Tectonic (LaTeX)** | Rendering ready-to-publish documents locally |
| **Frontend** | **Streamlit** | Seamless user interface for real-time interaction |

---

## 🚀 Setup and Installation

### 1. Prerequisites

Ensure you have **Python 3.11+** and **Tectonic** installed on your system (required for PDF rendering).

### 2. Clone & Environment

```bash
git clone [https://github.com/YOUR_USERNAME/AI-Researcher.git](https://github.com/YOUR_USERNAME/AI-Researcher.git)
cd AI-Researcher
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. API Configuration

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY="your_gemini_api_key_here"

```

---

## 🎯 Usage

1. **Launch the Frontend:**

```bash
streamlit run frontend.py

```

2. **Start Researching:** Enter a topic in the chat (e.g., *"Recent breakthroughs in RAG indexing, read the best paper, and write a summary with a chart comparing accuracies."*).
3. **Refine & Author:** * The AI will browse arXiv and suggest relevant papers.
* Select a paper for the agent to analyze in-depth.
* The agent will propose new research ideas and generate necessary visual data; choose one to generate your full LaTeX paper.


4. **Download:** Once the process is complete, grab your generated PDF directly from the interface or the `output/` folder.

---

<div align="center">
<p>Educational Purpose Only • Developed with ❤️</p>
</div>

```

```
