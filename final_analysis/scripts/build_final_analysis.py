#!/usr/bin/env python3
"""Build the final hybrid JEE Main analysis from self-contained data files."""
import json, csv, os, re
from collections import Counter, defaultdict

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)
DATA=os.path.join(ROOT,'data')
OUT=ROOT

lecture=json.load(open(os.path.join(DATA,'lecture_weightage.json')))
SUBJECTS=['Physics','Chemistry','Mathematics']
ALIAS={'Practical Organic Chemistry (POC)':'Practical Organic Chemistry'}

def canon(ch): return ALIAS.get(ch,ch)
for s in SUBJECTS:
    for r in lecture[s]: r['chapter']=canon(r['chapter'])

ds={}
for r in csv.DictReader(open(os.path.join(DATA,'chapter_weightage_all_papers.csv'))):
    if r['type']!='chapter': continue
    ds[(r['subject'],r['chapter'])]={'q':int(r['questions']),'avg':float(r['avg_per_paper']),
        'papers':int(r['papers_with_question']) if r['papers_with_question'] else 0,
        'rank':int(r['rank_in_subject'])}
qrows=list(csv.DictReader(open(os.path.join(DATA,'question_chapter_map.csv'))))
total=len(qrows)

def is_chapter(ch): return ch!='Unclassified' and not ch.startswith('Outside')
cover={}
for s in SUBJECTS:
    rs=[r for r in qrows if r['section_subject']==s]
    cover[s]={'total':len(rs),'classified':sum(1 for r in rs if is_chapter(r['chapter'])),
              'unclass':sum(1 for r in rs if r['chapter']=='Unclassified'),
              'outside':sum(1 for r in rs if r['chapter'].startswith('Outside')),
              'llm':sum(1 for r in rs if r['chapter_source']=='llm')}
manifest=json.load(open(os.path.join(DATA,'llm_manifest.json')))
classified=sum(c['classified'] for c in cover.values())
unclass=sum(c['unclass'] for c in cover.values())
outside=sum(c['outside'] for c in cover.values())

def pct(a,b): return f'{100*a/b:.1f}%'
def note(s,ch):
    chem_org={'Basics of Organic Chemistry (GOC)','Hydrocarbons','Haloalkanes and Haloarenes',
              'Alcohols, Phenols and Ethers','Aldehydes, Ketones & Carboxylic Acids',
              'Compounds Containing Nitrogen (Amines)'}
    if s=='Chemistry' and ch in chem_org:
        return 'DS lower bound: scheme-heavy organic text missing'
    if s=='Mathematics' and ch=='Indefinite Integrals':
        return 'DS artifact: bare integral signs diverted to Definite'
    if s=='Mathematics' and ch=='Differentiation':
        return 'DS undercount: derivative notation fragmented'
    if s=='Mathematics' and ch=='Sets, Relations & Functions':
        return 'DS includes ~38 reasoning-type labels'
    if s=='Physics' and ch in {'Atoms and Nuclei','Dual Nature of Radiation',
                               'Semiconductors / Electronic Devices','Units & Measurements'}:
        return 'DS all-era count underweights modern papers'
    if s=='Physics' and ch in {'Current Electricity','Kinematics (1D, 2D, Circular)'}:
        return 'DS all-era count inflated by old papers'
    if s=='Chemistry' and ch=='Practical Organic Chemistry':
        return 'DS count mapped from POC label'
    return '—'

def subject_rows(s):
    rows=[]
    for r in lecture[s]:
        d=ds.get((s,r['chapter']),{'q':0,'avg':0.0,'papers':0,'rank':0})
        rows.append({'chapter':r['chapter'],'y24':r['year_2024'],'y25':r['year_2025'],
                     'avg':r['yearly_avg_2024_26'],'shift':r['qs_per_shift'],'tier':r['tier'],
                     'branch':r.get('branch',''),'ds_q':d['q'],'ds_avg':d['avg'],
                     'note':note(s,r['chapter'])})
    return sorted(rows,key=lambda x:(-x['avg'],x['chapter']))

subject_avg_sum={s:sum(r['yearly_avg_2024_26'] for r in lecture[s]) for s in SUBJECTS}
all_rows=[]
for s in SUBJECTS:
    for r in subject_rows(s): r['subject']=s; all_rows.append(r)
all_sorted=sorted(all_rows,key=lambda x:(-x['avg'],x['subject'],x['chapter']))
top20=all_sorted[:20]
top20_sum=sum(r['avg'] for r in top20)
avg_total=sum(subject_avg_sum.values())

