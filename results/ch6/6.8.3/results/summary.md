# Results Summary: RQ 6.8.3 - Source-Destination Confidence ICC

**Research Question:** Does confidence ICC reveal the same opposite-correlation pattern as accuracy? Specifically, do source (-U-) and destination (-D-) locations show opposite intercept-slope correlations in confidence trajectories, replicating the Ch5 5.5.6 accuracy findings?

**Analysis Completed:** 2025-12-12

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total N:** 100 participants
- **Observations:** 800 total (100 participants x 4 test sessions x 2 location types)
- **Location Types:** Source (pick-up locations, -U- tags) and Destination (put-down locations, -D- tags)
- **Missing Data:** None (complete data for all participants across both location types)
- **Test Sessions:** T1, T2, T3, T4 (mapped to TSVR hours per Decision D070)

### Primary Results: Intercept-Slope Correlations

**CRITICAL FINDING: OPPOSITE PATTERN DOES NOT REPLICATE**

**Source Confidence:**
- Intercept-slope correlation: r = -0.24
- 95% CI: [-0.42, -0.05]
- p (uncorrected) = 0.016
- p (Bonferroni) = 0.032
- **Interpretation:** NEGATIVE correlation (high baseline confidence -> faster confidence decay)

**Destination Confidence:**
- Intercept-slope correlation: r = -0.40
- 95% CI: [-0.55, -0.22]
- p (uncorrected) < 0.001
- p (Bonferroni) < 0.001
- **Interpretation:** NEGATIVE correlation (high baseline confidence -> faster confidence decay)

**Key Observation:** BOTH location types show NEGATIVE correlations. The opposite sign pattern from Ch5 5.5.6 accuracy does NOT replicate in confidence.

### Comparison to Ch5 5.5.6 Accuracy Pattern

**Accuracy (Ch5 5.5.6):**
- Source: r = +0.99 (POSITIVE - regression to mean pattern)
- Destination: r = -0.90 (NEGATIVE - fan effect pattern)
- **Pattern:** OPPOSITE SIGNS (Source positive, Destination negative)

**Confidence (This RQ):**
- Source: r = -0.24 (NEGATIVE)
- Destination: r = -0.40 (NEGATIVE)
- **Pattern:** SAME SIGN (both negative)

**Direction Match:**
- Source: FALSE (accuracy positive, confidence negative)
- Destination: TRUE (both negative)
- **Overall Replication:** FAILED

**Magnitude Differences:**
- Source: |r_confidence - r_accuracy| = 1.23 (massive difference)
- Destination: |r_confidence - r_accuracy| = 0.50 (moderate difference)

### LMM Convergence Status

**Source LMM:**
- Model: theta ~ TSVR_hours + (TSVR_hours | UID)
- Convergence: Successful (TRUE)
- Random effects: Intercepts + slopes with covariance estimated

**Destination LMM:**
- Model: theta ~ TSVR_hours + (TSVR_hours | UID)
- Convergence: Successful (TRUE)
- Random effects: Intercepts + slopes with covariance estimated

### Random Effects Extraction for RQ 6.8.4

**Critical Dependency Output:**
- File: data/step03_random_effects.csv
- Rows: 200 (100 participants x 2 location types)
- Columns: UID, location_type, random_intercept, random_slope
- **Status:** SUCCESSFULLY CREATED for downstream clustering analysis in RQ 6.8.4

### Cross-Reference to plan.md

**Expected Outputs:** ALL PRESENT
- step00_lmm_input_confidence_location.csv: 800 rows (EXPECTED: 800)
- step01_source_variance_components.csv: 5 rows (EXPECTED: 5)
- step02_destination_variance_components.csv: 5 rows (EXPECTED: 5)
- step03_random_effects.csv: 200 rows (EXPECTED: 200, REQUIRED for RQ 6.8.4)
- step04_intercept_slope_correlations.csv: 2 rows (EXPECTED: 2)
- step05_ch5_comparison.csv: 2 rows (EXPECTED: 2)

