# Chapter 6: Metacognitive Monitoring in VR Episodic Memory

**Created:** 2025-12-06
**Status:** PLANNING
**Purpose:** Analyze confidence ratings to validate Ch5 findings and explore metacognition

---

## Design Rationale

### What Chapter 5 Established

**Universal Nulls (to validate with confidence):**
- Age × Forgetting Rate = NULL across all factor structures
- Domain Differences (What vs Where) = NULL
- Paradigm Differences (Free vs Cued vs Recognition) = NULL
- Schema Congruence Effects = NULL
- ICC_slope ≈ 0 (forgetting rate shows no trait-like variance)

**Robust Positives (to replicate with confidence):**
- Logarithmic forgetting curve (Ebbinghaus validated)
- Two-phase consolidation (6× faster early, then asymptote)
- IRT detects trajectory variance CTT misses
- Purification-Trajectory Paradox (4× replicated)

**Novel Discovery:**
- Source-Destination Dissociation (only strong clustering structure found)
- Opposite intercept-slope correlations (Source r=+0.99, Dest r=-0.90)

### Why Confidence Data is Special

**5-Level Likert Scale (0, 0.25, 0.5, 0.75, 1.0):**
- Complete guess → Absolutely certain
- One rating per item, per participant, per timepoint
- ~68 items × 100 participants × 4 timepoints = **27,200 confidence ratings**

**Advantages over dichotomous accuracy:**
1. **More information per response:** 5 levels vs 2 levels = 2.3× more bits
2. **Greater power for slope detection:** Ch5's ICC_slope ≈ 0 may be measurement limitation
3. **Continuous distribution:** Less floor/ceiling compression
4. **Metacognitive dimension:** Accuracy tells WHAT people remember; confidence tells WHETHER THEY KNOW IT

### Core Questions for Chapter 6

1. **Validation:** Do confidence trajectories mirror accuracy trajectories?
2. **Calibration:** Does confidence track accuracy as memories fade?
3. **Individual Differences:** Does confidence reveal slope variance that accuracy missed?
4. **False Certainty:** Do high-confidence errors increase over time?
5. **Predictive Power:** Can confidence predict future forgetting?

---

## Hierarchical RQ Structure

### Type 6.1: General Confidence Trajectories (ROOT)
*Establishes baseline confidence decline patterns*

| RQ | Title | Description | Ch5 Parallel |
|----|-------|-------------|--------------|
| 6.1.1 | Confidence Model Selection | Which functional form best describes confidence decline? (Log vs Lin vs Lin+Log vs Quad) | 5.1.1 |
| 6.1.2 | Two-Phase Confidence Pattern | Does confidence show early-rapid/late-slow phases like accuracy? | 5.1.2 |
| 6.1.3 | Age Effects on Confidence | Does age affect baseline confidence or confidence decline rate? | 5.1.3 |
| 6.1.4 | Confidence ICC Decomposition | Is confidence decline trait-like or state-like? (CRITICAL: more power than accuracy) | 5.1.4 |
| 6.1.5 | Confidence Trajectory Clustering | Do participants cluster into confidence phenotypes? | 5.1.5 |

