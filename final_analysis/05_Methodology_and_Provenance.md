# 05 - Methodology, Provenance and Review

## Why this is a hybrid

| Layer | Source | Use | Confidence |
| :--- | :--- | :--- | :--- |
| Current-syllabus priorities | Vedantu 2024-2026 lecture data (normalized to 65 chapters) | Study order, tiers, Qs/shift | High for current NTA pattern; it is curated data, not a fresh 173-paper count. |
| Historical counts | DeepSeek 173-paper extraction (15,825 questions) | Historical lookup, per-paper practice map, year trends | High for text-readable questions; low for organic schemes and calculus notation. |
| 2025 shift breakdown | DeepSeek question map (classifier-based) | Per-shift chapter distribution | Better than Gemini's 750-question appendix; still classifier-based. |

## What the two prior analyses actually were

- **DeepSeek:** 173 PDFs, 15,825 questions, bbox extraction, strict answer-key cut, 3! section detection, keyword classification + 802 LLM recoveries. 14,437 classified (91.2%); 1,221 unclassified; 167 outside list.
- **Gemini:** only the 10 January-2025 papers (750 questions) were classified. The subject tables were hardcoded from the Vedantu 2024-2026 slides, not derived from 173 PDFs. The “all 173 papers” README claim was therefore inaccurate.

## Verified review findings

- Gemini's 750-question appendix agreed with the DeepSeek map on only **47.7%** of chapters (Physics 55.2%, Maths 54.0%, Chemistry 34.0%) and contained clear errors (e.g., letter arrangements labelled Statistics, remainder-by-23 labelled Definite Integration). It is archived, not used.
- The “~40% of organic questions are reaction schemes” figure was never measured. Measured proxies: 780 Chemistry questions unclassified; 372 scheme/image-like tags across all subjects.
- Gemini's “72 questions / 3-year cycle” misreads its table: 72 is the average **per year**; the three-year total is ~216.
- The “top 20 chapters > 65%” claim is false: the top 20 account for **46.3%** of the 1,507 average annual questions (top 25 = 54.5%).
- The outside-list total is 167: Polymers 53, Surface 35, Everyday 34, Hydrogen/s-block 24, Environmental 17, Solid State 4. Earlier summaries omitted Environmental 17.
- DeepSeek's Sets row includes 38 strict negation/contrapositive questions; removing them leaves 451, still #2 in Maths. The distortion affects counts, not the top-level order.

## DeepSeek pipeline limits

- **Organic:** 780 Chemistry questions unclassified (image reaction schemes); GOC/Hydrocarbons/Haloalkanes/Alcohols/Amines undercounted.
- **Calculus:** Indefinite Integrals = 0, Differentiation = 19; bare integral signs were absorbed into Definite Integration.
- **Old-paper skew:** 2002-2005 have 225 questions; 2006 150; 2007 120; 2008 105; most modern papers 75/90. Raw totals over-weight old mechanics.
- **Coverage:** 91.2% overall; Chemistry 82.0%; Physics 99.4%; Maths 92.3%.

## What was removed and what was preserved

- `deepseek_analysis/` and `gemini_analysis/` were deleted as standalone folders.
- All key data was copied into `data/`: the 15,825-row question map, chapter tables, year matrix, paper summary, parsed/classified JSON, lecture JSON and LLM labels.
- Original documents are preserved in `archive/`: the DeepSeek report, Gemini subject tables/overall table/study plan/2025 appendix/generator, and prior review files.
- The pre-analysis Markdown backup is preserved in `backups/md_20261123_215819/`.
- Both source folders remain recoverable from git history.

## Regeneration

```bash
python3 final_analysis/scripts/build_final_analysis.py
```

This rebuilds `README.md` and `01`-`05` from `data/lecture_weightage.json` plus the DeepSeek CSVs. No dependency on the deleted folders.
