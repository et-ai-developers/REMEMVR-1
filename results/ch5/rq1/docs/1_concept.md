# RQ 5.1: Domain-Specific Forgetting Trajectories (What/Where/When)

**Chapter:** 5
**RQ Number:** 1
**Full ID:** 5.1

---

## Research Question

**Primary Question:**
Are there domain-specific differences in the rate and pattern of episodic forgetting over 6 days?

**Scope:**
This RQ examines forgetting rates for three episodic memory components (What, Where, When) using IRT-derived ability estimates across four test sessions (T1, T2, T3, T4). Time variable uses TSVR (actual hours since encoding), not nominal days (0, 1, 3, 6). Focuses on VR-based memory test items requiring binding of object identity, spatial location, and temporal order. All 100 participants included across all 4 tests.

**Theoretical Framing:**
This question matters for understanding episodic memory architecture. Dual-process theories predict differential forgetting patterns due to domain-specific reliance on familiarity vs. recollection processes. Identifying domain-specific trajectories informs theoretical models of episodic memory consolidation and retrieval dynamics.

---

## Theoretical Background

**Relevant Theories:**
- **Dual-Process Theory** (Yonelinas, 2002): Memory retrieval relies on familiarity (fast, automatic) and recollection (slow, effortful). What domain can rely on familiarity, while Where/When require recollection. Familiarity-based information is less hippocampus-dependent than contextual details.
- **Consolidation Theory** (Rasch & Born, 2013): Hippocampal-dependent memories (Where, When) consolidate more slowly and show greater vulnerability during consolidation compared to perirhinal-dependent memories (What).

**Key Citations:**
- Tulving (1972): Episodic memory as "mental time travel" requiring binding of What/Where/When
- Yonelinas (2002): Dual-process theory distinguishing familiarity and recollection processes
- Rasch & Born (2013): Sleep-dependent consolidation preferentially benefits hippocampal memories
- Kisker et al. (2021): Immersive VR promotes recollection-based memory (supports dual-process predictions in VR contexts)
- Stark et al. (2018): Hippocampal activation greater for temporal order vs. spatial location retrieval (neural evidence for domain dissociation)
- Deuker et al. (2016): Spatial and temporal episodic memory recruit dissociable functional networks

**Theoretical Predictions:**
Dual-process theory predicts What will show slowest forgetting (familiarity-based), Where intermediate, and When fastest (recollection-dependent). Object identity (What) may be more resilient than spatial (Where) or temporal (When) memory, consistent with dual-process theories suggesting familiarity-based information is less hippocampus-dependent than contextual details.

**Literature Gaps:**
Most episodic memory studies examine What and Where separately. Few studies test all three WWW domains together in immersive VR with longitudinal trajectories across 6 days. This RQ provides comprehensive assessment of domain-specific forgetting using psychometrically validated IRT ability estimates.

**Alternative Explanation:**
Domain differences could reflect initial encoding quality variations (e.g., spatial information encoded more richly; Bonnici et al., 2018) rather than differential decay rates. However, Day 0 baseline captures initial encoding state, and longitudinal trajectory slopes (not intercepts) test forgetting dynamics. If encoding quality alone drives differences, domains would differ at T1 but show parallel trajectories; if forgetting rates differ, Domain × Time interaction should emerge.

---

## Hypothesis

**Primary Hypothesis:**
Object identity (What) may be more resilient than spatial (Where) or temporal (When) memory, consistent with dual-process theories suggesting familiarity-based information is less hippocampus-dependent than contextual details.

**Secondary Hypotheses:**
1. Memory domains will show differential forgetting trajectories with What showing slowest forgetting, Where intermediate, and When fastest forgetting
2. Non-linear forgetting (logarithmic or quadratic better than linear) will better describe trajectories across domains

**Theoretical Rationale:**
Dual-process theory suggests What can rely on familiarity (perirhinal cortex), while Where and When require hippocampal binding. Familiarity-based retrieval is more resilient to forgetting than recollection-based retrieval. Consolidation theory predicts hippocampal-dependent memories are more vulnerable during early consolidation. Non-linear forgetting reflects consolidation and retrieval dynamics operating on different timescales.

