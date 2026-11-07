// n8n Code node ("Run Once for All Items", JavaScript) — validates Claude's JSON and shapes Sheet rows.
// Reads the Claude API response from the incoming item and the masked transcript from the "Preprocess" node.
const norm = s => s.toLowerCase().replace(/\[[^\]]*\]/g,' ').replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
function validate(resp, pre) {
  let txt = (resp.content || []).map(c => c.text || '').join('').trim().replace(/^```json|^```|```$/gm,'').trim();
  let out; try { out = JSON.parse(txt); } catch (e) { return [{row_type:'class_log', class_id:pre.class_id, status:'PARSE_ERROR', note:String(e).slice(0,120)}]; }
  const T = norm(pre.llm_text); const rows = [];
  const log = (status, note) => rows.push({row_type:'class_log', class_id:pre.class_id, subject:pre.subject, market:pre.market, status,
      quality_alert: (out.quality_alert && out.quality_alert.raised) || pre.quality_alert ? 'YES' : '', note: note || out.no_moment_reason || '',
      silence_min: pre.flags.total_silence_min, child_share: JSON.stringify(pre.flags.word_share)});
  if (out.status === 'NO_MOMENTS' || !out.moments || !out.moments.length) { log('NO_MOMENTS'); return rows; }
  let kept = 0;
  for (const m of out.moments) {
    // 1) hallucination guard: every dialogue fragment (split on […] / ...) of >=5 words must appear in the transcript
    const bad = [];
    for (const v of (m.verbatim || [])) for (const frag of String(v.text).split(/\[…\]|…|\.\.\./)) {
      const f = norm(frag); if (f.split(' ').length >= 5 && !T.includes(f)) bad.push(f.slice(0,50));
    }
    const total = m.score && m.score.total;
    if (bad.length) { log('DROPPED_UNVERIFIED_QUOTE', `${m.start}: ${bad[0]}`); continue; }
    if (total == null || total < 6) { log('DROPPED_LOW_SCORE', `${m.start}: ${total}`); continue; }
    kept++;
    rows.push({row_type:'candidate', brief_id:`${pre.class_id.split('_')[0].toUpperCase().slice(0,4)}-${String(m.rank).padStart(2,'0')}`, class_id:pre.class_id, subject:pre.subject, market:pre.market,
      start:m.start, end:m.end, duration_s:m.duration_s, bucket:m.bucket, score:total, tier:m.score.tier, hook_text:(m.hook_3s||[])[0]?.on_screen_text || '',
      verbatim:(m.verbatim||[]).map(v=>`${v.role}: ${v.text}`).join(' | '), geo_india:m.geography_fit?.india, geo_us:m.geography_fit?.us_uk_ca_au, geo_gcc:m.geography_fit?.gcc,
      compliance_flags:(m.compliance_flags||[]).join('; '), visual_risk:m.visual_risk, visual_checks:(m.visual_checks_required||[]).join('; '),
      editor_instructions:(m.editor_instructions||[]).map((x,i)=>`${i+1}) ${x}`).join(' '), confidence:m.confidence, decision:'PENDING'});
  }
  if (!kept) log('NO_MOMENTS', 'all candidates dropped by validator');
  else log('OK', `${kept} candidate(s)`);
  return rows;
}
if (typeof $input !== 'undefined') {
  const pre = $('Preprocess').first().json;
  return $input.all().flatMap(i => validate(i.json, pre).map(r => ({json: r})));
}
if (typeof module !== 'undefined') module.exports = { validate };
