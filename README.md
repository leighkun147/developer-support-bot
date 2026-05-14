# 🤖 Developer Support Bot

A Python-based developer support assistant for junior engineers, with Human-In-The-Loop (HITL), Human-On-The-Loop (HOTL), and Human-Out-Of-The-Loop (HOOTL) modes. It combines a knowledge base with real-time escalation to a senior engineer for critical or unknown issues.

## 🚀 Features
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
Empower junior developers with instant, typo-tolerant error help, while ensuring critical or ambiguous issues are escalated to a senior engineer for safe, high-quality support.

## 📄 License
MIT
