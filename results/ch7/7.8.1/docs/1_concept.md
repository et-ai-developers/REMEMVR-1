# RQ 7.8.1: Distinct REMEMVR memory profiles?

**Chapter:** 7
**Type:** Latent Profiles & Models  
**Subtype:** Latent Profile Analysis
**Full ID:** 7.8.1

---

## Research Question

**Primary Question:**
Are there distinct latent profiles of REMEMVR performance (e.g., "generalists" vs "specialists" vs "low performers")?

**Scope:**
This RQ examines heterogeneity in episodic memory profiles using Latent Profile Analysis on standardized theta scores from three domains (What, Where, When) across 100 participants. Analysis compares 1-4 profile solutions using BIC, AIC, entropy, and LMR-LRT to identify optimal number of distinct memory profiles.

**Theoretical Framing:**
If memory is unidimensional, one profile should fit best. If multidimensional with meaningful individual differences, multiple profiles will emerge representing distinct patterns of strength/weakness across episodic memory domains.

---

## Theoretical Background

**Relevant Theories:**
- **Individual Differences Framework:** People vary systematically in cognitive abilities. Some may be generalists (consistent across domains) while others show specific strengths/weaknesses.
- **Domain Specificity:** Episodic memory may show domain-specific patterns where individuals excel in object identity (What) but struggle with spatial (Where) or temporal (When) binding.

**Key Citations:**


**Theoretical Predictions:**
If memory domains are functionally distinct, expect multiple profiles representing different patterns of domain-specific performance. Generalists should show consistently high performance across all domains, while specialists might show selective strengths.

**Literature Gaps:**
Individual difference patterns in episodic memory binding across What/Where/When domains using virtual reality assessment are understudied.

---

## Hypothesis

**Primary Hypothesis:**
Expect 2-4 distinct profiles: (1) Generalists - high on all domains, (2) What-specialists - high What, lower Where/When, (3) Low performers - low across all domains.

**Secondary Hypotheses:**
Profiles should differ meaningfully on age and cognitive test performance, providing external validation of profile distinctions.

**Theoretical Rationale:**
Episodic memory binding involves multiple cognitive processes. Individual differences in these processes should create meaningful subgroups rather than continuous variation. Domain-specific patterns expected based on differential neural systems supporting object vs spatial vs temporal memory.

**Expected Effect Pattern:**
Optimal model with K=2-3 profiles based on BIC minimum. LMR-LRT should show significant improvement from K=1 to K=2, potentially to K=3, then non-significant for K=4. Entropy > 0.80 for classification quality.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity memory from Ch5 domain theta scores

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)  
  - [x] `-D-` tags (put-down location)
  - Description: Spatial memory from Ch5 domain theta scores

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order memory from Ch5 domain theta scores

**Inclusion Rationale:**
All three core episodic memory domains included to identify comprehensive memory profiles. Uses domain-specific theta scores that isolate What/Where/When performance patterns.

**Exclusion Rationale:**
No exclusions - comprehensive analysis of all episodic memory domains.

---

## Analysis Approach

**Analysis Type:**
Latent Profile Analysis (LPA) with external validation using cognitive tests

**High-Level Workflow:**

**Step 1:** Extract and prepare domain theta scores
- Load mean theta_What, theta_Where, theta_When per participant from Ch5
- Standardize scores for comparable scaling in LPA

**Step 2:** Fit LPA models with K=1,2,3,4 profiles  
- Use standardized domain scores as indicators
- Compare fit indices: BIC, AIC, entropy, LMR-LRT
- Assess classification quality and interpretability

**Step 3:** Select optimal number of profiles
- Primary criterion: BIC minimum 
- Secondary: LMR-LRT significance test
- Tertiary: Entropy > 0.80 and theoretical interpretability

**Step 4:** Characterize and label profiles
- Extract mean What/Where/When scores for each profile
- Label profiles based on domain patterns
- Compute profile membership probabilities

**Step 5:** External validation
- Test profile differences on age, cognitive tests (RAVLT, BVMT, RPM)
- Use ANOVA/Kruskal-Wallis for group comparisons
- Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)

**Step 6:** Model diagnostics and validation
- Check convergence and local maxima
- Assess profile separation and classification quality
- Bootstrap profile stability (if applicable)

**Expected Outputs:**
- data/step01_domain_theta_scores.csv (extracted and standardized scores)
- data/step02_lpa_fit_comparison.csv (fit indices for K=1,2,3,4)
- data/step03_optimal_profiles.csv (profile membership and probabilities)
- data/step04_profile_characteristics.csv (mean scores by profile)
- data/step05_external_validation.csv (profile differences on validators)
- data/step06_classification_quality.csv (entropy, posterior probabilities)
- results/lpa_summary.md (text summary for thesis)
- plots/profile_plots.png (visualization of domain patterns by profile)

**Success Criteria:**
- [ ] Fit LPA with K=1,2,3,4 profiles successfully
- [ ] All models converge without local maxima issues
- [ ] Select optimal K using fit indices (BIC primary criterion)
- [ ] Characterize profiles with interpretable domain patterns
- [ ] Achieve entropy > 0.80 for classification quality
- [ ] External validation shows profile differences on age/cognitive tests
- [ ] Report dual p-values (uncorrected and Bonferroni-corrected)
- [ ] Profiles have adequate sample size (n > 20 per profile)

---

## Data Source

**Data Type:**
DERIVED (from Ch5 domain-specific outputs)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.2.1, 5.2.2, 5.2.3 (Domain-specific analyses)

**File Paths:**
- results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta scores)
- results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain theta scores) 
- results/ch5/5.2.3/data/step03_theta_scores.csv (When domain theta scores)
- data/cache/master.xlsx (cognitive test scores for validation)

**Dependencies:**
Ch5 5.2.1, 5.2.2, 5.2.3 must complete IRT calibration and theta score extraction before this RQ can run.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from Ch5 domain analyses)

**Items:**
- N/A (theta scores already aggregated by domain)

**Tests:**
- [x] Mean theta across T1-T4 (aggregated temporal performance per domain)

---