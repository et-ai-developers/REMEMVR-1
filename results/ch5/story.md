# Chapter 5: What the Data Actually Says

**Draft Date:** 2025-12-03
**Status:** 18/31 RQs complete (58%), honest assessment
**Purpose:** Critical self-examination of findings, not thesis prose

---

## Executive Summary: The Honest Version

Chapter 5 set out to characterize episodic forgetting in VR. After 18 completed analyses, the story is more nuanced than expected. Some findings replicate classic memory research. Others are surprising nulls. A few reveal genuine measurement innovations. And some results raise questions we can't fully answer yet.

**The headline:** Forgetting follows the classic Ebbinghaus logarithmic curve, but almost nothing else we hypothesized about *what modulates* forgetting held up. Age doesn't matter. Domains don't differ (except for a measurement failure). Paradigms don't differentiate. Schemas don't help. Forgetting rate appears almost entirely situational, not a stable trait.

This is either a profound finding about the homogenizing effect of VR immersion, or it reflects limitations in our sample, task, or statistical power. Probably some of both.

---

## THE GOOD

### 1. Logarithmic Forgetting is Real and Robust

**Finding:** Across all analyses, the logarithmic model wins decisively.
- RQ 5.1.1: Log model AIC weight = 48% (Lin+Log = 32%, combined = 80%)
- RQ 5.2.1: Log model AIC weight = 62%
- RQ 5.3.1: Log model AIC weight = 99.99%
- RQ 5.4.1: Log model AIC weight = 99.998%

**What this means:** Memory declines rapidly in the first 24 hours (~0.55 SD drop from Day 0 to Day 1), then slows asymptotically (only ~0.25 SD additional drop from Day 3 to Day 6). This is the Ebbinghaus forgetting curve, replicated 140 years later in immersive VR.

**Validity assessment:** HIGH. This is the one finding I'd bet on. The pattern is consistent across domains, paradigms, and analysis approaches. The AIC weights are often >90%, leaving little room for alternative models.

**What it contributes:** Confirms VR episodic memory follows established forgetting dynamics. REMEMVR measures something real.

---

### 2. IRT Detects Individual Differences That CTT Cannot

**Finding (RQ 5.2.4, corrected):** When modeling forgetting trajectories:
- IRT random slope variance = 0.021 (meaningful individual differences)
- CTT random slope variance = 0.000 (boundary estimate - nothing detected)

**What this means:** IRT-based ability estimates can distinguish people who forget faster from people who forget slower. CTT-based mean scores cannot - everyone looks the same.

**Why this matters for the thesis:** This directly supports using IRT over CTT for clinical applications. If REMEMVR is ever used to identify people with atypical forgetting (e.g., MCI screening), IRT is necessary. CTT would miss individual variation entirely.

**Validity assessment:** MODERATE-HIGH. The effect emerged only after correcting a specification error (we were using linear random slopes when the fixed effects were logarithmic). The correction made theoretical sense and revealed the expected pattern. But:
- N=100 is marginal for detecting small random effects
- CTT boundary estimate *could* be a power issue, not a true ceiling
- Only tested in domain-specific analyses, not replicated across paradigms yet

**Caveat:** Static correlations between IRT and CTT are exceptional (r = 0.91-0.97). They measure the same thing at any single timepoint. The divergence is specifically in *trajectory* modeling.

---

### 3. Two-Phase Forgetting Pattern Exists (But Gradual)

**Finding (RQ 5.1.2):** Two of three tests support a two-phase pattern:
- Quadratic term significant (p < 0.001) - forgetting decelerates
- Slope ratio test: Late forgetting only 16% as fast as Early (p < 0.000002)
- BUT: Piecewise model NOT better than continuous (ΔAIC = +5 favoring continuous)

**What this means:** Forgetting does slow down after the first night (consistent with sleep consolidation), but the transition is gradual, not a sharp inflection at 48 hours. The classic "consolidation window" framing may be oversimplified.

**Validity assessment:** MODERATE. The piecewise model comparison is confounded - we used different random effect structures (the piecewise model failed to converge with full random slopes). A fair comparison would require matched structures. The pattern is real, but the precise timing of deceleration is uncertain.

---

### 4. The Analysis Pipeline Works

**Meta-finding:** After building and debugging 26 analysis tools and 13 specialized agents:
- 258/261 tests passing (98.9%)
- Zero-bug execution achieved on several RQs
- Full validation chain (rq_inspect → rq_plots → rq_results) catching errors

**What this means:** The infrastructure is publication-ready. Results are reproducible, validated, and auditable.

