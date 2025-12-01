# RQ 5.4.4: IRT-CTT Convergence

**Chapter:** 5
**Type:** Congruence
**Subtype:** IRT-CTT Convergence
**Full ID:** 5.4.4

---

## Research Question

**Primary Question:**
Do IRT theta scores and CTT mean scores yield the same conclusions about congruence-specific forgetting trajectories?

**Scope:**
This RQ examines convergence between two measurement approaches (IRT vs CTT) across three schema congruence categories (Common, Congruent, Incongruent). Sample: N=100 participants x 4 test sessions x 3 congruence levels = 1200 observations. Uses IRT-purified item set from RQ 5.4.1 to compute CTT scores for direct comparison.

**Theoretical Framing:**
Methodological validation to demonstrate that conclusions about schema congruence effects on forgetting are robust to measurement approach. If IRT and CTT converge (high correlations, similar LMM fixed effects), this provides evidence that findings are not measurement-method artifacts but reflect genuine episodic memory phenomena.

---

## Theoretical Background

**Relevant Theories:**
- **Classical Test Theory (CTT):** Assumes true score = observed score - error. Mean scores across items are unbiased estimates of ability. Simple, interpretable, but assumes equal item discrimination and parallel forms.
- **Item Response Theory (IRT):** Models probability of correct response as function of person ability (theta) and item parameters (difficulty, discrimination). Accounts for item heterogeneity, provides more precise ability estimates, especially at extremes.
- **Measurement Convergence:** Different measurement approaches should yield similar substantive conclusions if measuring the same underlying construct (episodic memory ability).

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If IRT and CTT both validly measure episodic memory ability, they should show:
1. High correlations (r > 0.70 strong, r > 0.90 exceptional) at each congruence level
2. Similar LMM fixed effect estimates (Cohen's kappa > 0.60 for agreement)
3. Comparable model fit (similar AIC/BIC patterns)
4. Convergent trajectory patterns across congruence categories

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
IRT and CTT should converge, demonstrating robustness of congruence findings to measurement approach. Expected convergence criteria:
1. Pearson correlations r > 0.70 (strong) for all three congruence levels (Common, Congruent, Incongruent)
2. Cohen's kappa > 0.60 (substantial agreement) for LMM fixed effect comparisons
3. Agreement >= 80% for substantive conclusions about schema congruence effects

**Secondary Hypotheses:**
- IRT may show slightly better model fit (lower AIC) due to accounting for item heterogeneity, but difference should be small (delta-AIC < 4)
- Correlations may be highest for Common items (most homogeneous) and lowest for Incongruent items (most variable encoding/retrieval)

**Theoretical Rationale:**
Both IRT and CTT measure episodic memory ability, but with different assumptions. If schema congruence effects are robust cognitive phenomena (not measurement artifacts), they should emerge regardless of measurement approach. Convergence provides critical methodological validation for substantive conclusions in RQ 5.4.1, 5.4.2, 5.4.3.

**Expected Effect Pattern:**
- Correlations: All three congruence levels show r > 0.70, tested with Holm-Bonferroni correction
- Cohen's kappa: Fixed effect estimates show kappa > 0.60 (substantial agreement threshold)
- Agreement percentage: >= 80% concordance for significance/non-significance of congruence x time interactions
- Model fit: IRT and CTT show comparable AIC/BIC (delta < 4 indicates negligible difference)

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Inherited from RQ 5.4.1 (Common/Congruent/Incongruent schema categories)

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All three Where tags inherited from RQ 5.4.1 congruence analysis

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Inherited from RQ 5.4.1 (Common/Congruent/Incongruent schema categories)

**Inclusion Rationale:**
This RQ examines congruence effects across all three episodic memory domains (What/Where/When). Schema congruence categories (Common, Congruent, Incongruent) apply to all three domains. Analysis compares IRT vs CTT measurement of these domain-stratified congruence effects.

**Exclusion Rationale:**
None - all three domains included. Room Free Recall (RFR) paradigm excluded as per RQ 5.4.1 parent specification (interactive paradigms only: IFR/ICR/IRE).

---

## Analysis Approach

**Analysis Type:**
Methodological convergence analysis comparing IRT theta scores vs CTT mean scores. Uses Linear Mixed Models (LMMs) with identical formula specification for direct comparison.

**High-Level Workflow:**

**Step 0:** Load IRT theta, TSVR mapping, and purified item list from RQ 5.4.1. Validate dependency (RQ 5.4.1 must complete successfully).

**Step 1:** Compute CTT mean scores per participant x test x congruence level using purified item set. CTT score = mean of binary responses (0/1) across items within each congruence category.

**Step 2:** Pearson correlations between IRT theta and CTT mean scores, stratified by congruence level (3 correlations: Common, Congruent, Incongruent). Apply Holm-Bonferroni sequential correction. Test against thresholds: r > 0.70 (strong), r > 0.90 (exceptional). Report dual p-values per Decision D068.

**Step 3:** Fit parallel LMMs with identical formula for IRT and CTT:
- IRT model: theta ~ Time x Congruence + (Time | UID)
- CTT model: ctt_score ~ Time x Congruence + (Time | UID)
Use REML=False for AIC comparison. If either model fails convergence, simplify both identically (remove random slopes, iterative simplification until both converge).

**Step 4:** Validate LMM assumptions for both models (residual normality, homoscedasticity, linearity, independence, random effects normality, influential observations). Flag violations requiring sensitivity analysis.

**Step 5:** Compare fixed effect estimates between IRT and CTT models. Compute Cohen's kappa for agreement on coefficient signs and significance (using alpha=0.05). Extract effect size concordance. Report 12 fixed effects comparison (Intercept, Time, Congruence levels, Time x Congruence interactions).

**Step 6:** Compare model fit via AIC and BIC. Compute delta-AIC (IRT - CTT). Interpret per Burnham & Anderson: delta < 2 (negligible), 2-4 (weak), 4-7 (moderate), > 7 (substantial). Expected: delta-AIC small, indicating comparable fit.

**Step 7:** Prepare scatterplot data showing IRT theta vs CTT mean scores, stratified by congruence level. Include regression lines and 95% CIs. Format: 1200 rows (one per observation).

**Step 8:** Prepare trajectory plot data showing observed means for IRT and CTT across 4 test sessions, stratified by congruence level. Format: 24 rows (2 methods x 3 congruence x 4 tests).

**Expected Outputs:**
- results/step02_correlations.csv (4 rows: 3 congruence + Overall)
- results/step03_irt_lmm_summary.txt (IRT model summary)
- results/step03_ctt_lmm_summary.txt (CTT model summary)
- results/step05_coefficient_comparison.csv (12 columns: fixed effect terms)
- results/step05_agreement_metrics.csv (Cohen's kappa, concordance %)
- plots/step07_scatterplot_data.csv (1200 rows: IRT vs CTT by congruence)
- plots/step08_trajectory_data.csv (24 rows: trajectories by method x congruence)

**Success Criteria:**
- All correlations r > 0.70 (strong threshold met for all congruence levels)
- Cohen's kappa > 0.60 (substantial agreement on fixed effects)
- Agreement >= 80% (concordance on significance/non-significance of effects)
- Both models converge with identical structure (same random effects specification)
- Dual p-values present per Decision D068 (p_uncorrected and p_bonferroni)
- Plot data exists with correct row counts and no missing values

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.4.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.4.1 (Schema-Specific Trajectories)

**File Paths:**
- results/ch5/5.4.1/data/step03_theta_scores.csv (IRT ability estimates per UID x test x congruence, 400 rows in wide format)
- results/ch5/5.4.1/data/step00_tsvr_mapping.csv (time mapping: UID x test x TSVR_hours, 400 rows)
- results/ch5/5.4.1/data/step02_purified_items.csv (IRT-retained items after purification, ~50-90 items expected)
- data/cache/dfData.csv (raw binary response data for CTT computation)

**Dependencies:**
RQ 5.4.1 must complete Steps 0-3 (IRT calibration Pass 1, item purification, IRT Pass 2, theta estimation) before this RQ can run. Circuit breaker active if RQ 5.4.1 status != success.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.4.1 (N=100, inherited inclusion criteria)
- No additional exclusions

**Items:**
- [x] Purified item set from RQ 5.4.1 (post-IRT purification per Decision D039)
- [ ] Excluded items (|b| > 3.0 or a < 0.4) NOT used for CTT computation
- Rationale: CTT computed on same item set as IRT for direct comparability

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) inherited from RQ 5.4.1
- Nominal Days: 0, 1, 3, 6
- Actual time: TSVR_hours (actual hours since encoding)

**Congruence Levels:**
- [x] Common items (tag patterns: *-i1, *-i2)
- [x] Congruent items (tag patterns: *-i3, *-i4)
- [x] Incongruent items (tag patterns: *-i5, *-i6)

---
