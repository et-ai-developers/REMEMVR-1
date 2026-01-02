# RQ 7.4.3: RPM Predicts Temporal Integration Performance

**Chapter:** 7
**Type:** Predictive Validity - Process-Specific
**Subtype:** RPM Predicting When Domain Integration
**Full ID:** 7.4.3

---

## Research Question

**Primary Question:**
Does RPM (fluid intelligence) predict performance on items requiring integration of What+Where+When information?

**Scope:**
This RQ examines whether fluid intelligence (measured by Raven's Progressive Matrices) differentially predicts performance on complex integration items versus simple single-domain items. Uses N=100 participants with theta scores from Ch5 analyses and RPM scores from master.xlsx.

**Theoretical Framing:**
Process-specific prediction analysis examining whether fluid intelligence supports relational binding and complex integration across episodic memory domains. Tests whether temporal integration (When domain) requires more fluid reasoning capacity than simple object identification.

---

## Theoretical Background

**Relevant Theories:**
- **Relational Binding Theory** (Oberauer, 2019): Fluid intelligence supports relational binding and complex integration across multiple information dimensions.
- **Working Memory Theory**: Complex episodic integration requiring What+Where+When coordination should tap fluid intelligence more than single-domain processing.

**Key Citations:**


**Theoretical Predictions:**
Fluid intelligence should predict complex integration items more strongly than simple single-domain items, as relational binding across domains requires fluid reasoning capacity.

**Literature Gaps:**
Limited research on whether fluid intelligence differentially predicts episodic memory performance based on integration complexity.

---

## Hypothesis

**Primary Hypothesis:**
RPM should predict complex integration items more than simple items. Relational binding across domains requires fluid reasoning.

**Secondary Hypotheses:**
Using Order (-O-) questions as proxy for temporal integration, RPM should show stronger correlation with When domain performance compared to What-only performance.

**Theoretical Rationale:**
Items requiring What+Where+When integration place greater demands on relational processing and working memory coordination, functions supported by fluid intelligence. Single-domain items rely more on domain-specific memory systems.

**Expected Effect Pattern:**
- r(RPM, Overall_Theta) = 0.32, p = 0.001
- r(RPM, What_Only_Theta) = 0.25, p = 0.012
- Difference tested via Steiger's Z-test, expecting significant differential prediction

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Used for single-domain comparison baseline

- [ ] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location)
  - [ ] `-U-` tags (pick-up location)
  - [ ] `-D-` tags (put-down location)
  - Description: Not primary focus for this integration analysis

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Primary focus as proxy for temporal integration complexity

**Inclusion Rationale:**
Uses Order (-O-) questions as proxy for temporal integration complexity. Compares overall theta (requiring all domains) versus single-domain What performance to test differential prediction.

**Exclusion Rationale:**
Where domain not directly examined in this analysis, focus is on temporal integration (When) versus object identification (What) as complexity contrast.

---

## Analysis Approach

**Analysis Type:**
Multiple correlation analysis with Steiger's Z-test for dependent correlations

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load overall theta scores from Ch5 analyses
- Extract What-only and When-only theta scores 
- Load RPM scores from master.xlsx
- Check data quality and handle missing values

**Step 2:** Define integration complexity
- Option A: Use Order (-O-) questions as proxy for temporal integration
- Option B: Compare overall theta (requires all domains) vs single-domain theta
- Create integration complexity variables

**Step 3:** Compute correlations
- r(RPM, Theta_Integration) - complex integration performance
- r(RPM, Theta_SingleDomain) - simple single-domain performance
- Extract correlation coefficients with 95% confidence intervals

**Step 4:** Test differential prediction
- Steiger's Z-test for difference between dependent correlations
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Bonferroni correction (± = 0.00179/4 = 0.000448)
- Secondary: FDR correction for comparison

**Step 5:** Effect sizes and confidence intervals
- Cohen's q for correlation difference
- bootstrap (1000 replications, seed=42) 95% CIs for correlation coefficients
- Semi-partial correlations if control variables included

**Step 6:** Model diagnostics
- Check assumptions for correlation analysis
- Identify potential outliers using Cook's D
- Test normality of variables (Shapiro-Wilk)

**Step 7:** Sensitivity analyses
- Exclude outliers and recompute correlations
- Try robust correlation methods (Spearman) if assumptions violated
- Compare different definitions of integration complexity

**Step 8:** Power analysis
- Post-hoc power for observed correlation differences
- Sensitivity analysis for smallest detectable difference

**Expected Outputs:**
- data/step01_rpm_extraction.csv (RPM scores from master.xlsx)
- data/step02_theta_integration.csv (integration complexity scores)
- data/step03_theta_single_domain.csv (simple domain scores)
- data/step04_correlation_analysis.csv (correlations with CIs, dual p-values)
- data/step05_steiger_test.csv (differential prediction test results)
- data/step06_effect_sizes.csv (Cohen's q, bootstrap (1000 replications, seed=42) CIs)
- data/step07_sensitivity_analysis.csv (robustness checks)
- data/step08_power_analysis.csv (post-hoc and sensitivity power)
- results/rq_7_4_3_summary.md (text summary for thesis)
- plots/correlation_comparison.png (visualization of differential prediction)

**

**Cross-Validation:**
- Implement 5-fold CV (seed=42) for generalization assessment
- Report mean CV-R² and SD across folds
- CV-R² to full-sample R² gap should be <0.10
- If gap >0.10: Consider regularization


**Success Criteria:**
- [ ] Both correlations computed successfully with valid 95% CIs
- [ ] Steiger's Z-test completed for dependent correlation comparison
- [ ] BOTH uncorrected AND corrected p-values reported (Decision D068)
- [ ] Effect size (Cohen's q) computed for correlation difference
- [ ] Power > 0.80 for medium correlation difference (r e 0.20)
- [ ] No influential outliers (Cook's D < 4/N)
- [ ] Variables approximately normally distributed (Shapiro-Wilk p > 0.05)
- [ ] Sensitivity analyses confirm main results
- [ ] Integration complexity operationalized clearly (When vs What comparison)

---

## Data Source

**Data Type:**
DERIVED (from Ch5 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 domain-specific analyses (5.2.x series for What/When theta scores)

**File Paths:**
- results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta)
- results/ch5/5.2.3/data/step03_theta_scores.csv (When domain theta, if available)
- results/ch5/5.1.1/data/step03_theta_scores.csv (Overall omnibus theta)
- data/cache/master.xlsx (RPM_Scor cognitive test)

**Dependencies:**
Ch5 domain analyses (5.2.x) must complete before this RQ can run. Specifically needs What and When domain theta estimates.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- [ ] Exclude participants with missing RPM scores
- [ ] Exclude participants with missing theta estimates

**Items:**
- [x] What domain items (-N- tags) for single-domain baseline
- [x] When domain items (-O- tags) for integration complexity
- [x] Overall omnibus factor for comprehensive integration measure

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) aggregated into domain-specific theta scores

---