---

## THE BAD

### 1. Age Effects Are Absent

**Finding (RQ 5.1.3, 5.2.3, 5.3.4, 5.4.3):** No significant age effects on forgetting rate across ANY analysis.
- RQ 5.1.3: Age × Time interaction p = 0.83 (linear), p = 0.76 (log)
- RQ 5.2.3: Age × Domain × Time all p > 0.4
- RQ 5.3.4: Age × Paradigm × Time all p > 0.7
- RQ 5.4.3: Age × Congruence × Time all p > 0.15

Effect sizes are trivial (Cohen's d ≈ 0.10 at Day 6, expected d = 0.2-0.5).

**Why this is problematic:** The hippocampal aging literature predicts older adults should show:
1. Lower baseline memory (encoding deficit)
2. Faster forgetting (consolidation deficit)

We see a marginal trend for lower baseline (p = 0.06 uncorrected, not significant after correction) and literally nothing for forgetting rate.

**Possible explanations:**
1. **VR scaffolding:** Immersive encoding may support older adults, masking deficits that appear in traditional tasks
2. **Practice effects:** Four repeated tests may allow older adults to catch up through re-learning
3. **Sample restriction:** Age range 20-70 (mean 44.6) may not include enough elderly participants (70-85) where deficits are strongest
4. **Power:** N=100 may be insufficient for age × time interactions (typically need N>150)
5. **Real null:** Maybe episodic forgetting rates genuinely don't differ by age in this paradigm

**Validity assessment:** UNCERTAIN. The null is consistent across multiple analyses, which argues against it being a fluke. But we cannot rule out methodological limitations masking a true effect. This needs explicit discussion in the thesis - we cannot claim "age doesn't matter" without acknowledging these caveats.

---

### 2. Domain Differences Largely Absent (What = Where)

**Finding (RQ 5.2.1):** What and Where domains show statistically equivalent forgetting.
- Where vs What: β = 0.037, p = 0.72

The hypothesis was that object identity (What) would be more resilient than spatial location (Where). There's no evidence for this.

**What it means:** Spatial and object memory decay at the same rate in VR, at least as measured here.

**Validity assessment:** MODERATE. The comparison is methodologically sound. But:
- Item counts differ substantially (What: 19 items, Where: 45 items after purification)
- When domain had to be excluded entirely (see "The Ugly")
- Different item pools may have different baseline difficulties that confound trajectory comparisons

---

### 3. Consolidation Benefits Are Domain/Paradigm-Invariant

**Finding (RQ 5.2.2, 5.3.3):** All tested categories show similar consolidation benefits.
- RQ 5.2.2: No domain-specific consolidation (all contrasts p > 0.68)
- RQ 5.3.3: No paradigm-specific consolidation (all contrasts p > 0.16 after correction)

Early slope (~-0.4 theta/day) vs Late slope (~-0.1 theta/day) - a ~6× reduction in forgetting rate after the first night. But this happens equally for everything.

**Why this contradicts theory:**
- Levels-of-processing predicts deeper encoding → more consolidation benefit (Free Recall should benefit most)
- Sleep consolidation literature suggests hippocampal-dependent memories (spatial) benefit more
- Schema theories predict congruent items consolidate preferentially

None of this held up.

**Validity assessment:** MODERATE. The analyses are well-powered for detecting the interactions we hypothesized. The null is probably real. But:
- 4 timepoints limits our ability to localize *when* consolidation effects emerge
- The "Day 0-1 vs Day 1-6" split is crude - consolidation may operate on different timescales

---

### 4. Schema Congruence Does Nothing

**Finding (RQ 5.4.1, 5.4.2, 5.4.3):** No schema effects on forgetting.
- Main effects: All p > 0.44
- Consolidation interaction: p = 0.94
- Age moderation: All p > 0.15

Common, Congruent, and Incongruent items all forget at the same rate.

**Why this is surprising:** Schema-based facilitation is well-established in memory literature (Bartlett 1932, updated by Ghosh & Gilboa 2014). Schema-congruent information should be easier to integrate into existing knowledge structures.

**Possible explanations:**
1. **VR context doesn't engage schemas:** The object-room pairings may not trigger schema-based processing
2. **Experimenter-defined ≠ participant-perceived:** Our congruence categories may not match how participants actually processed the items
3. **Schema effects on encoding, not forgetting:** Schemas may help initial learning (baseline) without affecting decay rate
4. **Item selection:** Only 2 item codes per category (i1-i6) - limited generalizability

**Validity assessment:** MODERATE. Null is consistent across three analyses. But the manipulation may have been weak.

---

## THE UGLY

### 1. When Domain is Unusable (77% Item Attrition)

**Finding (RQ 5.2.1 and propagated):** Temporal memory items (When) failed psychometrically.
- Original items: 26
- Retained after purification: 6 (23% retention)
- Probability at all timepoints: 6-9% (floor effect)

**What went wrong:** Participants couldn't do the temporal ordering task. Performance was near chance throughout the study. IRT purification correctly excluded items that don't discriminate ability levels, but this left us with too few items to meaningfully measure the construct.

**Impact:** When domain had to be excluded from ALL downstream domain analyses (RQ 5.2.2, 5.2.3, 5.2.4). We cannot make claims about temporal memory forgetting.

**Is this a failure?** Partially. The original task design didn't adequately support temporal encoding in VR. This is a legitimate finding about VR memory assessment (temporal memory is hard to measure this way), but it limits Chapter 5's scope.

**The silver lining:** Dual-scale reporting (Decision D069 - theta + probability plots) caught this. On the theta scale alone, When looked like it was forgetting *slower* than What/Where. The probability scale revealed this was an artifact - you can't forget what you never learned.

---

### 2. The ICC Paradox: Forgetting Rate is Not Trait-Like

**Finding (RQ 5.1.4):** Forgetting rate shows essentially zero between-person variance.
- ICC_intercept = 0.61 (good - 61% of baseline variance is stable individual differences)
- ICC_slope = 0.0005 (0.05% - virtually no stable individual differences in forgetting rate)

Slope variance is 3,000× smaller than intercept variance. This is extreme.

**What this means:** People differ reliably in how much they remember at baseline, but everyone forgets at almost exactly the same rate. Forgetting appears to be a situational (state) phenomenon, not a stable trait.

**Why this is problematic:**
1. Contradicts literature (typical ICC for forgetting = 0.30-0.50)
2. The intercept-slope correlation is r = -0.97, which is suspiciously high (literature: r = -0.2 to -0.4)
3. Raises questions about model specification

**Possible explanations:**
1. **VR homogenizes forgetting:** Immersive encoding creates uniform consolidation conditions
2. **Measurement precision:** 4 timepoints may be insufficient to reliably estimate individual slopes
3. **Model misspecification:** The Log model showed singular covariance (var_slope ≈ 0); Lin+Log fixed this but variance is still tiny
4. **Sample homogeneity:** If participants are relatively similar (healthy adults, narrow age range), individual differences may be genuinely small

**Validity assessment:** LOW-MODERATE. The finding is consistent across model variants, but the extreme values (0.05% ICC, -0.97 correlation, 3,000× variance ratio) suggest something may be wrong. This needs Bayesian sensitivity analysis and possibly more data before strong conclusions.

---

### 3. Random Slope Specification Error (Caught and Fixed)

**What happened:** Three RQs (5.2.4, 5.3.4, 5.4.3) used wrong random effects specification.
- Used: `re_formula="~TSVR_hours"` (linear time)
- Should have used: `re_formula="~log_TSVR"` (log time, per ROOT RQ model selection)

This caused random slope variance estimates of exactly 0.000 (boundary), masking individual differences.

**How it was caught:** User noticed suspicious pattern (all three RQs showing identical boundary estimates). Investigation revealed the mismatch with ROOT RQ model selection.

**Impact:** All three RQs had to be re-run. Results changed meaningfully - IRT now detects individual differences that were previously invisible.

**Lesson learned:** Random effects must align with fixed effects transformation. This is now documented as a methodological principle.

**Validity assessment:** HIGH (after correction). The correction was theoretically motivated and produced expected results. But this error existed for multiple sessions before being caught. What other specification issues might we have missed?

---

### 4. Statistical Fragility: Convergence Failures and Workarounds

**Pattern across Chapter 5:**
- RQ 5.1.2: Piecewise model non-convergence (had to use simpler random structure)
- RQ 5.1.4: Log model singular covariance (had to switch to Lin+Log)
- RQ 5.2.3: Complex 3-way model forced intercepts-only random effects
- Multiple RQs: Statsmodels pickle/patsy issues required monkey-patch workarounds

**What this means:** N=100 is marginal for the models we're fitting. Complex random effect structures (random slopes for time, especially with interactions) frequently fail to converge or hit boundary constraints.

**Impact on validity:** Every time we simplify random effects due to convergence failure, we're potentially biasing results. Simpler models may miss real effects. We're operating at the edge of what the data can support.

---

## What Story Is Chapter 5 Actually Telling?

### The Charitable Interpretation

REMEMVR successfully measures episodic memory in VR, and that memory decays logarithmically - the fundamental pattern discovered by Ebbinghaus in 1885. VR provides a standardized, immersive encoding experience that may homogenize individual differences in forgetting. This could be a feature, not a bug: REMEMVR measures memory decay under controlled conditions, stripping away the noise of differential encoding strategies, environmental distractions, and practice effects that plague traditional memory tasks.

The IRT methodology is vindicated: it detects individual trajectory differences that CTT cannot. This has clinical implications - IRT-based REMEMVR could identify atypical forgetting patterns (early MCI?) that would be invisible to simpler scoring approaches.

The null findings for age, domain, paradigm, and schema effects may reflect the power of VR immersion to create uniform memory experiences. Or they may point to theoretical weaknesses in traditional memory models when applied to rich, realistic encoding contexts.

### The Critical Interpretation

We failed to replicate most of what the literature predicts. Age effects are absent (sample too restricted? power too low?). Domain effects collapsed (What = Where, and When is unmeasurable). Paradigm and schema effects are null (weak manipulations? wrong tasks?).

The ICC finding is troubling. If forgetting rate really has 0.05% trait-like variance, it undermines the whole concept of "individual differences in forgetting" that much of memory research assumes. But values this extreme often indicate model problems, not true psychological phenomena.

We may have built an elaborate analysis infrastructure to discover that our task doesn't differentiate much of anything - everyone forgets the same amount, the same way, at the same rate. That's either a profound finding about VR memory or a sign that REMEMVR lacks sensitivity.

### The Balanced Interpretation

Chapter 5 provides solid evidence for:
1. Logarithmic forgetting (validated)
2. Two-phase consolidation pattern (supported, but gradual)
3. IRT superiority for trajectory modeling (supported)
4. When domain measurement failure (important negative finding)

Chapter 5 provides uncertain evidence for:
1. Absence of age effects (null, but could be methodological)
2. Domain/paradigm/schema invariance (null, possibly real)
3. State-like nature of forgetting rate (extreme values warrant skepticism)

Chapter 5 raises unresolved questions:
1. Why are ICC values so extreme?
2. What does the homogeneity of results mean for REMEMVR's utility?
3. Are the nulls real or power/design issues?

---

## Remaining Work (13 RQs)

### Ready for Execution (9 RQs)
- 5.1.5: K-means clustering - likely to show intercept-driven clusters (consistent with ICC finding)
- 5.2.6-5.2.7, 5.3.6-5.3.9, 5.4.5-5.4.7: Variance decomposition, purified CTT, clustering by category

### Blocked (4 RQs)
- 5.1.6, 5.2.8: Need GLMM tools (item-level analysis)
- 5.3.5, 5.4.4: Need CTT convergence tools

### Expected Pattern
Given the consistency of findings so far, I expect:
- More null results for category-specific effects
- Clustering driven by intercepts, not slopes
- IRT-CTT divergence to replicate across paradigms/congruence
- No surprises that change the overall story

---

## Recommendations for Thesis Writing

1. **Lead with what's solid:** Logarithmic forgetting, IRT advantages, two-phase pattern
2. **Be transparent about nulls:** Age, domain, paradigm, schema effects not detected - discuss power, design limitations
3. **Flag the ICC problem:** Don't hide that 0.05% ICC is anomalous. Discuss possible explanations, need for replication
4. **When domain as a lesson:** Use as example of how dual-scale reporting prevented misinterpretation
5. **Don't oversell:** "VR homogenizes forgetting" is speculation. "No effects detected" is honest.

---

## Files Referenced

**Completed RQ Summaries:**
- results/ch5/5.1.1/results/summary.md
- results/ch5/5.1.2/results/summary.md
- results/ch5/5.1.3/results/summary.md
- results/ch5/5.1.4/results/summary.md
- results/ch5/5.1.5/results/summary.md
- results/ch5/5.2.1/results/summary.md
- results/ch5/5.2.2/results/summary.md (via archive)
- results/ch5/5.2.3/results/summary.md (via archive)
- results/ch5/5.2.4/results/summary.md
- results/ch5/5.3.1/results/summary.md
- results/ch5/5.3.3/results/summary.md (via archive)
- results/ch5/5.3.4/results/summary.md (via archive)
- results/ch5/5.4.1/results/summary.md
- results/ch5/5.4.2/results/summary.md
- results/ch5/5.4.3/results/summary.md (via archive)

**Key Archives:**
- .claude/context/archive/rq_5.2.2_partial_execution_when_exclusion_consolidation.md
- .claude/context/archive/rq_5.3.3_complete_execution_piecewise_lmm_consolidation.md
- .claude/context/archive/rq_5.3.4_complete_execution_age_paradigm_interaction.md
- .claude/context/archive/rq_5.4.3_complete_execution_age_schema_congruence.md
- .claude/context/archive/validated_irt_settings_complete.md
- .claude/context/archive/rq_5_13_complete_rerun_linlog_model_validation_pipeline.md

**Methodology Documentation:**
- docs/v3/lmm_methodology.md
- docs/v3/project_specific_stats_insights.md

---

## Literature Comparison: How Do Our Findings Stack Up?

**Web search conducted:** 2025-12-03

### What the VR Memory Literature Shows

#### 1. VR-RAVLT Reliability (Most Directly Comparable)

The [VR-RAVLT validation study](https://www.frontiersin.org/journals/aging-neuroscience/articles/10.3389/fnagi.2022.980093/full) found:
- **ACQUISITION ICC = 0.732** (good reliability)
- **RETENTION ICC = 0.321** (marginal reliability)
- **Retroactive Interference ICC = -0.185** (poor, essentially random)

**Comparison to our findings:**
- Our ICC_intercept = 0.606 → **CONSISTENT** with VR-RAVLT acquisition (both ~0.6-0.7)
- Our ICC_slope = 0.0005 → **DRAMATICALLY LOWER** than VR-RAVLT retention (0.32)

This is concerning. Their retention ICC (0.32) is 640× higher than ours (0.0005). Either:
1. REMEMVR genuinely produces more homogeneous forgetting than VR-RAVLT
2. Our 6-day multi-timepoint design measures something different than their 2-3 week retest interval
3. Our slope estimation is compromised by methodological issues

#### 2. Age Effects in VR Memory

[Frontiers age-related VR study](https://frontiersin.org/articles/10.3389/fpsyg.2019.01330/full) found:
- **Seniors performed WORSE in immersive HMD** compared to desktop VR
- Young adults showed stable performance across modalities
- **No null age effects reported** - age differences consistently detected

[Plancher's What-Where-When studies](https://pmc.ncbi.nlm.nih.gov/articles/PMC7417675/) found:
- Older adults "perform worse than young people, particularly in binding scores"
- Age deficits in contextual memory (where/when), but not factual memory (what)
- **Lower performance in HMD conditions** for seniors

**Comparison to our findings:**
- We found **NULL age effects** on forgetting rate across all analyses
- This is **UNUSUAL** - most VR studies detect age differences
- **Possible explanation:** Our desktop VR may scaffold older adults better than HMD systems

However, [one real-world WWW study](https://pmc.ncbi.nlm.nih.gov/articles/PMC4435419/) found:
- "Older people were more likely to not remember any complete WWW combinations" (11/32 vs 3/26)
- BUT: "forgetting across the 30-minute retention interval did not differ by age" (χ²=2.70, p=0.10)
- Individual object/location memory showed **no age differences**

**This partially supports our null finding:** Age may affect binding/retrieval but NOT forgetting rate. We may be measuring the right thing.

#### 3. Individual Differences in Memory Trajectories

[Vandemeulebroecke longitudinal IRT study](https://pmc.ncbi.nlm.nih.gov/articles/PMC5613212/) (N=1,750 elderly, 13.9 years):
- Typical cognitive decline slope: **μ = -0.013 theta/year**
- Individual differences captured via random intercepts and slopes
- **Greater age at baseline → faster decline** (coefficient = -0.049, p < 0.001)

[ScienceDirect review on memory individual differences](https://www.sciencedirect.com/topics/neuroscience/individual-difference-in-memory):
- "Great variability in individual memory performance"
- Longitudinal designs "necessary to disentangle complex developmental patterns"
- "When variance of individual intercepts and slopes are statistically significant, it indicates that individuals reliably differ both in level and rate of change"

**The problem:** Literature expects significant slope variance. We found essentially none. Either:
1. VR memory is genuinely different (homogenized forgetting)
2. Our 6-day window is too short (compare to 13.9 years above)
3. Our sample is too homogeneous (healthy adults 20-70)

#### 4. The Desktop VR vs HMD Question

[Multiple studies](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2019.00050/full) show mixed results:
- "Desktop VR is better than non-ambulatory HMD VR for spatial learning"
- BUT: "Virtual memory palaces in HMD condition provide superior memory recall"
- Age-dependent: Seniors do WORSE in HMD, young adults stable across modalities

**REMEMVR uses desktop VR.** This may explain:
- Why older adults don't show expected deficits (desktop is easier)
- Why individual differences are compressed (less variability in cybersickness, presence)
- Why our results may not generalize to HMD-based assessments

#### 5. Forgetting Rate as Trait vs State

[Sleep-dependent consolidation research](https://pmc.ncbi.nlm.nih.gov/articles/PMC4007033/) shows:
- "Participants who slept exhibited markedly slower forgetting rates"
- Sleep benefit was equivalent across patients and controls
- Individual differences in forgetting emerged during **wakefulness, not sleep**

[Memory consolidation review](https://pmc.ncbi.nlm.nih.gov/articles/PMC4526749/):
- Systems consolidation "renders hippocampus-dependent memories independent of the hippocampus over weeks to years"
- Sleep has "dual role" - both consolidation AND adaptive forgetting

**Implication for our findings:**
- If all our participants had similar sleep patterns (controlled encoding time?), forgetting may be genuinely homogeneous
- The 6-day window may capture primarily the consolidation-stabilized portion (where individual differences are minimal)
- Longer retention (weeks/months) might reveal more slope variance as neural reorganization differs

### Summary: Are Our Results Anomalous?

| Finding | Literature Expectation | Our Result | Assessment |
|---------|------------------------|------------|------------|
| **Logarithmic forgetting** | Ebbinghaus curve | Confirmed | ✅ CONSISTENT |
| **ICC_intercept ~0.6** | 0.60-0.80 | 0.606 | ✅ CONSISTENT |
| **ICC_slope ~0.3-0.5** | 0.30-0.50 | 0.0005 | ❌ **ANOMALOUS** (640× lower) |
| **Age effects on rate** | Present | Absent | ⚠️ MIXED (some studies show null) |
| **Domain differences** | What > Where > When | What = Where | ⚠️ MIXED (binding vs retrieval?) |
| **Two-phase consolidation** | Sharp inflection | Gradual | ⚠️ PARTIAL SUPPORT |

### What This Means for the Thesis

**The ICC_slope finding is the outlier.** Everything else is either consistent with literature or within the range of published findings.

**Three possible framings:**

1. **VR homogenization (speculative but interesting):**
   - Desktop VR's standardized encoding creates uniform consolidation
   - Individual differences compressed by controlled environment
   - REMEMVR measures "pure" forgetting, free from encoding variability

2. **Methodological limitation (more likely):**
   - 4 timepoints insufficient for reliable slope estimation
   - 6-day window too short to detect trait-level differences
   - N=100 marginal for complex random effects
   - Need replication with more timepoints, longer retention

3. **Model specification (possible):**
   - Despite Lin+Log improvement, slope variance may still be underestimated
   - r = -0.97 correlation suggests near-collinearity
   - Bayesian analysis needed to test sensitivity

**Recommendation:** Frame ICC_slope as an open question requiring further investigation, not a definitive finding. The discrepancy with VR-RAVLT (ICC = 0.32 vs 0.0005) is too large to ignore.

---

## Sources from Web Search

### VR Memory Assessment
- [Systematic review of VR memory assessment](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2024.1380575/full) - Frontiers 2024
- [VR-RAVLT validation](https://www.frontiersin.org/journals/aging-neuroscience/articles/10.3389/fnagi.2022.980093/full) - Frontiers 2022
- [Age-related differences in VR](https://frontiersin.org/articles/10.3389/fpsyg.2019.01330/full) - Frontiers 2019
- [VR episodic memory review](https://link.springer.com/article/10.3758/s13423-019-01605-w) - Psychonomic Bulletin & Review

### VR and Aging
- [Plancher VR episodic memory aging](https://pmc.ncbi.nlm.nih.gov/articles/PMC7417675/) - PMC 2020
- [What-Where-When age effects](https://pmc.ncbi.nlm.nih.gov/articles/PMC4435419/) - PMC 2015
- [Immersive vs non-immersive memory](https://pmc.ncbi.nlm.nih.gov/articles/PMC6868024/) - PMC 2019

### Memory Consolidation and Individual Differences
- [Longitudinal IRT cognitive trajectories](https://pmc.ncbi.nlm.nih.gov/articles/PMC5613212/) - PMC 2017
- [Sleep-dependent consolidation and ALF](https://pmc.ncbi.nlm.nih.gov/articles/PMC4007033/) - PMC 2014
- [Memory consolidation review](https://pmc.ncbi.nlm.nih.gov/articles/PMC4526749/) - PMC 2015
- [Individual differences in memory](https://www.sciencedirect.com/topics/neuroscience/individual-difference-in-memory) - ScienceDirect

### Desktop vs Immersive VR
- [Desktop vs HMD spatial learning](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2019.00050/full) - Frontiers 2019
- [VR context and memory retention](https://www.nature.com/articles/s41539-022-00147-6) - Nature Scientific Learning 2022

---

## Deep Investigation: Why Can't We Detect Individual Slope Differences?

**Investigation Date:** 2025-12-03
**Status:** COMPLETE - Root causes identified

### The Core Problem

The ICC_slope = 0.0005 (0.05%) finding contradicts decades of memory literature showing ICC_slope = 0.30-0.50. After extensive investigation, we identified **multiple compounding issues** that explain this anomaly.

### Investigation 1: Scale Transformation (Theta → Probability)

**Hypothesis:** Literature uses proportion correct (bounded 0-1), we use IRT theta (unbounded). The nonlinear logit transformation may compress individual differences.

**Method:** Converted theta to probability via Test Characteristic Curve (TCC), re-fit LMM on probability scale.

**Result:**

| Scale | ICC_slope |
|-------|-----------|
| Theta (original) | 0.0005 |
| Probability (TCC) | 0.0017 |

**Verdict:** Scale transformation explains only 3.5× improvement. ICC still 200× below literature. **NOT the primary cause.**

### Investigation 2: Model Specification (Wrong Random Slope Variable)

**Discovery:** The Lin+Log model had random slopes on `Days`, not `log_TSVR`. Since the Log model is best by AIC, random slopes should be on the log-transformed time variable.

**Result with corrected specification:**

| Model | var_slope | ICC_slope |
|-------|-----------|-----------|
| Lin+Log with Days slopes | 0.000157 | 0.0005 |
| Lin+Log with log_TSVR slopes | 0.003346 | 0.011 |

**Verdict:** Correct specification improves ICC by 22×. Still far below literature (0.30-0.50). **Partial explanation.**

### Investigation 3: Shrinkage from Sparse Design

**The critical finding:** With only 4 timepoints per participant, individual slopes are estimated with massive uncertainty. The LMM correctly recognizes this and **shrinks** estimates toward the population mean.

**Quantified shrinkage:**

| Metric | Raw OLS | LMM BLUP | Shrinkage |
|--------|---------|----------|-----------|
| Slope SD | 0.209 | 0.017 | **92%** |
| Slope variance | 0.044 | 0.003 | **93%** |

The model shrinks slope variance by 93%! This is **not bias** - it's the LMM correctly handling unreliable estimates.

**Reliability of individual slopes:**
- With n=4 timepoints, df for slope estimation = 2
- Measurement error variance = 0.021
- Observed slope variance = 0.044
- **Estimated reliability = 51%** (at best)
- With some calculations: reliability as low as **14%**

**What this means:** Half or more of the apparent "individual slope differences" in raw data is measurement error. The LMM correctly downweights these unreliable estimates.

### Investigation 4: Likelihood Ratio Test for Random Slopes

**Critical test:** Do random slopes significantly improve model fit?

```
Full model (intercepts + slopes): LL = -429.65
Reduced model (intercepts only): LL = -430.02
LR statistic = 0.76, p = 0.685
```

**Verdict:** Random slopes do NOT significantly improve fit. The simpler random-intercepts-only model is preferred (lower AIC: 870.05 vs 873.29).

**This means:** The data itself doesn't support the existence of meaningful individual differences in forgetting rates. You cannot detect slope variance that isn't there.

### Investigation 5: Time-Varying Covariates (Sleep, Tiredness)

**Hypothesis:** If we reduce within-person residual variance by adding covariates, ICC_slope might increase.

**Variables tested:**
- Hours slept (before each test)
- Tiredness rating (at each test)
- Sleep quality (at each test)

**Result:**

| Model | var_residual | ICC_slope |
|-------|--------------|-----------|
| Without sleep covariates | 0.3106 | 0.0107 |
| With sleep covariates | 0.3104 | 0.0104 |

**Fixed effects of sleep:**
- hours_slept: b = 0.023, t = 0.70 (NOT significant)
- tiredness: b = -0.044, t = -0.44 (NOT significant)

**LR test for random slopes after adding covariates:** p = 0.694 (still not significant)

**Verdict:** Sleep variables explain essentially 0% of within-person variance. Random slopes remain non-significant. **Covariates do not help.**

### Investigation 6: Model Comparison (Beyond 5 Candidates)

Tested additional functional forms:

| Model | AIC | ΔAIC | ICC_slope |
|-------|-----|------|-----------|
| Quad+Log | 872.92 | 0.00 | 0.012 |
| Lin+Log | 873.29 | 0.37 | 0.011 |
| Log(days+1) | 873.71 | 0.79 | ~0 (boundary) |
| Exp decay (τ=3d) | 873.78 | 0.85 | ~0 (boundary) |
| Power -0.2 | 891.04 | 18.11 | 0.317 |
| Power -0.3 | 896.85 | 23.93 | 0.215 |

**Observation:** Power law models (-0.2, -0.3) show higher ICC_slope (0.22-0.32) but fit much worse (ΔAIC > 18). The models that fit well all show ICC_slope ≈ 0.01 or boundary estimates.

**Verdict:** No well-fitting model shows substantial slope variance.

### Summary: The Truth About ICC_slope

**The finding is NOT an artifact of:**
- ❌ Scale (theta vs probability) - only 3.5× improvement
- ❌ Model specification (after correction) - only 22× improvement
- ❌ Sleep/state covariates - no effect

**The finding IS explained by:**
- ✅ **Sparse design:** 4 timepoints → 14-51% reliability for slopes
- ✅ **Appropriate shrinkage:** LMM correctly downweights unreliable estimates
- ✅ **LR test:** Random slopes don't improve model fit (p = 0.69)
- ✅ **Raw data:** Even unshrunk, raw ICC = 0.12 (still below literature 0.30-0.50)

### What This Means for the Thesis

**You CANNOT claim:**
- "People don't differ in forgetting rates" (design lacks power to detect)
- "VR memory has homogeneous forgetting" (unfalsifiable with this design)
- "Forgetting is a universal process" (overgeneralization)

**You CAN claim:**
- "This design was optimized for group-level trajectory modeling, not individual slope estimation"
- "ICC for intercepts (0.57) confirms reliable between-person baseline differences"
- "Random slopes did not improve model fit, though this may reflect insufficient timepoints (n=4) rather than absence of true differences"
- "Future studies with more intensive longitudinal sampling are needed to characterize individual forgetting rates"

### The Honest Framing

**Old narrative (invalid):** "We'll find individual differences in forgetting rates and explain them with cognitive/demographic predictors"

**New narrative (supported by data):** "VR episodic memory shows strong individual differences in *baseline ability* (ICC = 0.57) but the current design cannot reliably estimate *individual forgetting rates*. With only 4 timepoints per participant, slope reliability is too low for meaningful individual-level trajectory analysis. Group-level findings (logarithmic forgetting, consolidation patterns) are robust; individual-level slope claims require more intensive designs."

### Recommendation: Do NOT Report ICC_slope

Instead:
1. Report **fixed effects** (population-level forgetting curve) - well-powered, robust
2. Report **ICC_intercept** (0.57) - reliable individual differences in baseline
3. Note in limitations: "Individual forgetting rates could not be reliably estimated with 4 timepoints per participant"
4. Recommend future work: "Intensive longitudinal designs (8+ timepoints) needed for individual trajectory analysis"

### The One Hope: Confidence Data

**Type 3 data (confidence ratings)** may reveal individual slope differences that accuracy cannot:
- Confidence is continuous (1-5 scale), not dichotomous
- Each item provides 5× more information than 0/1 accuracy
- Higher reliability → less shrinkage → more slope variance detectable
- If confidence shows ICC_slope ≈ 0.30 while accuracy shows 0.01, this points to accuracy measurement limitation

**This should be investigated in Chapter 6.**

### Information Loss from Dichotomous Data

**Additional factor:** Dichotomous (0/1) accuracy data has inherent limitations:

| Metric | Value |
|--------|-------|
| Items per test | 68 (after purification) |
| Binomial SE of sum score | 3.17 items |
| Binomial SE of change score | 4.49 items |
| Observed SD of T1→T4 change | 10.28 items |
| Signal-to-noise ratio | 2.29 |
| Reliability of change scores | 81% maximum |

Even with perfect analysis, dichotomous data limits slope reliability to ~80%. Continuous data (confidence) would have 5-10× better signal-to-noise.

---

**End of Investigation Section**

**Bottom line:** The ICC_slope anomaly is primarily a design limitation (4 timepoints), not a biological finding or analysis error. The thesis should not attempt to interpret individual forgetting rate differences from this data.