def md_table(rows, cols, headers):
    out=['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']
    for r in rows:
        out.append('| '+' | '.join(str(r[c]) for c in cols)+' |')
    return '\n'.join(out)

# ---------- README ----------
readme=[]
readme.append('# JEE Main Final Analysis')
readme.append('')
readme.append('**One consolidated answer, built from the two prior analyses but no longer dependent on either folder.**')
readme.append('')
readme.append('This is a **hybrid**: current-syllabus priorities come from the Vedantu 2024-2026 weightage data; historical counts come from the DeepSeek extraction of all 173 papers (2002-2025). Organic, calculus and modern-physics priorities are explicitly taken from the lecture data because the PDF text layer cannot see schemes/notation reliably.')
readme.append('')
readme.append('## Snapshot')
readme.append('')
readme.append(f'- **173 papers** parsed (2002-2025), **{total:,} questions** before answer keys.')
readme.append(f'- **{classified:,} ({pct(classified,total)})** placed into one of 65 chapters; **{unclass:,} unclassified**; **{outside:,} outside the 65-chapter list**.')
readme.append(f'- Second-pass LLM recovered **{manifest["placed"]}** of {manifest["labeled_unique"]} text-rich questions; {manifest["no_signal"]} returned NO_SIGNAL.')
readme.append(f'- Current-priority table: **{avg_total:,} average annual questions** across 65 chapters; top 20 account for **{top20_sum} ({pct(top20_sum,avg_total)})**, not the often-quoted 65%.')
readme.append('')
readme.append('## Top 10 current priorities (lecture 2024-2026, per year)')
readme.append('')
readme.append('| # | Subject | Chapter | Avg/year | Qs/shift | DS 173 Qs |')
readme.append('| ---: | :--- | :--- | ---: | :---: | ---: |')
for i,r in enumerate(all_sorted[:10],1):
    readme.append(f'| {i} | {r["subject"]} | {r["chapter"]} | {r["avg"]} | {r["shift"]} | {r["ds_q"]:,} |')
readme.append('')
readme.append('## Files')
readme.append('')
readme.append('| File | Purpose |')
readme.append('| :--- | :--- |')
readme.append('| `01_Priority_and_Weightage.md` | Main study table: 2024/2025/3-year lecture data, DeepSeek evidence, data-quality flags. |')
readme.append('| `02_Historical_Evidence.md` | DeepSeek 173-paper coverage, historical top chapters, year trends, limitations. |')
readme.append('| `03_2025_Shift_Analysis.md` | New 2025 shift breakdown generated from the audited question map. |')
readme.append('| `04_Study_Plan.md` | Phases + priority order for the 12 unstudied chapters. |')
readme.append('| `05_Methodology_and_Provenance.md` | Sources, pipeline, corrections, limitations, what was archived/deleted. |')
readme.append('| `data/` | Question map (15,825 rows), chapter CSVs, year matrix, paper summary, lecture JSON, LLM labels. |')
readme.append('| `scripts/build_final_analysis.py` | Regenerates these documents from `data/`. |')
readme.append('| `backups/` | Verified copy of the pre-analysis README and docs. |')
readme.append('| `archive/` | Original DeepSeek reports, Gemini tables/plan/2025 appendix/generator, and prior review files. |')
readme.append('')
readme.append('## How to use')
readme.append('')
readme.append('1. Study in the order of `01_Priority_and_Weightage.md` (lecture-based current priority).')
readme.append('2. When you finish a chapter, filter `data/question_chapter_map.csv` by that chapter for practice questions across 173 papers.')
readme.append('3. Use `02_Historical_Evidence.md` to sanity-check whether a chapter was historically frequent; do not use its organic/calculus counts as priority.')
readme.append('4. Use `04_Study_Plan.md` for the next-chapter order, especially the 12 unstudied chapters.')
readme.append('')
readme.append('> **Never quote:** Gemini\'s “173-paper” claim (it classified 750 questions + lecture data), DeepSeek\'s GOC #14 / Indefinite 0 as exam truth, or the claim that top 20 chapters are >65% of questions. The measured concentration is 46.3%.')
readme.append('')
open(os.path.join(OUT,'README.md'),'w').write('\n'.join(readme))

