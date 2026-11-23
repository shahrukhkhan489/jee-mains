# JEE Main Final Analysis

**One consolidated answer, built from the two prior analyses but no longer dependent on either folder.**

This is a **hybrid**: current-syllabus priorities come from the Vedantu 2024-2026 weightage data; historical counts come from the DeepSeek extraction of all 173 papers (2002-2025). Organic, calculus and modern-physics priorities are explicitly taken from the lecture data because the PDF text layer cannot see schemes/notation reliably.

## Snapshot

- **173 papers** parsed (2002-2025), **15,825 questions** before answer keys.
- **14,437 (91.2%)** placed into one of 65 chapters; **1,221 unclassified**; **167 outside the 65-chapter list**.
- Second-pass LLM recovered **802** of 1073 text-rich questions; 271 returned NO_SIGNAL.
- Current-priority table: **1,507 average annual questions** across 65 chapters; top 20 account for **697 (46.3%)**, not the often-quoted 65%.

## Top 10 current priorities (lecture 2024-2026, per year)

| # | Subject | Chapter | Avg/year | Qs/shift | DS 173 Qs |
| ---: | :--- | :--- | ---: | :---: | ---: |
| 1 | Mathematics | Coordinate Geometry (Lines, Circles, Conics) | 72 | 3 - 4 | 869 |
| 2 | Chemistry | Basics of Organic Chemistry (GOC) | 43 | 2 - 3 | 166 |
| 3 | Physics | Heat and Thermodynamics | 43 | 2 - 3 | 463 |
| 4 | Chemistry | Coordination Compounds | 42 | 2 - 3 | 338 |
| 5 | Physics | Properties of Matter (Solids & Fluids) | 37 | 1 - 2 | 201 |
| 6 | Mathematics | Matrices & Determinants | 36 | 1 - 2 | 187 |
| 7 | Mathematics | Three-Dimensional Geometry (3D) | 35 | 1 - 2 | 192 |
| 8 | Mathematics | Definite Integration | 32 | 1 - 2 | 360 |
| 9 | Mathematics | Sequence & Series | 32 | 1 - 2 | 246 |
| 10 | Physics | Current Electricity | 32 | 1 - 2 | 519 |

## Files

| File | Purpose |
| :--- | :--- |
| `01_Priority_and_Weightage.md` | Main study table: 2024/2025/3-year lecture data, DeepSeek evidence, data-quality flags. |
| `02_Historical_Evidence.md` | DeepSeek 173-paper coverage, historical top chapters, year trends, limitations. |
| `03_2025_Shift_Analysis.md` | New 2025 shift breakdown generated from the audited question map. |
| `04_Study_Plan.md` | Phases + priority order for the 12 unstudied chapters. |
| `05_Methodology_and_Provenance.md` | Sources, pipeline, corrections, limitations, what was archived/deleted. |
| `data/` | Question map (15,825 rows), chapter CSVs, year matrix, paper summary, lecture JSON, LLM labels. |
| `scripts/build_final_analysis.py` | Regenerates these documents from `data/`. |
| `backups/` | Verified copy of the pre-analysis README and docs. |
| `archive/` | Original DeepSeek reports, Gemini tables/plan/2025 appendix/generator, and prior review files. |

## How to use

1. Study in the order of `01_Priority_and_Weightage.md` (lecture-based current priority).
2. When you finish a chapter, filter `data/question_chapter_map.csv` by that chapter for practice questions across 173 papers.
3. Use `02_Historical_Evidence.md` to sanity-check whether a chapter was historically frequent; do not use its organic/calculus counts as priority.
4. Use `04_Study_Plan.md` for the next-chapter order, especially the 12 unstudied chapters.

> **Never quote:** Gemini's “173-paper” claim (it classified 750 questions + lecture data), DeepSeek's GOC #14 / Indefinite 0 as exam truth, or the claim that top 20 chapters are >65% of questions. The measured concentration is 46.3%.
