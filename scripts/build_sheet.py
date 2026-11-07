import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from briefs_data import BRIEFS, CLASS_SUMMARY
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as L
F='Arial'; H=PatternFill('solid',fgColor='0B3D91'); HF=Font(name=F,bold=True,color='FFFFFF',size=10)
BLUE=Font(name=F,color='0000FF',size=10); N=Font(name=F,size=10); B=Font(name=F,bold=True,size=10)
wb=Workbook()
def head(ws,cols,widths=None):
    for i,c in enumerate(cols,1):
        x=ws.cell(1,i,c); x.font=HF; x.fill=H; x.alignment=Alignment(wrap_text=True,vertical='center')
        ws.column_dimensions[L(i)].width=(widths or {}).get(c,16)
    ws.freeze_panes='A2'; ws.row_dimensions[1].height=30
# ---------- README
ws=wb.active; ws.title='README'
rows=[("Bambinos.live — Class → Ad Brief tracker (template)",B),("",N),
("TABS",B),("Candidates: one row per AI-proposed moment. n8n appends rows; marketers fill the YELLOW columns (decision, reason_code, reviewer…).",N),
("Class_Log: one row per class run (OK / NO_MOMENTS / NO_CONSENT / quality alert). Feeds the recall audit.",N),
("Reason_Codes: dropdown source + meaning. Metrics: live KPIs (formulas). Unit_Economics: edit BLUE cells to re-run the ROI.",N),("",N),
("HOW TO USE (marketing exec, daily)",B),("1) Filter Candidates: decision = PENDING, sort by score.  2) Open qa_link (video#t=start-5s).  3) Tick the visual checks.",N),
("4) Set decision = ACCEPT / EDIT-WINDOW / REJECT. A REJECT needs a reason_code.  5) Quality concern about a teacher? Do NOT discuss here — Slack #academic-quality.",N),("",N),
("EXAMPLE ROWS",B),("The 5 rows in Candidates are the real briefs from the 4 sample classes (decision = PENDING). Delete them before going live.",N),("",N),
("n8n column contract: header names in Candidates / Class_Log must match the keys emitted by n8n/code_validate.js (do not rename).",N)]
for i,(t,f) in enumerate(rows,1): ws.cell(i,1,t).font=f
ws.column_dimensions['A'].width=140
# ---------- Candidates
cols=["row_type","brief_id","class_id","subject","market","start","end","duration_s","bucket","score","tier","hook_text","verbatim","geo_india","geo_us","geo_gcc","compliance_flags","visual_risk","visual_checks","editor_instructions","confidence","qa_link","visual_verdict","decision","reason_code","reviewer","reviewed_at","editor_status","published","ad_id"]
wd={"verbatim":50,"editor_instructions":60,"visual_checks":45,"compliance_flags":40,"hook_text":30,"geo_india":24,"geo_us":24,"geo_gcc":24}
cs=wb.create_sheet('Candidates'); head(cs,cols,wd)
yellow=PatternFill('solid',fgColor='FFF2CC')
subj={'Gita':'Gita','Science':'Science'}
for r,b in enumerate(BRIEFS,2):
    vals=dict(row_type='candidate',brief_id=b['id'],class_id=b['cls'],subject=b['cls'].split('_')[0],market='india',start=b['start'],end=b['end'],duration_s=b['dur'],bucket=b['bucket'],score=b['score'],tier=b['tier'],hook_text=b['hook_text'],verbatim=' | '.join(b['verbatim']),geo_india=b['geo']['india'],geo_us=b['geo']['us'],geo_gcc=b['geo']['gcc'],compliance_flags=' ; '.join(b['flags']),visual_risk=b['vrisk'],visual_checks=' ; '.join(b['vchecks']),editor_instructions=' '.join(f"{i+1}) {x}" for i,x in enumerate(b['editor'])),confidence=b['conf'],decision='PENDING')
    for c,k in enumerate(cols,1):
        x=cs.cell(r,c,vals.get(k)); x.font=N; x.alignment=Alignment(wrap_text=True,vertical='top')
    cs.row_dimensions[r].height=90
