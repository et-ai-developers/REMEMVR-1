# RQ 5.10: Domain-Specific Age Effects on Forgetting

**Chapter:** 5
**RQ Number:** 10
**Full ID:** 5.10

---

## Research Question

**Primary Question:**
Does the effect of age on forgetting rate vary by memory domain (What, Where, When)?

**Scope:**
This RQ examines whether age-related memory decline differs across episodic memory domains (object identity, spatial location, temporal order) using IRT-derived ability estimates across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6). Time variable uses TSVR (actual hours since encoding). Age is treated as a between-subjects continuous predictor, grand-mean centered. Focuses on detecting a 3-way Age × Domain × Time interaction.

**Theoretical Framing:**
Hippocampal aging theory predicts that memory domains relying on hippocampal binding (Where, When) should show greater age-related vulnerability than familiarity-based memory (What, which relies on perirhinal cortex). If this holds, older adults should show disproportionate forgetting for spatial and temporal contexts compared to object identity.

---

## Theoretical Background

**Relevant Theories:**
- **Hippocampal Aging Hypothesis:** The hippocampus is particularly vulnerable to age-related structural and functional decline. Domains requiring hippocampal binding (spatial, temporal) should show greater age-related memory decline than domains relying on extra-hippocampal regions (object identity via perirhinal cortex).
- **Dual-Process Theory (Yonelinas, 2002):** Familiarity-based memory (What domain) relies on perirhinal cortex and is relatively preserved in aging. Recollection-dependent memory (Where, When domains) relies on hippocampus and shows age-related decline.
- **Age-Related Associative Deficit Hypothesis (Naveh-Benjamin, 2000):** Older adults show disproportionate impairment in binding multiple elements (What+Where+When) compared to individual element memory.

**Key Citations:**
- Yonelinas (2002): Dual-process theory and age-related preservation of familiarity
- Naveh-Benjamin (2000): Associative deficit hypothesis in aging
- Raz et al. (2005): Hippocampal volume decline in aging
- Rajah & D'Esposito (2005): Age-related changes in prefrontal-hippocampal networks

**Theoretical Predictions:**
Hippocampal aging theory predicts that Age × Time effects should be strongest for When (temporal binding), intermediate for Where (spatial binding), and weakest for What (object identity). This should manifest as a significant 3-way Age × Domain × Time interaction, where older adults show steeper forgetting slopes for hippocampal-dependent domains.

**Literature Gaps:**
Most aging studies examine What and Where separately, or use aggregate memory scores. Few studies test all three WWW domains together in immersive VR with fine-grained longitudinal trajectories (TSVR actual hours). This RQ provides domain-specific age effects across the full episodic memory spectrum.

---

## Hypothesis

**Primary Hypothesis:**
Age × Time effects will be strongest for spatial (Where) and temporal (When) domains, which rely more heavily on hippocampal binding than object identity (What). This predicts a significant 3-way Age × Domain × Time interaction.

**Secondary Hypotheses:**
1. When domain will show the strongest age effect (steepest age-related slope difference)
2. Where domain will show intermediate age effect
3. What domain will show the weakest age effect (minimal age-related slope difference)
4. Ordering: Age effect When > Where > What

**Theoretical Rationale:**
Dual-process theory suggests familiarity-based information (What) relies on perirhinal cortex, which is relatively preserved in aging. Recollection-dependent binding (Where, When) relies on hippocampus, which shows structural and functional decline with age. The hippocampal aging hypothesis specifically predicts that spatial and temporal binding should be more vulnerable than object identity in older adults.

**Expected Effect Pattern:**
Significant 3-way Age × Domain × Time interaction in LMM analysis (α = 0.0033 with Bonferroni correction). Post-hoc contrasts should show: Time × Age interaction significant for When domain (p < 0.001), potentially significant for Where domain (p < 0.01), non-significant or marginal for What domain. Older adults should show steeper forgetting slopes for When and Where compared to What, with divergence increasing over the retention interval.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: **ALL Where tags included** (complete spatial coverage)

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ examines age effects across all three WWW episodic memory components to test the hippocampal aging hypothesis. Complete domain coverage is necessary to evaluate domain-specific vulnerability to aging. Theoretical predictions require comparing hippocampal-dependent (Where, When) vs. perirhinal-dependent (What) domains.

**Exclusion Rationale:**
None - all WWW domains included for comprehensive age-by-domain interaction test.

---

## Analysis Approach

**Analysis Type:**
LMM (Linear Mixed Models) with 3-way Age × Domain × Time interaction

**High-Level Workflow:**

**Step 0:** Get Data
- Use theta scores from results/ch5/rq1/ (IRT ability estimates from RQ 5.1)
- Get TSVR mapping from results/ch5/rq1/data/step00_tsvr_mapping.csv (actual hours since encoding)
- Load Age from data/cache/dfData.csv (one value per UID, column name 'age')

**Step 1:** Data Preparation
- Merge Age with theta scores on UID
- Grand-mean center Age (Age_c = Age - mean(Age))
- Reshape to long format (Domain as factor variable: What/Where/When)
- Create time transformations: TSVR (hours), log(TSVR+1)
- Structure: 400 observations × 3 domains with Age as between-subjects predictor

**Step 2:** Fit LMM with 3-Way Interaction
- Formula: Theta ~ (Time + log(Time+1)) × Age_c × Domain + (Time | UID)
- Treatment coding: What as reference domain
- Random intercepts and slopes by UID
- Fit with REML=False
- Save model pickle

**Step 2b:** LMM Assumption Validation

After fitting LMM, validate all assumptions before proceeding to inference:

1. **Residual Normality:**
   - Q-Q plot of marginal residuals (visual inspection)
   - Shapiro-Wilk test (p>0.05 indicates normality)
   - If violated: Consider robust standard errors or square root transformation

