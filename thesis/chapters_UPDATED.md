# REMEMVR Thesis Chapter Structure (UPDATED)

**Last Updated:** 2026-01-02
**Status:** Ch1-3 partial drafts exist, Ch4 not written, Ch5-6 ready for writing (65 RQ reports complete), Ch7 deferred
**RQ Execution:** 65/85 RQs PLATINUM certified (35 Ch5 + 30 Ch6 + 0 Ch7)
**Architecture:** v4.X atomic agents (14 agents: rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, g_conflict, rq_tools, rq_analysis, g_code, g_debug, rq_inspect, rq_plots, rq_results, rq_report)
**Next Step:** Execute thesis/write.md plan (convert 65 reports → Ch5 + Ch6 thesis chapters)

---

# Chapter 1: INTRODUCTION

**File:** `thesis/introduction.md` (partial draft, 176 lines)
**Status:** §1.1-§1.6 drafted, §1.7 placeholder (no content)

**Description:**

This chapter establishes the theoretical and empirical foundation for why REMEMVR is needed. It reviews:
- Episodic memory definition using a functional/constructivist framework
- Neuroanatomical substrates (hippocampal network: CA1, CA3, dentate gyrus, entorhinal cortex, place cells, grid cells)
- Cognitive processes (encoding, consolidation via sleep, retrieval/reconstruction)
- Theoretical frameworks critically evaluated:
  - Process-Based Memory Framework (PMAT) - acknowledged as most empirically robust
  - Multiple Trace Theory (MTT) vs Standard Consolidation Theory
  - Scene Construction Theory (Hassabis & Maguire)
  - Contextual Binding Theory
- Measurement paradox: Existing tools achieve ecological validity OR experimental control, but not both
- The REMEMVR solution: How VR resolves this historical forced choice

**Theoretical Stance:** Framework-agnostic/exploratory (not testing specific framework hypotheses), functional/constructivist perspective adopted

**Section 1.7 Thesis Aims (TO WRITE):**
- 1.7.1 Characterizing VR episodic memory trajectories
- 1.7.2 Metacognitive monitoring in immersive environments
- 1.7.3 Individual differences and predictive validity
- 1.7.4 Methodological contributions (IRT+LMM pipeline)
- 1.7.5 Clinical and translational potential
- 1.7.6 Thesis structure overview

**Word count target:** §1.7 ~500 words total

---

# Chapter 2: METHOD

**File:** `thesis/methods.md` (partial draft, 137 lines)
**Status:** Drafted through §2.3.10

**Description:**

A concise but comprehensive protocol overview providing readers with the operational details needed to understand subsequent analyses:
- **Participants:** N=100, aged 20-70 (10 per 5-year band), stratified recruitment, 5 exclusions/withdrawals
- **VR apparatus:** Quest Pro, hand tracking, 1:1 locomotion, 8×5m space, Unity engine
- **Encoding procedure:** 4 rooms × 10 min, scripted interactions, 6 items per room
- **REMEMVR stimulus design:** Congruent/Incongruent/Common object categories, counterbalanced placement
- **Testing schedule:** Day 0/1/3/6, Latin square counterbalancing
- **Test structure:** 8 sections per test (Sleep → RFR → IFR → TCR → ICR → RRE → IRE → Strategy)
- **Scoring:** **Dichotomous (0/1)** - partial credit (0.5/0.25) piloted but abandoned due to scoring complexity
- **Confidence ratings:** 5-star Likert (1=Guess, 5=Certain), rescaled to 0-1, **not bias-corrected** (user concerned about interpretability loss)
- **Cognitive battery:** RAVLT, BVMT-R, NART (validity concerns - non-English speakers), RPM

**NOTE:** Partial credit description in §2.3.7 needs updating to reflect final decision (dichotomous only)

---

# Chapter 3: RATIONALE

**File:** `thesis/rationale.md` (partial draft, 136 lines)
**Status:** Drafted through §3.11

**Description:**

A detailed justification for every design decision, demonstrating that REMEMVR's development was systematic and theory-driven:
- **Why household rooms?** Familiarity, feasibility, 3D asset availability, cross-cultural applicability
- **Why 6 items not 8?** Pilot testing (N=20) showed floor effects with 8 items per room
- **Why congruent/incongruent/common categories?** Tests schema theory predictions
- **Why 3 paradigms?** Different retrieval processes: Generative (FR/CR) vs familiarity-based (RE)
- **Why logarithmic delay spacing?** 0, 1, 3, 6 days approximates Ebbinghaus curve
- **Why confidence ratings?** Metacognition, distinguishing lucky guesses from genuine recall
- **Why incidental encoding?** Prevents strategy confounds (participants unaware of test content)
- **Why hand tracking?** Embodied cognition, natural interaction, no controller learning curve
- **Design constraints acknowledged:** No tactile feedback, cultural generalizability limits (Western contexts), English-only

