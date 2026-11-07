import csv, json, os, sys
sys.path.insert(0, os.path.dirname(__file__)); from briefs_data import *
out = os.path.join(os.path.dirname(__file__), '..', 'outputs'); os.makedirs(out, exist_ok=True)
cols = ["brief_id","class","start","end","duration_s","segments","hook_3s_text","hook_alt","first_3s_what_we_see_hear","bucket","verbatim_dialogue","score","tier","score_breakdown(H,A,V,S,P,B)","geo_india","geo_us_uk_ca_au","geo_gcc","compliance_flags","visual_risk","visual_checks_required","editor_instructions","confidence"]
with open(f'{out}/ad_briefs.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(cols)
    for b in BRIEFS:
        w.writerow([b['id'],b['cls'],b['start'],b['end'],b['dur'],b['segs'],b['hook_text'],b['hook_alt'],b['hook_first3'],b['bucket'],' | '.join(b['verbatim']),b['score'],b['tier'],
          ', '.join(f"{k}={b['s'][k]}" for k in W),b['geo']['india'],b['geo']['us'],b['geo']['gcc'],' ; '.join(b['flags']),b['vrisk'],' ; '.join(b['vchecks']),' ; '.join(f"{i+1}) {x}" for i,x in enumerate(b['editor'])),b['conf']])
with open(f'{out}/ad_briefs.md','w') as f:
    f.write("# Extracted Ad Briefs — Bambinos sample classes\n\n> Produced by applying `prompts/01_moment_miner_system_prompt.md` to the four provided transcripts (see README for method + honest limits). Video files in the repo are Git-LFS pointers, so **all visual fields are UNVERIFIED** and listed as required checks. Scores are AI-proposed and uncalibrated until editor accept/reject data exists.\n\n")
    f.write("## Class-level yield\n\n| Class | Length | SHIP | Near-misses | Note |\n|---|---|---|---|---|\n")
    for r in CLASS_SUMMARY: f.write("| "+" | ".join(r)+" |\n")
    f.write("\n## Summary table\n\n| ID | Class | Start–End | Bucket | Score | Tier | Visual risk | India / US-UK-CA-AU / GCC |\n|---|---|---|---|---|---|---|---|\n")
    for b in BRIEFS: f.write(f"| {b['id']} | {b['cls'].split('_')[0]} | {b['start']}–{b['end']} | {b['bucket']} | {b['score']} | {b['tier']} | {b['vrisk']} | {b['geo']['india'].split(' –')[0]} / {b['geo']['us'].split(' –')[0]} / {b['geo']['gcc'].split(' –')[0]} |\n")
    for b in BRIEFS:
        f.write(f"\n---\n\n## {b['id']} — {b['bucket']} — {b['score']}/10 ({b['tier']})\n\n- **Class / window:** {b['cls']} · {b['start']}–{b['end']} ({b['dur']}s) · cut: {b['segs']}\n- **3-second hook (on-screen text):** {b['hook_text']}  \n  alt: {b['hook_alt']}\n- **First 3s (what we see/hear):** {b['hook_first3']}\n- **Verbatim dialogue (names masked, ASR errors preserved):**\n")
        for v in b['verbatim']: f.write(f"  - {v}\n")
        f.write("- **Score:** "+", ".join(f"{k} {b['s'][k]}/{W[k]}" for k in W)+f" = **{b['score']}**\n")
        f.write(f"- **Geography fit:** India — {b['geo']['india']}; US/UK/CA/AU — {b['geo']['us']}; GCC — {b['geo']['gcc']}\n- **Compliance flags:** "+"; ".join(b['flags'])+f"\n- **Visual risk:** {b['vrisk']} — checks required:\n")
        for c in b['vchecks']: f.write(f"  - [ ] {c}\n")
        f.write("- **Editor instructions:**\n")
        for i,e in enumerate(b['editor']): f.write(f"  {i+1}. {e}\n")
        f.write(f"- **Confidence an editor accepts:** {b['conf']}\n")
with open(f'{out}/rejected_moments_and_flags.md','w') as f:
    f.write("# Rejected moments, hard exclusions and quality alerts\n\n| Class | Window | Reason | Action |\n|---|---|---|---|\n")
    for r in REJECTED: f.write("| "+" | ".join(r)+" |\n")
json.dump({"class_id":"Maths_2125736982","status":"NO_MOMENTS","no_moment_reason":"Teacher monologue (96% of words); child voice absent; sustained negative teacher tone","quality_alert":{"raised":True,"reason":"Repeated shaming of the child and references to parents; escalate to Academic Quality","timestamps":["00:25:17","00:35:09","00:37:40","00:38:22","00:39:44","00:45:43","00:47:54"]},"moments":[],"rejected_near_misses":[]},open(f'{out}/sample_no_moments_maths.json','w'),indent=2)
print([ (b['id'],b['score']) for b in BRIEFS])
