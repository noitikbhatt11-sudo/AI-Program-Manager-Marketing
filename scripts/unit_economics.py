"""Unit economics: manual vs AI-assisted, 500 live classes/week. All inputs are ASSUMPTIONS to be replaced by a week-1 time-study."""
import csv, os, json
A = dict(
 classes=500, rate=450,            # INR / loaded hour (≈ ₹8L CTC + 25% overhead / ~2,080 h)
 review_min_manual=30,             # min per class: skim transcript + scrub video
 usable_per_class=0.18,            # usable raw clips per class (1 in ~5.5 classes, avg 1 clip) -> 90/wk
 edit_min_manual=45,               # find in/out, reframe 9:16, captions, name-blur
 edit_min_brief=25,                # with precise brief + visual verdict
 candidates=150, precision=0.60,   # AI-surfaced candidates/wk; share accepted by humans
 qa_min=3.5,                       # human QA per candidate (watch 30s + checklist)
 audit_share=0.05, audit_min=10,   # recall audit: 5% of 'NO_MOMENTS' classes reviewed manually
 ops_hours=4,                      # program-owner upkeep / week
 llm_inr_per_class=5,              # triage + miner tokens (~12k in / 1.5k out)  ≈ $0.06
 video_inr_per_candidate=10,       # video-model verification on ~35s snippets
 tools_inr_week=2000,              # n8n + storage + captioning subscriptions, prorated
)
def run(a):
    manual_clips = a['classes']*a['usable_per_class']
    m_review = a['classes']*a['review_min_manual']/60
    m_edit = manual_clips*a['edit_min_manual']/60
    m_hrs = m_review+m_edit; m_cost = m_hrs*a['rate']
    ai_clips = a['candidates']*a['precision']
    qa = a['candidates']*a['qa_min']/60
    audit = a['classes']*a['audit_share']*a['audit_min']/60
    ai_source = qa+audit+a['ops_hours']
    ai_edit = ai_clips*a['edit_min_brief']/60
    ai_hrs = ai_source+ai_edit
    ai_tool = a['classes']*a['llm_inr_per_class']+a['candidates']*a['video_inr_per_candidate']+a['tools_inr_week']
    ai_cost = ai_hrs*a['rate']+ai_tool
    return dict(manual_clips=round(manual_clips,1), manual_review_h=round(m_review,1), manual_edit_h=round(m_edit,1), manual_total_h=round(m_hrs,1),
      manual_cost=round(m_cost), manual_cost_per_clip=round(m_cost/manual_clips),
      ai_clips=round(ai_clips,1), ai_sourcing_h=round(ai_source,1), ai_edit_h=round(ai_edit,1), ai_total_h=round(ai_hrs,1),
      ai_tool_cost=round(ai_tool), ai_cost=round(ai_cost), ai_cost_per_clip=round(ai_cost/ai_clips),
      sourcing_speedup=round(m_review/ai_source,1), end_to_end_speedup=round(m_hrs/ai_hrs,1),
      hours_saved_week=round(m_hrs-ai_hrs,1), cost_saved_week=round(m_cost-ai_cost), cost_saved_year=round((m_cost-ai_cost)*52))
base = run(A)
sens=[]
for p in (0.40,0.60,0.75):
    for c in (150,250):
        a=dict(A, precision=p, candidates=c); r=run(a); sens.append(dict(precision=p,candidates=c,usable_clips=r['ai_clips'],ai_hours=r['ai_total_h'],hours_per_clip=round(r['ai_total_h']/r['ai_clips'],2),cost_per_clip_inr=r['ai_cost_per_clip'],vs_manual_hours_per_clip_x=round((r['manual_total_h']/r['manual_clips'])/(r['ai_total_h']/r['ai_clips']),1)))
if __name__=='__main__':
    out=os.path.join(os.path.dirname(__file__),'..','outputs'); 
    json.dump(dict(assumptions=A,base=base,sensitivity=sens),open(f'{out}/unit_economics.json','w'),indent=2)
    with open(f'{out}/unit_economics_sensitivity.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=sens[0].keys()); w.writeheader(); w.writerows(sens)
    print(json.dumps(base,indent=1)); print(sens)
