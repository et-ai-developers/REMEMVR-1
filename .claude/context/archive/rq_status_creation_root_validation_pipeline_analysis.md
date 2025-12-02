# rq_status_creation_root_validation_pipeline_analysis

**Topic:** RQ Status Tracking + Root RQ Validation + Pipeline Analysis
**Created:** 2025-12-02 16:30
**Last Updated:** 2025-12-02 17:45 (context-manager curation)

---

## Root RQ Pipeline Analysis + rq_status.tsv Creation + Data Source Update (2025-12-02 16:30)

**Context:** User requested analysis of unique analysis pipelines across 4 types (General, Domains, Paradigms, Congruence), then validation of root RQ summaries, then creation of accurate rq_status.tsv tracking file. Also updated step00 code to use local step00_input_data.csv instead of dfData.csv.

**Archived from:** state.md Session (2025-12-02 16:30)
**Original Date:** 2025-12-02 16:30
**Reason:** 3+ sessions old, comprehensive archival of completed analysis work

---

### Major Accomplishments

**1. Identified 8 Unique Analysis Pipeline Types**

Analyzed rq_refactor.tsv to find shared pipeline patterns:

| Pipeline | Subtype | RQs | Template Source |
|----------|---------|-----|-----------------|
| Functional Form Comparison | Root IRT + 5 LMM model selection | 5.1.1, 5.2.1, 5.3.1, 5.4.1 | 5.2.1 |
| Two-Phase/Consolidation Window | Piecewise LMM (Early/Late) | 5.1.2, 5.2.2, 5.3.3, 5.4.2 | 5.1.2 |
| Age × Factor Interactions | 3-way interaction LMM | 5.1.3, 5.2.3, 5.3.4, 5.4.3 | 5.1.3 |
| Variance Decomposition | ICC extraction | 5.1.4, 5.2.6, 5.3.7, 5.4.6 | 5.1.4 |
| Individual Clustering | K-means on random effects | 5.1.5, 5.2.7, 5.3.8, 5.4.7 | 5.1.5 (NOT STARTED) |
| Item Difficulty Interaction | Cross-classified LMM | 5.1.6, 5.2.8, 5.3.9, 5.4.8 | 5.1.6 (NOT STARTED) |
| IRT-CTT Convergence | Parallel LMMs + correlation | 5.2.4, 5.3.5, 5.4.4 | 5.2.4 |
| Purified CTT Effects | Steiger's z-test + AIC | 5.2.5, 5.3.6, 5.4.5 | 5.2.5 |
| Retrieval Support Gradient | Linear trend contrast | 5.3.2 | Unique to Paradigms |

**Critical Insight:** 5.3.2 is correctly UNIQUE to Paradigms (ordered Free > Cued > Recognition gradient only makes sense with ordered paradigm levels). IRT-CTT and Purified CTT correctly absent from General type (multi-factor structure required for meaningful validation).

---

**2. Updated Step00 Code for All 4 Root RQs**

Changed INPUT_FILE from `PROJECT_ROOT / "data" / "cache" / "dfData.csv"` to `RQ_DIR / "data" / "step00_input_data.csv"` for data isolation:

**Files Modified:**
- `results/ch5/5.1.1/code/step00_extract_data.py`
- `results/ch5/5.2.1/code/step00_extract_vr_data.py`
- `results/ch5/5.3.1/code/step00_prepare_paradigm_data.py`
- `results/ch5/5.4.1/code/step00_extract_congruence_data.py`

**Changes per file:**
- INPUT_FILE path updated
- Docstring EXPECTED INPUTS updated
- Log messages updated to reference step00_input_data.csv

---

**3. Comprehensive Root RQ Validity Analysis**

Used context_finder to analyze all 4 root RQ summary.md files. Created detailed validity report:

| RQ | Type | Overall Validity | Critical Issues |
|----|------|------------------|-----------------|
| **5.1.1** | General | HIGH | Log model 48% weight (moderate, not overwhelming) |
| **5.2.1** | Domains | **MODERATE** | **CRITICAL: When domain floor effect (6-9% accuracy)** |
| **5.3.1** | Paradigms | MODERATE-HIGH | Recognition faster forgetting (contradicts hypothesis) |
| **5.4.1** | Congruence | MODERATE-HIGH | NULL schema effects (valid finding, not validity threat) |