2. **Homoscedasticity:**
   - Plot residuals vs fitted values
   - Check for constant variance (no fanning pattern)
   - If violated: Consider weighted LMM or log transformation

3. **Random Effects Normality:**
   - Q-Q plot of random intercepts and slopes
   - Visual inspection for normality
   - If violated: May indicate outlier participants or model misspecification

4. **Independence:**
   - ACF plot of residuals (check autocorrelation)
   - Lag-1 ACF should be < 0.1
   - If violated: Consider autoregressive error structure AR(1)

5. **Linearity:**
   - Partial residual plots for Age and Time predictors
   - Check for linear relationships
   - If non-linear: Consider quadratic Age or splines

6. **Outliers/Influence:**
   - Cook's distance (D > 4/n = 0.04 threshold)
   - Leverage, DFBETAS for influential observations
   - Report outliers, conduct sensitivity analysis excluding them

7. **Convergence Diagnostics:**
   - Check for singularity warnings, gradient convergence
   - If warnings: Refit with simpler random structure (Time || UID or 1 | UID)
   - Report final convergence status

**Step 2c:** Model Selection for Random Effects

Test random effects structure via likelihood ratio test (with REML=True):

1. **Full model:** Theta ~ fixed effects + (Time | UID) [random intercepts + slopes]
2. **Uncorrelated model:** Theta ~ fixed effects + (Time || UID) [uncorrelated random effects]
3. **Intercept-only model:** Theta ~ fixed effects + (1 | UID) [random intercepts only]

- Compare models using LRT (chi-square test on -2 log-likelihood difference)
- Select most parsimonious model that significantly improves fit (p < 0.05)
- If random slopes model fails to converge: fall back to intercepts-only
- Refit selected model with REML=False for fixed effects inference

**Step 3:** Extract 3-Way Interaction Terms
- Extract Time × Age_c × Domain[Where/When]: Linear age-by-domain interactions
- Extract log(Time+1) × Age_c × Domain[Where/When]: Logarithmic age-by-domain interactions
- Apply Bonferroni correction: α = 0.05 / 2 = 0.025 (for 2 three-way interaction tests: linear + log)
- Note: Family-wise error rate defined as 2 three-way interaction terms only (primary hypothesis tests)
- If either interaction significant: Age effects on forgetting differ by domain

**Step 4:** Compute Domain-Specific Age Effects and Post-Hoc Contrasts
- Extract age effect on forgetting rate for each domain (What/Where/When)
- Evaluate at Day 3 (midpoint of observation window)
- Create summary table with age slopes per domain
- Test hypothesis: Where/When show stronger age-related decline than What

**Post-hoc pairwise comparisons** (if Step 3 interaction significant):
- Compare age × time slopes across all domain pairs: Where vs What, When vs What, Where vs When
- Apply Tukey HSD correction for 3 pairwise comparisons
- Critical value: q(3 groups, df) from Tukey distribution
- Test whether ordering is significant: Age effect When > Where > What

**Step 5:** Visualization
- Generate multi-panel plot (3 panels: What, Where, When)
- Within each panel: Age tertiles (Young/Middle/Older) with separate trajectories
- Include observed means with 95% CIs
- Overlay model predictions
- Highlight differential age effects across domains

**Data Preprocessing (Per Solution Section 1.4):**
- **IRT Theta Scores:** Use purified ability estimates from RQ 5.1 (no additional preprocessing)
- **Age Variable:** Continuous, grand-mean centered (Age_c = Age - mean(Age))
- **Time Variable:** TSVR (actual hours since encoding), plus log(TSVR+1) transformation
- **Domain Structure:** Long format with Domain as factor (What/Where/When)

**Special Methods:**
- **3-Way Interaction:** Tests Age × Domain × Time to detect domain-specific age effects
- **Treatment Coding:** What domain as reference (least hippocampal-dependent, natural baseline)
- **TSVR Time Variable:** Actual hours since encoding (not nominal days) for precise temporal resolution
- **Random Slopes:** Account for individual differences in forgetting rates (Time | UID), with LRT model selection
- **Bonferroni Correction:** α = 0.025 for 2 three-way interaction terms (linear + log time transformations)
- **Post-Hoc Correction:** Tukey HSD for 3 pairwise domain comparisons (controls family-wise error rate)
- **Assumption Validation:** Comprehensive LMM diagnostics (residual normality, homoscedasticity, independence, linearity, outliers, convergence)
- **Age Tertiles for Visualization:** Split Age into Young/Middle/Older groups for interpretable plotting (analysis uses continuous Age)

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.1 (Domain-Specific Forgetting Trajectories)

**File Paths:**
- `results/ch5/rq1/data/step00_tsvr_mapping.csv` (TSVR actual hours mapping)
- `results/ch5/rq1/data/step03_theta_scores.csv` (IRT ability estimates, purified)
  - Columns: composite_ID, domain (What/Where/When), test (T1/T2/T3/T4), theta
- `data/cache/dfData.csv` (Age variable)
  - Columns: UID, age (one value per participant)

**Dependencies:**
RQ 5.1 must complete Steps 0-3 (TSVR mapping, IRT calibration, purification, theta extraction) before this RQ can run.

**Usage:**
This RQ uses theta scores from RQ 5.1 as outcome variable for 3-way Age × Domain × Time LMM analysis. Age is merged from dfData.csv as between-subjects predictor.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.1 (inherited inclusion criteria)
- Note: Age is continuous predictor (grand-mean centered)

**Items:**
- N/A (theta scores already aggregated per domain from RQ 5.1 purified item set)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Time variable: TSVR (actual hours since encoding from RQ 5.1)

---
