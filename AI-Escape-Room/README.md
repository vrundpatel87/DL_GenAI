# AI Escape Room — Version 1 & Version 2

A small Python + Streamlit escape-room game based on the course assignment. Gemini acts as the Game Master/narrator; Version 2 moves authority over game rules into deterministic Python functions.

## Features

- **Version 1 — Interactive AI:** conversational Game Master, room exploration and session conversation history.
- **Version 2 — Reliable AI:** structured state, inventory, action validation, fixed puzzle solutions, invalid-action handling and basic prompt-injection resistance.
- Works without an API key using a local fallback narrator. Add a free Gemini API key to enable Gemini responses.
- Unit tests for normal play and challenging/adversarial inputs.

## Story and solution path

1. Examine the bookshelf → discover drawer combination `2718`.
2. Enter `2718` in the drawer → collect the brass key.
3. Examine the desk and take the UV lens.
4. Use the UV lens on the painting → reveal exit code `0426`.
5. Unlock the door using the brass key and `0426`.

The codes are intentionally visible in source code for the instructor to inspect. Do not read them if you want to play normally.

## Requirements

- Python 3.10 or newer
- Internet connection for Gemini API calls
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

Google's Gemini API has a free tier, but model availability and rate limits can change. See the [official pricing page](https://ai.google.dev/gemini-api/docs/pricing). This project does not require a paid API plan. If the free tier is unavailable or rate-limited, the game still runs using the fallback responses.

## Installation (Windows / macOS / Linux)

```bash
# 1. Clone your repository
git clone https://github.com/YOUR-USERNAME/AI-Escape-Room.git
cd AI-Escape-Room

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# macOS / Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your local environment file
# Windows PowerShell:
Copy-Item .env.example .env
# macOS / Linux:
cp .env.example .env

# 5. Edit .env and paste your Gemini API key
# GEMINI_API_KEY=your_real_key
```

## Run

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`). Choose Version 1 or Version 2 in the sidebar.

## Run tests

```bash
pytest -q
```

## Project structure

```text
AI-Escape-Room/
├── app.py
├── game_engine.py
├── gemini_client.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── REPORT.md
├── ARCHITECTURE.md
├── TEST_PLAN.md
└── tests/
    └── test_game_engine.py
```

## Version comparison

| Area | Version 1 | Version 2 |
|---|---|---|
| Game Master | Gemini controls conversational response | Gemini narrates approved Python outcome |
| State | Chat history + lightweight snapshot | Structured Python dictionary |
| Puzzle validation | Prompt-guided | Deterministic Python checks |
| Inventory | Narrative | Explicit list |
| Invalid actions | May be inconsistently handled | Rejected without state mutation |
| Adversarial input | Not in original scope | Basic rule-override/admin/secret requests blocked |

## Architecture and testing

See [ARCHITECTURE.md](ARCHITECTURE.md) and [TEST_PLAN.md](TEST_PLAN.md). The test suite can be run locally with `pytest -q`.

## GitHub workflow

Create an empty GitHub repository named `AI-Escape-Room`, then:

```bash
git init
git add .gitignore requirements.txt .env.example
git commit -m "chore: add project configuration"

git add app.py gemini_client.py
git commit -m "feat: add Streamlit interface and Gemini game master"

git add game_engine.py tests/
git commit -m "feat: add validated game state and puzzle engine"

git add README.md ARCHITECTURE.md TEST_PLAN.md REPORT.md
git commit -m "docs: add architecture, tests and project report"

git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/AI-Escape-Room.git
git push -u origin main
```

Make additional commits as you improve the project. Never commit `.env`, API keys, passwords, virtual environments or generated caches. Confirm `.env` is ignored with `git status`.

## Limitations

- Version 1 intentionally relies on the model and conversation, so it may drift or invent progress.
- Version 2's natural-language parser supports the documented command patterns; it is not a general-purpose language understanding system.
- The adversarial checks are basic defensive examples, not a security guarantee.
- Streamlit session state lasts for the current browser session and is not a persistent database.
- Gemini free-tier quotas, model names and regional availability can change.
