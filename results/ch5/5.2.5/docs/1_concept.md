# RQ 5.2.5: Does purified IRT item set change CTT conclusions?

**Chapter:** 5
**RQ Number:** 5.2.5
**Full ID:** 5.2.5

---

## Research Question

**Primary Question:**
If we compute CTT scores using only IRT-retained items (post-purification), do conclusions differ from full-item CTT?

**Scope:**
This RQ examines methodological convergence between Classical Test Theory (CTT) and Item Response Theory (IRT) approaches by comparing trajectory conclusions from: (a) full CTT (all items), (b) purified CTT (IRT-retained items only), and (c) IRT theta scores. Analysis uses the same participants × tests × domains structure as RQ 5.1, applying parallel LMM models to all three measurement approaches.

**Theoretical Framing:**
This RQ addresses fundamental psychometric questions about item selection and measurement precision. If IRT item purification removes noise (poorly discriminating items) rather than signal, then CTT scores computed from purified items should converge toward IRT conclusions while improving model fit. This tests the validity of IRT-based item selection and informs whether CTT analyses can benefit from IRT-informed item refinement.

---

## Theoretical Background

**Relevant Theories:**
- **Classical Test Theory (CTT):** Assumes all items contribute equally to total score (unit weighting). Measurement error assumed homogeneous across ability range. No item-level quality control beyond internal consistency.
- **Item Response Theory (IRT):** Models item-level difficulty and discrimination. Allows identification of psychometrically problematic items (extreme difficulty, low discrimination). Weights items by discrimination, providing more precise ability estimates.
- **Convergent Validity Theory:** Different measurement approaches targeting the same construct should yield similar conclusions. Divergence may indicate method artifacts or measurement error rather than true construct differences.

**Key Citations:**
- Lord (1980): IRT foundations and advantages over CTT for item selection
- McDonald (1999): Convergence between IRT and factor-analytic approaches when assumptions met
- Embretson & Reise (2000): Item purification as method for improving construct validity

**Theoretical Predictions:**
IRT purification should identify items with poor psychometric properties (e.g., very easy/hard items with b outside [-3, 3] or poorly discriminating items with a < 0.4-0.5). Removing these items from CTT computation should: (1) increase CTT-IRT correlation (reduced noise), (2) improve model fit (lower AIC), and (3) produce trajectory conclusions more similar to IRT. Full CTT may include measurement noise from problematic items, while purified CTT retains only high-quality items.

**Literature Gaps:**
Most studies compare IRT vs CTT in isolation. Few studies test whether CTT can benefit from IRT-informed item selection. This RQ fills gap by examining whether hybrid approach (CTT scoring on IRT-purified items) improves measurement quality and methodological convergence.

---

## Hypothesis

**Primary Hypothesis:**
Purified CTT (using only IRT-retained items) will show higher correlation with IRT theta scores compared to full CTT, demonstrating that item purification removes noise rather than signal.

**Secondary Hypotheses:**
1. Purified CTT will yield better model fit (lower AIC) than full CTT in parallel LMM analyses
2. Purified CTT trajectory conclusions (Domain × Time interactions) will match IRT conclusions more closely than full CTT
3. Correlation improvement will be modest (Δr ~ 0.02) because CTT equal weighting vs IRT discrimination weighting still introduces some divergence

**Theoretical Rationale:**
Item purification identifies and removes items with extreme difficulty (|b| > 3) or poor discrimination (a < 0.4-0.5). These items contribute measurement error to CTT total scores: extreme items provide little information across ability range, and low-discrimination items fail to distinguish between high/low ability participants. Removing these items reduces noise in CTT scores, improving construct validity and convergence with IRT (which naturally down-weights problematic items via discrimination parameter).

