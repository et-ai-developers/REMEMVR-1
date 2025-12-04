# RQ 5.5.1 Pipeline Execution - MINIMUM Settings Complete

**Topic:** First production execution of Type 5.5 Source-Destination RQ with MINIMUM IRT settings (pipeline validation phase)
**Created:** 2025-12-05 (context-manager)
**Status:** Superseded by production execution with correct IRT settings (Session 2025-12-05 09:30)

---

## RQ 5.5.1 Complete Pipeline Execution (MINIMUM Settings) (2025-12-04 22:00)

**Task:** Execute RQ 5.5.1 Pipeline with g_code (Step-by-Step Execution + MEDIUM IRT Settings)

**Context:** First production execution of Type 5.5 Source-Destination RQ. Executed all 8 analysis steps with MINIMUM settings first (pipeline validation), then upgraded to MEDIUM settings for production-quality theta.

**Archived from:** state.md Session (2025-12-04 22:00)
**Original Date:** 2025-12-04 22:00
**Reason:** Task completed, superseded by Session 2025-12-05 09:30 with corrected IRT settings (3+ sessions old)

---

### Complete RQ 5.5.1 Pipeline Execution (MINIMUM Settings)

All 8 steps executed successfully with MINIMUM IRT settings (mc_samples=10, iw_samples=10):

| Step | Description | Status | Output |
|------|-------------|--------|--------|
| **Step 0** | Extract VR data | ✅ SUCCESS | 36 items, 400 composite_IDs, Q-matrix |
| **Step 1** | IRT Pass 1 (all items) | ✅ SUCCESS | 36 item params, 400 theta scores |
| **Step 2** | Purify items (D039) | ✅ SUCCESS | 32 retained, 4 excluded (a<0.4) |
| **Step 3** | IRT Pass 2 (purified) | ✅ SUCCESS | 32 items, 400 theta (5 min) |
| **Step 4** | Merge theta + TSVR | ✅ SUCCESS | 800 rows (2 location types) |
| **Step 5** | LMM model selection | ✅ SUCCESS | **Logarithmic best** (AIC=1830, w=82%) |
| **Step 6** | Post-hoc contrasts | ✅ SUCCESS | D068 dual p-values |
| **Step 7** | Plot data | ✅ SUCCESS | Trajectory data ready |

**Key Code Fixes Applied:**
1. **Step 1:** Fixed `calibrate_irt` return order (df_thetas, df_items not item_params, theta_scores)
2. **Step 3:** Fixed column name extraction from coefficients CSV (not pickled model due to patsy env issues)
3. **Step 3:** Fixed groups definition (pattern-based `{'-U-': source}` not explicit item lists)
4. **Step 4:** Extended TSVR validation range to [0, 360] hours (some participants >7 days)
5. **Step 5:** Added coefficients CSV export (avoids patsy pickle loading issues)
6. **Step 6:** Fixed contrast extraction to use coefficients CSV instead of loading pickled model

### Statistical Results (MINIMUM Settings - Pipeline Validation)

**IRT Calibration:**
- 32 items retained (17 source, 15 destination)
- 4 items purified: TQ_IFR-D-i1, TQ_IFR-D-i4, TQ_IFR-U-i4, TQ_IRE-D-i4 (all a<0.4)
- Loss converged at 19.20

**LMM Model Selection:**
| Model | AIC | Delta | Weight |
|-------|-----|-------|--------|
| **Logarithmic** | 1830.15 | 0.00 | **81.9%** |
| Quadratic | 1834.48 | 4.33 | 9.4% |
| Lin+Log | 1835.05 | 4.90 | 7.1% |
| Quad+Log | 1838.32 | 8.17 | 1.4% |
| Linear | 1841.88 | 11.73 | 0.2% |

**Post-Hoc Contrasts (Decision D068 compliant):**
| Test | Coefficient | z | p (uncorr) | p (Bonf) |
|------|-------------|---|------------|----------|
| LocationType main effect | 0.108 | 1.29 | 0.196 | 0.392 |
| LocationType × Time | -0.119 | -1.85 | 0.065 | 0.130 |

