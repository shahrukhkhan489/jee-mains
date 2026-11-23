# 02 - Historical Evidence from 173 Papers

**Primary use:** historical lookup and audit. **Do not use this table alone for study priority** — Chemistry organic and Mathematics calculus are systematically undercounted by the PDF text layer.

## Coverage

| Subject | Questions | Classified | LLM recovered | Unclassified | Outside list | Coverage |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Physics | 5,275 | 5,241 | 160 | 34 | 0 | 99.4% |
| Chemistry | 5,275 | 4,328 | 311 | 780 | 167 | 82.0% |
| Mathematics | 5,275 | 4,868 | 331 | 407 | 0 | 92.3% |
| **Total** | **15,825** | **14,437** | **802** | **1,221** | **167** | **91.2%** |

## Historical top 15 by DeepSeek avg/paper

| # | Subject | Chapter | DS Qs | DS Avg/paper | Warning |
| ---: | :--- | :--- | ---: | ---: | :--- |
| 1 | Mathematics | Coordinate Geometry (Lines, Circles, Conics) | 869 | 5.02 | — |
| 2 | Physics | Current Electricity | 519 | 3.00 | DS all-era count inflated by old papers |
| 3 | Physics | Kinematics (1D, 2D, Circular) | 497 | 2.87 | DS all-era count inflated by old papers |
| 4 | Mathematics | Sets, Relations & Functions | 489 | 2.83 | DS includes ~38 reasoning-type labels |
| 5 | Physics | Heat and Thermodynamics | 463 | 2.68 | — |
| 6 | Physics | Magnetic Effects of Current | 362 | 2.09 | — |
| 7 | Chemistry | Chemical Bonding & Molecular Structure | 361 | 2.09 | — |
| 8 | Mathematics | Definite Integration | 360 | 2.08 | — |
| 9 | Chemistry | Some Basic Concepts of Chemistry (Mole) | 341 | 1.97 | — |
| 10 | Chemistry | Coordination Compounds | 338 | 1.95 | — |
| 11 | Chemistry | Thermodynamics | 331 | 1.91 | — |
| 12 | Mathematics | Applications of Derivatives (AOD) | 327 | 1.89 | — |
| 13 | Mathematics | Trigonometric Ratios and Identities | 325 | 1.88 | — |
| 14 | Physics | Laws of Motion (NLM) | 307 | 1.77 | — |
| 15 | Physics | Work, Power & Energy | 305 | 1.76 | — |

## Year-wise totals

| Year | Papers | Questions | Classified | Unclassified | Outside list |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2002 | 1 | 225 | 204 | 19 | 2 |
| 2003 | 1 | 225 | 212 | 12 | 1 |
| 2004 | 1 | 225 | 213 | 12 | 0 |
| 2005 | 1 | 225 | 210 | 14 | 1 |
| 2006 | 1 | 150 | 134 | 15 | 1 |
| 2007 | 1 | 120 | 114 | 6 | 0 |
| 2008 | 1 | 105 | 102 | 2 | 1 |
| 2009 | 1 | 90 | 87 | 2 | 1 |
| 2010 | 1 | 90 | 87 | 2 | 1 |
| 2011 | 1 | 90 | 87 | 3 | 0 |
| 2012 | 5 | 450 | 421 | 24 | 5 |
| 2013 | 5 | 450 | 422 | 23 | 5 |
| 2014 | 5 | 450 | 420 | 23 | 7 |
| 2015 | 3 | 270 | 242 | 21 | 7 |
| 2016 | 3 | 270 | 247 | 18 | 5 |
| 2017 | 3 | 270 | 237 | 29 | 4 |
| 2018 | 5 | 450 | 410 | 34 | 6 |
| 2019 | 16 | 1,440 | 1,279 | 144 | 17 |
| 2020 | 16 | 1,200 | 1,093 | 94 | 13 |
| 2021 | 26 | 2,340 | 2,118 | 192 | 30 |
| 2022 | 22 | 1,980 | 1,771 | 179 | 30 |
| 2023 | 24 | 2,160 | 1,941 | 190 | 29 |
| 2024 | 20 | 1,800 | 1,686 | 113 | 1 |
| 2025 | 10 | 750 | 700 | 50 | 0 |

## Known limitations

- **Organic chemistry:** 780 Chemistry questions remain unclassified, mostly image-based reaction schemes. GOC is #14 in DeepSeek (166) but #1 in the lecture data. Use lecture priority.
- **Calculus notation:** Indefinite Integrals = 0; Differentiation = 19. Bare `∫` questions were assigned to Definite Integration. These rows are not usable for priority.
- **Old-paper skew:** 2002-2005 have 225 questions; 2006: 150; 2007: 120; 2008: 105; most others 75/90. Raw totals over-weight old mechanics/classical chapters.
- **Outside list:** 167 old-syllabus/legacy questions were kept separate rather than forced into current chapters (Polymers 53, Surface 35, Everyday 34, Hydrogen/s-block 24, Environmental 17, Solid State 4).
- **Sets:** 38 strict reasoning-type questions (negation/contrapositive) are included in Sets; removing them would leave Sets at 451, still #2.

**Audit file:** `data/question_chapter_map.csv` contains all 15,825 rows with paper, question number, subject, chapter, score, margin and `chapter_source`.
