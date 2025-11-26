# RQ 5.11: IRT-CTT Convergent Validity

**Chapter:** 5
**RQ Number:** 11
**Full ID:** 5.11

---

## Research Question

**Primary Question:**
Do IRT theta scores and CTT mean scores yield the same conclusions about domain-specific forgetting trajectories?

**Scope:**
This RQ examines convergent validity between two measurement approaches (IRT vs CTT) for episodic memory ability across three domains (What, Where, When) and four test sessions (T1, T2, T3, T4). Focuses on correlation magnitude (r > 0.90 threshold), statistical significance agreement in LMM coefficients, and trajectory pattern overlap. Uses identical data sources and models for direct comparison.

**Theoretical Framing:**
Convergent validity is a cornerstone of construct validity - if IRT and CTT measure the same latent construct (episodic memory ability), they should correlate highly and reach identical statistical conclusions despite different scaling (IRT: unbounded latent, CTT: 0-1 manifest). Divergence would indicate method-specific artifacts threatening construct validity of forgetting trajectory findings.

---

## Theoretical Background

**Relevant Theories:**
- **Classical Test Theory (CTT)**: Assumes true score = observed score - error. Mean scores aggregate item responses linearly. Simple, deterministic, but ignores item-level psychometrics (difficulty, discrimination).
- **Item Response Theory (IRT)**: Models latent ability probabilistically. GRM estimates person ability (theta) accounting for item difficulty (b) and discrimination (a). Nonlinear, more psychometrically sophisticated.
- **Convergent Validity (Campbell & Fiske, 1959)**: Multiple methods measuring same construct should correlate highly (r > 0.85-0.90). Low correlation signals method-specific variance or different constructs.

**Key Citations:**
- Hambleton & Swaminathan (1985): IRT vs CTT comparison - IRT superior for heterogeneous item difficulties, but both converge with good psychometric properties
- Nunnally & Bernstein (1994): CTT reliability and convergent validity standards
- Campbell & Fiske (1959): Multitrait-multimethod matrix for construct validation

**Theoretical Predictions:**
IRT and CTT should converge (r > 0.90) because both estimate same latent construct (episodic memory ability). Scaling differences expected (IRT unbounded, CTT 0-1), but slopes, interaction patterns, and statistical significance should agree. Divergence would suggest IRT item purification removed psychometrically problematic items that CTT retained (method-specific artifacts).

**Literature Gaps:**
Most IRT-CTT comparisons use cross-sectional data. Longitudinal trajectory modeling (LMM) with repeated measures tests whether IRT and CTT converge not just on static ability but also on dynamic forgetting patterns. This RQ extends convergent validity to time-domain analysis.

---

## Hypothesis

**Primary Hypothesis:**
Exploratory. IRT theta scores and CTT mean scores should converge (r > 0.90, agreement rate > 80% on LMM coefficient significance), demonstrating robustness of domain-specific forgetting trajectory conclusions to measurement approach.

**Secondary Hypotheses:**
1. Correlations will be high but not perfect (r = 0.90-0.95) due to IRT item purification removing extreme items that CTT retains
2. Agreement on statistical significance will exceed 80% for Domain × Time interaction terms
3. IRT model may show slightly better fit (lower AIC) due to psychometric optimization

**Theoretical Rationale:**
Both IRT and CTT estimate latent episodic memory ability, but via different assumptions. IRT is probabilistic and nonlinear, accounting for item-level difficulty and discrimination. CTT is deterministic and linear, treating all items equally. If underlying construct is real (not measurement artifact), both methods should reach same conclusions about forgetting trajectories. Convergence strengthens confidence in domain-specific forgetting findings (RQ 5.1). Divergence would indicate method-specific artifacts requiring careful interpretation.

**Expected Effect Pattern:**
High Pearson correlations (r > 0.90) between IRT and CTT scores for each domain. Parallel LMM analysis should show identical significance patterns for Time × Domain interactions (all p-values agree on <0.05 or >0.05). Effect sizes (beta coefficients) may differ in magnitude due to scaling differences, but signs and relative ordering should match. AIC comparison may favor IRT due to item purification, but ΔAIC < 10 suggests equivalent fit.

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
  - Disambiguation: **ALL Where tags included** for complete spatial coverage (matches RQ 5.1 domain definitions)

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ examines convergent validity across all three WWW episodic memory components. Domain-specific comparisons allow testing whether IRT-CTT convergence varies by memory type (e.g., What might show higher convergence due to simpler psychometric properties). Comprehensive coverage matches RQ 5.1 design for direct comparison.

**Exclusion Rationale:**
None - all WWW domains included to match RQ 5.1 analysis scope.

---

## Analysis Approach

**Analysis Type:**
Convergent validity comparison using Correlation Analysis + Parallel LMM (Linear Mixed Models) for IRT vs CTT ability estimates

**High-Level Workflow:**

