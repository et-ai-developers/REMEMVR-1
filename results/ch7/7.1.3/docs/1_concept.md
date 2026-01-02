# RQ 7.1.3: Domain-Specific Prediction Patterns

**Chapter:** 7
**Type:** Predictive Validity (Core)
**Subtype:** Domain-Specific Prediction
**Full ID:** 7.1.3

---

## Research Question

**Primary Question:**
Do verbal tests (RAVLT) preferentially predict What memory, visuospatial tests (BVMT) predict Where memory, and neither predicts When memory?

**Scope:**
This RQ examines domain-specific prediction patterns using IRT-derived theta scores for What, Where, and When domains. Compares predictive strength of RAVLT (verbal), BVMT (visuospatial), and RPM (fluid intelligence) across the three episodic memory domains. N=100 participants with complete cognitive test and REMEMVR data.

**Theoretical Framing:**
Tests Baddeley's working memory model prediction that verbal and visuospatial systems are dissociable. If true, RAVLT should predict What (verbally encoded objects) more than Where (spatially encoded locations), while BVMT should show the opposite pattern. When (temporal sequence) may rely on distinct hippocampal mechanisms not captured by either test.

---

## Theoretical Background

**Relevant Theories:**
- **Baddeley's Working Memory Model (1992):** Posits dissociable verbal and visuospatial subsystems. Verbal tests should predict verbally-encoded domains (What), while visuospatial tests should predict spatially-encoded domains (Where).
- **Hippocampal Sequence Processing (Eichenbaum, 2014):** Temporal order memory may rely on hippocampal sequence encoding mechanisms distinct from both verbal and visuospatial systems.

**Key Citations:**
To be enhanced by rq_scholar

**Theoretical Predictions:**
Working memory theory predicts domain-specific patterns: RAVLT  What, BVMT  Where. Neither should strongly predict When due to reliance on distinct hippocampal sequence mechanisms. RPM (fluid intelligence) should predict all domains equally due to domain-general nature.

**Literature Gaps:**
To be identified by rq_scholar

---

## Hypothesis

**Primary Hypothesis:**
Domain-specific prediction pattern expected:
- RAVLT  What (object identity verbally encoded)
- BVMT  Where (spatial locations visuospatially encoded)  
- Neither  When (temporal order relies on distinct mechanism)
- RPM  All domains equally (fluid intelligence is domain-general)

**Secondary Hypotheses:**
1. RAVLT beta coefficient for What domain > RAVLT beta for Where domain
2. BVMT beta coefficient for Where domain > BVMT beta for What domain
3. R²_When < R²_What H R²_Where (temporal order less predictable)

**Theoretical Rationale:**
Based on Baddeley's working memory model separating verbal and visuospatial systems. Object identity relies on verbal encoding/retrieval (phonological loop), spatial locations rely on visuospatial encoding (visuo-spatial sketchpad). Temporal sequence relies on hippocampal mechanisms not strongly tapped by either traditional test.

**Expected Effect Pattern:**
Steiger's Z-tests should show significant differences: RAVLT_What > RAVLT_Where (p < 0.05) and BVMT_Where > BVMT_What (p < 0.05). When domain R² should be lowest across all models.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming (verbally encoded)

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location) 
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where tags included (spatially encoded)

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence (hippocampally encoded)

**Inclusion Rationale:**
All three core episodic memory domains examined to test domain-specific prediction patterns. What domain expected to correlate with verbal tests (RAVLT), Where domain with visuospatial tests (BVMT), and When domain with neither due to distinct encoding mechanisms.

**Exclusion Rationale:**
None - this RQ specifically requires all three domains to test cross-domain prediction patterns.

---

## Analysis Approach

**Analysis Type:**
Multiple Linear Regression with cross-domain beta coefficient comparisons

**High-Level Workflow:**

**Step 1:** Extract domain-specific theta scores from Ch5 5.2.x results and compute mean per UID per domain

**Step 2:** Fit three domain-specific regression models:
- Model_What: `Theta_What ~ RAVLT_T + BVMT_T + RPM_T`  
- Model_Where: `Theta_Where ~ RAVLT_T + BVMT_T + RPM_T`
- Model_When: `Theta_When ~ RAVLT_T + BVMT_T + RPM_T`

**Step 3:** Extract beta coefficients and R² values for each domain model

**Step 4:** Compare beta coefficients across domains using Steiger's Z-tests:
- Test: beta_RAVLT_What > beta_RAVLT_Where
- Test: beta_BVMT_Where > beta_BVMT_What

**Step 5:** Compare R² across domains using bootstrap 95% CIs

**Step 6:** Create beta coefficient heatmap visualization (rows=domains, columns=tests)

**CRITICAL for Ch7 and multiple comparisons:**
- Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
- Include model diagnostics (residual normality, homoscedasticity, influential points)
- Include effect sizes with 95% CIs (R², ² coefficients)
- Bootstrap CIs for R² comparisons

**Expected Outputs:**
- data/step01_domain_theta_scores.csv (mean theta per UID per domain)
- data/step02_what_model_results.csv (What domain regression results)
- data/step03_where_model_results.csv (Where domain regression results)  
- data/step04_when_model_results.csv (When domain regression results)
- data/step05_beta_comparison_matrix.csv (cross-domain beta coefficients)
- data/step06_steiger_z_tests.csv (cross-domain comparison statistics)
- plots/domain_prediction_heatmap.png (beta coefficient visualization)
- results/domain_specific_prediction_summary.md (text summary for thesis)

**Success Criteria:**
- RAVLT_beta_What > RAVLT_beta_Where (p < 0.05)
- BVMT_beta_Where > BVMT_beta_What (p < 0.05)
- R²_When < R²_What and R²_When < R²_Where
- RPM shows similar beta coefficients across all domains
- All models converge, residuals normally distributed

---

## Data Source

**Data Type:**
DERIVED (from Ch5 domain analysis outputs + master.xlsx)

### DERIVED Data Source:

**Source RQ:**
Ch5 5.2.x (Domain-specific analyses)

**File Paths:**
- results/ch5/5.2.1/data/step03_theta_what.csv (What domain theta scores)
- results/ch5/5.2.2/data/step03_theta_where.csv (Where domain theta scores)  
- results/ch5/5.2.3/data/step03_theta_when.csv (When domain theta scores)
- data/cache/master.xlsx (cognitive test scores: RAVLT_T, BVMT_T, RPM_T)

**Dependencies:**
Ch5 domain analyses (5.2.1, 5.2.2, 5.2.3) must complete IRT calibration and theta estimation before this RQ can run.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with complete cognitive test and REMEMVR data
- [ ] Exclude: Participants missing any cognitive test scores

**Items:**
- N/A (theta scores already aggregated by domain)

**Tests:**
- [x] All tests aggregated into domain-specific theta scores

---