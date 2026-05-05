# 🔋 Agentic AI Workflow for EV Battery Health Monitoring

An **autonomous multi-agent AI system** for predictive maintenance in Electric Vehicles (EVs), built using **LangGraph**, **Streamlit**, **RAG (Retrieval-Augmented Generation)**, and **Groq LLMs** for ultra-fast inference. This project simulates how intelligent agent pipelines can autonomously monitor battery health, plan services, schedule appointments, and communicate recommendations.

---

## 🚗 Project Overview

The workflow is orchestrated using **LangGraph** and consists of four specialized agents that pass state to each other in sequence:

### ✳️ Agents in the Workflow

1. **BatteryInsightAgent**
   - Analyzes synthetic EV battery usage logs and degradation trends
   - Detects anomalies in charging behavior
   - Calculates State of Health (SoH) metrics
   - Identifies the impact of fast vs. slow charging on battery life

2. **ServicePlannerAgent**
   - Decides whether maintenance is needed based on battery insights
   - Uses **RAG** (FAISS + HuggingFace embeddings) to query a service manual for specific procedures
   - Recommends diagnostic routines and maintenance actions

3. **SchedulerAgent**
   - Simulates booking appointments with nearby service centers
   - Handles dealer selection and slot availability logic

4. **CommunicatorAgent**
   - Prepares user-facing messages with battery insights
   - Uses **Groq LLM** to generate professional email communications
   - Integrates RAG-based service manual recommendations

---

## 📁 Folder Structure

```
Agentic_AI_Workflow_Automotive/
├── agents/
│   ├── battery_agent.py            # Battery analysis agent
│   ├── service_planner_agent.py    # Service planning with RAG
│   ├── scheduler_agent.py          # Appointment scheduling
│   └── communicator_agent.py       # LLM-powered communication (Groq)
├── langgraph_flow/
│   ├── graph.py                    # LangGraph workflow definition
│   └── state.py                    # Shared state management
├── data/
│   ├── synthetic_data_generator.py # Generates synthetic EV battery data
│   ├── synthetic_data.csv          # Sample dataset
│   ├── vector_embeddings.py        # RAG setup using FAISS
│   └── vector_index/               # FAISS vector store (auto-generated)
├── app.py                          # Streamlit dashboard
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| LLM Inference | **Groq API** (llama3-8b-8192) |
| RAG | FAISS + HuggingFace Sentence Transformers |
| Dashboard | Streamlit |
| Data Processing | Pandas, NumPy |
| LLM Framework | LangChain |

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hariprasadvm-dev/Agentic_AI_Workflow_Automotive.git
cd Agentic_AI_Workflow_Automotive
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install faiss-cpu sentence-transformers langchain-community python-dotenv
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com/)

### 4. Generate Synthetic Battery Data

```bash
cd data
python synthetic_data_generator.py
```

### 5. Create Vector Embeddings (One-time setup)

```bash
cd data
python vector_embeddings.py
```

This builds the FAISS vector index from service manual data for RAG functionality.

### 6. Run the Streamlit App

```bash
streamlit run app.py
```

### 7. Use the Dashboard

- **Upload Data**: Use the sidebar to upload `synthetic_data.csv`
- **Run Analysis**: Click **🚀 Run AI Analysis** to trigger the full agent workflow
- **View Results**: Explore battery insights, service plans, and AI-generated emails
- **Navigate Sections**: Each agent's output is displayed in a separate section

---

## 📊 Data Flow

```
Battery CSV Input
      ↓
BatteryInsightAgent  →  Anomaly detection + SoH metrics
      ↓
ServicePlannerAgent  →  RAG-enhanced maintenance recommendations
      ↓
SchedulerAgent       →  Simulated dealer appointment booking
      ↓
CommunicatorAgent    →  Groq LLM-powered professional email
```

---

## 📌 Key Features

- 🔋 **Battery Health Analysis** — SoH tracking, anomaly detection, charging pattern analysis
- 🛠️ **Intelligent Service Planning** — Rule-based decisions augmented with RAG
- 📅 **Automated Scheduling** — Simulated service center appointment booking
- ✉️ **Smart Communication** — Groq-powered professional email generation
- ⚡ **Fast Inference** — Groq API delivers sub-second LLM responses vs. standard OpenAI latency

---

## 🌱 Future Enhancements

- Real EV fleet API integration
- Multi-manufacturer support (beyond Tesla-style data)
- ML-based battery failure prediction
- Real service center booking API integration
- Mobile-friendly UI
- IoT/telematics real-time data feed



