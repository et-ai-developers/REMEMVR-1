# RQ 5.2.1: Domain-Specific Forgetting Trajectories (What/Where/When)

**Chapter:** 5
**RQ Number:** 2.1
**Full ID:** 5.2.1

---

## Research Question

**Primary Question:**
Are there domain-specific differences in the rate and pattern of episodic forgetting over 6 days?

**Scope:**
This RQ examines forgetting trajectories for three episodic memory components (What, Where, When) using IRT-derived theta ability estimates across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6). Time variable uses TSVR (Time Since VR, actual hours since encoding), not nominal days. Analysis focuses on VR-based memory test items requiring binding of object identity, spatial location, and temporal order.

**Theoretical Framing:**
Episodic memory consists of integrated What/Where/When components (Tulving's "mental time travel"). Understanding domain-specific forgetting patterns reveals whether these components decay independently or show coordinated trajectories, informing theories of episodic memory consolidation and retrieval.

---

## Theoretical Background

**Relevant Theories:**
- **Dual-Process Theory**: Suggests familiarity-based information (What - object identity) is less hippocampus-dependent than contextual details (Where - spatial, When - temporal). Predicts differential forgetting rates across domains based on retrieval process differences.
- **Episodic Memory Theory (Tulving)**: Episodic memory requires binding of What/Where/When components. Domain-specific forgetting patterns test whether binding integrity is maintained or degrades differentially over time.

**Key Citations:**
- Tulving (1972): Episodic memory as "mental time travel" requiring What/Where/When binding
- Dual-process theories suggesting familiarity vs. recollection differences in hippocampal dependence

**Theoretical Predictions:**
Dual-process theory predicts object identity (What) may be more resilient than spatial (Where) or temporal (When) memory, as familiarity-based information is less hippocampus-dependent than contextual details requiring recollection.

**Literature Gaps:**
Most episodic memory studies examine domains separately. This RQ tests all three What/Where/When components together in immersive VR with longitudinal trajectories across 6 days, providing integrated assessment of domain-specific forgetting.

---

## Hypothesis

**Primary Hypothesis:**
Object identity (What) may be more resilient than spatial (Where) or temporal (When) memory, consistent with dual-process theories suggesting familiarity-based information is less hippocampus-dependent than contextual details.

**Secondary Hypotheses:**
Not explicitly stated in thesis. Analysis will test whether domain differences emerge through Domain × Time interaction in LMM analysis.

**Theoretical Rationale:**
Dual-process theory suggests What can rely on familiarity (less hippocampus-dependent), while Where and When require hippocampal binding and recollection processes. This predicts What will show slower forgetting (shallower slope) compared to Where/When.

**Expected Effect Pattern:**
Significant Domain × Time interaction in LMM analysis. Post-hoc contrasts should show differential forgetting slopes across domains (Where-What, When-What comparisons with Bonferroni correction α = 0.0033/3 = 0.0011).

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
  - Disambiguation: **ALL Where tags included** (*-L-*, *-U-*, *-D-*) to capture complete spatial memory coverage

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
All three What/Where/When episodic memory components examined to test differential forgetting trajectories. Complete coverage of episodic memory binding per Tulving's definition.

**Exclusion Rationale:**
None - all WWW domains included for comprehensive episodic memory assessment.

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation + LMM (Linear Mixed Models) for trajectory modeling

**High-Level Workflow:**

**Step 1:** Load data from data/cache/dfData.csv, keep columns ['UID', 'TEST', 'TSVR', 'TQ_*']

**Step 2:** Dichotomize TQ_* values (less than 1 becomes 0, greater than or equal to 1 becomes 1)

**Step 3:** Prepare data for IRT analysis with composite = ["UID", "TEST"], time = "TSVR", items = ["TQ_*"], factors: what = ["*-N-*"], where = ["*-L-*", "*-U-*", "*-D-*"], when = ["*-O-*"]. Save to data/ folder.

**Step 4:** Run IRT Analysis using correlated factors, 2-category GRM. Extract theta scores, difficulty (b), and discrimination (a) parameters.

**Step 5:** Purify IRT items - remove items with difficulty < -3 or > 3, and discrimination < 0.4 (within-domain filter)

**Step 6:** Re-run IRT on purified items (2-pass IRT purification)

**Step 7:** Fit 5 candidate LMMs with Domain × Time interactions using TSVR as time variable:
  - Linear: Time × Domain
  - Quadratic: (Time + Time²) × Domain
  - Logarithmic: log(Time+1) × Domain
  - Lin+Log: (Time + log(Time+1)) × Domain
  - Quad+Log: (Time + Time² + log(Time+1)) × Domain
  - All models use Treatment coding (What as reference), random intercepts and slopes
  - Fit with REML=False for AIC comparison
  - Select best model via AIC, compute Akaike weights

**Step 8:** Translate best model theta predictions back into probability using reverse logit: probability = 1 / (1 + exp(-(discrimination * (theta - difficulty))))

**Step 9:** Post-hoc contrasts - Extract Time×Domain interaction terms from best model, test differences in forgetting slopes: Where-What, When-What. Bonferroni correction: α = 0.0033/3 = 0.0011 for 3 pairwise tests. Report both corrected and uncorrected results.

**Step 10:** Effect size computation - Calculate Cohen's d for domain differences at each time point (Days 0, 1, 3, 6) after model fitted. Report: d_What_Where, d_What_When, d_Where_When. Both with and without Bonferroni correction, for both ability (theta) and probability scales.

**Step 11:** Visualization - Generate trajectory plot with 3 lines (What/Where/When) over time. Include observed means with 95% CIs and model-predicted lines.

**Data Preprocessing:**
- **Accuracy Scores:** Dichotomize TQ_* values before IRT (less than 1 → 0, greater than or equal to 1 → 1)
- **IRT Model:** 2-category GRM (Graded Response Model) with correlated factors
- **Time Variable:** TSVR (Time Since VR, actual hours since encoding), not nominal days

**Special Methods:**
- **2-Pass IRT Purification:** First IRT calibration identifies problematic items (|b| > 3 or a < 0.4), second IRT re-calibrates on purified item set
- **TSVR Time Variable:** Use actual hours since encoding, not nominal days (0, 1, 3, 6)
- **Dual-Scale Reporting:** Report results in both theta (ability) and probability scales for interpretability
- **Model Selection:** AIC comparison across 5 functional forms (Linear, Quadratic, Logarithmic, Lin+Log, Quad+Log) to determine best-fitting trajectory shape

**Expected Tools:**
- IRT calibration tools (correlated factors GRM)
- Item purification tools (difficulty/discrimination filters)
- LMM trajectory modeling tools (Domain × Time interactions, random slopes)
- Reverse logit transformation (theta → probability)
- Post-hoc contrast tools (pairwise domain comparisons)
- Effect size computation tools (Cohen's d)
- Trajectory plotting tools (observed + predicted lines, 95% CIs)

---

## Data Source

**Data Type:**
RAW (extracted from data/cache/dfData.csv, which is derived from master.xlsx)

### RAW Data Extraction:

**Tag Patterns:**
- Domain tags: `-N-` (What), `-L-/-U-/-D-` (Where), `-O-` (When)
- Item pattern: `TQ_*` (all VR test questions)
- Complete patterns:
  - What: `*-N-*` in TQ_* columns
  - Where: `*-L-*`, `*-U-*`, `*-D-*` in TQ_* columns
  - When: `*-O-*` in TQ_* columns

**Extraction Method:**
Load data/cache/dfData.csv, keep columns ['UID', 'TEST', 'TSVR', 'TQ_*']. Dichotomize TQ_* values. Prepare for IRT analysis with factor assignments: what = ["*-N-*"], where = ["*-L-*", "*-U-*", "*-D-*"], when = ["*-O-*"].

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions mentioned in thesis)

**Items:**
- [x] All VR items matching TQ_* pattern
- [x] All paradigms included (thesis uses TQ_* pattern, which includes all VR paradigms)
- Note: Item purification step (Step 5) will filter out psychometrically problematic items (|b| > 3 or a < 0.4) after initial IRT calibration

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Note: Time variable uses TSVR (actual hours since encoding), not nominal days

---
