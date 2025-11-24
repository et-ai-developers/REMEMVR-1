# Pipeline Stability

**Topic:** v4.X pipeline stability, production RQ execution, infrastructure enhancements
**Created:** 2025-11-24 12:30 (context-manager curation)

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