**Expected Effect Pattern:**
Significant Domain × Time interaction in LMM analysis. Post-hoc contrasts should show: What ≠ When (p < 0.001), Where intermediate. Non-linear time terms (log, quadratic) should improve model fit (ΔAIC > 2) compared to linear-only model.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: **ALL Where tags included** (`*-L-*`, `*-U-*`, `*-D-*`). Complete spatial coverage needed for comprehensive assessment of spatial memory domain.

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ examines all three WWW episodic memory components to test differential forgetting trajectories. Complete coverage of What/Where/When binding is theoretically necessary per Tulving's episodic memory definition. All three domains required to test dual-process predictions about familiarity (What) vs. recollection (Where/When) differences.

**Exclusion Rationale:**
None - all WWW domains included for comprehensive episodic memory assessment.

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation + LMM (Linear Mixed Models) for trajectory modeling

**High-Level Workflow:**

**Step 1:** Data Preparation - Load data from data/cache/dfData.csv, keep columns ['UID', 'TEST', 'TSVR', 'TQ_*']

**Step 2:** Dichotomization - Convert TQ_* values: <1 becomes 0, >=1 becomes 1 (binary accuracy scoring)

**Step 3:** IRT Data Prep - Send to irt_data_prep tool with composite=["UID", "TEST"], time="TSVR", items=["TQ_*"], factors={what: ["*-N-*"], where: ["*-L-*", "*-U-*", "*-D-*"], when: ["*-O-*"]}

**Step 4:** IRT Pass 1 - Calibrate correlated factors, 2-category GRM. Extract theta scores, difficulty (b), discrimination (a). **IRT Assumption Validation:** (1) Check unidimensionality via eigenvalue ratio (first/second eigenvalue >3.0), (2) Compute Q3 statistic for all item pairs within each domain to detect local dependence (Q3 <0.2 threshold per Christensen et al. 2017). If >10% of item pairs show Q3 >0.2, consider bifactor IRT model. Report Q3 statistics in validation logs.

**Step 5:** Item Purification - Remove items with extreme difficulty (|b| > 3.0) or low discrimination (a < 0.4) to ensure psychometric quality. This also controls for room-level memorability variance by excluding outlier items. Apply within-domain filter to ensure balanced representation across What/Where/When.

**Step 6:** IRT Pass 2 - Re-calibrate GRM on purified items only

**Step 7:** LMM Trajectory Modeling - Fit 5 candidate models with Domain × Time interactions: Linear, Quadratic, Logarithmic, Lin+Log, Quad+Log. Use Treatment coding (What as reference), random intercepts and slopes by UID. Fit with REML=False for AIC/AICc comparison. **Convergence Strategy:** If random slopes fail to converge (singular fit warnings), compare random intercept-only model via likelihood ratio test. Only retain random slopes if: (1) they significantly improve fit (LRT p<0.05) AND (2) model converges without warnings. Report convergence status. Select best model via AIC and AICc (small-sample corrected); if they disagree, favor AICc (N=100).

**Step 8:** Theta to Probability Conversion - Translate best model predictions back to probability scale using reverse logit: `probability = 1 / (1 + np.exp(-(discrimination * (theta - difficulty))))`

**Step 9:** Post-hoc Contrasts - Extract Time×Domain interaction terms from best model. Test differences in forgetting slopes: Where-What, When-What. Report with and without Bonferroni correction (α = 0.0033/3 = 0.0011 for 3 pairwise tests). Perform for both ability (theta) and probability scales.

**Step 10:** Effect Size Computation - Calculate Cohen's d for domain differences at each nominal time point (Days 0, 1, 3, 6). Report: d_What_Where, d_What_When, d_Where_When. Compute with and without Bonferroni, for both ability and probability scales.

**Step 11:** Visualization - Generate trajectory plot: 3 lines (What/Where/When) over time. Include observed means with 95% CIs and model-predicted lines.

**Data Preprocessing (Per Solution Section 1.4):**
- **Accuracy Scores (-ANS tags):** Dichotomize before IRT: >=1 = 1, <1 = 0 (no partial credit)
- **Confidence Ratings:** Not applicable to this RQ (accuracy only)
- **IRT Model:** GRM (Graded Response Model) - handles dichotomous items (2 categories)
- **Time Variable:** TSVR (Time Since VR, actual hours since encoding) NOT nominal days

