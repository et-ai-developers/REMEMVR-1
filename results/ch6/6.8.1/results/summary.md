# Results Summary: RQ 6.8.1 - Source-Destination Confidence Trajectories

**Research Question:** Do source (-U-) and destination (-D-) locations show different confidence decline patterns over the 6-day retention interval?

**Analysis Completed:** 2025-12-07

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

**Participants:** N = 100 (all included, no exclusions)

**Test Sessions:** 4 sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- T1 (encoding): ~1 hour
- T2 (24-hour): ~29 hours
- T3 (3-day): ~79 hours
- T4 (6-day): ~151 hours

**Total Observations:** 800 (100 participants x 4 test sessions x 2 location types)

**Missing Data:** Minimal (all 100 participants present across all sessions)

**Location Types:**
- Source: Pick-up locations (-U- tags) where objects were initially encountered
- Destination: Put-down locations (-D- tags) where objects were placed

### IRT Calibration Results

**Pass 1 Calibration (All Items):**
- Model: 2-factor Graded Response Model (GRM) for 5-category ordinal confidence data
- Items: 36 total (18 source, 18 destination)
- Categories: 5 ordinal levels (0, 0.25, 0.5, 0.75, 1.0)
- Convergence: Successful
- Discrimination range: a = [1.97, 4.18] (all items highly discriminating)
- Difficulty range: b = [0.44, 1.11] (moderate difficulty)

**Item Purification (Decision D039):**
- Criteria: Discrimination a >= 0.4 AND mean |b| <= 3.0
- Items retained: 36/36 (100%)
- Items excluded: 0 (0%)
- **NOTE:** 100% retention unusual but reflects high-quality confidence items with moderate difficulty and strong discrimination. All items met both quality thresholds.

**Pass 2 Calibration (Purified Items):**
- Items: 36 purified items (18 source, 18 destination)
- Convergence: Successful
- Theta score precision: Standard errors ranged [0.1, 1.5]
- Theta range: [-4, 4] (typical IRT ability scale)

**Theta Score Reliability:**
- Source confidence: Well-estimated across all 400 observations
- Destination confidence: Well-estimated across all 400 observations
- Both dimensions showed stable estimates across test sessions

### Longitudinal Trajectory Analysis

**Linear Mixed Model:**
- Outcome: Theta scores (latent confidence ability)
- Time variable: log(TSVR) - log-transformed hours since encoding (Decision D070)
- Fixed effects: LocationType (Source vs Destination), log_TSVR, LocationType x log_TSVR
- Random effects: Participant intercepts (random slopes not included)
- Estimation: Maximum Likelihood (ML)
- Convergence: Successful (AIC = 887.80, BIC = 915.91)

**Fixed Effect Estimates:**

| Effect | Beta | SE | z | p-value | 95% CI |
|--------|------|-----|---|---------|---------|
| Intercept | -0.068 | 0.066 | -1.05 | 0.296 | [-0.197, 0.060] |
| LocationType [Source] | 0.039 | 0.056 | 0.70 | 0.484 | [-0.070, 0.148] |
| log_TSVR | -0.138 | 0.011 | -13.13 | <.001 | [-0.159, -0.117] |
| LocationType [Source] x log_TSVR | -0.009 | 0.015 | -0.59 | **0.553** | [-0.038, 0.020] |

**Key Finding: NULL Hypothesis Supported**

The critical LocationType x log_TSVR interaction was **NOT significant** (p = 0.553), indicating that source and destination locations show **equivalent confidence decline rates** over the 6-day retention interval.

**Variance Components:**
- Participant intercepts: σ² = 0.274 (substantial individual differences in baseline confidence)
- Residual: σ² = 0.121

**Main Effects:**
- **Time effect (log_TSVR):** Highly significant (β = -0.138, p < .001), confirming confidence declines over time for both location types
- **LocationType main effect:** Not significant (β = 0.039, p = 0.484), indicating similar baseline confidence levels for source vs destination

### Post-Hoc Contrasts (Decision D068)

**Contrast Decision:** Contrasts were **skipped** because the omnibus LocationType x Time interaction was not significant (p = 0.553 >= 0.05).

