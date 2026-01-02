# RQ 7.6.3: ICC slope replication across domains

**Chapter:** 7
**Type:** Individual Differences
**Subtype:** ICC slope replication across domains
**Full ID:** 7.6.3

---

## Research Question

**Primary Question:**
Does the ICC_slope pattern (21% between-person variance) replicate across What, Where, When domains?

**Scope:**
This RQ examines individual differences in forgetting slopes computed separately for What, Where, and When domains. Tests whether between-person variance in forgetting rates is consistent across episodic memory domains. N=100 participants with domain-specific slopes extracted from Ch5 analyses.

**Theoretical Framing:**
Replication analysis to determine whether individual differences in forgetting are domain-general or domain-specific. If slopes show similar ICC patterns across domains, this supports domain-general forgetting processes. If When domain shows different patterns, this may reflect measurement issues rather than theoretical differences.

---

## Theoretical Background

**Relevant Theories:**
- **Domain-specific consolidation theory**: Different memory domains may show different individual difference patterns due to distinct neural substrates and consolidation processes
- **Domain-general forgetting theory**: Individual differences in forgetting reflect general cognitive aging or strategic factors that operate similarly across domains
- **Measurement theory**: ICC patterns may reflect measurement quality rather than theoretical differences, particularly for When domain with known item exclusion issues

**Key Citations:**
(To be enhanced by rq_scholar)

**Theoretical Predictions:**
Domain-general forgetting theory predicts similar ICC_slope values across What, Where, When domains. Domain-specific theory predicts different ICC patterns. Measurement issues predict When domain to show atypical patterns due to high item exclusion rate.

**Literature Gaps:**
Limited research on domain-specificity of individual differences in episodic memory forgetting rates.

---

## Hypothesis

**Primary Hypothesis:**
What and Where domains will show ICC_slope H 20% similar to overall findings from Ch5. When domain will show lower ICC_slope due to measurement issues with 77% item exclusion.

**Secondary Hypotheses:**
bootstrap (1000 replications, seed=42) confidence intervals for What and Where ICC_slope values will overlap, while When domain 95% CI will be lower and potentially non-overlapping.

**Theoretical Rationale:**
Based on Ch5 findings where When domain showed measurement challenges with high item exclusion rates. What and Where domains have better item quality and should replicate the overall ICC_slope pattern. Individual differences in forgetting should be most reliable for well-measured domains.

**Expected Effect Pattern:**
ICC_slope_What H 0.19-0.22, ICC_slope_Where H 0.19-0.22, ICC_slope_When H 0.05-0.15. When domain significantly lower than What/Where domains in pairwise comparisons.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object naming/identity domain with domain-specific forgetting slopes

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Spatial location domain with domain-specific forgetting slopes

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order domain with domain-specific forgetting slopes

**Inclusion Rationale:**
Analyzes all three episodic memory domains to test domain-generality vs domain-specificity of individual differences in forgetting rates. Uses domain-specific slope estimates from Ch5 domain analyses to compute domain-specific ICC values.

**Exclusion Rationale:**
None - all three domains required for comprehensive test of domain-specificity hypothesis.

---

## Analysis Approach

**Analysis Type:**
Variance component analysis (ICC computation) with bootstrap (1000 replications, seed=42) confidence intervals and pairwise comparisons

**High-Level Workflow:**

**Step 1:** Extract domain-specific slopes
- Load per-participant slopes from Ch5 5.2.1 (What), 5.2.2 (Where), 5.2.3 (When)
- Alternatively, re-fit domain-specific LMMs if slopes not available
- Verify 100 participants with complete slope data

**Step 2:** Compute ICC for each domain's slope variance
- ICC_slope_What: Between-person variance / Total variance for What slopes
- ICC_slope_Where: Between-person variance / Total variance for Where slopes  
- ICC_slope_When: Between-person variance / Total variance for When slopes
- Use variance component estimation

**Step 3:** bootstrap (1000 replications, seed=42) confidence intervals
- Bootstrap resample participants (1000 iterations)
- Compute ICC for each bootstrap (1000 replications, seed=42) sample
- Extract 95% confidence intervals for each domain ICC

**Step 4:** Statistical comparisons
- Test differences between domain ICCs using bootstrap (1000 replications, seed=42) samples
- Pairwise comparisons: What vs Where, What vs When, Where vs When
- Report effect sizes for ICC differences

**Step 5:** Model diagnostics
- Check slope distributions for normality
- Identify potential outliers in domain-specific slopes
- Assess impact of outliers on ICC estimates

**Step 6:** Cross-validation
- Split-half reliability for ICC estimates
- Compare ICC estimates from random halves of participants

**Step 7:** Power analysis
- Post-hoc power for detecting ICC differences
- Sensitivity analysis for smallest detectable ICC difference

**Expected Outputs:**
- data/step01_domain_slopes.csv (extracted slopes from Ch5)
- data/step02_icc_estimates.csv (ICC values by domain)
- data/step03_bootstrap (1000 replications, seed=42)_cis.csv (confidence intervals)
- data/step04_pairwise_comparisons.csv (domain comparison statistics)
- data/step05_outlier_analysis.csv (slope outlier diagnostics)
- data/step06_split_half_reliability.csv (cross-validation results)
- data/step07_power_analysis.csv (power and sensitivity analysis)
- results/icc_replication_summary.md (text summary for thesis)
- plots/icc_comparison.png (ICC estimates with CIs by domain)
- plots/slope_distributions.png (domain-specific slope histograms)

**Success Criteria:**
- [ ] Extract complete slope data for all 100 participants across 3 domains
- [ ] Compute ICC_slope for What, Where, When domains
- [ ] bootstrap (1000 replications, seed=42) 95% CIs for each ICC estimate
- [ ] Test statistical differences between domain ICCs
- [ ] What/Where ICCs in range 0.15-0.30 (realistic for individual differences)
- [ ] When ICC potentially lower due to measurement issues
- [ ] bootstrap (1000 replications, seed=42) CIs exclude 0.0 for What/Where domains
- [ ] Split-half reliability r > 0.70 for ICC estimates
- [ ] Power > 0.80 for detecting medium ICC differences (d = 0.50)

---

## Data Source

**Data Type:**
DERIVED (from Ch5 domain-specific analyses)

### DERIVED Data Sources:

**Source RQs:**
- Ch5 5.2.1 (What domain analysis)
- Ch5 5.2.2 (Where domain analysis)  
- Ch5 5.2.3 (When domain analysis)

**File Paths:**
- results/ch5/5.2.1/data/step##_participant_slopes.csv (What domain slopes)
- results/ch5/5.2.2/data/step##_participant_slopes.csv (Where domain slopes)
- results/ch5/5.2.3/data/step##_participant_slopes.csv (When domain slopes)

**Dependencies:**
Ch5 domain analyses (5.2.1, 5.2.2, 5.2.3) must complete LMM fitting and participant-level slope extraction before this RQ can run.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from Ch5 domain analyses (inherited inclusion criteria)
- [ ] Subset: None - requires complete slope data for all participants

**Items:**
- N/A (analysis uses participant-level slopes, not item-level data)

**Tests:**
- [x] All 4 tests (slopes computed across T1-T4 forgetting trajectory)

---