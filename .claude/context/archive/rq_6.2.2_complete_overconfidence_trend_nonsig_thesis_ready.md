# RQ 6.2.2 Complete - Overconfidence Trend Non-Significant (Thesis-Ready)

## RQ 6.2.2 Execution: Overconfidence Proportion Trend Test (2025-12-11 20:15)

**Research Question:** Does the proportion of overconfident observations increase over time?

**Status:** ✅ THESIS-READY

**Finding:** Overconfidence proportion increases descriptively (+10%, from 41% to 51%), but logistic trend test is NON-SIGNIFICANT (p=0.230).

---

### Analysis Pipeline Overview

**Script:** `results/ch6/6.2.2/code/steps_00_to_05.py`

**Steps Executed:**
- Step 00: Load calibration scores from RQ 6.2.1 (400 rows)
- Step 01: Classify observations: Overconfident (>0.1), Underconfident (<-0.1), Calibrated (±0.1)
- Step 02: Compute proportion overconfident per timepoint with Wilson CIs
- Step 03: Fit logistic regression trend test (overconfident_binary ~ time_ordinal)
- Step 04: Compute mean calibration per timepoint
- Step 05: Prepare dual-axis plot data

**Data Discovery:**
- RQ 6.2.1 output column names differed from 4_analysis.yaml specification
- Actual columns: `UID`, `test`, `composite_ID`, `TSVR_hours`, `z_theta_accuracy`, `z_theta_confidence`, `calibration` (lowercase)
- Code adapted to handle actual column names

---

### Primary Statistical Results

**Classification Distribution (Overall):**
- Overconfident: 187 (46.8%)
- Underconfident: 177 (44.2%)
- Calibrated: 36 (9.0%)

**Proportion Overconfident Trajectory:**

| Test | N_overconf | Proportion | 95% CI |
|------|------------|------------|--------|
| T1 | 41 | 41.0% | [31.9%, 50.8%] |
| T2 | 48 | 48.0% | [38.5%, 57.7%] |
| T3 | 47 | 47.0% | [37.5%, 56.7%] |
| T4 | 51 | 51.0% | [41.3%, 60.6%] |

**Change T1→T4:** +10 percentage points (41% → 51%)

**Trend Test (Logistic Regression):**
- **Slope:** β = 0.053 (log-odds per day)
- **SE:** 0.044
- **z:** 1.201
- **p-value:** 0.230 (NON-SIGNIFICANT at α=0.05)
- **Odds Ratio:** 1.054 [0.967, 1.149]

**Mean Calibration Trajectory:**
- T1: -0.116 (underconfident)
- T4: +0.111 (overconfident)
- Change: +0.227

---

### Theoretical Interpretation - NUANCED FINDING

**Key Result:** Overconfidence trend is NOT SIGNIFICANT (p=0.230)

**Integration with RQ 6.2.1:**
- **RQ 6.2.1:** Calibration MAGNITUDE worsens significantly (p_LRT=0.004)
- **RQ 6.2.2:** Direction shifts toward overconfidence but trend NOT SIGNIFICANT

**Interpretation:**
- Calibration change is GRADUAL shift in DEGREE (continuous)
- NOT a discrete CATEGORY flip (overconfident vs underconfident)
- Miscalibration increases SYMMETRICALLY (both over- and underconfidence)
- The +10% descriptive increase is REAL but not statistically reliable
- Suggests RELATIVELY COUPLED system with INCREASING NOISE

---

### Validation Workflow

**Agents Invoked (4 total, SEQUENTIAL per execute.md lesson):**

| Agent | Status | Key Finding |
|-------|--------|-------------|
| rq_inspect | ✅ PASS | 4-layer validation, all files exist, correct row counts |
| rq_plots | ✅ SUCCESS | 2 plots: overconfidence_trajectory.png, classification_distribution.png |
| rq_results | ✅ COMPLETE | summary.md with nuanced finding documented |
| rq_validate | ✅ PASS WITH NOTES | 0 critical/high, 3 moderate (non-independence, diagnostics, multiple comparisons) |

**Moderate Issues (Documented, Non-Blocking):**
1. Non-independence: 4 obs/participant without mixed-effects logistic (acceptable given p=0.230)
2. Model diagnostics: Hosmer-Lemeshow not run (low impact for simple model)
3. Multiple comparisons: Two metrics tested (acceptable - only proportion has formal p-value)

---

### Files Created

**Code:**
- results/ch6/6.2.2/code/steps_00_to_05.py (NEW - comprehensive analysis pipeline)

**Data (6 files):**
- step00_calibration_loaded.csv (400 rows)
- step01_calibration_classified.csv (400 rows with Classification)
- step02_proportion_overconfident.csv (4 rows)
- step03_trend_test.csv (2 rows: Intercept + time_ordinal)
- step04_mean_calibration.csv (4 rows)
- step05_overconfidence_trajectory_data.csv (4 rows)

**Plots:**
- results/ch6/6.2.2/plots/plots.py (NEW)
- results/ch6/6.2.2/plots/overconfidence_trajectory.png
- results/ch6/6.2.2/plots/classification_distribution.png

**Results:**
- results/ch6/6.2.2/results/summary.md
- results/ch6/6.2.2/results/validation.md

**Status:**
- results/ch6/6.2.2/status.yaml (all 12 agents = success)
- results/ch6/rq_status.tsv (6.2.2 THESIS-READY)

---

### Chapter 6 Progress Impact

**Completed RQs:** 11/31 (35%)
- 6.1.1 (ROOT), 6.1.2, 6.1.3, 6.1.4, 6.1.5, 6.2.1 (ROOT), **6.2.2**, 6.3.1, 6.4.1, 6.5.1, 6.8.1

**Remaining ROOT RQs:** 2 (6.6.1, 6.7.2)

**Ready to Execute (Derivatives):**
- 6.2.5 (Age Effects on Calibration) - depends on 6.2.1 ✅
- 6.7.3 (Calibration Predicts Forgetting) - depends on 6.2.1 ✅
- 6.3.X, 6.4.X, 6.5.X, 6.8.X series (roots complete)

---

**Archived from:** state.md Session (2025-12-11 20:15)
**Original Date:** 2025-12-11 20:15
**Reason:** Session archived (3+ sessions old per context-manager protocol)

---
