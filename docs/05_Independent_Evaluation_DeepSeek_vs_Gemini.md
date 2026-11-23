# Independent Evaluation: DeepSeek vs Gemini JEE Main Analyses

> **Scope:** A source-level audit of `deepseek_analysis/` and `gemini_analysis/`, checked against the 173 PDFs, the 2024–2026 lecture weightage, and each project's own generator code.
>
> **Status:** Observations only. Neither analysis folder was modified. A prior review exists at `docs/04_DeepSeek_vs_Gemini_Analysis_Evaluation.md`; this file is an independent re-check based on the current artifacts and adds quantitative evidence that the earlier review does not contain.

---

## 1. Bottom line

| Question | Answer |
| :--- | :--- |
| Which one actually processes all 173 papers? | **DeepSeek** — 15,825 questions parsed, 14,437 classified (91.2%). |
| Which one has the better current-syllabus priorities? | **Gemini** — its chapter tables reproduce the lecturer's 2024–2026 yearly totals, including the organic chapters DeepSeek's text pipeline cannot see. |
| Which one is more reproducible and auditable? | **DeepSeek** — scripts, per-question CSV, year matrix, coverage accounting. |
| Which one is safer to quote as “empirical 173-paper analysis”? | **Neither, as marketed.** Gemini's “173 papers” claim is not supported by its generator; DeepSeek did the corpus work but has documented chemistry/calculus blind spots. |
| Best combined use | Gemini for **what to study first**; DeepSeek for **historical question lookup and audit**. |

The two projects are not equivalent artifacts. DeepSeek is a bottom-up corpus-mining pipeline; Gemini is a curated study guide built on the lecturer's 2024–2026 weightage plus a small 2025 question-classification appendix.

---

## 2. What each project actually does

### DeepSeek (`deepseek_analysis/`)

- Extracts all 173 PDFs with `pdftotext -bbox-layout`, cuts at `ANSWER KEYS`, and splits into `Q1..Qn`.
- Result: **15,825 questions**, no missing blocks, 173/173 papers.
- Assigns every question to one of 65 chapters with a keyword/notation classifier, then a second LLM pass over text-rich unclassified questions.
- Coverage: **14,437 / 15,825 = 91.2%** classified; 1,221 unclassified; 167 outside the 65-chapter lecture list.
  - Physics 99.4%; Mathematics 92.3%; **Chemistry 82.0%**.
- Outputs: `reports/01_chapter_weightage_all_papers.md`, per-chapter CSV, chapter×year matrix, paper summary, and a 15,825-row per-question map with `chapter_source`.
- Known limits, documented by the project:
  - Organic reaction-scheme questions are images in the PDF text layer; GOC ends at #14 with 166 questions, which is not its true importance.
  - `∫` and derivative notation fragment; **Indefinite Integrals = 0**, Differentiation = 19, with integral-symbol questions absorbed into Definite Integration.
  - Old-paper patterns (2002–2005: 225 questions; 2006: 150; 2007: 120; 2008: 105) skew raw totals.

### Gemini (`gemini_analysis/`)

- The README says all 173 papers were analysed, but `scripts/generate_gemini_analysis.py` shows two different things:
  1. It parses only the **10 January-2025 papers** (`papers/2025_Jan/*.pdf`) for the shift-by-shift appendix: **750 questions** (10 × 75), or **4.7%** of the DeepSeek corpus.
  2. The Physics/Chemistry/Mathematics/overall tables are **hardcoded from the Vedantu 2024–2026 lecture slides** (“Ground-truth multi-year totals” in the script), not derived from the 173 PDFs.
- The subject tables are therefore a faithful restatement of the lecture data: Coordinate Geometry 72, GOC 43, Heat & Thermodynamics 43, Coordination 42, etc.
- The 750-question appendix is the only independently classified Gemini content.

**Consequence:** Gemini's “173-paper” framing is inaccurate. It is a 2024–2026 lecture-weightage study guide plus a 2025-January appendix, not a 23-year empirical count.

---

## 3. Quantitative cross-check

### 3.1 Scope and coverage

| Metric | DeepSeek | Gemini |
| :--- | ---: | ---: |
| Papers actually classified | **173** | 10 (2025 Jan only) |
| Questions actually classified | **15,825 parsed / 14,437 placed** | 750 |
| Share of total corpus | 91.2% placed | 4.7% classified |
| Chapter source | PDF extraction + classifier + LLM | Hardcoded lecture totals + 2025 appendix |
| Per-question audit file | Yes (`question_chapter_map.csv`) | No; only snippets in one appendix |
| Year matrix | 2002–2025 | Narrative era summary only |

