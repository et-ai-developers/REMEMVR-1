# RQ 6.3.4: ICC by Domain - Is Confidence Decline More Trait-Like for Some Domains?

**Chapter:** 6
**Type:** Domain Confidence
**Subtype:** ICC by Domain
**Full ID:** 6.3.4

---

## Research Question

**Primary Question:**
Is confidence decline more trait-like (individual difference) for some memory domains than others?

**Scope:**
This RQ examines domain-stratified variance decomposition of confidence trajectories across What/Where/When memory domains. Analyzes N=100 participants x 4 tests x 3 domains = 1200 observations derived from RQ 6.3.1 (domain-specific confidence trajectories). Computes ICC_intercept and ICC_slope per domain using random-effects LMMs.

**Theoretical Framing:**
ICC decomposition reveals whether forgetting rates show individual consistency (trait-like, high ICC_slope) or state-like variability (low ICC_slope). If 5-level confidence data reveals slope variance (per RQ 6.1.4 hypothesis), some domains may show higher ICC_slope than others, indicating domain-specific trait differences in metacognitive monitoring. This extends Ch5 5.2.6 accuracy findings (all ICC_slope approximately 0 for dichotomous data).

---

## Theoretical Background

**Relevant Theories:**
- **Dual-Process Theory** (Yonelinas, 2002): What domain relies on familiarity (fast, automatic), while Where/When require recollection (slow, effortful). Metacognitive monitoring may differ across these processes.
- **Consolidation Theory** (Dudai, 2004): Hippocampal-dependent domains (Where, When) show greater consolidation vulnerability. If metacognitive monitoring tracks memory processes, these domains may show higher ICC_slope.
- **Measurement Theory**: 5-level ordinal confidence data provides 2.3x more information per response than dichotomous accuracy (0/1). If ICC_slope differences exist, richer measurement may reveal them.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Where/When domains (hippocampal, recollection-based) may show HIGHER ICC_slope than What domain (familiarity-based) if recollection processes have more individual variability in metacognitive access. Alternatively, if metacognitive monitoring is domain-general, ICC_slope may be equivalent across domains.

**Literature Gaps:**
Domain-specific ICC decomposition for confidence trajectories is unexplored. Ch5 5.2.6 found all ICC_slope approximately 0 for accuracy (dichotomous data limitation). This RQ tests whether 5-level confidence data reveals domain-specific trait variance.

---

## Hypothesis

**Primary Hypothesis:**
ICC_slope may differ by domain. If 5-level confidence data reveals slope variance (per RQ 6.1.4), some domains may show higher ICC_slope than others. Recollection-based domains (Where, When) may show more individual variability in metacognitive monitoring than familiarity-based What domain.

**Secondary Hypotheses:**
Null hypothesis: All domains show ICC_slope approximately 0 (paralleling Ch5 5.2.6 accuracy pattern), suggesting no domain-specific trait differences in confidence decline rates.

**Theoretical Rationale:**
Recollection processes (Where/When) require controlled retrieval with more conscious monitoring. This may create more individual variability in metacognitive tracking. Familiarity processes (What) are automatic and may show less variability in confidence judgments. However, if metacognitive monitoring is domain-general (single monitoring system for all memory types), ICC_slope should be equivalent across domains.

**Expected Effect Pattern:**
Compare ICC_slope_What vs ICC_slope_Where vs ICC_slope_When. If any domain shows ICC_slope > 0.10 while others approximate 0, evidence for domain-specific trait variance. Compare to Ch5 5.2.6 where all ICC_slope_accuracy approximately 0 for all domains.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming domain
  - Theoretical basis: Perirhinal cortex, familiarity-based retrieval

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where tags combined (following Ch5 5.2.X convention)
  - Theoretical basis: Hippocampal, recollection-based retrieval

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence domain
  - Theoretical basis: Hippocampal, recollection-based retrieval

**Inclusion Rationale:**
All three WWW (What/Where/When) episodic memory domains included to enable comprehensive domain-stratified variance decomposition. Compares familiarity-based (What) vs recollection-based (Where, When) metacognitive monitoring.

