# 🛡️ Sentinel-QA

## Cognitive QA Ecosystem — From Requirements to Autonomous Execution

> **Status: 🧪 Alpha / Prototype**  
> This is a working proof-of-concept demonstrating autonomous test generation, execution, and triage. Production-ready architecture, but currently under active development and evaluation. Not yet recommended for mission-critical production workloads without additional hardening.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)](https://playwright.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📖 The Vision

Sentinel isn't another test automation framework. It's a **Cognitive QA Ecosystem** where AI handles the boring stuff so humans can focus on what matters.

**One sentence:** You type "User creates a new employee" → Sentinel generates the test plan, waits for your approval, executes it across parallel browsers, and if something breaks — auto-creates a Jira ticket with full context and screenshot attached.

---

## 🎯 What Sentinel Solves

| Problem | Sentinel Solution |
|---------|-------------------|
| Manual test script writing | AI Requirement Analyst generates structured plans from plain English |
| Broken selectors after every deploy | Historical failure memory + pattern detection |
| Bug reporting as manual bottleneck | Autonomous Jira ticket creation with screenshot attachment |
| Flaky tests wasting CI time | SQLite memory to distinguish flaky vs. systemic failures |
| LLM hallucinations reaching production | HITL Streamlit dashboard — every plan requires human approval |

---

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────────────┐
│ USER INPUT │
│ "User logs into OrangeHRM with Admin" │
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ REQUIREMENT ANALYST (AI) │
│ LangChain + SambaNova/Groq/Ollama → Structured Plan │
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ FASTAPI GATEWAY + SQLite │
│ Stores plan with status: "pending" │
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ HITL DASHBOARD (Streamlit) │
│ Human reviews, edits, approves → "approved" │
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ CI/CD (GitHub Actions) │
│ Fetches approved plans → Parallel execution │
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ PLAYWRIGHT EXECUTION ENGINE (pytest-xdist) │
│ 10-20 parallel browsers • Sync + networkidle │
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ FAILURE DETECTED? │
│ Yes → AI Triage Agent │
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ BUG REPORTER (AI) │
│ Queries SQLite history → Drafts report → Creates Jira │
│ → Attaches screenshot → Updates Allure │
└─────────────────────────────────────────────────────────────────┘

text



## 🧠 The Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Brain** | LangChain + SambaNova/Groq/Ollama | Multi-LLM with fallback chain |
| **Heart** | FastAPI | API gateway, single source of truth |
| **Memory** | SQLite (WAL mode) | Persistent failure history, concurrent access |
| **Muscle** | Playwright + pytest-xdist | Parallel browser automation |
| **Hands** | GitHub Actions | CI/CD automation |
| **Governance** | Streamlit | Human-in-the-loop approval dashboard |
| **Reporting** | Allure | Test reports + trend tracking |
| **Integration** | Jira Cloud API | Autonomous bug ticket creation |


## 🚀 Quick Start

```bash
# Prerequisites
python --version  # 3.11+
playwright install chromium

# Clone and install
git clone https://github.com/yourusername/sentinel-qa.git
cd sentinel-qa
pip install -r requirements.txt

# Set up environment variables (create .env file)
cat > .env << EOF
SAMBANOVA_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_token
JIRA_PROJECT_KEY=PROJ
DATABASE_URL=sqlite:///./sentinel.db
EOF

# Initialize database
python -c "from core.db_client import DBClient; DBClient()"

# Terminal 1: Start FastAPI Gateway
uvicorn api.main:app --reload --port 8000

# Terminal 2: Start HITL Dashboard
streamlit run approval_app.py

# Terminal 3: Generate a test plan
python agents/requirement_analyst.py

# Terminal 4: Run tests
pytest tests/test_engine.py -n auto
📁 Project Structure
text
sentinel-qa/
├── agents/
│   ├── requirement_analyst.py   # AI generates test plans from text
│   └── bug_reporter.py          # AI triages failures + creates Jira tickets
├── api/
│   ├── main.py                  # FastAPI application
│   └── schemas.py               # Pydantic models
├── core/
│   ├── action_registry.py       # Playwright action mappings
│   ├── ai_factory.py            # Multi-LLM provider with fallback chain
│   ├── api_client.py            # API contract validation
│   ├── db_client.py             # SQLite with WAL mode
│   ├── jira_client.py           # Jira Cloud API wrapper
│   └── models.py                # SQLAlchemy models
├── data/
│   └── test_plans/approved/     # Legacy YAML (being phased out)
├── tests/
│   └── test_engine.py           # Main pytest executor
├── scripts/
│   └── migrate_yamls.py         # One-time YAML → SQLite migration
├── approval_app.py              # Streamlit HITL dashboard
├── conftest.py                  # pytest hooks + Allure integration
├── pytest.ini                   # pytest configuration
├── config.yaml                  # AI provider + model selection
├── requirements.txt
└── .env
⚙️ Configuration
config.yaml

yaml
project: "OrangeHRM-Pilot"
ai_provider: "sambanova"  # Options: sambanova, groq, ollama
base_url: "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
model: "Meta-Llama-3.3-70B-Instruct"
LLM Fallback Chain: SambaNova → Groq → Ollama (automatic if provider fails)

🔄 Core Workflows
AI Test Plan Generation

python
analyst = RequirementAnalyst()
analyst.generate_test_plan("User logs in with Admin/admin123 and verifies dashboard")
# → POSTs to FastAPI → status: "pending"
Human Approval → Open http://localhost:8501 → Review/Edit steps → Click Approve → status: "approved"
Test Execution → pytest tests/test_engine.py -n auto → Fetches approved plans → Parallel execution

Failure Triage (Automatic) → Screenshot captured → BugReporter queries SQLite history → LLM analyzes pattern → Jira ticket created → Screenshot attached → Allure updated

🧪 Current Limitations (Alpha Status)
Limitation	Status	Workaround
Production metrics	Not yet available	Local benchmarks only
Visual regression	Not implemented	Manual checks only
Test impact analysis	Not implemented	Runs all approved tests
Prompt versioning	Not implemented	Manual tracking
Multi-environment support	Hard-coded URLs	Edit config.yaml

🛣️ Roadmap
Add visual regression with Playwright screenshots
Implement test impact analysis (git diff → selective execution)
Prompt versioning and A/B testing
Production performance benchmarks
Kubernetes deployment manifests
Slack/Teams notifications

🤝 Contributing
This is an open-source prototype. Contributions welcome!
Fork the repository
Create a feature branch
Commit your changes
Open a Pull Request
Areas needing help: Additional action registry methods, New LLM provider integrations, Dashboard improvements, Documentation

⚠️ Disclaimer
Alpha Status: This software is provided "as is" without warranties. It demonstrates concepts but hasn't been hardened for production workloads. Use at your own risk.
No Production Metrics Claimed: The performance improvements described in blog posts are directional targets based on local development benchmarks, not production deployment metrics.

📝 Related Content
Part 1: From Manual Scripts to Self-Driving QA
Part 2: Building a QA Operating System
Part 3: The Final Verdict — From Script to Ecosystem
