---
title: "Live Class → Scroll-Stopping Ad Content: An AI Moment-Mining & Production Pipeline"
subtitle: "Bambinos.live · AI Program Manager (Marketing) · Take-Home Case — Deliverables A, B, D (+ C summary)"
---

# 0. Executive summary

**The problem is a filtering problem, not a video-editing problem.** ~85–90% of review time is spent on classes that contain nothing usable, so the highest-leverage design choice is a pipeline that is *rewarded for saying "no"* cheaply and early, and that sends humans only a short list of pre-vetted candidates.

**What I built (all in the GitHub repo):**

| Piece | What it is |
|---|---|
| `scripts/preprocess_vtt.py` | Free, deterministic pre-pass: merges cues, masks names, and computes silence gaps, talk-share, monologues, PII and negative-tone flags |
| `prompts/01…03` | Production prompts: **Moment Miner** (gates → buckets → 10-pt rubric → JSON brief), **Visual Verifier** (video model; closes the audio-vs-visual gap), **Hook/Caption writer** |
| `outputs/` | Briefs for the 4 real classes (CSV + MD), rejected-moment log, a `NO_MOMENTS` + quality-alert example, unit-economics model |
| This report | Taxonomy, rubric, exclusions, SOP, KPIs, 30-60-90 |

**What the four real classes taught me (this shaped the design):**

