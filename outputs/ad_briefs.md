# Extracted Ad Briefs — Bambinos sample classes

> Produced by applying `prompts/01_moment_miner_system_prompt.md` to the four provided transcripts (see README for method + honest limits). Video files in the repo are Git-LFS pointers, so **all visual fields are UNVERIFIED** and listed as required checks. Scores are AI-proposed and uncalibrated until editor accept/reject data exists.

## Class-level yield

| Class | Length | SHIP | Near-misses | Note |
|---|---|---|---|---|
| English_2125604619 | 53:31 | 0 | 1 near-miss | Child-heavy (51% of words) but PII, guilt-tripping, 13.8 min silence, static teacher photo. ZERO-MOMENT class. |
| Gita_2125422751 | 51:21 | 4 | — | Best yield: story suspense, child recall, spontaneous 'too short', values. Child speaks 19% of words. |
| Maths_2125736982 | 49:20 | 0 | 0 | ZERO-MOMENT + QUALITY ALERT: sustained teacher shaming; teacher 96% of words. |
| Science_2125687282 | 52:37 | 0 ship / 1 review | 1 near-miss | Teacher-led concept demo; garbled code-mixed ASR; 6 min parent/billing chat (PII). Hold for human. |

## Summary table

| ID | Class | Start–End | Bucket | Score | Tier | Visual risk | India / US-UK-CA-AU / GCC |
|---|---|---|---|---|---|---|---|
| GITA-01 | Gita | 00:19:32–00:19:58 | B3 Story-Mode | 7.8 | SHIP | MED | High / Med-High / Low |
| GITA-02 | Gita | 00:03:30–00:03:53 | B2 Proof of Learning | 7.7 | SHIP | LOW | High / High / Med |
| GITA-03 | Gita | 00:40:55–00:41:15 | B1 Spark | 7.4 | SHIP | HIGH | High / High / Med |
| GITA-04 | Gita | 00:26:38–00:27:19 | B6 Values & Life Skills | 7.0 | SHIP | MED | High / Med / DO NOT RUN |
| SCI-01 | Science | 00:17:36–00:18:03 | B5 Wow Concept | 6.2 | REVIEW | HIGH | High / Med-High / Med-High |

---

## GITA-01 — B3 Story-Mode — 7.8/10 (SHIP)

- **Class / window:** Gita_2125422751 · 00:19:32–00:19:58 (19s) · cut: 00:19:32–00:19:41 + 00:19:48–00:19:58 (jump-cut)
- **3-second hook (on-screen text):** A cliffhanger… in a Gita class?  
  alt: “You want Shiva to help this boy?” — “YES!”