### 3.2 Question-level agreement

For the 750 questions Gemini does classify, I compared its chapter labels with DeepSeek's independently built map:

- **Exact chapter agreement: 358 / 750 = 47.7%.**
- Mathematics: 135/250 = 54.0%.
- Physics: 138/250 = 55.2%.
- Chemistry: **85/250 = 34.0%.**

Agreement is not accuracy — DeepSeek has its own errors — but the gap is large enough that Gemini's appendix cannot be treated as ground truth. Manual checks show clear Gemini errors in the 29 Jan Shift 2 section alone:

| Question | Gemini label | What the question actually is |
| :--- | :--- | :--- |
| Q1 (integral-defined range) | Sets, Relations & Functions | Definite Integration / integral calculus |
| Q7 (“KANPUR” letter arrangements in dictionary order) | Statistics | Permutations & Combinations |
| Q8 (λ values for a quadratic with no real roots) | Sequence & Series | Quadratic Equations |
| Q12 (remainder when divided by 23) | Definite Integration | Binomial Theorem |

These are not isolated boundary calls; they are chapter-level misses. The appendix is useful as a sketch, not as an empirical dataset.

### 3.3 Table semantics

The Gemini subject tables show “2025 Qs”, “2024 Qs” and “3-Year Avg”:

- The 2025 and 2024 columns are **full-year totals across all shifts**, not the 10 January-2025 papers. Example sums: Physics 461 (2025) and 556 (2024); the January appendix has only 250 Physics questions.
- The 3-year average includes 2026, but there is no 2026 column. Prose mentions 2026 surges (e.g., Current Electricity “48 Qs”) without a displayed 2026 count.
- The values themselves match the lecturer's slides, so they are internally consistent with their actual source — the issue is the “173 papers” claim, not the arithmetic.

---

## 4. Ranking comparison

The metrics differ, so raw numbers cannot be compared directly: DeepSeek reports totals/avg per paper across 173 papers; Gemini reports full-year totals and a 3-year average from the lecture.

| Chapter | DeepSeek (all 173) | Gemini (2024–2026 lecture) | Observation |
| :--- | :--- | :--- | :--- |
| Coordinate Geometry | #1, 869 Qs, 5.02/paper | #1, 72 avg, 3–4/shift | Both agree: the single highest-value chapter. |
| Current Electricity | #2, 519 Qs, 3.00/paper | #8, 32 avg, 1–2/shift | DeepSeek is inflated by old papers and by counting electricity-style questions broadly. |
| Kinematics | #3, 497 Qs, 2.87/paper | #7, 29 avg, 1–2/shift | DeepSeek's all-era average emphasizes mechanics more than the modern 75-question pattern does. |
| Heat & Thermodynamics | #5, 463 Qs, 2.68/paper | #1 Physics, 43 avg, 2–3/shift | Gemini's current-syllabus rank is the more useful study signal. |
| Chemical Bonding | #7 overall, 361 Qs | #4 Chemistry, 31 avg | Broad agreement within inorganic. |
| GOC | #14 Chemistry, 166 Qs, 0.96/paper | **#1 Chemistry, 43 avg, 2–3/shift** | DeepSeek is wrong for study purposes here; the gap is text-extraction blindness, not a real decline. |
| Definite Integration | #3 Maths, 360 Qs | #5 Maths, 32 avg | Both high; DeepSeek absorbs indefinite-integral questions into this row. |
| Indefinite Integrals | #21 Maths, **0 Qs** | #20 Maths, 8 avg | DeepSeek's row is unusable; the notation collapse is real. |
| Coordination Compounds | #3 Chemistry, 338 Qs | #2 Chemistry, 42 avg | Both rank it as a top inorganic chapter. |
| Matrices & Determinants | #10 Maths, 187 Qs | #2 Maths, 36 avg | Gemini's lecture-based ranking is closer to the modern paper pattern. |

What both agree on:

1. **Coordinate Geometry is the #1 chapter in the exam.**
2. **Coordination Compounds and Chemical Bonding are top inorganic priorities.**
3. **Current Electricity and Heat & Thermodynamics are core Physics chapters.**
4. **Definite Integration, Vectors/3D and Matrices/Determinants are high-value Mathematics blocks.**