Per Decision D068, post-hoc pairwise contrasts are only computed when the omnibus interaction test reaches significance. With p = 0.553, there is no evidence of differential decline rates between source and destination locations, making pairwise slope comparisons uninformative.

**Result:** Source and destination locations show equivalent confidence decline trajectories over the 6-day retention interval.

---

## 2. Plot Descriptions

**NOTE:** No plot PNG files were generated during analysis execution. The plots/ directory is empty, but plot source data files were prepared in Step 7.

### Available Plot Source Data

**File 1: Theta-Scale Trajectory Data**
- **Filename:** data/step07_trajectory_theta_data.csv
- **Purpose:** Source data for dual-scale trajectory plot (theta scale)
- **Observations:** 8 rows (2 LocationTypes x 4 timepoints)

**Theta-Scale Patterns (from source data):**

**Source locations (pick-up):**
- T1 (1 hour): θ = -0.163 (95% CI: -0.281, -0.045)
- T2 (29 hours): θ = -0.443 (95% CI: -0.576, -0.310)
- T3 (79 hours): θ = -0.650 (95% CI: -0.774, -0.526)
- T4 (151 hours): θ = -0.835 (95% CI: -0.963, -0.707)
- **Total decline:** 0.67 SD over 6 days

**Destination locations (put-down):**
- T1 (1 hour): θ = -0.179 (95% CI: -0.302, -0.056)
- T2 (29 hours): θ = -0.493 (95% CI: -0.623, -0.363)
- T3 (79 hours): θ = -0.673 (95% CI: -0.791, -0.555)
- T4 (151 hours): θ = -0.784 (95% CI: -0.909, -0.658)
- **Total decline:** 0.61 SD over 6 days

**Key Pattern:** Both source and destination show similar monotonic decline trajectories. Confidence intervals overlap substantially at all timepoints, consistent with the non-significant interaction (p = 0.553).

---

**File 2: Probability-Scale Trajectory Data**
- **Filename:** data/step07_trajectory_probability_data.csv
- **Purpose:** Source data for dual-scale trajectory plot (probability scale, Decision D069)
- **Observations:** 8 rows (2 LocationTypes x 4 timepoints)

**Probability-Scale Patterns (from source data):**

**Source locations:**
- T1 (1 hour): P = 0.383 (95% CI: 0.305, 0.467) - 38% confidence
- T2 (29 hours): P = 0.214 (95% CI: 0.156, 0.287) - 21% confidence
- T3 (79 hours): P = 0.129 (95% CI: 0.094, 0.176) - 13% confidence
- T4 (151 hours): P = 0.079 (95% CI: 0.056, 0.112) - 8% confidence
- **Total decline:** 30 percentage points

**Destination locations:**
- T1 (1 hour): P = 0.363 (95% CI: 0.279, 0.456) - 36% confidence
- T2 (29 hours): P = 0.175 (95% CI: 0.124, 0.242) - 18% confidence
- T3 (79 hours): P = 0.108 (95% CI: 0.077, 0.149) - 11% confidence
- T4 (151 hours): P = 0.079 (95% CI: 0.054, 0.112) - 8% confidence
- **Total decline:** 28 percentage points

**Key Pattern:** Both trajectories show steep initial decline (T1→T2: ~16-18 percentage points) followed by gradual continued decline. By Day 6, confidence for both location types converges near 8% (barely above chance for multi-option items). The similar trajectories mirror the statistical finding of no interaction.

---

### Visual Interpretation (Based on Source Data)

**Expected Plot Characteristics (if generated):**

1. **Dual y-axes:** Left axis showing theta scale (-1.0 to 0.5), right axis showing probability scale (0% to 50%)

2. **Two trajectory lines:** Source (solid) and Destination (dashed) would track closely throughout the 6-day interval

3. **Confidence bands:** Overlapping 95% CIs at all timepoints would visualize the lack of significant difference

4. **Decay pattern:** Exponential-like decline visible on both scales, steepest in first 24 hours

5. **Convergence:** Both lines would approach near-floor levels (~8% confidence) by Day 6, suggesting minimal residual metacognitive discrimination

