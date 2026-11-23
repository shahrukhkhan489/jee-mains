# DeepSeek analysis — JEE Main chapter weightage from 173 papers

This folder contains a separate, self-contained analysis so it does not collide with the existing `docs/`, `raw_sources/`, or `papers/` structure.

## Deliverable

- **`reports/01_chapter_weightage_all_papers.md`** — main report: coverage, subject-wise chapter tables, top-20 overall, year-wise totals, method and caveats.
- `reports/chapter_weightage_all_papers.csv` — the same weightage table in machine-readable form (65 chapters plus unclassified/outside rows).
- `reports/chapter_year_matrix.csv` — chapter × year question counts (2002–2025).
- `reports/question_chapter_map.csv` — every question with its paper, year, shift, section, assigned chapter, keyword score and margin (15,825 rows).
- `reports/paper_summary.csv` — processing order (newest first), per-paper question counts and detected subject order.

## Sources and scope

- All **173 question papers** in `papers/` (2002–2025), newest first, answer-key sections excluded.
- Question text extracted with `pdftotext -bbox-layout` for reading order, then split on `Q1..Qn`.
- **15,825 questions** parsed; no missing question blocks.
- **65 chapters** from the lecture weightage list (`docs/02_Chapterwise_Weightage_Analysis.md`), with per-question assignment.
- Paper patterns differ: 2002–2005 have 225 questions, 2006 has 150, 2007 has 120, 2008 has 105; most papers have 90 (pre-2025) or 75 (2025). Use `Avg/paper` or `% of subject`, not raw totals, for priorities.

## Method

1. `parse_papers.py` extracts text, cuts at `ANSWER KEYS`, and builds question blocks.
2. `classify_papers.py`:
   - detects the three subject sections per paper by evidence scoring (2025 is Maths → Physics → Chemistry; all older papers are Physics → Chemistry → Maths);
   - classifies each question only within its section;
   - uses a weighted keyword/notation taxonomy (`chapters.py`) with plural handling and Unicode math normalization;
   - labels scheme-only or text-poor questions `Unclassified` and chapters absent from the 65-chapter list as `Outside current chapter list`.
3. `build_report.py` aggregates counts and writes the report/CSVs.

Regenerate with:

```bash
python3 deepseek_analysis/parse_papers.py
python3 deepseek_analysis/classify_papers.py
python3 deepseek_analysis/build_report.py
```

## Coverage (read this before using the table)

- Overall: **13,905 / 15,825 (87.9%)** questions placed in a chapter; 1,753 unclassified (11.1%); 167 outside the 65-chapter list (1.1%).
- Physics: 99.4% classified. Mathematics: 86.0%. **Chemistry: 78.2%.**
- Chemistry's remaining unclassified share is mostly organic reaction-scheme questions whose reagents/products are images, so organic chapters (GOC, Hydrocarbons, Haloalkanes, Alcohols, Amines) are **under-counted**. Cross-check with the lecture weightage in `docs/02_Chapterwise_Weightage_Analysis.md`.
- **Second pass:** a parallel LLM classified **270** of the 1,073 text-rich unclassified questions (Physics 160, Chemistry 110); a 12-question sample was 12/12 correct. The other **803** text-rich questions were not processed after the classifier agents failed repeatedly; they remain in the Unclassified row rather than being guessed.
- Outside-list topics found in old papers but absent from the lecture list: polymers, surface chemistry, chemistry in everyday life, environmental chemistry, hydrogen/s-block, solid state. They are reported separately rather than forced into a wrong chapter.
- Definite and indefinite integrals share the `∫` glyph in extracted text; integral-symbol-only questions are counted under Definite Integration. The Indefinite row therefore shows only explicit wording.

## Backup

The pre-analysis Markdown state is preserved byte-for-byte in:

`deepseek_analysis/backups/md_20261123_215819/` (`README.md` + `docs/`)

## Validation

- Parser: 173/173 papers, 15,825 questions, 0 missing blocks, all answer-key boundaries found.
- Assignment audit: all 15,825 rows are in `question_chapter_map.csv`; a 15-question keyword spot-check gave 14 clear matches and 1 defensible alternative, and a 12-question LLM-label sample was 12/12 correct.
- Accounting: each subject's classified + unclassified + outside counts equal its 5,275 parsed questions; the CSV totals equal 15,825.

## Notes

This folder is intentionally separate from `docs/` and the earlier DeepSeek/Gemini deliverables. Nothing in the existing documentation was overwritten; the backup is a copy, not a move.
