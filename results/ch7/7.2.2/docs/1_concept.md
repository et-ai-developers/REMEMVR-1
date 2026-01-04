# RQ 7.2.2: Do cognitive tests attenuate age effects on REMEMVR?

**Chapter:** 7
**Type:** Predictive Validity
**Subtype:** Age Attenuation Analysis
**Full ID:** 7.2.2

---

## Research Question

**Primary Question:**
What proportion of age-related variance is attenuated when controlling for cognitive tests? Complete attenuation suggests tests capture all age-sensitive processes; partial attenuation suggests REMEMVR captures additional age-sensitive processes.

**Scope:**
Cross-sectional analysis examining how cognitive tests (RAVLT, BVMT, RPM) attenuate the relationship between age and REMEMVR theta scores. Uses bivariate age effects from RQ 7.2.1 as baseline and compares to controlled effects from Model 2. Attenuation calculated as percentage reduction in age coefficients. N=100 participants.

**Theoretical Framing:**
Tests whether traditional cognitive assessments fully capture age-related memory decline measured by REMEMVR, or whether REMEMVR captures additional age-sensitive processes beyond traditional tests. Central to understanding REMEMVR's incremental validity for aging research.

---

## Theoretical Background

**Relevant Theories:**
- **Age-Related Memory Decline Theory**: Normal aging shows selective decline in episodic memory due to hippocampal vulnerability and reduced processing speed.
- **Cognitive Reserve Theory** (Stern, 2002): Individual differences in cognitive capacity influence age-related decline patterns.
- **VR Scaffolding Hypothesis**: Environmental support in VR may reduce age differences by providing external memory cues.

**Key Citations:**
- Park & Reuter-Lorenz (2009): Dual-process model of cognitive aging
- Craik & Bialystok (2006): Cognition through the lifespan

**Theoretical Predictions:**
If RAVLT/BVMT comprehensively measure episodic memory, they should fully explain age-related REMEMVR variance. If attenuation is partial, REMEMVR captures age-sensitive processes beyond traditional tests. VR scaffolding hypothesis predicts substantial attenuation due to environmental support.

**Literature Gaps:**
Limited research on whether ecologically valid VR assessments capture age effects beyond traditional neuropsychological tests. Understanding attenuation patterns informs whether VR assessments provide incremental value for aging research.

---

## Hypothesis

**Primary Hypothesis:**
Complete or near-complete attenuation expected (>70%), consistent with VR scaffolding hypothesis from Ch5. Traditional tests should capture most age-related variance if they tap the same underlying episodic memory processes.

**Secondary Hypotheses:**
Domain-specific attenuation patterns may differ: What domain may show greater attenuation (more scaffolded by visual cues), while When domain may show less attenuation (temporal processing less scaffolded).

**Theoretical Rationale:**
VR scaffolding provides environmental support that reduces age differences compared to traditional tests. If scaffolding is effective, cognitive tests should account for most age-related REMEMVR variance because both tap similar episodic processes but VR reduces age-related deficits.

**Expected Effect Pattern:**
Attenuation ratio: (beta_Age_bivariate - beta_Age_controlled) / beta_Age_bivariate. Expected >70% attenuation with 95% CI not including 0, indicating significant mediation by cognitive tests.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in overall theta_all scores and domain-specific analyses

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in overall theta_all scores and domain-specific analyses

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in overall theta_all scores and domain-specific analyses

**Inclusion Rationale:**
Analyzes attenuation for overall REMEMVR (theta_all) and each domain separately to identify domain-specific patterns. Uses pre-computed theta scores from Ch5 domain analyses.

**Exclusion Rationale:**
None - comprehensive analysis includes all episodic memory domains to understand complete attenuation picture.

---

## Analysis Approach

**Analysis Type:**
Attenuation analysis using regression coefficients from hierarchical models with bootstrap confidence intervals

**High-Level Workflow:**

