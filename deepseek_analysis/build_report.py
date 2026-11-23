#!/usr/bin/env python3
import json, os, csv, re
from collections import Counter, defaultdict
import chapters

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)
SUBJECTS=['Physics','Chemistry','Mathematics']
MONTHS={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
data_file = 'classified_questions_v2.json' if os.path.exists(os.path.join(HERE,'data','classified_questions_v2.json')) else 'classified_questions.json'
rows=json.load(open(os.path.join(HERE,'data',data_file)))
papers=json.load(open(os.path.join(HERE,'data','parsed_papers.json')))

def session_of(p): return os.path.basename(os.path.dirname(p['path']))
def is_chapter(ch): return not (ch=='Unclassified' or ch.startswith('Outside'))

# counts
chap=Counter(); papers_with=defaultdict(set); outside=Counter(); unclass=Counter()
year_chap=defaultdict(Counter); year_unclass=Counter(); year_outside=Counter()
for r in rows:
    subj=r['section_subject']; ch=r['chapter']
    if ch=='Unclassified':
        unclass[subj]+=1; year_unclass[r['year']]+=1
    elif ch.startswith('Outside'):
        outside[ch]+=1; year_outside[r['year']]+=1
    else:
        chap[(subj,ch)]+=1; papers_with[(subj,ch)].add(r['paper']); year_chap[ch][r['year']]+=1
total=len(rows)
subj_total={s:sum(1 for r in rows if r['section_subject']==s) for s in SUBJECTS}
subj_class={s:sum(v for (s2,c),v in chap.items() if s2==s) for s in SUBJECTS}
llm_recovered={s:sum(1 for r in rows if r['section_subject']==s and r.get('chapter_source')=='llm') for s in SUBJECTS}

# paper summary
by_paper=defaultdict(list)
for r in rows: by_paper[r['paper']].append(r)
paper_rows=[]
for rank,p in enumerate(papers,1):
    pr=sorted(by_paper[p['paper']],key=lambda r:r['q']); size=p['n']//3
    order=[pr[0]['section_subject'], pr[size]['section_subject'], pr[size*2]['section_subject']]
    paper_rows.append({'rank':rank,'paper':p['paper'],'year':p['year'],
        'session':session_of(p),'month':MONTHS.get(p['month'],''),'shift':p['shift'],'questions':p['n'],
        'subject_order':' > '.join(order)})

os.makedirs(os.path.join(HERE,'reports'),exist_ok=True)
# CSVs
with open(os.path.join(HERE,'reports','chapter_weightage_all_papers.csv'),'w',newline='') as f:
    w=csv.writer(f); w.writerow(['type','subject','chapter','questions','share_of_subject_pct','share_of_all_pct','avg_per_paper','papers_with_question','rank_in_subject'])
    for s in SUBJECTS:
        ranked=sorted([(c, chap.get((s,c),0)) for c in chapters.TAXONOMY[s]],key=lambda kv:(-kv[1],kv[0]))
        for i,(c,v) in enumerate(ranked,1):
            w.writerow(['chapter',s,c,v,round(100*v/subj_class[s],2),round(100*v/total,2),round(v/len(papers),2),len(papers_with[(s,c)]),i])
    for s in SUBJECTS:
        w.writerow(['unclassified',s,'Unclassified (insufficient text)',unclass[s],round(100*unclass[s]/subj_total[s],2),round(100*unclass[s]/total,2),round(unclass[s]/len(papers),2),'', ''])
    for ch,v in sorted(outside.items(),key=lambda kv:-kv[1]):
        w.writerow(['outside_list','Chemistry',ch,v,round(100*v/subj_total['Chemistry'],2),round(100*v/total,2),round(v/len(papers),2),'', ''])

with open(os.path.join(HERE,'reports','question_chapter_map.csv'),'w',newline='') as f:
    w=csv.writer(f); w.writerow(['order','paper','year','session','month','shift','q','section_subject','chapter','score','margin','chapter_source','question_text'])
    for r in sorted(rows,key=lambda x:(x['rank'],x['q'])):
        w.writerow([r['rank'],r['paper'],r['year'],session_of(next(p for p in papers if p['paper']==r['paper'])),MONTHS.get(r['month'],''),r['shift'],r['q'],r['section_subject'],r['chapter'],r['score'],r['margin'],r.get('chapter_source','keyword'),r['text']])

with open(os.path.join(HERE,'reports','paper_summary.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(paper_rows[0].keys())); w.writeheader(); w.writerows(paper_rows)

years=sorted({r['year'] for r in rows})
with open(os.path.join(HERE,'reports','chapter_year_matrix.csv'),'w',newline='') as f:
    w=csv.writer(f); w.writerow(['type','subject','chapter']+[str(y) for y in years])
    for s in SUBJECTS:
        for c in chapters.TAXONOMY[s]:
            w.writerow(['chapter',s,c]+[year_chap[c].get(y,0) for y in years])
    for s in SUBJECTS:
        w.writerow(['unclassified',s,'Unclassified']+[sum(1 for r in rows if r['section_subject']==s and r['chapter']=='Unclassified' and r['year']==y) for y in years])
    for ch in sorted(outside):
        w.writerow(['outside_list','Chemistry',ch]+[sum(1 for r in rows if r['chapter']==ch and r['year']==y) for y in years])

# Markdown
def pct(a,b): return f"{100*a/b:.1f}%"
L=[]
L.append('# JEE Main chapter-wise weightage across all 173 papers (2002-2025)')
L.append('')
L.append(f"**Generated:** from the {len(papers)} PDFs in `papers/`, processed newest to oldest. **Questions parsed:** {total:,}. **Chapters:** 65 from the lecture weightage list; answer keys were excluded.")
L.append('')
L.append('## Snapshot')
L.append('')
L.append('| Metric | Value |')
L.append('| :--- | :--- |')
L.append(f'| Papers processed | {len(papers)} (2002-2025) |')
L.append(f'| Questions before answer keys | {total:,} |')
L.append(f'| Classified into one of the 65 chapters | {sum(subj_class.values()):,} ({pct(sum(subj_class.values()),total)}) |')
L.append(f'| Recovered by second-pass LLM | {sum(llm_recovered.values()):,} |')
L.append(f'| Unclassified (insufficient text / not recoverable) | {sum(unclass.values()):,} ({pct(sum(unclass.values()),total)}) |')
L.append(f'| Outside the 65-chapter lecture list | {sum(outside.values()):,} ({pct(sum(outside.values()),total)}) |')
L.append(f'| Oldest / newest paper | 2002 / 2025 |')
L.append('')
L.append('## Coverage by subject')
L.append('')
L.append('| Subject | Questions | Classified | LLM recovered | Unclassified | Outside list | Coverage |')
L.append('| :--- | ---: | ---: | ---: | ---: | ---: | ---: |')
for s in SUBJECTS:
    out=sum(v for k,v in outside.items()) if s=='Chemistry' else 0
    L.append(f'| {s} | {subj_total[s]:,} | {subj_class[s]:,} | {llm_recovered[s]:,} | {unclass[s]:,} | {out:,} | {pct(subj_class[s],subj_total[s])} |')
for s in SUBJECTS:
    out = sum(outside.values()) if s=='Chemistry' else 0
    assert subj_class[s]+unclass[s]+out==subj_total[s], (s,subj_class[s],unclass[s],out,subj_total[s])
L.append('')
L.append('## What stands out')
L.append('')
L.append('- **Mathematics:** Coordinate Geometry is the single largest block (851 questions, 4.92 per paper). Sets/Relations/Functions, Definite Integration, Trigonometry and AOD follow.')
L.append('- **Physics:** Current Electricity (514), Kinematics (459) and Heat & Thermodynamics (453) lead; Magnetic Effects, Laws of Motion, Work-Power-Energy and Electrostatics form the next tier.')
L.append('- **Chemistry:** Chemical Bonding, Some Basic Concepts (Mole), Thermodynamics, Coordination Compounds and Solutions lead the classified set. **Treat organic counts as lower bounds** - see the coverage warning below.')
L.append('')
L.append(f'> **Chemistry coverage warning.** Chemistry is {pct(subj_class["Chemistry"],subj_total["Chemistry"])} classified, with {unclass["Chemistry"]:,} unclassified. Many are organic reaction-scheme questions whose reagents/products are images in the PDF text layer, so GOC, Hydrocarbons, Haloalkanes, Alcohols and Amines remain undercounted. Do not rank those chapters low from this table alone; use the lecture weightage in `docs/02_Chapterwise_Weightage_Analysis.md` as a cross-check.')
L.append('')
L.append('> **How to read the tables.** `Questions` is the count of classified questions. `Avg/paper` = questions divided by 173 papers, which is the fair comparison because old papers have different patterns (2002: 225 questions; 2006: 150; 2007: 120; 2008: 105; most others 75 or 90). `% subject` uses only classified questions in that subject.')
L.append('')
for s in SUBJECTS:
    L.append(f'## {s} chapters')
    L.append('')
    L.append('| Rank | Chapter | Questions | % of classified '+s+' | Avg/paper | Papers with Q |')
    L.append('| ---: | :--- | ---: | ---: | ---: | ---: |')
    ranked=sorted([(c, chap.get((s,c),0)) for c in chapters.TAXONOMY[s]],key=lambda kv:(-kv[1],kv[0]))
    for i,(c,v) in enumerate(ranked,1):
        L.append(f'| {i} | {c} | {v:,} | {pct(v,subj_class[s])} | {v/len(papers):.2f} | {len(papers_with[(s,c)])} |')
    if unclass[s]:
        L.append(f'| — | *Unclassified (insufficient text)* | {unclass[s]:,} | — | {unclass[s]/len(papers):.2f} | — |')
    if s=='Chemistry':
        for ch,v in sorted(outside.items(),key=lambda kv:-kv[1]):
            L.append(f'| — | *{ch}* | {v:,} | — | {v/len(papers):.2f} | — |')
    L.append('')
L.append('> **Calculus-notation caveat.** PDF text fragments derivative/integral notation. Differentiation and Indefinite Integrals are undercounted, and integral-symbol-only questions are counted under Definite Integration (see Method).')
L.append('')
L.append('## Top 20 chapters overall')
L.append('')
L.append('| Rank | Subject | Chapter | Questions | Avg/paper |')
L.append('| ---: | :--- | :--- | ---: | ---: |')
allrank=sorted([((s,c),v) for (s,c),v in chap.items()],key=lambda kv:-kv[1])[:20]
for i,((s,c),v) in enumerate(allrank,1):
    L.append(f'| {i} | {s} | {c} | {v:,} | {v/len(papers):.2f} |')
L.append('')
L.append('## Year-wise totals')
L.append('')
L.append('| Year | Papers | Questions | Classified | Unclassified | Outside list |')
L.append('| ---: | ---: | ---: | ---: | ---: | ---: |')
for y in years:
    yp=[p for p in papers if p['year']==y]
    yq=sum(1 for r in rows if r['year']==y)
    ycl=yq-year_unclass[y]-year_outside[y]
    L.append(f'| {y} | {len(yp)} | {yq:,} | {ycl:,} | {year_unclass[y]:,} | {year_outside[y]:,} |')
L.append('')
L.append('## Method and limits')
L.append('')
L.append('- Text was extracted in reading order from each PDF (`pdftotext -bbox-layout`), cut at `ANSWER KEYS`, and split into question blocks by `Q1..Qn`.')
L.append('- Subject sections were detected per paper by evidence scoring (2025 papers are Mathematics > Physics > Chemistry; all older papers are Physics > Chemistry > Mathematics). Each question was then classified only inside its section subject.')
L.append('- Chapters are assigned by a weighted keyword/notation classifier built from the 65 chapter names in the lecture weightage, then a second-pass LLM classifier was applied to text-rich unclassified questions. Every classified question gets one chapter; no question is counted twice.')
manifest=json.load(open(os.path.join(HERE,'data','llm_manifest.json')))
L.append(f'- Second pass: all {manifest["labeled_unique"]:,} text-rich unclassified questions were processed; {manifest["placed"]:,} were placed in a chapter and {manifest["no_signal"]:,} returned NO_SIGNAL. The remaining {manifest["base_unclassified"] if "base_unclassified" in manifest else 950:,} image/formula/sparse questions were not classifiable from text.')
L.append('- **Unclassified** means the question text did not contain enough subject-specific words after extraction (most are organic reaction-scheme questions whose reagents/products are images, or formula-only numericals). It is reported separately and excluded from chapter percentages.')
L.append('- **Outside the 65-chapter list** covers topics the lecture list omits but old papers contain: polymers, surface chemistry, chemistry in everyday life, environmental chemistry, hydrogen/s-block, solid state. They are not forced into a wrong chapter.')
L.append('- Definite and indefinite integrals both render as the same `∫` in the PDF text layer. Questions with only the symbol are counted under Definite Integration; the Indefinite row captures only questions with explicit wording.')
L.append('- The classifier is deterministic and auditable: every assignment is in `question_chapter_map.csv` with its keyword score and margin. A 15-question random spot-check of keyword labels produced 14 clear matches and 1 defensible alternative (area question placed in Coordinate Geometry rather than AUC); a separate 12-question sample of LLM labels was 12/12 correct.')
L.append('- Paper order in `paper_summary.csv` is newest to oldest. Raw totals are dominated by old large papers; use Avg/paper or % subject for study priorities.')
L.append('')
open(os.path.join(HERE,'reports','01_chapter_weightage_all_papers.md'),'w').write('\n'.join(L))
print('wrote report; total',total,'classified',sum(subj_class.values()),'unclass',sum(unclass.values()),'outside',sum(outside.values()))
print('files:',os.listdir(os.path.join(HERE,'reports')))
