# RQ 5.2.8: Domain � Item Difficulty Interaction

**Chapter:** 5
**Type:** Domains
**Subtype:** Domain � Item Difficulty Interaction
**Full ID:** 5.2.8

---

## Research Question

**Primary Question:**
Do easier items show faster forgetting than harder items, and does this interaction pattern differ across episodic memory domains (What, Where, When)?

**Scope:**
This RQ examines item-level response data with crossed random effects (participants � items) across three memory domains. Analysis uses IRT-derived item difficulty parameters from RQ 5.2.1 merged with raw binary responses from data/cache/dfData.csv. Structure includes N=100 participants � 4 test sessions � domain-specific items, with TSVR (actual hours since encoding) as the time metric.

**Theoretical Framing:**
Exploratory analysis testing whether the relationship between item difficulty and forgetting rate varies by domain. If domain-specific difficulty effects exist, this would suggest different forgetting mechanisms operate for What (object identity), Where (spatial location), and When (temporal order) memory components. This addresses whether easier items' potential encoding weakness (leading to faster forgetting) or ceiling effects (leading to slower apparent forgetting) manifest differently across domains.

---

## Theoretical Background

**Relevant Theories:**

- **Dual-Process Theory:** Object identity (What) can rely on familiarity-based recognition (fast, automatic, perirhinal cortex), while spatial (Where) and temporal (When) information requires recollective binding (effortful, hippocampal). Item difficulty may interact with forgetting differently depending on whether familiarity or recollection supports retrieval.

- **Encoding Strength Hypothesis:** Easier items may reflect weaker encoding demands, potentially predicting faster forgetting. Alternatively, easier items may reach ceiling performance, showing slower apparent forgetting. Domain differences could emerge if encoding strength operates differently for object features versus spatiotemporal bindings.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Domain-specific difficulty effects may reflect different forgetting mechanisms. What domain (perirhinal-dependent) may show ceiling effects for easy items, leading to negative difficulty � time interaction. Where/When domains (hippocampal-dependent) may show encoding strength effects, where easier items exhibit faster forgetting (positive interaction). Alternatively, no interaction may exist if difficulty affects only baseline performance (intercept) without influencing forgetting rate (slope).

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Exploratory analysis. Tests whether item difficulty � time interaction differs across What/Where/When domains. No directional prediction due to competing theoretical predictions (encoding strength vs ceiling effects).

**Secondary Hypotheses:**
Three-way interaction (Time � Difficulty_c � domain) will be statistically significant at Bonferroni-corrected alpha = 0.0033, indicating domain-specific difficulty effects on forgetting rate.

**Theoretical Rationale:**
If dual-process theory holds, What domain may show different difficulty � time patterns than Where/When domains due to reliance on different neural systems (perirhinal vs hippocampal). Encoding strength hypothesis suggests easier items may forgetting faster in hippocampal-dependent domains (Where/When) but not in perirhinal-dependent domains (What).

**Expected Effect Pattern:**
Cross-classified linear mixed model with crossed random effects by participant and item. Extract Time � Difficulty_c � domain interaction terms with Bonferroni-corrected alpha = 0.0033 (correcting for 3 domains � 5 statistical tests per RQ type). Expected: significant three-way interaction indicates domain-specific difficulty effects. Sign and magnitude of interaction coefficients will determine whether encoding strength or ceiling effects dominate per domain.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object naming/recognition (e.g., "ball", "chair")
  - Items: ~29 items from RQ 5.2.1
  - Theoretical basis: Perirhinal cortex, familiarity-based retrieval

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Items: ~50 items from RQ 5.2.1
  - Disambiguation: All Where sub-tags included (L/U/D combined as single "Where" factor)
  - Theoretical basis: Hippocampal binding, recollective retrieval

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal sequence memory
  - Items: ~26 items from RQ 5.2.1
  - Theoretical basis: Hippocampal binding, recollective retrieval

**Inclusion Rationale:**
RQ 5.2.8 examines all three WWW episodic memory domains to test whether item difficulty interacts with forgetting rate differently across domains. Domain-specific interactions would suggest different forgetting mechanisms for object identity versus spatiotemporal binding.

**Exclusion Rationale:**
None - all three episodic memory domains included. Analysis requires domain comparison to test for differential difficulty effects.

---

## Analysis Approach

