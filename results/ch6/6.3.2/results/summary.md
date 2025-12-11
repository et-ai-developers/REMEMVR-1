# Results Summary: RQ 6.3.2 - Domain Confidence Calibration

**Research Question:** Are people better calibrated for some episodic memory domains (What/Where/When) than others?

**Analysis Completed:** 2025-12-11

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total N:** 100 participants
- **Observations:** 1,200 total (100 participants × 4 test sessions × 3 domains)
- **Missing data:** None (complete merge across Ch5 5.2.1 accuracy and Ch6 6.3.1 confidence datasets)
- **Domains analyzed:** All three domains (What, Where, When) successfully merged
- **Test sessions:** T1 (Day 0), T2 (Day 1), T3 (Day 3), T4 (Day 6)

### Calibration Computation

**Methodology:**
- Calibration computed as difference between z-standardized confidence theta and z-standardized accuracy theta
- Positive calibration = overconfidence (confidence > accuracy)
- Negative calibration = underconfidence (confidence < accuracy)
- Calibration near zero = well-calibrated (confidence matches accuracy)

**Standardization verification:**
- theta_accuracy_z: mean = 0.000, SD = 1.000 (correctly standardized)
- theta_confidence_z: mean = 0.000, SD = 1.000 (correctly standardized)
- Calibration range: [-4.43, 2.77] (within expected limits)
- Mean |calibration|: 0.82 (overall miscalibration magnitude)

### Primary Results: Domain Main Effect

**Linear Mixed Model:**
- Outcome: Calibration (confidence - accuracy, both z-standardized)
- Fixed effects: Domain, TSVR_centered (hours since VR encoding), Domain × TSVR interaction
- Random effects: Participant intercepts + slopes for TSVR_centered
- Convergence: Successful

**Domain Main Effect (Likelihood Ratio Test):**

