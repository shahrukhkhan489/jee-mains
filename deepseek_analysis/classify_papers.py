#!/usr/bin/env python3
"""Classify every parsed question into a chapter, then aggregate weightage."""
import json, os, re, unicodedata, sys, time
from collections import Counter
from itertools import permutations
import chapters

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
SUBJECTS = ['Physics','Chemistry','Mathematics']

# Precompile keyword matchers once.
TERM_SPECS = {}
for subj, chs in chapters.TAXONOMY.items():
    for name,(strong,weak) in chs.items():
        items=[]
        for w,terms in ((4,strong),(1,weak)):
            for term in terms:
                term=term.lower()
                if ' ' in term or '-' in term or "'" in term:
                    items.append((term,w,None))
                else:
                    items.append((term,w,re.compile(r'(?<![a-z0-9])'+re.escape(term)+r'(?:s|es)?(?![a-z0-9])')))
        TERM_SPECS[(subj,name)] = items

def norm(t):
    t = unicodedata.normalize('NFKC', t).lower()
    t = t.replace('\u2019',"'").replace('\u2013','-').replace('\u2014','-')
    return re.sub(r'\s+',' ',t)

def score_all(t):
    out={}
    for key,items in TERM_SPECS.items():
        s=0
        for term,w,pat in items:
            c = t.count(term) if pat is None else len(pat.findall(t))
            if c: s += min(c,2)*w
        if s: out[key]=s
    return out

def top_in(scores, subject):
    best=None
    for (subj,ch),s in scores.items():
        if subj!=subject: continue
        if best is None or s>best[1]: best=(ch,s)
    if not best: return 'Unclassified',0
    # margin within subject
    second=0
    for (subj,ch),s in scores.items():
        if subj==subject and s<best[1]: second=max(second,s)
    return best[0], best[1]-second

def classify_paper(p):
    size=p['n']//3
    blocks=[p['questions'][i*size:(i+1)*size] for i in range(3)]
    cached=[]  # (q, scores)
    ev=[[0.0]*3 for _ in range(3)]
    for bi,block in enumerate(blocks):
        for q in block:
            t=norm(q['text']); sc=score_all(t); cached.append((bi,q,sc))
            for si,subj in enumerate(SUBJECTS):
                ev[bi][si]+=sum(s for (s2,_),s in sc.items() if s2==subj)
    best_perm,best_score=None,-1
    for perm in permutations(range(3)):
        s=sum(ev[bi][perm[bi]] for bi in range(3))
        if s>best_score: best_score,best_perm=s,perm
    order=[SUBJECTS[i] for i in best_perm]
    out=[]
    for bi,q,sc in cached:
        subj=order[bi]
        ch,margin=top_in(sc,subj)
        score=max((s for (s2,c),s in sc.items() if s2==subj), default=0)
        out.append({'q':q['q'],'text':q['text'],'section_subject':subj,
                    'subject':subj,'chapter':ch,'score':score,'margin':margin})
    return order,out

def main():
    t0=time.time()
    papers=json.load(open(os.path.join(HERE,'data','parsed_papers.json')))
    rows=[]; orders={}
    for rank,p in enumerate(papers,1):
        order,qs=classify_paper(p); orders[p['paper']]=order
        for q in qs:
            rows.append({'rank':rank,'paper':p['paper'],'year':p['year'],'month':p['month'],
                         'shift':p['shift'],**q})
        if rank%25==0: print('...',rank,'papers',round(time.time()-t0,1),'s',flush=True)
    json.dump(rows,open(os.path.join(HERE,'data','classified_questions.json'),'w'),ensure_ascii=False)
    print('classified rows',len(rows),'in',round(time.time()-t0,1),'s')
    print('unclassified',sum(1 for r in rows if r['chapter']=='Unclassified'))
    for subj in SUBJECTS:
        c=Counter(r['chapter'] for r in rows if r['section_subject']==subj)
        print('\n',subj,'total',sum(c.values()),'unclassified',c.get('Unclassified',0))
        for k,v in c.most_common(8): print('   ',k,v)
    print('\norders sample:',list(orders.items())[:8])

if __name__=='__main__': main()
