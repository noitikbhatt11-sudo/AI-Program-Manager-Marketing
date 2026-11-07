# n8n workflow spec (build time ≈ 2–3 h; no live export included — I could not run n8n in my environment)

| # | Node | Type | Config |
|---|---|---|---|
| 1 | Class Recorded | Webhook / GCS trigger | Fires on `recording.completed` or new `.vtt` in the transcripts bucket |
| 2 | Fetch Metadata | Google Sheets / CRM | Lookup by class_id → subject, age_band, teacher, market, **consent_on_file** |
| 3 | Consent Gate | IF | `consent_on_file != true` → write `NO_CONSENT` row, stop |
| 4 | Download VTT | HTTP Request | GET transcript URL |
| 5 | Pre-filter | Code (Python/JS port of `preprocess_vtt.py`) | Outputs masked transcript + flags |
| 6 | Quality Alert | IF → Slack | ≥3 negative-tone teacher turns → #academic-quality (private) |
| 7 | Moment Miner | HTTP Request → Claude API | System = `prompts/01…`; user = meta + flags + transcript; temp 0.2; JSON only |
| 8 | Validate | Code | JSON schema; each `verbatim` must be a substring of transcript; drop score < 6 |
| 9 | NO_MOMENTS? | IF | Write row `NO_MOMENTS` (counts toward audit pool) |
| 10 | Cut Snippet | Execute Command (ffmpeg) | `-ss start-8 -to end+8` from MP4 |
| 11 | Visual Verifier | HTTP Request → video model | Prompt 02; REJECT → close with code V1–V7 |
| 12 | Write Candidate | Google Sheets | Row per moment, `status=NEEDS_QA`, deep link `video#t=start-5` |
| 13 | Notify QA | Slack | Daily digest to #marketing-qa |
| 14 | On ACCEPT (Sheet trigger) | Google Sheets trigger | → Prompt 03 (hooks/captions) → create Drive folder → Slack #creative card |
| 15 | Weekly Report | Cron | Pivot of precision, reject codes, time-to-brief, cost → Slack |

Phase-1 shortcut: skip nodes 10–11 and let the human QA run the visual checklist from the Sheet.