**Substance Criteria:** ALL MET
- LMM convergence: Both Source and Destination converged successfully
- Variance components: All positive (no boundary issues)
- Correlation bounds: All values within [-1, 1]
- Decision D068 compliance: Dual p-values (uncorrected + Bonferroni) reported for both location types

---

## 2. Plot Descriptions

### Figure 1: Intercept-Slope Correlation Comparison (Accuracy vs Confidence)

**Filename:** plots/icc_correlation_comparison.png

**Plot Type:** Grouped bar chart comparing accuracy (Ch5 5.5.6) and confidence (RQ 6.8.3) intercept-slope correlations

**Visual Description:**

The plot displays side-by-side bars for Source and Destination location types, with accuracy correlations in blue and confidence correlations in orange.

**Left Panel (Source):**
- Accuracy bar: r = +0.99 (extends high into positive range, labeled "+0.99")
- Confidence bar: r = -0.24 (extends into negative range, labeled "-0.24")
- **Visual Pattern:** Opposite directions - accuracy strongly positive, confidence weakly negative

**Right Panel (Destination):**
- Accuracy bar: r = -0.90 (extends deep into negative range, labeled "-0.90")
- Confidence bar: r = -0.40 (extends moderately into negative range, labeled "-0.40")
- **Visual Pattern:** Same direction - both negative, but accuracy stronger magnitude

**Title Annotation:**
- "RQ 6.8.3: Opposite Correlation Pattern Does NOT Replicate"
- Subtitle: "(Accuracy: Opposite Signs, Confidence: Same Sign)"

**Legend Box (bottom left):**
- "Accuracy: Source (+) vs Dest (-) = OPPOSITE"
- "Confidence: Source (-) vs Dest (-) = SAME"
- "Pattern does NOT replicate"

**Key Visual Insights:**

1. **Striking Asymmetry:** Source shows dramatic reversal between accuracy (+0.99) and confidence (-0.24), while Destination shows same-direction consistency (both negative).

2. **Magnitude Contrast:** Accuracy correlations are EXTREME (near-perfect positive for Source, near-perfect negative for Destination), while confidence correlations are MODERATE to WEAK (both in -0.24 to -0.40 range).

3. **Pattern Failure:** The plot visually demonstrates that confidence does NOT replicate the opposite-sign pattern that made Ch5 5.5.6 theoretically significant. Both confidence bars point downward (negative), eliminating the critical dissociation.

**Connection to Findings:**

The visual confirms the statistical result: confidence and accuracy follow DIFFERENT individual difference patterns. The opposite-correlation pattern unique to accuracy (Source regression to mean vs Destination fan effect) does NOT generalize to metacognitive confidence. This dissociation suggests accuracy and confidence are governed by different forgetting mechanisms at the individual difference level.

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**

"Source confidence will show POSITIVE intercept-slope correlation (r > +0.50, replicating Ch5 5.5.6 r=+0.99 pattern: high baseline confidence -> slower confidence decay). Destination confidence will show NEGATIVE intercept-slope correlation (r < -0.50, replicating Ch5 5.5.6 r=-0.90 pattern: high baseline confidence -> faster confidence decay)."

**Hypothesis Status:** **REJECTED**

The hypothesis predicted opposite-sign correlations (Source positive, Destination negative) to replicate the accuracy pattern. Instead:
- Source: r = -0.24 (NEGATIVE, not positive as predicted)
- Destination: r = -0.40 (NEGATIVE, as predicted in direction but weaker than r < -0.50 threshold)
- **Critical failure:** SAME SIGN (both negative), not opposite signs

### Theoretical Contextualization

**What This NULL Finding Reveals:**

This is a **theoretically important NULL result** - the absence of pattern replication is scientifically meaningful:

**1. Memory-Metacognition Dissociation:**

