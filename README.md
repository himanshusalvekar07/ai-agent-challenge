# ai-agent-challenge
Coding agent challenge which write custom parsers for Bank statement PDF.

🤖 Karbon AI Agent

An autonomous AI agent that generates custom parsers for bank statements (PDF → DataFrame) using the Groq LLM.
It can plan → write parser code → test → refine itself (self-debugging loops).
The project supports both CLI mode and a Streamlit UI for interactive usage.

✨ Features

🔄 Agent loop (plan → generate → run tests → self-fix ≤3 attempts)

📑 Bank statement parser generation (parse(pdf_path) -> pd.DataFrame)

✅ Schema validation with provided CSV (DataFrame.equals)

💻 CLI interface (python run.py --target icici)

🌐 Streamlit web UI for chatting with agents (Code Assistant, Research Analyst, Creative Writer, General Assistant)

🔒 Environment variable management with .env file

📦 Modular structure (agent_tools.py, config.py, utils.py)

📂 Project Structure
karbon-ai-agent/
│── agent_tools.py      # Tools used by the agent
│── app.py              # Streamlit UI
│── config.py           # Configurations (keys, models, UI settings)
│── run.py              # CLI entry point
│── utils.py            # Helper functions
│── requirements.txt    # Dependencies
│── .gitignore          # Ignore venv, .env, caches
│── .env                # Store your API keys (not committed)


⚙️ Installation
1. Clone the repo
git clone https://github.com/your-username/karbon-ai-agent.git
cd karbon-ai-agent

2.Install Dependencies
pip install -r requirements.txt

3. Set environment variables

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

4. Run Streamlit UI
streamlit run app.py


Features:

Select agent type (Code Assistant, Research Analyst, Creative Writer, General Assistant).

Chat with Groq-powered LLM.

Export chat history as JSON.

Track conversation statistics.

Agent Architecture

The Karbon AI Agent follows a lightweight plan → act → observe → refine loop:

+-----------+       +----------+       +----------+       +-------------+
|  Planner  | ----> |  Coder   | ----> |  Tester  | ----> |  Self-Fixer |
+-----------+       +----------+       +----------+       +-------------+
       ^                                                          |
       +----------------------------------------------------------+


Planner: decides which parser to build.

Coder: generates custom_parsers/<bank>_parser.py.

Tester: validates output vs CSV schema.

Self-Fixer: retries (≤3 attempts) until tests pass.

Evaluation Criteria (per assignment)

Agent autonomy (self-debug loops) → 35%

Code quality (typing, docs, clarity) → 25%

Architecture clarity → 20%

Demo ≤60s → 20%


