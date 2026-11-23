#!/usr/bin/env python3
"""Merge all validated LLM labels from both label directories into classified_questions_v2.json."""
import json, os, sys
from collections import Counter
import chapters

HERE=os.path.dirname(os.path.abspath(__file__))
DIRS=[os.path.join(HERE,'data','llm_labels'), os.path.join(HERE,'data','llm_labels_rem')]
VALID={s:set(chapters.TAXONOMY[s]) for s in ['Physics','Chemistry','Mathematics']}

labels={}; dup=0; bad=0
for d in DIRS:
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if not f.endswith('.jsonl'): continue
        for line in open(os.path.join(d,f),encoding='utf-8'):
            line=line.strip()
            if not line: continue
            try: o=json.loads(line)
            except Exception: bad+=1; continue
            i,ch=o.get('id'),o.get('chapter')
            if i in labels and labels[i]!=ch: dup+=1
            labels[i]=ch
print('label ids',len(labels),'bad json',bad,'conflicting duplicates',dup)

rows=json.load(open(os.path.join(HERE,'data','classified_questions.json')))
merged=Counter(); no_signal=0; unknown=0
for r in rows:
    r.setdefault('chapter_source','keyword')
    if r['chapter']!='Unclassified': continue
    i=f"{r['paper']}|{r['q']}"; ch=labels.get(i)
    if not ch: continue
    if ch=='NO_SIGNAL': no_signal+=1; continue
    if ch not in VALID[r['section_subject']]:
        unknown+=1; continue
    r['chapter']=ch; r['chapter_source']='llm'; merged[r['section_subject']]+=1
print('merged',dict(merged),'total',sum(merged.values()),'NO_SIGNAL',no_signal,'unknown chapter',unknown)
json.dump(rows,open(os.path.join(HERE,'data','classified_questions_v2.json'),'w'),ensure_ascii=False)
manifest={'textrich_total':1073,'labeled_unique':len(labels),'placed':sum(merged.values()),
          'no_signal':len({i for i,c in labels.items() if c=='NO_SIGNAL'}),
          'unprocessed_textrich':1073-len(labels)}
json.dump(manifest,open(os.path.join(HERE,'data','llm_manifest.json'),'w'),indent=1)
print('manifest',manifest)