ci={c:i+1 for i,c in enumerate(cols)}
for k in ('visual_verdict','decision','reason_code','reviewer','reviewed_at','editor_status','published','ad_id'):
    for r in range(1,201):
        if r>1: cs.cell(r,ci[k]).fill=yellow
    cs.cell(1,ci[k]).fill=PatternFill('solid',fgColor='BF8F00')
def dv(ws,col,items,rng_end=1000,formula=None):
    d=DataValidation(type='list',formula1=formula or '"'+','.join(items)+'"',allow_blank=True); ws.add_data_validation(d); d.add(f"{L(col)}2:{L(col)}{rng_end}")
dv(cs,ci['decision'],["PENDING","ACCEPT","EDIT-WINDOW","REJECT"]); dv(cs,ci['published'],["Y","N"])
dv(cs,ci['visual_verdict'],["PASS","FIX_THEN_PASS","REJECT"]); dv(cs,ci['editor_status'],["NOT_STARTED","IN_EDIT","BOUNCED","DONE"])
# ---------- Reason codes
rc=wb.create_sheet('Reason_Codes'); head(rc,["code","meaning","stage"],{"meaning":70})
CODES=[("R1","No hook in first 3 seconds","QA"),("R2","Teacher-led; child is not the star","QA"),("R3","Child embarrassed / struggling","QA"),("R4","PII or consent issue","QA"),("R5","Camera off / face not visible","QA"),("R6","Audio unintelligible / overlap","QA"),("R7","Off-brand / cringe","QA"),("R8","Duplicate of an existing creative","QA"),("R9","Other (write in note)","QA"),
("V1_CAMERA_OFF","Verifier: child camera off","Verifier"),("V2_STATIC_TEACHER_ONLY","Verifier: only a static teacher image","Verifier"),("V3_FACE_UNLIT","Verifier: face too dark","Verifier"),("V4_PII_VISIBLE","Verifier: name/sibling/parent visible","Verifier"),("V5_IP_VISIBLE","Verifier: third-party IP visible/audible","Verifier"),("V6_AUDIO_BAD","Verifier: audio unusable","Verifier"),("V7_EXPRESSION_MISMATCH","Verifier: words and expression disagree","Verifier"),
("E-DEADFOOTAGE","Editor bounce: dead footage in window","Editor"),("E-NO-FACE","Editor bounce: no usable face","Editor"),("E-STATIC-TEACHER","Editor bounce: teacher tile is a photo","Editor"),("E-WINDOW","Editor bounce: window cannot be cut cleanly","Editor")]
for r,row in enumerate(CODES,2):
    for c,v in enumerate(row,1): rc.cell(r,c,v).font=N
nrc=len(CODES)+1
dv(cs,ci['reason_code'],[],formula=f"=Reason_Codes!$A$2:$A${nrc}")
# ---------- Class log
cl=wb.create_sheet('Class_Log'); lcols=["row_type","class_id","subject","market","status","quality_alert","note","silence_min","child_share"]
head(cl,lcols,{"note":70,"child_share":40,"class_id":24})
cinfo={"English_2125604619":("English","NO_MOMENTS","", "Zero-moment: PII, guilt-tripping, 13.8 min silence, static teacher photo",13.8,'{"Teacher":0.49,"Child":0.51}'),
"Gita_2125422751":("Gita","OK","","4 SHIP candidates",6.0,'{"Teacher":0.81,"Child":0.19}'),
"Maths_2125736982":("Maths","NO_MOMENTS","YES","Sustained teacher shaming; escalate to Academic Quality",6.7,'{"Teacher":0.96,"Child":0.04}'),
"Science_2125687282":("Science","OK","","1 REVIEW candidate; 6 min parent/billing chat excluded",0.0,'{"Teacher":0.89,"Child":0.11}')}
for r,(k,v) in enumerate(cinfo.items(),2):
    for c,x in enumerate(["class_log",k,v[0],"india",v[1],v[2],v[3],v[4],v[5]],1): cl.cell(r,c,x).font=N