**Design Requirements Met:**
- Standardization (scripted protocol, fixed order)
- Longitudinal (4 timepoints, intercept/slope/residual decomposition)
- What/Where/When structure (Tulving's triad as heuristic, not cognitive architecture claim)
- Multi-paradigm (FR/CR/RE paradigms test different retrieval processes)
- Confidence ratings (5-star Likert, 2×2 contingency tables for metacognitive behaviors)

---

# Chapter 4: ANALYSIS METHODS

**Status:** NOT WRITTEN (planned but no draft exists)

**Description:**

This chapter explains the two-stage psychometric analysis pipeline and why it's superior to traditional approaches. Will likely include:

**Stage 1: Measurement Model (IRT)**
- Why GRM over Rasch/2PL/3PL models
- Multidimensional IRT specifications (What/Where/When factors)
- deepirtools IWAVE (variational autoencoder) estimation
- Composite_ID stacking approach (100 participants × 4 tests = 400 pseudo-participants)
  - Assumption violation acknowledged: Breaks independence assumption
  - Justification: Necessary compromise for model stability with N=100
- Iterative item purification procedure (a≥0.4, |b|≤3.0)
  - 2-pass calibration: All items → flag low quality → purified items only → final theta
- IRT assumptions and diagnostic checks
- **Missing:** IRT fit indices (RMSEA, CFI, TLI, test information curves) - user asks which to use
- **Missing:** Differential Item Functioning (DIF) testing - user asks if needed

**Stage 2: Longitudinal Model (LMM)**
- Why LMM over repeated-measures ANOVA
- Random intercepts + random slopes specification
- Time coding (Days, Days², log(Days+1), power-law variants)
- Model selection via AIC (Akaike weights, ΔAIC interpretation)
- Model averaging when best model weight < 0.90
- Assumption checking (residual normality, homoscedasticity, autocorrelation)

**CTT vs IRT Comparison**
- When conclusions differ
- Measurement precision advantages
- Convergence analysis (r_theta_CTT)

**Statistical Inference**
- Dual p-value reporting (uncorrected + Bonferroni, Decision D068)
- **NOTE:** Multiple comparisons corrections NOT YET APPLIED (user acknowledges needed)
- Effect sizes (Cohen's d, f², partial η²)
- LMM-specific effect sizes (ICC, marginal R², conditional R²)

**Software and Reproducibility**
- IRT: deepirtools (Python), mirt (R)
- LMM: statsmodels (Python), lme4 (R)
- Visualization: matplotlib + seaborn
- **Monte Carlo sampling:** mc_samples=1 for model_fit, mc_samples=100 for model_scores (rationale unclear - user can't recall)

**UNRESOLVED QUESTIONS:**
1. IRT fit indices to report? (User asks which)
2. DIF testing needed? (User asks if should)
3. Monte Carlo sample size justification? (User forgot rationale)
4. Multiple comparisons correction strategy? (Bonferroni, FDR, or none?)

**Action:** Could extract methodology from RQ report Section 4 (Methodology) across 65 reports to populate this chapter

---

# Chapter 5: THE TRAJECTORY OF EPISODIC FORGETTING

**Status:** ✅ **35/35 RQs PLATINUM CERTIFIED** + ✅ **35/35 RQ REPORTS GENERATED** → Ready for thesis chapter writing

**RQ Reports Location:** `./reports/5.*/report.md` (10-section comprehensive reports, 2025-12-31 to 2026-01-01)

**Writing Plan:** `thesis/write.md` (Hybrid Master + Theme Agents architecture, 9-15 hours estimated)

**Chapter Structure (from write.md):**
- §5.0 Introduction (500 words)
- §5.1 Power-Law Forgetting Paradigm (~3,500 words)
- §5.2 Content Effects (~3,000 words)
- §5.3 Age-Invariant VR Forgetting (~2,000 words)
- §5.4 Individual Differences (~2,500 words)
- §5.5 Methodological Validation (~1,500 words)
- §5.6 Chapter Summary (~1,000 words)
- **Total:** ~14,000 words

---

## 5.1 General Trajectory + Functional Form (5 RQs → 5.1.1-5.1.5)

**5.1.1 Functional Form of Forgetting Trajectories** ✅ PLATINUM
- **Finding:** Power-law (α_eff=0.41) DOMINATES, not Ebbinghaus logarithmic
- Extended model comparison: 66 models tested (vs original 5)
- Best model: PowerLaw_Alpha04 (AIC=866.61), Log model ranked #33 (ΔAIC=+3.10)
- Evidence ratio: 4.7:1 in favor of power law over logarithmic
- **Paradigm shift:** Wixted-style power-law forgetting, NOT Ebbinghaus tradition
- Report: `./reports/5.1.1/report.md` (453 lines, 26KB)

**5.1.2 Two-Phase Forgetting (Consolidation Window)** ✅ PLATINUM
- **Finding:** Deceleration confirmed, but gradual not discrete
- Three-test triangulation: Quadratic, piecewise, slope ratio
- Consolidation window vs practice saturation ambiguity
- Practice decomposition: T1→T2 vs T2→T4 effects separated
- Report: `./reports/5.1.2/report.md`

**5.1.3 General Age Effects** ✅ PLATINUM
- **Finding:** Age-invariant VR forgetting (Age×Time β=0.000022, p=.96)
- Age predicts baseline marginally (β=-0.011, p=.48, d=0.01 trivial)
- Age does NOT predict slope (all interactions p>.40)
- Model averaging across 40 converged models (17 competitive)
- **VR scaffolding hypothesis:** Contextual richness equalizes forgetting rates ages 20-70
- Report: `./reports/5.1.3/report.md`

**5.1.4 Variance Decomposition** ✅ PLATINUM
- **Finding:** Model averaging paradigm shift
- ICC_slope: 0.05% (single-model) → 21.61% (model-averaged) = **432-fold increase**
- Functional form sensitivity: Power-law allocates curvature to slopes, linear to residuals
- Intercept-slope correlation: r=-0.643 (compensatory mechanism)
- ICC_intercept=56.95% (2.6× larger than ICC_slope)
- Report: `./reports/5.1.4/report.md`

**5.1.5 Latent Trajectory Profiles (Clustering)** ✅ PLATINUM
- **Finding:** Three provisional profiles (weak quality, unstable)
- Cluster 0 "Low Stable" (N=25, θ=-0.78, slope≈0)
- Cluster 1 "High Maintainers" (N=44, θ=+0.37, slow decline)
- Cluster 2 "Fast Learners" (N=31, θ=+0.10, **IMPROVEMENT** +0.054)
- 31% show POSITIVE slopes (challenges universal forgetting assumption)
- Silhouette s=0.408 (weak), Jaccard=0.293 (unstable) - appropriate uncertainty
- Report: `./reports/5.1.5/report.md`

---

## 5.2 Domain-Specific Forgetting (7 RQs → 5.2.1-5.2.7)

**5.2.1 Domain Trajectories (What/Where/When)** ✅ PLATINUM
- **Finding:** Theta-scale trajectories PARALLEL (common forgetting mechanism)
- What/Where: Parallel decline (~0.86 SD over 6 days, β≈-0.143)
- When: Appears faster (β=-0.415, p<.001) BUT measurement failure
- Dual-scale reporting crucial: Theta parallel, probability divergent (baseline differences)
- Report: `./reports/5.2.1/report.md`

**5.2.2 Domain-Specific Consolidation** ✅ PLATINUM
- Analysis: Day 0→1 slope vs Day 1→6 slope by domain
- Report: `./reports/5.2.2/report.md`

**5.2.3 Domain × Age Interaction** ✅ PLATINUM
- **Finding:** Age null effects replicate across domains (all p>.40)
- No disproportionate spatial (Where) deficits in older adults
- Report: `./reports/5.2.3/report.md`

**5.2.4 IRT-CTT Convergent Validity (Domains)** ✅ PLATINUM
- **Finding:** Exceptional convergence (r_theta_CTT > 0.90)
- What: r=0.96, Where: r=0.94, When: r=0.89 (lowest due to floor compression)
- Trajectory shape robust to measurement choice (slope estimates within 5%)
- IRT critical for external validity (Ch7), CTT adequate for within-study
- Report: `./reports/5.2.4/report.md`

**5.2.5 Item Purification Effects (Domains)** ✅ PLATINUM
- **Finding:** What/Where purification improves (p<.001), When WORSENS
- When domain: 77% item exclusion → 6-item scale (measurement failure)
- Purification paradox: Strict thresholds improve quality but reduce coverage
- Report: `./reports/5.2.5/report.md`

**5.2.6 Domain ICC Decomposition** ✅ PLATINUM
- **Finding:** ICC_slope≈0 (design limitation replicates)
- 4-timepoint design insufficient for stable slope estimation
- Report: `./reports/5.2.6/report.md`

**5.2.7 Domain-Specific Clustering** ✅ PLATINUM
- **Finding:** Weak clustering quality (silhouette s=0.352)
- VR episodic memory = continuous distribution, NOT discrete phenotypes
- Report: `./reports/5.2.7/report.md`

---

## 5.3 Paradigm-Specific Forgetting (9 RQs → 5.3.1-5.3.9)

**5.3.1 Paradigm Trajectories (FR/CR/Recognition)** ✅ PLATINUM
- Analysis: 3-factor LMM with Paradigm × Time interaction
- Report: `./reports/5.3.1/report.md`

**5.3.2 Linear Trend in Paradigm Forgetting** ✅ PLATINUM
- **Finding:** Retrieval support PARADOX
- Recognition shows HIGHEST baseline BUT FASTEST forgetting (opposite TAP prediction)
- Familiarity-based recognition decays faster than recollection-based free recall
- Challenges Transfer-Appropriate Processing theory
- Report: `./reports/5.3.2/report.md`

**5.3.3 Paradigm-Specific Consolidation** ✅ PLATINUM
- Analysis: Early vs late forgetting by paradigm
- Report: `./reports/5.3.3/report.md`

**5.3.4 Paradigm × Age Interaction** ✅ PLATINUM
- **Finding:** Age null effects replicate across paradigms
- Report: `./reports/5.3.4/report.md`

**5.3.5 IRT-CTT Convergence (Paradigms)** ✅ PLATINUM
- **Finding:** Exceptional convergence (FR r=0.91, CR r=0.93, RE r=0.95)
- Report: `./reports/5.3.5/report.md`

**5.3.6 Purification Effects (Paradigms)** ✅ PLATINUM
- Analysis: Pre- vs post-purification paradigm effects
- Report: `./reports/5.3.6/report.md`

**5.3.7 Paradigm ICC Decomposition** ✅ PLATINUM
- **Finding:** ICC_slope≈0 (design limitation replicates)
- Report: `./reports/5.3.7/report.md`

**5.3.8 Paradigm-Specific Clustering** ✅ PLATINUM
- **Finding:** Silhouette s=0.367 (weak clustering quality)
- Report: `./reports/5.3.8/report.md`

**5.3.9 Paradigm × Item Difficulty Interaction** ✅ PLATINUM
- Analysis: Difficult items × paradigm × time
- Report: `./reports/5.3.9/report.md`

---

## 5.4 Schema Congruence Effects (7 RQs → 5.4.1-5.4.7)

**5.4.1 Schema Congruence Trajectories** ✅ PLATINUM
- **Finding:** Schema congruence shows NO trajectory effects (all p>.44)
- Congruent/Incongruent/Common items show parallel decay
- Schema-based consolidation NOT detectable in immersive VR
- Report: `./reports/5.4.1/report.md`

**5.4.2 Schema-Specific Consolidation** ✅ PLATINUM
- **Finding:** No differential consolidation for congruent items
- 3-way interaction (Congruence × Time-segment) non-significant
- Report: `./reports/5.4.2/report.md`

**5.4.3 Schema × Age Interaction** ✅ PLATINUM
- **Finding:** Age null effects replicate for schema conditions
- Report: `./reports/5.4.3/report.md`

**5.4.4 IRT-CTT Convergence (Schema)** ✅ PLATINUM
- **Finding:** Exceptional convergence (r>0.90 across all congruence levels)
- Report: `./reports/5.4.4/report.md`

**5.4.5 Purification Effects (Schema)** ✅ PLATINUM
- **Finding:** Purification-trajectory paradox (4/4 replications)
- Δr positive (convergence improves), ΔAIC +1.8 to +3.0 (fit worsens)
- Report: `./reports/5.4.5/report.md`

**5.4.6 Schema ICC Decomposition** ✅ PLATINUM
- **Finding:** ICC_slope≈0 (design limitation replicates)
- Report: `./reports/5.4.6/report.md`

**5.4.7 Schema-Specific Clustering** ✅ PLATINUM
- **Finding:** Silhouette s=0.236 (WEAKEST of all Ch5 clustering analyses)
- Report: `./reports/5.4.7/report.md`

---

## 5.5 Spatial Memory (Source vs Destination) (6 RQs → 5.5.1-5.5.6)

**5.5.1 Spatial Trajectory (Source vs Destination)** ✅ PLATINUM
- **Finding:** Minimal differentiation (p=.08, small effect)
- Source vs Destination show similar decay rates
- Report: `./reports/5.5.1/report.md`

**5.5.2 Spatial Consolidation** ✅ PLATINUM
- Analysis: Source vs destination consolidation windows
- Report: `./reports/5.5.2/report.md`

**5.5.3 Spatial × Age Interaction** ✅ PLATINUM
- **Finding:** Age null effects replicate for spatial memory
- Report: `./reports/5.5.3/report.md`

**5.5.4 IRT-CTT Convergence (Spatial)** ✅ PLATINUM
- **Finding:** Exceptional convergence (Source r=0.94, Destination r=0.92)
- Report: `./reports/5.5.4/report.md`

**5.5.5 Purification Effects (Spatial)** ✅ PLATINUM
- **Finding:** Purification paradox replicates (ΔAIC +17.92)
- Report: `./reports/5.5.5/report.md`

**5.5.6 Spatial ICC Decomposition** ✅ PLATINUM
- **Finding:** ICC_slope≈0 (design limitation replicates)
- Report: `./reports/5.5.6/report.md`

---

## Chapter 5 Summary (Major Theoretical Contributions)

**1. Power-Law Paradigm Shift:**
- 140 years of Ebbinghaus logarithmic tradition challenged
- Power-law (α_eff=0.41) dominates across ALL content facets
- Model averaging essential (extreme uncertainty, N_eff=15 competitive models)
- Theoretical shift: Wixted-style power-law forgetting (temporal distinctiveness theory)

**2. Baseline Effects, Trajectory Nulls:**
- Content affects WHAT you remember (baseline), NOT HOW you forget (theta-scale parallel)
- Domain/Paradigm/Schema differ at encoding but share common forgetting mechanism
- Dual-scale reporting prevents misattribution (theta reveals mechanism, probability reveals impact)

**3. Age-Invariant VR Forgetting:**
- VR scaffolding hypothesis: Contextual richness equalizes forgetting rates ages 20-70
- Age predicts baseline (marginally) but NOT slope (7/7 analyses p>.40)
- Contrasts sharply with traditional tests (Ch7 shows robust age effects)

**4. Model Averaging Paradigm Shift (Individual Differences):**
- ICC_slope: 0.05% → 21.61% = 432-fold increase via model averaging
- Functional form sensitivity: Variance decomposition extraordinarily sensitive to trajectory parameterization
- Forgetting rate IS trait-like when properly measured, but 4-timepoint design insufficient (need 8-10)

**5. Methodological Validation:**
- IRT-CTT convergence exceptional (r>0.90 across all facets)
- Trajectory shapes robust to measurement choice
- IRT critical for external validity (Ch7 cross-test prediction), CTT adequate for within-study

**6. Weak Clustering Quality (Cross-Cutting):**
- ALL clustering analyses show weak quality (s=0.236-0.408)
- VR episodic memory = continuous unidimensional construct, NOT discrete phenotypes
- Appropriate uncertainty quantification (not methodological flaw)

---

# Chapter 6: METACOGNITION IN EPISODIC MEMORY

**Status:** ✅ **30/30 RQs PLATINUM CERTIFIED** + ✅ **30/30 RQ REPORTS GENERATED** → Ready for thesis chapter writing

**RQ Reports Location:** `./reports/6.*/report.md` (10-section comprehensive reports, 2025-12-31 to 2026-01-01)

**Writing Plan:** `thesis/write.md` (Hybrid Master + Theme Agents architecture, integrated with Ch5)

**Chapter Structure (from write.md):**
- §6.0 Introduction (500 words)
- §6.1 Confidence Trajectories (~3,000 words)
- §6.2 Calibration & Metacognitive Accuracy (~3,500 words)
- §6.3 High-Confidence Errors (~2,500 words)
- §6.4 Confidence-Accuracy Dissociation (~2,000 words)
- §6.5 Chapter Summary (~500 words)
- **Total:** ~11,000 words

---

## 6.1 Confidence Trajectories (4 RQs → 6.1.1-6.1.4)

**6.1.1 General Confidence Trajectory** ✅ PLATINUM
- **Finding:** Confidence declines parallel accuracy on theta scale
- But ordinal confidence detects 54-221× more trait variance than binary accuracy
- Report: `./reports/6.1.1/report.md`

**6.1.2 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.1.2/report.md`

**6.1.3 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.1.3/report.md`

**6.1.4 Ordinal Confidence vs Binary Accuracy (Measurement Comparison)** ✅ PLATINUM
- **Finding:** 824× ICC ratio (confidence ICC / accuracy ICC)
- Ordinal confidence: ICC=54.1%, Binary accuracy: ICC=0.07%
- Ordinal measurement detects trait variance binary scales miss
- **Theoretical:** Metacognitive monitoring partially dissociated from memory architecture
- Report: `./reports/6.1.4/report.md`

---

## 6.2 Calibration & Utility (5 RQs → 6.2.1-6.2.5)

**6.2.1 Metacognitive Resolution (Gamma Correlation)** ✅ PLATINUM
- Analysis: Ability to distinguish correct from incorrect across time
- Report: `./reports/6.2.1/report.md`

**6.2.2 Calibration Curves** ✅ PLATINUM
- **Finding:** Overconfidence at all delays
- Metacognitive monitoring degrades with memory trace strength
- Report: `./reports/6.2.2/report.md`

**6.2.3 Brier Score Decomposition** ✅ PLATINUM
- Analysis: Calibration, resolution, uncertainty components
- Report: `./reports/6.2.3/report.md`

**6.2.4 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.2.4/report.md`

**6.2.5 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.2.5/report.md`

---

## 6.3 Domain-Specific Metacognition (4 RQs → 6.3.1-6.3.4)

**6.3.1 Domain-Specific Confidence Trajectories** ✅ PLATINUM
- **Finding:** What/Where confidence parallel, When steeper decline
- Domain trajectories dissociate between accuracy (Ch5 5.2.1) and confidence
- Report: `./reports/6.3.1/report.md`

**6.3.2 Domain Calibration Crossover** ✅ PLATINUM
- **Finding:** When/Where/What show different metacognitive accuracy patterns
- Calibration varies by content type (domain-specific monitoring mechanisms)
- Report: `./reports/6.3.2/report.md`

**6.3.3 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.3.3/report.md`

**6.3.4 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.3.4/report.md`

---

## 6.4 Paradigm-Specific Metacognition (4 RQs → 6.4.1-6.4.4)

**6.4.1 Paradigm Confidence Trajectories** ✅ PLATINUM
- Analysis: FR/CR/Recognition confidence patterns
- Report: `./reports/6.4.1/report.md`

**6.4.2 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.4.2/report.md`

**6.4.3 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.4.3/report.md`

**6.4.4 Paradigm Calibration** ✅ PLATINUM
- **Finding:** Recognition shows better metacognitive monitoring (familiarity signals clearer)
- Report: `./reports/6.4.4/report.md`

---

## 6.5 Schema & Metacognition (4 RQs → 6.5.1-6.5.4)

**6.5.1 Schema Confidence Trajectories** ✅ PLATINUM
- Analysis: Congruence effects on confidence
- Report: `./reports/6.5.1/report.md`

**6.5.2 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.5.2/report.md`

**6.5.3 High-Confidence Errors by Schema** ✅ PLATINUM
- **Finding:** HCE rate shows NULL schema effects (replicates Ch5 5.4.1 accuracy pattern)
- Schema does NOT affect metacognitive dissociation rates
- Report: `./reports/6.5.3/report.md`

**6.5.4 Schema Calibration** ✅ PLATINUM
- Analysis: Congruence effects on metacognitive accuracy
- Report: `./reports/6.5.4/report.md`

---

## 6.6 High-Confidence Errors (General) (2 RQs → 6.6.1-6.6.2)

**6.6.1 HCE Temporal Patterns** ✅ PLATINUM
- **Finding:** 15-20% of errors made with high confidence
- HCE rate stable across delays (no temporal increase)
- **Theoretical:** HCE driven by metacognitive monitoring failure, not memory reconstruction
- Report: `./reports/6.6.1/report.md`

**6.6.2 Dunning-Kruger Effect** ✅ PLATINUM
- **Finding:** NOT SUPPORTED (double null)
- Low performers do NOT show overconfidence bias
- Report: `./reports/6.6.2/report.md`

---

## 6.7 Domain × HCE (4 RQs → 6.7.1-6.7.4)

**6.7.1 HCE Domain Modulation** ✅ PLATINUM
- Analysis: What/Where/When HCE rates
- Report: `./reports/6.7.1/report.md`

**6.7.2 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.7.2/report.md`

**6.7.3 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.7.3/report.md`

**6.7.4 HCE Paradigm Modulation** ✅ PLATINUM
- Analysis: FR/CR/Recognition HCE patterns
- Report: `./reports/6.7.4/report.md`

---

## 6.8 Spatial Metacognition (4 RQs → 6.8.1-6.8.4)

**6.8.1 Spatial Confidence Trajectories** ✅ PLATINUM
- Analysis: Source vs destination confidence patterns
- Report: `./reports/6.8.1/report.md`

**6.8.2 [RQ Description]** ✅ PLATINUM
- Report: `./reports/6.8.2/report.md`

**6.8.3 Spatial Source-Destination Dissociation** ✅ PLATINUM
- **Finding:** OPPOSITE correlations (accuracy vs confidence)
- Accuracy: +0.99 source, -0.90 destination
- Confidence: -0.24, -0.40 (both negative)
- **Theoretical:** Metacognition partially dissociated from memory architecture
- Report: `./reports/6.8.3/report.md`

**6.8.4 HCE Spatial Patterns** ✅ PLATINUM
- Analysis: Source vs destination HCE rates
- Report: `./reports/6.8.4/report.md`

---

## Chapter 6 Summary (Major Theoretical Contributions)

**1. Confidence-Accuracy Convergence AND Dissociation:**
- Confidence tracks forgetting (parallel theta-scale decline)
- BUT ordinal confidence detects 54-221× more trait variance (measurement dissociation)
- Domain trajectories differ (When steeper for confidence vs accuracy parallel)

**2. Overconfidence at All Delays:**
- Metacognitive monitoring degrades with memory trace strength
- Calibration varies by content type (domain-specific mechanisms)

**3. HCE Driven by Metacognition, Not Memory:**
- 15-20% of errors made with high confidence
- HCE rate stable across delays (no temporal increase = not reconstruction failure)
- Metacognitive monitoring failure, not false memory generation

**4. Dunning-Kruger NOT Supported:**
- Low performers do NOT show overconfidence bias (double null)
- Challenges popular metacognitive theory

**5. Spatial Dissociation:**
- Opposite correlations for accuracy vs confidence (source-destination patterns)
- Metacognitive monitoring partially independent from memory architecture

---

# Chapter 7: INDIVIDUAL DIFFERENCES IN EPISODIC MEMORY

**Status:** ⚠️ **0/28 RQs EXECUTED** (Specifications complete, execution pending)

**RQ Reports Location:** N/A (Ch7 work not yet started)

**Specifications:** `results/ch7/specs.md` (comprehensive RQ specs, ready for rq_concept)

**Central Thesis Question:** If REMEMVR (ecological VR memory) and traditional tests (RAVLT, BVMT) measure the same construct, they should correlate highly. If they don't, what explains the gap, and what does REMEMVR reveal that traditional tests miss?

**Why Ch7 is the ANCHOR Chapter:** Ch7 connects REMEMVR (new, exploratory) to existing literature (RAVLT, BVMT - tried and tested). The divergence between REMEMVR and traditional tests is one of the key arguments of the thesis introduction.

---

## Theme 1: Predictive Validity (Core) — 4 RQs

| RQ | Title | Priority |
|----|-------|----------|
| **7.1.1** | Do cognitive tests predict overall REMEMVR ability? | TIER 1 |
| **7.1.2** | Do tests predict intercept (Day 0) vs slope (forgetting)? | TIER 1 |
| **7.1.3** | Which test predicts which domain? (RAVLT→What, BVMT→Where) | TIER 1 |
| **7.1.4** | Unique REMEMVR variance unexplained by all predictors (>50%)? | TIER 1 |

**Key Finding Expected:** Cognitive tests predict ~35% of REMEMVR variance (convergent validity), but >50% remains unexplained (divergent validity = ecological validity gap).

---

## Theme 2: Age × VR Scaffolding — 4 RQs

| RQ | Title | Priority |
|----|-------|----------|
| **7.2.1** | Does age predict REMEMVR after controlling for cognitive tests? | TIER 1 |
| **7.2.2** | Do cognitive tests attenuate age effects on REMEMVR? | TIER 1 |
| **7.2.3** | Is there Age × Cognitive Test interaction? | TIER 1 |
| **7.2.4** | **VR Scaffolding Validation:** REMEMVR age-invariant while RAVLT declines? | TIER 1 (NEW) |

**Key Finding Expected:** Same participants show age decline on RAVLT but not REMEMVR. This validates VR scaffolding hypothesis from Ch5 (Age×Time p=.96).

---

## Theme 3: Metacognition Predictors — 5 RQs (NEW THEME)

| RQ | Title | Priority |
|----|-------|----------|
| **7.3.1** | Do cognitive tests predict confidence trajectories? | TIER 2 (NEW) |
| **7.3.2** | Do cognitive tests predict calibration quality? | TIER 2 (NEW) |
| **7.3.3** | Do cognitive tests predict HCE (high-confidence error) rate? | TIER 2 (NEW) |
| **7.3.4** | Does DASS-Anxiety predict metacognition more than memory? | TIER 2 |
| **7.3.5** | Does confidence-accuracy gap predict cognitive reserve? | TIER 2 (NEW) |

**Key Finding Expected:** Traditional tests predict accuracy but NOT confidence/calibration. RPM may predict calibration (metacognition requires executive processes). Connects to Ch6's 824× ICC ratio.

---

## Theme 4: Process-Specific Prediction — 3 RQs

| RQ | Title | Priority |
|----|-------|----------|
| **7.4.1** | Does RAVLT Free Recall predict REMEMVR Free Recall > Recognition? | TIER 3 |
| **7.4.2** | Does BVMT predict Where more than What? | TIER 3 |
| **7.4.3** | Does RPM predict complex integration (What+Where+When)? | TIER 3 |

**Key Finding Expected:** Process-specific transfer confirmed (RAVLT→Free Recall, BVMT→Where). Domain-specificity validates theoretical distinction between verbal and visuospatial memory systems.

---

## Theme 5: Self-Report & Contextual — 4 RQs

| RQ | Title | Priority |
|----|-------|----------|
| **7.5.1** | Do sleep, education, VR experience predict REMEMVR? | TIER 4 |
| **7.5.2** | Does DASS predict memory performance? | TIER 4 |
| **7.5.3** | Do memory strategies correlate with performance? | TIER 4 |
| **7.5.4** | **Per-Test Sleep:** Does sleep BEFORE each test predict THAT test? | TIER 4 (NEW) |

**Key Finding Expected:** Per-test sleep shows within-person state effects (unique longitudinal contribution). DASS effects small.

---

## Theme 6: Individual Differences in Forgetting — 4 RQs (NEW THEME)

| RQ | Title | Priority |
|----|-------|----------|
| **7.6.1** | Do cognitive tests predict individual differences in slope? | TIER 3 |
| **7.6.2** | Does RAVLT Delayed predict REMEMVR slope? | TIER 3 (NEW) |
| **7.6.3** | ICC slope replication across domains? | TIER 3 (NEW) |
| **7.6.4** | Purification & Slope: Do predictors change after IRT purification? | TIER 3 (NEW) |

**Key Finding Expected:** Tests predict intercept but NOT slope. Ch5 found ICC_slope = 21% (individual differences exist), but they're unpredicted by traditional tests (different mechanism = consolidation vs encoding).

---

## Theme 7: Clinical Utility & Alternative Interpretation — 4 RQs (NEW THEME)

| RQ | Title | Priority |
|----|-------|----------|
| **7.7.1** | Reverse Inference: Can REMEMVR predict RAVLT/BVMT? | TIER 1 |
| **7.7.2** | Discrepancy Analysis: Who shows RAVLT-REMEMVR divergence? | TIER 1 (NEW) |
| **7.7.3** | Alternative RAVLT Scoring: Learning Slope better than Total? | TIER 1 (NEW) |
| **7.7.4** | Clinical Profiles: "False negatives" (low RAVLT, normal REMEMVR)? | TIER 1 (NEW) |

**Key Finding Expected:** When tests and REMEMVR disagree, identify who diverges and why. Older adults may show VR-favored pattern (VR scaffolding). Alternative RAVLT scoring suggestions for clinical practice.

---

## Theme 8: Latent Profiles & Models — 4 RQs

| RQ | Title | Priority |
|----|-------|----------|
| **7.8.1** | Distinct REMEMVR memory profiles (K=2-4)? | TIER 4 |
| **7.8.2** | Cognitive test profiles predict REMEMVR profiles? | TIER 4 |
| **7.8.3** | Parsimonious predictive model with 5-fold cross-validation | TIER 4 |
| **7.8.4** | Multivariate vs univariate prediction | TIER 4 |

**Key Finding Expected:** 2-3 latent profiles (Generalist, Average, Low). Age + RAVLT + BVMT achieves CV-R² ≈ 0.30-0.35 with acceptable shrinkage.

---

## Chapter 7 Status Summary

| Metric | Value |
|--------|-------|
| **Total RQs** | 28 (8 themes) |
| **New RQs (vs old 20)** | 12 added (metacognition, clinical utility, slope predictors) |
| **IRT analyses complete** | 0/28 |
| **Specifications complete** | 28/28 (`results/ch7/specs.md`) |
| **Reports generated** | 0/28 |

### Priority Tiers

| Tier | Theme | RQs | Est. Hours | Description |
|------|-------|-----|------------|-------------|
| **TIER 1** | 1, 2, 7 | 12 | ~12h | Core thesis: Predictive validity + Age + Clinical utility |
| **TIER 2** | 3 | 5 | ~6h | Metacognition: Connects to Ch6 |
| **TIER 3** | 4, 6 | 7 | ~8h | Process-specific + Slope predictors: Connects to Ch5 |
| **TIER 4** | 5, 8 | 8 | ~8h | Self-report + Profiles: Nice-to-have |
| **TOTAL** | - | 28 | ~34h | Full Ch7 execution |

**Minimum Viable Ch7:** Tier 1 (12 RQs, ~12h) delivers the anchor chapter connecting REMEMVR to existing literature.

### Data Sources

| Source | Variables | Usage |
|--------|-----------|-------|
| Ch5 results | Theta_All, domain theta, slopes | DVs for prediction |
| Ch6 results | Confidence theta, calibration, HCE | DVs for metacognition RQs |
| master.xlsx | RAVLT, BVMT, NART, RPM | IVs: cognitive tests |
| master.xlsx | Age, Education, Sleep, DASS | IVs: demographics/self-report |
| master.xlsx | Per-test sleep (SLP tags) | State-dependent analysis (7.5.4) |

### Key Theoretical Contributions Expected

1. **Convergent + Divergent Validity:** Tests predict ~35%, but >50% unexplained = ecological validity gap
2. **VR Scaffolding Validated:** RAVLT shows age decline, REMEMVR doesn't (same sample)
3. **Metacognition Distinct:** Traditional tests don't predict confidence/calibration
4. **Clinical Utility:** Discrepancy analysis + alternative scoring recommendations
5. **Encoding vs Consolidation:** Tests predict intercept (encoding), NOT slope (consolidation)

---

# Chapter 8: DISCUSSION

**Status:** NOT WRITTEN (outlined only)

**Description:**

Synthesizes findings across all empirical chapters, interprets within broader theoretical landscape, discusses implications.

**Likely Structure:**
- Summary of key findings (Ch5: power-law, age-invariant, model averaging; Ch6: confidence-accuracy dissociation, HCE mechanisms; Ch7: TBD)
- Theoretical implications: Which frameworks supported? (Framework-agnostic stance maintained)
- Methodological contributions: REMEMVR as new tool, IRT+LMM advantages
- Clinical utility: Early detection potential, memory disorder differentiation
- Ecological validity achieved: Did we measure "real" episodic memory?
- Limitations:
  - Sample size (N=100 adequate for IRT, marginal for complex interactions)
  - Cultural generalizability (Western household rooms)
  - VR limitations (no tactile feedback, visual resolution)
  - Single encoding session
  - 4-timepoint design (insufficient for stable slope estimation)
- Future directions:
  - Normative data collection across lifespan
  - Clinical validation (MCI, AD, frontal amnesia cohorts)
  - Longitudinal follow-up (forgetting slopes predict future decline?)
  - Cross-cultural room packs
  - Neuroimaging integration (fMRI during VR encoding)
  - Intervention studies (rTMS, cognitive training)
- Translational vision: REMEMVR as standard assessment in memory clinics (complement not replace current tests)

**Unifying Finding:** "Traditional pen-paper tests aren't measuring episodic memory as we understand/use it in everyday life. REMEMVR provides tools to better understand/interpret traditional test results OR develop VR test practical for clinic."

**Elevator Pitch (to develop):** REMEMVR demonstrates that ecological episodic memory assessment in VR reveals age-invariant forgetting patterns and metacognitive dissociations invisible to traditional tests, with implications for refining clinical interpretation and assessment practices.

---

# RQ EXECUTION SUMMARY

| Chapter | RQs Planned | RQs PLATINUM | Reports Generated | Status |
|---------|-------------|--------------|-------------------|--------|
| Ch1 (Intro) | N/A | N/A | N/A | Partial draft (§1.7 placeholder) |
| Ch2 (Methods) | N/A | N/A | N/A | Partial draft (complete) |
| Ch3 (Rationale) | N/A | N/A | N/A | Partial draft (complete) |
| Ch4 (Analysis) | N/A | N/A | N/A | Not written |
| **Ch5 (Forgetting)** | **35** | **35** ✅ | **35** ✅ | **READY FOR WRITING** |
| **Ch6 (Metacognition)** | **30** | **30** ✅ | **30** ✅ | **READY FOR WRITING** |
| Ch7 (Individual Diffs) | 28 | 0 | 0 | Specs complete (results/ch7/specs.md) |
| Ch8 (Discussion) | N/A | N/A | N/A | Not written |
| **TOTAL** | **93** | **65** | **65** | **70% PLATINUM certified** |

---

# NEXT STEPS

**IMMEDIATE (Week of 2026-01-02):**

1. **Resolve conflicts** (see `thesis/conflicts_analysis.md`)
   - Update thesis/methods.md §2.3.7 (partial credit → dichotomous)
   - Write thesis/introduction.md §1.7 (500 words, thesis aims)
   - Decide: Write Ch4 first or use placeholders in Ch5-Ch6?

2. **Execute thesis/write.md plan** (9-15 hours)
   - Phase 1: Master prep (read 65 report summaries, create theme specs)
   - Phase 2: Create rq_theme_writer agent
   - Phase 3: Execute 9 theme agents (5 Ch5 + 4 Ch6)
   - Phase 4: Master integration (transitions, intro, summary)
   - Phase 5: Cohesion & polish (g_conflict, standardize, validate)
   - Phase 6: User review & revision

3. **Deliverables:**
   - thesis/chapter_5_empirical.md (~14k words, THESIS-READY)
   - thesis/chapter_6_empirical.md (~11k words, THESIS-READY)

**MEDIUM-TERM (Post Ch5-Ch6):**

4. **Chapter 4: Analysis Methods** (if needed before thesis submission)
   - Extract methodology from 65 RQ reports Section 4
   - Use rq_theme_writer to synthesize cross-RQ method descriptions
   - Resolve unresolved questions (IRT fit indices, DIF testing, multiple comparisons)

5. **Chapter 7: Individual Differences** (SPECIFICATIONS COMPLETE)
   - Specs location: `results/ch7/specs.md` (28 RQs, 8 themes)
   - Tier 1 (Core Thesis): 12 RQs, ~12h - Predictive validity + Age + Clinical utility
   - Tier 2 (Metacognition): 5 RQs, ~6h - Connects to Ch6
   - Tier 3 (Processes): 7 RQs, ~8h - Connects to Ch5
   - Tier 4 (Profiles): 8 RQs, ~8h - Nice-to-have
   - Execute via: rq_concept → rq_planner → remaining pipeline → rq_report
   - NEW RQs: VR scaffolding validation (7.2.4), metacognition predictors (7.3.x), clinical utility (7.7.x)

**LONG-TERM (Post-Thesis):**

6. **Chapter 8: Discussion** (synthesis + future directions)
7. **Publication planning** (extract journal articles from thesis chapters)
8. **Clinical validation studies** (MCI, AD cohorts)

---

**END CHAPTERS.MD UPDATE**
