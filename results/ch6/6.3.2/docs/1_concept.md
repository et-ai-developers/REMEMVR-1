# RQ 6.3.2: Domain Confidence Calibration

**Chapter:** 6
**Type:** Domain Confidence
**Subtype:** Calibration
**Full ID:** 6.3.2

---

## Research Question

**Primary Question:**
Are people better calibrated for some episodic memory domains (What/Where/When) than others?

**Scope:**
This RQ examines calibration (confidence-accuracy alignment) across three episodic memory domains: What (object identity), Where (spatial location), and When (temporal order). Analysis uses N=100 participants x 4 test sessions x 3 domains = 1200 observations. Calibration is computed as the difference between standardized confidence theta and standardized accuracy theta per participant-domain-timepoint combination.

**Theoretical Framing:**
If metacognitive monitoring varies by memory domain, calibration quality should differ across What/Where/When. Specifically, the When domain may show better calibration despite floor effects in accuracy: if both accuracy AND confidence are low, calibration remains good (correctly uncertain). Conversely, What/Where domains may exhibit overconfidence (moderate accuracy but high confidence). This question addresses whether metacognitive processes track domain-specific memory quality or operate uniformly across domains.

---

## Theoretical Background

**Relevant Theories:**
- **Dual-Process Theory** (Yonelinas, 2002): Familiarity-based retrieval (What domain) may generate higher confidence judgments than recollection-based retrieval (Where/When domains), potentially creating domain-specific calibration patterns.
- **Metacognitive Monitoring Theory**: Metacognitive judgments may rely on different cues for different memory domains. Object memory (What) may generate strong fluency cues that inflate confidence relative to accuracy, while spatial/temporal memory (Where/When) may provide less misleading fluency signals.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
When domain may show better calibration than What/Where despite lower absolute accuracy: if both confidence and accuracy track the floor effect, calibration (their difference) remains good. What/Where domains may show overconfidence due to retrieval fluency signals that inflate confidence beyond actual accuracy levels.

**Literature Gaps:**
Domain-specific calibration in episodic memory has not been systematically examined, particularly in ecologically valid VR contexts. Most calibration research treats memory as unitary rather than examining What/Where/When dissociations.

---

## Hypothesis

**Primary Hypothesis:**
When domain shows BETTER calibration than What/Where domains despite floor effects. Calibration quality ranking: When > Where > What. Rationale: When domain's floor effects should affect both accuracy and confidence similarly, maintaining calibration. What/Where domains may show overconfidence (moderate accuracy but higher confidence due to fluency signals).

**Secondary Hypotheses:**
Domain × Time interaction: Calibration differences between domains may emerge or strengthen over retention interval as differential forgetting rates interact with metacognitive monitoring processes.

**Theoretical Rationale:**
If metacognitive monitoring uses domain-specific cues, calibration quality should vary by domain. What domain's reliance on familiarity may generate false fluency (high confidence for moderate accuracy). Where domain's recollection requirement may reduce false fluency. When domain's floor effects may paradoxically create good calibration through matched low accuracy and low confidence.

**Expected Effect Pattern:**
Significant Domain main effect on calibration (p < 0.05). Post-hoc contrasts reveal When domain has lowest |calibration| (best calibrated). Domain × Time interaction possible but not predicted (calibration patterns may be stable or evolve).

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object naming/identity confidence and accuracy

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where tags combined for domain-level analysis

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal sequence confidence and accuracy

**Inclusion Rationale:**
All three core episodic memory domains (What/Where/When) are necessary to test domain-specific calibration hypothesis. Domain-stratified IRT from RQ 6.3.1 provides confidence theta estimates; domain-stratified IRT from Ch5 5.2.1 provides accuracy theta estimates.

**Exclusion Rationale:**
None - comprehensive domain coverage required.

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) examining calibration as outcome variable with Domain and Time as fixed effects

**High-Level Workflow:**

**Step 0:** Load accuracy theta by domain from Ch5 5.2.1 (results/ch5/5.2.1/data/step03_theta_accuracy_domain.csv)
**Step 1:** Load confidence theta by domain from RQ 6.3.1 (results/ch6/6.3.1/data/step03_theta_confidence_domain.csv)
**Step 2:** Merge accuracy and confidence datasets by UID × TEST × Domain
**Step 3:** Compute calibration per domain: Calibration = theta_confidence - theta_accuracy (both z-standardized first)
**Step 4:** Fit LMM: Calibration ~ Domain × Time + (Time | UID)
**Step 5:** Test Domain main effect and Domain × Time interaction using dual p-values (Decision D068)
**Step 6:** Post-hoc contrasts: What vs Where, What vs When, Where vs When
**Step 7:** Identify best-calibrated and worst-calibrated domains
**Step 8:** Prepare plot data showing calibration trajectories by domain

**Expected Outputs:**
- data/step01_calibration_by_domain.csv (1200 rows: UID, TEST, Domain, theta_accuracy, theta_confidence, calibration)
- results/step02_lmm_summary.txt (full model output with variance components)
- results/step03_domain_effects.csv (Domain main effect and interaction terms with dual p-values)
- results/step04_domain_ranking.csv (domains ranked by mean |calibration|)
- plots/step05_calibration_by_domain.csv (plot source data: Domain × TEST means + SE)

**Success Criteria:**
- Merge successful: 1200 observations (100 participants × 4 tests × 3 domains)
- No missing data after merge
- Calibration computed correctly (z-standardized theta_confidence - z-standardized theta_accuracy)
- LMM converges without warnings
- Domain effects tested with dual p-values (D068: parametric and bootstrap)
- Post-hoc contrasts complete for all 3 pairwise comparisons
- Domain ranking identifies best and worst calibrated domains
- Plot data structured for visualization

---

## Data Source

**Data Type:**
DERIVED (from two upstream RQ sources)

### DERIVED Data Sources:

**Source RQ 1:**
Ch5 5.2.1 (Domain-stratified accuracy trajectories)

**File Paths:**
- results/ch5/5.2.1/data/step03_theta_accuracy_domain.csv (1200 rows: UID, TEST, Domain, theta_accuracy)

**Source RQ 2:**
RQ 6.3.1 (Domain-stratified confidence trajectories)

**File Paths:**
- results/ch6/6.3.1/data/step03_theta_confidence_domain.csv (1200 rows: UID, TEST, Domain, theta_confidence)

**Dependencies:**
- Ch5 5.2.1 must complete Steps 1-3 (domain-stratified IRT calibration, theta estimation)
- RQ 6.3.1 must complete Steps 1-3 (domain-stratified IRT calibration for confidence)
- Both source RQs must use identical domain definitions and IRT methodology (GRM with p1_med prior)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from source RQs (inherited inclusion criteria)
- Note: Participant set determined by Ch5 5.2.1 and RQ 6.3.1 purification steps

**Items:**
- N/A (theta scores already aggregated per domain)
- Item-level purification handled by source RQs

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4 corresponding to Days 0, 1, 3, 6)
- Inherited from source RQs

**Domains:**
- [x] What domain (object identity)
- [x] Where domain (spatial location - all tags combined)
- [x] When domain (temporal order)
- Note: If When domain excluded in RQ 6.3.1 due to purification issues (< 10 items), analysis reduces to What vs Where only

---