dv(cl,5,["OK","NO_MOMENTS","NO_CONSENT","PARSE_ERROR","DROPPED_LOW_SCORE","DROPPED_UNVERIFIED_QUOTE"])
# ---------- Metrics
m=wb.create_sheet('Metrics'); m.column_dimensions['A'].width=46; m.column_dimensions['B'].width=16; m.column_dimensions['C'].width=60
D=L(ci['decision']); P=L(ci['published'])
met=[("Candidates surfaced","=COUNTA(Candidates!B2:B1000)","All rows in Candidates"),
("Accepted (ACCEPT + EDIT-WINDOW)",f'=COUNTIF(Candidates!{D}2:{D}1000,"ACCEPT")+COUNTIF(Candidates!{D}2:{D}1000,"EDIT-WINDOW")',""),
("Rejected",f'=COUNTIF(Candidates!{D}2:{D}1000,"REJECT")',""),
("Pending QA",f'=COUNTIF(Candidates!{D}2:{D}1000,"PENDING")',""),
("PRECISION (accepted ÷ reviewed)",'=IFERROR(B3/(B3+B4),"n/a")',"Target: D30 ≥50%, D60 ≥65%, D90 ≥75%"),
("FALSE-POSITIVE rate",'=IFERROR(B4/(B3+B4),"n/a")',"AI picks that humans rejected"),
("Clips published",f'=COUNTIF(Candidates!{P}2:{P}1000,"Y")',""),
("Clip→ad conversion",'=IFERROR(B8/B3,"n/a")',"Published ÷ accepted. Target D90 ≥65%"),
("Classes processed","=COUNTA(Class_Log!B2:B5000)",""),
("NO_MOMENTS classes",'=COUNTIF(Class_Log!E2:E5000,"NO_MOMENTS")',""),
("Zero-moment rate",'=IFERROR(B11/B10,"n/a")',"Healthy range is high; audit 5% weekly for misses"),
("Quality alerts raised",'=COUNTIF(Class_Log!F2:F5000,"YES")',"Route to Academic Quality (private)")]
m.cell(1,1,"KPI").font=HF; m.cell(1,2,"Value").font=HF; m.cell(1,3,"Note").font=HF
for c in (1,2,3): m.cell(1,c).fill=H
for r,(a,f,n) in enumerate(met,2):
    m.cell(r,1,a).font=B if a.isupper() or 'PRECISION' in a else N; m.cell(r,2,f).font=N; m.cell(r,3,n).font=N
for r in (6,7,9,13): m.cell(r,2).number_format='0.0%'
r0=len(met)+4; m.cell(r0-1,1,"Reject reasons (count)").font=B
for i,(code,mean,_) in enumerate(CODES):
    m.cell(r0+i,1,f"{code} — {mean}").font=N
    m.cell(r0+i,2,f'=COUNTIF(Candidates!{L(ci["reason_code"])}2:{L(ci["reason_code"])}1000,"{code}")').font=N