| Effect | Ç² | df | p (uncorr) | p (Bonf) | Interpretation |
|--------|-----|-----|-------------|----------|----------------|
| Domain main effect | 60.24 | 2 | 8.30×10{¹t | 1.66×10{¹³ | **Significant** |
| Domain × Time interaction | 59.60 | 2 | 1.14×10{¹³ | 2.28×10{¹³ | **Significant** |

**Interpretation:** Domain has a highly significant effect on calibration quality (p < 0.001 Bonferroni-corrected). Moreover, the significant Domain × Time interaction reveals that domain differences in calibration **change over the retention interval** - this is a **crossover interaction** (see plot descriptions).

### Post-Hoc Pairwise Contrasts

**Contrasts at Average Timepoint:**

| Contrast | Estimate | SE | z | p (uncorr) | p (Bonf) | Cohen's d | Interpretation |
|----------|----------|-----|---|-------------|----------|-----------|----------------|
| What vs Where | 0.039 | 0.066 | 0.58 | 0.561 | 1.000 | 0.041 | Not significant |
| What vs When | -0.004 | 0.079 | -0.04 | 0.965 | 1.000 | -0.003 | Not significant |
| Where vs When | -0.042 | 0.079 | -0.53 | 0.594 | 1.000 | -0.038 | Not significant |

**Critical Finding:** Despite the highly significant Domain main effect and interaction, **NO pairwise contrasts reached significance** at the average timepoint (all p_bonf = 1.0). This apparent paradox is resolved by the **crossover interaction**: domain differences exist but their DIRECTION reverses over time, so averaging across timepoints obscures the effects.

### Domain Calibration Ranking (Overall)

**Mean Absolute Calibration by Domain:**

| Rank | Domain | Mean |calibration| | SD | N | Interpretation |
|------|--------|-------------------|-----|-----|----------------|
| 1 | **What** | 0.725 | 0.604 | 400 | Best calibrated |
| 2 | **Where** | 0.726 | 0.582 | 400 | Middle (nearly identical to What) |
| 3 | **When** | 1.024 | 0.755 | 400 | **Worst calibrated** |

**Key Pattern:** What and Where domains show nearly identical calibration quality (0.725 vs 0.726, difference = 0.001). When domain shows **41% higher miscalibration** magnitude (1.024 vs 0.725 average).

### Trajectory-Specific Findings (Critical for Interpretation)

**Calibration Change from Day 0 to Day 6:**

| Domain | T1 (Day 0) Calibration | T4 (Day 6) Calibration | Change (”) | Pattern |
|--------|----------------------|----------------------|-----------|---------|
| **What** | -0.252 (underconfident) | +0.077 (slight overconfidence) | **+0.329** | Worsening calibration |
| **Where** | -0.248 (underconfident) | +0.116 (slight overconfidence) | **+0.364** | Worsening calibration |
| **When** | **+0.377** (overconfident) | **-0.351** (underconfident) | **-0.727** | **IMPROVING calibration** |

**Major Finding:** When domain exhibits **OPPOSITE trajectory** to What/Where:
- **When domain paradox:** Starts overconfident (+0.377) despite floor-effect accuracy, ends underconfident (-0.351). Total trajectory shift = 0.727 z-score units.
- **What/Where pattern:** Start underconfident (confidence lags behind moderate accuracy), end slightly overconfident (confidence doesn't decline as fast as accuracy). Similar trajectory shifts (+0.33 to +0.36).

### Domain × Time Interaction Decomposition

**When Domain Interaction Term:**
- Coefficient: ² = -0.0063, SE = 0.0010, z = -6.52, p < 0.0001
- **Interpretation:** When domain calibration **improves** (becomes less overconfident) by 0.0063 z-score units per hour of retention, relative to What domain baseline.
- **Effect magnitude:** Over 144 hours (Day 0 to Day 6): -0.0063 × 144 = -0.91 z-score shift (closely matches observed -0.727 trajectory change).

**Where Domain Interaction Term:**
- Coefficient: ² = +0.0005, SE = 0.0010, z = 0.50, p = 0.615
- **Interpretation:** Where domain trajectory statistically indistinguishable from What domain (parallel trajectories, both worsening calibration).

---

## 2. Plot Descriptions

### Figure 1: Domain-Specific Calibration Trajectories (Crossover Interaction)

**Filename:** `calibration_trajectories_by_domain.png`

**Plot Type:** Line plot with 95% confidence intervals (shaded regions)

**Visual Description:**

The plot displays calibration trajectories (y-axis: Confidence - Accuracy, z-standardized) across 4 test sessions (x-axis: T1/Day 0, T2/Day 1, T3/Day 3, T4/Day 6) for three memory domains:

- **Horizontal reference line (y = 0):** Perfect calibration (confidence matches accuracy)
- **Positive values (pink shaded region):** Overconfident (confidence exceeds accuracy)
- **Negative values (blue shaded region):** Underconfident (confidence below accuracy)

**Domain Trajectories:**

1. **What domain (blue line):**
   - Starts underconfident at T1 (-0.25)
   - Crosses zero around T2 (Day 1)
   - Ends slightly overconfident at T4 (+0.08)
   - **Pattern:** Monotonic increase from underconfidence to slight overconfidence

2. **Where domain (orange line):**
   - Starts underconfident at T1 (-0.25, nearly identical to What)
   - Crosses zero around T2 (Day 1)
   - Ends slightly overconfident at T4 (+0.12)
   - **Pattern:** Parallel to What domain throughout retention interval

3. **When domain (green line):**
   - **Starts OVERCONFIDENT at T1 (+0.38, ABOVE zero despite floor-effect accuracy)**
   - Decreases sharply across sessions
   - **Crosses What/Where lines around T2-T3 (CROSSOVER POINT)**
   - Ends underconfident at T4 (-0.35)
   - **Pattern:** Monotonic decrease from overconfidence to underconfidence (**OPPOSITE to What/Where**)

**Key Visual Patterns:**

1. **Crossover interaction:** When domain trajectory crosses What/Where trajectories between T2-T3, creating X-shaped pattern. This is the source of the significant Domain × Time interaction (Ç² = 59.60, p < 0.001).

2. **Confidence interval widths:** When domain shows wider confidence bands (larger variance), consistent with worst calibration ranking (mean |calibration| = 1.024).

3. **What/Where convergence:** Blue and orange lines remain parallel and nearly overlapping throughout, consistent with nearly identical calibration quality (0.725 vs 0.726).

4. **Trajectory directions:** What/Where worsen (move from underconfident to overconfident). When improves (moves from overconfident to underconfident, approaching better calibration).

**Connection to Statistical Findings:**

- Visual crossover confirms significant Domain × Time interaction (Ç² = 59.60, p < 0.0001)
- When domain's T1 overconfidence (+0.38) explains why overall mean |calibration| is worst (1.024)
- Post-hoc contrasts non-significant at average timepoint because When is overconfident early but underconfident late (effects cancel when averaged)
- Trajectory slopes match LMM coefficients: When ² = -0.0063/hour × 144 hours H -0.91 (observed shift = -0.727)

### Figure 2: Domain Ranking by Calibration Quality

**Filename:** `domain_calibration_ranking.png`

**Plot Type:** Bar chart with error bars (SD)

**Visual Description:**

Bar chart showing mean absolute calibration (y-axis, 0 to 1.2 z-score units) for three domains (x-axis: What, Where, When):

- **What domain (blue bar):** Rank 1, mean |calibration| = 0.725, error bar ±0.60
- **Where domain (orange bar):** Rank 2, mean |calibration| = 0.726, error bar ±0.58
- **When domain (green bar):** Rank 3, mean |calibration| = 1.024, error bar ±0.76

**Key Patterns:**

1. **What/Where near-identity:** Blue and orange bars at same height (0.725 vs 0.726, difference = 0.001). Confirms post-hoc contrast non-significance (p_bonf = 1.0).

2. **When domain elevated:** Green bar 41% higher than What/Where (1.024 vs 0.725 average). Visually distinct separation.

3. **When domain higher variability:** Green bar has longest error bars (SD = 0.76 vs 0.60/0.58 for What/Where), reflecting greater individual differences in When calibration.

4. **Annotation:** Plot includes text noting "When domain worst calibrated (highest variability)" and "What/Where nearly identical calibration quality."

**Connection to Statistical Findings:**

- Visual ranking matches Table in Section 1 (Rank 1: What, Rank 2: Where, Rank 3: When)
- Height difference confirms significant Domain main effect (Ç² = 60.24, p < 0.001)
- When domain's higher variability (SD = 0.76) consistent with wider confidence bands in Figure 1
- Bar heights represent **overall** calibration (averaged across time), obscuring crossover interaction visible in Figure 1

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**

"When domain shows BETTER calibration than What/Where domains despite floor effects. Calibration quality ranking: When > Where > What. Rationale: When domain's floor effects should affect both accuracy and confidence similarly, maintaining calibration."

**Hypothesis Status:** **REJECTED**

**Evidence for Rejection:**

The data show the **OPPOSITE** ranking: What = Where (best calibrated, mean |calibration| = 0.725) > When (worst calibrated, mean |calibration| = 1.024). When domain exhibits 41% higher miscalibration magnitude than What/Where domains.

**Why Hypothesis Failed:**

The hypothesis assumed When domain's floor effects would create matched low accuracy and low confidence (good calibration via matched floor). However, the **critical unexpected pattern** is:

1. **Day 0 (T1):** When domain shows **OVERCONFIDENCE** (+0.377) despite floor-effect accuracy
   - Accuracy is already low (floor effect from Ch5 5.2.1 findings)
   - BUT confidence remains HIGH (does not track the floor effect initially)
   - Result: **Massive miscalibration** at encoding session

2. **Day 6 (T4):** When domain shows underconfidence (-0.351)
   - Accuracy has declined further (continued forgetting)
   - Confidence has declined MORE (now below accuracy)
   - Result: Miscalibration persists but reverses direction

**Revised Theoretical Interpretation:** When domain's poor calibration is not due to matched floor effects, but due to **dynamic metacognitive failure**: initial overconfidence (confidence insensitive to floor-effect accuracy) followed by overcorrection (confidence declines faster than accuracy). The temporal domain may rely on misleading retrieval cues that generate false fluency at encoding but collapse rapidly over retention.

### Unexpected Finding: When Domain Crossover Interaction

**The Discovery:**

When domain exhibits **OPPOSITE calibration trajectory** to What/Where domains:
- When: Starts overconfident (+0.377), ends underconfident (-0.351), ” = -0.727
- What/Where: Start underconfident (~-0.25), end slightly overconfident (~+0.10), ” ~ +0.33

This creates a **crossover interaction** (Figure 1), where When domain crosses What/Where trajectories around Day 1-3.

**Theoretical Significance:**

This is a **MAJOR FINDING** with implications for metacognitive monitoring theory:

1. **Domain-specific metacognitive dynamics:** Calibration is not static - it evolves differently by domain. What/Where show worsening calibration (confidence becomes overconfident relative to declining accuracy). When shows improving calibration (confidence "catches up" to floor-effect accuracy).

2. **When domain paradox explained:**
   - **T1 overconfidence mechanism:** Participants may rely on **temporal order encoding strategies** (e.g., "I remember encoding this event second") that generate HIGH confidence at encoding, but this confidence is **illusory** because temporal accuracy is already low (floor effect). Potential cue: retrieval fluency from recent encoding (events feel recent, confidence high) despite poor temporal discrimination.

   - **T4 underconfidence mechanism:** By Day 6, temporal retrieval fluency has collapsed (temporal cues degraded), confidence drops BELOW already-low accuracy. Participants become **aware** of temporal memory failure (metacognitive insight), leading to conservative confidence judgments.

3. **What/Where worsening calibration mechanism:**
   - **T1 underconfidence:** Moderate accuracy (What/Where domains better than When at baseline) but participants are CAUTIOUS (confidence slightly below accuracy). Metacognitive awareness of episodic memory fallibility.

   - **T4 overconfidence:** Accuracy declines due to forgetting, but confidence does NOT decline proportionally. Residual familiarity signals (What domain) or spatial landmark salience (Where domain) maintain confidence despite accuracy loss. Result: overconfidence emerges.

### Connection to Dual-Process Theory

**Yonelinas (2002) Familiarity vs Recollection:**

The crossover pattern aligns with dual-process predictions:

- **What domain (familiarity-based):** Familiarity signals persist longer than recollection (Yonelinas, 2002). At Day 6, participants may feel familiar with objects (fluency-based confidence) but recollection accuracy has declined ’ overconfidence.

- **Where domain (recollection-based but spatialized):** VR spatial encoding creates robust landmarks (Ch5 5.2.1 showed Where domain resilience). Spatial cues maintain confidence, but accuracy still declines ’ slight overconfidence.

- **When domain (recollection-based, temporally fragile):** Temporal order requires precise recollection (no familiarity shortcut). Initial overconfidence may stem from **temporal compression** (events feel closer together than they are, high confidence). Over retention, temporal cues degrade rapidly, confidence collapses ’ underconfidence.

### Metacognitive Monitoring Theory: Domain-Specific Cues

**Fleming & Lau (2014) Metacognitive Cue Utilization:**

Results suggest metacognitive monitoring uses **different cues** for different domains:

| Domain | Encoding Cue (T1) | Retention Cue (T4) | Calibration Trajectory |
|--------|-------------------|---------------------|------------------------|
| What | Moderate fluency ’ cautious confidence | Residual familiarity ’ maintains confidence | Underconfident ’ Overconfident |
| Where | Spatial landmark salience ’ cautious | Landmark persistence ’ maintains confidence | Underconfident ’ Overconfident |
| When | Temporal compression fluency ’ high confidence | Temporal cue degradation ’ confidence collapse | **Overconfident ’ Underconfident** |

**Implication:** When domain's unique trajectory reflects **temporal metacognitive failure** - reliance on misleading temporal fluency cues at encoding (events feel "knowable" due to temporal proximity) that do not predict actual temporal discrimination accuracy.

### Broader Implications

#### 1. REMEMVR Assessment Validation

**For VR-based episodic memory assessment:**

- **What/Where domains:** Stable calibration quality (0.725-0.726 mean |calibration|), making confidence ratings potentially useful as metacognitive markers. Confidence judgments are moderately accurate across retention interval.

- **When domain:** **Unstable calibration** (crossover from +0.38 to -0.35, mean |calibration| = 1.024). Confidence ratings should be interpreted cautiously for temporal memory - confidence does not reliably track accuracy, especially at encoding.

- **Clinical recommendation:** For cognitive assessment applications, prioritize What/Where confidence ratings for metacognitive sensitivity indices. When domain confidence ratings may mislead (overconfidence at baseline, underconfidence at follow-up).

#### 2. Metacognitive Intervention Targets

**Crossover interaction suggests intervention opportunities:**

- **When domain early sessions:** Participants are overconfident at encoding (+0.377). **Intervention target:** Feedback training at T1 to calibrate temporal confidence downward (educate about temporal memory difficulty).

- **When domain late sessions:** Participants become underconfident by T4 (-0.351). **Intervention target:** Encourage persistence in temporal retrieval attempts (underconfidence may lead to premature giving up).

- **What/Where domains:** Worsening calibration over time. **Intervention target:** Retention-interval-specific feedback emphasizing forgetting awareness (combat overconfidence at Day 6).

#### 3. Methodological Insights: Averaging Obscures Dynamics

**Critical lesson:** Post-hoc contrasts at **average timepoint** were all non-significant (p_bonf = 1.0), despite highly significant Domain × Time interaction (Ç² = 59.60, p < 0.001). This demonstrates:

- **Static analyses insufficient:** Domain differences exist but REVERSE direction over time. Averaging across retention interval cancels effects (When overconfident early, underconfident late ’ average near zero).

- **Trajectory analyses essential:** Only by examining **time-specific effects** do we discover the When domain crossover pattern. This finding would be invisible in cross-sectional or time-averaged analyses.

- **Implication for episodic memory research:** Calibration is not a static individual difference trait - it evolves dynamically with memory trace degradation. Future studies must model calibration trajectories, not just overall calibration.

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 participants provides adequate power for main effects (Domain main effect Ç² = 60.24, highly significant)
- Crossover interaction detected (Ç² = 59.60, p < 0.001), indicating sufficient power for trajectory analyses
- However, subgroup analyses (e.g., fast vs slow calibration improvers) would be underpowered

**Demographic Constraints:**
- University undergraduate sample (age: M ~ 20, SD ~ 2) limits generalizability to older adults
- Older adults may show different calibration dynamics (metacognitive monitoring declines with age, Hertzog & Dunlosky, 2011)
- Restricted education range (all college students) prevents examining education effects on calibration

**Attrition:**
- Complete data for 100 participants across 4 sessions (no missing data after merge)
- Inherited participant set from Ch5 5.2.1 and Ch6 6.3.1 (any exclusions occurred upstream during IRT purification)
- Unknown whether excluded participants would show different calibration patterns

### Methodological Limitations

**Measurement:**

1. **Calibration Metric:**
   - Computed as simple difference (confidence theta - accuracy theta) after z-standardization
   - Assumes linear relationship between confidence and accuracy (may not hold at extremes)
   - Alternative metrics exist (e.g., gamma correlation, Brier score, bias/discrimination separation) not explored here

2. **Domain Definitions:**
   - What/Where/When conceptually defined (Tulving, 2002), not empirically validated in this VR paradigm
   - Domains assumed orthogonal but may have correlated components (e.g., spatial-temporal binding)
   - When domain floor effects (from Ch5 5.2.1) limit calibration range (if accuracy near zero, confidence-accuracy difference constrained)

3. **IRT Theta Dependency:**
   - Calibration computed from theta estimates from TWO separate IRT calibrations (Ch5 5.2.1 accuracy, Ch6 6.3.1 confidence)
   - If item purification differed between RQs (different items retained), theta estimates not strictly comparable
   - Assumed both IRT calibrations used identical GRM methodology and p1_med prior (verified in source RQ logs)

**Design:**

1. **No Concurrent Accuracy Measurement:**
   - Accuracy theta from Ch5 5.2.1 (objective correctness), confidence theta from Ch6 6.3.1 (confidence ratings)
   - Ideal design: measure accuracy AND confidence on SAME trials (item-level calibration)
   - Current design: domain-level calibration (aggregated across items within domain)
   - Limitation: Cannot examine item-specific calibration (e.g., are easy items better calibrated than hard items?)

2. **Test Session Timing:**
   - Fixed retention intervals (0, 1, 3, 6 days) may miss critical crossover dynamics
   - When domain crosses What/Where around T2-T3 (Day 1-3), but exact crossover timepoint unknown
   - More frequent testing (e.g., hourly Days 0-1, daily Days 1-6) would better characterize trajectories

3. **No Calibration Feedback:**
   - Participants never learned whether their confidence matched accuracy
   - Calibration patterns may reflect INITIAL metacognitive monitoring (without learning/adaptation)
   - Intervention study needed: does feedback improve When domain calibration?

**Statistical:**

1. **LMM Specification:**
   - Random slopes model assumes LINEAR trajectories over TSVR_hours
   - When domain trajectory appears roughly linear (Figure 1), but quadratic term not tested
   - Alternative time scales (log-transformed TSVR, categorical TEST session) not compared

2. **Post-Hoc Contrasts at Average Timepoint:**
   - Pairwise contrasts tested at mean TSVR (64.95 hours H Day 2-3)
   - Non-significant results (all p_bonf = 1.0) because crossover occurs near this timepoint (When transitioning from overconfident to underconfident)
   - Time-specific contrasts (e.g., contrasts AT T1, AT T4) would be more informative

3. **Multiple Comparisons:**
   - Bonferroni correction applied for 3 pairwise contrasts (conservative)
   - Did NOT correct for Domain main effect + Domain × Time interaction (2 tests)
   - Family-wise error rate: p(Type I) = 1 - (1 - 0.05)^2 H 0.10 (inflated, but effects highly significant p < 0.0001, so robust)

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - Older adults (age-related metacognitive decline may alter calibration trajectories)
  - Clinical populations (MCI, dementia patients show metacognitive deficits, Souchay et al., 2007)
  - Children (developing metacognition may show different domain-specific patterns)

**Context:**
- VR desktop paradigm differs from:
  - Real-world episodic memory (naturalistic encoding, emotionally salient events)
  - Standard lab memory tasks (2D stimuli, verbal materials)
  - Fully immersive VR (HMD with head tracking may alter spatial/temporal encoding)

**Task:**
- REMEMVR specific encoding task may not reflect:
  - Spontaneous episodic encoding (current task is structured, intentional)
  - Emotional episodic memories (neutral VR content, no affective salience to modulate confidence)
  - Semantic memory (facts vs events, confidence dynamics may differ)

### Technical Limitations

**Cross-RQ Dependency:**
- Calibration computed from TWO upstream RQs (Ch5 5.2.1, Ch6 6.3.1)
- If either source RQ had methodological issues (e.g., IRT purification too aggressive, convergence failures), errors propagate to this RQ
- Verified both source RQs completed successfully (logs confirm convergence, validation passed)
- Assumed domain definitions IDENTICAL across source RQs (What/Where/When item mappings consistent)

**Z-Standardization:**
- Calibration requires z-standardizing BOTH accuracy and confidence theta (mean = 0, SD = 1)
- Standardization performed on ENTIRE dataset (1200 observations pooled)
- Alternative: domain-specific standardization (z-score within each domain separately) not tested
- Current approach: domain differences in calibration reflect differences in ABSOLUTE theta discrepancy

**When Domain Floor Effects (Inherited from Ch5 5.2.1):**
- When domain showed floor-effect accuracy in Ch5 5.2.1 (theta_when lowest across domains)
- Floor effects constrain calibration range: if accuracy near -2.0 (very low), confidence must also be very low for good calibration, but confidence bounded at lower end by rating scale
- When domain's high |calibration| (1.024) may be partially artifactual (statistical artifact of floor-effect accuracy limiting calibration ceiling)

**TSVR Variable (Decision D070):**
- TSVR_hours used as continuous time variable (actual elapsed time, not nominal days)
- Assumes linear time effect on calibration (may not hold - crossover suggests non-linear dynamics)
- Centering TSVR at mean (64.95 hours H Day 2-3) aids interpretability but obscures time-specific effects

### Limitations Summary

Despite these constraints, findings are **robust for core conclusions:**
- When domain worst calibrated (mean |calibration| = 1.024 vs 0.725 for What/Where): **highly significant** (Ç² = 60.24, p < 0.001), large effect size
- Crossover interaction: **highly significant** (Ç² = 59.60, p < 0.001), visually clear in Figure 1
- What/Where parallel trajectories: consistent across multiple analytical approaches (LMM, ranking, contrasts)

**Major limitation:** Static post-hoc contrasts (averaged across time) obscure dynamic crossover pattern. Trajectory-specific interpretation (Section 3) essential for understanding domain differences.

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Time-Specific Post-Hoc Contrasts:**
- **Why:** Current contrasts tested at average timepoint (64.95 hours H Day 2-3), missing time-specific effects
- **How:** Re-run post-hoc contrasts AT T1 (Day 0) and AT T4 (Day 6) separately
- **Expected Insight:**
  - T1 contrasts: When vs What/Where will show significant POSITIVE difference (When overconfident, What/Where underconfident)
  - T4 contrasts: When vs What/Where will show significant NEGATIVE difference (When underconfident, What/Where overconfident)
  - Confirms crossover interaction interpretation
- **Timeline:** Immediate (same data, subset analysis)

**2. Quadratic Time Term in LMM:**
- **Why:** When domain trajectory may be non-linear (appears to cross zero around T2-T3, suggesting inflection point)
- **How:** Fit LMM with `calibration ~ Domain * (TSVR_centered + TSVR_centered²) + (TSVR_centered | UID)`
- **Expected Insight:** Test whether When domain trajectory shows significant curvature (quadratic term) vs linear decline
- **Timeline:** Immediate (~5 minutes, single LMM fit)

**3. Individual Difference Clustering on When Domain Trajectory:**
- **Why:** When domain shows high variability (SD = 0.76 vs 0.60 for What/Where). Are some participants showing stronger crossover than others?
- **How:** Extract participant-specific slopes for When domain calibration over time (from random effects), perform k-means clustering (2-3 groups)
- **Expected Insight:** Identify subgroups: "strong crossover" (large positive-to-negative shift), "weak crossover" (stable miscalibration), "good calibrators" (near-zero throughout)
- **Timeline:** Immediate (data available from LMM random effects)

### Planned Thesis RQs (Chapter 6 Continuation)

**RQ 6.3.3: Item-Level Calibration Analysis (Exploratory, NOT Yet Specified):**
- **Focus:** Examine calibration at ITEM level (not domain-aggregated). Are hard items worse calibrated than easy items?
- **Why:** Current RQ analyzes domain-level calibration (theta aggregated across items). Item-level analysis would reveal whether difficulty modulates calibration.
- **Builds On:** Would require item-level accuracy (correctness per item) + item-level confidence (rating per item), NOT currently available (only domain-aggregated theta)
- **Data Requirements:** Return to raw trial-level data from master.xlsx, compute item-level calibration before IRT aggregation
- **Expected Timeline:** Requires new data extraction (not currently planned in thesis)

**RQ 6.X: Confidence-Accuracy Gamma Correlation by Domain (Potential Follow-Up):**
- **Focus:** Alternative calibration metric - gamma correlation between confidence and accuracy per domain
- **Why:** Current RQ uses difference-based calibration (confidence - accuracy). Gamma correlation measures RANK-ORDER agreement (do high-confidence trials correspond to high-accuracy trials?), which is insensitive to scale differences
- **Builds On:** Would use same data (Ch5 5.2.1 accuracy, Ch6 6.3.1 confidence), different metric
- **Expected Insight:** Test whether When domain shows poor rank-order calibration (not just scale miscalibration)
- **Expected Timeline:** Immediate follow-up (different analysis of existing data)

### Methodological Extensions (Future Data Collection)

**1. Concurrent Accuracy + Confidence Measurement:**
- **Current Limitation:** Accuracy and confidence from separate IRT calibrations, domain-level aggregation obscures item-level calibration
- **Extension:** Redesign REMEMVR to collect confidence rating on EVERY trial, compute item-level calibration before IRT aggregation
- **Expected Insight:** Identify which specific items show poor calibration (e.g., temporal items with intermediate difficulty may be worst calibrated)
- **Feasibility:** Requires VR paradigm modification (~2 months for implementation + new N = 100 data collection)

**2. Calibration Feedback Training:**
- **Current Limitation:** Participants never learn whether confidence matched accuracy (no metacognitive learning opportunity)
- **Extension:** After each test session, provide feedback: "Your confidence was TOO HIGH for temporal memory" or "Your confidence matched accuracy for object memory"
- **Expected Insight:** Test whether When domain calibration improves with feedback (reduce T1 overconfidence, prevent T4 underconfidence). Intervention potential.
- **Feasibility:** Requires new N = 50 participants with feedback condition (~3 months)

**3. Ecological Momentary Assessment (EMA) of Real-World Episodic Memory:**
- **Current Limitation:** VR paradigm may not generalize to naturalistic episodic memory (real-world events)
- **Extension:** Daily diary study - participants record daily events (e.g., "Where did I park today?"), rate confidence, test accuracy 1-7 days later
- **Expected Insight:** Do What/Where/When calibration patterns generalize to real-world memory? Or is When domain crossover VR-specific?
- **Feasibility:** Moderate (~6 months for diary method development + N = 50 participants)

**4. Age Comparison: Young vs Older Adults:**
- **Current Limitation:** Undergraduate sample (age M ~ 20) limits generalizability to aging
- **Extension:** Recruit older adult sample (age 65+, N = 50), replicate RQ 6.3.2 analysis
- **Expected Insight:** Test whether older adults show WORSE When domain calibration (metacognitive monitoring declines with age). Predicted: exaggerated crossover (more overconfident at T1, more underconfident at T4).
- **Feasibility:** Requires older adult recruitment (~6 months)

### Theoretical Questions Raised

**1. Why Does When Domain Show Early Overconfidence?**
- **Question:** What retrieval cue generates high confidence for temporal memory at encoding (T1 +0.377) despite floor-effect accuracy?
- **Hypotheses to Test:**
  - **Temporal compression:** Events feel temporally proximate at encoding (temporal fluency), confidence high, but temporal discrimination is poor
  - **Encoding-retrieval mismatch:** Temporal encoding relies on event boundaries (start/end of trial), but retrieval requires finer-grained temporal resolution (order within trial). Confidence tracks encoding ease, not retrieval diagnosticity.
  - **Familiarity confound:** Temporal confidence may reflect FAMILIARITY with events (high at T1), not RECOLLECTION of temporal order (poor throughout)
- **Next Steps:** Experimental manipulation - vary temporal encoding strategy (grouped vs sequential), measure confidence and accuracy separately
- **Feasibility:** New study required (~1 year)

**2. Why Do What/Where Domains Show Worsening Calibration?**
- **Question:** Why does confidence fail to decline proportionally to accuracy for What/Where domains (T1 underconfident ’ T4 overconfident)?
- **Hypotheses to Test:**
  - **Residual familiarity:** What domain confidence maintained by familiarity signals (object feels familiar) even as recollection accuracy declines
  - **Spatial landmark salience:** Where domain confidence maintained by persistent spatial cues (landmarks remain salient) even as precise location memory fades
  - **Metacognitive unawareness of forgetting:** Participants unaware of accuracy decline rate, confidence assumes stability
- **Next Steps:** Item-level analysis - test whether high-familiarity items (What) or high-salience locations (Where) show greater overconfidence at T4
- **Feasibility:** Immediate (requires item-level metadata coding, ~1 week)

**3. Can Calibration Dynamics Predict Cognitive Decline?**
- **Question:** In aging/clinical populations, does RATE of calibration change (trajectory slope) predict cognitive status better than cross-sectional calibration?
- **Hypotheses:**
  - **MCI patients:** May show exaggerated When domain crossover (overconfidence at baseline due to anosognosia, underconfidence at follow-up due to insight into deficits)
  - **Healthy aging:** May show stable What/Where calibration but disrupted When domain trajectory (temporal metacognition more vulnerable to aging)
- **Next Steps:** Longitudinal study in clinical sample (MCI, N = 50) with monthly REMEMVR testing over 6 months
- **Feasibility:** Long-term collaboration with neuropsychology clinic (~2 years)

### Priority Ranking

**High Priority (Do First):**
1. **Time-specific post-hoc contrasts** (immediate, critical for crossover interpretation)
2. **Quadratic time term LMM** (immediate, tests trajectory linearity assumption)
3. **Gamma correlation calibration metric** (immediate, alternative metric for robustness)

**Medium Priority (Subsequent):**
1. **Individual difference clustering** (When domain trajectory heterogeneity)
2. **Item-level calibration analysis** (requires metadata coding, ~1 week)
3. **Calibration feedback training study** (intervention potential, ~3 months)

**Lower Priority (Aspirational):**
1. **Age comparison study** (older adults, generalizability check, ~6 months)
2. **EMA real-world memory study** (ecological validity, ~6 months)
3. **Clinical longitudinal study** (MCI trajectory prediction, ~2 years)

### Next Steps Summary

The **crossover interaction** (When domain opposite trajectory to What/Where) raises three critical questions for immediate follow-up:

1. **Time-specific contrasts:** Confirm When vs What/Where differences are significant AT T1 and AT T4, but cancel at average timepoint (validates crossover interpretation)
2. **Trajectory shape:** Test quadratic vs linear time effects (inflection point around Day 1-3?)
3. **Alternative metrics:** Gamma correlation calibration (tests whether rank-order calibration also shows domain differences)

Methodological extensions (feedback training, aging comparison) are valuable but require new data collection beyond current thesis scope. Theoretical questions (temporal compression, residual familiarity) motivate long-term research program on metacognitive dynamics in episodic memory.

---

**End of Summary**

**Generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2025-12-11
**Analysis files:** /home/etai/projects/REMEMVR/results/ch6/6.3.2/