**Expected Findings:**
- 6.1.1: Logarithmic decline expected (same as accuracy)
- 6.1.2: Two-phase pattern expected (consolidation affects confidence too)
- 6.1.3: NULL expected (age didn't affect accuracy trajectories)
- 6.1.4: **KEY TEST:** If ICC_slope > 0.10 for confidence but ≈ 0 for accuracy, this proves the dichotomous data limited slope detection
- 6.1.5: Expect 2-3 clusters (same as 5.1.5)

---

### Type 6.2: Calibration Dynamics (NEW - Unique to Ch6)
*Tests whether confidence tracks accuracy over time*

| RQ | Title | Description | Rationale |
|----|-------|-------------|-----------|
| 6.2.1 | Calibration Over Time | Does calibration (accuracy - confidence alignment) change from Day 0 to Day 6? | Core metacognition question |
| 6.2.2 | Under/Overconfidence Trajectory | Do people become overconfident as memories fade? | DRM false memory literature |
| 6.2.3 | Resolution Over Time | Does discrimination ability (gamma) decline over retention? | Metacognitive monitoring |
| 6.2.4 | Calibration by Accuracy Level | Are high vs low performers equally well-calibrated? | Individual differences |
| 6.2.5 | Age Effects on Calibration | Does calibration decline faster for older adults? | Metacognitive aging literature |

**Metrics:**
- **Calibration:** Mean(Confidence) - Mean(Accuracy) per person per timepoint
- **Resolution (Gamma):** Goodman-Kruskal gamma between confidence and correctness
- **Brier Score:** Mean squared error between confidence and accuracy
- **Expected Calibration Error (ECE):** Bin-weighted absolute calibration error

**Expected Findings:**
- 6.2.1: Calibration should remain stable IF confidence and accuracy decline in parallel
- 6.2.2: Overconfidence may emerge as accuracy drops faster than confidence adjusts
- 6.2.3: Resolution (gamma) expected to decline slightly (harder to discriminate when memory is worse)
- 6.2.4: High performers may be better calibrated (metacognitive skill correlates with memory skill)
- 6.2.5: NULL expected (age showed no accuracy trajectory effects)

---

### Type 6.3: Domain-Specific Confidence (What/Where/When)
*Mirrors Type 5.2 structure - tests domain effects on confidence*

| RQ | Title | Description | Ch5 Parallel |
|----|-------|-------------|--------------|
| 6.3.1 | Domain Confidence Trajectories | Do What/Where/When show different confidence decline? | 5.2.1 |
| 6.3.2 | Domain Calibration | Are people better calibrated for some domains than others? | NEW |
| 6.3.3 | Domain-Specific Age Effects | Does age interact with domain for confidence decline? | 5.2.3 |
| 6.3.4 | Domain Confidence ICC | Is confidence decline more trait-like for some domains? | 5.2.6 |

**Expected Findings:**
- 6.3.1: NULL expected (domains didn't differ for accuracy)
- 6.3.2: When domain may show OVER-calibration (low confidence matches low accuracy from floor effect)
- 6.3.3: NULL expected (age × domain was null for accuracy)
- 6.3.4: ICC_slope may be detectable here with 5-level data

**Note:** When domain had 77% item exclusion in Ch5. May need to exclude from confidence analyses too or analyze separately.

---

### Type 6.4: Paradigm-Specific Confidence (Free/Cued/Recognition)
*Mirrors Type 5.3 structure - tests paradigm effects on confidence*

| RQ | Title | Description | Ch5 Parallel |
|----|-------|-------------|--------------|
| 6.4.1 | Paradigm Confidence Trajectories | Do Free/Cued/Recognition show different confidence decline? | 5.3.1 |
| 6.4.2 | Paradigm Calibration | Are people better calibrated with more retrieval support? | NEW |
| 6.4.3 | Paradigm-Specific Age Effects | Does age interact with paradigm for confidence decline? | 5.3.4 |
| 6.4.4 | Paradigm Confidence ICC | Is confidence decline more trait-like for some paradigms? | 5.3.7 |

**Expected Findings:**
- 6.4.1: Recognition may show highest confidence (like accuracy), but NULL slope differences expected
- 6.4.2: Recognition may show OVER-confidence (high confidence but accuracy still declines)
- 6.4.3: NULL expected (age × paradigm was null for accuracy)
- 6.4.4: Free Recall may show highest ICC_slope (most individual variability in challenging tasks)

**Theoretical Interest:** Retrieval support affects BASELINE performance but not decay rate (Ch5). Does it affect CALIBRATION? If Recognition shows overconfidence, retrieval support may give false sense of remembering.

---

### Type 6.5: Schema Congruence and Confidence
*Mirrors Type 5.4 structure - tests schema effects on confidence*

| RQ | Title | Description | Ch5 Parallel |
|----|-------|-------------|--------------|
| 6.5.1 | Schema Confidence Trajectories | Do Common/Congruent/Incongruent show different confidence decline? | 5.4.1 |
| 6.5.2 | Schema Calibration | Are people better calibrated for congruent items? | NEW |
| 6.5.3 | High-Confidence Errors by Schema | Do schema-incongruent items produce more false certainty? | NEW (key) |

**Expected Findings:**
- 6.5.1: NULL expected (schema didn't affect accuracy trajectories)
- 6.5.2: Congruent items may show OVER-confidence (schema-consistent feels familiar)
- 6.5.3: **KEY TEST:** Schema-consistent false memories (DRM effect) - congruent items may generate high-confidence WRONG answers

**Theoretical Importance:** Schema effects were NULL for accuracy in Ch5. But schemas might affect CONFIDENCE without affecting ACCURACY - you feel more certain about schema-consistent information even if you're not more accurate.

---

### Type 6.6: High-Confidence Errors (NEW - Unique to Ch6)
*Analyzes false certainty and metacognitive failures*

| RQ | Title | Description | Rationale |
|----|-------|-------------|-----------|
| 6.6.1 | High-Confidence Error Rate Over Time | Do high-confidence errors increase from Day 0 to Day 6? | Memory distortion literature |
| 6.6.2 | High-Confidence Error Profiles | Who makes high-confidence errors? (baseline ability, age, confidence bias) | Individual differences |
| 6.6.3 | Domain Specificity of Errors | Are high-confidence errors domain-specific (more for What vs Where)? | Binding hypothesis |

**Definition:** High-Confidence Error = Confidence ≥ 0.75 AND Accuracy = 0

**Expected Findings:**
- 6.6.1: HCE rate may INCREASE over time as memories degrade but confidence doesn't fully adjust
- 6.6.2: Low baseline performers may make more HCEs (poor memory + poor metacognition)
- 6.6.3: When domain may show most HCEs (floor effect + uncertainty about temporal order)

---

### Type 6.7: Predictive Validity (NEW - Unique to Ch6)
*Tests whether early confidence predicts future forgetting*

| RQ | Title | Description | Rationale |
|----|-------|-------------|-----------|
| 6.7.1 | Day 0 Confidence Predicts Forgetting | Does high initial confidence predict slower forgetting? | JOL literature |
| 6.7.2 | Confidence Variability Predicts Stability | Do people with variable confidence show variable memory? | Metacognitive consistency |
| 6.7.3 | Calibration Predicts Forgetting | Are well-calibrated people more stable forgetters? | Metacognitive skill |

**Expected Findings:**
- 6.7.1: Weak positive relationship expected (high confidence items are well-encoded)
- 6.7.2: High variability may predict instability (metacognitive noise reflects encoding noise)
- 6.7.3: Well-calibrated people may have more predictable forgetting curves

---

### Type 6.8: Source-Destination Confidence (Extends Ch5 Discovery)
*Applies confidence analysis to the one factor that showed structure*

| RQ | Title | Description | Ch5 Parallel |
|----|-------|-------------|--------------|
| 6.8.1 | Source-Destination Confidence Trajectories | Do source vs destination show different confidence decline? | 5.5.1 |
| 6.8.2 | Source-Destination Calibration | Are people better calibrated for source or destination? | NEW |
| 6.8.3 | Source-Destination ICC | Does confidence ICC reveal the same opposite-correlation pattern? | 5.5.6 |
| 6.8.4 | Source-Destination Confidence Clustering | Does confidence clustering replicate the strong 4-cluster structure? | 5.5.7 |

**Expected Findings:**
- 6.8.1: Destination may show faster confidence decline (matching accuracy pattern)
- 6.8.2: Source may be better calibrated (lower uncertainty about pick-up locations)
- 6.8.3: **KEY TEST:** If opposite intercept-slope correlations replicate in confidence, this is a fundamental memory-metacognition dissociation
- 6.8.4: If clustering is also strong for confidence, source-destination is genuinely special

**Theoretical Importance:** Source-Destination was the ONLY factor to show strong clustering in Ch5. If confidence replicates this, it validates that source-destination dissociation reflects real individual difference structure.

---

## Summary Table

| Type | Focus | # RQs | Ch5 Parallel | Primary Question |
|------|-------|-------|--------------|------------------|
| 6.1 | General Confidence | 5 | 5.1 | Does confidence decline like accuracy? |
| 6.2 | Calibration Dynamics | 5 | NEW | Does confidence track accuracy over time? |
| 6.3 | Domain Confidence | 4 | 5.2 | Do domains differ in confidence/calibration? |
| 6.4 | Paradigm Confidence | 4 | 5.3 | Do paradigms differ in confidence/calibration? |
| 6.5 | Schema Confidence | 3 | 5.4 | Does schema affect confidence/false certainty? |
| 6.6 | High-Confidence Errors | 3 | NEW | When do people feel certain but wrong? |
| 6.7 | Predictive Validity | 3 | NEW | Can confidence predict future forgetting? |
| 6.8 | Source-Destination | 4 | 5.5 | Does the one strong factor replicate? |
| **TOTAL** | | **31** | | |

---

## What We Removed from Original Ch6 Plan

1. **IRT-CTT Convergence RQs:** Ch5 already established IRT superiority 4× over. Not needed for confidence.
2. **Purification RQs:** The paradox is documented. Apply purification as needed, don't make it an RQ.
3. **Consolidation Window RQs:** Subsumed into 6.1.2 (two-phase pattern). Don't need separate piecewise analyses.
4. **Redundant Validation RQs:** Ch5 validated methodology. Ch6 can use it.

## What We Added

1. **Type 6.2 (Calibration):** Core metacognition not possible with accuracy alone
2. **Type 6.6 (High-Confidence Errors):** False certainty is a unique confidence phenomenon
3. **Type 6.7 (Predictive Validity):** Confidence as predictor, not just outcome
4. **Type 6.8 (Source-Destination):** Extend the ONE factor that worked in Ch5

## What We Kept/Adapted

1. **General trajectories (6.1):** Parallel to 5.1, validates with different measure
2. **Domain/Paradigm/Schema (6.3-6.5):** Parallel structure, but focused on calibration questions
3. **Age effects:** Tested within each type, not as separate type
4. **ICC decomposition:** Tested within types, especially important with 5-level data

---

## Critical Hypotheses

### H1: ICC_slope Will Be Detectable for Confidence
Ch5 found ICC_slope ≈ 0 for accuracy, but this may be a limitation of dichotomous data (4 timepoints × 0/1 = low power for slope estimation). With 5-level confidence data, we have 2.3× more information per response. If ICC_slope > 0.10 for confidence, this proves:
- Individual differences in metacognitive decline EXIST
- The accuracy ICC_slope ≈ 0 was a measurement limitation, not a true null

### H2: All Ch5 Nulls Will Replicate
If age, domain, paradigm, and schema effects are NULL for confidence trajectories (as they were for accuracy), this provides strong convergent validity. The nulls aren't IRT artifacts—they're genuine properties of VR episodic memory.

### H3: Calibration Will Reveal New Information
Even if trajectories match (both decline logarithmically), calibration can diverge:
- If confidence declines SLOWER than accuracy → overconfidence emerges
- If confidence declines FASTER than accuracy → underconfidence emerges
- If calibration varies by factor → domain/paradigm affects metacognition differently than memory

### H4: Source-Destination Will Replicate
The opposite intercept-slope correlations (Source r=+0.99, Destination r=-0.90) should replicate in confidence if they reflect fundamental memory processing differences. This would be a major finding—the only factor in Ch5 with real structure also shows structure in metacognition.

---

## Data Requirements

### Confidence Tags (TC_)
- 5-level ordinal: 0, 0.25, 0.5, 0.75, 1.0
- One rating per item × participant × timepoint
- Same items as accuracy (TQ_)
- Requires extraction from master.xlsx

### IRT for Confidence
- Graded Response Model (GRM) for 5 categories
- Same analysis sets as accuracy: All, All by Domain, All by Paradigm
- Produces Theta_Confidence scores

### Derived Metrics
- **Calibration:** Mean(Confidence) - Mean(Accuracy)
- **Resolution (Gamma):** Goodman-Kruskal gamma
- **Brier Score:** Mean squared error
- **High-Confidence Error Rate:** P(Correct=0 | Confidence ≥ 0.75)

---

## Bonferroni Correction

**31 RQs → α = 0.05 / 31 = 0.00161 per RQ**

Or by type:
- Type 6.1: α = 0.01 (5 RQs)
- Type 6.2: α = 0.01 (5 RQs)
- Type 6.3: α = 0.0125 (4 RQs)
- Type 6.4: α = 0.0125 (4 RQs)
- Type 6.5: α = 0.0167 (3 RQs)
- Type 6.6: α = 0.0167 (3 RQs)
- Type 6.7: α = 0.0167 (3 RQs)
- Type 6.8: α = 0.0125 (4 RQs)

---

## Next Steps

1. **Extract TC_ data** from master.xlsx
2. **Run IRT pipeline** on confidence data (GRM 5-category)
3. **Create Type 6.1 specifications** (parallel to 5.1 structure)
4. **Execute Type 6.1** to establish baseline confidence patterns
5. **Proceed through types** in parallel where possible

---

**End of Chapter 6 Plan**
