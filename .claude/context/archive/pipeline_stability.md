# Pipeline Stability

**Topic:** v4.X pipeline stability, production RQ execution, infrastructure enhancements
**Created:** 2025-11-24 12:30 (context-manager curation)

---

## RQ 5.2 Full Pipeline Execution - 4 Bug Fixes Applied (2025-11-24 10:00)

**Task:** Process RQ 5.2 (Differential Consolidation Across Domains) through complete v4.X pipeline

**Pipeline Execution Summary:**
- All 13 agents executed successfully
- 4 bugs discovered and fixed during execution
- Agent prompts enhanced with project-specific knowledge

**Agent Execution Sequence:**
1. rq_builder: Created folder structure (6 subfolders + status.yaml)
2. rq_concept: Created 1_concept.md (piecewise LMM, 3-way interaction)
3. rq_scholar: 9.5/10 APPROVED (sleep consolidation theory excellent)
4. rq_stats: 9.0/10 CONDITIONAL (fixed Bonferroni alpha: 0.05/6=0.0083)
5. rq_planner: 6 steps planned (data prep + LMM + slopes + contrasts + benefit + plots)
6. rq_tools: 11 tools cataloged (6 analysis + 5 validation)
7. rq_analysis: 4_analysis.yaml created (100% validation coverage)
8. g_code: 6 Python scripts generated and executed
9. rq_inspect: 4-layer validation PASS
10. rq_plots: 2 dual-scale trajectory plots generated
11. rq_results: summary.md created with 2 anomalies flagged

**4 Bugs Fixed (Pipeline Improvements):**

| Bug | Problem | Fix | Documentation Added |
|-----|---------|-----|---------------------|
| Test Value Mapping | Code used 0,1,3,6 (nominal days) instead of 1,2,3,4 (test session numbers) | Updated SEGMENT_MAPPING in step00 | g_code.md: "REMEMVR Data Conventions" section |
| TSVR Validation Too Strict | Validation rejected real data (late=7.71 days > expected 6) | Relaxed validation margins (allow up to 10 days for Late segment) | g_code.md: TSVR validation guidance |
| statsmodels n_groups Attribute | `lmm_result.n_groups` doesn't exist | Use `len(lmm_result.model.group_labels)` instead | g_code.md: statsmodels LMM attributes section |
| statsmodels Model Loading | `pickle.load()` causes patsy/eval errors | Use `MixedLMResults.load(str(path))` instead | g_code.md: statsmodels model loading section |

**rq_analysis Folder Convention Fix:**
- Problem: Intermediate CSV outputs going to `results/` instead of `data/`
- Fix: Added "CRITICAL: Output Folder Conventions" section to rq_analysis.md
- Rule: `data/` for ALL data outputs (.csv, .pkl, .txt); `results/` for ONLY final summary reports

**Agent Prompts Enhanced:**
- `.claude/agents/g_code.md` - Added "REMEMVR Data Conventions" section (~40 lines)
- `.claude/agents/rq_analysis.md` - Added "CRITICAL: Output Folder Conventions" section (~20 lines)

**RQ 5.2 Scientific Results:**
- Model: Piecewise LMM (theta ~ Days_within * Segment * Domain)
- AIC: 3192.05, converged successfully
- Hypothesis Outcome: NOT SUPPORTED (predicted Where benefits most, actual: When showed least forgetting)
- No contrasts significant after Bonferroni correction (alpha=0.0083)
- 2 anomalies flagged: wrong direction effect + Where continued late decay

**Files Created:**
- `results/ch5/rq2/` - Complete RQ folder with all outputs (docs, code, data, plots, results)
- 6 Python scripts (step00-05), 6 data CSVs, 2 trajectory plots, 1 summary.md

**Session Duration:** ~60 minutes
**Token Usage:** ~100k tokens
**Bugs Fixed:** 4 (all documented in agent prompts)
**Pipeline Status:** Fully operational after RQ 5.2

**Archived from:** state.md
**Original Date:** 2025-11-24 10:00
**Reason:** RQ 5.2 complete, bug fixes applied, pipeline stability evidence

---

## D0XX Reference Removal (2025-11-23 03:00)

**Task:** Codebase cleanup - Remove D0XX decision references

**User Request:** "I am sick of these Decision D069, D070, and others permeating everything"
**User Choice:** Option A - Complete removal from entire codebase