**Analysis Type:**
Cross-classified Generalized Linear Mixed Model (GLMM) with binomial family and logit link, featuring crossed random effects by participant (UID) and item. Uses IRT-derived item difficulty parameters as predictor. Implements pymer4 for crossed random effects structure.

### Statistical Model Specification

**Primary Analysis:** Generalized Linear Mixed Model (GLMM) with binomial family and logit link.

**Justification for GLMM over LMM:**
Item-level responses are binary (correct=1, incorrect=0), violating the normality assumption required for linear mixed models. GLMM with binomial family appropriately models binary outcomes:
- Coefficients represent log-odds of correct response
- Odds ratios (exp(β)) reported for interpretation
- Predicted probabilities bounded [0, 1]

**Formula:** `Response ~ Time * Difficulty_c * domain + (Time | UID) + (1 | Item)`
**Family:** binomial (link = "logit")
**Implementation:** pymer4 Lmer() with family='binomial' parameter

### Exploratory vs Confirmatory Design

**Design Type:** Exploratory analysis

**Rationale:** This RQ tests whether item difficulty × time interaction differs across domains, with competing theoretical predictions (encoding strength vs ceiling effects). Given the absence of clear directional predictions, this is exploratory rather than confirmatory.

**Implications for Multiple Testing:**
- Primary test: Three-way Time × Difficulty_c × domain interaction (single omnibus test, α = 0.05)
- Post-hoc domain-specific tests: Conducted only if omnibus interaction is significant (α = 0.05, no Bonferroni correction for post-hoc following significant omnibus)
- Effect sizes reported regardless of significance (Cohen's d, odds ratios)

**Note:** The originally specified Bonferroni α = 0.0033 is overly conservative for exploratory analysis and would inflate Type II error. We retain Bonferroni correction only for the 3 domain-specific post-hoc contrasts (α = 0.05/3 = 0.0167) if the omnibus test is significant.

**High-Level Workflow:**

**Step 1:** Load item parameters (difficulty estimates) from RQ 5.2.1 (results/ch5/5.2.1/data/step03_item_parameters.csv) and merge with domain labels. Create data/step00_item_difficulty_by_domain.csv with columns: item_id, domain, difficulty.

**Step 2:** Extract raw binary response data from data/cache/dfData.csv in long format (one row per UID � test � item response). Merge with item difficulty and domain from Step 1. Merge with TSVR mapping from RQ 5.2.1 (results/ch5/5.2.1/data/step00_tsvr_mapping.csv) to add time variable. Create data/step01_response_level_data.csv in long format with columns: UID, test, item_id, response (0/1), TSVR_hours, domain, difficulty.

**Step 3:** Grand-mean center item difficulty (Difficulty_c) to enable interpretation of main effects and interactions. Verify Difficulty_c mean approximately 0. Transform time variable as needed (e.g., Time = TSVR_hours, log_Time = log(TSVR_hours + 1)).

**Step 4:** Fit cross-classified GLMM using pymer4 with formula: Response ~ Time * Difficulty_c * domain + (Time | UID) + (1 | Item), family='binomial'. Model structure: fixed effects for all main effects, two-way interactions, and three-way interaction; random intercepts and slopes by UID (participant-level individual differences); random intercepts by Item (item-level baseline differences). Use REML=False for model comparison via likelihood-based methods. Save fitted model and summary to results/step03_glmm_model_summary.txt.

**Step 4b: Random Effects Model Selection**
With N=100 participants and binary responses, random slopes may fail to converge. Pre-specified model selection strategy:
1. Attempt full model: (Time | UID) + (1 | Item)
2. If convergence fails, try alternative optimizers (bobyqa, nlminb)
3. If still fails, simplify to uncorrelated random effects: (1 + Time || UID) + (1 | Item)
4. If still fails, use random intercepts only: (1 | UID) + (1 | Item)
5. Document final model structure in results; interpret interaction terms acknowledging any simplification

**Step 5:** Extract interaction terms from fitted model, focusing on Time × Difficulty_c × domain three-way interaction. For exploratory analysis: report omnibus interaction test at α = 0.05. If significant, conduct domain-specific post-hoc contrasts with Bonferroni correction (α = 0.0167 for 3 tests). Report both uncorrected and Bonferroni-corrected p-values per Decision D068 (dual p-value reporting). Report odds ratios with 95% CIs for interpretation. Save interaction coefficients, standard errors, z-statistics, odds ratios, and dual p-values to results/step03_difficulty_domain_interaction.csv.

**Step 6:** Prepare plot data showing predicted trajectories for easy items (Difficulty = -1SD) versus hard items (Difficulty = +1SD) stratified by domain. Generate 6 trajectory lines: What-Easy, What-Hard, Where-Easy, Where-Hard, When-Easy, When-Hard. Include observed marginal means and model-predicted values across 4 timepoints (T1, T2, T3, T4). Save to plots/step04_difficulty_trajectories_by_domain.png and underlying data.

**Expected Outputs:**
- data/step00_item_difficulty_by_domain.csv (item-level difficulty by domain)
- data/step01_response_level_data.csv (long format response data with difficulty)
- results/step03_glmm_model_summary.txt (full GLMM summary with convergence status and random effects structure)
- results/step03_difficulty_domain_interaction.csv (interaction terms with odds ratios and dual p-values)
- plots/step04_difficulty_trajectories_by_domain.png (6-line trajectory plot on probability scale)

**Success Criteria:**
- Model converged (model.converged = True for pymer4) OR documented simplification applied
- Random effects structure documented (full slopes, uncorrelated, or intercepts-only)
- All fixed effects estimated without singularity
- Domain-stratified interactions extracted successfully
- Interaction interpretation clear:
  - Positive coefficient (OR > 1): easier items show faster forgetting (encoding strength effect)
  - Negative coefficient (OR < 1): easier items show slower forgetting (ceiling effect)
- Plot shows 6 distinct trajectories (2 difficulty levels × 3 domains) on predicted probability scale
- Dual p-values reported per Decision D068 (p_uncorrected and p_bonferroni for post-hoc tests)
- Odds ratios with 95% CIs reported for all interaction terms

---

## Validation Procedures

### GLMM Assumption Checks

1. **Overdispersion:** Residual deviance / df should be approximately 1.0 (acceptable range: 0.8-1.2)
2. **Link Function:** Predicted probabilities should span reasonable range (not all near 0 or 1)
3. **Random Effects:** Q-Q plot of random intercepts and slopes (if retained)
4. **Influential Observations:** Identify items or participants with extreme residuals

### Remedial Actions

- If overdispersion detected: Report quasi-binomial model as sensitivity analysis
- If convergence fails with random slopes: Apply pre-specified simplification strategy (Step 4b)
- If extreme observations detected: Sensitivity analysis excluding outliers

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.2.1 outputs) + RAW (binary responses from dfData.csv)

