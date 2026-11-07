# Rejected moments, hard exclusions and quality alerts

| Class | Window | Reason | Action |
|---|---|---|---|
| Maths_2125736982 | 00:35:09–00:39:44 | G3 teacher shaming ('how many times… silly, silly things', 'complete wastage for me') | Quality alert |
| Maths_2125736982 | 00:45:43–00:48:08 | G2+G3 child says 'I didn't understand measurement'; teacher: 'from the next time you will score full zero', 'your father always say she doesn't study' | Quality alert |
| Maths_2125736982 | 00:00:24–00:34:00 | No bucket: teacher monologues (3 turns >180 words; child speaks 3.9% of words); no child voice | NO_MOMENTS |
| English_2125604619 | 00:01:30–00:03:30 | G1 child's travel plans/country (Luxembourg/Belgium), name used; location PII | Hard exclude |
| English_2125604619 | 00:07:42–00:08:52; 00:23:13–00:23:50 | G1/G6 family at the door, background interruptions; '$100' payment remark (G5) | Hard exclude |
| English_2125604619 | 00:16:29–00:16:36; 00:21:02–00:21:24; 00:30:18–00:30:28 | G3 guilt-tripping ('I'll cry now', 'I'm very angry today', 'you're so naughty') | Quality alert |
| English_2125604619 | 00:09:56–00:11:06 | Near-miss (5.8, DROP): charming 'octopus on the beach / I saw a video of that', but child is corrected on a factual error (G2) and ASR is garbled (G7) | Drop |
| English_2125604619 | 00:19:39–00:49:00 | 13.8 min of transcript silence (writing). Visual gap: likely dead footage, no speech to caption | Dead air |
| English_2125604619 | 00:08:52 | VISUAL GAP caught: child says 'you put a picture of you there' → teacher tile is a STATIC PHOTO; no teacher-side footage usable | Flag |
| Gita_2125422751 | 00:36:58–00:37:07 | G1 child's birthday month/date/year stated ('January… 2021', teacher: 'falls on January 21') | Hard exclude (Sankranti segment 00:34:47–00:37:41 dropped) |
| Gita_2125422751 | 00:22:25–00:22:40; 00:42:17–00:42:25 | G8/G1 'too dark in your room'; 'my baby brother's disturbing' (home environment/sibling) | Hard exclude |
| Gita_2125422751 | 00:44:45–00:45:30 | G7 mispronunciation + garbled ASR ('wet cheese'); also child is corrected (G2) | Drop |
| Gita_2125422751 | 00:30:02 | FALSE POSITIVE of the regex tone-flag ('Silly me' is the teacher mocking HERSELF) → shows why flags are signals, not verdicts | Info |
| Science_2125687282 | 00:35:41–00:41:26 | G5/G1 ~6 min of scheduling/booking talk with a parent ('free slot', 'Monday 9pm'), asking someone's name & age | Hard exclude |
| Science_2125687282 | 00:21:09–00:21:48 | G8 tech trouble ('I can't see the screen', rejoin) | Dead air |
| Science_2125687282 | 00:29:05–00:29:58 | Near-miss (5.5, DROP): 'robot doesn't need soup' analogy is charming but teacher-only; child silent | Drop |
