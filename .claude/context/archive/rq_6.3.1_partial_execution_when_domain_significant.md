# RQ 6.3.1 Partial Execution - When Domain Significant

Archive of RQ 6.3.1 execution history (Steps 00-05 from Session 2025-12-07 11:00).

---

## RQ 6.3.1 Steps 00-05 Complete (2025-12-07 11:00)

**Task:** RQ 6.3.1 Execution - Domain Confidence Trajectories (3-Factor GRM)

**Context:** Executing second ROOT RQ for Chapter 6. RQ 6.3.1 tests whether What/Where/When episodic memory domains show different confidence decline patterns. Primary hypothesis is NULL (based on Ch5 5.2.1 accuracy findings showing unitized VR encoding).

**Major Accomplishments:**

### 1. RQ 6.3.1 Partial Execution (Steps 00-05 Complete)

**Step 00 - Extract Confidence Data:**
- Extracted 72 TC_* items across 3 domains
- What: 18 items, Where: 36 items, When: 18 items
- Created: step00_irt_input.csv (400 × 73), step00_tsvr_mapping.csv, step00_q_matrix.csv

**Step 01 - IRT Calibration Pass 1 (3-Factor GRM):**
- MINIMUM settings for code validation: mc_samples=1, iw_samples=1
- Fixed multiple issues:
  - Long format column mapping (UID/test/item_name/score required)
  - Return value unpacking order from prepare_irt_input_from_long
  - Validation column names (Overall_Discrimination/Difficulty, not a/b)
- Discrimination: 2.07 - 5.82, Difficulty: -0.01 - 1.12, Theta: -2.34 - 0.63
- Generated: step01_pass1_item_params.csv (72 items), step01_pass1_theta.csv (400 rows)

**Step 02 - Item Purification (Decision D039):**
- All 72 items RETAINED (100%) - all meet a≥0.4, |b|≤3.0
- Generated: step02_purified_items.csv, step02_excluded_items.csv (0 items)

**Step 03 - IRT Calibration Pass 2:**
- Same as Pass 1 (100% retention → mathematically equivalent)
- Generated: step03_pass2_item_params.csv, step03_pass2_theta.csv

**Step 04 - Merge Theta with TSVR:**
- Created 1200 rows (400 sessions × 3 domains)
- TSVR range: 1.0 - 246.2 hours (some sessions > 1 week)
- Theta means: What=-0.75, When=-0.76, Where=-0.79 (very similar)
- Generated: step04_lmm_input.csv (1200 × 7 cols)

**Step 05 - Fit LMM with Domain × Time Interaction:**
- Formula: theta ~ C(domain) * log_TSVR + (1 | UID)
- **UNEXPECTED RESULT:** When domain interaction SIGNIFICANT (p=0.020)
  - C(domain)[T.When]:log_TSVR: coef=-0.0253, p=0.0202 *
  - C(domain)[T.Where]:log_TSVR: coef=-0.0012, p=0.9159 (NULL)
- AIC=506.19, BIC=546.91, converged=True
- Generated: step05_lmm_coefficients.csv, step05_lmm_summary.txt

### 2. Key Finding

**Primary hypothesis PARTIALLY REFUTED:**
- When domain shows significantly steeper confidence decline than What domain
- Where domain shows equivalent decline (NULL as expected)
- Effect size small (coef=-0.025) but statistically significant

**Interpretation:** "When" (temporal context) confidence may be more vulnerable to forgetting than object/location confidence. Contrasts with Ch5 accuracy findings where all domains showed equivalent forgetting.

### 3. Technical Fixes Applied

**Critical fixes added to execute.md:**
1. **IRT Background Process Management:** Don't poll epoch status repeatedly (blows up context)
2. **Flush pattern for log():** f.flush() + print(flush=True) for real-time visibility
3. **MINIMUM settings for validation:** mc_samples=1, iw_samples=1 for code testing

**Tool interface issues identified:**
- fit_lmm_trajectory_tsvr tool has column name expectations that differ from prepared data
- Used statsmodels directly instead of tool (data already prepared in Step 04)

### 4. Current Status

**Completed:** Steps 00-05
**Pending:** Steps 06-07 (post-hoc contrasts if needed, trajectory plot data)

**Archived from:** state.md Session 2025-12-07 11:00
**Original Date:** 2025-12-07 11:00
**Reason:** Session 3+ old (content superseded by complete execution in Session 2025-12-07 13:50)

**Superseded by:** Session 2025-12-07 13:50 completed Steps 06-07, archived to `rq_6.3.1_complete_execution_when_domain_steeper_decline.md`

---
