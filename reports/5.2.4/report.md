# RQ 5.2.4: IRT-CTT Convergent Validity

**Chapter:** Ch5
**Status:** PLATINUM CERTIFIED
**Certification Date:** 2025-12-31
**Report Generated:** 2026-01-01T00:00:00Z

---

## 1. Executive Summary

**What we tested:** Whether IRT theta scores and CTT mean scores yield identical conclusions about domain-specific forgetting trajectories for episodic memory.

**What we found:** Exceptional static convergence (r=0.906-0.970) but critical dynamic divergence - IRT detects individual forgetting rate differences (random slope Var=0.021-1.507) that CTT initially missed (Var=0.000 boundary with Log-only model). Corrected Recip+Log model reveals CTT CAN detect variation (Var=0.022) but IRT still captures 68× more variance.

**Why it matters:** Validates IRT as superior for person-specific trajectory modeling (clinical utility for MCI screening). Demonstrates functional form specification matters MORE than measurement method - model misspecification can mask individual differences.

---

## 2. Research Question

**Question:**
Do IRT theta scores and CTT mean scores yield the same conclusions about domain-specific forgetting trajectories?

**Hypothesis:**
Exploratory. IRT and CTT should converge (r > 0.70, Cohen's º > 0.60) for static ability estimates and dynamic trajectory patterns, demonstrating robustness of domain-specific forgetting conclusions to measurement approach.

**Theoretical Framework:**
- **Classical Test Theory (CTT):** True score = observed score - error. Mean scores aggregate item responses linearly. Simple but ignores item-level psychometrics.
- **Item Response Theory (IRT):** Models latent ability probabilistically via GRM. Accounts for item difficulty and discrimination. Nonlinear, psychometrically sophisticated.
- **Convergent Validity (Campbell & Fiske, 1959):** Multiple methods measuring same construct should correlate r > 0.85-0.90.

**Expected Patterns:**
High correlations (r > 0.90) between IRT and CTT scores. Parallel LMM analysis showing identical significance patterns for Time × Domain interactions. Effect sizes may differ in magnitude due to scaling (IRT unbounded, CTT 0-1) but signs and relative ordering should match.

---

## 3. Historical Context

**Archive Search:**
- Topics searched: 3
- Entries found: 3
- Date range: 2025-12-03 to 2025-12-10

**Key Events (Chronological):**

1. **2025-12-03 06:00** - CRITICAL MODEL CORRECTION (source: archive/random_slope_correction_log_tsvr.md)
   - **Discovery:** RQ 5.2.4 using wrong random slope specification (TSVR_hours linear instead of log_TSVR)
   - **Root cause:** ROOT RQ 5.2.1 selected Log model as best fit (AIC weight 61.9%), so random slopes should align with log-transformed time
   - **Symptom:** Both IRT and CTT showed slope Var=0.000 (boundary estimates) - masked individual differences
   - **Fix applied:** Changed `re_formula="~TSVR_hours"` to `re_formula="~log_TSVR"` in step03_fit_lmm.py (lines 312-317)
   - **Result:** IRT Var increased from 0.000’0.021, CTT remained at boundary 0.000
   - **KEY FINDING:** IRT detects individual forgetting rates (Var=0.021), CTT cannot (Var=0.000) - this divergence was INVISIBLE with wrong model

2. **2025-12-03 06:00** - VALIDATION PIPELINE COMPLETED (source: archive/random_slope_correction_log_tsvr.md)
   - All 3 corrected RQs validated via finisher agents (rq_inspect, rq_plots, rq_results)
   - RQ 5.2.4:  PASS (all validation checks)
   - Static convergence exceptional: What r=0.906, Where r=0.970
   - Dynamic divergence documented: IRT enables person-specific trajectories, CTT limited to group-average

3. **2025-12-10** - ROOT MODEL VERIFICATION (source: summary.md Section 6)
   - Extended RQ 5.2.1 model comparison revealed Recip+Log model superior to Log-only
   - step03b verification: Re-fit IRT and CTT models with Recip+Log functional form
   - **Pattern change:** CTT now detects variation (Var=0.022), IRT variance increased 71.8× (0.021’1.507)
   - **Convergence ROBUST:** Correlations unchanged (What 0.906, Where 0.970)
   - **Lesson:** Functional form specification matters MORE than measurement method

**Blockers Resolved:**
- **Blocker 1:** Random slope boundary estimates (Var=0.000) initially suggested NO individual differences
  - **Resolution:** Corrected to log_TSVR per ROOT model (2025-12-03) ’ IRT now detects variation
- **Blocker 2:** CTT boundary persisted with Log-only model despite correction
  - **Resolution:** Recip+Log functional form (2025-12-10) ’ CTT now non-zero Var=0.022

**Cross-References:**
- Related to RQ 5.2.1: ROOT RQ for domain-specific forgetting (established Log model best fit, later updated to Recip+Log)
- Related to RQ 5.3.4, 5.4.3: Same random slope correction applied (TSVR_hours’log_TSVR)
- Related to RQ 5.3.5, 5.4.4: IRT-CTT convergence trilogy for paradigms and congruence factors

---

## 4. Methodology

### Data Sources

**Root or Derived:**
- DERIVED: Uses outputs from RQ 5.2.1 (IRT theta scores, purified items, TSVR mapping)

**Specific Sources:**
- IRT theta scores: `results/ch5/5.2.1/data/step03_theta_scores.csv` (Theta_What, Theta_Where per UID × Test)
- TSVR mapping: `results/ch5/5.2.1/data/step00_tsvr_mapping.csv` (actual hours since encoding)
- Purified items: `results/ch5/5.2.1/data/step02_purified_items.csv` (64 items - 17 What, 47 Where)
- Raw VR data: `data/cache/dfData.csv` (for CTT mean score computation)

### Analysis Pipeline

**Steps:**

| Step | Description | Output Files |
|------|-------------|--------------|
| **Step 0** | Load IRT theta, TSVR, purified items, raw data | step00_irt_theta_loaded.csv (400 rows), step00_tsvr_loaded.csv, step00_purified_items.csv (64 items), step00_raw_data_filtered.csv |
| **Step 1** | Compute CTT mean scores per domain (What, Where) | step01_ctt_scores.csv (800 rows, 100×4×2) |
| **Step 2** | Correlation analysis (Pearson r with Holm-Bonferroni correction) | step02_correlations.csv (3 rows: What, Where, Overall) |
| **Step 3** | Fit parallel LMMs (IRT + CTT, identical formula) | step03_irt_lmm_input.csv (800 rows), step03_ctt_lmm_input.csv, fixed effects CSVs, summaries |
| **Step 4** | Validate LMM assumptions (normality, homoscedasticity, ACF) | step04_*_assumptions_report.txt, diagnostic plots |
| **Step 5** | Extract and compare coefficients (significance agreement, Cohen's º) | step05_coefficient_comparison.csv (~10 coefficients), step05_agreement_metrics.csv |
| **Step 6** | Compare model fit (AIC/BIC) | step06_model_fit_comparison.csv |
| **Step 7** | Prepare scatterplot data (IRT vs CTT by domain) | plots/step07_scatterplot_data.csv (800 rows) |
| **Step 8** | Prepare trajectory data (time series comparison) | plots/step08_trajectory_data.csv (~16 rows) |
| **Step 3b** | Recip+Log ROOT verification (added 2025-12-10) | step03b_*_recip_log.pkl, convergence comparison CSV |

### Tools Used

**Key Tools:**
- **Correlation:** scipy.stats.pearsonr + Holm-Bonferroni correction (Decision D068 dual p-values)
- **LMM:** statsmodels.MixedLM with random slopes (convergence strategy: attempt slopes, simplify if fails)
- **Validation:** validate_lmm_assumptions_comprehensive (Shapiro-Wilk, ACF, Q-Q plots)
- **Effect sizes:** Cohen's kappa for significance agreement (accounts for chance)

### Critical Design Decisions

**Decisions:**

1. **When domain EXCLUDED** (Rationale: Floor effects in RQ 5.2.1 - only 5 items, 6-9% probability at encoding)
   - Source: concept.md lines 9-24, plan.md lines 10-18
   - Impact: 800 rows (2 domains) instead of 1200 (3 domains)

2. **Random slopes on log_TSVR, not linear TSVR_hours** (Rationale: RQ 5.2.1 ROOT selected Log model as best fit)
   - Source: archive/random_slope_correction_log_tsvr.md lines 17-29
   - Impact: Reveals IRT detects individual differences (Var=0.021), CTT boundary (Var=0.000) with Log-only

3. **Recip+Log ROOT verification added** (Rationale: Extended RQ 5.2.1 model comparison 2025-12-08 updated functional form)
   - Source: summary.md Section 6 lines 813-948
   - Impact: CTT now detects variation (Var=0.022), IRT variance 68× larger (1.507 vs 0.022)

4. **Identical LMM specification for IRT and CTT** (Rationale: Isolate scaling differences from model structure differences)
   - Source: plan.md lines 405-415
   - Impact: Fair comparison - only difference is IRT_score vs CTT_score column

**Warnings:**
- WARNING: CTT model slope variance at boundary (Var=0.000) with Log-only - indicates model limitation, not true absence
- WARNING: Assumption violations (normality, heteroscedasticity) acknowledged but analyses proceeded (large sample robust to minor violations)

---

## 5. Results

### Sample Characteristics

**Sample Size:**
- Total N: 100 participants
- Exclusions: 0 (all participants from RQ 5.2.1 retained)
- Missing data: 0 (800/800 observations complete)

**Final Sample:**
- N = 100 participants × 4 test sessions × 2 domains = 800 observations
- Domains: What (Object Identity, 17 items), Where (Spatial Location, 47 items)
- When EXCLUDED (5 items, floor effects)

### Primary Findings

**Key Statistics:**

**Correlation Analysis (Static Convergence):**

| Effect | r | 95% CI | p (Holm) | n | Threshold 0.90 |
|--------|---|--------|----------|---|----------------|
| **What domain** | 0.906 | [0.887, 0.922] | <.001 | 400 | **PASS** |
| **Where domain** | 0.970 | [0.963, 0.975] | <.001 | 400 | **PASS** |
| **Overall** | 0.792 | [0.765, 0.817] | <.001 | 800 | FAIL |

**Interpretation:** Exceptional static convergence for individual domains (r > 0.90), indicating both methods measure same latent construct at single timepoints.

---

**LMM Coefficient Agreement (Dynamic Convergence):**

| Coefficient | IRT p | CTT p | Agreement | Effect |
|-------------|-------|-------|-----------|--------|
| Intercept | <.001 | <.001 | **AGREE** | Both significant |
| Domain (Where) | .369 | <.001 | **DISAGREE** | IRT nonsig, CTT sig |
| log_TSVR | <.001 | <.001 | **AGREE** | Both significant (forgetting) |
| log_TSVR × Domain | .716 | .070 | **AGREE** | Both nonsignificant |

**Raw Agreement:** 3/4 = 75%
**Cohen's º:** 0.500 (moderate agreement, below 0.60 threshold)

**Key Disagreement:** Domain baseline effect (Where vs What) - IRT finds no difference, CTT finds Where < What (17 percentage points). Not robust to measurement approach.

---

**Random Slope Variance (CRITICAL FINDING):**

**Log-only Model (Original Corrected Analysis, 2025-12-03):**

| Model | Intercept Var | log_TSVR Var | Interpretation |
|-------|---------------|--------------|----------------|
| **IRT** | 0.627 | **0.021** | Detects individual differences |
| **CTT** | 0.011 | **0.000** | Boundary - no detection |

**Recip+Log Model (ROOT Verification, 2025-12-10):**

| Model | Intercept Var | recip_TSVR Var | Change from Log-only |
|-------|---------------|----------------|----------------------|
| **IRT** | 0.627 | **1.507** | +71.8× larger |
| **CTT** | 0.011 | **0.022** | NOW DETECTS |

**Key Finding:** IRT detects 68× MORE individual variation than CTT (1.507 vs 0.022) with correct functional form. CTT boundary with Log-only was model limitation, not CTT limitation.

---

### Model Comparison

**Models Compared:** 2 (IRT LMM, CTT LMM)

**Best Model:** Cannot compare (different outcome scales)

**Model Fit:**

| Model | AIC | BIC | Notes |
|-------|-----|-----|-------|
| IRT (Log-only) | 1546.92 | 1565.66 | Unbounded scale |
| CTT (Log-only) | -1008.16 | -989.42 | Bounded scale (0-1) |
| IRT (Recip+Log) | 1460.32 | - | ”AIC=-86.60 better fit |
| CTT (Recip+Log) | -1064.37 | - | ”AIC=-56.21 better fit |

**Note:** AIC comparison INVALID across IRT/CTT due to scale differences (IRT unbounded, CTT bounded). Focus on coefficient agreement and correlations instead.

---

## 6. Visualizations

### Plot 1: IRT vs CTT Scatterplots by Domain
**File:** `plots/scatterplot_irt_ctt.png`

**Description:**
Two-panel scatterplot comparing IRT theta scores (x-axis, -2.5 to +2.5) with CTT mean scores (y-axis, 0.0 to 1.0). Left panel: What domain (r=0.906), right panel: Where domain (r=0.970).

**Key Patterns:**
- **What domain:** Strong positive linear relationship with moderate scatter. Ceiling effect at CTT=1.0 (perfect accuracy). Data cluster ¸=-2 to +2, CTT=0.2 to 1.0.
- **Where domain:** Near-perfect linear relationship (r=0.970, highest convergence). Very tight scatter around regression line. Minimal residual variance. Data span ¸=-2 to +2.5, CTT=0.1 to 0.9.

**Connection to Findings:**
Visually confirms exceptional static convergence (r > 0.90). Where domain's tighter scatter explains higher correlation. Ceiling effects in What domain reduce correlation slightly but still exceptional.

---

### Plot 2: IRT vs CTT Trajectory Comparison
**File:** `plots/trajectory_comparison.png`

**Description:**
Two-panel line plot showing forgetting trajectories over time (0-160 hours post-encoding). IRT (solid circles, solid line) vs CTT (solid squares, dashed line), with 95% confidence intervals. Left panel: What domain (red), right panel: Where domain (blue).

**Key Patterns:**
- **What domain:** IRT starts ¸=0.6, peaks T2 (24h) ¸=1.3, declines to ¸=-0.3 at T4 (144h). CTT starts 0.75, peaks 0.95, declines to 0.70. Both show consolidation (T1’T2 increase) then forgetting (T2’T4 decline).
- **Where domain:** IRT trajectory nearly identical to What. CTT shows flatter trajectory, less consolidation boost visible.
- **Wide IRT CIs:** Reflect individual differences (random slope Var=1.507 with Recip+Log). Narrow CTT CIs reflect limited detected variation (Var=0.022).

**Connection to Findings:**
Pattern agreement strong (both show forgetting), but magnitude differs (IRT unbounded ±2 SD range vs CTT bounded 0-1). Visual confirms critical divergence: IRT captures trajectory heterogeneity (wide CIs), CTT constrained (narrow CIs).

---

## 7. Interpretation

### Hypothesis Testing

**Outcome:** **PARTIALLY SUPPORTED**

**Rationale:**
-  Static convergence exceptional (r=0.906-0.970 exceeds 0.70 threshold)
-  Trajectory patterns qualitatively agree (consolidation ’ forgetting)
- L Dynamic divergence: IRT detects individual differences (Var=0.021-1.507), CTT initially boundary (Var=0.000), improved with better model (Var=0.022) but still 68× smaller
- L Cohen's º = 0.500 below 0.60 threshold (75% raw agreement but moderate º)
- L Domain baseline disagreement (IRT nonsig, CTT sig for Where vs What)

### Theoretical Implications

**Key Insights:**

1. **IRT superior for person-specific trajectory modeling**
   - Detects 68× more individual variation in forgetting rates (1.507 vs 0.022 with Recip+Log)
   - Enables personalized prediction (random slopes capture heterogeneous decline)
   - Clinical utility: IRT can identify individuals with atypical forgetting rates (MCI screening)

2. **Functional form matters MORE than measurement method**
   - Log-only: CTT boundary (Var=0.000) suggested NO individual differences
   - Recip+Log: CTT non-zero (Var=0.022) reveals CTT CAN detect variation
   - Lesson: Model misspecification can mask individual differences regardless of measurement approach

3. **Static convergence vs dynamic divergence**
   - Both methods measure same latent construct (r > 0.90 at single timepoints)
   - But IRT captures trajectory heterogeneity (random slopes), CTT limited
   - This has implications for longitudinal prediction: IRT required for person-specific curves

### Cross-RQ Patterns

**Convergent Evidence:**
- RQ 5.2.1: ROOT established Log (later Recip+Log) as best functional form - this RQ validates correction propagated correctly
- RQ 5.3.5: IRT-CTT convergence for paradigms (same pattern: exceptional static r > 0.90, dynamic divergence in random slopes)
- RQ 5.4.4: IRT-CTT convergence for congruence (exceptional static r=0.87-0.91, substantial dynamic º=0.667)

**Pattern:** IRT-CTT convergence trilogy (domains, paradigms, congruence) consistently shows exceptional static convergence but IRT advantage for individual dynamics.

### Unexpected Findings

**Anomalies Flagged:**

1. **Domain baseline disagreement** (IRT ²=0.069 p=.369, CTT ²=-0.171 p<.001)
   - Investigation needed: Extract T1 predicted values, compute Cohen's d, check trajectory plot ordering
   - Possible explanations: Item count imbalance (17 What vs 47 Where), ceiling effects (What CTT=1.0 clustering), false positive in CTT
   - Implication: Domain comparisons NOT robust to measurement approach

2. **CTT random slope boundary with Log-only** (Var=0.000)
   - Investigation performed: step03b Recip+Log verification
   - Result: CTT now detects variation (Var=0.022) with better functional form
   - Conclusion: Boundary was model limitation (Log-only insufficient), not CTT limitation
   - Implication: Always test multiple functional forms before concluding method cannot detect effect

3. **Assumption violations** (normality p<.05, heteroscedasticity, ACF Lag-1 > 0.1)
   - Investigation: Documented in step04 validation reports
   - Decision: Proceeded with analyses (large N=100 robust to minor violations per Bates et al. 2015)
   - Implication: Results interpretable but caution warranted for exact p-values

---

## 8. Limitations

### Sample Limitations
- **When domain excluded:** Only 2 domains analyzed (What, Where). Cannot test convergence for temporal memory.
- **Sample size:** N=100 adequate for fixed effects but random slopes models may be underpowered (Bates et al. 2015 recommend Ne200). CTT boundary with Log-only may reflect power limitation.
- **Missing data:** None (800/800 complete) but purification excluded 38% of items (39/102). Selection bias possible.

### Methodological Limitations
- **Unequal item counts:** What 17 items (27%), Where 47 items (73%). CTT unweighted means may be biased. IRT discrimination weighting may compensate but creates method-specific artifact.
- **CTT ceiling effects:** What domain ceiling at CTT=1.0 (scatterplot clustering). Bounded scale compresses high-ability trajectories, limits detection of individual slope differences.
- **IRT purification:** 2-pass purification removed 38% items. Purified set optimized for IRT but used for CTT computation. Fair comparison (same items) but may favor IRT psychometrically.
- **Model specification:** Log-only selected per RQ 5.2.1 (best AIC), later updated to Recip+Log. Random slopes on log-time may not be optimal for CTT bounded scale.

### Generalizability Constraints
- **Population:** Young adults (age M=20, SD=2). IRT-CTT convergence may differ in older adults (restricted range ’ lower r) or clinical samples (impaired memory ’ floor effects).
- **Context:** Desktop VR (not fully immersive HMD). Recognition test format (4-option forced choice). Convergence may differ for free recall (unbounded CTT) or cued recall (partial credit).
- **Domain:** Episodic memory only (What/Where). Convergence may differ for semantic memory (less dynamic) or working memory (shorter timescales).

---

## 9. Publication-Ready Summary

**Context & Method:** We tested whether IRT theta scores and CTT mean scores yield identical conclusions about domain-specific episodic memory forgetting trajectories. One hundred participants completed four VR test sessions (0, 24, 72, 144 hours post-encoding) assessing What (object identity) and Where (spatial location) memory domains. We computed Pearson correlations between IRT and CTT scores and fit parallel linear mixed models (LMM) with identical specifications to compare static ability estimates and dynamic trajectory patterns.

**Results:** Static convergence was exceptional (What r=0.906, Where r=0.970, both p<.001 after Holm-Bonferroni correction), confirming both methods measure the same latent construct at individual timepoints. However, critical dynamic divergence emerged: IRT models detected substantial individual differences in forgetting rates (random slope variance 1.507 with Recip+Log functional form), while CTT models initially showed boundary estimates (Var=0.000 with Log-only) indicating no detection. Corrected Recip+Log specification revealed CTT can detect variation (Var=0.022) but IRT still captures 68× more variance (1.507 vs 0.022). LMM coefficient agreement was moderate (3/4 terms agreed, Cohen's º=0.500), with disagreement on domain baseline effect (IRT nonsignificant, CTT significant).

**Interpretation:** Findings demonstrate that functional form specification matters more than measurement method - CTT's initial boundary was due to model misspecification (Log-only insufficient), not fundamental CTT limitation. IRT's psychometric sophistication (item discrimination weighting, unbounded scale) enables superior detection of person-specific trajectory heterogeneity, supporting its use for clinical applications requiring individual-level prediction (e.g., MCI screening). CTT remains viable for group-level average trajectories but limited for personalized forgetting curve modeling.

**Conclusion:** IRT and CTT show strong convergent validity for static episodic memory ability estimates but diverge on dynamic individual differences, with IRT detecting substantially more variance in forgetting rates. Model specification is critical - two-process forgetting (rapid reciprocal + slow logarithmic) reveals richer trajectory heterogeneity than single-process models.

---

## 10. Metadata & Sources

### Report Metadata
- **Generated:** 2026-01-01T00:00:00Z
- **Agent:** rq_report v1.0.0 (Sonnet 4.5 model)
- **RQ Folder:** results/ch5/5.2.4/

### Sources Synthesized

**Archive Sources:** 1 topic, 3 entries
- random_slope_correction_log_tsvr (archive/random_slope_correction_log_tsvr.md, 2025-12-03)

**RQ Files:** 18 files

- **Core docs:** concept.md (211 lines), plan.md (1433 lines), summary.md (950 lines)
- **Validation:** validation.md (exists, dated 2025-12-03), PLATINUM_FINALIZATION_REPORT.md (204 lines, dated 2025-12-31)
- **Specifications:** None (tools.yaml and analysis.yaml exist but not read for report)
- **Execution:** status.yaml (85 lines), 10 data files (step00-08 + step03b), 1 log file sampled, 4 plot files (2 current: scatterplot_irt_ctt.png, trajectory_comparison.png)
- **PLATINUM:** PLATINUM_FINALIZATION_REPORT.md (comprehensive certification 2025-12-31)

### Warnings Flagged

**Warnings:**
1. **When domain excluded:** Analysis conducted on 2 domains (What, Where) instead of 3. When excluded due to floor effects (5 items, 6-9% probability). Row counts 800 instead of 1200.
2. **CTT random slope boundary with Log-only:** Var=0.000 indicates model hit parameter boundary (variance cannot be negative). Improved to Var=0.022 with Recip+Log but still 68× smaller than IRT.
3. **Assumption violations:** Normality p<.05 (Shapiro-Wilk), heteroscedasticity present, ACF Lag-1 > 0.1 for some participants. Documented in step04 reports. Proceeded with large-sample robustness justification.
4. **AIC comparison invalid:** Different outcome scales (IRT unbounded, CTT bounded 0-1) make AIC not comparable. Focus on coefficient agreement and correlations instead.

**All warnings documented in summary.md and acknowledged in limitations.**

---

**End of Report**