- **Only 1 of 4 classes was a strong source.** Gita yielded 4 SHIP-tier moments; Science 1 REVIEW; **English and Maths yielded zero.** A pipeline that forced "3 clips per class" would have shipped bad content.
- **Maths is a compliance event, not a content source:** the teacher shames the child for ~10 minutes (8 flagged turns, "how many times do I need to explain…", "your father always says she doesn't study"). The pipeline must *route this to Academic Quality*, not just skip it.
- **English contained 5 distinct hard-exclusion types** (child's travel/location, family at the door, a "$100" payment remark, teacher guilt-tripping, and a static-photo teacher camera) plus **13.8 min of transcript silence** (the child writing — dead footage).
- **Gita's "silence" is the opposite of dead air:** the 60 s gap before the best Spark moment is a guided meditation — potentially the hero visual. A naive "drop silence" rule would delete the ad. So silence is a *flag for visual verification*, never a verdict.
- **A hidden PII hit:** the child states her birthday (month/date/year) mid-way through Gita. Regex alone would miss it; the LLM gate + human check catch it.

**Headline economics (500 classes/week, stated assumptions, §D1):** cost per usable clip **₹1,588 → ₹339 (−79%)**; sourcing hours **250 → ~17/week (≈15×)**; end-to-end hours per clip **≈5.8× lower**. I deliberately report end-to-end (not just the flattering sourcing number).


# A. Research & Creative Taxonomy

## A1. What makes a parent stop scrolling? — competitor research (sourced)

**Method.** I read public Meta Ad Library records as summarised by the Hawky ad-gallery (counts through 12 Aug 2026; creative categories, hook types and emotions are *model-assigned by that tool*, and **public libraries carry no spend, impression or conversion data**, so run-length is a fatigue/conviction proxy, not proof of conversion). I could not open the live Ad Library UI from my environment, so Bambinos.live's own ads and **Bhanzu (not in the source)** remain for the 2-hour manual audit in the checklist.

| Brand | Public ads (live) | Format | Most-repeated openers & angles | Offer / CTA | Creative turnover |
|---|---|---|---|---|---|
| **PlanetSpark** | 1,989 (708) | **78% video** (category avg 47%) | "Public speaking for kids"; "Are you even a leader if you can't speak properly?"; shy-child-to-confident-speaker *transformation* and parent testimonials; hook types: problem-solution 452, benefit 362, curiosity 146 (of 1,036 classified) | Free trial/demo; "Book now" on 1,941 of 1,989 ads; 98% value-led, ~1% discount | **61% of dated ads ran <1 week**; average life 46 d vs 70 category |
| **Vedantu** | 2,168 (291) | 47% video / 53% static | "Get FLAT 40% OFF" (58 ads); scholarship test; topper scorecards ("I scored 98.4%…"); "No silent bench here"; price-anchoring is the top angle; emotions: aspiration + fear of missing out | Discount/scholarship; "Learn more" 987, "Book now" 433 | Typical 32 d; 620 ads <1 week |
| **BrightChamps** | 3,053 (208) | 52% video | Mostly coding; logic/critical-thinking creative | "Book now" on 2,528 | Typical 71 d |
| **Bhanzu** | — | — | *Not covered by the source → manual audit* | — | — |

**What this means for Bambinos (my reading, to be tested):**

1. **Creative volume is the competitive moat, and the bottleneck.** PlanetSpark retires most ads within a week and runs ~80% video; Vedantu's top reused ads are variants of the same few assets. A brand that cannot produce fresh, credible video fast is stuck recycling — which is exactly the manual bottleneck this pipeline removes.
2. **The visible openers are offer-, claim- or problem-led** (discounts, toppers' scores, "are you even a leader if…"). From these sources I cannot tell whether any competitor runs *unscripted real-class moments* — that is the first thing to check in the Library, because it decides how differentiated Bambinos' best format really is.
3. **"Transformation" is the dominant emotional promise** (PlanetSpark's shy-child-to-champion; Vedantu's topper stories). Bambinos can show the *observable seeds* of transformation — a child retelling a story, asking for a longer meditation — **without result claims**, which is both more credible and safer (see CCPA guidance in A4). This is why buckets B2 and B4 exist.
4. **Parent anxieties named in the ads are speaking/confidence (PlanetSpark), marks/ranks (Vedantu) and future skills (BrightChamps).** Bambinos' small-group, story-driven classes map best to *confidence + joy + retention*.
5. **Sound-off default:** with 50–80% video share in this category, the first 3 s must work as text + face + gesture; every brief therefore carries on-screen hook text and caption instructions.

**Still to verify manually (2 h):** log 20 longest-running active ads per brand (+ Bambinos.live) in India and US/UAE: *hook, who speaks (child/teacher/VO), real vs staged, proof element, CTA, length*, then tag each with the six buckets.

**Evidence from the real classes (child talk-share, a proxy for "child is the star"):** English 51% · Gita 19% · Science 11% · Maths 4%. Talk-share alone does *not* predict quality (English is child-heavy but low-quality) — a prioritisation signal, never a score.

## A2. Moment buckets (6)

| # | Bucket | What the parent sees | Hook pattern | Real example found |
|---|---|---|---|---|
| B1 | **Spark** | Unprompted delight/humour/"more please" | Child's own words in quotes | Gita 00:40:55 — "I feel like it wasn't that long" after a meditation |
| B2 | **Proof of Learning** | Child recalls/explains/solves in own words | "Last class → now" | Gita 00:03:30 — retells last week's story from memory |
| B3 | **Story-Mode** | Suspense, prediction, role-play; child leaning in | Cliffhanger question | Gita 00:19:32 — "You want Shiva to help this boy?" "Yes, yes!" |
| B4 | **Seen & Supported** | Teacher notices child-specific detail; hesitant child succeeds | "She almost gave up…" (only if literally on-camera) | *None found in the 4 classes* — the best bucket for 1:few attention; needs video |
| B5 | **Wow Concept** | Concept made tangible via demo/analogy/game | "Can you tell which is alive?" | Science 00:17:36 — touch-me-not vs dry twig |
| B6 | **Values & Life Skills** | Calm, focus, bravery, culture in practice | Child's answer to a big question | Gita 00:26:38 — "Why do we pray?" |

*Not a bucket:* teacher lecturing, recap, greetings, homework, tech chatter.

## A3. Scoring rubric (0–10) — gates first, then points

| Criterion | Max | 0 | Full marks |
|---|---|---|---|
| **H**ook in first 3 s | 2.0 | Needs context/intro | Question, surprise, emotion or cliffhanger a stranger can't scroll past |
| **A**uthenticity & child voice | 2.0 | Teacher monologue | Imperfect, specific, unscripted *child* carries it |
| **V**alue proof for parent | 2.0 | Nothing to learn | Parent can name the benefit (curiosity, retention, confidence, focus) |
| **S**ound-off legibility | 1.5 | Meaning only in audio | Works with burned-in captions + visible action |
| **P**roduction viability | 1.5 | Garbled ASR / no clean 10–20 s cut | Clean boundaries, intelligible audio, self-contained |
| **B**rand & trust fit | 1.0 | Cringe/off-brand | Warm, professional, culturally apt |

**Penalties:** −1.0 if the child's key line is garbled in ASR; −0.5 if teacher speaks >70% of the clip.
**Tiers:** **≥ 7.0 SHIP** · **6.0–6.9 REVIEW** (human decides) · **< 6.0 DROP.** A 9+ should be extremely rare. *Weights are v1 — recalibrated at Day 60 against real hook-rate/CPL data (§D3).*

## A4. Hard exclusions & compliance red flags (gates — they override any score)

| Code | Exclusion | Why / example from the data |
|---|---|---|
| **G1** | Child PII: name, school, location, **birthday/age**, phone, siblings/parents heard or seen | English: child's travel plans; Gita: birthday "January… 2021"; "my baby brother" |
| **G2** | Child embarrassed, scolded, wrong-answer struggle, "I don't understand" | Maths 00:46:09; English octopus correction |
| **G3** | Teacher negative tone: shaming, guilt-trips, parent complaints (**also raises a Quality alert**) | Maths ×8 turns; English "I'll cry now… I'm very angry" |
| **G4** | Unverified outcome claims (scores, ranks, "improved in X weeks", health claims from meditation) | Only literal, observable behaviour may be used |
| **G5** | Billing/sales/scheduling talk | Science: ~6 min with a parent on slots/batches; English "$100" |
| **G6** | Third-party IP/persons: chants, songs, cartoons, textbook pages, non-enrolled people | Gita chant track played 00:39:39–00:40:55 |
| **G7** | Child speech unintelligible → can't be captioned for sound-off | Garbled ASR in several Science/English cues |
| **G8** | Dead air / tech trouble / camera or lighting issues | Science 00:21:09 "I can't see the screen"; Gita "too dark in your room" |
| **G9** | Not self-contained in 20 s | Needs prior-lesson context |
| **M-REL** | Religious content → **India/diaspora only; GCC = do-not-run** without local review | Gita briefs |
| **M-DATA** | Verifiable consent on file per student; no child-targeted tracking; takedown path | **CCPA Coaching Guidelines (13 Nov 2024):** no false/exaggerated success, rank or guarantee claims; testimonials/photos of students need written consent obtained *after* the success (applies to coaching centres of >50 students and excludes creative/sports activities — counsel to confirm for Bambinos' academic subjects; I treat it as the standard for all ads). India **DPDP Act 2023** (verifiable parental consent for under-18s; restrictions on tracking/targeting children), **COPPA** (under-13, US), **UK Children's Code/GDPR**, Meta/ASCI rules on misleading claims. *Not legal advice — counsel to confirm current rules.* |

**Voice rule:** never clone a child's or teacher's voice (ElevenLabs only for a neutral narrator).

# B. End-to-End Workflow & SOP

## B1. Architecture (humans in **bold**)

**Class ends** → ① Ingest *(auto)* → ② Pre-filter *(auto)* → ③ AI mining *(auto)* → ④ Visual verify *(auto, candidates only)* → ⑤ **Human QA gate** → ⑥ Brief handoff *(auto)* → ⑦ **Edit** → ⑧ **Final compliance** → ⑨ Launch & learn *(auto + weekly review)*

*Reject codes from ③④⑤⑦⑧ all flow into one Sheet — the single source of truth that feeds the weekly prompt/rubric improvement loop.*

| # | Stage | Input → Output | Tool | Owner / SLA | Quality gate |
|---|---|---|---|---|---|
| 1 | Ingest | `recording.completed` → VTT + MP4 URL + metadata (subject, age band, teacher, market, **consent flag**) | n8n webhook + HTTP (transcripts already sit in a GCS bucket); CRM/Sheet lookup | Auto · <5 min | Missing transcript/consent → park in "Needs data" tab |
| 2 | Pre-filter | VTT → masked turns + flags (silence ≥45 s, talk-share, monologues, PII, tone) | `preprocess_vtt.py` (n8n Code node / Cloud Function) | Auto · <1 min | `consent≠true` → stop; ≥3 negative-tone teacher turns → **Quality alert** (Slack #academic-quality), mining continues on other windows |
| 3 | AI mining | Masked transcript + flags → JSON: 0–3 moments with timestamps, hook, bucket, verbatim, score, geo-fit, flags, visual checks | **Claude Sonnet-class** API (Prompt 01), temp 0.2; optional cheap triage pass (Haiku/Flash-class) for 5-min windows | Auto · <3 min | JSON schema validation; verbatim-substring check vs transcript (auto-reject any quote not found); score <6 dropped |
| 4 | Visual verify | Candidate window ±8 s → verdict JSON | ffmpeg cut → **Gemini-class video model** (Prompt 02), candidates only | Auto · <5 min | `REJECT` codes V1–V7 auto-close the brief with reason |
| 5 | **Human QA** | Candidate card + 30 s clip + deep link → ACCEPT / EDIT-WINDOW / REJECT(+reason) | Google Sheets (Airtable later) + Slack; Form dropdown | Marketing exec · ≤3.5 min each, same day | Required reason code on every reject (feeds §D3) |
| 6 | Handoff | Accepted brief → editor task | Sheet → Slack #creative card + Drive folder `BRIEFID_market_bucket` | Auto | Editor must see: window, hook, captions text, crop, **"never include"** list |
| 7 | **Edit** | Brief + source MP4 → 9:16 cut, captions, name-blur | CapCut / Premiere; OpusClip *only* for reframing; licensed music | Editor · ≈25 min/clip | Editor can bounce a brief with code `E-*` |
| 8 | **Final compliance** | Cut → publish-ready | 10-item checklist (below); consent proof linked | Marketer + (sampled) Legal | Zero PII/IP escapes; sign-off tick in Sheet |
| 9 | Launch & learn | Ad → performance by brief ID | Meta Ads Manager UTM `utm_content=BRIEFID_bucket_market` → Sheet/BigQuery | Perf marketer weekly | Hook rate / hold rate / CPL by **bucket & score band** → rubric weights |

**Tooling choices, and why:** *n8n* (self-hostable; handles webhooks, HTTP, Code, Sheets, Slack natively — Make/Zapier work equally); *Google Sheets* as v1 database (zero-training for marketers; swap for Airtable/BigQuery at 90 days); *Claude* for mining (long-context, strict-JSON, strong instruction-following on negative constraints); *a native-video model* only on 30–40 s candidate snippets (never whole classes — cost); *ElevenLabs* only for neutral VO in other languages.

## B2. Solving the audio-vs-visual gap (5 layers, cheapest first)

A transcript cannot tell us whether a camera is on, who is on screen, or what a silence *is*. The pipeline therefore **never trusts words alone**:

1. **Structural signals from the transcript (free).** Long silences (≥45 s), child talk-share, and teacher monologues are computed deterministically. A silence is a **flag, not a verdict**: *English 13.8 min of silence = child writing (dead footage, reject)*; *Gita 60 s silence = meditation (potential hero visual, verify)*.
2. **The miner must confess what it cannot see.** Every brief has mandatory `visual_risk` (LOW/MED/HIGH) and `visual_checks_required` (child camera on? face lit? teacher tile live or static image? screen-share content? name tile?). The prompt forbids pretending otherwise.
3. **Visual Verifier on candidates only (Prompt 02).** Returns structured verdicts and reject codes `V1_CAMERA_OFF … V7_EXPRESSION_MISMATCH` plus a *tighter recommended in/out* when the visual peak differs from the words, and `dead_footage_seconds`.
4. **Human 3-minute gate** using a deep link `video#t=start-5s` + the same checklist as a dropdown (works on day 1, before any video automation exists).
5. **Editor feedback loop.** Editors tag bounce reasons (`E-DEADFOOTAGE`, `E-NO-FACE`, `E-STATIC-TEACHER`); weekly counts decide which checks to automate next.

**Concrete catches from the sample data:** English 00:08:52 — the child says *"you put a picture of you there"* ⇒ the teacher tile is a **static photo** (editors would otherwise try to cut teacher footage that doesn't exist). Science 00:21:09 — "I can't see the screen" ⇒ shared-screen content may not have been visible/recorded. Gita 00:19:32 — words say "yes, yes!" but only video can confirm the *expression* matches ⇒ `V7_EXPRESSION_MISMATCH` check.

## B3. SOP for non-technical teams (one page)

**Marketing exec — daily QA (≈45 min for ~12 cards):**

1. Open **Candidates** tab, filter `status=NEEDS_QA`, sort by score.
2. Click the deep link; watch the 30 s clip **with sound and with sound off**.
3. Tick the visual checklist.
4. **ACCEPT** (green) if every check passes and you'd be proud for a parent to see it.
5. **EDIT-WINDOW** if the moment is right but the cut is off — type the new in/out.
6. **REJECT** — you *must* pick a reason: `R1 no-hook · R2 teacher-led · R3 child embarrassed · R4 PII/consent · R5 camera/face · R6 audio · R7 off-brand · R8 duplicate · R9 other(text)`.
7. Any teacher-tone concern → click **"Raise quality alert"** (never publish, never discuss in public channels).
8. Weekly: spot-check **10 random `NO_MOMENTS` classes** (recall audit) and log any miss.

**Editor — per brief:** read hook + "never include" list → cut per window → 9:16 crop on the child tile → burn captions (from audio, not ASR) → blur name tiles/background PII → licensed music only → export to the Drive folder → tick the 10-item publish checklist. *Bounce, don't fix, a bad brief* (reason code `E-*`).

**10-item publish checklist:** no child name (audio/caption/tile/chat) · no school/location/DOB · no sibling/parent audible or visible · consent proof linked · no third-party IP/music · no outcome claim · captions correct · hook ≤7 words · market-appropriate (religion/geo tag respected) · naming convention applied.

## B4. Edge cases handled unprompted

| Edge case | Handling |
|---|---|
| **Zero-moment classes** (50% of my sample) | `NO_MOMENTS` is a valid, cheap result; 5% weekly recall audit prevents the model from becoming lazily strict |
| **Teacher conduct problems** (Maths) | Quality alert to Academic team; class excluded from mining windows; the marketing team never sees the shaming clip |
| **Camera off / static photo / screen-share only** | §B2; brief downgraded to "teacher-led VO + slide" or rejected |
| **Hinglish / Malayalam code-mixing → garbled ASR** (Science, English) | Penalty + REVIEW tier; re-caption from audio; for US/GCC require clean English VO |
| **Regional fit** | Each brief carries `geo_fit` per market; religion = India/diaspora-only, GCC do-not-run; US framing = "screen time that's worth it" |
| **Consent revocation** | Brief IDs trace every ad to a class + student ID; 24 h takedown SOP; Sheet column `consent_revoked` blocks re-use |
| **Music/IP played in class** | Gate G6; editor mutes class audio under chants/songs |
| **Prompt injection inside transcripts** | Transcript is delimited as data; instruction-like text is flagged |
| **Multi-child classes** | Only enrolled-consented children usable; others cropped/blurred or class rejected |

# C. Working prototype — summary

Full prompts: `prompts/01–03`. Pre-processor: `scripts/preprocess_vtt.py`. Full briefs: `outputs/ad_briefs.csv` / `.md`. *The 4 transcripts → 5 briefs (4 SHIP, 1 REVIEW) + 2 zero-moment classes:*

| ID | Class · window | Bucket | Score | Tier | 3-s hook (on-screen) | Geo: IN / US-UK-CA-AU / GCC | Visual risk |
|---|---|---|---|---|---|---|---|
| GITA-01 | Gita 00:19:32–00:19:58 | B3 Story-Mode | **7.8** | SHIP | "A cliffhanger… in a Gita class?" | High / Med-High / Low | MED |
| GITA-02 | Gita 00:03:30–00:03:53 | B2 Proof of Learning | **7.7** | SHIP | "Last class's story. In her own words." | High / High / Med | LOW |
| GITA-03 | Gita 00:40:55–00:41:15 | B1 Spark | **7.4** | SHIP | "Her only complaint? Too short." | High / High / Med | **HIGH** |
| GITA-04 | Gita 00:26:38–00:27:19 | B6 Values | **7.0** | SHIP | "'Why do we pray?' A child answers." | High / Med / **DO NOT RUN** | MED |
| SCI-01 | Science 00:17:36–00:18:03 | B5 Wow Concept | **6.2** | REVIEW | "Touch this plant. What happens?" | High / Med-High / Med-High | **HIGH** |
| Maths | whole class | — | — | **NO_MOMENTS + Quality alert** | — | — | — |
| English | whole class | — | — | **NO_MOMENTS** (1 near-miss, 5.8) | — | — | — |

**Example brief (GITA-01)** — *Verbatim:* TEACHER "Do you think he is going to take him?" · CHILD "Yes. Yes." · TEACHER "But what about Shiva? Don't you think Shiva should come and help him?" · CHILD "yes, yes," · TEACHER "Let's find out. Let's see if Shiva is going to help this boy or not." *Editor:* cut 00:19:32–00:19:41 then jump to 00:19:48–00:19:58 (≈19 s); 9:16 crop on the child tile at "yes, yes"; cutaway to the story slide on "But what about Shiva?"; captions on; hold last frame 0.7 s on "or not."; **no chant audio**; blur name tile. *Compliance:* C-NAME, C-CONSENT, C-RELIGION (GCC off). *Must verify on video:* child camera on · expression genuine · teacher tile live.

# D. Business impact, metrics & 30-60-90 rollout

## D1. Unit economics — 500 live classes/week

**Assumptions (to be replaced by a Week-1 time study):** loaded cost ₹450/h · manual review 30 min/class · 0.18 usable clips/class (≈90/week; "1 in ~5.5 classes") · manual edit 45 min/clip · AI surfaces 150 candidates/week at 60% human acceptance · human QA 3.5 min/candidate · 5% recall audit (10 min each) · 4 h/week program upkeep · edit 25 min/clip with a brief · LLM ≈ ₹5/class · video verification ≈ ₹10/candidate · tools ≈ ₹2,000/week.

| Per week | Manual today | AI-assisted | Δ |
|---|---|---|---|
| Sourcing/review hours | 250.0 h | 16.9 h (QA 8.75 + audit 4.2 + ops 4) | **−93% (≈15×)** |
| Editing hours | 67.5 h | 37.5 h | −44% |
| **Total hours** | **317.5 h** | **54.4 h** | **−263 h (≈5.8×)** |
| Usable clips | 90 | 90 | = (same yield; the upside is in §D3) |
| Tools & AI spend | — | ₹6,000 | |
| **Total cost** | **₹1,42,875** | **₹30,488** | **−₹1.12 L/week (≈₹58 L/year)** |
| **Cost per usable clip** | **₹1,588** | **₹339** | **−79%** |

**Sensitivity (what if the model is worse than I assumed?):**

| Human acceptance | Candidates/wk | Usable clips | Hours/clip | ₹/clip | Hours/clip vs manual (3.5 h) |
|---|---|---|---|---|---|
| 40% | 150 | 60 | 0.70 | 414 | 5.1× |
| 60% | 150 | 90 | 0.60 | 339 | 5.8× |
| 60% | 250 | 150 | 0.57 | 302 | 6.2× |
| 75% | 250 | 187 | 0.54 | 279 | 6.6× |

**Reading it honestly:** the "10×" holds for *sourcing* (≈15×); end-to-end it is ≈5–6× because editing remains human. The bigger prize isn't savings, it's **throughput**: the ~263 freed hours/week can produce ~2–3× more creative variants per ad-rupee — the real constraint on scaling spend. Even at 40% precision the system remains ≈5× cheaper per clip, so the business case is robust to model quality.

## D2. Adoption & QA — earning trust from skeptical editors

**Principle: "AI proposes, humans dispose."** Editors and marketers hold a veto; the AI's job is to remove the worst task (scrubbing), not to judge taste.

- **Train (60-min workshop + 1-page SOP + 5-min Loom):** show the *rejected near-misses* and the Maths quality-alert example so people see the system is strict, not enthusiastic.
- **Champion model:** one editor and one marketer co-own the rubric and prompt changelog; they see every prompt change *before* it ships.
- **Make rejection frictionless and valuable:** one click + reason code; a weekly "**You said / we changed**" note shows each rejection pattern turning into a prompt fix.
- **Blind test before launch:** editors label 100 historical AI picks vs 100 manual picks without knowing the source — wins trust with data, not decree.
- **Scoreboard (public, weekly):** acceptance rate, minutes saved, clips live, bounce reasons.

**Metrics**

| KPI | Definition | D30 | D60 | D90 |
|---|---|---|---|---|
| **Precision / false-positive rate** | accepted ÷ surfaced (FP = editor/QA rejects) | ≥50% | ≥65% | ≥75% |
| **Recall proxy** | missed moments in audited `NO_MOMENTS` classes | ≤20% | ≤15% | ≤10% |
| **Time-to-brief** | class end → brief in Sheet | <24 h | <4 h | <1 h |
| **Editor min/clip** | in→publish-ready | 35 | 28 | ≤25 |
| **Clip→ad conversion** | accepted briefs live within 7 days | 40% | 55% | 65% |
| **Compliance escapes** | published clips with PII/IP/claim issues | **0** | **0** | **0** |
| **Hook rate / hold rate / CPL** | by bucket & score band vs manual-sourced control | baseline | A/B live | rubric reweighted |
| **Adoption** | % briefs actioned <24 h; weekly active reviewers | 70% | 85% | 90% |
| **Cost/usable clip** | §D1 formula | ≤₹600 | ≤₹450 | ≤₹350 |

**False-positive tracking:** every REJECT carries a code (R1–R9, V1–V7, E-*). A weekly pivot shows the top-3 reject reasons → each becomes (a) a new hard gate, (b) a rubric re-weight, or (c) a pre-filter rule. Prompt versions are changelogged `v1.0 → v1.x` with before/after precision.

## D3. 30-60-90 plan

| Window | Goal | Actions | Exit criteria |
|---|---|---|---|
| **Days 0–30 — Prove it** | Trust + baseline | **Wk 1:** time-study 2 editors × 40 classes to replace my assumptions; align taxonomy v1 + exclusions with the function head, Legal/Compliance (consent source, DPDP/COPPA, takedown SOP). **Wk 2:** run on the last ~500 historical classes in *shadow mode*; blind-label 100 picks. **Wk 3–4:** live on ~100 classes/week via Sheet + Slack (n8n flow v1, manual video check); 60-min training. | Precision ≥50%; 0 compliance escapes; editors confirm briefs save time; baseline CPL captured |
| **Days 31–60 — Scale** | Full coverage | Automate all 500 classes/week; add Visual Verifier; dashboards (precision, time-to-brief, bounce codes); weekly reject-code → prompt-fix loop; India + one export market (US/UK or GCC) variants; **A/B: AI-sourced vs manually-sourced creatives** on identical audiences | Precision ≥65%; ≥40 clips/week live; cost/clip ≤₹450 |
| **Days 61–90 — Optimise & institutionalise** | Compounding value | Feed hook-rate/CPL back into rubric weights; add word-level timestamps for exact cuts; multi-language caption variants; searchable **Moment Library** for performance marketers; route Quality alerts into teacher coaching; document SOP, hand over day-to-day ownership, define the next hire | Precision ≥75%; ≥90 clips/week; cost/clip ≤₹350; measurable CPL/hook-rate lift or no worse than manual at ≥3× volume |

**Top risks & mitigations:** *(1) a minor appears in a published ad without valid consent* → consent gate at step 2, mandatory proof at step 8, 24 h takedown; *(2) model silently over-strict or over-lenient* → recall audit + near-miss log; *(3) editor rejection of "AI work"* → veto, champions, blind test; *(4) ASR quality on code-mixed audio* → penalty + audio re-caption + (Day 60) test a stronger multilingual transcriber; *(5) vendor/price drift* → model-agnostic prompts, JSON contract, cost line in the dashboard.

# Sources (research)

- Hawky Ad Gallery — PlanetSpark: https://hawky.ai/ad-gallery/planetspark · Vedantu: https://hawky.ai/ad-gallery/vedantu · BrightChamps: https://hawky.ai/ad-gallery/brightchamps (public Meta Ad Library records to 12 Aug 2026; classifications model-assigned; no spend data).
- CCPA *Guidelines for Prevention of Misleading Advertisement in Coaching Sector, 2024* (13 Nov 2024): summaries at https://taxguru.in/corporate-law/ccpa-guidelines-target-misleading-coaching-advertisements.html · https://theprint.in/india/no-using-toppers-photos-without-consent-no-false-ads-what-are-govts-new-rules-for-coaching-centres/2356251 · https://www.tribuneindia.com/news/nation/centre-out-with-norms-to-regulate-misleading-ads-by-coaching-centres/amp

# Appendix — Build assets & reproduce

**Included build assets:** importable n8n workflow (`n8n/bambinos_class_to_brief.workflow.json`), Code-node JS for pre-filter and validator (tested against the Python version on all four classes), a Google-Sheets tracker template with dropdowns, KPI formulas and a live unit-economics model (`sheet/`), `docs/SETUP_GUIDE.md`, `docs/loom_script.md`.

## Reproduce in 15 minutes

1. `python scripts/preprocess_vtt.py marketing/transcripts/Gita_2125422751.vtt --out outputs/stats/` → produces `*.llm.txt`, `*.stats.json`.
2. Paste Prompt 01 into a Claude Project (or API system prompt); send `<class_meta>`, `<preprocess_flags>` (from stats.json) and `<transcript>` (from `.llm.txt`).
3. Validate the JSON; check every `verbatim` string is a substring of the transcript.
4. For each candidate, cut the window ±8 s with ffmpeg and run Prompt 02 on a video model (or use the human checklist).
5. `python scripts/build_outputs.py` and `python scripts/unit_economics.py` regenerate the tables.
