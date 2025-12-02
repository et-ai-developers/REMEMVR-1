# RQ 5.1.6: Item Difficulty Interaction

**Chapter:** 5
**Type:** General
**Subtype:** Item Difficulty Interaction
**Full ID:** 5.1.6

---

## Research Question

**Primary Question:**
Do easier items (lower difficulty) show faster forgetting than harder items, consistent with initial strength predicting decay rate?

**Scope:**
This RQ examines the relationship between item difficulty and forgetting rate using cross-classified mixed models. Analysis uses item-level responses (UID x Test x Item) with IRT-derived difficulty parameters from RQ 5.2.1. Item difficulty varies across the full range of calibrated items. Time variable uses TSVR (actual hours since encoding). Sample: N=100 participants x 4 tests x ~70-105 items (post-purification from RQ 5.2.1) = approximately 28,000-42,000 item-level observations.

**Theoretical Framing:**
Exploratory analysis testing competing theoretical predictions about the relationship between initial item strength (operationalized as IRT difficulty) and subsequent forgetting rate. Addresses fundamental question of whether easier-to-encode items show differential forgetting trajectories compared to harder items. Cross-classified random effects structure (participants and items) accounts for dependencies in repeated measures design.

---

## Theoretical Background

**Relevant Theories:**

- **Strength-Dependent Forgetting**: Items encoded with greater initial strength may show different forgetting rates than weakly-encoded items. Direction of effect contested in literature.

- **Ceiling Effects Hypothesis**: Easier items (high accuracy) may show artifactually slower forgetting due to measurement ceiling effects constraining observable decline.

- **Encoding Variability**: Harder items may require more variable encoding strategies across participants, potentially affecting stability of memory traces over time.

**Key Citations:**
- Agresti, A. (2013). *Categorical Data Analysis* (3rd ed.). Wiley. (GLMM methodology for binary outcomes)
- Bates, D., et al. (2015). Fitting linear mixed-effects models using lme4. *Journal of Statistical Software*, 67(1), 1-48. (lme4/pymer4 backend for GLMM)
- Schielzeth, H., et al. (2020). Robustness of linear mixed-effects models to violations of distributional assumptions. *Methods in Ecology and Evolution*, 11(9), 1141-1152. (LMM vs GLMM for binary data)
- [Additional citations to be added by rq_scholar]

**Theoretical Predictions:**

Three competing predictions exist:

1. **Positive Interaction (Easier -> Faster Forgetting)**: Easier items reflect weaker encoding and show faster forgetting. Initial strength negatively predicts retention.

2. **Negative Interaction (Easier -> Slower Forgetting)**: Easier items experience ceiling effects that constrain observable forgetting, producing artifactually shallow decline.

3. **No Interaction (Difficulty Affects Intercept Only)**: Item difficulty shifts baseline performance but does not affect forgetting rate. All items decay at same proportional rate.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Exploratory analysis with no directional prediction. Three competing theoretical predictions outlined above. Interaction tested at alpha = 0.05 (single planned comparison; Bonferroni correction unnecessary for single test).

**Secondary Hypotheses:**
None - exploratory analysis.

**Theoretical Rationale:**
Item difficulty x time interaction tests whether forgetting rate (slope) depends on initial item strength. Positive coefficient indicates easier items (lower difficulty parameter) show faster forgetting. Negative coefficient indicates easier items show slower forgetting (potentially due to ceiling effects). Non-significant interaction indicates difficulty affects baseline performance only, not forgetting rate.

**Expected Effect Pattern:**
Time:Difficulty_c interaction term extracted from cross-classified binomial GLMM. Alpha = 0.05 (single planned comparison). Effect size interpretation based on log-odds coefficient sign:
- Positive coefficient: Easier items show faster forgetting (steeper decline in log-odds of correct response)
- Negative coefficient: Easier items show slower forgetting (ceiling effect on probability scale)
- Non-significant: No differential forgetting by difficulty (null hypothesis)

Report odds ratio (OR) with 95% CI for clinical interpretability. OR = exp(coefficient) represents multiplicative change in odds per unit change in difficulty.

