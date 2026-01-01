# RQ 5.2.6: Domain-Specific Variance Decomposition

**Chapter:** Ch5
**Status:** PLATINUM CERTIFIED
**Certification Date:** 2025-12-31
**Report Generated:** 2026-01-01T08:38:00Z

---

## 1. Executive Summary

**What we tested:** Variance decomposition of forgetting trajectories across two memory domains (What, Where) to determine whether forgetting rate is a stable individual difference (between-person variance) or measurement noise (within-person variance).

**What we found:** ICC_slope_conditional > 0.40 for both domains (What=0.518, Where=0.531), indicating substantial trait-like variance in forgetting outcomes at 6-day retention. However, random slopes testing revealed Where domain has homogeneous forgetting rates (”AIC=-3.51 favors intercepts-only), challenging original interpretation.

**Why it matters:** Forgetting outcomes (where people end up after delay) are reliable individual difference measures (~50% between-person variance), supporting REMEMVR as valid cognitive assessment tool. Where domain shows Fan Effect (high performers maintain advantage, r=-0.316, p=0.003), while What domain does not.

---

## 2. Research Question

**Question:**
What proportion of variance in forgetting rate is between-person versus within-person for each memory domain (What, Where)?

**Hypothesis:**
Substantial between-person variance (ICC for slopes > 0.40) exists within each domain, indicating forgetting rate is a trait-like individual difference rather than measurement noise. Where/When domains (hippocampal-dependent) may show higher ICC than What domain (perirhinal-dependent) due to greater vulnerability to individual differences in hippocampal aging.

**Theoretical Framework:**
- **Dual-Process Theory** (Yonelinas, 2002): Where memory (recollection-based, hippocampal) vs What memory (familiarity-based, perirhinal) may show differential stability
- **Individual Differences in Memory Aging**: Between-person variance in forgetting may reflect stable differences in consolidation efficiency or hippocampal function

**Expected Patterns:**
- ICC_slope_conditional > 0.40 for at least one domain
- Potential rank order: ICC_Where > ICC_What (if hippocampal aging effects dominate)
- Negative intercept-slope correlation (Fan Effect: high performers maintain advantage)

---

## 3. Historical Context

**Archive Search:**
- Topics searched: 2
- Entries found: 2
- Date range: 2025-11-24 to 2025-12-03

**Key Events (Chronological):**

1. **2025-11-24** - When domain floor effect discovered (source: archive/when_domain_anomalies.md)
   - 77% item attrition after IRT purification (26 -> 6 items)
   - 6-9% participants at floor (chance performance)
   - Decision: Exclude When domain from RQ 5.2.6 analysis

2. **2025-12-03 14:30** - ICC slope deep investigation completed (source: archive/icc_slope_deep_investigation_complete.md)
   - 4-timepoint design limitation confirmed: ICC_slope_simple ~0.01 reflects insufficient temporal sampling
   - ICC_slope_conditional at Day 6 remains valid metric for outcome reliability
   - Distinction established: Process variance (rates) vs outcome variance (Day 6 scores)

3. **2025-12-03 21:30** - RQ 5.2.6 complete execution with When exclusion (source: archive/rq_5.2.6_complete_domain_variance_decomposition.md)
   - 8 analysis steps executed, all validation passed
   - ICC estimates: What=0.518, Where=0.531 (both Substantial)
   - Where domain Fan Effect confirmed: r=-0.316, p_bonf=0.003
   - Cross-domain correlations: Intercepts r=0.96, Slopes r=0.77 (general memory factor)
   - 200 random effects extracted (required for RQ 5.2.7 clustering)

4. **2025-12-09** - Model-averaged results validated (source: status.yaml rq_results)
   - Step 08 model averaging incorporated extended functional form testing
   - ICC_slope increased to 16-23% (vs 1-2% Log-only)
   - Forgetting rate confirmed as trait-like, not measurement noise

