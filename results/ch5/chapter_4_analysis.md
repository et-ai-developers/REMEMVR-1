# Chapter 4: Statistical Analysis

## 4.1 Overview of Analytic Strategy

[TBD: 200-300 words explaining multi-stage analysis pipeline, why IRT+LMM, dealing with repeated measures]

---

## 4.2 Item Response Theory (IRT) Calibration

### 4.2.1 Graded Response Model (GRM)

[TBD: Model specification, estimation method, convergence criteria, output]

### 4.2.2 Item Purification Protocol (Decision D039)

**Rationale:** Psychometric quality control. Items with poor discrimination (a < 0.4) or extreme difficulty (|b| > 3.0) reduce measurement precision and may not generalize beyond this sample.

**Criteria:**
- Discrimination parameter: a ≥ 0.4 (items must differentiate between high/low ability participants)
- Difficulty parameter: |b| ≤ 3.0 (items must be neither too easy nor too hard for this sample)

**Two-Pass Calibration Procedure:**

*Pass 1:* Calibrate GRM on all items (omnibus or domain-specific factor structure). Flag items violating quality thresholds.

*Pass 2:* Re-calibrate GRM on purified item set (excluded items removed). Final theta estimates derived from Pass 2 only.

**Retention Rate Expectations:** Typical IRT purification retains 40-70% of items. Lower retention (<40%) signals measurement issues requiring item redesign. Higher retention (>70%) suggests well-designed assessment.

**Statistical Justification:** Purification improves theta estimate reliability by removing noisy items. Trade-off: Narrower content coverage for higher precision.

### 4.2.3 Dimensionality Considerations

[TBD: Omnibus vs domain-specific factors, justification for different RQ approaches]

---

## 4.3 Linear Mixed Models (LMM)

### 4.3.1 Model Specification

[TBD: Fixed effects, random effects, rationale, estimation methods]

### 4.3.2 Model Comparison Procedures

**Information Criteria:** Akaike Information Criterion (AIC) = -2×log(likelihood) + 2×k, where k = number of parameters. Lower AIC indicates better fit penalized for complexity.

**Delta AIC Interpretation (Burnham & Anderson, 2004):**
- ΔAIC < 2: Models essentially equivalent (competitive)
- ΔAIC 2-10: Weak support for worse model (may retain for theoretical reasons)
- ΔAIC > 10: Essentially no support for worse model (reject)

**Akaike Weights:** Relative probability each model is best in candidate set. Weight = exp(-0.5×ΔAIC) / Σ[exp(-0.5×ΔAIC)] across all models. Interpretation:
- Weight > 0.90: Strong evidence (single best model)
- Weight 0.60-0.90: Moderate evidence (clear favorite)
- Weight 0.30-0.60: Weak evidence (consider model averaging)
- Weight < 0.30: Poor model (multiple alternatives better)

**Model Averaging:** When no single model has weight > 0.90, compute weighted predictions across top models (cumulative weight ≥ 0.95). Reduces model selection bias.

**Estimation Note:** REML=False required for valid AIC comparison across models with different fixed effects. REML=True used for final parameter estimation after model selection.

### 4.3.3 Assumption Checking

[TBD: Normality, homoscedasticity, independence, multicollinearity, convergence diagnostics]

---

## 4.4 Effect Size Reporting

### 4.4.1 Standardized Effect Sizes

**Cohen's d:** Standardized mean difference = (M₁ - M₂) / SD_pooled

Interpretation (Cohen, 1988):
- Small: d = 0.2 (means differ by 0.2 SD)
- Medium: d = 0.5 (means differ by 0.5 SD)
- Large: d = 0.8 (means differ by 0.8 SD)

**Cohen's f²:** Effect size for regression = R² / (1 - R²)

Interpretation:
- Small: f² = 0.02 (2% variance explained)
- Medium: f² = 0.15 (15% variance explained)
- Large: f² = 0.35 (35% variance explained)

**Partial η²:** Effect size for ANOVA = SS_effect / (SS_effect + SS_error)

Interpretation:
- Small: η² = 0.01 (1% variance explained)
- Medium: η² = 0.06 (6% variance explained)
- Large: η² = 0.14 (14% variance explained)

### 4.4.2 LMM-Specific Effect Sizes

[TBD: ICC, marginal R², conditional R²]

---

## 4.5 Multiple Comparisons Corrections

### 4.5.1 Bonferroni Correction (Decision D068)

**Applied when:** Multiple pairwise comparisons within single RQ (e.g., comparing 3 memory domains = 3 pairwise tests).

**Method:** Adjusted significance threshold = α / k, where k = number of comparisons. For α = 0.05 and k = 3 comparisons: α_adj = 0.05 / 3 = 0.0167.

**Dual Reporting:** Per Decision D068, report both:
1. Uncorrected p-values (for transparency)
2. Bonferroni-corrected significance (for inference)

**Example:** "The What-Where comparison was significant before correction (p = .023) but not after Bonferroni adjustment (α_adj = .0167)."

**Conservative Nature:** Bonferroni controls family-wise error rate (FWER), ensuring Type I error ≤ α across all comparisons. Trade-off: Reduced power (increased Type II errors).

### 4.5.2 False Discovery Rate (FDR)

[TBD: Benjamini-Hochberg procedure for exploratory analyses]

---

## 4.6 Missing Data Handling

**Participant-Level Exclusions:** Three participants excluded during data collection for insufficient effort (answered "I don't know" for majority of items, reported no confidence). Replaced with new participants to maintain n = 10 per age group.

**Item-Level Exclusions:** IRT purification excludes ~35% of items on average (see §4.2.2). Items excluded for poor psychometric properties, not missingness.

**Post-Calibration Missing Data:** 0% missing data. All 100 retained participants completed all 4 test sessions (T1-T4). No imputation required.

**Statistical Implication:** Complete data simplifies analysis (no listwise deletion, no multiple imputation). Results generalize to participants who complete full protocol with adequate effort.

---

## 4.7 Software and Reproducibility

**IRT Calibration:**
- Python implementation: `mirt` package (via rpy2) or custom PyIRT
- R implementation: `mirt` package version [TBD from logs]
- Estimation: Expectation-Maximization (EM) algorithm with marginal maximum likelihood

**LMM Estimation:**
- Python implementation: `statsmodels` version [TBD from logs]
- R implementation: `lme4` package version [TBD from logs]
- Estimation: REML or maximum likelihood (specified per analysis)

**Visualization:**
- Python: `matplotlib` version [TBD], `seaborn` version [TBD]
- R: `ggplot2` version [TBD]

**Reproducibility:**
- All analysis code: github.com/rememvr/analysis
- Random seeds: Set for all stochastic procedures (IRT initialization, MCMC sampling)
- Data availability: De-identified data available upon request (ethics approval required)

---

**END CHAPTER 4 (Analysis Methods)**