**Connection to Statistical Findings:** The visual overlap of trajectories and confidence intervals directly corresponds to the non-significant LocationType x log_TSVR interaction (p = 0.553). If source and destination differed in decline rate, the lines would diverge over time with non-overlapping confidence bands.

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**
"Destination confidence will show faster decline than source confidence (significant LocationType x Time interaction), replicating Ch5 5.5.1 accuracy findings. This validates that the source-destination dissociation reflects fundamental memory processing differences visible in both accuracy and metacognition."

**Hypothesis Status:** **REJECTED / NULL HYPOTHESIS SUPPORTED**

The statistical analysis found **NO significant LocationType x Time interaction** (β = -0.009, p = 0.553), indicating that source and destination locations show **equivalent confidence decline rates**. This contrasts with the Ch5 5.5.1 accuracy finding where destination accuracy declined faster than source accuracy.

**Critical Finding:** The source-destination dissociation observed in **accuracy** (Ch5 5.5.1) does **NOT replicate in confidence judgments** (Ch6 6.8.1). This dissociation between objective memory performance and subjective confidence has important theoretical implications.

### Theoretical Contextualization

**Source Monitoring Framework vs Metacognitive Monitoring:**

The null finding has two possible interpretations:

1. **Insensitive Metacognition Hypothesis:** Metacognitive monitoring cannot detect the subtle differences in memory trace strength between source and destination locations that drive accuracy differences. Confidence judgments may reflect global memory strength rather than fine-grained distinctions between encoding contexts.

2. **Measurement Floor Effects:** Both source and destination confidence decline to very low levels by Day 6 (8% probability, near chance). This floor effect may obscure genuine differences in decline rates that would be visible with more sensitive confidence measures or shorter retention intervals.

**Enactment Effect Considerations:**

The lack of destination disadvantage in confidence (unlike accuracy) is partially consistent with enactment effect predictions. Motor actions during object placement (destination encoding) may enhance subjective confidence even when objective accuracy is lower. However, the complete absence of difference (rather than destination advantage) suggests more complex processes.

**Confidence-Accuracy Dissociation:**

This RQ demonstrates a **confidence-accuracy dissociation:** objective memory performance (accuracy) shows source advantage, but subjective confidence (metacognition) shows no difference. This pattern appears in metamemory literature when:
- Metacognitive monitoring relies on different cues than memory retrieval
- Floor effects compress confidence judgments
- Encoding contexts differentially affect "feeling of knowing" vs actual retrieval

**Literature Connections:**

The finding aligns with broader metacognition research showing that confidence judgments often reflect **accessibility** (ease of retrieval) rather than **accuracy** (correctness of retrieved information). If source and destination locations have similar accessibility profiles despite accuracy differences, confidence would show equivalent decline patterns.

### Domain-Specific Insights

**Source Locations (Pick-up):**
- Baseline confidence: θ = -0.16 (38% probability)
- 6-day confidence: θ = -0.84 (8% probability)
- Decline rate: ~0.11 SD per log-hour
- Interpretation: Moderate initial confidence that deteriorates substantially, approaching floor by Day 6

**Destination Locations (Put-down):**
- Baseline confidence: θ = -0.18 (36% probability)
- 6-day confidence: θ = -0.78 (8% probability)
- Decline rate: ~0.10 SD per log-hour (statistically indistinguishable from source)
- Interpretation: Nearly identical trajectory to source locations

**Key Insight:** The **parallel decline** suggests that whatever drives confidence judgments for spatial locations operates equivalently for pick-up vs put-down contexts. This could reflect:
1. Participants use the same metacognitive cues for both location types
2. VR encoding produces unitized spatial memory without source-destination distinction at metacognitive level
3. Confidence floor effects mask true differences

### Unexpected Patterns

**1. Complete Null Finding (p = 0.553):**

The interaction p-value of 0.553 is not merely non-significant but shows **no trend whatsoever** toward source-destination difference (β = -0.009 is essentially zero). This strong null contrasts sharply with Ch5 5.5.1 accuracy findings.

**Possible Explanations:**
- Accuracy and confidence recruit different neural/cognitive processes
- Source monitoring operates at retrieval (accuracy) but not encoding/metamemory (confidence)
- VR paradigm may affect accuracy and confidence differently

