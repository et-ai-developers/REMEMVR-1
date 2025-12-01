# RQ 5.3.4: Age × Paradigm Interactions

**Chapter:** 5
**Type:** Paradigms
**Subtype:** Age × Paradigm Interactions
**Full ID:** 5.3.4

---

## Research Question

**Primary Question:**
Does the effect of age on forgetting rate vary by retrieval paradigm?

**Scope:**
This RQ examines age-related differences in forgetting trajectories across three retrieval paradigms: Free Recall, Cued Recall, and Recognition. N=100 participants (age 20-70 years) x 4 test sessions x 3 paradigms = 1200 observations. Time variable uses TSVR (actual hours since encoding). Tests for 3-way Age x Paradigm x Time interaction to determine if age effects on memory decline differ by retrieval support level.

**Theoretical Framing:**
Aging differentially affects memory systems depending on retrieval demands. This RQ tests whether older adults show greater age-related deficits in self-initiated retrieval (Free Recall) compared to supported retrieval (Cued Recall, Recognition), consistent with hippocampal aging effects on recollection-dependent processes.

---

## Theoretical Background

**Relevant Theories:**

- **Dual-Process Theory** (Yonelinas, 2002): Memory retrieval relies on familiarity (fast, automatic) and recollection (slow, effortful). Free Recall is most recollection-dependent, while Recognition can rely on familiarity. Hippocampal aging disproportionately impairs recollection.

- **Retrieval Support Hypothesis**: Older adults benefit more from environmental support during retrieval. Cued Recall and Recognition provide retrieval cues that reduce demands on self-initiated retrieval processes that decline with age.

- **Hippocampal Aging**: Age-related hippocampal volume loss and functional decline disproportionately affect processes requiring pattern completion and self-initiated retrieval (Free Recall) compared to familiarity-based recognition (perirhinal cortex).

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Age x Time effects strongest for Free Recall (most demanding, recollection-dependent) and weakest for Recognition (familiarity-based, less age-sensitive). Cued Recall falls intermediate. This predicts significant 3-way Age x Paradigm x Time interaction.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Age x Time effects will be strongest for Free Recall (most demanding) and weakest for Recognition (familiarity-based). 3-way Age x Paradigm x Time interaction significant at Bonferroni alpha=0.025.

**Secondary Hypotheses:**
None specified - primary focus on 3-way interaction pattern.

**Theoretical Rationale:**
Older adults show disproportionate deficits in self-initiated retrieval processes (Free Recall) due to hippocampal aging effects on recollection. Recognition relies more on familiarity (perirhinal cortex), which is relatively preserved in aging. Cued Recall provides intermediate retrieval support, reducing but not eliminating age-related deficits.

**Expected Effect Pattern:**
Significant 3-way Age x Paradigm x Time interaction (p < 0.025 Bonferroni-corrected). Paradigm-specific age effects at Day 3 midpoint will show: Free Recall > Cued Recall > Recognition in magnitude of age-related forgetting acceleration. Post-hoc contrasts with Tukey HSD will confirm ordered pattern.

---

## Memory Domains

**Domains Examined:**

- [x] **Paradigm-Based Analysis** (not domain-based)
  - Focus: Free Recall (IFR), Cued Recall (ICR), Recognition (IRE)
  - Structure: Three retrieval paradigms differing in retrieval support level

**Paradigm Selection:**

**Free Recall (IFR):**
- Self-initiated retrieval, no cues
- Most demanding, recollection-dependent
- Hippocampal-dependent pattern completion

**Cued Recall (ICR):**
- Retrieval with category cues
- Intermediate support level
- Reduces self-initiation demands

**Recognition (IRE):**
- Item recognition with distractors
- Least demanding, familiarity-based option
- Can rely on perirhinal cortex familiarity signals

**Inclusion Rationale:**
These three paradigms span the retrieval support gradient from unsupported (Free Recall) to fully supported (Recognition), allowing test of whether age effects vary systematically with retrieval demands.

**Exclusion Rationale:**
Room Free Recall (RFR), Think Cued Recall (TCR), and Room Recognition (RRE) excluded as they involve different encoding/retrieval processes (spatial navigation, think encoding) that confound paradigm comparisons.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) with 3-way Age x Paradigm x Time interaction

**High-Level Workflow:**

**Step 0:** Load RQ 5.3.1 theta scores (1200 rows: 100 participants x 4 tests x 3 paradigms) and Age variable from data/cache/dfData.csv

**Step 1:** Merge theta scores with TSVR mapping and Age. Grand-mean center Age (Age_c, verify mean ~ 0). Create time transformation log_TSVR = log(TSVR_hours + 1)

**Step 2:** Fit LMM with full 3-way interaction structure:
- Formula: theta ~ TSVR_hours + log_TSVR + Age_c + paradigm + all 2-way interactions + 3-way Age_c x paradigm x Time interactions + (TSVR_hours | UID)
- Random effects: random slopes for TSVR_hours by participant (UID)
- REML=False for model comparison

**Step 3:** Extract 4 three-way interaction terms (Age_c x paradigm x TSVR_hours, Age_c x paradigm x log_TSVR for 3 paradigm levels). Test significance at Bonferroni alpha=0.025 (correcting for 2 time transformations). Report dual p-values per Decision D068 (uncorrected and Bonferroni-corrected).