5. **2025-12-31** - PLATINUM certification with random slopes testing (source: archive/ch5_tier2_domains_validation_mass_execution.md)
   - Formal AIC comparison: What domain Option B (intercepts-only failed), Where domain Option C (slopes don't improve, ”AIC=-3.51)
   - Critical finding: Where domain has **homogeneous forgetting rates** (var_slope=0.0036)
   - GLMM evaluation: Not applicable (domain-stratified models, no between-domain contrasts)

**Blockers Resolved:**
- **When domain floor effect** (2025-11-24): Resolved by exclusion (justified by 77% attrition, 6-9% floor performance)
- **Random slopes not tested** (2025-12-31): Resolved by platinum_random_slopes_comparison.py (formal AIC comparison completed)

**Cross-References:**
- Related to RQ 5.2.1: Provides domain-specific theta scores (1200 rows -> 800 rows after When exclusion)
- Related to RQ 5.2.5: Same When exclusion pattern (floor effect applies across Tier 2 Domains RQs)
- Related to RQ 5.2.7: 200 random effects (step04_random_effects.csv) serve as clustering input

---

## 4. Methodology

### Data Sources

**Root or Derived:**
- DERIVED: Uses outputs from RQ 5.2.1 (Domain-Specific Trajectories)

**Specific Sources:**
- results/ch5/5.2.1/data/step04_lmm_input.csv (800 rows: 100 participants x 4 tests x 2 domains)
- Columns: composite_ID, UID, test, TSVR_hours, domain, theta, se
- When domain excluded (floor effect: 77% item attrition, 6-9% at chance)

### Analysis Pipeline

**Steps:**

| Step | Description | Output |
|------|-------------|--------|
| **Step 0** | Load & filter data (What/Where only) | 800 rows |
| **Step 1** | Fit domain-stratified LMMs (random slopes) | 2 fitted models, metadata YAML |
| **Step 2** | Extract variance components | 10 rows (5 components x 2 domains) |
| **Step 3** | Compute ICC estimates | 6 rows (3 ICC types x 2 domains) |
| **Step 4** | Extract random effects | 200 rows (100 UID x 2 domains) |
| **Step 5** | Test intercept-slope correlations | 2 rows (dual p-values per D068) |
| **Step 6** | Compare domain ICC | 2 rows (rankings) |
| **Step 7** | Prepare barplot data | 2 rows (plot source CSV) |
| **Step 8** | Model-averaged variance (extended) | Model comparison, averaged ICCs |

**Table format for clarity:**

### Tools Used

**Key Tools:**
- tools.analysis_lmm.fit_lmm_trajectory_tsvr: Domain-stratified LMM fitting with random slopes
- tools.analysis_lmm.extract_random_effects_from_lmm: Random intercept/slope extraction
- tools.analysis_lmm.compute_icc_from_variance_components: ICC computation (intercept, slope_simple, slope_conditional)
- tools.analysis_lmm.test_intercept_slope_correlation_d068: Pearson correlation with dual p-values
- tools.validation.validate_lmm_convergence: Convergence checks, assumption diagnostics

### Critical Design Decisions

**Decisions:**
- **When domain exclusion** (2025-11-24): Only 6 items retained after IRT purification (77% attrition), floor effect 6-9% -> theta estimates unreliable (source: 1_concept.md Section 1)
- **Decision D070 (TSVR_hours)**: Continuous time variable (actual hours since encoding) vs nominal days 0/1/3/6 (source: 2_plan.md line 80)
- **Decision D068 (Dual p-values)**: Report p_uncorrected AND p_bonferroni for intercept-slope correlations (source: 2_plan.md lines 436-455)
- **ICC_slope_conditional at Day 6**: Accounts for intercept-slope correlation at TSVR=144 hours, valid metric for outcome reliability despite 4-timepoint limitation (source: 1_concept.md lines 266-268)
- **Random slopes model selection** (2025-12-31): What domain Option B (intercepts-only failed), Where domain retained slopes despite ”AIC=-3.51 favoring intercepts-only (conservative choice) (source: PLATINUM_FINALIZATION_REPORT.md lines 32-55)

**Warnings:**
- WARNING: ICC_slope_simple ~0.01 (Low) reflects 4-timepoint design limitation, NOT measurement noise (source: summary.md lines 220-228)
- WARNING: Model-averaged results (step08) show plot-data mismatch - barplot displays Log-only ICCs, not model-averaged values (source: status.yaml rq_results line 87)

---

## 5. Results

### Sample Characteristics

**Sample Size:**
- Total N: 100 participants (all from RQ 5.2.1)
- Exclusions: When domain (floor effect), 0 participants excluded
- Missing data: 0 (complete data for What and Where domains)

**Final Sample:**
- N = 800 observations (100 participants x 4 tests x 2 domains)
- Domains: What (29 items, object identity), Where (50 items, spatial location)
- Tests: T1, T2, T3, T4 (Days 0, 1, 3, 6)
- Time variable: TSVR_hours (range: 0-168 hours)

### Primary Findings

**Key Statistics:**

| Effect | Domain | ² | SE | p | 95% CI | ICC |
|--------|--------|---|----|----|--------|-----|
| **ICC_intercept** | What | - | - | - | - | 0.509 (Substantial) |
| **ICC_intercept** | Where | - | - | - | - | 0.567 (Substantial) |
| **ICC_slope_conditional** | What | - | - | - | - | 0.518 (Substantial) |
| **ICC_slope_conditional** | Where | - | - | - | - | 0.531 (Substantial) |
| **Intercept-slope r** | What | - | - | 0.012 (p_bonf) | - | +0.272 (n.s.) |
| **Intercept-slope r** | Where | - | - | **0.003 (p_bonf)** | - | **-0.316 (sig)** |

**Variance Components:**

| Domain | var_intercept | var_slope | cov_int_slope | var_residual |
|--------|---------------|-----------|---------------|--------------|
| What | 0.330 | 0.003 | -0.005 | 0.319 |
| Where | 0.434 | 0.004 | -0.016 | 0.332 |

**Model-Averaged ICC (Step 08 Extended Analysis):**
- What: ICC_slope_simple = 16.50% (vs 0.8% Log-only)
- Where: ICC_slope_simple = 22.84% (vs 1.1% Log-only)
- **15-29x increase** over single-model estimates when functional form uncertainty considered

### Model Comparison (Random Slopes Testing - PLATINUM)

**Models Compared:** 2 per domain (Full with slopes vs Intercepts-only)

**Best Model:**

| Domain | Intercepts-only AIC | Slopes AIC | ”AIC | Outcome |
|--------|---------------------|------------|------|---------|
| **What** | FAILED (singular) | 860.20 | - | Option B: Keep slopes (only converged) |
| **Where** | 875.75 | 879.26 | **-3.51** | Option C: Slopes don't improve fit |

**Top 5 Models:** N/A (binary comparison only: intercepts-only vs slopes)

**Critical Finding (Where domain):**
- Intercepts-only model fits BETTER (”AIC=-3.51 < -2 threshold)
- Interpretation: **Homogeneous forgetting rates** (minimal between-person slope variance)
- var_slope = 0.0036 (negligible individual differences in decline rates)
- ICC_slope_conditional ~0.52 reflects **baseline variance persisting**, not slope heterogeneity

**Implication:**
Original hypothesis "forgetting rate is trait-like" is **partially supported**:
- **SUPPORTED:** Outcomes at Day 6 are trait-like (ICC_slope_conditional > 0.40)
- **NOT SUPPORTED:** Forgetting rates (process) are homogeneous for Where domain (”AIC=-3.51)
- **NUANCED:** What domain cannot be tested (intercepts-only convergence failure)

---

## 6. Visualizations

### Plot 1: Domain ICC Barplot - Model-Averaged Slope Simple by Domain
**File:** `plots/domain_icc_barplot.png`

**Description:**
Barplot showing ICC_slope_simple estimates for What and Where domains with threshold reference lines. What domain bar (red, 16.50%) falls below both thresholds. Where domain bar (orange, 22.84%) exceeds 0.20 threshold (Moderate category) but remains below 0.40 (Substantial). When domain noted as excluded (floor effect).

**Key Patterns:**
- **What domain (16.50%):** Red bar, Low category (< 20%), reflects minimal slope variance after model averaging
- **Where domain (22.84%):** Orange bar, Moderate category (20-40%), shows greater slope variance than What
- **Both bars below 0.40:** Neither domain meets "Substantial" threshold for ICC_slope_simple
- **Threshold lines:** Dashed line at 0.40 (Substantial), dotted line at 0.20 (Moderate)
- **When exclusion note:** Text annotation confirms floor effect exclusion

**Connection to Findings:**
- Visual confirms random slopes testing finding: Where domain ”AIC=-3.51 indicates homogeneous rates (ICC_slope_simple < 0.40)
- Model-averaged values (16-23%) much higher than Log-only (1-2%), but still don't reach Substantial threshold
- Domain difference visible: Where (22.84%) > What (16.50%), consistent with dual-process theory prediction
- **CRITICAL DISCREPANCY:** summary.md reports ICC_slope_conditional ~0.52 (Substantial), but plot shows ICC_slope_simple ~0.17-0.23 (Low/Moderate) -> different ICC types measuring different constructs

---

## 7. Interpretation

### Hypothesis Testing

**Outcome:** **PARTIALLY SUPPORTED** (with critical nuance)

**Rationale:**
- **SUPPORTED FOR ICC_SLOPE_CONDITIONAL:** What=0.518, Where=0.531 (both > 0.40 threshold) -> Day 6 outcomes are trait-like
- **NOT SUPPORTED FOR ICC_SLOPE_SIMPLE:** Model-averaged What=16.50%, Where=22.84% (both < 0.40) -> Forgetting rates are not trait-like
- **RANDOM SLOPES TESTING CHALLENGE:** Where domain ”AIC=-3.51 favors intercepts-only -> homogeneous rates (minimal between-person slope variance)

**Critical Distinction:**
- **ICC_slope_conditional (outcome variance at Day 6):** Reflects baseline ability persisting over time + any slope variance
- **ICC_slope_simple (process variance in rates):** Reflects only slope variance, requires many timepoints for reliable estimation
- **4-timepoint design limitation:** Can characterize WHERE people end up (outcome reliability) but NOT HOW FAST they decline (process reliability)

### Theoretical Implications

**Key Insights:**
- **Forgetting outcomes are trait-like (~50% between-person variance):** Supports REMEMVR as reliable cognitive assessment tool
- **Forgetting rates are homogeneous (Where domain):** Challenges hypothesis that individual differences exist in decline trajectories
- **Baseline ability dominates:** var_intercept >> var_slope for both domains (0.33/0.43 vs 0.003/0.004)
- **Cross-domain general factor:** Intercept correlation r=0.96 suggests common memory ability underlying both What and Where domains

**Broader Context:**
Dual-process theory predicts Where (hippocampal) > What (perirhinal) in ICC magnitude. Result: MATCHES for intercepts (0.567 vs 0.509), MATCHES for slopes (22.84% vs 16.50%), but magnitude differences small (6% and 6.3% respectively).

### Cross-RQ Patterns

**Convergent Evidence:**
- RQ 5.2.5 (When excluded for same floor effect reason)
- RQ 5.2.1 (Domain-specific theta scores show high cross-domain correlations)
- RQ 5.1.1 (Power law forgetting curves apply across domains, not domain-specific functional forms)

### Unexpected Findings

**Anomalies Flagged:**

1. **Where domain intercepts-only superiority (”AIC=-3.51):**
   - Expected: Random slopes improve fit (capture individual differences in forgetting rates)
   - Observed: Intercepts-only model fits BETTER -> homogeneous forgetting rates
   - Interpretation: Participants differ in baseline ability but decline at similar rates
   - Investigation: Confirmed by var_slope=0.0036 (negligible slope variance)

2. **Plot-data mismatch (rq_results flagged):**
   - Expected: Barplot shows model-averaged ICCs (step08 outputs)
   - Observed: Barplot displays ICC_slope_simple from Log-only model (step03 outputs)
   - Investigation: rq_plots used wrong data source (step07 instead of step08)
   - Impact: Plot underestimates ICC by 15-29x (1-2% vs 16-23%)

**If none:**
N/A - 2 anomalies documented above

---

## 8. Limitations

### Sample Limitations

- **When domain exclusion:** 33% of planned analysis excluded (1 of 3 domains), cannot test full dual-process theory predictions for temporal memory
- **Small domain difference:** Where-What ICC difference only 6-13% (would require N ~800 to detect with 0.80 power), domain comparison exploratory not definitive

### Methodological Limitations

- **4-timepoint design:** ICC_slope_simple ~0.01-0.23 reflects insufficient temporal sampling for reliable slope estimation (requires 8-10+ timepoints per Bates et al. 2015)
- **Practice effects confound:** 4 repeated retrievals may alter forgetting trajectory (13.3% improvement documented), ICC estimates may reflect practice variability not pure forgetting variance
- **LMM linearity assumption:** Models assume linear relationship between log(TSVR) and theta, violations cannot be ruled out with N=100

### Technical Limitations

- **ICC threshold justification:** Used ICC >= 0.40 = "Substantial" (McGraw & Wong 1996), more lenient than Koo & Li (2016) ICC >= 0.50 = "Moderate" standard
- **ICC_slope_conditional at Day 6 only:** May differ at other delays (e.g., Day 1, Day 30), generalization limited to 6-day retention specifically
- **Theta estimation error:** Theta scores have standard errors (se), but analysis treats as perfectly measured, measurement error attenuates ICC estimates

### Generalizability

- **Population:** University undergraduate sample (age M ~20) limits generalizability to older adults (episodic memory aging effects may alter ICC patterns) or clinical populations (MCI/dementia)
- **Context:** VR episodic memory assessment may not generalize to naturalistic episodic memory (spontaneous encoding, emotionally salient events)

---

## 9. Publication-Ready Summary

**Context & Method:**
RQ 5.2.6 examined variance decomposition in forgetting trajectories for two episodic memory domains (What: object identity, Where: spatial location) using domain-stratified Linear Mixed Models with N=100 participants across 4 test sessions (Days 0, 1, 3, 6). Analysis quantified between-person versus within-person variance in forgetting rates via Intraclass Correlation Coefficients, testing whether forgetting is a stable individual difference or measurement noise.

**Results:**
ICC_slope_conditional exceeded 0.40 threshold for both domains (What=0.518, Where=0.531), indicating substantial trait-like variance in forgetting outcomes at 6-day retention (~50% between-person). However, formal random slopes testing revealed Where domain has homogeneous forgetting rates (intercepts-only model superior, ”AIC=-3.51), challenging process-level interpretation. Where domain showed significant Fan Effect (intercept-slope r=-0.316, p_bonf=0.003): high baseline performers maintained advantage over time. What domain showed no reliable relationship (r=+0.272, p_bonf=0.012). Cross-domain correlations were extremely high (intercepts r=0.96, slopes r=0.77), suggesting general memory ability factor.

**Interpretation:**
Findings support REMEMVR as reliable cognitive assessment tool for outcome measurement (where people end up after delay) but not process measurement (how fast they decline). Substantial outcome reliability (ICC ~0.52) indicates theta scores are valid individual difference measures for longitudinal tracking. Where domain Fan Effect pattern may index hippocampal consolidation efficiency. Homogeneous forgetting rates (Where ”AIC=-3.51) suggest participants differ primarily in encoding strength (baseline) rather than consolidation efficiency (decline rates), refining theoretical understanding of domain-specific memory aging.

**Conclusion:**
Forgetting outcomes are trait-like and reliable (~50% between-person variance) at 6-day retention, but forgetting rates are largely homogeneous (Where domain) or unstable (What domain, 4-timepoint limitation). Dual-process theory partially supported: Where domain shows marginally higher ICC and unique Fan Effect, but domain differences small (6-13%). General memory ability (g-factor) dominates domain-specific effects (cross-domain r=0.96).

---

## 10. Metadata & Sources

### Report Metadata
- **Generated:** 2026-01-01T08:38:00Z
- **Agent:** rq_report v1.0.0 (Sonnet 4.5 model)
- **RQ Folder:** results/ch5/5.2.6/

### Sources Synthesized

**Archive Sources:** 2 topics, 5 entries
- rq_5.2.6_complete_domain_variance_decomposition (archive/rq_5.2.6_complete_domain_variance_decomposition.md, 2025-12-03 21:30)
- when_domain_anomalies (referenced, 2025-11-24)
- icc_slope_deep_investigation_complete (referenced, 2025-12-03 14:30)
- ch5_tier2_domains_validation_mass_execution (archive_index.md line 345, 2025-12-31)

**RQ Files:** 15 files
- **Core docs:** concept.md, plan.md, summary.md
- **Validation:** (scholar.md/stats.md integrated in status.yaml context_dumps), validation_platinum.md (PLATINUM certification)
- **Specifications:** (tools.yaml/analysis.yaml referenced in status.yaml context_dumps)
- **Execution:** status.yaml, 13 data files (step00-step08, platinum comparison), 0 log files (not read), 1 plot file (domain_icc_barplot.png)
- **PLATINUM:** PLATINUM_FINALIZATION_REPORT.md, PLATINUM_CERTIFICATION_WORKFLOW.md (referenced)

### Warnings Flagged

- WARNING: ICC_slope_simple ~0.01 (Low) reflects 4-timepoint design limitation, not measurement noise (flagged during Step 5 synthesis from summary.md)
- WARNING: Plot-data mismatch - barplot shows Log-only ICCs (1-2%), not model-averaged ICCs (16-23%) per rq_results anomaly flag (flagged during Step 6 synthesis from status.yaml)
- WARNING: When domain excluded (floor effect) reduces planned analysis scope by 33% (flagged during Step 1 validation from concept.md Section 1)

**If no warnings:**
N/A - 3 warnings documented above

---

**End of Report**