**CRITICAL FINDING - When Domain Invalid:**
- When domain: 6-9% accuracy (essentially chance for temporal ordering)
- Only 6 items retained after purification (77% loss vs 35% for What/Where)
- Theta trajectory appears "stable" but is floor artifact
- **ALL 5.2.X downstream RQs must use What/Where ONLY**

---

**4. Created Accurate rq_status.tsv**

Created `results/ch5/rq_status.tsv` with accurate file existence checks via Python script. Initial version had errors (5.1.5, 5.1.6 marked TRUE when folders were empty).

**Final Accurate Status:**

| Status | Count | RQs |
|--------|-------|-----|
| COMPLETE (all TRUE) | 13 | 5.1.1-5.1.4, 5.2.1-5.2.5, 5.3.1-5.3.2, 5.4.1-5.4.2 |
| Partial (concept/scholar/stats only) | 16 | 5.2.6-5.2.8, 5.3.3-5.3.9, 5.4.3-5.4.8 |
| NOT STARTED | 2 | 5.1.5, 5.1.6 |

**Key Notes in rq_status.tsv:**
- 5.1.5, 5.1.6: "NOT STARTED. Depends on 5.1.4 random effects."
- 5.2.X (all downstream): "USE WHAT/WHERE ONLY (When floor effect)"
- 5.2.6, 5.2.7: "4 clustering vars not 6" (due to When exclusion)
- 5.3.1: "Recognition faster forgetting - investigate"
- 5.4.X: "NULL schema effects expected (per 5.4.1)"

**Files Created:**
- `results/ch5/rq_status.tsv` (32 rows - accurate tracking with notes)

**Files Modified:**
- 4 × step00 code files (INPUT_FILE path + docstrings + log messages)

---

### Session Metrics

**Token Usage:**
- Session start: ~10k tokens (after /refresh)
- Session end: ~85k tokens (estimate)
- Delta: ~75k tokens consumed
- Remaining: ~115k (57% available)

---

### Key Insights

**Pipeline Template Strategy:**
- 8 reusable pipeline templates cover 30 of 31 RQs
- Only 5.3.2 (Retrieval Support Gradient) is unique
- Write code once per template, copy with variable changes

**Data Isolation Benefits:**
- Each root RQ now has step00_input_data.csv in its own data folder
- No cross-type dependencies on dfData.csv
- Easier rerun and debugging

**When Domain Discovery:**
- Floor effect confirmed by both RQ 5.2.1 summary AND 27/37 temporal item exclusions in RQ 5.1.1
- Downstream RQs must reduce from 3 domains to 2 (What/Where)
- 5.2.6/5.2.7 clustering: 4 variables not 6

---

### Related Topics

From context-finder (2025-12-02 16:30):
- cross_type_dependency_resolution_step0_creation_documentation_update.md (2025-12-01 14:00: root RQ independence, dfData.csv extraction)
- rq_refactor_tsv_extended_6_columns_comprehensive_specification_database.md (2025-12-01 02:30: 31 RQs × 11 columns)
- when_domain_anomalies.md (2025-11-24: When domain 6-9% floor, 77% item exclusion)

---

**End of Session (2025-12-02 16:30)**

**Status:** ✅ **rq_status.tsv CREATED + ROOT RQs VALIDATED** - Identified 8 reusable pipeline templates (30 of 31 RQs). Updated all 4 root RQ step00 scripts to use local step00_input_data.csv. Validated all root RQ summaries with context_finder - discovered When domain floor effect (6-9%) invalidates 5.2.X downstream RQs unless What/Where only. Created accurate rq_status.tsv with notes column for critical guidance. 5.1.5 and 5.1.6 are NOT STARTED (empty folders). **Next:** Create concept files for 5.1.5/5.1.6, then run plan/tools/analysis for 16 partial RQs.