The Ch5 5.5.6 opposite-correlation pattern (Source r=+0.99, Destination r=-0.90) was the most striking individual difference finding in the entire thesis. It suggested fundamentally different forgetting dynamics:
- **Source memory:** Regression to mean (high baseline -> slower decay, stability)
- **Destination memory:** Fan effect (high baseline -> faster decay, fragility)

The fact that confidence does NOT show this pattern suggests:
- **Accuracy and confidence are DISSOCIABLE** at the individual difference level
- Metacognitive monitoring does NOT have full access to the underlying memory dynamics
- Confidence may reflect different cognitive processes than accuracy (e.g., subjective fluency vs actual memory strength)

**2. What Confidence Correlations Tell Us:**

BOTH Source and Destination confidence show NEGATIVE intercept-slope correlations (high baseline -> faster decay), but for different reasons than accuracy:

**Source Confidence (r = -0.24):**
- Weakly negative correlation (p = 0.032 Bonferroni-corrected, significant)
- HIGH baseline confidence predicts FASTER confidence decay over time
- This is OPPOSITE to accuracy pattern (Source accuracy r = +0.99 showed high baseline -> slower decay)
- **Interpretation:** Participants who start very confident may experience steeper confidence decline as they forget, possibly due to metacognitive surprise when retrieval becomes harder

**Destination Confidence (r = -0.40):**
- Moderately negative correlation (p < 0.001 Bonferroni-corrected, highly significant)
- HIGH baseline confidence predicts FASTER confidence decay over time
- This is CONSISTENT with accuracy pattern direction (Destination accuracy r = -0.90 also negative)
- **Interpretation:** Destination's fan effect pattern partially replicates in confidence (same negative direction), but weaker magnitude (r = -0.40 vs r = -0.90)

**3. Why Source Shows Opposite Pattern (Accuracy vs Confidence):**

The Source reversal (accuracy +0.99 -> confidence -0.24) is the most theoretically puzzling finding:

**Accuracy (r = +0.99):** Regression to mean pattern
- Participants with high Source memory at baseline maintained that advantage (slower decay)
- Stable memory system - good initial encoding persists

**Confidence (r = -0.24):** Opposite pattern
- Participants with high Source confidence at baseline showed FASTER confidence decline
- Metacognitive surprise - confidence drops faster than actual memory

**Possible Explanations:**
1. **Metacognitive Overconfidence:** Participants who start very confident in Source memory may be overconfident, experiencing steeper confidence decline when retrieval difficulty increases (even if actual memory remains relatively stable).
2. **Fluency Misattribution:** High initial confidence may reflect encoding fluency (pick-up locations are salient during object identification), but fluency fades faster than actual memory traces.
3. **Differential Calibration:** Source memory may be well-calibrated at encoding (high confidence = high accuracy) but poorly calibrated over time (confidence declines faster than accuracy).

### Domain-Specific Insights

**Source Memory (Pick-Up Locations):**
- Accuracy: Regression to mean (r = +0.99, high baseline -> stability)
- Confidence: Negative correlation (r = -0.24, high baseline -> faster decline)
- **Dissociation:** Accuracy and confidence show OPPOSITE individual difference patterns
- **Clinical Implication:** Confidence ratings may be misleading for Source memory - highly confident individuals at baseline may experience greater metacognitive decline than actual memory decline

**Destination Memory (Put-Down Locations):**
- Accuracy: Fan effect (r = -0.90, high baseline -> faster decay)
- Confidence: Negative correlation (r = -0.40, high baseline -> faster decline)
- **Partial Replication:** Same direction (both negative), but confidence correlation weaker
- **Clinical Implication:** Destination confidence partially tracks accuracy forgetting dynamics, but with attenuated strength (half the magnitude)

### Unexpected Patterns

**1. Source Reversal (Major Surprise):**