**Step 0:** Get Data
- Load IRT theta scores from results/ch5/rq1/data/ (step03_theta_scores.csv or equivalent)
- Load TSVR mapping from results/ch5/rq1/data/step00_tsvr_mapping.csv (UID, Test, TSVR)
- Load raw VR item scores from data/cache/dfData.csv for CTT computation

**Step 1:** Data Preparation
- Extract IRT theta scores (Theta_What, Theta_Where, Theta_When) per UID × Test
- Compute CTT mean scores from raw data: Extract all TQ_ items per domain (What: -N-, Where: -L-/-U-/-D-, When: -O-), calculate mean score per UID × Test × Domain
- Merge IRT and CTT scores on UID, Test, Domain
- Merge TSVR data on UID, Test
- Reshape to long format for LMM (columns: UID, Test, Domain, TSVR, IRT_Score, CTT_Score)

**Step 2:** Correlation Analysis
- Compute Pearson correlations between IRT and CTT for each domain (What, Where, When) + overall
- Test if r > 0.90 (high convergence threshold)
- Report 95% confidence intervals and p-values
- Generate scatterplots: IRT (x-axis) vs CTT (y-axis) with regression lines, separate panels per domain

**Step 3:** Parallel LMM Comparison
- Fit identical LMMs for IRT and CTT: Ability ~ (Time + log(Time+1)) × Domain + (Time | UID)
- Extract Time × Domain interaction coefficients for both models
- Compare statistical significance patterns (p < 0.05 threshold)
- Calculate agreement rate: % of coefficients with matching significance (both sig or both nonsig)
- Compare effect size magnitudes (beta coefficients)

**Step 4:** Model Fit Comparison
- Compare AIC/BIC between IRT and CTT models
- Compute ΔAIC = AIC_CTT - AIC_IRT (negative = IRT better, positive = CTT better)
- If |ΔAIC| < 2: Equivalent fit. If |ΔAIC| > 10: Substantial difference.

**Step 5:** Visualization
- Generate comparison plot showing IRT vs CTT trajectories for each domain
- Three panels (What, Where, When) or overlaid lines with different styles (solid = IRT, dashed = CTT)
- Include observed means with 95% CIs and model-predicted lines for both approaches
- Scale CTT scores to match IRT range for visual comparison (optional, note if applied)

**Data Preprocessing (Per Solution Section 1.4):**
- **Accuracy Scores:** Already dichotomized in RQ 5.1 IRT pipeline (1 = 1, <1 = 0). For CTT, use same dichotomization rule for consistency.
- **Confidence Ratings:** Not used in this RQ (focuses on accuracy-based ability estimates only).
- **IRT Model:** GRM (from RQ 5.1), 2-pass purified item set. CTT uses same items for fair comparison (purified set only).
- **Likert Response Bias:** Not applicable (no confidence ratings analyzed).

**Special Methods:**
- **Paired Comparison Design:** IRT and CTT scores paired per observation (UID × Test × Domain) for within-subject correlation
- **Identical Model Specification:** LMMs use same formula for both IRT and CTT to isolate scaling differences from model structure differences
- **Scaling Note:** IRT (unbounded, typically -3 to +3) vs CTT (0-1) → Compare slopes/patterns, not raw values. May z-score both for visualization.
- **TSVR Time Variable:** Use actual hours since encoding (not nominal days) to match RQ 5.1 LMM specification

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.1 IRT outputs + raw data for CTT computation)

### DERIVED Data Source:

**Source RQ:**
RQ 5.1 (Domain-Specific Forgetting Trajectories)

**File Paths:**
- **IRT Scores:** `results/ch5/rq1/data/step03_theta_scores.csv` (or equivalent theta output file)
  - Columns: UID, Test, Domain, Theta (IRT ability estimates)
- **TSVR Mapping:** `results/ch5/rq1/data/step00_tsvr_mapping.csv`
  - Columns: UID, Test, TSVR (actual hours since encoding)
- **Raw Data for CTT:** `data/cache/dfData.csv` (master dataset)
  - Columns: UID, TEST, TQ_* (all VR item scores for domain-specific aggregation)

**Dependencies:**
RQ 5.1 must complete Steps 0-3 (TSVR extraction, IRT calibration Pass 1, purification, IRT calibration Pass 2, theta extraction) before this RQ can run. This RQ uses purified IRT theta scores and computes CTT scores from the same purified item set for fair comparison.

**Usage:**
This RQ uses IRT theta scores from RQ 5.1 as one measurement approach. CTT scores are computed fresh from raw data (dfData.csv) using domain-specific item aggregation. Both scores are merged for paired correlation and parallel LMM comparison.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.1 (inherited inclusion criteria - likely all 100 participants with valid VR data)

**Items:**
- [x] Purified IRT item set from RQ 5.1 (items passing difficulty |b| < 3.0 and discrimination a > 0.4 thresholds)
- Note: CTT scores computed from same purified item set to ensure fair comparison (not all raw TQ items)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) - inherited from RQ 5.1

---
