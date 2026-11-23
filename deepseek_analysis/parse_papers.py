#!/usr/bin/env python3
"""Parse every JEE Main PDF into question blocks using bbox reading order."""
import glob, os, re, subprocess, html, json, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONTHS = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
HEADER = re.compile(r'^(JEE Main .*MathonGo|MathonGo|Question Paper|Join the Most Relevant.*|https?://\S+)$', re.I)

def bbox_text(pdf):
    xml = subprocess.run(['pdftotext','-bbox-layout',pdf,'-'],capture_output=True).stdout.decode('utf-8','ignore')
    pages = re.findall(r'<page width="[\d.]+" height="[\d.]+">(.*?)</page>', xml, re.S)
    out = []
    for p in pages:
        words = []
        for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', p):
            words.append((round(float(m.group(2))/3)*3, float(m.group(1)), html.unescape(m.group(5))))
        lines = {}
        for y,x,t in words: lines.setdefault(y,[]).append((x,t))
        for y in sorted(lines):
            line = ' '.join(t for x,t in sorted(lines[y])).strip()
            if line and not HEADER.match(line): out.append(line)
    return '\n'.join(out)

def key_start(text):
    last = None
    for m in re.finditer(r'(?im)^\s*ANSWER\s*KEYS?\s*$', text): last = m.start()
    if last is not None: return last
    for m in re.finditer(r'(?im)^\s*(?:HINTS?\s*(?:&|AND)\s*)?SOLUTIONS?\s*$', text):
        if m.start() > len(text)*0.6: last = m.start()
    return last if last is not None else len(text)

def paper_meta(path):
    base = os.path.basename(path); year = int(re.search(r'JEE_Main_(\d{4})', base).group(1))
    folder = os.path.basename(os.path.dirname(path))
    mm = re.match(r'(\d{4})_(\w{3})', folder); month = MONTHS.get(mm.group(2),0) if mm else 0
    daym = re.search(r'_(\d{2})_(\w{3})_', base)
    day = int(daym.group(1)) if daym else 0
    sm = re.search(r'Shift_(\d)', base); shift = int(sm.group(1)) if sm else 0
    return base, year, month, day, shift

def parse(path):
    base, year, month, day, shift = paper_meta(path)
    text = bbox_text(path)
    ks = key_start(text); body = text[:ks]
    marks = [(m.start(), int(m.group(1))) for m in re.finditer(r'(?m)^\s*Q\s*(\d+)\s*[\.\)]', body)]
    first = {}
    for pos,n in marks: first.setdefault(n,pos)
    positions = sorted(first.values())
    nxt = {p: positions[i+1] for i,p in enumerate(positions[:-1])}
    maxq = max(first) if first else 0
    qs = []
    for n in range(1, maxq+1):
        pos = first.get(n)
        if pos is None:
            qs.append({'q':n,'text':'','missing':True}); continue
        end = nxt.get(pos, len(body))
        block = re.sub(r'\s+',' ',body[pos:end]).strip()
        # drop repeated page furniture inside blocks
        block = re.sub(r'\bJEE Main .*? MathonGo\b','',block).strip()
        qs.append({'q':n,'text':block,'missing':False})
    return {'paper':base,'year':year,'month':month,'day':day,'shift':shift,
            'path':os.path.relpath(path,ROOT),'n':maxq,'questions':qs,
            'parsed':sum(0 if q['missing'] else 1 for q in qs),
            'key_found':ks < len(text)}

def main():
    files = sorted(glob.glob(os.path.join(ROOT,'papers','**','*.pdf'), recursive=True))
    with ThreadPoolExecutor(max_workers=6) as ex: papers = list(ex.map(parse, files))
    papers.sort(key=lambda p:(p['year'],p['month'],p['day'],p['shift'],p['paper']), reverse=True)
    os.makedirs(os.path.join(ROOT,'deepseek_analysis','data'), exist_ok=True)
    json.dump(papers, open(os.path.join(ROOT,'deepseek_analysis','data','parsed_papers.json'),'w'), ensure_ascii=False)
    total = sum(p['parsed'] for p in papers)
    print('papers',len(papers),'questions',total)
    from collections import Counter
    print(Counter(p['n'] for p in papers).most_common())
    bad = [(p['paper'],p['parsed'],p['n']) for p in papers if p['parsed']<p['n']]
    print('papers with missing blocks:',len(bad)); print(bad[:15])
    print('key not found:',[p['paper'] for p in papers if not p['key_found']][:10])

if __name__ == '__main__': main()
