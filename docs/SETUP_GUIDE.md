# Setup guide — from zero to a working run (≈45–60 min)

## 1) Google Sheet (5 min)
1. Open Google Drive → **New → File upload** → `sheet/Bambinos_Brief_Tracker_TEMPLATE.xlsx` → open with **Google Sheets** → **File → Save as Google Sheets**.
2. Keep the tab names and header names unchanged (n8n maps by header name).
3. Copy the Sheet ID from the URL: `docs.google.com/spreadsheets/d/<THIS_PART>/edit`.

## 2) n8n (10 min)
1. Sign up at n8n.io (Cloud free trial) — or `docker run -it -p 5678:5678 n8nio/n8n` for free local use.
2. **Workflows → Import from file** → `n8n/bambinos_class_to_brief.workflow.json`.
3. Credentials (n8n will show red nodes until set):
   - **Claude: Moment Miner** → *Header Auth* credential: Name `x-api-key`, Value = your key from console.anthropic.com.
   - **Sheet: Candidates / Sheet: Class_Log / Log: NO_CONSENT** → Google Sheets OAuth2 credential; paste your Sheet ID in each node's *Document* field (replace `PASTE_YOUR_GOOGLE_SHEET_ID`).
4. Open **Config (per class)** and set `class_id, subject, market, age_band, consent_on_file, vtt_url`.
   The default `vtt_url` is the public Gita transcript from the official repo README.

## 3) Run
**Execute workflow.** Expected: rows appear in *Candidates* (decision = PENDING) and a status row in *Class_Log*. Re-run with the other three transcript URLs from `marketing/README.md` (English, Maths, Science). Maths should log `NO_MOMENTS` with `quality_alert = YES`.

## 4) What the nodes do (and where to demo)
`Preprocess` (flags + name masking) → `Consent OK?` → `Claude: Moment Miner` (Prompt 01) → `Validate + Shape Rows` (drops any quote that isn't in the transcript, drops score <6, handles bad JSON) → `Candidates` / `Class_Log`.

## 5) Troubleshooting
| Symptom | Fix |
|---|---|
| HTTP 400 from Claude mentioning a parameter | Remove optional params from the body; keep `model, max_tokens, system, messages` |
| HTTP 401 | Header Auth name must be exactly `x-api-key` |
| `PARSE_ERROR` in Class_Log | Model returned prose; re-run, or tighten "return ONLY JSON" |
| Sheet node says columns not found | Header row names changed — restore from the template |
| Download VTT returns binary | In that node set Response Format = Text, property name `vtt` |
| No API key / no n8n access | Paste Prompt 01 into a Claude Project and feed `outputs/stats/*.llm.txt` manually — same output schema |

## 6) Honest status of this build
Tested here: the Code-node JavaScript (matches the Python pre-filter on all 4 classes; validator tested on real, fabricated and low-score quotes), workflow JSON structure, and sheet formulas. **Not tested here:** the live n8n import, the Claude API call and the Google Sheets OAuth (no keys/accounts in my environment) — so budget ~15 min for first-run fixes using the table above.