# ---------- 01 ----------
l=[]
l.append('# 01 - Priority and Weightage')
l.append('')
l.append('**Primary use:** decide what to study next. **Priority column:** Vedantu 2024-2026 lecture data. **Evidence columns:** DeepSeek 173-paper count (2002-2025).')
l.append('')
l.append('> **Column semantics:** `2024` and `2025` are full-year totals across all shifts; `Avg 2024-26` is the average annual total, not the average of the two displayed years. `Qs/Shift` is the lecture estimate. DeepSeek counts are raw classified totals and are **not** per-shift; compare them as historical context only.')
l.append('')
l.append(f'## Concentration check')
l.append('')
l.append(f'The 65 chapters sum to **{avg_total:,} average annual questions**. The top 20 chapters sum to **{top20_sum} = {pct(top20_sum,avg_total)}**; the top 25 sum to **{sum(r["avg"] for r in all_sorted[:25])} = {pct(sum(r["avg"] for r in all_sorted[:25]),avg_total)}**. The older “top 20 > 65%” claim is false.')
l.append('')
l.append('## Top 20 overall (current priority)')
l.append('')
l.append('| # | Subject | Chapter | Avg/year | Qs/shift | DS 173 Qs | DS Avg/paper |')
l.append('| ---: | :--- | :--- | ---: | :---: | ---: | ---: |')
for i,r in enumerate(top20,1):
    l.append(f'| {i} | {r["subject"]} | {r["chapter"]} | {r["avg"]} | {r["shift"]} | {r["ds_q"]:,} | {r["ds_avg"]:.2f} |')
l.append('')
for s in SUBJECTS:
    rows=subject_rows(s)
    l.append(f'## {s} chapters')
    l.append('')
    l.append('| # | Chapter | 2024 | 2025 | Avg 2024-26 | Qs/shift | Tier | DS 173 Qs | DS Avg/paper | Evidence note |')
    l.append('| ---: | :--- | ---: | ---: | ---: | :---: | :--- | ---: | ---: | :--- |')
    for i,r in enumerate(rows,1):
        l.append(f'| {i} | {r["chapter"]} | {r["y24"]} | {r["y25"]} | {r["avg"]} | {r["shift"]} | {r["tier"]} | {r["ds_q"]:,} | {r["ds_avg"]:.2f} | {r["note"]} |')
    l.append('')
l.append('## Which column to trust')
l.append('')
l.append('- **Current priority / what to study:** the lecture `Avg`/`Qs/shift` columns, especially for organic, calculus and modern physics.')
l.append('- **Historical frequency / how often it appeared:** DeepSeek `DS 173 Qs` and `DS Avg/paper`.')
l.append('- **Never mix the units:** a DeepSeek raw total is 23 years of classified text; a lecture annual total is one year across all shifts. Use `Qs/shift` or `DS Avg/paper` for comparisons.')
l.append('')
open(os.path.join(OUT,'01_Priority_and_Weightage.md'),'w').write('\n'.join(l))

# ---------- 02 ----------
l=[]
l.append('# 02 - Historical Evidence from 173 Papers')
l.append('')
l.append('**Primary use:** historical lookup and audit. **Do not use this table alone for study priority** — Chemistry organic and Mathematics calculus are systematically undercounted by the PDF text layer.')
l.append('')
l.append('## Coverage')
l.append('')
l.append('| Subject | Questions | Classified | LLM recovered | Unclassified | Outside list | Coverage |')
l.append('| :--- | ---: | ---: | ---: | ---: | ---: | ---: |')
for s in SUBJECTS:
    c=cover[s]
    l.append(f'| {s} | {c["total"]:,} | {c["classified"]:,} | {c["llm"]:,} | {c["unclass"]:,} | {c["outside"]:,} | {pct(c["classified"],c["total"])} |')
l.append(f'| **Total** | **{total:,}** | **{classified:,}** | **{sum(c["llm"] for c in cover.values()):,}** | **{unclass:,}** | **{outside:,}** | **{pct(classified,total)}** |')
l.append('')
l.append('## Historical top 15 by DeepSeek avg/paper')
l.append('')
l.append('| # | Subject | Chapter | DS Qs | DS Avg/paper | Warning |')
l.append('| ---: | :--- | :--- | ---: | ---: | :--- |')
ds_sorted=sorted([(k,v) for k,v in ds.items()],key=lambda kv:-kv[1]['avg'])[:15]
for i,((s,ch),v) in enumerate(ds_sorted,1):
    l.append(f'| {i} | {s} | {ch} | {v["q"]:,} | {v["avg"]:.2f} | {note(s,ch)} |')
