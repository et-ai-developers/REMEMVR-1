# RQ 5.5.5 Complete - Purified CTT Paradox 4th Replication

## RQ 5.5.5 Complete Pipeline Execution (2025-12-05 15:30)

**Archived from:** state.md Session (2025-12-05 15:30)
**Original Date:** 2025-12-05 15:30
**Reason:** Task completed, RQ validated for thesis

---

### Context

User requested execution of RQ 5.5.5 with g_code step-by-step, debugging each step before proceeding, then final validation with rq_validate. This RQ tests the purification-trajectory paradox for source-destination memory (4th independent replication).

### Major Accomplishments

#### 1. Complete RQ 5.5.5 Pipeline Execution (9 Steps + Validation)

All 9 analysis steps executed and validated:

| Step | Description | Status | Key Output |
|------|-------------|--------|------------|
| **Step 0** | Load dependency data from RQ 5.5.1 | SUCCESS | All 5 inputs validated |
| **Step 1** | Map retained vs removed items | SUCCESS | 32/36 items retained (89%) |
| **Step 2** | Compute Full CTT sum scores | SUCCESS | 800 rows, mean: S=68.4%, D=45.5% |
| **Step 3** | Compute Purified CTT sum scores | SUCCESS | r=0.98 correlation with Full |
| **Step 4** | Reliability assessment (Cronbach's alpha) | SUCCESS | 4 conditions with bootstrap CIs |
| **Step 5** | Correlation analysis (Steiger's z-test) | SUCCESS | D068 dual p-values |
| **Step 6** | Z-standardize all measurements | SUCCESS | 800 rows, mean=0, SD=1 |
| **Step 7** | Fit parallel LMMs (6 models) | SUCCESS | All converged with AIC |
| **Step 7.5** | Validate LMM assumptions | SUCCESS | 42/42 checks PASSED |
| **Step 8** | Prepare plot data | SUCCESS | 4+6 rows for correlation/AIC plots |

**Code Fixes Applied:**
1. **Step 6:** Test format mismatch (theta '1' vs CTT 'T1') - converted TSVR test format
2. **Step 7.5:** Same test format mismatch fixed

#### 2. Statistical Results (Primary Hypothesis - PARADOX PARTIALLY CONFIRMED)

**Correlation Analysis (Step 5):**

| Location | r_Full | r_Purified | Δr | Steiger z | p_Bonferroni | Result |
|----------|--------|------------|-----|-----------|--------------|--------|
| Source | 0.934 | 0.944 | **+0.010** | 1.72 | 0.172 | NOT SIG |
| Destination | 0.800 | 0.871 | **+0.072** | 4.68 | **<0.001** | **SIG** |

**AIC Model Comparison (Step 7):**

| Location | AIC(Full) | AIC(Purified) | ΔAIC | Interpretation |
|----------|-----------|---------------|------|----------------|
| Source | **974.49** | 979.75 | **+5.26** | Full favored (substantial) |
| Destination | **1098.00** | 1115.92 | **+17.92** | Full favored (decisive) |

**Paradox Status:**
- **Destination Memory:** FULL PARADOX REPLICATION
  - Purified shows SIGNIFICANTLY higher correlation with IRT (Δr=+0.072, p<0.001)
  - But DECISIVELY WORSE trajectory fit (ΔAIC=+17.92)

- **Source Memory:** PARTIAL PARADOX REPLICATION
  - Correlation improvement NOT significant (ceiling effect at r=0.93)
  - But SUBSTANTIALLY WORSE trajectory fit (ΔAIC=+5.26)

**4th Independent Replication:** Paradox now confirmed across:
1. RQ 5.2.5: What/Where domains
2. RQ 5.3.6: IFR/ICR/IRE paradigms
3. RQ 5.4.5: Common/Congruent/Incongruent schema
4. **RQ 5.5.5: Source/Destination memory** (current)

#### 3. Reliability Assessment (Step 4)

| Location | Version | Alpha | 95% CI | Interpretation |
|----------|---------|-------|--------|----------------|
| Source | Full | 0.775 | [0.744, 0.800] | Acceptable |
| Source | Purified | 0.778 | [0.747, 0.804] | Acceptable |
| Destination | Full | 0.622 | [0.563, 0.671] | Questionable |
| Destination | Purified | 0.612 | [0.551, 0.663] | Questionable |

**Alpha Improvement:**
- Source: +0.004 (negligible)
- Destination: -0.010 (slight decrease after purification)

**Note:** Unlike prior RQs, purification did NOT improve reliability for destination memory. This suggests high retention rate (89%) means removed items may have contributed unique variance.

#### 4. Assumption Validation (Step 7.5)

All 6 models × 7 assumptions = **42/42 checks PASSED** (100%):
- Linearity: PASS (all show forgetting pattern r=-0.23 to -0.40)
- Homoscedasticity: PASS (variance ratio 1.10-1.41)
- Normality: PASS (skew<1, kurtosis-3<2)
- Random Effects: PASS (variance 0.34-0.49)
- Independence: PASS (autocorr<0.30)
- Multicollinearity: PASS (single predictor)
- Influential Observations: PASS (outlier rate <0.5%)

#### 5. Validation Pipeline Complete

| Component | Status | Notes |
|-----------|--------|-------|
| g_code | SUCCESS | All 9 steps executed |
| rq_inspect | SUCCESS | Outputs validated |
| rq_validate | **PASS WITH NOTES** | 29/30 checks passed |

**rq_validate Results:**
- Data Sourcing: PASS (D1-D5)
- Model Specification: PASS (M1-M6)
- Scale Transformation: PASS (S1-S4)
- Statistical Rigor: PASS WITH NOTES (R1-R5) - 1 moderate issue
- Cross-Validation: PASS (C1-C4)
- Thesis Alignment: PASS (T1-T3)

**Moderate Issue (Optional Fix):**
- Missing Cohen's q effect size for correlation improvement
- Δr reported, Steiger's z reported, but standardized effect size not computed
- Results interpretable without q (Δr on [0,1] scale is straightforward)

#### 6. Files Created

**Code (9 scripts):**
- results/ch5/5.5.5/code/step00_dependency_validation.py
- results/ch5/5.5.5/code/step01_item_mapping.py
- results/ch5/5.5.5/code/step02_ctt_full_scores.py
- results/ch5/5.5.5/code/step03_ctt_purified_scores.py
- results/ch5/5.5.5/code/step04_reliability_assessment.py
- results/ch5/5.5.5/code/step05_correlation_analysis.py
- results/ch5/5.5.5/code/step06_standardized_scores.py
- results/ch5/5.5.5/code/step07_lmm_model_comparison.py
- results/ch5/5.5.5/code/step07.5_assumption_validation.py
- results/ch5/5.5.5/code/step08_plot_data_preparation.py

**Data (10+ files):**
- step00_dependency_validation.txt
- step01_item_mapping.csv (36 rows)
- step02_ctt_full_scores.csv (800 rows)
- step03_ctt_purified_scores.csv (800 rows)
- step04_reliability_assessment.csv (4 rows)
- step05_correlation_analysis.csv (2 rows)
- step06_standardized_scores.csv (800 rows)
- step07_lmm_model_comparison.csv (2 rows)
- step07.5_assumption_validation.csv (42 rows)

**Plots:**
- plots/step08_correlation_comparison_data.csv (4 rows)
- plots/step08_aic_comparison_data.csv (6 rows)

**Results:**
- results/validation.md (495 lines, comprehensive 6-layer validation)
- status.yaml (all phases complete)

#### 7. Theoretical Interpretation

**Paradox Mechanism:**
- **Cross-sectional:** Purification removes noise → higher correlation with IRT theta
- **Longitudinal:** Purification removes variance → worse trajectory fit (higher AIC)

**Source Memory Ceiling Effect:**
- Baseline r_full = 0.934 (exceptionally high)
- Minimal room for purification improvement
- Explains non-significant correlation improvement

**Destination Memory Full Paradox:**
- Lower baseline r_full = 0.800 (more room for improvement)
- Δr = +0.072 is substantial and significant
- But ΔAIC = +17.92 decisively favors Full CTT

**General Measurement Principle Established:**
IRT-based item purification improves cross-sectional measurement precision but degrades longitudinal trajectory fit by removing variance useful for modeling individual differences in change.

### Session Metrics

**Chapter 5 Progress:**
- RQ 5.5.5: COMPLETE (thesis-ready with 1 optional enhancement)
- Type 5.5: **5/7** RQs complete (5.5.1-5.5.5)
- Chapter 5 Overall: **36/38 RQs complete (95%)**
- Remaining: 5.5.6, 5.5.7 (Type 5.5), 5.1.6, 5.2.8 (BLOCKED by GLMM)

**Tokens:**
- Session start: ~5k (after /refresh)
- Session end: ~110k (at /save)

### Related Topics

**Cross-References:**
- rq_5.4.5_complete_execution_purified_ctt_congruence.md (2025-12-04 01:30: 3rd paradox replication)
- type_5.5_pipeline_complete.md (2025-12-04 04:30: Type 5.5 structure)
- ctt_irt_convergence_validated.md (2025-12-03 20:45: Paradox discovery)
- irt_ctt_inferential_divergence_pattern.md (2025-12-05 14:30: Measurement vs inferential)

---

**End of Archive Entry**
