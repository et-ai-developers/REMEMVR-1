# RQ 7.7.4: Clinical Profiles - False Negatives

**Chapter:** 7
**Type:** Clinical Utility
**Subtype:** False Negative Reduction
**Full ID:** 7.7.4

---

## Research Question

**Primary Question:**
Can we identify "false negatives" - individuals with low RAVLT but normal REMEMVR? These may have intact ecological memory despite poor lab performance.

**Scope:**
This RQ examines discordance patterns between traditional neuropsychological assessment (RAVLT) and ecological VR assessment (REMEMVR) in 100 participants. Focuses specifically on identifying individuals who appear impaired on traditional tests but perform normally on VR tests, suggesting traditional tests may underestimate real-world memory function.

**Theoretical Framing:**
Clinical utility analysis examining false negative rates in traditional neuropsychological assessment. REMEMVR could provide reassurance for individuals flagged as impaired by traditional tests but who maintain intact ecological memory function.

---

## Theoretical Background

**Relevant Theories:**
- **Ecological Validity Theory**: Traditional laboratory-based cognitive tests may lack ecological validity and fail to capture real-world cognitive functioning. VR environments may better simulate everyday memory demands.
- **Test Specificity Theory**: Different memory tests tap different underlying cognitive processes. Traditional tests emphasize verbal/acoustic processing while VR tests emphasize spatial/visual processing.
- **Clinical Utility Framework**: Diagnostic tests should minimize false negatives to avoid unnecessary clinical concern while maintaining sensitivity to genuine impairment.

**Key Citations:**
[Literature review to be enhanced by rq_scholar]

**Theoretical Predictions:**
Traditional tests may produce false negatives due to factors like test anxiety, language barriers, or reliance on specific cognitive strategies that don't reflect overall memory capacity. VR tests may be less susceptible to these confounds.

**Literature Gaps:**
Limited research on discordance patterns between traditional and VR-based memory assessments, particularly regarding false negative identification in clinical screening.

---

## Hypothesis

**Primary Hypothesis:**
Some low-RAVLT individuals may show normal REMEMVR performance, suggesting traditional tests underestimate their real-world memory function. False negatives may be characterized by specific demographic profiles (older age, higher education, non-native English speakers).

**Secondary Hypotheses:**
- False negatives will show higher premorbid IQ (NART scores) than true positives
- False negatives may be older adults who perform poorly on traditional tests due to age-related test anxiety but retain ecological memory skills
- False negatives may have higher education levels, suggesting intact cognitive reserve

**Theoretical Rationale:**
Traditional neuropsychological tests may be influenced by factors unrelated to memory capacity, such as test-taking strategies, language proficiency, or anxiety. VR-based assessment may bypass some of these confounds by providing more naturalistic memory evaluation.

**Expected Effect Pattern:**
Classification matrix showing approximately 6-10% false negative rate (low RAVLT + normal REMEMVR). False negatives expected to differ from true positives on age, education, and premorbid IQ measures.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in overall REMEMVR theta scores

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in overall REMEMVR theta scores

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in overall REMEMVR theta scores

**Inclusion Rationale:**
Uses omnibus REMEMVR theta scores from Ch5 that aggregate across all episodic memory domains to provide comprehensive ecological memory assessment comparable to RAVLT total scores.

**Exclusion Rationale:**
No domain-specific exclusions. Analysis requires comprehensive memory assessment to fairly compare against RAVLT total performance.

---

## Analysis Approach

**Analysis Type:**
Cross-sectional classification analysis with demographic characterization

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load REMEMVR theta scores from Ch5 results
- Extract RAVLT total scores from dfnonvr.csv
- Standardize both measures to z-scores for classification

**Step 2:** Define classification criteria
- Low RAVLT: z-score < -1.0 (16th percentile)
- Normal REMEMVR: z-score > -0.5 (31st percentile)
- Create 2x2 classification matrix

**Step 3:** Identify false negative cases
- Apply criteria: RAVLT_z < -1 AND REMEMVR_z > -0.5
- Count cases meeting false negative criteria
- Report classification matrix with cell counts

**Step 4:** Characterize false negatives
- Extract demographics: Age, Education, VR_Experience
- Extract cognitive measures: NART (premorbid IQ)
- Compute descriptive statistics for false negative group

**Step 5:** Compare groups
- Compare false negatives vs true positives on demographics
- Test group differences with t-tests or chi-square
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary correction: Bonferroni for multiple comparisons

**Step 6:** Clinical interpretation
- Compute base rates and clinical significance
- Discuss implications for clinical assessment
- Provide recommendations for dual assessment approach

**Expected Outputs:**
- data/step01_cognitive_scores.csv (RAVLT and REMEMVR standardized scores)
- data/step02_classification_matrix.csv (2x2 contingency table)
- data/step03_false_negatives.csv (identified cases with demographics)
- data/step04_group_comparisons.csv (statistical comparisons with dual p-values)
- data/step05_clinical_metrics.csv (sensitivity, specificity, base rates)
- results/false_negative_summary.md (clinical interpretation summary)
- plots/classification_scatter.png (RAVLT vs REMEMVR scatter plot with quadrants)
- plots/demographic_comparisons.png (false negatives vs true positives)

**Success Criteria:**
- [ ] Successfully identify false negative cases
- [ ] Create valid 2x2 classification matrix
- [ ] Characterize false negatives demographically
- [ ] Report dual p-values (uncorrected and Bonferroni-corrected)
- [ ] Compute clinical metrics (sensitivity, specificity)
- [ ] Provide meaningful clinical interpretation
- [ ] Generate clear visualization of classification patterns

---

## Data Source

**Data Type:**
DERIVED (from Ch5 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (Functional Form Comparison - provides omnibus REMEMVR theta scores)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (REMEMVR theta estimates)
- data/cache/master.xlsx (RAVLT total scores, demographics, NART)

**Dependencies:**
Ch5 5.1.1 must complete IRT calibration and theta estimation before this RQ can run

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with complete RAVLT and REMEMVR data
- [ ] Exclude participants with missing RAVLT total scores
- [ ] Exclude participants with incomplete REMEMVR theta estimates

**Items:**
- N/A (uses aggregated theta scores and total test scores)

**Tests:**
- [x] REMEMVR omnibus performance (aggregated across all sessions)
- [x] RAVLT total learning score (T1-T5 sum)
- [x] NART premorbid IQ estimate
- [x] Basic demographics (age, education, VR experience)

---