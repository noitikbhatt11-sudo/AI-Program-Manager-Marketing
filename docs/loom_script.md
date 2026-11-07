# Loom script (2:45) — screen recording

**0:00–0:20 | The problem & thesis.** *Show the case PDF page 1.* "Finding ad moments is a filtering problem: 85–90% of review time is wasted, so I built a pipeline that is rewarded for saying no — cheaply and early — and only sends humans a short list."

**0:20–0:55 | Pre-filter.** *Terminal or n8n Preprocess node.* Run `preprocess_vtt.py` on Maths and Gita. Point at: Maths child talks 4% / 8 negative-tone turns → Quality alert; English 13.8 min silence; Gita 60 s silence = meditation (flag, not verdict). "Free and deterministic — runs before any AI spend."

**0:55–1:40 | The prompt.** *Open prompts/01.* Show the 3 ideas: (1) hard gates before score — a compliance fail can't be averaged away; (2) `NO_MOMENTS` is a first-class answer; (3) mandatory `visual_risk` + `visual_checks_required` — the model must confess what it can't see.

**1:40–2:20 | Output.** *Open Sheet → Candidates.* Show GITA-01: hook, verbatim, 7.8 score breakdown, geo-fit (GCC = Low), compliance flags, editor instructions. Then show the validator catching a fabricated quote (run `node` test or the DROPPED_UNVERIFIED_QUOTE row). Then Class_Log: Maths = NO_MOMENTS + quality alert.

**2:20–2:45 | Business case & rollout.** *Unit_Economics tab.* "₹1,588 → ₹339 per usable clip; 15× on sourcing, ~6× end-to-end — and still ~5× at 40% precision." Close with the 30-60-90: prove with a blind test, scale with automation + A/B, optimise with ad-performance feedback. "Limits: I couldn't watch the videos (LFS stubs) — that's exactly why the verifier layer exists."

**Tip:** do one rehearsal; keep the cursor still while talking; don't read the slides.
