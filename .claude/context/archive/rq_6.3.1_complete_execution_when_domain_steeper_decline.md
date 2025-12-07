# RQ 6.3.1 Complete Execution - When Domain Steeper Decline

Archive of RQ 6.3.1 complete execution history (Steps 06-07 from Session 2025-12-07 13:50, completing the RQ).

---

## RQ 6.3.1 Steps 06-07 Complete - Post-Hoc Contrasts and Trajectory Plots (2025-12-07 13:50)

**Task:** RQ 6.3.1 Completion - Steps 06-07 (Post-hoc Contrasts + Trajectory Plots)

**Context:** Finishing RQ 6.3.1 according to execute.md protocol. Steps 00-05 complete from previous session (2025-12-07 11:00). Interaction significant (When:log_TSVR p=0.020), so post-hoc contrasts required per plan.

**Archived from:** state.md Session 2025-12-07 13:50
**Original Date:** 2025-12-07 13:50
**Reason:** Task completed, RQ 6.3.1 now fully complete (all 8 steps), superseded by RQ 6.4.1 execution (Session 2025-12-07 22:00)

---

### 1. Step 06 - Post-Hoc Contrasts (Decision D068)

**Initial attempt failed:**
- g_code generated code that called `tools.analysis_lmm.compute_contrasts_pairwise()`
- Tool had internal bug: expected 'sig_uncorrected' column that doesn't exist
- Tool bypassed - wrote direct implementation using statsmodels

**Fixed implementation:**
- Checked interaction significance from Step 05 (p=0.020 < 0.05 → compute contrasts)
- Re-fitted LMM model: theta ~ C(domain) * log_TSVR + (~log_TSVR | UID)
- Computed 3 pairwise slope contrasts:
  1. **When vs What:** estimate=-0.0253, se=0.0093, z=-2.724
     - p(uncorrected)=0.0064, p(Bonferroni)=0.019 * (SIGNIFICANT)
     - Cohen's d=-0.116
  2. **Where vs What:** estimate=-0.0012, se=0.0093, z=-0.124
     - p(uncorrected)=0.901, p(Bonferroni)=1.000 ns (non-significant)
     - Cohen's d=-0.005
  3. **When vs Where:** estimate=-0.0242, se=0.0093, z=-2.601
     - p(uncorrected)=0.0093, p(Bonferroni)=0.028 * (SIGNIFICANT)
     - Cohen's d=-0.111
- Dual p-value reporting per Decision D068 (uncorrected + Bonferroni)
- Generated: step06_post_hoc_contrasts.csv (3 rows), step06_contrast_decision.txt

**Key Findings:**
- When domain has significantly steeper decline than both What (p=0.019) and Where (p=0.028)
- Where and What are equivalent (p=1.000)
- Effect sizes small but meaningful (d ~ -0.11)

---

### 2. Step 07 - Trajectory Plot Data (Decision D069)

**Initial attempt failed:**
- g_code grouped by domain × TSVR_hours (exact values per participant)
- Created 885 rows instead of 12 (3 domains × 4 tests)
- Each participant has slightly different TSVR timing

**Fixed implementation:**
- Changed grouping from `['domain', 'TSVR_hours']` to `['domain', 'test']`
- Compute mean TSVR_hours per test as "time" coordinate
- Aggregated to 12 rows (3 domains × 4 timepoints)
- Created dual-scale outputs per Decision D069:
  1. **Theta-scale:** Raw theta values [-1.04, -0.39]
  2. **Probability-scale:** IRT transformation [0.016, 0.205]
- Used domain-specific mean discrimination for probability transformation:
  - What: a=3.79 (18 items)
  - Where: a=3.96 (36 items)
  - When: a=3.52 (18 items)
- All validation checks passed (12 rows, no NaN, CI bounds valid)
- Generated: step07_trajectory_theta_data.csv, step07_trajectory_probability_data.csv

---

### 3. Technical Fixes Applied

**g_code aggregation bug pattern identified:**
- g_code sometimes misidentifies grouping variables
- TSVR_hours varies per participant → must group by test, then compute mean time
- Fixed by editing generated code: group by 'test' not 'TSVR_hours'
- Similar pattern may occur in other trajectory RQs

**Tool bypass pattern confirmed:**
- Some tools have internal bugs or interface mismatches
- Direct statsmodels implementation often cleaner for LMM post-hoc
- Document tool issues but don't block on fixing them

---

### 4. RQ 6.3.1 Complete - Scientific Summary

**Primary Hypothesis:** NULL (all domains equivalent due to unitized VR encoding)

**Result:** PARTIALLY REFUTED

**Findings:**
1. **When domain:** Significantly steeper confidence decline (p<0.05 both contrasts)
2. **Where domain:** Equivalent to What (NULL as expected)
3. **What domain:** Reference level