Visualization: Plot predicted probability trajectories (inverse logit scale) for easy items (-1SD difficulty) vs hard items (+1SD difficulty). Significant interaction shows divergence over time; non-significant interaction shows parallel trajectories.

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: NOT specifically examined - analysis uses all items from RQ 5.2.1

- [ ] **Where** (Spatial Location)
  - Tag Codes: `-L-`, `-U-`, `-D-`
  - Description: NOT specifically examined - analysis uses all items from RQ 5.2.1

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: NOT specifically examined - analysis uses all items from RQ 5.2.1

**Inclusion Rationale:**
This is a General analysis (Type 5.1.X) examining item difficulty effects across all domains combined. Uses the full purified item set from RQ 5.2.1 (What/Where/When combined) to maximize item difficulty variability and statistical power. Domain distinctions are not focal to this RQ - the analysis examines difficulty as a continuous item-level predictor across all episodic memory content.

**Exclusion Rationale:**
None - all purified items from RQ 5.2.1 included to maximize range of item difficulty values and ensure sufficient statistical power for detecting item-level effects.

---

## Analysis Approach

**Analysis Type:**
Cross-Classified Generalized Linear Mixed Model (GLMM) with item-level binary responses. Uses pymer4 package for crossed random effects structure: (Time | UID) + (1 | Item). **Model family: binomial with logit link** (required for binary response data - TQ dichotomized to 0/1). Coefficients reported as log-odds; exponentiate for odds ratios interpretation.

**High-Level Workflow:**

**Step 1:** Load item parameters from RQ 5.2.1 (IRT difficulty parameter 'b' for each item) and raw response data from dfData.csv. Convert raw responses to long format (one row per UID x Test x Item observation).

**Step 2:** Merge item difficulty (IRT parameter 'b') into response-level data. Each item-level observation receives its corresponding difficulty value.

**Step 3:** Grand-mean center item difficulty to create Difficulty_c predictor. Verify mean approximately 0. Centering facilitates interpretation of main effects and reduces multicollinearity.

**Step 4:** Fit cross-classified binomial GLMM using pymer4:
- Formula: `Response ~ Time * Difficulty_c + (Time | UID) + (1 | Item)`
- **Model specification:** `Lmer(formula, data, family='binomial')` with nAGQ=1 (Laplace approximation, default for speed; increase to nAGQ=7 for accuracy if model converges)
- Crossed random effects: participants (UID) and items (Item)
- Random slopes for Time by UID (individual forgetting trajectories on log-odds scale)
- Random intercepts for Item (item difficulty differences)
- Fixed effects: Time (main effect of retention interval), Difficulty_c (main effect of difficulty), Time:Difficulty_c (interaction testing differential forgetting)
- **Estimation:** Adaptive Gaussian quadrature via lme4 backend

**Step 4b: Convergence Fallback Strategy** (if Step 4 fails to converge):
1. First attempt: Simplify to uncorrelated random effects `(Time || UID)` (removes correlation parameter)
2. Second attempt: Remove random slopes `(1 | UID) + (1 | Item)` (intercepts only)
3. Third attempt: Single grouping factor `(1 | UID)` (remove item random effects)
4. Document simplification with LRT justification (compare nested models)
5. If all fail: Report convergence failure as legitimate finding (model complexity exceeds data support)

**Step 5:** Validate GLMM assumptions:
- Check overdispersion (dispersion parameter should be ~1.0 for binomial)
- Examine residual patterns (DHARMa package or manual simulation)
- Verify random effects normality (Q-Q plots for UID and Item random effects)

**Step 6:** Extract Time:Difficulty_c interaction term. Report:
- Log-odds coefficient, SE, z-statistic, p-value
- Odds ratio (exp(coefficient)) with 95% CI
- Apply alpha = 0.05 threshold (single planned comparison; Bonferroni 0.0033 overly conservative for exploratory study)
- Interpret coefficient sign on log-odds scale:
  - Positive: Easier items (lower difficulty) show faster forgetting (steeper decline in log-odds)
  - Negative: Easier items show slower forgetting (ceiling effect on probability scale)