**Exclusion Rationale:**
Note: When domain may have limited items after IRT purification in RQ 6.3.1 (floor effects documented in Ch5). If fewer than 10 items retained, ICC estimates for When domain may be unstable. This will be documented in results if encountered.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) with random intercepts and random slopes (by participant) for variance decomposition. ICC (Intraclass Correlation Coefficient) computation per domain.

**High-Level Workflow:**

**Step 1:** Fit domain-stratified LMMs with random slopes
- Separate LMM per domain: What, Where, When
- Model: theta_confidence ~ Time + (Time | UID)
- Extract variance components: var_intercept, var_slope, cov_int_slope, var_residual per domain

**Step 2:** Extract variance components per domain
- Create variance components table (15 rows: 3 domains x 5 components)
- Components: var_intercept, var_slope, cov_int_slope, var_residual, total_variance

**Step 3:** Compute ICC per domain
- ICC_intercept = var_intercept / (var_intercept + var_residual)
- ICC_slope_simple = var_slope / (var_slope + var_residual)
- ICC_slope_conditional at Day 6 (accounting for covariance)
- Create ICC estimates table (9 rows: 3 domains x 3 ICC types)

**Step 4:** Extract random effects per domain
- 100 participant random intercepts per domain
- 100 participant random slopes per domain
- Create random effects table (300 rows: 100 participants x 3 domains)
- Required for potential downstream clustering analyses

**Step 5:** Compare ICC_slope across domains
- Test if ICC_slope differs significantly between domains
- Rank domains by ICC_slope (highest to lowest individual trait variance)
- Identify which domain shows most trait-like confidence decline

**Step 6:** Compare to Ch5 5.2.6
- Ch5 5.2.6 findings: All domains showed ICC_slope approximately 0 for accuracy
- Test if 5-level confidence data reveals domain differences that dichotomous accuracy data missed
- Document whether ICC_slope_confidence > ICC_slope_accuracy for any domain

**Expected Outputs:**
- data/step02_variance_components.csv (15 rows: 3 domains x 5 variance components)
- data/step03_icc_estimates.csv (9 rows: 3 domains x 3 ICC types)
- data/step04_random_effects.csv (300 rows: 100 participants x 3 domains, intercept + slope per domain)
- results/step05_domain_icc_comparison.csv (domain ranking by ICC_slope)
- results/step06_ch5_comparison.csv (Ch5 5.2.6 comparison table)

**Success Criteria:**
- All 3 domain-stratified LMMs converge successfully
- ICC values in valid range [0, 1]
- Variance components all non-negative
- 300 random effects extracted (100 participants x 3 domains)
- Ch5 5.2.6 comparison documented (ICC_slope_accuracy vs ICC_slope_confidence per domain)
- Interpretation addresses: Does 5-level data reveal domain-specific trait variance that dichotomous data missed?

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.3.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 6.3.1 (Domain Confidence Trajectories)

**File Paths:**
- results/ch6/6.3.1/data/step03_theta_confidence_domain.csv (1200 rows: 100 participants x 4 tests x 3 domains)

**Dependencies:**
RQ 6.3.1 must complete Steps 0-3 (data extraction, IRT calibration with 3-factor GRM for What/Where/When, theta score generation) before this RQ can run. RQ 6.3.1 provides domain-stratified confidence ability estimates (theta_confidence) required for variance decomposition.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 6.3.1 (inherited inclusion criteria)
- Expected N=100 participants unless RQ 6.3.1 excluded any

**Items:**
- N/A (theta scores already aggregated across items per domain)
- Item-level filtering completed in RQ 6.3.1 IRT purification

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) inherited from RQ 6.3.1
- Time variable: TSVR (actual hours since encoding), not nominal days

**Domains:**
- [x] What domain (object identity)
- [x] Where domain (spatial location: -L-, -U-, -D- combined)
- [x] When domain (temporal order)
- Note: When domain may be excluded if fewer than 10 items survived RQ 6.3.1 purification (floor effects documented in Ch5)

---

**Cross-Chapter Comparison:**
This RQ directly compares to Ch5 5.2.6 (ICC by Domain for accuracy). Critical test: Does 5-level confidence measurement reveal domain-specific trait variance that dichotomous accuracy measurement (0/1) could not detect?

---