**Step 4:** Compute paradigm-specific age effects at Day 3 midpoint. Extract marginal slopes for each paradigm at mean age vs age+1SD. Post-hoc contrasts with Tukey HSD to test ordered pattern (Free > Cued > Recognition). Report dual p-values.

**Step 5:** Prepare plot data by age tertiles (Young/Middle/Older) for visualization. Aggregate observed means and model predictions per paradigm x age tertile x timepoint.

**Expected Outputs:**
- data/step01_lmm_input.csv (1200 rows: theta, TSVR_hours, log_TSVR, Age_c, paradigm, UID, test)
- data/step02_lmm_model.pkl (saved fitted model object)
- data/step03_interaction_terms.csv (4 rows: 3-way interaction coefficients, SE, z, p-values)
- data/step04_age_effects_by_paradigm.csv (3 rows: paradigm-specific age effect sizes and post-hoc contrasts)
- plots/step05_age_effects_plot_data.csv (plot data: 3 paradigms x 3 age tertiles x 4 timepoints = 36 rows)

**Success Criteria:**
- Model converges (model.converged=True)
- All 1200 observations present in merged data
- Age_c grand-mean centered (mean ~ 0, tolerance ±0.1)
- 4 three-way interaction terms extracted with valid SE and z-statistics
- Dual p-values reported per Decision D068 (both uncorrected and Bonferroni-corrected)
- 3 paradigms with age effect estimates and confidence intervals
- Plot data complete: 36 rows (3 paradigms x 3 tertiles x 4 tests), no NaN values
- Random slopes variance positive (indicates between-person variability in time effects)
- All assumption validation checks documented (see Validation Procedures below)

---

## Validation Procedures

### LMM Assumption Checks

1. **Residual Normality:** Q-Q plot + Shapiro-Wilk test (accept if p > 0.01)
2. **Homoscedasticity:** Residuals vs fitted plot; Levene's test by paradigm × age tertile
3. **Random Effects Normality:** Q-Q plot of random effect estimates
4. **Independence:** ACF plot of residuals (no significant autocorrelation)
5. **Linearity:** Residuals vs TSVR_hours and log_TSVR (no systematic patterns)
6. **Outliers:** Cook's distance < 4/N threshold

### Remedial Actions

- If normality violated: Report robust standard errors or use bootstrap confidence intervals
- If heteroscedasticity: Use weighted LMM or variance function by paradigm
- If outliers detected: Sensitivity analysis with/without outliers

### Convergence Contingency Plan

If the full model (random slopes for TSVR_hours) fails to converge:
1. Try alternative optimizers (bobyqa, nlminb)
2. Use likelihood ratio test (LRT) to compare random slopes vs intercept-only
3. If LRT p < 0.05, retain slopes with simplified correlation structure
4. If LRT p ≥ 0.05, use random intercepts-only model
5. Document which structure achieved convergence in results

Reference: Bates et al. (2015) parsimonious mixed models guidelines.

### Log Transformation Rationale

**Why log(TSVR_hours + 1):**
- The +1 constant ensures log transformation is defined for Day 0 (TSVR_hours = 0 at immediate test)
- Logarithmic time captures the well-established non-linear forgetting pattern where forgetting rate decelerates over time (Ebbinghaus, 1885; Wixted & Ebbesen, 1991)
- Chapter 5 model selection (RQs 5.1.1, 5.3.1) consistently identifies logarithmic or Lin+Log models as best-fitting
- Including both linear (TSVR_hours) and logarithmic (log_TSVR) terms allows the model to capture both early rapid forgetting and later asymptotic retention

### Multiple Testing Correction

Bonferroni alpha = 0.025 corrects for 2 time transformation terms (linear and logarithmic). This is a conservative approach ensuring family-wise error rate control. Both uncorrected and corrected p-values reported per Decision D068 to allow readers to assess effect robustness under different correction assumptions.

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.3.1 outputs and raw Age variable)

### DERIVED Data Source:

**Source RQ:**
RQ 5.3.1 (Paradigm-Specific Trajectories)

**File Paths:**
- results/ch5/5.3.1/data/step03_theta_scores.csv (IRT ability estimates per participant x test, reshaped to 1200 rows for 3 paradigms)
- results/ch5/5.3.1/data/step00_tsvr_mapping.csv (actual hours since encoding per participant x test)
- data/cache/dfData.csv (Age variable: participant age in years, range 20-70)

**Dependencies:**
RQ 5.3.1 must complete through Step 3 (IRT calibration on paradigm-specific factors: Free Recall, Cued Recall, Recognition) before this RQ can run. Requires theta scores for all 3 paradigms.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 5.3.1 (inherited inclusion criteria)
- Age range: 20-70 years (full sample, no exclusions)
- Age transformation: Grand-mean centered (Age_c = Age - mean(Age))

**Items:**
- N/A (theta scores already aggregated at paradigm level per RQ 5.3.1)
- Item purification completed in RQ 5.3.1 (Decision D039: a >= 0.4, |b| <= 3.0)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- [x] TSVR (actual hours since encoding) used as continuous time variable, not nominal days

**Paradigms:**
- [x] Free Recall (IFR) - unsupported retrieval
- [x] Cued Recall (ICR) - cued retrieval
- [x] Recognition (IRE) - recognition with distractors
- [ ] Room Free Recall (RFR) - EXCLUDED (different encoding/retrieval process)
- [ ] Think Cued Recall (TCR) - EXCLUDED (different encoding)
- [ ] Room Recognition (RRE) - EXCLUDED (spatial navigation confound)

---