### DERIVED Data Source:

**Source RQ:**
RQ 5.2.1 (Domain-Specific Trajectories)

**File Paths:**
- results/ch5/5.2.1/data/step03_item_parameters.csv (IRT-derived item difficulty estimates)
- results/ch5/5.2.1/data/step00_tsvr_mapping.csv (time mapping: UID � test -> TSVR_hours)
- results/ch5/5.2.1/data/step02_purified_items.csv (list of retained items post-purification)

**Dependencies:**
RQ 5.2.1 must complete Steps 1-3 (IRT calibration with 3-factor What/Where/When structure, item purification per Decision D039, final IRT Pass 2) before this RQ can run. Item difficulty parameters from final calibration required.

### RAW Data Source:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- What domain: `-N-` tags (object identity items)
- Where domain: `-L-`, `-U-`, `-D-` tags (spatial location items)
- When domain: `-O-` tags (temporal order items)

**Extraction Method:**
Extract binary responses (0/1) for all items included in RQ 5.2.1 purified item set. Reshape from wide format (one row per UID � test with item columns) to long format (one row per UID � test � item response). Merge with item difficulty from RQ 5.2.1 and TSVR time mapping.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 5.2.1 inclusion criteria)
- No exclusions at participant level

**Items:**
- [x] Only items retained after RQ 5.2.1 purification (Decision D039: a >= 0.4, |b| <= 3.0)
- Expected: ~70 items across all three domains (What ~29, Where ~50, When ~26)
- Items removed during purification are excluded
- Rationale: Item difficulty parameters only available for purified items; using full item set would require separate IRT calibration

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Nominal Days: 0, 1, 3, 6
- Time metric: TSVR_hours (actual hours since encoding)

**Paradigms:**
- [x] Interactive paradigms only (IFR, ICR, IRE) - inherited from RQ 5.2.1
- [ ] Room Free Recall (RFR) - EXCLUDED
- [ ] Test Cued Recall (TCR) - EXCLUDED
- [ ] Room Recognition (RRE) - EXCLUDED

---