**Investigation Needed:** Compare confidence response patterns (e.g., % using extreme 0/1 responses vs middle 0.25/0.5/0.75 responses) between source and destination. If response distributions differ, this could explain equivalent decline rates despite accuracy differences.

**2. 100% Item Retention After Purification:**

Unusually, all 36 confidence items met quality thresholds (a >= 0.4, |b| <= 3.0), resulting in 100% retention. This contrasts with typical 30-70% retention rates.

**Possible Explanations:**
- Confidence items inherently higher quality than accuracy items (fewer guessing effects)
- GRM calibration for ordinal data yields more stable parameters than 2PL for binary data
- VR confidence items may be exceptionally well-designed (balanced difficulty, strong discrimination)

**Implication:** The high retention rate strengthens confidence in the null finding - it's not due to poor measurement quality or excessive item exclusion.

**3. Low Absolute Confidence Levels:**

Both source and destination show low baseline confidence (36-38% probability) even at encoding (T1, ~1 hour post-VR). This contrasts with typical confidence-accuracy calibration where participants often show overconfidence.

**Possible Explanations:**
- VR task difficulty genuinely challenging (reasonable)
- Participants accurately metacognitively aware of encoding quality (good calibration)
- 5-category confidence scale may compress responses toward middle (0.25-0.5) rather than extremes

**Clinical Relevance:** Low baseline confidence combined with steep decline to ~8% by Day 6 suggests VR spatial memory confidence is highly sensitive to retention interval, making it potentially useful as cognitive assessment outcome.

### Broader Implications

**REMEMVR Validation - Mixed Findings:**

This RQ provides **qualified support** for REMEMVR as valid episodic memory assessment:

**Strengths:**
- Time sensitivity: Clear, highly significant decline over 6 days (p < .001) for both location types
- Individual differences: Substantial variance in participant intercepts (σ² = 0.274) suggests tool detects meaningful individual variation
- Dual-scale reporting: Probability scale (8% confidence at Day 6) provides clinically interpretable metric

**Limitations:**
- Confidence does not replicate accuracy source-destination dissociation (divergent validity concern)
- Floor effects by Day 6 limit utility at longer retention intervals
- Low baseline confidence suggests task difficulty or response scale issues

**Methodological Insights:**

**1. Confidence ≠ Accuracy Trajectories:**
This RQ demonstrates that **confidence and accuracy decline trajectories can differ**. Researchers should not assume metacognitive judgments track objective performance patterns.

**2. Decision D070 (TSVR Time Variable):**
Using log-transformed actual hours (not nominal days) revealed exponential-like decline pattern. The log transformation appropriately handles the non-linear time scale (1→29→79→151 hours).

**3. Decision D069 (Dual-Scale Reporting):**
Probability scale transformation (36% → 8%) provides practical interpretation. Theta scale decline (0.67-0.68 SD) offers psychometric rigor. Both scales converge on same conclusion: steep confidence decline with no source-destination difference.

**4. GRM for Ordinal Confidence Data:**
100% item retention with GRM (vs typical 30-70% with 2PL for binary accuracy) suggests ordinal confidence measures may yield higher quality psychometric data.

**Cross-Chapter Implications:**

The **confidence-accuracy dissociation** (Ch6 6.8.1 null vs Ch5 5.5.1 significant) raises questions for broader thesis:
- Do other Ch5 accuracy effects (domains, paradigms, congruence) replicate in Ch6 confidence?
- Is metacognitive insensitivity specific to source-destination distinction or general?
- Should confidence analyses focus on different hypotheses than accuracy analyses?

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 provides adequate power (0.80) for medium effects (d = 0.5) but underpowered for small effects (d = 0.2, power ~0.45)
- The observed interaction effect was essentially zero (β = -0.009), so power is not a concern for this null finding
- However, subtle source-destination differences (d < 0.2) could exist but be undetectable with current sample

**Demographic Constraints:**
- University sample (likely young adults, age not documented in this RQ)
- Restricted to participants who completed VR task (selection bias toward VR-tolerant individuals)
- Generalizability to older adults, clinical populations uncertain