**Step 1:** Extract baseline effects from RQ 7.2.1
- Load bivariate age effects (beta_Age_bivariate)
- Load controlled age effects (beta_Age_controlled from Model 2)
- Verify coefficient availability for overall and domain-specific analyses

**Step 2:** Compute attenuation ratios
- Overall: (beta_Age_bivariate - beta_Age_controlled) / beta_Age_bivariate
- Domain-specific: repeat for What, Where, When theta scores
- Convert to percentages for interpretability

**Step 3:** Bootstrap confidence intervals
- 1000 bootstrap samples for attenuation ratios
- 95% CI construction for each domain
- Test significance: CI excludes 0 indicates significant attenuation

**Step 4:** Domain comparison analysis
- Compare attenuation across domains using bootstrap
- Test: Do domains show differential attenuation patterns?
- Expected: What > Where > When based on scaffolding theory

**Step 5:** Effect size interpretation
- Classify attenuation: <30% minimal, 30-70% partial, >70% substantial
- Compare to published mediation studies in aging literature
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Bonferroni (alpha = 0.05/4 = 0.0125 for 4 domains)

**Step 6:** Model diagnostics and validation
- Verify original regression assumptions from 7.2.1
- Sensitivity analysis: exclude potential outliers, recompute
- Cross-validation: bootstrap stability of attenuation estimates

**CRITICAL for Ch7 and multiple comparisons:**
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Include bootstrap CIs for non-normal attenuation distributions
- Include power analysis for detecting meaningful attenuation (>30%)
- Include effect sizes: Cohen's f for overall model improvement

**Expected Outputs:**
- data/step01_attenuation_ratios.csv (primary analysis results)
- data/step02_bootstrap_cis.csv (confidence intervals)
- data/step03_domain_comparisons.csv (between-domain tests)
- data/step04_sensitivity_analysis.csv (robustness checks)
- data/step05_effect_sizes.csv (f, R change, with 95% CIs)
- results/attenuation_summary.md (text summary for thesis)
- plots/attenuation_visualization.png (domain comparison plot)

**Success Criteria:**
- Attenuation > 50% for overall REMEMVR (supports scaffolding hypothesis)
- No domain shows significant residual age effect after control (p > 0.05)
- Bootstrap CIs stable (width < 40% of point estimate)
- Pattern consistent with VR scaffolding hypothesis (What > Where > When)
- Sensitivity analysis shows robust findings (5% with outlier exclusion)

---

## Data Source

**Data Type:**
DERIVED (from RQ 7.2.1 regression coefficients + Ch5 domain-specific analyses)

### DERIVED Data Sources:

**Source RQ:**
RQ 7.2.1 (Age and cognitive test effects on REMEMVR)

**File Paths:**
- results/ch7/7.2.1/data/step04_regression_results.csv (age coefficients)
- results/ch5/5.1.1/data/step03_theta_scores.csv (overall theta_all)
- results/ch5/5.2.1/data/step03_theta_scores.csv (What domain theta)
- results/ch5/5.2.2/data/step03_theta_scores.csv (Where domain theta)
- results/ch5/5.2.3/data/step03_theta_scores.csv (When domain theta)

**Dependencies:**
RQ 7.2.1 must complete hierarchical regression analysis before this RQ can run. Specifically requires both Model 1 (bivariate age) and Model 2 (age + cognitive tests) results.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 7.2.1 (inherited inclusion criteria)
- [x] Complete cognitive test data required
- [x] No missing age data

**Items:**
- N/A (uses pre-computed theta scores from Ch5 analyses)

**Tests:**
- [x] All 4 tests aggregated into theta scores (inherited from Ch5)

**Additional Requirements:**
- Complete RAVLT, BVMT, and RPM test scores from dfnonvr.csv
- No participants with missing demographic data that would affect Model 2 results
- Requires both uncorrected and controlled age effects from 7.2.1 for attenuation calculation

---