# Archive — provenance only

These files are preserved so that no source material is lost after consolidating the two analyses into `final_analysis/`.

## deepseek/
- `README.md` — original DeepSeek methodology and coverage.
- `01_chapter_weightage_all_papers.md` — original 173-paper report.
- `scripts/` — original pipeline scripts. Their hardcoded paths refer to the old `deepseek_analysis/` layout; they are archived for audit, not run from here.

## gemini/
- Subject tables, overall table, README, high-yield plan, multi-year trend matrix.
- `2025_Jan_shifts_classified.md` — original 750-question appendix. **Known to disagree with the audited map on 47.7% of chapter labels**; kept only for provenance.
- `generate_gemini_analysis.py` — original generator. The subject tables are hardcoded from the 2024–2026 lecture slides; only the 2025 appendix was independently classified.

## reviews/
- The two prior evaluation documents. Their findings are summarized and corrected in `05_Methodology_and_Provenance.md`.

The canonical data lives in `../data/`; the canonical study tables are `../01`–`../05`.