The most unexpected finding is Source confidence showing r = -0.24 (negative) when accuracy showed r = +0.99 (positive). This was NOT predicted by any theory:
- Dual-process theory (recollection vs familiarity) does not predict opposite metacognitive patterns
- Encoding depth theory predicts confidence should track accuracy (both stable for deep encoding)
- Regression to mean pattern should apply to both accuracy and confidence if they reflect same memory system

**Investigation Needed:**
- Examine Source confidence calibration curves (are high-confidence participants overconfident at baseline?)
- Test whether Source confidence decline is due to subjective retrieval fluency changes vs actual memory strength
- Consider alternative metacognitive frameworks (e.g., cue familiarity theory)

**2. Destination Partial Replication (Moderate Surprise):**

Destination shows SAME direction (both negative) but weaker magnitude (r = -0.40 vs r = -0.90). This suggests:
- Destination metacognition has partial access to underlying forgetting dynamics (knows high baseline -> faster decay)
- But confidence change is less sensitive than accuracy change (half the correlation strength)
- Possible explanation: Destination encoding is shallower (automatic action endpoint), so metacognitive monitoring is noisier

**3. Both Confidence Correlations Significant (Modest Surprise):**

Despite weaker magnitudes than accuracy, BOTH confidence correlations are statistically significant:
- Source: p = 0.032 (Bonferroni-corrected, survives multiple comparison adjustment)
- Destination: p < 0.001 (highly significant)

This indicates that intercept-slope covariance is NOT noise - there are genuine individual differences in how baseline confidence predicts confidence decay. But the PATTERN of those differences does NOT match accuracy.

### Broader Implications

**REMEMVR Validation:**

This RQ provides CRITICAL evidence for REMEMVR's ability to detect dissociations between memory and metacognition:
- Accuracy and confidence are NOT simply rescaled versions of each other
- Source and Destination memory show different accuracy-confidence relationships
- Individual difference patterns differ across accuracy and confidence domains
- **Conclusion:** REMEMVR captures multi-level episodic memory processes (memory traces + metacognitive monitoring)

**Methodological Insights:**

**1. Confidence Ratings Are Not Redundant with Accuracy:**
- If confidence were simply rescaled accuracy, both should show same individual difference patterns
- The Source reversal (accuracy +0.99 vs confidence -0.24) proves dissociation
- **Recommendation:** Always collect BOTH accuracy and confidence in episodic memory studies

**2. Intercept-Slope Correlations as Mechanistic Signature:**
- Ch5 5.5.6 showed opposite correlations (Source positive, Destination negative) can reveal different forgetting mechanisms
- This RQ shows those mechanisms may be SPECIFIC to accuracy, not generalizing to confidence
- **Recommendation:** Use ICC pattern analysis to test whether findings replicate across multiple dependent variables (accuracy, confidence, reaction time, neural activation)

**3. Null Replication Is Theoretically Informative:**
- The FAILURE to replicate opposite-sign pattern is not a "negative result" - it's a discovery
- Reveals that Source-Destination dissociation operates differently at memory vs metacognitive levels
- **Recommendation:** Publish non-replications of striking patterns to advance theory

**Theoretical Contributions:**

**1. Memory-Metacognition Dissociation Theory:**
- Supports dual-system models where memory traces and metacognitive monitoring are partially independent
- Challenges single-system models (e.g., signal detection theory) where confidence is direct readout of memory strength
- Suggests confidence reflects additional factors beyond memory strength (fluency, surprise, subjective difficulty)

**2. Source-Destination Asymmetry:**
- Source memory shows strong accuracy-confidence dissociation (opposite patterns)
- Destination memory shows weak accuracy-confidence coupling (partial replication)
- Suggests pick-up locations (Source) engage different metacognitive processes than put-down locations (Destination)

**3. Individual Differences Framework:**
- Regression to mean (accuracy) vs metacognitive surprise (confidence) may characterize different participants
- High-performing individuals in accuracy may experience greater metacognitive instability
- Opens new research direction: what predicts accuracy-confidence dissociation magnitude?