l.append('')
l.append('## Year-wise totals')
l.append('')
l.append('| Year | Papers | Questions | Classified | Unclassified | Outside list |')
l.append('| ---: | ---: | ---: | ---: | ---: | ---: |')
years=sorted({int(r['year']) for r in qrows})
for y in years:
    rs=[r for r in qrows if int(r['year'])==y]
    papers=len({r['paper'] for r in rs})
    l.append(f'| {y} | {papers} | {len(rs):,} | {sum(1 for r in rs if is_chapter(r["chapter"])):,} | {sum(1 for r in rs if r["chapter"]=="Unclassified"):,} | {sum(1 for r in rs if r["chapter"].startswith("Outside")):,} |')
l.append('')
l.append('## Known limitations')
l.append('')
l.append('- **Organic chemistry:** 780 Chemistry questions remain unclassified, mostly image-based reaction schemes. GOC is #14 in DeepSeek (166) but #1 in the lecture data. Use lecture priority.')
l.append('- **Calculus notation:** Indefinite Integrals = 0; Differentiation = 19. Bare `∫` questions were assigned to Definite Integration. These rows are not usable for priority.')
l.append('- **Old-paper skew:** 2002-2005 have 225 questions; 2006: 150; 2007: 120; 2008: 105; most others 75/90. Raw totals over-weight old mechanics/classical chapters.')
l.append('- **Outside list:** 167 old-syllabus/legacy questions were kept separate rather than forced into current chapters (Polymers 53, Surface 35, Everyday 34, Hydrogen/s-block 24, Environmental 17, Solid State 4).')
l.append('- **Sets:** 38 strict reasoning-type questions (negation/contrapositive) are included in Sets; removing them would leave Sets at 451, still #2.')
l.append('')
l.append('**Audit file:** `data/question_chapter_map.csv` contains all 15,825 rows with paper, question number, subject, chapter, score, margin and `chapter_source`.')
l.append('')
open(os.path.join(OUT,'02_Historical_Evidence.md'),'w').write('\n'.join(l))

# ---------- 03 2025 shifts ----------
l=[]
l.append('# 03 - 2025 January Shift Analysis')
l.append('')
l.append('**Generated from the audited DeepSeek question map**, not from Gemini\'s 750-question appendix (which had only 47.7% exact chapter agreement with this map and clear misclassifications).')
l.append('')
l.append('Ten papers, 75 questions each (25 Mathematics, 25 Physics, 25 Chemistry), newest to oldest.')
l.append('')
paper_order=[]
for r in csv.DictReader(open(os.path.join(DATA,'paper_summary.csv'))):
    if r['session']=='2025_Jan' and r['year']=='2025':
        paper_order.append((int(r['rank']),r['paper']))
paper_order.sort()
l.append('| Paper | Mathematics top 5 | Physics top 5 | Chemistry top 5 | Unclassified |')
l.append('| :--- | :--- | :--- | :--- | ---: |')
for rank,paper in paper_order:
    rs=[r for r in qrows if r['paper']==paper]
    cells=[]
    for s in ['Mathematics','Physics','Chemistry']:
        c=Counter(r['chapter'] for r in rs if r['section_subject']==s and is_chapter(r['chapter']))
        cells.append(', '.join(f'{ch} ({n})' for ch,n in c.most_common(5)) or '—')
    un=sum(1 for r in rs if r['chapter']=='Unclassified')
    l.append(f'| {paper.replace("JEE_Main_","").replace(".pdf","")} | {cells[0]} | {cells[1]} | {cells[2]} | {un} |')
l.append('')
l.append('## 2025 January chapter totals (classified)')
l.append('')
for s in SUBJECTS:
    l.append(f'### {s}')
    l.append('')
    c=Counter(r['chapter'] for r in qrows if r['year']=='2025' and r['session']=='2025_Jan' and r['section_subject']==s and is_chapter(r['chapter']))
    l.append('| Chapter | Questions |')
    l.append('| :--- | ---: |')
    for ch,n in c.most_common(10): l.append(f'| {ch} | {n} |')
    l.append('')
l.append('> The original Gemini per-shift appendix is preserved in `archive/gemini/2025_Jan_shifts_classified.md` for provenance, but it is not the recommended reference.')
l.append('>')
l.append('> **Accuracy note:** these labels are classifier-based. The subject column is trustworthy, but individual chapter labels can be wrong (for example, integral-defined range questions occasionally land in Sets). Verify the question text before high-stakes use.')
l.append('')
open(os.path.join(OUT,'03_2025_Shift_Analysis.md'),'w').write('\n'.join(l))

