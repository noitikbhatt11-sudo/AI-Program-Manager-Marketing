#!/usr/bin/env python3
"""
preprocess_vtt.py  -  Step 2 of the Bambinos pipeline (runs BEFORE the LLM).
Parses a Zoom-style WebVTT transcript and emits:
  1. <class>.turns.json  : merged speaker turns with start/end seconds
  2. <class>.stats.json  : structural signals used to flag the AUDIO-vs-VISUAL gap
                           (silence gaps, talk share, long monologues, PII + negative-tone hits)
  3. <class>.llm.txt     : "[HH:MM:SS-HH:MM:SS] ROLE: text" with names masked, ready for the miner prompt

Usage:  python preprocess_vtt.py path/to/class.vtt --out outputs/stats/
No third-party deps. Python 3.8+.
"""
import re, json, argparse, os
from collections import defaultdict

TS = re.compile(r'(\d+):(\d+):(\d+)\.(\d+)\s*-->\s*(\d+):(\d+):(\d+)\.(\d+)')
def sec(h,m,s,ms): return int(h)*3600+int(m)*60+int(s)+int(ms)/1000
def hms(x): x=int(x); return f"{x//3600:02d}:{x%3600//60:02d}:{x%60:02d}"

PII_PATTERNS = {
  "phone":   re.compile(r'(?<!\d)(?:\+?\d[\s-]?){10,13}(?!\d)'),
  "email":   re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'),
  "money":   re.compile(r'[$₹£€]\s?\d+|\b\d+\s?(?:dollars|rupees)\b', re.I),
  "address_cue": re.compile(r'\b(?:my (?:house|address|apartment)|we live|i live)\b', re.I),
  "school_cue":  re.compile(r'\b(?:my school|our school)\b', re.I),
  "family_cue":  re.compile(r"\b(?:my (?:mother|mom|mummy|father|dad|papa|sister|brother)|baby brother|at the door)\b", re.I),
  "scheduling_billing": re.compile(r'\b(?:free slot|slot the book|batch)\b', re.I),
}
NEGATIVE_TONE = re.compile(r"\b(?:how many times|silly|wastage|not (?:at all )?learning|stupid|will not teach|i'm very angry|naughty|scold)\b", re.I)

def parse(path):
    lines = open(path, encoding='utf-8').read().split('\n'); cues=[]; i=0
    while i < len(lines):
        m = TS.match(lines[i].strip())
        if m:
            s=sec(*m.groups()[:4]); e=sec(*m.groups()[4:]); txt=[]; i+=1
            while i<len(lines) and lines[i].strip():
                txt.append(lines[i].strip()); i+=1
            full=' '.join(txt); spk,_,body = full.partition(': ')
            if not body: spk, body = 'UNKNOWN', full
            cues.append((s,e,spk,body))
        i+=1
    return cues

def merge_turns(cues, gap=2.0):
    turns=[]
    for s,e,spk,t in cues:
        if turns and turns[-1]['speaker']==spk and s-turns[-1]['end']<=gap:
            turns[-1]['end']=e; turns[-1]['text']+=' '+t
        else: turns.append(dict(start=s,end=e,speaker=spk,text=t))
    return turns

def analyse(turns):
    words=defaultdict(int)
    for t in turns: words[t['speaker']]+=len(t['text'].split())
    teacher=max(words,key=words.get); total=sum(words.values()) or 1
    gaps=[dict(from_=hms(a['end']),to=hms(b['start']),seconds=round(b['start']-a['end']))
          for a,b in zip(turns,turns[1:]) if b['start']-a['end']>=45]
    mono=[dict(at=hms(t['start']),seconds=round(t['end']-t['start']),words=len(t['text'].split()))
          for t in turns if t['speaker']==teacher and len(t['text'].split())>180]
    pii=[dict(at=hms(t['start']),type=k) for t in turns for k,p in PII_PATTERNS.items() if p.search(t['text'])]
    neg=[hms(t['start']) for t in turns if t['speaker']==teacher and NEGATIVE_TONE.search(t['text'])]
    return dict(duration=hms(turns[-1]['end']),teacher_label=teacher,
        word_share={k:round(v/total,3) for k,v in words.items()},
        silence_gaps_ge_45s=gaps,total_silence_min=round(sum(g['seconds'] for g in gaps)/60,1),
        long_teacher_monologues=mono,pii_hits=pii,negative_tone_turns=neg)

def mask_names(turns):
    """Swap participant labels for roles and mask name tokens so full names never reach the LLM or an editor brief."""
    wc=defaultdict(int)
    for t in turns: wc[t['speaker']]+=len(t['text'].split())
    teacher=max(wc,key=wc.get); roles={}
    for l in wc: roles[l]='TEACHER' if l==teacher else ('CHILD' if 'CHILD' not in roles.values() else 'OTHER')
    out=[]
    for t in turns:
        txt=t['text']
        for l in wc:
            for part in l.split():
                if len(part)>3: txt=re.sub(re.escape(part),'[NAME]',txt,flags=re.I)
        out.append(dict(t,speaker=roles[t['speaker']],text=txt))
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('vtt'); ap.add_argument('--out',default='.')
    a=ap.parse_args(); os.makedirs(a.out,exist_ok=True)
    base=os.path.splitext(os.path.basename(a.vtt))[0]
    turns=merge_turns(parse(a.vtt)); st=analyse(turns)
    json.dump(st,open(f'{a.out}/{base}.stats.json','w'),indent=2)
    json.dump(turns,open(f'{a.out}/{base}.turns.json','w'),indent=1)
    with open(f'{a.out}/{base}.llm.txt','w') as f:
        for t in mask_names(turns): f.write(f"[{hms(t['start'])}-{hms(t['end'])}] {t['speaker']}: {t['text']}\n")
    print(base, st['duration'], st['word_share'], 'silence_min=',st['total_silence_min'])
