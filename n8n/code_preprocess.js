// n8n Code node ("Run Once for All Items", JavaScript) — port of scripts/preprocess_vtt.py
// Input item must contain: vtt (string, from the HTTP node) + class_id, subject, market, consent_on_file, age_band.
const TS = /(\d+):(\d+):(\d+)\.(\d+)\s*-->\s*(\d+):(\d+):(\d+)\.(\d+)/;
const sec = (h,m,s,ms) => (+h)*3600 + (+m)*60 + (+s) + (+ms)/1000;
const hms = x => { x = Math.floor(x); const p = n => String(n).padStart(2,'0'); return `${p(Math.floor(x/3600))}:${p(Math.floor(x%3600/60))}:${p(x%60)}`; };
const PII = {
  phone: /(?<!\d)(?:\+?\d[\s-]?){10,13}(?!\d)/, email: /[\w.+-]+@[\w-]+\.[\w.]+/,
  money: /[$₹£€]\s?\d+|\b\d+\s?(?:dollars|rupees)\b/i,
  address_cue: /\b(?:my (?:house|address|apartment)|we live|i live)\b/i, school_cue: /\b(?:my school|our school)\b/i,
  family_cue: /\b(?:my (?:mother|mom|mummy|father|dad|papa|sister|brother)|baby brother|at the door)\b/i,
  scheduling_billing: /\b(?:free slot|slot the book|batch)\b/i,
};
const NEG = /\b(?:how many times|silly|wastage|not (?:at all )?learning|stupid|will not teach|i'm very angry|naughty|scold)\b/i;

function parse(vtt) {
  const lines = vtt.split('\n'); const cues = [];
  for (let i = 0; i < lines.length; i++) {
    const m = TS.exec(lines[i].trim()); if (!m) continue;
    const s = sec(m[1],m[2],m[3],m[4]), e = sec(m[5],m[6],m[7],m[8]); const txt = []; i++;
    while (i < lines.length && lines[i].trim()) { txt.push(lines[i].trim()); i++; }
    const full = txt.join(' '); const k = full.indexOf(': ');
    cues.push(k < 0 ? [s,e,'UNKNOWN',full] : [s,e,full.slice(0,k),full.slice(k+2)]);
  }
  return cues;
}
function mergeTurns(cues, gap = 2.0) {
  const t = [];
  for (const [s,e,spk,txt] of cues) {
    const l = t[t.length-1];
    if (l && l.speaker === spk && s - l.end <= gap) { l.end = e; l.text += ' ' + txt; }
    else t.push({start:s, end:e, speaker:spk, text:txt});
  }
  return t;
}
function analyse(turns) {
  const words = {}; turns.forEach(t => words[t.speaker] = (words[t.speaker]||0) + t.text.split(/\s+/).length);
  const teacher = Object.keys(words).sort((a,b) => words[b]-words[a])[0];
  const total = Object.values(words).reduce((a,b)=>a+b,0) || 1;
  const gaps = []; for (let i=0;i<turns.length-1;i++){ const g = turns[i+1].start - turns[i].end; if (g>=45) gaps.push({from:hms(turns[i].end), to:hms(turns[i+1].start), seconds:Math.round(g)}); }
  const mono = turns.filter(t => t.speaker===teacher && t.text.split(/\s+/).length>180).map(t => ({at:hms(t.start), seconds:Math.round(t.end-t.start)}));
  const pii = []; turns.forEach(t => { for (const [k,p] of Object.entries(PII)) if (p.test(t.text)) pii.push({at:hms(t.start), type:k}); });
  const neg = turns.filter(t => t.speaker===teacher && NEG.test(t.text)).map(t => hms(t.start));
  const share = {}; for (const k in words) share[k] = Math.round(words[k]/total*1000)/1000;
  return {duration: hms(turns[turns.length-1].end), word_share: share, silence_gaps_ge_45s: gaps,
          total_silence_min: Math.round(gaps.reduce((a,g)=>a+g.seconds,0)/6)/10, long_teacher_monologues: mono, pii_hits: pii, negative_tone_turns: neg};
}
function maskNames(turns) {
  const wc = {}; turns.forEach(t => wc[t.speaker] = (wc[t.speaker]||0) + t.text.split(/\s+/).length);
  const labels = Object.keys(wc); const teacher = labels.sort((a,b)=>wc[b]-wc[a])[0]; const roles = {}; let childUsed = false;
  labels.forEach(l => { if (l===teacher) roles[l]='TEACHER'; else if (!childUsed) { roles[l]='CHILD'; childUsed = true; } else roles[l]='OTHER'; });
  return turns.map(t => { let txt = t.text;
    labels.forEach(l => l.split(' ').forEach(part => { if (part.length>3) txt = txt.replace(new RegExp(part.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'gi'),'[NAME]'); }));
    return {...t, speaker: roles[t.speaker], text: txt}; });
}
function run(item) {
  const turns = mergeTurns(parse(item.vtt)); const flags = analyse(turns);
  const llm_text = maskNames(turns).map(t => `[${hms(t.start)}-${hms(t.end)}] ${t.speaker}: ${t.text}`).join('\n');
  const meta = {class_id:item.class_id, subject:item.subject, age_band:item.age_band||'unknown', market_hint:item.market, consent_on_file:item.consent_on_file, duration:flags.duration};
  const user_message = `<class_meta>${JSON.stringify(meta)}</class_meta>\n<preprocess_flags>${JSON.stringify(flags)}</preprocess_flags>\n<transcript>\n${llm_text}\n</transcript>`;
  return {...item, vtt: undefined, flags, llm_text, user_message, quality_alert: flags.negative_tone_turns.length >= 3};
}
// ---- n8n entry point (guarded so the file can also be unit-tested with plain node) ----
if (typeof $input !== 'undefined') { return $input.all().map(i => ({json: run({...i.json, vtt: i.json.vtt ?? i.json.data}) })); }
if (typeof module !== 'undefined') module.exports = { run, parse, mergeTurns, analyse, maskNames };