# ---------- Unit economics
u=wb.create_sheet('Unit_Economics'); u.column_dimensions['A'].width=52; u.column_dimensions['B'].width=16; u.column_dimensions['C'].width=70
inp=[("classes_per_week",500,"Given in the case brief"),("loaded_rate_inr_per_hr",450,"ASSUMPTION: ≈₹8L CTC + 25% overhead ÷ ~2,080 h"),("manual_review_min_per_class",30,"ASSUMPTION — replace with Week-1 time study"),
("usable_clips_per_class",0.18,"ASSUMPTION: ≈1 usable moment in ~5.5 classes → 90/week"),("manual_edit_min_per_clip",45,"ASSUMPTION"),("brief_edit_min_per_clip",25,"ASSUMPTION: with precise brief + visual verdict"),
("ai_candidates_per_week",150,"ASSUMPTION"),("human_acceptance_rate",0.6,"ASSUMPTION = precision; track in Metrics"),("qa_min_per_candidate",3.5,"ASSUMPTION"),("recall_audit_share",0.05,"Share of classes manually audited"),
("audit_min_per_class",10,"ASSUMPTION"),("program_upkeep_hrs_per_week",4,"ASSUMPTION"),("llm_inr_per_class",5,"ASSUMPTION ≈ $0.06 (triage+miner)"),("video_verify_inr_per_candidate",10,"ASSUMPTION"),("tools_inr_per_week",2000,"ASSUMPTION: n8n, storage, captions")]
u.cell(1,1,"INPUTS (blue = edit)").font=B
for i,(k,v,n) in enumerate(inp,2):
    u.cell(i,1,k).font=N; c=u.cell(i,2,v); c.font=BLUE; u.cell(i,3,n).font=N
R={k:f"$B${i}" for i,(k,_,_) in enumerate(inp,2)}
o0=len(inp)+4; u.cell(o0-1,1,"OUTPUTS (formulas)").font=B
out=[("Manual usable clips / week",f"={R['classes_per_week']}*{R['usable_clips_per_class']}"),
("Manual review hours",f"={R['classes_per_week']}*{R['manual_review_min_per_class']}/60"),
("Manual edit hours",f"=B{o0}*{R['manual_edit_min_per_clip']}/60"),
("Manual total hours",f"=B{o0+1}+B{o0+2}"),("Manual cost (INR/week)",f"=B{o0+3}*{R['loaded_rate_inr_per_hr']}"),("Manual cost per usable clip (INR)",f"=B{o0+4}/B{o0}"),
("AI usable clips / week",f"={R['ai_candidates_per_week']}*{R['human_acceptance_rate']}"),
("AI sourcing hours (QA + audit + upkeep)",f"={R['ai_candidates_per_week']}*{R['qa_min_per_candidate']}/60+{R['classes_per_week']}*{R['recall_audit_share']}*{R['audit_min_per_class']}/60+{R['program_upkeep_hrs_per_week']}"),
("AI edit hours",f"=B{o0+6}*{R['brief_edit_min_per_clip']}/60"),("AI total hours",f"=B{o0+7}+B{o0+8}"),
("AI tools + model spend (INR/week)",f"={R['classes_per_week']}*{R['llm_inr_per_class']}+{R['ai_candidates_per_week']}*{R['video_verify_inr_per_candidate']}+{R['tools_inr_per_week']}"),
("AI total cost (INR/week)",f"=B{o0+9}*{R['loaded_rate_inr_per_hr']}+B{o0+10}"),("AI cost per usable clip (INR)",f"=B{o0+11}/B{o0+6}"),
("Sourcing speed-up (x)",f"=B{o0+1}/B{o0+7}"),("End-to-end hours per clip speed-up (x)",f"=(B{o0+3}/B{o0})/(B{o0+9}/B{o0+6})"),
("Hours saved / week",f"=B{o0+3}-B{o0+9}"),("Cost saved / week (INR)",f"=B{o0+4}-B{o0+11}"),("Cost saved / year (INR)",f"=B{o0+16}*52")]
for i,(k,f) in enumerate(out):
    u.cell(o0+i,1,k).font=N; c=u.cell(o0+i,2,f); c.font=N; c.number_format='#,##0.0' if 'x)' in k or 'hours' in k.lower() or 'clips' in k else '#,##0'
for ws_ in wb.worksheets:
    for row in ws_.iter_rows():
        for c in row:
            if c.font is None or c.font.name!=F: c.font=Font(name=F,size=10,bold=c.font.bold if c.font else False,color=c.font.color if c.font else None)
wb.save(os.path.join(os.path.dirname(__file__),'..','sheet','Bambinos_Brief_Tracker_TEMPLATE.xlsx'))