**Step 7:** Prepare plot data comparing easy items (difficulty at -1SD) vs hard items (difficulty at +1SD). Generate predicted probability trajectories (not log-odds) across 4 test sessions using inverse logit transformation. Plot shows convergence/divergence pattern on interpretable probability scale.

**Practice Effects Consideration:** Practice effects across 4 test sessions are mitigated via: (1) IRT theta scoring removes item-level practice confounds, (2) Random slopes (Time | UID) capture individual practice trajectories, (3) Time effect represents average forgetting net of practice. Acknowledge as limitation in interpretation.

**Expected Outputs:**
- `data/step00_item_difficulty.csv` - Item parameters from RQ 5.2.1 (item IDs + difficulty values)
- `data/step01_response_level_data.csv` - Raw responses in long format (UID x Test x Item)
- `data/step02_merged_data.csv` - Response data merged with item difficulty and TSVR
- `results/step03_glmm_model_summary.txt` - Full pymer4 GLMM output (binomial family)
- `results/step03_convergence_log.txt` - Convergence status and any fallback steps taken
- `results/step04_glmm_diagnostics.txt` - Overdispersion, residual checks, random effects normality
- `results/step05_difficulty_interaction.csv` - Interaction term (log-odds coefficient, SE, z, p, OR, 95% CI)
- `plots/step06_difficulty_trajectories.png` - Easy vs hard item probability trajectories (inverse logit scale)

**Success Criteria:**
- pymer4 binomial GLMM converges successfully (model.converged = True, or fallback model documented)
- Item difficulty merged correctly (no missing values, all items matched)
- Difficulty_c grand-mean centered (mean ~ 0, verified)
- GLMM diagnostics acceptable (overdispersion ~1.0, no systematic residual patterns)
- Interaction term successfully extracted with finite SE and p-value
- Both log-odds coefficient AND odds ratio reported with 95% CI
- Interpretation matches coefficient sign (positive/negative/null correctly interpreted on log-odds scale)
- Plot shows predicted probabilities (not log-odds) with divergence or parallel trajectories
- Convergence fallback strategy documented if initial model fails
- Analysis replicates with same random seed

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.2.1 outputs) + RAW (from dfData.csv for response data)

### DERIVED Data Source:

**Source RQ:**
RQ 5.2.1 (Domain-Specific Trajectories)

**File Paths:**
- `results/ch5/5.2.1/data/step03_item_parameters.csv` - IRT item parameters (difficulty 'b' values post-purification)
- `results/ch5/5.2.1/data/step00_tsvr_mapping.csv` - TSVR mapping (actual hours since encoding)

**Dependencies:**
RQ 5.2.1 must complete Step 3 (IRT Pass 2 calibration on purified items) before this RQ can run. Item parameters required to determine which items retained post-purification and their IRT difficulty values.

### RAW Data Source:

**Source File:**
`data/cache/dfData.csv`

**Tag Patterns:**
- All interactive paradigm items (IFR, ICR, IRE)
- What domain: `-N-` tags
- Where domain: `-L-`, `-U-`, `-D-` tags
- When domain: `-O-` tags
- Excludes RFR, TCR, RRE (non-interactive paradigms)

**Extraction Method:**
Step 1 filters dfData.csv to include only items that survived RQ 5.2.1 purification (Decision D039: a >= 0.4, |b| <= 3.0). Responses dichotomized (TQ < 1 -> 0, TQ >= 1 -> 1). Data reshaped from wide format (one row per UID x Test) to long format (one row per UID x Test x Item) for item-level analysis.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- Inherited from RQ 5.2.1

**Items:**
- [x] Only purified items from RQ 5.2.1 (approximately 70-105 items retained, 30-70% retention rate expected)
- [ ] Items excluded by RQ 5.2.1 purification (Decision D039: |b| > 3.0 OR a < 0.4)
- Rationale: Analysis requires valid IRT difficulty parameters; only purified items have reliable parameter estimates

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Time variable: TSVR_hours (actual hours since encoding, not nominal days)

---
