
# 🤖 Developer Support Bot

An intelligent, API-free Python assistant for junior developers. This project features three support modes—Human-In-The-Loop (HITL), Human-On-The-Loop (HOTL), and Human-Out-Of-The-Loop (HOOTL)—to deliver instant, typo-tolerant help for Python errors. All answers are generated **without calling any external APIs**: the bot relies solely on the curated knowledge base in `bilgi.txt` and, when needed, escalates to a senior engineer via `operator.py` for expert guidance. This ensures privacy, reliability, and full offline operation.


## 🚀 Features
- **No APIs, No Cloud, No LLMs:** All answers are generated locally using only the information in `bilgi.txt`—no internet connection or external services required.
- **HOOTL:** Answers common errors using a knowledge base (`bilgi.txt`).
- **HITL:** Forwards all questions to a senior engineer via `operator.py`.
- **HOTL:** Answers automatically unless the issue is risky or uncertain, then escalates to a human.
- **Manual Levenshtein distance** for typo-tolerant matching (no external libraries).
- **No dictionaries or LLM APIs** used—fully compliant with strict constraints.
- **Turkish code comments** for educational clarity.

## 🛠️ Files
- `bot.py` — Main CLI for junior devs (3 modes)
- `operator.py` — Senior engineer interface
- `bilgi.txt` — Knowledge base (error:solution)

## 🏁 Quick Start
```bash
# Clone the repo
https://github.com/leighkun147/developer-support-bot.git
cd developer-support-bot

# Run operator in one terminal
python3 operator.py

# Run bot in another terminal
python3 bot.py hootl   # or hitl, hotl
```


## 🎯 Project Goal
Empower junior developers with instant, typo-tolerant error help, while ensuring critical or ambiguous issues are escalated to a senior engineer for safe, high-quality support. All logic is transparent and local—no hidden API calls, no external dependencies, just pure Python and your own knowledge base.

## 📄 License
MIT