# ---------- 04 study plan ----------
l=[]
l.append('# 04 - Study Plan')
l.append('')
l.append('The phase structure is adapted from Gemini\'s study plan; the chapter priorities come from the lecture 2024-2026 data. Target marks are editorial, not data.')
l.append('')
l.append('## Phase 1 - Quick-win foundation')
l.append('')
l.append('- **Physics:** Units & Measurements + Dual Nature + Atoms & Nuclei + Semiconductors (~20 marks).')
l.append('- **Chemistry:** Biomolecules + Periodic Table + Coordination Compounds + Chemical Bonding.')
l.append('- **Mathematics:** Matrices & Determinants + Vector Algebra + Statistics + Sequence & Series.')
l.append('')
l.append('## Phase 2 - Core heavyweights')
l.append('')
l.append('- **Mathematics:** Coordinate Geometry (including Conic Sections) + Three-Dimensional Geometry.')
l.append('- **Physics:** Heat & Thermodynamics + Current Electricity + Electrostatics + Properties of Matter.')
l.append('- **Chemistry:** GOC (including Isomerism) + Aldehydes/Ketones/Carboxylic Acids + d- and f-Block + Electrochemistry.')
l.append('')
l.append('## Phase 3 - Targeted finishers')
l.append('')
l.append('- **Mathematics:** Definite Integration + Differential Equations + Area Under the Curve + Binomial Theorem.')
l.append('- **Physics:** Geometrical Optics + Wave Optics + Kinematics + Gravitation.')
l.append('- **Chemistry:** Thermodynamics + Chemical Kinetics + Solutions + Amines.')
l.append('')
l.append('## Your 12 unstudied chapters - recommended order')
l.append('')
l.append('| Order | Your label | Maps to chapter | Avg/year | Qs/shift | Urgency | Action |')
l.append('| ---: | :--- | :--- | ---: | :---: | :--- | :--- |')
plan=[
 ('1','Conic Sections','Coordinate Geometry (Lines, Circles, Conics)','Critical','Highest-yield block; do this first.'),
 ('2','Isomerism','Basics of Organic Chemistry (GOC)','Critical','Foundation for all organic mechanisms.'),
 ('3','Equilibrium (Partially)','Equilibrium (Physical & Ionic)','High','Finish pH, buffers, Ksp, Le Chatelier.'),
 ('4','Probability','Probability','High','Bayes + conditional + distribution.'),
 ('5','Capacitors','Capacitor','Medium','Short formula chapter; combine with electrostatics.'),
 ('6','Alternating Current','Alternating Current (AC)','Medium','LCR/resonance/power factor.'),
 ('7','Waves','Waves (Sound & String)','Medium','Organ pipes, beats, Doppler.'),
 ('8','Electromagnetic Waves','Electromagnetic Waves','Medium','Short theory; quick marks.'),
 ('9','Statistics','Statistics','Quick win','Mean/variance/SD; 1 direct question often.'),
 ('10','Practical Organic Chemistry','Practical Organic Chemistry','Medium','Qualitative tests + purification.'),
 ('11','Redox Reactions','Redox Reactions','Low','n-factor/balancing; links to electrochemistry.'),
 ('12','Indefinite Integration','Indefinite Integrals','Low','Do only after Definite; DeepSeek row is an artifact.')]
# lookup lecture avg
lookup={r['chapter']:r for s in SUBJECTS for r in lecture[s]}
for order,label,ch,urgency,action in plan:
    r=lookup.get(ch)
    avg=r['yearly_avg_2024_26'] if r else '—'; shift=r['qs_per_shift'] if r else '—'
    l.append(f'| {order} | {label} | {ch} | {avg} | {shift} | {urgency} | {action} |')
l.append('')
l.append('> “Conic Sections” is part of Coordinate Geometry, and “Isomerism” sits under GOC/Hydrocarbons in the lecture tables; neither is a separate chapter row.')
l.append('')
open(os.path.join(OUT,'04_Study_Plan.md'),'w').write('\n'.join(l))