Where they diverge, the cause is usually methodological, not factual: DeepSeek's text classifier over-assigns broad mechanics/calculus terms and cannot see organic schemes; Gemini uses the lecturer's curated modern totals.

---

## 5. Strengths and weaknesses

### DeepSeek

**Strengths**

- Genuinely covers the whole archive (2002–2025) and accounts for every question, including an explicit unclassified/outside-list bucket.
- Fully auditable: every assignment is traceable to a paper, question number, keyword score and source (`keyword`/`llm`).
- Reproducible pipeline with scripts and a verified Markdown backup.
- Strong for historical lookup (“which paper asked this chapter?”), year trends, and practice-paper selection.

**Weaknesses**

- Chemistry is 82.0% classified; 780 questions remain, heavily organic reaction schemes. GOC at #14 is a known false negative.
- Calculus notation is fragmented: Indefinite Integrals = 0, Differentiation = 19. These rows should not be used for study priority.
- Raw totals are skewed by old paper patterns; even avg/paper is not year-weighted.
- The classifier was validated on small samples (15 keyword, 12 LLM, 10 late labels), not exhaustively. Some broad-chapter assignments remain approximate.

### Gemini

**Strengths**

- The subject tables align with the current 2024–2026 lecture data and the rationalized syllabus; organic and calculus rankings look sensible for a 2026/2027 aspirant.
- Clear tiering and a practical three-phase study plan.
- Excludes deleted/legacy chapters (polymers, surface chemistry, everyday chemistry, solid state) from the priority tables.
- Readable, subject-organized presentation.

**Weaknesses**

- The “all 173 papers” claim is not true of the generator; only 750 January-2025 questions are classified, and the main tables are hardcoded lecture totals.
- The 750-question appendix has low chapter-level agreement with an independent map (47.7% overall, 34.0% Chemistry) and clear misclassifications.
- No per-question audit for the 173-paper claim; no raw CSV equivalents; no year matrix beyond a narrative.
- Table columns are easy to misread: “2025/2024” are full-year totals, while “3-Year Avg” includes an undisplayed 2026; some prose cites 2026 values not shown in the table.
- The “25/65 rule” and phase mark targets are editorial claims, not outputs of the data shown.

---

## 6. Which should you use, and for what?

1. **For deciding what to study next:** use **Gemini's priority tiers and study plan**, but treat the numbers as “lecture 2024–2026 data,” not “my 173-paper count.”
2. **For checking a chapter's historical frequency or finding practice questions:** use **DeepSeek's `question_chapter_map.csv` and year matrix**.
3. **For organic chemistry:** trust **Gemini/lecture data**, not DeepSeek's GOC/Hydrocarbons/Haloalkanes counts. DeepSeek itself flags this.
4. **For calculus:** trust **Gemini/lecture data** for Definite vs Indefinite differentiation; DeepSeek's Indefinite row is an extraction artifact.
5. **Do not merge the numbers blindly.** The two tables use different units (all-paper totals vs yearly lecture totals) and different chapter definitions. A merged table would be numerically invalid unless normalized to a common “questions per shift” basis.

---

## 7. Assessment of the earlier docs/04 review

`docs/04_DeepSeek_vs_Gemini_Analysis_Evaluation.md` reaches a broadly similar directional conclusion: DeepSeek for historical scale, Gemini for current strategy. Its key factual observations — DeepSeek's GOC undercount, calculus notation gap, old-paper skew, and Gemini's 750-question/teacher-data basis — check out against the current files.

It does, however, describe Gemini as “accurate” on organic distribution without stressing that this accuracy comes from **hardcoded lecture totals**, not from Gemini's own 173-paper classification. It also presents Gemini's 2025 appendix as a stronger empirical asset than the 47.7% agreement warrants. This file is therefore the more conservative reference for provenance and data quality.

---

## 8. Final verdict

- **DeepSeek is the better data-engineering artifact.** It is the only project that actually attempts the requested 173-paper classification, and it exposes its own failures instead of hiding them.
- **Gemini is the better study guide.** Its priorities reflect the current exam pattern and the lecturer's 2024–2026 data, especially for organic chemistry and calculus.
- **Neither is a complete standalone answer.** The honest combined recommendation is:
  - Gemini's tiers for **priority**;
  - DeepSeek's map for **evidence and practice**;
  - lecture weightage (`docs/02_Chapterwise_Weightage_Analysis.md`) as the **tie-breaker** for organic and calculus;
  - never quote Gemini's “173 papers” or DeepSeek's “GOC #14 / Indefinite 0” as exam facts.