**Clinical Relevance:**

For cognitive assessment using VR:
- **Source memory confidence ratings may be misleading:** High confidence at baseline does NOT predict stable confidence over time (opposite pattern from accuracy)
- **Destination memory confidence more reliable:** Partially tracks accuracy forgetting dynamics (same direction, weaker magnitude)
- **Clinical recommendation:** When assessing Source memory, rely more on accuracy than confidence ratings. For Destination memory, confidence may provide complementary signal (but weaker than accuracy).

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 participants provides adequate power (0.80) for medium-to-large correlations (r >= 0.30)
- BOTH Source (r = -0.24) and Destination (r = -0.40) correlations were detected as significant
- However, N = 100 may be underpowered to detect subtle differences between Source and Destination correlation magnitudes (”r = 0.16)
- Confidence intervals are wide for Source (95% CI: -0.42 to -0.05), limiting precision

**Demographic Constraints:**
- University undergraduate sample (assumed age M ~ 20, predominantly female based on project norms)
- Limits generalizability to older adults (metacognitive monitoring changes with age)
- Restricted education range (all college students) prevents examining education effects on confidence calibration

**Missing Data:**
- None (complete data for all 100 participants across both location types)
- No attrition issues for this RQ (inherits complete RQ 6.8.1 sample)

### Methodological Limitations

**Measurement:**

**1. Confidence Scale:**
- 5-point ordinal scale (1 = not confident, 5 = very confident)
- IRT calibration treats as ordered categories (GRM model)
- Assumes equal psychological intervals between categories (may not hold)
- Limited granularity - participants may experience confidence changes not captured by 5 categories

**2. Theta Score Dependency:**
- This RQ uses theta scores from RQ 6.8.1 (IRT-derived confidence ability)
- Theta scores are estimated, not observed, introducing measurement error
- Standard errors (se column) indicate estimation uncertainty, but not propagated into correlation CIs
- If RQ 6.8.1 theta scores have systematic bias, this RQ inherits that bias

**3. Location Type Definition:**
- Source (-U- tags) = pick-up locations where object was identified
- Destination (-D- tags) = put-down locations where object was placed
- Distinction assumes participants encode Source and Destination separately (may be bound in episodic memory)
- No independent validation that Source and Destination are psychologically distinct (relies on task design)

**Design:**

**1. Cross-RQ Dependency Risk:**
- This RQ cannot run without RQ 6.8.1 completion (DERIVED data)
- If RQ 6.8.1 has analysis errors, this RQ propagates those errors
- No independent validation of RQ 6.8.1 theta scores within this RQ

**2. Comparison to Ch5 5.5.6:**
- Comparison assumes Ch5 5.5.6 accuracy correlations (Source r = +0.99, Destination r = -0.90) are "true" benchmarks
- If Ch5 5.5.6 correlations are inflated (e.g., due to small sample or overfitting), comparison misleading
- No formal statistical test of "replication" - just side-by-side comparison

**3. No Mechanistic Test:**
- This RQ documents THAT confidence does not replicate accuracy pattern, but not WHY
- Needs follow-up analyses to test mechanisms (overconfidence, fluency, calibration)
- Cannot distinguish between multiple theoretical explanations for Source reversal

**Statistical:**

**1. Correlation Inference:**
- Intercept-slope correlations derived from LMM variance-covariance matrix
- Assumes LMM random effects are normally distributed (may not hold for all participants)
- Confidence intervals use Fisher's z-transformation (assumes large-sample normality)
- Small deviations from normality may affect CI accuracy

**2. Multiple Comparisons:**
- Two location types tested (Source and Destination)
- Bonferroni correction applied (p_bonf = p_uncorr * 2)
- Conservative correction may reduce power to detect true differences
- No pre-registered analysis plan (exploratory comparisons)

