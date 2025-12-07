# rq_6.4.1_step00_complete_paradigm_extraction

**Topic Description:** RQ 6.4.1 Step 00 data extraction - 72 TC items (24 per paradigm: IFR/ICR/IRE), 3-factor Q-matrix, n_cats=5 detection, adaptive implementation

**Related Topics:**
- `rq_6.4.1_step01_five_systematic_bug_fixes` (Session 2025-12-07 19:45)
- `ch6_dfdata_wide_format_paradigm_parsing` (archived earlier)
- `ch6_grm_irt_pattern_mc_samples_1_100` (archived earlier)

---

## RQ 6.4.1 Step 00 - Data Extraction Complete (2025-12-07 19:45)

**Archived from:** state.md Session (2025-12-07 19:45)
**Original Date:** 2025-12-07 19:45
**Reason:** Step 00 fully complete, subsequent steps have moved forward

### Generated Code and Outputs

**Generated code:** step00_extract_confidence_data.py (435 lines)
**Execution time:** <10 seconds

**Outputs created:**
- `data/step00_irt_input.csv` (400 rows × 73 cols: composite_ID + 72 TC_* items)
- `data/step00_tsvr_mapping.csv` (400 rows × 4 cols: UID, test, TSVR, composite_ID)
- `data/step00_q_matrix.csv` (72 rows × 4 cols: 3-factor structure IFR/ICR/IRE)

### Key Findings

**Item Detection:**
- n_cats = 5 detected (values: {0.2, 0.4, 0.6, 0.8, 1.0} - no 0.0 values after filtering)
- 72 items extracted (24 per paradigm: IFR=24, ICR=24, IRE=24)
- TSVR range: 1.0-246.24 hours (some sessions >1 week - acceptable real data)

**Technical Implementation:**
- g_code included adaptive n_cats detection per user clarification
- Q-matrix format: 3-factor structure (IFR/ICR/IRE paradigms)
- Paradigm-based 3-factor GRM (vs domain-based in RQ 6.3.1)

### Validation Results

**Status:** All checks passed except TSVR range warning (expected)

**TSVR Range Warning:** Some participants tested after 1 week (>168 hours). This is acceptable - represents real scheduling variations in longitudinal data collection.

### Context

**RQ 6.4.1 Purpose:** Test whether Free Recall, Cued Recall, and Recognition paradigms show different confidence decline patterns. Primary hypothesis is NULL (paradigm affects baseline, not slopes - paralleling Ch5 5.3.1-5.3.2 accuracy findings).

**Statistical Structure:** Paradigm-based 3-factor GRM (identical structure to RQ 6.3.1 domain-based 3-factor GRM, only factor names differ)

---