**Special Methods:**
- **2-Pass IRT Purification** (Decision D039): Mandatory for all IRT analyses to remove psychometrically problematic items (|b| > 3.0 or a < 0.4)
- **TSVR Time Variable** (Decision D070): Use actual hours since encoding, not nominal days (0, 1, 3, 6) for LMM fitting
- **Dual-Scale Reporting** (Decision D068): Report results on both theta (ability) and probability scales for interpretability
- **Dual-Scale Trajectory Plots** (Decision D069): Plot theta + probability scales for interpretability
- **Correlated Factors IRT:** What, Where, When domains modeled as correlated factors (not independent) to account for episodic binding
- **GRM Model Clarification:** GRM (Graded Response Model) handles dichotomous (2 categories: 0, 1) items. For dichotomized accuracy, GRM reduces to 2PL dichotomous IRT mathematically.

---

## Data Source

**Data Type:**
RAW (extracted from master.xlsx via data/cache/dfData.csv)

### RAW Data Extraction:

**Tag Patterns:**
- Domain tags: `-N-` (What), `-L-/-U-/-D-` (Where), `-O-` (When)
- Item pattern: `TQ_*` (all VR task items in master.xlsx)
- Complete patterns:
  - What: `*-N-*` (matches TQ_RVR-*-N-*-*)
  - Where: `*-L-*`, `*-U-*`, `*-D-*` (matches TQ_RVR-*-L/U/D-*-*)
  - When: `*-O-*` (matches TQ_RVR-*-O-*-*)

**Extraction Method:**
Load data from data/cache/dfData.csv (preprocessed from master.xlsx). Select columns: ['UID', 'TEST', 'TSVR', 'TQ_*']. Dichotomize TQ_* values (<1 → 0, >=1 → 1). Send to irt_data_prep tool with composite=["UID", "TEST"], time="TSVR", items=["TQ_*"], factors={what, where, when}. Tool yields long-format CSV with columns: composite_ID, item_code, response (0-1).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)

**Items:**
- [x] All VR items matching TQ_* pattern
- Note: Item purification in Step 5 removes psychometrically problematic items (|b| > 3.0 or a < 0.4) AFTER initial calibration

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4 - nominal Days 0, 1, 3, 6)
- Note: Time variable uses TSVR (actual hours since encoding), not nominal days

---

## Validation Procedures & Limitations

**LMM Assumption Diagnostics:**

After selecting best model via AIC/AICc, validate core assumptions:
1. **Residual Normality:** Q-Q plot + Shapiro-Wilk test (p>0.05 threshold). If violated, use robust standard errors (Huber-White).
2. **Homoscedasticity:** Residual vs fitted plot (visual inspection for constant variance).
3. **Outliers:** Cook's distance (D > 4/100 = 0.04 flags influential observations). Report with/without outliers if detected.
4. **Autocorrelation:** ACF plot (lag-1 ACF < 0.1 for independence). If violated, consider GEE with AR(1) structure.

Report all diagnostic results in validation logs. Remedial actions specified above guide handling of assumption violations (Schielzeth et al. 2020).

**Practice Effects Limitation:**

Repeated testing across T1-T4 introduces practice effects (performance improvements due to task familiarity) that may partially offset forgetting (Calamia et al. 2013, d = 0.25 typical effect size; Jutten et al. 2020). We assume practice effects are domain-general (affect What/Where/When equally), preserving validity of Domain×Time interaction for testing differential forgetting. However, main effect of time confounds practice and forgetting, so absolute forgetting rates should be interpreted cautiously. IRT theta estimates partially account for task familiarity by separating item difficulty from person ability. Non-linear trajectory models can capture initial practice-driven improvements vs. later decay-driven decline.

**Methodological Notes:**

- **Sample Size:** N=100 adequate for fixed effects but marginal for random slopes (Ryoo 2011 recommends N≥200). Convergence strategy (Step 7) addresses this limitation.
- **Local Dependence:** Episodic memory items may violate IRT local independence due to serial position effects and contextual binding (Bock et al. 2021). Q3 validation (Step 4) detects violations.

---