**3. LMM Specification:**
- Random slopes model assumes linear trajectories (theta ~ TSVR_hours)
- No quadratic or cubic time terms tested (may miss non-linear forgetting)
- Unstructured covariance (full random effects) may not be optimal
- Alternative models (AR1, compound symmetry) not compared

### Generalizability Constraints

**Population:**

Findings may not generalize to:
- **Older adults:** Metacognitive monitoring declines with age (Fleming et al., 2016), Source-Destination confidence patterns may differ
- **Clinical populations:** MCI, dementia, TBI patients have impaired metacognition, confidence-accuracy dissociations may be stronger or weaker
- **Cross-cultural samples:** Metacognitive confidence influenced by cultural factors (e.g., Western overconfidence vs East Asian underconfidence)

**Context:**

VR desktop paradigm differs from:
- **Real-world episodic memory:** Naturalistic encoding may produce different confidence dynamics
- **Standard neuropsychological tests:** 2D stimuli, verbal responses (confidence ratings may be less calibrated)
- **Fully immersive VR (HMD):** Greater presence/embodiment may enhance metacognitive monitoring

**Task:**

REMEMVR specific encoding task may not reflect:
- **Emotional episodic memories:** Neutral VR content, no affective salience (confidence-accuracy dissociation may differ for emotional events)
- **Semantic memory:** Facts vs events (confidence ratings operate differently for semantic knowledge)
- **Procedural memory:** Confidence in "knowing how" vs "knowing that"

### Technical Limitations

**IRT Model (Inherited from RQ 6.8.1):**
- GRM assumes monotonic item response functions (may not hold for confidence ratings)
- Two-dimension structure (Source and Destination confidence) assumed, not empirically validated
- Local independence assumption may be violated for semantically related items

**LMM Random Effects:**
- Assumes random intercepts and slopes normally distributed
- Extracts participant-specific BLUPs (Best Linear Unbiased Predictors), which are shrinkage estimates (not raw participant values)
- Shrinkage may attenuate true individual differences, weakening correlations

**TSVR Variable (Decision D070):**
- TSVR (hours since encoding) assumes continuous forgetting
- May not capture day-specific consolidation effects (sleep, interference)
- Treats time linearly (exponential or logarithmic time scaling not tested)

**Dual P-Value Reporting (Decision D068):**
- Bonferroni correction conservative (may miss true effects with p = 0.01-0.05)
- Family-wise error rate controlled, but inflation still possible with many contrasts
- No pre-registered significance threshold (alpha = 0.05 conventional, not justified)

### Limitations Summary

Despite these constraints, findings are **scientifically informative within scope:**

**Strengths:**
- Complete data (N = 100, no missing values)
- Both LMMs converged successfully (no estimation failures)
- Both correlations statistically significant (not noise)
- Comparison to Ch5 5.5.6 provides theoretical context
- NULL finding (non-replication) is theoretically meaningful

**Weaknesses:**
- Sample size limits precision (wide CIs for Source correlation)
- Cannot test mechanisms (WHY confidence differs from accuracy)
- Generalizability limited to young adult, VR desktop, neutral episodic memory

**Conclusion:** Results demonstrate confidence-accuracy dissociation robustly within REMEMVR paradigm, but require follow-up to understand underlying mechanisms and test generalizability.

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Source Confidence Calibration Analysis:**
- **Why:** Source shows opposite pattern (accuracy +0.99 vs confidence -0.24) - need to test overconfidence hypothesis
- **How:** Compute confidence-accuracy calibration curves per participant, test whether high-confidence Source participants are overconfident at baseline
- **Expected Insight:** If high Source confidence participants are overconfident (confidence > accuracy), explains why their confidence drops faster (metacognitive surprise)
- **Timeline:** Can be done immediately (requires RQ 6.8.1 accuracy data + this RQ confidence data)