**Expected Effect Pattern:**
- Correlation: Full CTT-IRT r ≈ 0.95; Purified CTT-IRT r ≈ 0.97 (Δr ≈ +0.02)
- Model fit: Purified CTT AIC < Full CTT AIC (ΔAIC ≈ -30 to -40, substantial improvement)
- Trajectory slopes: Purified CTT Domain × Time interactions should match IRT more closely than full CTT
- Residual divergence: Purified CTT still slightly worse fit than IRT (ΔAIC ≈ +10-15) due to equal weighting vs discrimination weighting

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
  - Disambiguation: **ALL Where tags included** (full coverage from RQ 5.2.1)

- [ ] **When** (Temporal Order) - **EXCLUDED**
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ examines What and Where domains to test whether IRT item purification improves CTT-IRT convergence. These two domains have adequate psychometric properties for trajectory analysis.

**Exclusion Rationale:**
**When domain excluded due to floor effect discovered in RQ 5.2.1:**
- 77% item attrition after IRT purification (only 4 of 18 items retained)
- 6-9% floor effect (participants at chance level)
- Insufficient item count for reliable CTT computation
- All Type 5.2.x RQs exclude When to maintain consistency

---

## Analysis Approach

**Analysis Type:**
Methodological comparison - CTT vs IRT convergence testing using correlation analysis and parallel LMM model fitting

**High-Level Workflow:**

**Step 0:** Get Data
- Load IRT item parameters and theta scores from results/ch5/5.2.1/
- Load TSVR mapping from results/ch5/5.2.1/data/step00_tsvr_mapping.csv
- Load raw scores from data/cache/dfData.csv for CTT computation

**Step 1:** Identify IRT-Retained Items
- Load IRT item parameters (difficulty b and discrimination a from RQ 5.2.1 purification)
- For each domain (What/Where only - When excluded): identify items with acceptable discrimination (0.5 ≤ a ≤ 4.0)
- Create list of retained items (union across What and Where factors)
- Document counts: retained vs removed items per domain

**Step 2:** Compute Full CTT Scores
- Extract all TQ_ items from raw data (dfData.csv)
- Group items by domain (What: -N-, Where: -U-/-D-) - **When (-O-) excluded**
- Calculate mean scores per UID × Test × Domain using ALL items (full CTT)

**Step 3:** Compute Purified CTT Scores
- Filter to only IRT-retained items identified in Step 1
- Calculate mean scores per UID × Test × Domain using retained items only
- Compare item counts: Full vs Purified per domain

**Step 3b:** CTT Reliability Assessment
- Compute Cronbach's alpha for full and purified CTT item sets per domain (What/Where only)
- Use `tools.analysis_ctt.compute_cronbachs_alpha()` with bootstrap 95% confidence intervals
- Report alpha with CIs for both item sets per domain
- **Interpretation:**
  - If alpha increases or remains stable (within 95% CI) after purification → validates that IRT item selection improved/maintained CTT reliability
  - If alpha decreases → suggests removed items contained meaningful variance from CTT perspective, requiring discussion of CTT-IRT framework differences
- Compare: alpha_full_What vs alpha_purified_What (repeat for Where)

**Step 4:** Correlation Analysis
- Correlate Purified CTT with IRT theta (expect r > Full CTT-IRT correlation)
- Correlate Purified CTT with Full CTT (expect high r but some divergence)
- Correlate Full CTT with IRT theta (baseline convergence)
- **Test statistical significance** of correlation differences using **Steiger's z-test for dependent correlations** (Steiger 1980, *Psychological Bulletin*, 87, 245-251)
  - Implement via `tools.analysis_ctt.compare_correlations_dependent()` computing asymptotic covariance of overlapping correlations
  - Test H0: r(Full CTT, IRT) = r(Purified CTT, IRT) using all three pairwise correlations
  - **Rationale:** Full CTT, Purified CTT, and IRT theta are from same N=100 participants (dependent correlations), so Fisher's r-to-z (which assumes independent samples) is invalid

**Step 5:** Parallel LMM Comparison

**Step 5a:** Standardize Outcomes for Valid AIC Comparison
- **Critical:** AIC comparison across different outcome scales (Full CTT [0,1], Purified CTT [0,1], IRT theta [logit scale]) violates identical-data requirement
- **Solution:** Standardize all three measurements to z-scores before LMM fitting
  - Within each UID × Test × Domain cell: z = (score - mean) / SD
  - Ensures comparable scales across all three measurement approaches
  - Preserves relative differences while enabling valid AIC comparison per Burnham & Anderson