**Files Cleaned (~50+ files):**
- Agent Prompts (7): rq_planner, rq_analysis, rq_tools, rq_plots, rq_specification, rq_results, rq_concept
- Templates (7): plan.md, tools.md, analysis.md, results.md, plots.md, stats_report.md, inspect_criteria.md
- Tool Code (3): analysis_irt.py, analysis_lmm.py, plotting.py
- Generated Code (9): step00-step07.py + plots.py
- Generated Docs (6): 1_concept.md, 1_scholar.md, 1_stats.md, 2_plan.md, 3_tools.yaml, 4_analysis.yaml
- Other Docs (15+): tools_catalog.md, tools_inventory.md, names.md, validation_audit.md, todo.yaml, etc.
- Tests (4): test_filter_items_by_quality.py, test_compute_contrasts_pairwise.py, etc.

**Replacement Mapping:**
| Before | After |
|--------|-------|
| Decision D039 | 2-pass IRT purification |
| Decision D068 | dual p-value reporting |
| Decision D069 | dual-scale trajectory plots |
| Decision D070 | TSVR time variable |

**Preserved:** .claude/context/archive/ (historical records), .venv/, .archive/

**Test Status:** 107 pass, 14 fail (pre-existing, D0XX removal caused NO new failures)

**Session Duration:** ~45 minutes | **D0XX References Removed:** ~210+ across 50+ files

**Archived from:** state.md
**Original Date:** 2025-11-23 03:00
**Reason:** Task completed, codebase cleanup orthogonal to current RQ work

---

## Phase 28 - rq_results Agent Testing Complete (2025-11-23 04:00)

**Task:** Test rq_results agent on RQ 5.1 to create publication-ready summary.md

**Bloat Cleanup:**
- Before: 812 lines
- After: 715 lines
- Reduction: 12% (relatively lean agent already)
- Removed: Redundant circuit breaker section (98 lines), replaced with reference to universal.md

