# PEC — S28 Software Developer Support Bot

## Scenario Name
S28 — Software Developer Support (HOOTL / HITL / HOTL)

## Usage Story (1–2 sentences)
A junior developer types an error name or a short problem description into `bot.py`. The bot answers locally from `bilgi.txt` when it is confident, and escalates to a senior engineer (via `operator.py`) when the situation is risky or uncertain.

## Target User
- Primary: Junior developer who needs fast, typo-tolerant debugging help.
- Secondary: Senior engineer/operator who provides expert guidance for ambiguous or high-risk cases.

## Mode Logic
### HOOTL (Human-Out-Of-The-Loop)
- Reads `bilgi.txt` ("Key: Solution" lines).
- Computes Levenshtein distance between the user input and each error key.
- If the best distance is **<= 3**, prints the matched solution.
- If the best distance is **> 3**, prints: `Hata bulunamadi.`

### HITL (Human-In-The-Loop)
- Skips `bilgi.txt` completely.
- Writes the user message to `kuyruk.txt` as `BOT:<message>`.
- Waits until the operator appends a response as `OPERATOR:<advice>`.
- Prints only the operator advice to the junior developer.

### HOTL (Human-On-The-Loop) — Escalation Reasons
HOTL answers automatically only when it is safe and confident. Otherwise it escalates.

**Danger keywords (immediate escalation)**
| Keyword | Why it’s a “Danger” Word |
|---|---|
| database / db | Modifying or querying a database is high-risk; a bot error could delete user data. |
| production / prod | Any error in the live environment needs a human’s eyes to prevent downtime. |
| deleted / drop | These suggest data loss, which requires immediate expert intervention. |
| crash | If the whole system is down, a bot’s simple fix might not be enough. |
| security / auth | Security breaches or login failures are too sensitive for a basic bot to handle. |
| payment / money | Financial transactions involve high liability; a human must oversee the fix. |
| deployment | If the pipeline is broken, a human needs to verify the fix before pushing code live. |

**High uncertainty escalation**
- If the best Levenshtein distance is **> 4**, the bot admits uncertainty and escalates to the operator.

**No match found escalation**
- If the bot cannot find any usable match (no similar keyword / invalid parse), it routes the request to the operator instead of returning a generic "not found".

## Test Samples (5 inputs)
These samples demonstrate behavior (run `operator.py` in a second terminal for HITL/HOTL escalations).

1) Input: `SyntaxError` (HOTL)
- Expected: Auto-answer from `bilgi.txt` (close match).

2) Input: `SyntaXEror` (HOOTL)
- Expected: Auto-answer if distance <= 3 (typo-tolerant).

3) Input: `there is a problem with the dataset` (HOTL)
- Expected: If distance > 4 / no match => escalates to operator.

4) Input: `database migration failed` (HOTL)
- Expected: Immediate escalation due to danger keyword (`database`).

5) Input: `payment refunded twice` (HOTL)
- Expected: Immediate escalation due to danger keyword (`payment`).

## Required Files Checklist
- `PEC.md` — This document.
- `bilgi.txt` — >= 12 lines of "key: answer" entries for debugging help.
- `bot.py` — Single script supporting `hootl`, `hitl`, `hotl` via `sys.argv[1]`.
- `operator.py` — Separate script that monitors `kuyruk.txt` and writes `OPERATOR:` replies.
