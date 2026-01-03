# RQ 7.8.2: Profile External Validation

**Chapter:** 7
**Type:** Profile Analysis
**Subtype:** External Validation
**Full ID:** 7.8.2

---

## Research Question

**Primary Question:**
Do cognitive test profiles (e.g., verbal-dominant vs spatial-dominant) correspond to REMEMVR profiles?

**Scope:**
This RQ examines correspondence between cognitive test latent profile analysis (LPA) and REMEMVR performance latent profiles from RQ 7.8.1. Cognitive profiles derived from RAVLT, BVMT, and RPM test scores. REMEMVR profiles based on domain-specific theta scores. N=100 participants. Cross-tabulation analysis with chi-square test of association and Cramer's V effect size.

**Theoretical Framing:**
External validation of REMEMVR latent profiles using established cognitive tests. If REMEMVR profiles are meaningful, they should correspond to cognitive ability patterns. Verbal-dominant individuals (high RAVLT, low BVMT) may show What-specialist patterns, while spatial-dominant individuals may show Where-specialist patterns.

---

## Theoretical Background

**Relevant Theories:**
- **Cognitive Specialization Theory**: Individual differences in cognitive abilities create domain-specific strengths. Verbal abilities (RAVLT) should predict episodic What performance, while spatial abilities (BVMT) should predict episodic Where performance.
- **Dual-Process Theory**: Recollection-based domains (Where, When) may correlate with working memory and executive function, while familiarity-based domains (What) may correlate with verbal memory.

**Theoretical Predictions:**
External validation should show meaningful correspondence between cognitive and REMEMVR profiles. Verbal-dominant cognitive profiles predict What-specialist REMEMVR profiles. Spatial-dominant cognitive profiles predict Where-specialist REMEMVR profiles. Generalist cognitive profiles predict balanced REMEMVR performance.

---

## Hypothesis

**Primary Hypothesis:**
Verbal-dominant cognitive profiles (high RAVLT, low BVMT) will predict What-specialist REMEMVR profiles. Spatial-dominant cognitive profiles (high BVMT, low RAVLT) will predict Where-specialist REMEMVR profiles. Generalist cognitive profiles (high on both) will predict balanced REMEMVR performance.

**Secondary Hypotheses:**
Cramer's V association strength will be medium to large (V > 0.30) indicating meaningful correspondence. Chi-square test will be significant (p < 0.05) demonstrating non-random association between cognitive and REMEMVR profile membership.

**Theoretical Rationale:**
If REMEMVR profiles reflect genuine individual differences in episodic memory systems, they should align with established cognitive ability patterns. Verbal memory specialists should excel in object identity (What) tasks, spatial memory specialists should excel in location (Where) tasks.

**Expected Effect Pattern:**
Chi-square test significant (p < 0.001), Cramer's V = 0.30-0.40 indicating medium-large association between cognitive and REMEMVR profile classifications.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in REMEMVR domain-specific theta scores from Ch5

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in REMEMVR domain-specific theta scores from Ch5

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in REMEMVR domain-specific theta scores from Ch5

**Inclusion Rationale:**
Uses REMEMVR profiles from RQ 7.8.1 which are based on domain-specific theta scores (What, Where, When) from Ch5 analyses. All three episodic memory domains included to capture individual difference patterns across the full WWW framework.

---

## Analysis Approach

**Power Analysis:**
- Sample size: N=100 with k predictors
- Post-hoc power for medium effects (f²=0.15): Approximately 80%
- Minimum detectable effect: f²=0.10 with current sample
- Limitation acknowledged: Underpowered for small effects (f²<0.10)


**Analysis Type:**
Latent Profile Analysis (LPA) for cognitive tests + Chi-square test of association + Cramer's V effect size

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load REMEMVR profile classifications from RQ 7.8.1 results
- Extract cognitive test scores (RAVLT, BVMT, RPM) from master.xlsx
- Standardize cognitive test scores to T-scores (M=50, SD=10)
- Merge datasets by participant ID

**Step 2:** Fit cognitive test LPA
- Variables: RAVLT_T, BVMT_T, RPM_T
- Test 2-5 latent profiles using mixtures package
- Select optimal K using BIC, entropy, interpretability
- Extract profile classifications and probabilities

**Step 3:** Cross-tabulate profiles
- Create contingency table: Cognitive profile × REMEMVR profile
- Calculate observed frequencies and expected frequencies
- Compute cell percentages and standardized residuals

**Step 4:** Test association
- Chi-square test of independence
- Report both uncorrected and Bonferroni-corrected p-values (Decision D068)
- Primary correction: ± = 0.05/28 = 0.00179 (Ch7 family-wise)
- Cramer's V for effect size with 95% confidence interval

**Step 5:** Interpret correspondence patterns
- Identify which cognitive profiles predict which REMEMVR profiles
- Calculate conditional probabilities P(REMEMVR profile | Cognitive profile)
- Assess theoretical coherence of associations

**Expected Outputs:**
- data/step01_cognitive_lpa_input.csv (standardized test scores)
- data/step02_cognitive_profile_classifications.csv (LPA results)
- data/step03_profile_crosstab.csv (contingency table with frequencies)
- data/step04_association_test.csv (chi-square results, Cramer's V, dual p-values)
- data/step05_conditional_probabilities.csv (prediction patterns)
- results/profile_correspondence_summary.md (text summary for thesis)
- plots/profile_correspondence_heatmap.png (visualization)



**Success Criteria:**
- Cognitive LPA converges with entropy > 0.70
- Cross-tabulation shows non-random pattern
- Chi-square significant after correction (p < 0.00179)
- Cramer's V > 0.20 (small-medium association minimum)
- Theoretical coherence: verbal profiles predict What-specialists
- At least 60% correct classification rate above chance

---

## Data Source

**Data Type:**
DERIVED (from RQ 7.8.1 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
RQ 7.8.1 (REMEMVR Latent Profile Analysis)

**File Paths:**
- results/ch7/7.8.1/data/step03_rememvr_profile_classifications.csv (REMEMVR profile assignments)
- data/cache/master.xlsx (cognitive test scores RAVLT, BVMT, RPM)

**Dependencies:**
RQ 7.8.1 must complete LPA and profile extraction before this RQ can run

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 7.8.1 (inherited inclusion criteria)
- [x] Complete cognitive test data required (RAVLT, BVMT, RPM)
- [ ] Exclude: Participants missing any cognitive test scores

**Items:**
- N/A (uses profile classifications, not individual items)

**Tests:**
- [x] Cognitive tests: RAVLT total, BVMT total recall, RPM total score
- [x] REMEMVR: All domain theta scores used in profile analysis

---