- **First 3s (what we see/hear):** Teacher: “Do you think he is going to take him?” Child: “Yes. Yes.” (cut on the child's reaction)
- **Verbatim dialogue (names masked, ASR errors preserved):**
  - TEACHER: Do you think he is going to take him?
  - CHILD: Yes. Yes.
  - TEACHER: But what about Shiva? Don't you think Shiva should come and help him?
  - CHILD: Yes,
  - TEACHER: You want Shiva to help this boy?
  - CHILD: yes, yes,
  - TEACHER: Let's find out. Let's see if Shiva is going to help this boy or not.
- **Score:** H 1.6/2.0, A 1.6/2.0, V 1.4/2.0, S 1.2/1.5, P 1.1/1.5, B 0.9/1.0 = **7.8**
- **Geography fit:** India — High – story-led Gita is the USP; US/UK/CA/AU — Med-High – diaspora parents; frame as 'storytelling + culture'; GCC — Low – religious imagery; local review required
- **Compliance flags:** C-NAME: blur/crop Zoom name tile; C-CONSENT: confirm media release for student; C-RELIGION: geo-restrict (GCC)
- **Visual risk:** MED — checks required:
  - [ ] Is the child's camera ON and face visible during 'yes, yes'?
  - [ ] Does her expression show real excitement (not boredom)?
  - [ ] Is the story slide (Yamdev/Shivling art) on screen – usable as cutaway?
  - [ ] Is the teacher tile a live camera or a static photo?
- **Editor instructions:**
  1. Cut 00:19:32–00:19:41, then jump-cut to 00:19:48–00:19:58 (drops the repeated question at 00:19:42–00:19:47).
  2. 9:16 crop on the CHILD tile when she says 'yes, yes'; cutaway to story slide on the teacher's 'But what about Shiva?'.
  3. Burn-in captions (white, 2 lines max); hold final frame 0.7s on 'or not.' as the cliffhanger.
  4. Music: soft instrumental only. Do NOT use any chant track.
  5. Blur/crop name tile. No end-card claims.
- **Confidence an editor accepts:** 0.7

---

## GITA-02 — B2 Proof of Learning — 7.7/10 (SHIP)

- **Class / window:** Gita_2125422751 · 00:03:30–00:03:53 (20s) · cut: 00:03:30–00:03:53 (snap start to audio; cue-level timing only)
- **3-second hook (on-screen text):** Last class's story. In her own words.  
  alt: “And then he prayed, and prayed, and prayed…”
- **First 3s (what we see/hear):** Child: “…he had to pray to Shiva to get more, um, power…”  (teacher asked at 00:02:35 'what story did we do in our last class?')
- **Verbatim dialogue (names masked, ASR errors preserved):**
  - CHILD: [ASR garbled intro] … he had to pray to Shiva to get more, um, power to destroy the hundred boys.
  - TEACHER: hmm.
  - CHILD: And then he prayed, prayed, and prayed in, in the stormy day in the night, when all the animals came. he did not move. He was a
- **Score:** H 1.4/2.0, A 1.8/2.0, V 1.8/2.0, S 1.0/1.5, P 0.8/1.5, B 0.9/1.0 = **7.7**
- **Geography fit:** India — High – parents value recall + culture; US/UK/CA/AU — High – diaspora 'stay connected to roots'; GCC — Med – Indian-expat audiences only
- **Compliance flags:** C-NAME: child name is in the speaker label; mask in captions; C-ASR: first ~8s of the child's cue is garbled – re-caption from audio; C-AUDIO-VERIFY: if a human cannot understand the child on listen → REJECT; C-CONSENT
- **Visual risk:** LOW — checks required:
  - [ ] Is the child's speech intelligible when you listen (ASR was messy)?
  - [ ] Is the child's face on camera while retelling?
  - [ ] Does the child look confident, not hesitant (several 'first, first, first' stutters precede)?
- **Editor instructions:**
  1. Start at the audio onset of 'he had to pray to Shiva' (≈00:03:30), end on 'he did not move' (00:03:53).
  2. Remove 'um' pauses >0.4s with ripple trim; keep child grammar as spoken.
  3. Caption from the AUDIO, not the ASR; mask the name.
  4. Overlay small context tag at 0–3s: 'Teacher asked: what story did we do last class?'
  5. No claim about 'memory improving'.
- **Confidence an editor accepts:** 0.6

---

## GITA-03 — B1 Spark — 7.4/10 (SHIP)

- **Class / window:** Gita_2125422751 · 00:40:55–00:41:15 (20s) · cut: 00:40:55–00:41:15
- **3-second hook (on-screen text):** Her only complaint? Too short.  
  alt: “I feel like it wasn't that long.”
- **First 3s (what we see/hear):** Teacher: “Now you can open your eyes. So how was it?” Child: “Yes, but I feel like it wasn't that long.”
- **Verbatim dialogue (names masked, ASR errors preserved):**
  - TEACHER: Very good. Now you can open your eyes. So how was it? Was it good?
  - CHILD: Yes, but
  - CHILD: I feel like it wasn't that long.
  - TEACHER: [It] was in that long [sic/ASR: 'wasn't that long'] because we are trying to just teach you a method right now. … Once you understand the drill … then we'll do it for longer time.
- **Score:** H 1.5/2.0, A 1.8/2.0, V 1.2/2.0, S 1.1/1.5, P 0.9/1.5, B 0.9/1.0 = **7.4**
- **Geography fit:** India — High – focus/calm is a parent concern; US/UK/CA/AU — High – mindfulness-for-kids resonates; GCC — Med – OK if chant audio removed
- **Compliance flags:** C-IP: a chant track is played 00:39:39–00:40:55 – never use that audio; C-NAME; C-CONSENT; C-CLAIM: do not say 'reduces anxiety/improves focus'
- **Visual risk:** HIGH — checks required:
  - [ ] The 60s transcript silence before this (00:39:55–00:40:55) is the meditation: is the child seated, eyes closed, camera on? (could be the HERO visual, or dead footage)
  - [ ] Is the child smiling/relaxed when she says 'it wasn't that long'?
  - [ ] Is the chant audio bleeding into the clip start?
- **Editor instructions:**
  1. Open on the child's tile at 00:40:55; if the visual is a calm seated pose, add a 2s b-roll from 00:40:20–00:40:40 for context (check first).
  2. Cut at 00:41:15 after 'longer time.'
  3. Mute/replace chant audio with licensed neutral music; captions on.
  4. Never show the on-screen name tile.
  5. No health claims.
- **Confidence an editor accepts:** 0.65

---

## GITA-04 — B6 Values & Life Skills — 7.0/10 (SHIP)

- **Class / window:** Gita_2125422751 · 00:26:38–00:27:19 (20s) · cut: 00:26:38–00:26:48 + 00:27:09–00:27:19 (jump-cut; both cut points fall inside cues → snap to audio)
- **3-second hook (on-screen text):** “Why do we pray?” A child answers.  
  alt: From “to get things” to “because he is brave.”
- **First 3s (what we see/hear):** Child: “…to get stuff, to get things you want from [God].”  Teacher: “That's true. That's also the reason…”
- **Verbatim dialogue (names masked, ASR errors preserved):**
  - CHILD: get stuff, to get things you want from [God].
  - TEACHER: true. That's true. That's also the reason. But … the most important reason that we pray to God, because when we pray now, God gave us confidence. [sic/ASR]
  - TEACHER: … Why do you think he was not scared of anyone?
  - CHILD: Because, because he is brave,
- **Score:** H 1.2/2.0, A 1.5/2.0, V 1.6/2.0, S 0.9/1.5, P 1.0/1.5, B 0.8/1.0 = **7.0**
- **Geography fit:** India — High – values-based learning; US/UK/CA/AU — Med – diaspora only; GCC — DO NOT RUN – religious content
- **Compliance flags:** C-RELIGION: India/diaspora only; legal/brand review before US paid-social; C-ASR: teacher line has ASR errors; re-caption; C-CLAIM: do not imply praying causes bravery as a promised outcome; C-NAME; C-CONSENT
- **Visual risk:** MED — checks required:
  - [ ] Is the teacher's tile a live camera (the teacher speaks ~25s uninterrupted)?
  - [ ] Is the child visible on 'because he is brave'?
  - [ ] Is the stitched cut intelligible without the dropped middle?
- **Editor instructions:**
  1. Segment A: child's answer + teacher's 'That's also the reason'. Segment B: teacher's question + child's 'Because he is brave'.
  2. Add caption bridge between A and B: 'Teacher: what made him brave?'
  3. Show the child tile on every child line; teacher tile only for B's question.
  4. Quiet instrumental, captions on, no religious iconography added by us.
  5. Tag the asset India/diaspora-only in the naming convention.
- **Confidence an editor accepts:** 0.5

---

## SCI-01 — B5 Wow Concept — 6.2/10 (REVIEW)

- **Class / window:** Science_2125687282 · 00:17:36–00:18:03 (21s) · cut: 00:17:36–00:17:51 + 00:17:57–00:18:03 (≈21s; trim ≤1s)
- **3-second hook (on-screen text):** Touch this plant. What happens?  
  alt: Alive or not? A touch-me-not vs a twig.
- **First 3s (what we see/hear):** Teacher: “Now a student touches a touch-me-not plant… what happens to the leaves?”  (show plant visual if on slide)
- **Verbatim dialogue (names masked, ASR errors preserved):**
  - TEACHER: a student who touches a touch me not plant. You know what is a touch me not plant? And what happens when you touch it? What happens to the leaves?
  - TEACHER: when you touch it, what happens is that it's… folds inwards, okay.
  - TEACHER: But on the other hand she steps onto a dry wooden twig, okay. It just breaks.
- **Score:** H 1.2/2.0, A 0.8/2.0, V 1.4/2.0, S 1.1/1.5, P 0.8/1.5, B 0.9/1.0 = **6.2**
- **Geography fit:** India — High – STEM concepts; US/UK/CA/AU — Med-High – needs clean English VO; GCC — Med-High – STEM/English; re-record VO
- **Compliance flags:** C-ASR-HIGH: teacher code-mixes English + Malayalam; transcript garbled in places → re-caption/VO; C-CHILD-WEAK: child's line is unintelligible (excluded); C-CONSENT; Keep clear of 00:35:41–00:41:26 (parent/scheduling talk)
- **Visual risk:** HIGH — checks required:
  - [ ] Is the touch-me-not shown (photo/GIF/video) on the shared screen? If it is text-only → REJECT
  - [ ] Is the slide free of third-party watermarks/stock-IP?
  - [ ] Is the child visible reacting?
- **Editor instructions:**
  1. Use as a TEACHER-LED 'wow demo' with the slide as the main visual (not a class-capture).
  2. Replace audio with a clean English VO (ElevenLabs narrator voice — never clone teacher/child) or re-caption from audio.
  3. Hook text on screen 0–3s; end on the twig 'breaks' frame.
  4. Only run in markets where this concept is on-curriculum.
  5. Human decides on REVIEW tier; drop if the visual is text-only.
- **Confidence an editor accepts:** 0.35
