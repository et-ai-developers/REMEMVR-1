# RQ 5.3.2: Linear Trend in Forgetting Rate Across Paradigms

**Chapter:** 5
**RQ Number:** 5.3.2
**Full ID:** 5.3.2

---

## Research Question

**Primary Question:**
Does forgetting rate decrease monotonically from Free Recall -> Cued Recall -> Recognition, consistent with an ordered retrieval support gradient?

**Scope:**
This RQ examines whether paradigm-specific forgetting rates lie on an ordered continuum rather than merely differing pairwise. Tests three retrieval paradigms (Free Recall, Cued Recall, Recognition) ordered by decreasing retrieval support. Uses slope estimates from best-fitting LMM model from RQ5.3, evaluated at Day 3 (midpoint).

**Theoretical Framing:**
Retrieval support gradient theory predicts that paradigms providing more retrieval cues (Recognition > Cued > Free) should show slower forgetting because more cues are available to access degrading memory traces. Testing linear trend is more powerful than pairwise contrasts for confirming this ordered theoretical prediction.

---

## Theoretical Background

**Relevant Theories:**
- **Retrieval Support Gradient:** Memory performance improves with more retrieval cues - Free Recall (no cues) < Cued Recall (partial cues) < Recognition (full cues). Forgetting should follow inverse pattern.
- **Encoding-Retrieval Specificity** (Tulving & Thomson, 1973): Retrieval success depends on overlap between encoding context and retrieval cues. More supportive paradigms provide greater overlap.

**Key Citations:**
- Rosenthal & Rosnow (1985): Linear trend contrast methodology - more powerful than pairwise tests for detecting ordered effects
- Maxwell & Delaney (2004): Polynomial contrasts - standard approach for ordered factors, orthogonal to intercept

**Theoretical Predictions:**
Linear trend contrast predicts forgetting rate (slope magnitude) follows ordered pattern: Free > Cued > Recognition. Positive trend slope indicates forgetting decreases as retrieval support increases.

**Literature Gaps:**
Most studies compare paradigms pairwise. Linear trend test provides stronger, unified test of retrieval support continuum hypothesis with higher statistical power (1 df vs 3 df for pairwise tests).

---

## Hypothesis

**Primary Hypothesis:**
Forgetting rate (slope magnitude) follows ordered trend: Free > Cued > Recognition. More negative slope = faster forgetting. Paradigms should lie on a monotonic continuum.

**Secondary Hypotheses:**
1. Linear trend contrast will be significant at Bonferroni-corrected alpha = 0.0033

**Theoretical Rationale:**
Retrieval support gradient predicts monotonic ordering. Recognition provides maximum retrieval support (full item re-presentation), Cued Recall provides partial support, Free Recall provides minimal support. Trace degradation affects all paradigms equally, but retrieval success probability differs based on available cues.

**Expected Effect Pattern:**
- Slope estimates (Day 3): Free ~ -0.08, Cued ~ -0.06, Recognition ~ -0.04
- Linear trend contrast: Positive coefficient (~0.02), indicating forgetting decreases with more support
- One-tailed test justified by directional hypothesis (if opposite direction found, interpreted as no support for theory, not evidence against)

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Not directly examined - paradigm-level analysis

- [ ] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location)
  - [ ] `-U-` tags (pick-up location)
  - [ ] `-D-` tags (put-down location)
  - Disambiguation: Not directly examined - paradigm-level analysis

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Not directly examined - paradigm-level analysis

**Inclusion Rationale:**
This RQ does NOT examine specific WWW memory domains. Instead, it examines retrieval paradigms (Free, Cued, Recognition) that cut across all memory domains. The analysis uses theta scores aggregated at the paradigm level from RQ5.3, which may include items from multiple domains.

**Exclusion Rationale:**
Domain-specific analysis is covered by RQ5.1-5.2. This RQ tests paradigm effects independently of domain membership.

---

## Analysis Approach

**Analysis Type:**
Secondary Analysis (Linear Trend Contrast) on model outputs from RQ5.3

**High-Level Workflow:**

**Step 1:** Load saved best-fitting LMM model from RQ5.3 (pickle file)

**Step 2:** Recreate theta scores data in long format (load from RQ5.3 data files)

**Step 3:** Extract paradigm-specific slopes from model parameters
- For Lin+Log model: Combine linear and logarithmic slope components
- Evaluate instantaneous slopes at Day 3 (midpoint of observation window)
- Create summary table: Free, Cued, Recognition slopes

**Step 4:** Linear Trend Contrast Test (Within-LMM Approach)
- Test linear trend contrast directly within RQ5.3 LMM using emmeans-equivalent approach
- Extract paradigm marginal means at Day 3 and apply contrast weights [-1, 0, +1]
- This preserves full sample information (N=100 participants) and proper degrees of freedom
- Apply Bonferroni correction: alpha = 0.0033

**Step 5:** Visualization
- Generate bar plot showing forgetting rates for three paradigms
- Overlay linear trend line for visual interpretation (NOT for statistical inference)
- Include horizontal reference line at zero

**Data Preprocessing (Per Solution Section 1.4):**
- Not applicable - uses pre-processed theta scores from RQ5.3
- No raw data extraction required

**Special Methods:**
- **Within-LMM contrast testing:** Test linear trend contrast within RQ5.3 LMM using marginaleffects or statsmodels contrast methods (Maxwell & Delaney, 2004 recommend testing contrasts within omnibus model)
- **Contrast weights:** [-1, 0, +1] for ordered categorical predictor (Free=1, Cued=2, Recognition=3)
- **Instantaneous slope at Day 3:** For Lin+Log models, slope varies with time; evaluate at midpoint to avoid extrapolation bias
- **One-tailed test:** Directional hypothesis justified by strong theoretical prediction - if opposite direction found, interpreted as no support for theory

---

## Data Source

**Data Type:**
DERIVED (from RQ5.3 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.3 (Paradigm-Specific Forgetting Trajectories)

**File Paths:**
- `results/ch5/5.3.1/data/theta_scores_by_paradigm.csv` (theta scores long format)
- `results/ch5/5.3.1/code/best_model.pkl` (best-fitting LMM pickle)

**Dependencies:**
RQ5.3 must complete successfully before RQ5.4 can execute. Required outputs:
1. Best-fitting LMM model (pickle) with paradigm-specific slopes
2. Theta scores data in long format with paradigm labels

**Usage:**
Slopes extracted from RQ5.3 model are the outcome variable for linear trend analysis. No re-fitting of LMM required.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ5.3 (inherited inclusion criteria)

**Items:**
- N/A (theta scores already aggregated per paradigm from RQ5.3)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) - inherited from RQ5.3 model

---