**Interpretation (PRELIMINARY - awaiting MEDIUM settings):**
- **No significant main effect** of LocationType (p=0.196)
- **Marginal interaction** (p=0.065 uncorrected) - possible different forgetting rates
- Effect sizes small (Cohen's d < 0.2 at all timepoints)
- Logarithmic decay best fits both source and destination trajectories

### MEDIUM Settings Upgrade (In Progress at Session End)

Updated Step 3 IRT configuration:
- `mc_samples=100` (was 10)
- `iw_samples=100` (was 10)
- Expected runtime: ~45-60 minutes (vs ~5 min with MINIMUM)

**Status at /save:** IRT Pass 2 with MEDIUM settings running in background (Bash ID: 1f2be8)
- Started at ~05:02 UTC
- Currently at epoch ~1500, loss stable at 19.20
- Estimated completion: ~40-50 minutes remaining

**NOTE:** This MEDIUM settings run was later discovered to have WRONG mc_samples configuration (100/100 instead of 1/100), causing 100× slowdown. See `irt_mc_samples_pattern_discovery.md` for root cause and fix.

### Output Files Generated

All files in `results/ch5/5.5.1/`:

**code/** (8 Python scripts):
- step00_extract_vr_data.py
- step01_irt_calibration_pass1.py
- step02_purify_items.py
- step03_irt_calibration_pass2.py (updated to MEDIUM settings - WRONG config)
- step04_merge_theta_tsvr.py
- step05_fit_lmm.py
- step06_compute_post_hoc_contrasts.py
- step07_prepare_plot_data.py

**data/** (17 CSV files):
- step00_irt_input.csv, step00_q_matrix.csv, step00_tsvr_mapping.csv
- step01_pass1_item_params.csv, step01_pass1_theta.csv
- step02_purified_items.csv, step02_purification_report.txt
- step03_item_parameters.csv, step03_theta_scores.csv, step03_pass2_diagnostics.txt
- step04_lmm_input.csv
- step05_model_comparison.csv, step05_lmm_coefficients.csv, step05_lmm_random_effects.csv, step05_lmm_summary.txt, step05_lmm_fitted_model.pkl
- step06_post_hoc_contrasts.csv, step06_effect_sizes.csv
- step07_individual_trajectories.csv, step07_predicted_trajectories.csv, step07_summary_by_timebin.csv

### Session Metrics

**Chapter 5 Progress:**
- RQ 5.5.1: Pipeline executed with MINIMUM settings (8/8 steps SUCCESS)
- MEDIUM settings run in progress (~40 min remaining)
- Type 5.5: 1/7 RQs in execution (5.5.1)

**Files Modified:**
- results/ch5/5.5.1/code/*.py (8 files created)
- results/ch5/5.5.1/data/*.csv (17+ files created)
- results/ch5/5.5.1/logs/*.log (8 files created)

**Tokens:**
- Session start: ~7k (after /refresh)
- Session end: ~140k (at /save)

**Background Process:**
- Bash ID: 1f2be8
- Command: poetry run python -u results/ch5/5.5.1/code/step03_irt_calibration_pass2.py
- Status: Running (IRT MEDIUM settings - WRONG config)
- Action needed after /clear+/refresh: Check BashOutput 1f2be8 for completion, then re-run Steps 4-7

### Lessons Learned

1. **MINIMUM settings pipeline validation:** Validates code correctness before investing hours in MEDIUM settings
2. **Incremental execution approach:** Fixed 6 bugs during MINIMUM run (would have blocked MEDIUM run)
3. **Patsy pickle limitation:** Statsmodels/patsy creates unpicklable models, CSV export workaround required
4. **TSVR range extension:** Some participants tested >7 days (168 hours), need [0, 360] range
5. **Code fixes prevent propagation:** Fixing bugs in first RQ (5.5.1) prevents errors in 5.5.2-5.5.7

### Status at Session End

⏳ **RQ 5.5.1 MINIMUM COMPLETE, MEDIUM IN PROGRESS**

All 8 analysis steps executed successfully with MINIMUM IRT settings. Logarithmic model selected (AIC=1830, w=82%). No significant LocationType main effect (p=0.20), marginal interaction (p=0.065). MEDIUM settings IRT running in background (~40 min remaining). After completion, re-run Steps 4-7 for production-quality results.

**SUPERSEDED:** This session's MEDIUM settings run used WRONG IRT configuration (mc_samples=100 for model_fit instead of 1), causing 100× slowdown. Fixed in Session 2025-12-05 09:30.

---
