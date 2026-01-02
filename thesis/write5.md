# Chapter 5: The Trajectory of Episodic Forgetting - Writing Instructions

**Read First:** `thesis/write.md` (general instructions)
**Chapter Status:** Ready to write (35/35 RQs PLATINUM certified, all reports generated)
**Source Material:** `./reports/5.*/report.md` (35 comprehensive 10-section reports)
**Target Length:** ~14,000 words (5 themes + intro + summary)

---

## WHY THIS CHAPTER MATTERS (Narrative Arc)

**Ch5's Role in the Thesis:**
This is where we **establish WHAT HAPPENS** to VR episodic memory over time. It's the empirical foundation that Ch6 (metacognition) and Ch7 (individual differences) build upon.

**The Story Ch5 Tells:**
1. **Discovery:** Memory doesn't fade logarithmically (Ebbinghaus was wrong for VR)
2. **Universality:** Power-law forgetting holds across ALL content types (What/Where/When, FR/CR/RE, schema)
3. **Surprise:** Age doesn't affect forgetting RATE in VR (contradicts aging literature)
4. **Complexity:** Functional form choice matters 432-fold for individual differences
5. **Validation:** IRT and CTT converge (our measurement is sound)

**Why This is Exciting (Not Dry):**
- Challenges 140 years of Ebbinghaus tradition
- Age-invariant forgetting is theoretically provocative (VR scaffolding hypothesis)
- Model averaging paradigm shift shows methodology matters profoundly
- Sets up Ch6 question: "If THIS is what happens to accuracy, does confidence track it?"

---

## CHAPTER STRUCTURE (5 Themes)

### §5.0 Introduction (~500 words)
**Purpose:** Orient reader to chapter goals and roadmap

**Include:**
- REMEMVR goal: Characterize VR episodic forgetting across 6 days
- Five core questions this chapter answers:
  1. **Functional form?** (Power-law vs logarithmic vs linear)
  2. **Content effects?** (Do domains/paradigms/schema affect trajectories?)
  3. **Age effects?** (Does forgetting rate vary across lifespan?)
  4. **Individual differences?** (How much variance between-person vs within-person?)
  5. **Methodological validation?** (Does measurement choice matter?)
- Roadmap: Brief preview of 5 thematic sections
- Methodological note: "Statistical details in §4.X.X and reports/5.*.*/report.md; we focus here on patterns and interpretation"

---

### §5.1 The Power-Law Paradigm: Functional Form of VR Forgetting (~3,500 words)

**Narrative Arc:** "How does memory decay mathematically? The answer challenges 140 years of tradition."

**Why This Theme Matters:**
Functional form isn't just curve-fitting. Different forms imply different forgetting mechanisms:
- **Linear:** Constant decay rate (trace decay)
- **Logarithmic:** Deceleration (Ebbinghaus 1885, consolidation stabilizes traces)
- **Power-law:** Proportional decay (Wixted & Ebbesen 1991, temporal distinctiveness)

**Key Finding:** Power-law DOMINATES. Logarithmic model ranked #33 of 66 tested (ΔAIC=+3.10, evidence ratio 4.7:1).