**Interpretation:**
- Temporal memory confidence is more vulnerable to forgetting than object/location confidence
- Contrasts with Ch5 accuracy findings where all domains showed equivalent decline
- Suggests **dissociation between confidence and accuracy** for temporal information
- Confidence for "When" decays faster than actual memory accuracy suggests

**Thesis Implications:**
- Metacognitive monitoring may be less accurate for temporal context
- Participants are more uncertain about "When" than performance warrants
- Could reflect different neural substrates for temporal vs spatial/object memory confidence

---

### 5. Files Created

**Step 06 (Post-hoc contrasts):**
- results/ch6/6.3.1/code/step06_compute_post_hoc_contrasts.py (367 lines, direct implementation)
- results/ch6/6.3.1/data/step06_post_hoc_contrasts.csv (3 contrasts)
- results/ch6/6.3.1/data/step06_contrast_decision.txt (decision documentation)
- results/ch6/6.3.1/logs/step06_compute_post_hoc_contrasts.log

**Step 07 (Trajectory plot data):**
- results/ch6/6.3.1/code/step07_prepare_trajectory_plot_data.py (fixed grouping bug)
- results/ch6/6.3.1/data/step07_trajectory_theta_data.csv (12 rows, theta-scale)
- results/ch6/6.3.1/data/step07_trajectory_probability_data.csv (12 rows, probability-scale)
- results/ch6/6.3.1/logs/step07_prepare_trajectory_plot_data.log

**Updated tracking:**
- results/ch6/rq_status.tsv (RQ 6.3.1: code=TRUE)

---

### 6. Session Metrics

**Execution Time:** ~30 min (including 2 g_code invocations + debugging)
**g_code Invocations:** 2 (Step 06, Step 07)
**Code Fixes Applied:** 2 (tool bypass, aggregation bug)
**Steps Completed:** 2 (06, 07)
**Total RQ 6.3.1 Steps:** 8/8 (100% - COMPLETE)

**Tokens:**
- Session start: ~7k (after /refresh)
- Session end: ~67k (at /save)

---

### 7. Related Topics

**Session Active Topics (documented at end of Session 2025-12-07 13:50):**

- rq_6.3.1_complete_execution_when_domain_steeper_decline
- ch6_g_code_aggregation_bug_pattern
- ch6_post_hoc_contrasts_tool_bypass
- ch6_dual_scale_plots_decision_d069

**Relevant Archived Topics (referenced in session):**
- rq_6.3.1_partial_execution_when_domain_significant (Steps 00-05 from Session 2025-12-07 11:00)
- rq_6.1.1_complete_execution_logarithmic_best (ROOT RQ pattern)
- ch6_execute_md_protocol (execution workflow)

---

### 8. Cross-RQ Patterns for Future Reference

**Pattern #1: g_code Aggregation Bug (Trajectory Plots)**
- **Problem:** g_code groups by continuous TSVR_hours instead of discrete test
- **Symptom:** Hundreds of rows instead of expected dozen (factors × 4 tests)
- **Fix:** Change groupby from `['factor', 'TSVR_hours']` to `['factor', 'test']`, compute mean TSVR_hours per test
- **Recurrence:** May occur in RQ 6.4.1, 6.5.1, 6.6.1, 6.7.2, 6.8.1 (all trajectory RQs)

**Pattern #2: Tool Bypass for LMM Post-Hoc**
- **Problem:** compute_contrasts_pairwise tool has internal bugs (expects non-existent columns)
- **Solution:** Direct statsmodels implementation cleaner and more reliable
- **Decision:** Don't block on tool fixes, bypass when necessary

**Pattern #3: Dual-Scale Plots (Decision D069)**
- **Requirement:** All trajectory plots need theta-scale AND probability-scale versions
- **Transformation:** Use factor-specific mean discrimination (a) for IRT transformation
- **Implementation:** Separate CSVs for theta and probability scales
- **Validation:** Check CI bounds, no NaN, correct number of rows

---

**Status:** ✅ **RQ 6.3.1 COMPLETE - When Domain Steeper Decline (p<0.05)**

All 8 steps complete (00-07). When domain shows significantly steeper confidence decline than both What and Where domains (Bonferroni-corrected p<0.05). Primary NULL hypothesis partially refuted. Scientific finding: Confidence-accuracy dissociation for temporal memory. Dual-scale trajectory data generated per Decision D069. rq_status.tsv updated.

**Next:** Execute remaining ROOT RQs: 6.4.1, 6.5.1, 6.6.1, 6.7.2, 6.8.1. Watch for g_code aggregation bug pattern in other trajectory RQs.

---