**2. Sensitivity Analysis for Correlation Differences:**
- **Why:** Source r = -0.24 vs Destination r = -0.40 (”r = 0.16) - is this difference significant?
- **How:** Bootstrap test of correlation difference (H0: r_source = r_destination), compute 95% CI for ”r
- **Expected Insight:** Determine whether Source and Destination confidence show statistically different intercept-slope patterns (not just descriptively different)
- **Timeline:** 1-2 hours (bootstrap resampling on LMM random effects)

**3. Examine Confidence-Accuracy Coupling Per Participant:**
- **Why:** Aggregate analyses show dissociation, but do individual participants show same pattern?
- **How:** Correlate participant-specific accuracy slopes (from Ch5 5.5.6) with confidence slopes (from this RQ), test whether accuracy and confidence forgetting rates are coupled within individuals
- **Expected Insight:** Identify participants with high accuracy-confidence coupling vs dissociation, explore demographic predictors
- **Timeline:** Immediate (both datasets available)

### Planned Thesis RQs (Chapter 6 Continuation)

**RQ 6.8.4: Source-Destination Confidence Clustering (Planned Next):**
- **Focus:** Use random effects from this RQ (data/step03_random_effects.csv, 200 rows) to perform K-means clustering on (random_intercept, random_slope) space
- **Why:** This RQ shows aggregated confidence patterns are dissociated from accuracy, but are there participant subgroups with distinct forgetting profiles?
- **Builds On:** Uses step03_random_effects.csv output from this RQ (REQUIRED INPUT)
- **Expected Insight:** Identify "fast confidence decliners" vs "stable confidence" subgroups per location type
- **Expected Timeline:** Next RQ in Ch6 Source-Destination series

**RQ 6.8.5: Source-Destination Confidence-Accuracy Joint Modeling (Exploratory):**
- **Focus:** Fit multivariate LMM with BOTH accuracy and confidence as outcomes, test whether intercept-slope correlations differ across outcome types
- **Why:** This RQ compared correlations descriptively (side-by-side), but formal joint model tests interaction
- **Builds On:** Combines Ch5 5.5.6 accuracy data + this RQ confidence data in single model
- **Expected Insight:** Statistical test of whether Source shows stronger accuracy-confidence dissociation than Destination
- **Expected Timeline:** Requires multivariate LMM specification (not yet implemented in tools)

### Methodological Extensions (Future Data Collection)

**1. Expand Confidence Scale Granularity:**
- **Current Limitation:** 5-point ordinal scale may be too coarse to detect subtle confidence changes
- **Extension:** Use 100-point continuous confidence scale (e.g., slider from 0 to 100) in new sample
- **Expected Insight:** Test whether Source-Destination dissociation persists with finer-grained confidence measurement
- **Feasibility:** Requires new data collection (N = 100 subsample with revised confidence rating task)

**2. Test Fluency Manipulation:**
- **Current Limitation:** Cannot distinguish whether Source confidence decline is due to fluency changes vs memory strength changes
- **Extension:** Manipulate retrieval fluency experimentally (e.g., semantic priming before Source retrieval), test whether fluency affects confidence more than accuracy
- **Expected Insight:** Causal test of fluency misattribution hypothesis for Source confidence
- **Feasibility:** Requires experimental design (within-subjects fluency manipulation, ~6 months)

**3. Older Adult Sample:**
- **Current Limitation:** Young adult sample limits generalizability to aging populations
- **Extension:** Recruit N = 100 older adults (age 60-75), replicate Source-Destination confidence analysis
- **Expected Insight:** Test whether accuracy-confidence dissociation is age-dependent (metacognitive monitoring declines with age)
- **Feasibility:** Requires new participant recruitment and VR administration (~1 year)