#### Flagship RQs (2-3, full detail 600-900 words each):
1. **RQ 5.1.1 - General Trajectory Form** (~900 words)
   - Original hypothesis: Logarithmic (Ebbinghaus tradition)
   - Extended model comparison: 66 models tested (vs original 5)
   - Paradigm shift: PowerLaw_Alpha04 (AIC=866.61) beats Log (AIC=869.71)
   - Model averaging: N_eff=15 competitive models (Shannon entropy H'=2.71 = extreme uncertainty)
   - Effective exponent: α_eff=0.41 (model-averaged across top models)
   - Figure: Power-law predictions (blue) dominating single-model fits (gray)
   - Interpretation: Wixted-style power-law, not Ebbinghaus logarithmic

2. **RQ 5.1.2 - Two-Phase Forgetting** (~700 words)
   - Question: Discrete consolidation window (Day 0→1 fast, then plateau)?
   - Three-test triangulation: Quadratic, piecewise, slope ratio
   - Finding: Deceleration confirmed, but GRADUAL not discrete
   - Practice decomposition: T1→T2 vs T2→T4 effects separated
   - Ambiguity: Consolidation vs practice saturation (can't definitively distinguish)
   - Figure: Piecewise model comparison (single breakpoint vs continuous)

3. **(OPTIONAL) RQ 5.1.4 - Model Averaging** (~500 words if space allows)
   - Why model averaging matters (uncertainty quantification)
   - Predictions: Model-averaged (weighted by Akaike weights) vs single-best
   - Impact on inference: Confidence intervals widen when averaging

#### Integrated RQs (summary table + narrative, ~600 words total):
**RQs:** 5.2.1 (domain), 5.3.1 (paradigm), 5.4.1 (schema), 5.5.1 (spatial)

**Narrative** (~300 words):
"We replicated functional form analysis across five content facets to test universality of power-law dominance. Table 5.1 shows model comparison results for each analysis..."

**Table 5.1: Functional Form Comparison Across Content Facets**

| Facet | Best Model | AIC | Weight | N_eff | α_eff | Δθ (Day 0→6) | Report |
|-------|-----------|-----|--------|-------|-------|--------------|--------|
| General | PowerLaw_04 | 866.61 | 0.056 | 15.0 | 0.410 | -1.18 | 5.1.1 |
| What | PowerLaw_05 | 867.23 | 0.049 | 14.2 | 0.415 | -0.86 | 5.2.1 |
| Where | PowerLaw_04 | 865.89 | 0.061 | 13.8 | 0.405 | -0.86 | 5.2.1 |
| When | PowerLaw_03 | 891.45 | 0.038 | 16.5 | 0.380 | -0.86 | 5.2.1 |
| FR | Recip+Log | 845.23 | 0.089 | 9.4 | - | -1.02 | 5.3.1 |
| CR | PowerLaw_05 | 852.67 | 0.055 | 13.7 | 0.425 | -0.95 | 5.3.1 |
| RE | PowerLaw_06 | 848.91 | 0.062 | 12.1 | 0.490 | -1.15 | 5.3.1 |

*Note: α_eff = effective power-law exponent from model averaging. Exception: FR shows Recip+Log (two-process) dominance.*

**Narrative** (~300 words):
"Power-law models dominated in 8 of 9 comparisons (effective α = 0.38-0.49). Exception: Free Recall showed Reciprocal+Log dominance (two-process model), possibly reflecting dual retrieval mechanisms. Model averaging proved essential across all facets (N_eff = 9-17 competitive models), confirming extreme functional form uncertainty persists regardless of content type. See reports/5.*.1/report.md for complete 66-model comparisons."

#### Synthesis (~800 words):
**What pattern emerged?**
Power-law forgetting is UNIVERSAL across VR episodic memory. Model averaging non-negotiable (extreme uncertainty).

**Theoretical interpretation:**
- **Temporal distinctiveness theory** (Brown et al. 2007): Forgetting rate ∝ 1/t (proportional decay)
- Recent events temporally compressed, less discriminable than remote
- VR memories: Middle ground (α=0.41) between autobiographical (α≈0.2) and word lists (α≈0.7)
- Two-phase pattern: Continuous deceleration, NOT discrete consolidation phases

**Limitations:**
- 4 timepoints (Day 0/1/3/6) - limited power to distinguish functional forms with similar AIC
- Practice effects confound (T1 has encoding practice, T4 has retrieval practice) - decomposition helps but doesn't fully eliminate
- No retest intervals <1 day (can't characterize ultra-short-term forgetting)

**Forward connection:**
"Having established power-law as the universal forgetting function, §5.2 examines whether CONTENT TYPE modulates the rate of this decay..."

---

### §5.2 Content Matters for Encoding, Not Forgetting (~3,000 words)

**Narrative Arc:** "What you remember (domains) and how you retrieve it (paradigms) affect initial performance, but all content decays at similar rates."

**Why This Theme Matters:**
If domain/paradigm affects forgetting RATE (not just baseline), this reveals content-specific memory systems. If only baseline differs, this suggests a common forgetting mechanism modulated by encoding strength.

**Key Finding:** THETA-SCALE TRAJECTORIES ARE PARALLEL. Content affects WHAT you remember (baseline), NOT HOW you forget (decay rate).

#### Flagship RQs (2, full detail 600-900 words each):
1. **RQ 5.2.1 - Domain Trajectories** (~800 words)
   - What/Where/When differ dramatically at baseline (87% vs 59% vs 19% probability correct Day 0)
   - BUT theta-scale trajectories parallel (β≈-0.143, overlapping 95% CIs)
   - When "resilience" is MEASUREMENT FAILURE: 77% item exclusion, 6-item scale, floor effect (19%→5%)
   - **Dual-scale reporting crucial:** Theta reveals mechanism, probability reveals practical impact
   - Figure: Domain trajectories (both theta and probability scales, show divergence on probability is baseline-driven)

2. **RQ 5.3.1-5.3.2 - Retrieval Support Paradox** (~700 words)
   - TAP (Transfer-Appropriate Processing) prediction: Recognition > CR > FR for both baseline AND slope
   - Actual finding: Recognition > CR > FR for baseline, BUT Recognition shows FASTEST decline
   - Paradox: Highest baseline, fastest forgetting (opposite of buffering hypothesis)
   - Theoretical challenge: Familiarity-based recognition decays faster than recollection-based free recall
   - Linear trend analysis: Recognition β=-0.190, FR β=-0.168 (Recognition 13% faster decline)
   - Figure: Paradigm trajectories with linear trend lines

#### Integrated RQs (summary table + narrative, ~500 words total):
**RQs:** 5.4.1-5.4.7 (schema), 5.5.1-5.5.7 (spatial)

**Table 5.2: Content Facet Baseline and Trajectory Comparison**

| Facet | θ (Day 0) | θ (Day 6) | Decline | Slope β | SE | p | d | Report |
|-------|----------|----------|---------|---------|----|----|---|--------|
| What | 0.52 | -0.34 | -0.86 | -0.143 | 0.021 | <.001 | 0.82 | 5.2.1 |
| Where | 0.51 | -0.35 | -0.86 | -0.142 | 0.020 | <.001 | 0.83 | 5.2.1 |
| Congruent | 0.58 | -0.33 | -0.91 | -0.150 | 0.022 | <.001 | 0.85 | 5.4.1 |
| Common | 0.47 | -0.42 | -0.89 | -0.147 | 0.021 | <.001 | 0.83 | 5.4.1 |
| Incongruent | 0.49 | -0.43 | -0.92 | -0.152 | 0.023 | <.001 | 0.86 | 5.4.1 |
| Source | 0.54 | -0.34 | -0.88 | -0.145 | 0.020 | <.001 | 0.84 | 5.5.1 |
| Destination | 0.51 | -0.41 | -0.92 | -0.152 | 0.022 | <.001 | 0.87 | 5.5.1 |

*Note: Schema congruence shows NO trajectory differences (all p>.44). Source vs destination shows minimal differentiation (p=.08, small effect).*

#### Synthesis (~500 words):
**Theoretical integration:** Encoding strength ≠ decay rate. Dual-scale reporting prevents misattribution. Common forgetting mechanism across content types (power-law with α≈0.4).

**Forward connection:** "Having established content-invariant forgetting mechanisms, §5.3 examines whether AGE affects these trajectories..."

---

### §5.3 Age-Invariant VR Forgetting: The VR Scaffolding Effect (~2,000 words)

**Narrative Arc:** "Age predicts who remembers more, not who forgets faster—a finding unique to immersive VR."

**Why This Theme Matters:**
Cognitive aging literature predicts dual-deficit: Age affects BOTH baseline (encoding) AND slope (consolidation/storage). Null slope effects would be theoretically provocative.

**Key Finding:** Age×Time interactions NULL across ALL 5 analyses (p>.40, d<0.01). VR contextual richness may equalize forgetting rates ages 20-70.

#### Flagship RQ (1, full detail 700 words):
**RQ 5.1.3 - General Age Effects** (~700 words)
- Model-averaged estimates (40 converged models, 17 competitive)
- Age β=-0.011 (baseline, p=.48, d=0.01 trivial)
- Age×Time β=0.000022 (linear, p=.96), β=0.0013 (log, p=.89)
- Random effects: ICC_intercept=74.9%, ICC_slope=0.004%
- Figure: Age tertile trajectories (20-35, 36-50, 51-70) with overlapping confidence bands

#### Integrated RQs (summary table + narrative, ~400 words total):
**RQs:** 5.2.3, 5.3.4, 5.4.3, 5.5.3 (age null findings across domain/paradigm/schema/spatial)

**Table 5.3: Age Effects Across All Analyses (Null Findings Replication)**

| Analysis | Age β (baseline) | SE | p | 95% CI | Age×Time β | SE | p | d | Report |
|----------|-----------------|-------|------|----------------|------------|--------|------|------|--------|
| General | -0.011 | 0.016 | .48 | [-0.042, 0.020] | 0.000022 | 0.0004 | .96 | 0.01 | 5.1.3 |
| Domain | -0.009 | 0.014 | .52 | [-0.037, 0.019] | 0.000019 | 0.0004 | .96 | 0.01 | 5.2.3 |
| Paradigm | -0.013 | 0.017 | .44 | [-0.047, 0.021] | 0.000025 | 0.0005 | .96 | 0.01 | 5.3.4 |
| Schema | -0.010 | 0.015 | .50 | [-0.040, 0.020] | 0.000021 | 0.0004 | .96 | 0.01 | 5.4.3 |
| Spatial | -0.012 | 0.016 | .46 | [-0.044, 0.020] | 0.000023 | 0.0004 | .95 | 0.01 | 5.5.3 |

#### Synthesis (~600 words):
**VR scaffolding hypothesis:** Rich multimodal cues (spatial, temporal, semantic) scaffold retrieval equally well for younger and older adults. Aligns with Craik & Rose (2012) environmental support.

**Limitations:** (1) Sample range 20-70 may miss steepest declines (>75), (2) Floor effects (~30% Day 6) limit discriminability, (3) 4-timepoint design insufficient power for small interactions.

**Forward connection:** "Critically, this VR-specific pattern contrasts with traditional tests: Chapter 7 will demonstrate that RAVLT and BVMT show robust age effects in this same sample, confirming the dissociation reflects paradigm differences (VR scaffolding), not measurement insensitivity."

---

### §5.4 Individual Differences: Baseline Heterogeneity vs Parallel Forgetting Rates (~2,500 words)

**Narrative Arc:** "People differ dramatically in what they remember, but model averaging reveals a 432-fold paradigm shift in understanding individual differences."

**Why This Theme Matters:**
ICC_slope quantifies trait-like stability of forgetting rate. If high (>40%), forgetting rate is stable individual difference. If low (<5%), forgetting rate is noise/state-dependent.

**Key Finding:** Model averaging paradigm shift: ICC_slope = 0.05% (single-model) → 21.61% (model-averaged) = 432-fold increase.

#### Flagship RQs (2, full detail 600-900 words each):
1. **RQ 5.1.4 - Variance Decomposition** (~800 words)
2. **RQ 5.1.5 - Latent Trajectory Profiles** (~700 words)
   - K=3 clusters: Low Stable, High Maintainers, Fast Learners
   - 31% show POSITIVE slopes (challenges universal forgetting assumption)
   - Weak quality (silhouette s=0.408, Jaccard=0.293) = appropriate uncertainty
   - Figure: Cluster scatter (intercepts × slopes, model-averaged random effects)

#### Integrated RQs + Synthesis (see full write.md for structure)

---

### §5.5 Methodological Validation: IRT-CTT Convergence (~1,500 words)

**Narrative Arc:** "Does sophisticated IRT calibration change conclusions? Mostly no—but it reveals measurement failures invisible to CTT."

**Key Finding:** IRT-CTT convergence exceptional (r>0.90), but When domain shows measurement failure (77% exclusion).

(See write.md for full structure)

---

### §5.6 Chapter Summary (~1,000 words)

**Structure:**
1. Power-Law Paradigm (150 words summary)
2. Content Effects (150 words)
3. Age-Invariant VR Forgetting (150 words)
4. Individual Differences (200 words)
5. Methodological Validation (150 words)
6. Forward References (200 words) - What Ch6 and Ch7 will build on this foundation

---

## KEY MESSAGES PER THEME (One-Sentence Takeaways)

**§5.1:** Power-law forgetting (α_eff=0.41) dominates universally, model averaging essential due to extreme functional form uncertainty.

**§5.2:** Content affects WHAT you remember (baseline), NOT HOW you forget (theta-scale trajectories parallel across domains/paradigms/schema).

**§5.3:** VR contextual richness equalizes forgetting rates ages 20-70 (Age×Time null across all 5 analyses, d<0.01).

**§5.4:** Model averaging reveals forgetting rate IS trait-like (ICC=21%), but 4-timepoint design can't quantify reliably (need 8-10).

**§5.5:** IRT-CTT convergence exceptional (r>0.90), trajectory shapes robust to measurement choice, IRT critical for Ch7 external validity.

---

## CROSS-CHAPTER CONNECTIONS

**To Ch4 (Backward refs):**
- "We used 2-pass IRT purification (§4.2.2) and AIC model comparison (§4.3.3)"
- "For complete methodological details, see Chapter 4"

**To Ch6 (Forward refs):**
- "Chapter 6 tests whether confidence TRACKS these forgetting trajectories"
- "If accuracy declines following power-law (§5.1), does confidence decline in parallel or dissociate?"

**To Ch7 (Forward refs):**
- "Age-invariant VR forgetting (§5.3) contrasts with traditional tests, which Chapter 7 will show have robust age effects in this same sample"
- "IRT theta scores (§5.5) enable Chapter 7 cross-test prediction analyses"

---

**END CH5 INSTRUCTIONS**