**Step 5b:** Fit Parallel LMMs to Standardized Outcomes
- Fit identical LMMs for three standardized measurement approaches: (a) Full CTT (z-scored), (b) Purified CTT (z-scored), (c) IRT theta (z-scored)
- Formula: z_Ability ~ (Time + log(Time+1)) × Domain + (Time | UID)
- Compare AIC on standardized outcomes (now valid comparison)
- Compare coefficients: Does purified CTT Domain × Time interaction match IRT conclusions?
- **Interpret AIC differences** using Burnham & Anderson thresholds: ΔAIC < 2 = equivalent, ΔAIC 2-10 = moderate support, ΔAIC > 10 = substantial support

**Step 6:** Visualization
- Generate comparison plot showing all three trajectories (Full CTT, Purified CTT, IRT) per domain
- Highlight convergence of Purified CTT toward IRT
- Include observed means with 95% CIs and model-predicted lines

**Data Preprocessing (Per Solution Section 1.4):**
- **Accuracy Scores:** Already dichotomized in dfData.csv (CTT uses these dichotomized values)
- **CTT Computation:** Simple mean of dichotomized items per domain (no weighting)
- **IRT Theta:** Pre-computed from RQ 5.1 (discrimination-weighted ability estimates)
- **Time Variable:** TSVR (actual hours since encoding) from RQ 5.1 mapping

**Special Methods:**
- **Parallel LMM Design:** Identical model formula applied to all three measurement approaches (Full CTT, Purified CTT, IRT) to isolate measurement method effects
- **IRT-Informed CTT:** Hybrid approach - CTT scoring on IRT-purified items tests whether CTT can benefit from IRT item selection
- **Convergent Validity Testing:** Correlation and AIC comparison quantify degree of methodological convergence

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.1 outputs + raw data for CTT computation)

### DERIVED Data Source:

**Source RQ:**
RQ 5.1 (Domain-Specific Forgetting Trajectories)

**File Paths:**
- **IRT Item Parameters:** `results/ch5/5.2.1/data/step02_purified_items.csv` (item list with discrimination a and difficulty b estimates post-purification)
- **IRT Theta Scores:** `results/ch5/5.2.1/data/step03_theta_scores.csv` (ability estimates per UID × Test × Domain)
- **TSVR Mapping:** `results/ch5/5.2.1/data/step00_tsvr_mapping.csv` (UID × Test → TSVR hours)
- **Raw Data for CTT:** `data/cache/dfData.csv` (dichotomized TQ_ item responses for CTT scoring)

**Dependencies:**
RQ 5.1 must complete Steps 0-4 (IRT calibration, purification, theta extraction) before this RQ can run. This RQ uses RQ 5.1 purification criteria (0.5 ≤ a ≤ 4.0) to identify retained items for purified CTT computation.

**Usage:**
- IRT item parameters identify which items to retain vs exclude for purified CTT
- IRT theta scores serve as gold standard for convergent validity testing
- TSVR mapping ensures consistent time variable across all three measurement approaches
- Raw data (dfData.csv) required for CTT computation (IRT analysis consumed/transformed this data)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.1 (inherited inclusion criteria)
- Note: Same N as RQ 5.1 ensures direct comparability

**Items:**
- [x] Full CTT: All TQ_ items (What: -N-, Where: -U-/-D-) - **When (-O-) excluded**
- [x] Purified CTT: Only items retained by RQ 5.2.1 purification (0.5 ≤ a ≤ 4.0)
- Expected counts (What/Where only):
  - Full CTT: ~18 What, ~18 Where (~36 total)
  - Purified CTT: ~14 What, ~14 Where (~28 total, ~8 removed)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Note: Same test structure as RQ 5.1 (Time variable uses TSVR, not nominal days)

---
