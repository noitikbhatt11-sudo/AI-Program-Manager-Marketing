# Bambinos.live — AI PM (Marketing) Take-Home: Live Class → Ad-Brief Pipeline

**Start here:** `Bambinos_AI_PM_Marketing_Case_Report.pdf` (Deliverables A, B, D + C summary; source `docs/Case_Report.md`). **Run it:** `docs/SETUP_GUIDE.md`.

```
prompts/   01_moment_miner_system_prompt.md · 02_visual_verifier_prompt.md · 03_hook_and_caption_writer.md
n8n/       bambinos_class_to_brief.workflow.json (importable) · code_preprocess.js · code_validate.js · claude_api_test.sh
sheet/     Bambinos_Brief_Tracker_TEMPLATE.xlsx  (Candidates, Class_Log, Reason_Codes, Metrics, Unit_Economics — formulas live)
scripts/   preprocess_vtt.py · briefs_data.py · build_outputs.py · build_sheet.py · unit_economics.py
outputs/   ad_briefs.csv|md (5 briefs) · rejected_moments_and_flags.md · sample_no_moments_maths.json · unit_economics.* · stats/
docs/      Case_Report.md · SETUP_GUIDE.md · loom_script.md · submission_checklist.md · n8n_workflow_spec.md
```

## What was tested vs not
| Tested | Not tested (needs your keys/accounts) |
|---|---|
| Python + JS pre-filters agree on all 4 real classes · validator catches fabricated quotes / low scores / bad JSON · workflow JSON structure · Sheet formulas = Python model | Live n8n import · Claude API call · Google Sheets OAuth |

## Method & honest limits
- Input: the 4 real VTT transcripts. Briefs were produced by applying Prompt 01's rules in a Claude session (not by a scheduled n8n run); scores are uncalibrated until editors label accepts/rejects.
- Video: the repo's `.mp4` files are Git-LFS pointers, so visual fields are **UNVERIFIED** and listed as required checks.
- §A1 competitor research uses Meta Ad Library records via a third-party gallery (PlanetSpark, Vedantu, BrightChamps); Bhanzu and a direct Library audit are still to be done by hand.
- Economics inputs are assumptions (`sheet/…Unit_Economics`, `scripts/unit_economics.py`).