# ---------- 05 methodology ----------
l=[]
l.append('# 05 - Methodology, Provenance and Review')
l.append('')
l.append('## Why this is a hybrid')
l.append('')
l.append('| Layer | Source | Use | Confidence |')
l.append('| :--- | :--- | :--- | :--- |')
l.append('| Current-syllabus priorities | Vedantu 2024-2026 lecture data (normalized to 65 chapters) | Study order, tiers, Qs/shift | High for current NTA pattern; it is curated data, not a fresh 173-paper count. |')
l.append('| Historical counts | DeepSeek 173-paper extraction (15,825 questions) | Historical lookup, per-paper practice map, year trends | High for text-readable questions; low for organic schemes and calculus notation. |')
l.append('| 2025 shift breakdown | DeepSeek question map (classifier-based) | Per-shift chapter distribution | Better than Gemini\'s 750-question appendix; still classifier-based. |')
l.append('')
l.append('## What the two prior analyses actually were')
l.append('')
l.append('- **DeepSeek:** 173 PDFs, 15,825 questions, bbox extraction, strict answer-key cut, 3! section detection, keyword classification + 802 LLM recoveries. 14,437 classified (91.2%); 1,221 unclassified; 167 outside list.')
l.append('- **Gemini:** only the 10 January-2025 papers (750 questions) were classified. The subject tables were hardcoded from the Vedantu 2024-2026 slides, not derived from 173 PDFs. The “all 173 papers” README claim was therefore inaccurate.')
l.append('')
l.append('## Verified review findings')
l.append('')
l.append('- Gemini\'s 750-question appendix agreed with the DeepSeek map on only **47.7%** of chapters (Physics 55.2%, Maths 54.0%, Chemistry 34.0%) and contained clear errors (e.g., letter arrangements labelled Statistics, remainder-by-23 labelled Definite Integration). It is archived, not used.')
l.append('- The “~40% of organic questions are reaction schemes” figure was never measured. Measured proxies: 780 Chemistry questions unclassified; 372 scheme/image-like tags across all subjects.')
l.append('- Gemini\'s “72 questions / 3-year cycle” misreads its table: 72 is the average **per year**; the three-year total is ~216.')
l.append('- The “top 20 chapters > 65%” claim is false: the top 20 account for **46.3%** of the 1,507 average annual questions (top 25 = 54.5%).')
l.append('- The outside-list total is 167: Polymers 53, Surface 35, Everyday 34, Hydrogen/s-block 24, Environmental 17, Solid State 4. Earlier summaries omitted Environmental 17.')
l.append('- DeepSeek\'s Sets row includes 38 strict negation/contrapositive questions; removing them leaves 451, still #2 in Maths. The distortion affects counts, not the top-level order.')
l.append('')
l.append('## DeepSeek pipeline limits')
l.append('')
l.append('- **Organic:** 780 Chemistry questions unclassified (image reaction schemes); GOC/Hydrocarbons/Haloalkanes/Alcohols/Amines undercounted.')
l.append('- **Calculus:** Indefinite Integrals = 0, Differentiation = 19; bare integral signs were absorbed into Definite Integration.')
l.append('- **Old-paper skew:** 2002-2005 have 225 questions; 2006 150; 2007 120; 2008 105; most modern papers 75/90. Raw totals over-weight old mechanics.')
l.append('- **Coverage:** 91.2% overall; Chemistry 82.0%; Physics 99.4%; Maths 92.3%.')
l.append('')
l.append('## What was removed and what was preserved')
l.append('')
l.append('- `deepseek_analysis/` and `gemini_analysis/` were deleted as standalone folders.')
l.append('- All key data was copied into `data/`: the 15,825-row question map, chapter tables, year matrix, paper summary, parsed/classified JSON, lecture JSON and LLM labels.')
l.append('- Original documents are preserved in `archive/`: the DeepSeek report, Gemini subject tables/overall table/study plan/2025 appendix/generator, and prior review files.')
l.append('- The pre-analysis Markdown backup is preserved in `backups/md_20261123_215819/`.')
l.append('- Both source folders remain recoverable from git history.')
l.append('')
l.append('## Regeneration')
l.append('')
l.append('```bash')
l.append('python3 final_analysis/scripts/build_final_analysis.py')
l.append('```')
l.append('')
l.append('This rebuilds `README.md` and `01`-`05` from `data/lecture_weightage.json` plus the DeepSeek CSVs. No dependency on the deleted folders.')
l.append('')
open(os.path.join(OUT,'05_Methodology_and_Provenance.md'),'w').write('\n'.join(l))
print('generated final docs')