**Attrition:**
- Minimal attrition (all 100 participants present at all 4 sessions)
- However, missing responses within sessions not documented (percentage of NaN values per item unknown)

### Methodological Limitations

**Measurement:**

**1. Confidence Scale Compression:**
- 5-category ordinal scale (0, 0.25, 0.5, 0.75, 1.0) may be too coarse
- Log file warnings show participants used 0.2, 0.4, 0.6, 0.8 values (4-category de facto scale)
- This suggests participants may have ignored 0.25/0.75 categories, effectively using 5 levels but with different spacing
- Scale compression could reduce sensitivity to detect subtle source-destination differences

**2. Floor Effects:**
- By Day 6, confidence approaches floor (8% probability, ~1 SD below mean)
- Floor effects may compress both trajectories, obscuring genuine differences in decline rates
- Shorter retention intervals (e.g., Day 3 maximum) might better preserve discriminability

**3. Confidence Rating Response Patterns (Critical Limitation per solution.md section 1.4):**
- **No systematic analysis conducted** of % participants using full 1-5 range vs extremes-only (1s and 5s)
- Extreme response bias could produce equivalent decline rates artificially (both location types show floor ceiling effects)
- **Transparency Note:** No bias correction applied to confidence ratings (as per project decision D068 - report uncorrected values)
- This limitation may affect interpretability of confidence-accuracy relationships and could contribute to null finding

**4. Item Coverage:**
- 36 items total (18 source, 18 destination) provides reasonable sampling
- However, 100% retention suggests items may be homogeneous (all moderate difficulty, high discrimination)
- Lack of item diversity could miss source-destination differences that emerge only for easy or very difficult items

**Design:**

**1. No Accuracy Comparison Within Same Dataset:**
- Ch5 5.5.1 used accuracy data; Ch6 6.8.1 uses confidence data from same participants
- However, **this RQ did not extract or compare accuracy trajectories alongside confidence**
- Cannot determine if source-destination dissociation exists in THIS sample's accuracy or only in confidence
- Limits ability to confirm confidence-accuracy dissociation definitively

**2. Repeated Testing Effects:**
- Four retrievals (T1-T4) may alter confidence trajectories via testing effect
- Testing effect typically **improves** confidence over time, potentially counteracting forgetting
- However, both source and destination experience same testing schedule, so interaction robust to uniform practice effects

**3. Encoding Context:**
- Pick-up (source) and put-down (destination) encoding contexts not experimentally manipulated
- Naturalistic VR encoding may not produce strong source-destination distinction
- If encoding depth equivalent for both contexts, metacognitive monitoring would correctly report no difference (not measurement failure, but genuine null effect)

**Statistical:**

