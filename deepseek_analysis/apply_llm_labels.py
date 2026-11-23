#!/usr/bin/env python3
"""Validate second-pass LLM labels and merge accepted labels into the classification."""
import json, os, re, csv, sys
from collections import Counter, defaultdict
import chapters

HERE=os.path.dirname(os.path.abspath(__file__))
SUBJECTS=['Physics','Chemistry','Mathematics']
CHUNK_SUB={'physics':'Physics','chemistry':'Chemistry','mathematics':'Mathematics'}
VALID={s:set(chapters.TAXONOMY[s]) for s in SUBJECTS}

def load_chunks():
    out={}
    d=os.path.join(HERE,'data','llm_chunks')
    for f in sorted(os.listdir(d)):
        if not f.endswith('.json'): continue
        subj=f.split('_')[0]
        arr=json.load(open(os.path.join(d,f)))
        out[f[:-5]]=(CHUNK_SUB[subj],arr)
    return out

def load_labels():
    labels={}; problems=[]
    d=os.path.join(HERE,'data','llm_labels')
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if not f.endswith('.jsonl'): continue
        for line in open(os.path.join(d,f),encoding='utf-8'):
            line=line.strip()
            if not line: continue
            try: o=json.loads(line)
            except Exception: problems.append((f,'bad json',line[:80])); continue
            labels[o.get('id')]=o.get('chapter')
    return labels,problems

def validate(chunks,labels):
    ok=[]; bad=[]; no_signal=0; unknown=0; missing_files=[]
    for name,(subj,arr) in chunks.items():
        if not os.path.exists(os.path.join(HERE,'data','llm_labels',name+'.jsonl')):
            missing_files.append(name); continue
        ids={x['id'] for x in arr}
        got={i for i in labels if i in ids}
        if ids-got: ok.append((name,'missing',len(ids-got)))
        for i in ids:
            if i not in labels: continue
            ch=labels[i]
            if ch=='NO_SIGNAL': no_signal+=1; continue
            if ch not in VALID[subj]:
                # tolerant exact-ish normalization
                normalized={c.lower():c for c in VALID[subj]}
                if str(ch).lower() in normalized: labels[i]=normalized[str(ch).lower()]
                else: unknown+=1; bad.append((name,i,ch))
    return no_signal,unknown,bad,missing_files

def main():
    chunks=load_chunks(); labels,problems=load_labels()
    print('chunks',len(chunks),'labels',len(labels),'problems',len(problems))
    no_signal,unknown,bad,missing_files=validate(chunks,labels)
    print('NO_SIGNAL',no_signal,'unknown chapter',unknown,'missing label files',missing_files)
    if problems: print('problems sample',problems[:5])
    if bad: print('bad sample',bad[:10])
    if unknown or problems or missing_files:
        print('Validation failed; not merging.'); sys.exit(1)
    rows=json.load(open(os.path.join(HERE,'data','classified_questions.json')))
    merged=0
    for r in rows:
        if r['chapter']!='Unclassified': r.setdefault('chapter_source','keyword'); continue
        qid=f"{r['paper']}|{r['q']}"
        ch=labels.get(qid)
        if ch and ch!='NO_SIGNAL':
            r['chapter']=ch; r['chapter_source']='llm'; merged+=1
        else:
            r['chapter_source']='keyword'
    json.dump(rows,open(os.path.join(HERE,'data','classified_questions_v2.json'),'w'),ensure_ascii=False)
    print('merged',merged,'of',sum(1 for r in rows if r['chapter_source']=='llm'),'llm labels')

if __name__=='__main__': main()