**g_conflict Pre-flight:**
- Found: 12 conflicts (4 HIGH, 6 MODERATE, 2 LOW)
- Fixed all HIGH priority:
  - Prior agent count: "10" -> "9" (g_conflict/g_code/g_debug don't write context_dumps)
  - Template line count: Removed stale line counts
  - Circuit breaker naming: STEP_ERROR -> STEP ERROR (space, not underscore)
  - Path format: Split combined file references into separate lines

**Agent Execution Results (PASS):**
- summary.md Created: results/ch5/rq1/results/summary.md (436 lines)
- Quality: Publication-ready
- 5 Required Sections: ALL PRESENT
  1. Statistical Findings (IRT calibration, LMM results, contrasts, effect sizes)
  2. Plot Descriptions (theta scale, probability scale trajectories)
  3. Interpretation (hypothesis testing, dual-scale, domain insights)
  4. Limitations (sample, methodological, technical, generalizability)
  5. Next Steps (immediate, planned RQs, extensions)

**Error Handling Test (PASS):**
Re-ran agent on already-completed RQ -> Correctly returned STEP ERROR with guidance

**Files Modified:**
- `.claude/agents/rq_results.md` - Bloat cleanup + conflict fixes (812->715 lines)
- `docs/v4/templates/results.md` - Fixed "10 prior agents" -> "9 prior RQ-specific agents"
- `results/ch5/rq1/results/summary.md` - Publication-ready summary (436 lines)
- `results/ch5/rq1/status.yaml` - rq_plots + rq_results = success

**Session Duration:** ~30 minutes | **Agent Tested:** rq_results (Phase 28 COMPLETE)

**Archived from:** state.md
**Original Date:** 2025-11-23 04:00
**Reason:** Phase 28 testing completed, rq_results validated

---

## Trajectory Plot Enhancement - Continuous TSVR + Publication Style (2025-11-23 05:00)

**Task:** step07 plot data enhancement - User noticed only 4 time points (aggregated by test session). Requested continuous TSVR data and publication-style plots matching legacy `.archive/v1/plots.py`.

**Step07 Redesign: Aggregated -> Individual-Level Data**
- **Root Cause:** Original step07 aggregated theta scores by domain x test session, collapsing 400 observations per domain into 4 mean points.
- **Solution:** Rewrote step07 to output individual-level data
- **Before:** 12 rows (3 domains x 4 test sessions, aggregated means with CI)
- **After:** 1,200 rows (100 participants x 4 tests x 3 domains, individual observations)

**Column Changes:**
- Before: `[time, test, domain, mean_theta, CI_lower, CI_upper, predicted_theta, n_obs]`
- After: `[TSVR_hours, domain, theta, predicted_theta, UID]`

**Plots.py Rewrite: Publication Style (Matching Legacy)**
User Reference: `.archive/v1/plots.py` with faded scatter points, dashed fitted curves, shaded 95% CI bands from LMM covariance matrix.

**Implementation (3 iterations):**
1. Used `plot_trajectory()` from tools/plotting.py - No scatter, just error bars
2. Custom bootstrap CI - Worked but not matching legacy style
3. Proper LMM-based CI using `patsy.dmatrix` (matching legacy code)

**Final plots.py Features:**
- Re-fits LMM model in plots.py to get covariance matrix
- Uses `patsy.dmatrix()` to create design matrix for CI calculation
- Proper delta method: `pred_var = np.sum((X @ fe_cov) * X, axis=1)`
- 95% CI = mean +/- 1.96 x SE
- Probability scale converts theta CI through logistic function

**Style Constants (matching legacy):**
```python
RESIDUAL_SCATTER_POINT_ALPHA = 0.15
MEAN_CI_ALPHA = 0.2
IRT_LINE_STYLE = 'dashed'
```

**Color Scheme Updated:**
- What: Blue (#3498DB)
- Where: Green (#2ECC71)
- When: Orange (#E67E22)

**Files Modified:**
- `results/ch5/rq1/code/step07_prepare_trajectory_plot_data.py` - Rewritten for individual-level output
- `results/ch5/rq1/plots/plots.py` - Rewritten with LMM-based CI (matching legacy)
- `results/ch5/rq1/plots/step07_trajectory_theta_data.csv` - 1,200 rows (was 12)
- `results/ch5/rq1/plots/step07_trajectory_probability_data.csv` - 1,200 rows (was 12)
- `results/ch5/rq1/plots/trajectory_theta.png` - Publication style with CI bands
- `results/ch5/rq1/plots/trajectory_probability.png` - Publication style with CI bands

**TSVR Data Range:** 1.0 - 246.2 hours (showing real variability in test timing)

**Session Duration:** ~45 minutes | **Plot Style:** Publication-ready with LMM-based CI bands

**Archived from:** state.md
**Original Date:** 2025-11-23 05:00
**Reason:** Infrastructure enhancement completed, plots now publication-ready

---

## RQ 5.4 Full Pipeline Execution - Linear Trend Contrast (2025-11-24 14:15)

**Task:** Process RQ 5.4 (Linear Trend in Forgetting Rate Across Paradigms) through complete v4.X pipeline

**Objective:** Secondary analysis on RQ 5.3 testing linear trend across paradigm-specific forgetting rates

**Key Accomplishments:**

**1. Full RQ 5.4 Pipeline Execution (All 11 Agents)**

**Agent Execution Sequence:**
- rq_builder: Created folder structure (6 subfolders + status.yaml)
- rq_concept: Created 1_concept.md (linear trend contrast, secondary analysis on RQ 5.3)
- rq_scholar: 9.4/10 APPROVED (encoding-retrieval specificity, polynomial contrasts)
- rq_stats: 9.1/10 CONDITIONAL - Required 2 fixes applied:
  - Changed from N=3 regression to within-LMM contrast testing (preserves N=100)
  - Removed R-squared hypothesis (meaningless with 3 data points)
- rq_planner: 4 steps planned (load RQ5.3 + marginal means + linear contrast + plot data)
- rq_tools: 4 analysis + 2 validation tools cataloged (mostly stdlib)
- rq_analysis: 4_analysis.yaml created
- g_code: 4 Python scripts generated and executed - 1 bug fix (coefficient parsing)
- rq_inspect: 4-layer validation PASS
- rq_plots: 1 bar chart generated (paradigm forgetting rates)
- rq_results: summary.md created with 2 anomalies flagged

**2. Bug Fix: Coefficient Parsing**

**Problem:** `log_Days Var` (random effect variance) was being selected instead of `log_Days` (fixed effect slope) due to substring matching in coefficient extraction.

**Fix:** Use exact string matching for coefficient names rather than substring matching.

**3. rq_stats Required Changes Applied**

**Change 1: Within-LMM Contrast Testing**
- Original: Proposed N=3 regression on extracted slopes (only 1 df)
- Fixed: Test linear trend contrast directly within RQ5.3 LMM using marginal means
- Benefit: Preserves full sample information (N=100) and proper degrees of freedom

**Change 2: Remove R-squared Hypothesis**
- Original: "R-squared for linearity of trend will exceed 0.90"
- Fixed: Removed (statistically meaningless with N=3 data points)

**4. RQ 5.4 Scientific Results (SUPERSEDED BY IRT SETTINGS CORRECTION)**

**NOTE:** These results used imprecise IRT settings (20-100x lower than validated "Med" settings). Full rerun required - see Session 2025-11-24 21:30.

**Linear Trend Contrast:**
| Statistic | Value |
|-----------|-------|
| Estimate (b) | -0.127 |
| z-value | -2.47 |
| p (uncorrected) | 0.01 |
| p (Bonferroni) | 0.20 |
| 95% CI | [-0.228, -0.026] |

**Paradigm-Specific Marginal Means (Day 3):**
- Free Recall: -0.470 (slowest forgetting)
- Cued Recall: -0.520
- Recognition: -0.597 (fastest forgetting)

**Hypothesis Outcome: NOT SUPPORTED**
- Predicted: Free > Cued > Recognition (forgetting DECREASES with more retrieval support)
- Observed: Free < Cued < Recognition (forgetting INCREASES with more retrieval support)
- Direction is OPPOSITE to theoretical prediction
- Effect does not survive Bonferroni correction

**2 Anomalies Flagged:**
1. Wrong direction effect (opposite to theory)
2. Non-monotonic marginal means (Recognition > Free > Cued, not strictly monotonic)

**5. Files Created (RQ 5.4)**

**Documentation:**
- `results/ch5/rq4/docs/1_concept.md` - RQ concept (linear trend contrast)
- `results/ch5/rq4/docs/1_scholar.md` - Scholarly validation (9.4/10 APPROVED)
- `results/ch5/rq4/docs/1_stats.md` - Statistical validation (9.1/10 CONDITIONAL)
- `results/ch5/rq4/docs/2_plan.md` - Analysis plan (4 steps)
- `results/ch5/rq4/docs/3_tools.yaml` - Tool specifications
- `results/ch5/rq4/docs/4_analysis.yaml` - Complete analysis recipe

**Code:**
- `results/ch5/rq4/code/step00_load_rq53_outputs.py`
- `results/ch5/rq4/code/step01_extract_marginal_means.py`
- `results/ch5/rq4/code/step02_compute_linear_trend_contrast.py`
- `results/ch5/rq4/code/step03_prepare_paradigm_plot_data.py`

**Data:**
- `results/ch5/rq4/data/step00_model_loaded.txt` - Model load confirmation
- `results/ch5/rq4/data/step01_marginal_means.csv` - 3 rows (paradigms)
- `results/ch5/rq4/data/step02_linear_trend_contrast.csv` - 1 row (contrast results)
- `results/ch5/rq4/data/step02_contrast_interpretation.txt` - Plain-language interpretation

**Plots:**
- `results/ch5/rq4/plots/paradigm_forgetting_rates.png` - Bar chart with trend line
- `results/ch5/rq4/plots/step03_paradigm_forgetting_rates_data.csv` - Plot source data
- `results/ch5/rq4/plots/plots.py` - Plot generation script

**Results:**
- `results/ch5/rq4/results/summary.md` - Publication-ready summary (SUPERSEDED)

**6. plots.py Path Fix**

**Problem:** `ModuleNotFoundError: No module named 'tools'` when running plots.py
**Fix:** Added sys.path.insert to add project root to Python path (5-level parent from plots.py)

---

**Session Duration:** ~45 minutes
**Token Usage:** ~95k tokens
**RQ Processed:** ch5/rq4 (Linear Trend Contrast)
**Bugs Fixed:** 1 (coefficient parsing)
**rq_stats Required Changes:** 2 applied (within-LMM contrast, remove R-sq)
**Hypothesis Outcome:** NOT SUPPORTED (2 anomalies flagged - opposite direction)

**Status:** RQ 5.4 COMPLETE but results SUPERSEDED by IRT settings correction (Session 2025-11-24 21:30). Rerun required after RQ 5.1 and 5.3 complete.

**Archived from:** state.md
**Original Date:** 2025-11-24 14:15
**Reason:** RQ 5.4 pipeline execution history preserved, but scientific results superseded by IRT settings correction requiring full rerun

---