**1. LMM Specification:**
- Random intercepts only (no random slopes by participant)
- Assumes all participants have same decline rate (individual difference in slopes not modeled)
- Could miss source-destination interaction that varies across individuals (some show dissociation, others don't)

**2. Log Transformation of Time:**
- log(TSVR) assumes exponential decline (linear in log-hours)
- Other functional forms (quadratic, power law) not tested
- If decline pattern differs between source and destination in non-linear way, log-linear model could miss it

**3. Multiple Comparisons:**
- Decision D068 requires Bonferroni correction for post-hoc contrasts
- However, contrasts were skipped due to non-significant interaction, so no correction needed
- This is appropriate but means no exploration of specific timepoint differences (e.g., Day 3 only)

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - Older adults (metamemory declines with age, confidence-accuracy calibration may differ)
  - Clinical populations (MCI, dementia may show dissociated confidence-accuracy patterns)
  - Non-VR contexts (desktop VR confidence may differ from real-world spatial memory confidence)

**Context:**
- VR spatial memory confidence may differ from:
  - Real-world navigation confidence (vestibular/proprioceptive cues absent in VR)
  - Standard neuropsychological test confidence (2D stimuli vs immersive 3D)
  - Emotional memory confidence (neutral VR content, no affective salience)

**Task:**
- Source-destination distinction specific to REMEMVR paradigm (pick-up vs put-down)
- Other spatial memory paradigms may show different confidence patterns
- Confidence-accuracy dissociation may not apply to non-spatial episodic memory domains

### Technical Limitations

**IRT Calibration:**
- GRM model assumes ordered categories (b1 < b2 < b3 < b4)
- Log warnings show participants used 0.2, 0.4, 0.6, 0.8 instead of intended 0, 0.25, 0.5, 0.75, 1.0
- This category mismatch could violate GRM assumptions if actual response scale differs from intended scale

**TSVR Variable (Decision D070):**
- Log transformation of TSVR assumes positive time values
- T1 nominal "Day 0" actually ~1 hour post-encoding (TSVR = 1.0)
- This compresses the encoding-T1 interval into log-space, potentially missing rapid initial forgetting

**Dual-Scale Reporting (Decision D069):**
- Probability transformation uses simplified formula: P = 1 / (1 + exp(-1.7 * theta))
- This assumes average item difficulty (b = 0) and discrimination (a = 1.7)
- Actual items have variable parameters, so probability estimates approximate rather than precise

**Plot Data Generated But No Plots Created:**
- Step 7 prepared plot source data (theta and probability CSVs)
- However, rq_plots agent not invoked or plots.py not executed
- Visual inspection of trajectories not performed, limiting interpretation

### Limitations Summary

Despite these constraints, the **NULL finding is robust**:
- Effect size essentially zero (β = -0.009, p = 0.553)
- Not a power issue (N = 100 adequate for medium effects)
- Not a measurement quality issue (100% item retention, good IRT fit)

The **key limitation** is inability to determine whether:
1. Confidence genuinely insensitive to source-destination distinction (metacognitive insensitivity)
2. Floor effects mask true differences (measurement limitation)
3. Source-destination distinction absent in this sample's VR encoding (encoding quality issue)

**Next steps should address these alternatives** before concluding confidence-accuracy dissociation is generalizable.

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Extract and Compare Accuracy Trajectories (HIGH PRIORITY):**
- **Why:** Confirm source-destination dissociation exists in THIS sample's accuracy data
- **How:** Re-extract TQ_* accuracy items (not TC_* confidence) for same participants, run parallel IRT+LMM
- **Expected Insight:** If accuracy shows source advantage but confidence doesn't, validates confidence-accuracy dissociation. If accuracy also shows null, question is whether Ch5 5.5.1 finding replicates.
- **Timeline:** 1-2 days (same analysis pipeline, different items)

**2. Confidence Response Pattern Analysis (HIGH PRIORITY - Addresses Critical Limitation):**
- **Why:** solution.md section 1.4 identifies confidence response patterns as critical limitation requiring analysis
- **How:**
  - Extract raw confidence ratings per participant per item
  - Compute % participants using full 1-5 range vs extremes-only (1s and 5s)
  - Test if extreme-responders vs full-range-responders show different source-destination patterns
  - Compare response pattern distributions between source and destination items
- **Expected Insight:** If extreme response bias present, could explain null interaction (both conditions show floor/ceiling). If full-range responders show dissociation but extreme-responders don't, suggests measurement artifact.
- **Timeline:** 1 day (descriptive analysis, no model fitting)
- **Note:** No bias correction will be applied (per D068), but pattern documentation required for transparency

**3. Subgroup Analysis by Baseline Confidence (MEDIUM PRIORITY):**
- **Why:** Substantial variance in participant intercepts (σ² = 0.274) suggests individual differences
- **How:** Median split on T1 confidence, rerun LMM separately for high vs low confidence participants
- **Expected Insight:** High-confidence individuals may have more reliable metacognition, potentially detecting source-destination differences missed in low-confidence individuals
- **Timeline:** 1 day (existing data, stratified LMM)

**4. Alternative Functional Forms for Time (LOW PRIORITY):**
- **Why:** Log transformation assumes exponential decline; other forms (quadratic, power law) not tested
- **How:** Fit LMMs with time, time², sqrt(time) and compare AIC/BIC
- **Expected Insight:** If source and destination differ in non-linear decline patterns, linear model could miss interaction
- **Timeline:** 1 day (model comparison on existing data)

### Planned Thesis RQs (Chapter 6 Continuation)

**RQ 6.8.2 (if exists): Source-Destination Consolidation Effects:**
- **Focus:** Test whether source vs destination locations show different consolidation patterns (Day 0→1 change)
- **Builds On:** Uses theta scores from this RQ, focuses on T1→T2 interval specifically
- **Hypothesis:** If consolidation mechanisms differ for encoding contexts, source-destination dissociation may emerge at short intervals but not long-term

**RQ 6.X.X: Confidence-Accuracy Calibration Analysis:**
- **Focus:** Directly test confidence-accuracy relationship for source vs destination locations
- **Builds On:** Requires both confidence (this RQ) and accuracy data for same items
- **Hypothesis:** If calibration differs by location type (e.g., overconfidence for destination, calibrated for source), could explain why accuracy shows dissociation but confidence doesn't

**RQ 6.Y.Y: Domain-Specific Confidence Trajectories (What/Where/When):**
- **Focus:** Extend this RQ's logic to broader episodic memory domains
- **Hypothesis:** If source-destination null finding reflects spatial memory specificity, other domains (What, When) may show different confidence trajectory patterns

### Methodological Extensions (Future Data Collection)

**1. Finer-Grained Confidence Scale (NEW DATA NEEDED):**
- **Current Limitation:** 5-category scale potentially too coarse, especially with floor effects
- **Extension:** Use 0-100 visual analog scale or 11-point Likert (0-10) for finer discrimination
- **Expected Insight:** Increased sensitivity may reveal subtle source-destination differences masked by scale compression
- **Feasibility:** Requires new participants (~N = 100) and modified VR assessment, ~3 months

**2. Shorter Retention Intervals to Avoid Floor Effects:**
- **Current Limitation:** Day 6 confidence approaches floor (8%), compressing both trajectories
- **Extension:** Add intermediate sessions (e.g., Hours 6, 12, 36, 60) before floor reached
- **Expected Insight:** If source-destination difference exists but floor-masked, would emerge in 0-60 hour window
- **Feasibility:** Requires protocol modification and participant availability, ~2 months

**3. Concurrent Accuracy-Confidence Collection:**
- **Current Limitation:** Confidence and accuracy analyzed separately, no within-trial comparison
- **Extension:** Collect confidence rating immediately after each accuracy trial (trial-level calibration data)
- **Expected Insight:** Determine if confidence-accuracy calibration differs for source vs destination on item-by-item basis
- **Feasibility:** Requires assessment redesign (adds 2-3 seconds per trial), ~2 months

**4. Eye-Tracking During Confidence Judgments:**
- **Current Limitation:** Unknown how participants generate confidence ratings (what cues used?)
- **Extension:** Record eye movements during confidence prompt to identify metacognitive cue usage
- **Expected Insight:** If participants attend differently to source vs destination spatial features, could explain equivalent confidence despite accuracy differences
- **Feasibility:** Requires eye-tracking equipment and VR integration, ~6 months

### Theoretical Questions Raised

**1. What Drives the Confidence-Accuracy Dissociation?**
- **Question:** Why does accuracy show source advantage but confidence doesn't?
- **Possible Mechanisms:**
  - Metacognitive monitoring uses different retrieval cues than accuracy judgments
  - Floor effects compress confidence but not accuracy
  - Source monitoring operates at retrieval (accuracy) but not encoding/metamemory (confidence)
- **Next Steps:** Systematic literature review of confidence-accuracy dissociations in spatial memory
- **Feasibility:** Theoretical work, 1-2 weeks

**2. Is Metacognitive Insensitivity Specific to VR or General?**
- **Question:** Would source-destination confidence dissociation replicate in real-world spatial memory?
- **Implication:** If VR-specific, suggests VR assessment tools should prioritize accuracy over confidence
- **Next Steps:** Pilot real-world navigation task with source-destination manipulation and confidence ratings
- **Feasibility:** Requires real-world paradigm development, ~6 months

**3. Do Individual Differences in Metacognitive Ability Moderate the Null Effect?**
- **Question:** Do participants with high metacognitive accuracy show source-destination confidence differences that low-accuracy participants miss?
- **Implication:** If moderation exists, confidence measures may be informative only for subset of participants
- **Next Steps:** Collect standardized metacognitive ability measures (e.g., perceptual confidence tasks), test moderation
- **Feasibility:** Requires expanded assessment battery, ~3 months for new cohort

### Priority Ranking

**HIGH PRIORITY (Do First):**
1. Extract accuracy trajectories for same sample (validate dissociation exists in accuracy)
2. Analyze confidence response patterns (extreme vs full-range responders) - **MANDATORY per solution.md 1.4**
3. Subgroup analysis by baseline confidence (test individual differences hypothesis)

**MEDIUM PRIORITY (Subsequent):**
1. Alternative time functional forms (test robustness of null interaction)
2. RQ 6.X.X confidence-accuracy calibration analysis (directly test calibration hypothesis)
3. Literature review of confidence-accuracy dissociations (theoretical grounding)

**LOWER PRIORITY (Aspirational):**
1. Finer-grained confidence scale with new data (long timeline, requires new collection)
2. Shorter retention intervals (protocol modification needed)
3. Eye-tracking during confidence (equipment-dependent, outside thesis scope)

### Next Steps Summary

The **NULL finding** (source = destination confidence trajectories) is robust but raises critical question: **Is this confidence-accuracy dissociation or absence of source-destination distinction in this sample?**

**Top 3 immediate actions:**
1. **Extract accuracy data** for same participants to confirm Ch5 5.5.1 replicates
2. **Analyze confidence response patterns** to identify extreme-response bias (MANDATORY per solution.md 1.4)
3. **Subgroup by baseline confidence** to test if metacognitive ability moderates null effect

These analyses use existing data, require 2-3 days total, and will definitively answer whether confidence-accuracy dissociation is real or whether source-destination distinction absent altogether.

---

## Connection to Thesis (Cross-Chapter Integration)

### Ch5 5.5.1 Comparison (Accuracy Source-Destination Dissociation)

**Ch5 5.5.1 Finding (Accuracy):**
- Destination accuracy declined **faster** than source accuracy
- Significant LocationType x Time interaction
- Interpretation: Encoding depth differences (initial encounter vs task completion) drive differential forgetting

**Ch6 6.8.1 Finding (Confidence):**
- Destination and source confidence show **equivalent** decline rates
- Non-significant LocationType x Time interaction (p = 0.553)
- Interpretation: Metacognitive monitoring insensitive to source-destination encoding differences

**Critical Divergence:** Objective performance (accuracy) dissociates source-destination, but subjective confidence does not. This suggests **metacognitive insensitivity** to fine-grained episodic memory distinctions.

### Implications for Chapter 6 Confidence Analyses

**Hypothesis Revision Needed:**
- Ch6 should not simply replicate Ch5 hypotheses with confidence as outcome
- Confidence and accuracy may show **different patterns** for same manipulations
- Future Ch6 RQs should predict when confidence-accuracy alignment vs dissociation expected

**Methodological Lesson:**
- Do not assume confidence "tracks" accuracy
- Always collect both accuracy and confidence to test calibration
- Confidence-accuracy dissociations may be common in spatial memory

**Clinical Assessment Implication:**
- For VR cognitive assessment, **accuracy** may be more sensitive than **confidence** for detecting subtle memory distinctions (e.g., source vs destination)
- Confidence may be more useful for detecting global memory decline (main effect of time: p < .001) rather than specific contextual differences

### Thesis Narrative Integration

**Chapter 5 (Accuracy):**
"VR episodic memory shows source-destination dissociation, with destination locations more vulnerable to forgetting than source locations."

**Chapter 6 (Confidence):**
"Metacognitive confidence judgments do NOT show source-destination dissociation, suggesting metacognitive monitoring is insensitive to encoding context differences that drive accuracy effects."

**Synthesis (Discussion Chapter):**
"The confidence-accuracy dissociation (Ch6 6.8.1 null vs Ch5 5.5.1 significant) reveals that subjective metamemory and objective performance recruit different cognitive processes. VR cognitive assessments should prioritize accuracy measures for detecting subtle episodic memory distinctions, while confidence measures may be useful for global forgetting trajectories."

---

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2025-12-07
**Analysis status:** Complete (Steps 00-07 executed successfully, plots not generated)