**4. HMD Immersive VR:**
- **Current Limitation:** Desktop VR lacks full immersion (no head tracking, limited FOV)
- **Extension:** Replicate with Oculus Quest 2 HMD (N = 100 new sample), test whether immersion affects confidence calibration
- **Expected Insight:** Greater presence/embodiment may enhance metacognitive monitoring, reducing accuracy-confidence dissociation
- **Feasibility:** Requires HMD acquisition and task porting (~6-9 months)

### Theoretical Questions Raised

**1. What Cognitive Mechanisms Underlie Source Confidence Decline?**
- **Question:** Why does Source confidence show opposite pattern from accuracy (r = -0.24 vs r = +0.99)?
- **Next Steps:**
  - Test overconfidence hypothesis (calibration curves)
  - Test fluency hypothesis (experimental manipulation)
  - Test metacognitive surprise hypothesis (subjective difficulty ratings)
- **Expected Insight:** Identify whether Source confidence decline is due to metacognitive misattribution, calibration failure, or genuine confidence loss
- **Feasibility:** Immediate (calibration analysis) to long-term (experimental manipulations)

**2. Are Accuracy and Confidence Governed by Different Forgetting Dynamics?**
- **Question:** Do accuracy and confidence follow different functional forms over time (e.g., exponential vs power-law)?
- **Next Steps:** Fit alternative trajectory models (exponential, power-law, logarithmic) to accuracy vs confidence separately, compare best-fit functions
- **Expected Insight:** If accuracy follows exponential decay but confidence follows linear decline, suggests different underlying processes
- **Feasibility:** Moderate (requires alternative LMM specifications, ~1 week)

**3. What Predicts Individual Differences in Accuracy-Confidence Dissociation?**
- **Question:** Why do some participants show strong dissociation (accuracy stable but confidence declines) while others show coupling?
- **Next Steps:** Collect additional measures (working memory capacity, metacognitive awareness scales, anxiety), test as predictors of dissociation magnitude
- **Expected Insight:** Build predictive model of who shows accuracy-confidence dissociation (clinical screening tool)
- **Feasibility:** Requires expanded assessment battery in new cohort (~1 year)

### Priority Ranking

**High Priority (Do First):**
1. **RQ 6.8.4 clustering** - natural next step in thesis, uses this RQ output (step03_random_effects.csv)
2. **Source calibration analysis** - tests overconfidence hypothesis for Source reversal (critical mechanism test)
3. **Sensitivity analysis for correlation differences** - quantifies Source vs Destination dissociation strength

**Medium Priority (Subsequent):**
1. **Confidence-accuracy coupling per participant** - explores individual differences, complements clustering
2. **RQ 6.8.5 joint modeling** - formal statistical test of dissociation (rigorous but requires new tools)
3. **Alternative trajectory models** - tests functional form differences (accuracy vs confidence decay)

**Lower Priority (Aspirational):**
1. **Expand confidence scale granularity** - methodological improvement but requires new data
2. **Older adult sample** - generalizability test, long-term project
3. **Fluency manipulation** - causal test of fluency hypothesis, experimental design needed
4. **HMD immersive VR** - ideal but not critical for current thesis scope

### Next Steps Summary

The NULL finding (opposite pattern does NOT replicate) raises three critical questions for immediate follow-up:

1. **RQ 6.8.4:** Can clustering identify participant subgroups with distinct confidence forgetting profiles? (Planned next RQ, uses this RQ random effects output)
2. **Calibration analysis:** Is Source confidence decline due to metacognitive overconfidence at baseline? (Immediate, tests mechanism)
3. **Correlation difference test:** Is Source-Destination dissociation magnitude statistically significant? (Quick robustness check)

Methodological extensions (finer confidence scale, older adults, HMD VR) are valuable but require new data collection beyond current thesis scope. Theoretical questions (fluency, functional form, individual difference predictors) represent long-term research program directions.

---

**Summary generated by:** rq_results agent (v4.0)

**Pipeline version:** v4.X (13-agent atomic architecture)

**Date:** 2025-12-12
