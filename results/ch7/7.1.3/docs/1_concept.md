# RQ 7.1.3: Which test predicts which domain?

**Chapter:** 7
**Type:** Predictive Validity (Core)
**Subtype:** Domain-Specific Prediction
**Full ID:** 7.1.3

---

## Research Question

**Primary Question:**
Do verbal tests (RAVLT) preferentially predict What memory, visuospatial tests (BVMT) predict Where memory, and neither predicts When memory?

**Scope:**
100 participants across all domain-specific theta scores from Ch5 domain analyses

**Theoretical Framing:**
Tests cognitive test domain specificity by examining whether different neuropsychological tests show differential prediction patterns for episodic memory domains (What/Where/When) as measured by REMEMVR.

---

## Theoretical Background

**Relevant Theories:**
Baddeley's working memory model (1992) posits dissociable verbal and visuospatial subsystems. The RAVLT taps verbal/phonological processing while BVMT assesses visuospatial working memory. Temporal order memory may rely on hippocampal sequence encoding (Eichenbaum, 2014) not captured by either test.

**Key Citations:**
- Baddeley (1992): Working memory model with domain-specific subsystems
- Eichenbaum (2014): Hippocampal sequence encoding for temporal order

**Theoretical Predictions:**
Domain-specific prediction pattern expected based on test modality:
- RAVLT should predict What memory (object identity verbally encoded)
- BVMT should predict Where memory (spatial locations visuospatially encoded) 
- Neither should predict When memory (temporal order relies on distinct mechanism)
- RPM should predict all domains equally (fluid intelligence is domain-general)

**Literature Gaps:**
Few studies have examined domain-specific prediction patterns between traditional neuropsychological tests and ecologically valid VR memory tasks across What/Where/When episodic memory domains.

---

## Hypothesis

**Primary Hypothesis:**
RAVLT will show stronger prediction of What memory than Where memory, while BVMT will show stronger prediction of Where memory than What memory.

**Secondary Hypotheses:**
1. Neither RAVLT nor BVMT will significantly predict When memory
2. RPM will show similar beta coefficients across all domains (domain-general fluid intelligence)
3. R² for When memory models will be lower than What and Where memory models

**Theoretical Rationale:**
Working memory subsystems (verbal vs visuospatial) should map onto episodic memory encoding strategies, with objects encoded verbally and locations encoded spatially. Temporal order may depend on hippocampal sequence processing not assessed by traditional tests.

**Expected Effect Pattern:**
Domain-specificity tests using Steiger's Z:
- RAVLT_beta_What > RAVLT_beta_Where (p < 0.05)
- BVMT_beta_Where > BVMT_beta_What (p < 0.05) 
- R² pattern: What H Where > When
- RPM shows consistent beta coefficients across domains

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: RAVLT preferentially predicts object identity memory through verbal encoding strategies

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: BVMT preferentially predicts spatial location memory through visuospatial encoding strategies

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Neither test predicts temporal order (distinct hippocampal mechanism)

**Inclusion Rationale:**
Uses domain-specific theta scores from Ch5 5.2.x analyses to test whether different cognitive tests show domain-specific prediction patterns based on test modality (verbal vs visuospatial).

**Exclusion Rationale:**
None - all three core episodic memory domains are examined to test domain-specificity hypothesis.

---

## Analysis Approach

**Analysis Type:**
Multiple Linear Regression with Domain-Specific Models and Cross-Domain Beta Comparisons

**High-Level Workflow:**

**Step 1:** Extract domain-specific theta scores
- Load from Ch5 5.2.1/5.2.2/etc. results  
- Compute mean theta per UID per domain

**Step 2:** Fit domain-specific models
- Model_What: `Theta_What ~ RAVLT_T + BVMT_T + RPM_T`
- Model_Where: `Theta_Where ~ RAVLT_T + BVMT_T + RPM_T` 
- Model_When: `Theta_When ~ RAVLT_T + BVMT_T + RPM_T`

**Step 3:** Compare beta coefficients across domains
- Extract beta_RAVLT for each domain
- Steiger's Z-test: Is beta_RAVLT_What > beta_RAVLT_Where?
- Steiger's Z-test: Is beta_BVMT_Where > beta_BVMT_What?

**Step 4:** Compare R² across domains
- Bootstrap CIs for each model's R²
- Hypothesis: R²_When < R²_What H R²_Where

**Step 5:** Create beta coefficient matrix
- Heatmap visualization: rows=domains, columns=tests

**Expected Outputs:**
- data/step01_domain_theta_scores.csv (mean theta per UID per domain)
- data/step02_cognitive_tests.csv (RAVLT, BVMT, RPM scores)
- data/step03_analysis_input.csv (merged dataset)
- data/step04_domain_models.csv (regression results per domain)
- data/step05_beta_comparisons.csv (Steiger's Z-test results)
- results/domain_prediction_summary.md (text summary)
- plots/domain_specificity_heatmap.png (beta coefficient matrix)

**Success Criteria:**
- RAVLT_beta_What > RAVLT_beta_Where (p < 0.05)
- BVMT_beta_Where > BVMT_beta_What (p < 0.05)
- R²_When < R²_What and R²_When < R²_Where  
- RPM shows similar beta across all domains

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.2.x domain theta scores + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.2.x (domain-specific analyses)

**File Paths:**
- results/ch5/5.2.1/data/step03_theta_scores.csv (What domain)
- results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain)  
- results/ch5/5.2.3/data/step03_theta_scores.csv (When domain)
- data/cache/master.xlsx (cognitive test scores)

**Dependencies:**
Ch5 5.2.1, 5.2.2, and 5.2.3 must complete before this RQ can run

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with complete cognitive test data

**Items:**
- [x] Domain-specific theta scores from Ch5 analyses

**Tests:**
- [x] RAVLT Total Score (T1-T5 sum)
- [x] BVMT Total Recall Score  
- [x] RPM Total Score

**Variables Extracted:**
- **DVs:** Mean Theta_What, Theta_Where, Theta_When per UID
- **IVs:** RAVLT_T, BVMT_T, RPM_T from master.xlsx
- **Sample:** N=100 participants

---