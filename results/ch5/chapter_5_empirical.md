# Chapter 5: Empirical Results

## 5.0 Introduction

[TBD: 300-500 words]

The REMEMVR study investigated episodic memory forgetting in immersive virtual reality across a 6-day retention interval. This chapter presents empirical findings from 35 research questions organized into five thematic sections corresponding to theoretical questions about forgetting dynamics.

**Core Research Questions:**

1. **§5.1 - Functional Form of Forgetting:** What mathematical function describes memory decline over time? Do individuals differ in forgetting trajectories?

2. **§5.2 - Domain-Specific Patterns:** Do What (object identity), Where (spatial location), and When (temporal order) memory domains follow different forgetting trajectories?

3. **§5.3 - Age and Cognitive Predictors:** Does forgetting accelerate with age? Do baseline cognitive abilities predict memory performance?

4. **§5.4 - Encoding Factors:** Do schema congruence, object salience, and task demands influence memory formation and retention?

5. **§5.5 - Consolidation and Sleep:** Do sleep quality and consolidation intervals moderate forgetting?

**Methodological Note:** Statistical methods are detailed in Chapter 4 (Analysis). This chapter focuses on empirical patterns and theoretical interpretation. Cross-references to Chapter 4 (§4.X.X) indicate relevant methodological sections.

**Sample:** N = 100 healthy adults aged 20-70 years (n = 10 per 5-year age band). Four test sessions: T1 (~1 hour post-encoding), T2 (~1 day), T3 (~3 days), T4 (~6 days). Memory assessed via IRT-calibrated theta scores (see §4.2 for calibration procedures).

**Organization:** Research questions nested within thematic sections. Each RQ reports: research question, hypothesis, brief analysis summary with Chapter 4 cross-references, results narrative integrating statistics, and figures with publication-quality captions.

---

## 5.1 Functional Form and Individual Differences in Forgetting Trajectories

[TBD: Section introduction 150-200 words]

The functional form of forgetting trajectories reveals underlying memory mechanisms. Linear forgetting implies constant-rate trace decay. Logarithmic forgetting (Ebbinghaus, 1885) implies rapid initial decline followed by asymptotic stabilization, consistent with consolidation processes. Power-law forgetting (Wixted & Ebbesen, 1991) implies time-scale invariance. Distinguishing among functional forms has theoretical implications for memory consolidation, retrieval dynamics, and clinical assessment.

This section examines: (1) which functional form best approximates aggregate forgetting (§5.1.1), (2) whether functional form varies by age (§5.1.2), (3) whether individuals differ in forgetting rates (§5.1.3), and (4) whether random slopes improve model fit (§5.1.4-5.1.7).

---

### 5.1.1 Functional Form of Forgetting Trajectories

**Research Question:** Which functional form best describes episodic forgetting across a 6-day retention interval?

**Hypothesis:** Logarithmic model will provide best fit, consistent with Ebbinghaus (1885) forgetting curve.

**Analysis:** (§4.2.2, §4.3.2)
- Sample: N = 100, 400 observations
- IRT: 2-pass GRM purification, 68/105 items retained (see §4.2.2)
- LMM: 5 candidate models compared via AIC (see §4.3.2)

**Results:**

The logarithmic model provided the best fit to forgetting trajectories (AIC = 873.71, Akaike weight = 0.48), with the Linear+Logarithmic model highly competitive (AIC = 874.55, ΔAIC = 0.84, weight = 0.32). Combined, these two logarithmic-based models accounted for 79.9% of the evidence. In stark contrast, the linear model severely underperformed (AIC = 905.54, ΔAIC = 31.83, weight < 0.001), decisively rejecting constant-rate trace decay theory.

Memory ability declined 1.18 standard deviations over 6 days (Day 0: θ = 0.67, 95% CI [0.50, 0.84]; Day 6: θ = -0.51, 95% CI [-0.68, -0.34]). This decline was non-uniform: rapid initial forgetting (Day 0→1: 0.55 SD decline) transitioned to gradual asymptotic approach (Day 3→6: 0.25 SD decline), the hallmark pattern of logarithmic forgetting. Translating to probability scale, recall accuracy dropped from 68% (Day 0) to 38% (Day 6), a 30 percentage point decline. By Day 6, performance approached chance levels (38% vs 33% for 3-option forced choice), suggesting floor effects limit diagnostic utility beyond 6-day retention.

The moderate Akaike weight for the best model (48%) indicates model uncertainty. Burnham & Anderson (2004) recommend model averaging when best model weight falls below 0.90. The competitive performance of the Linear+Logarithmic model suggests both logarithmic and linear components may contribute to forgetting dynamics, potentially approximating power-law forgetting (Wixted & Ebbesen, 1991) which was not directly tested.

An unexpected finding emerged during IRT purification: 27 of 37 excluded items (73%) were temporal order items (When domain: IFR-O, ICR-O, IRE-O, TCR-O tags), primarily excluded for low discrimination (a < 0.4). This suggests temporal memory may have lower signal-to-noise ratio in VR episodic memory tasks, potentially due to fewer naturalistic temporal cues or participant reliance on guessing strategies for temporal order judgments. Domain-specific analyses (§5.2) further investigate this pattern.

**Theoretical Implications:** REMEMVR replicates the classic Ebbinghaus forgetting curve in immersive VR episodic memory tasks, validating the paradigm for longitudinal cognitive assessment. The 1.18 SD decline represents a large effect size (Cohen's d > 0.8) directly comparable to meta-analytic estimates in the episodic memory literature. The rapid early forgetting followed by asymptotic stabilization indicates consolidation processes operating within the first 24 hours, consistent with two-stage memory consolidation theory (Hardt et al., 2013). The decisive rejection of the linear model (ΔAIC = 31.83) confirms that simple trace decay theory cannot account for the non-linear dynamics of episodic forgetting.

**Limitations:** The omnibus IRT factor aggregating What/Where/When domains may obscure domain-specific differences in functional form (§5.2 addresses this). The 6-day retention interval may be too short to definitively distinguish logarithmic from power-law forgetting, which requires longer time scales. IRT convergence warnings in Pass 1 calibration and missing standard error estimates introduce uncertainty in theta score precision. No practice effect control was implemented; repeated testing across four sessions may induce retrieval practice effects that counteract forgetting, conflating the observed trajectory.

**Figure 5.1.1:** [results/ch5/5.1.1/plots/step07_trajectory_functional_form.png](results/ch5/5.1.1/plots/step07_trajectory_functional_form.png)

*Episodic memory forgetting trajectories across 6-day retention interval, shown on dual scales (N = 100, 400 observations). **Left panel (Theta Scale):** Memory ability (IRT-derived theta estimates) declined logarithmically from θ = 0.67 (Day 0, 95% CI [0.50, 0.84]) to θ = -0.51 (Day 6, 95% CI [-0.68, -0.34]), representing 1.18 SD total decline. Blue points show observed means with 95% confidence intervals. Steeper decline Day 0→1 (0.55 SD) than Day 3→6 (0.25 SD) is characteristic of logarithmic forgetting. **Right panel (Probability Scale):** Corresponding recall probabilities dropped from 68% (95% CI [0.63, 0.73]) to 38% (95% CI [0.33, 0.43]), a 30 percentage point decline. Orange points show observed performance with 95% CIs. Error bars widen over time, indicating increased individual variability at longer retention intervals. Annotation indicates best model: Logarithmic (AIC = 873.7, Akaike weight = 0.48). Both scales show identical logarithmic curvature, confirming non-linear forgetting dynamics predicted by Ebbinghaus (1885).*

---

### 5.1.2 Two-Phase Forgetting: Rapid Initial Decline vs Gradual Asymptote

**Research Question:** Do episodic memory data support a two-phase model with rapid initial decline (Day 0-1) followed by slower decay (Day 1-6)?

**Hypothesis:** Forgetting exhibits two distinct phases: rapid pre-consolidation decline (Day 0-1) followed by slower post-consolidation decay (Day 1-6), evidenced by (1) significant positive quadratic term, (2) piecewise model outperforming continuous model (ΔAIC < -2), and (3) Late/Early slope ratio < 0.5.

**Analysis:** (§4.3.1, §4.3.2)
- Sample: N = 100, 400 observations
- Triangulation strategy: Three convergent tests (quadratic term, AIC comparison, slope ratio)
- Bonferroni correction: α = 0.003333 (15 RQs in Chapter 5)

**Results:**

Three convergent tests provided mixed but interpretable evidence for two-phase forgetting. Test 1 (quadratic term) strongly supported deceleration: Time² coefficient = 0.000054, highly significant (p < 0.001, well below Bonferroni α = 0.0033), indicating forgetting rate slows over time. Test 3 (slope ratio) provided very strong support: Late forgetting (48-240 hours) was only 16% as fast as Early forgetting (0-48 hours), with Late/Early ratio = 0.161 << 0.5 threshold and interaction p < 0.000002. However, Test 2 (model comparison) was neutral: piecewise model AIC = 873.31 vs continuous quadratic AIC = 873.24 (ΔAIC = -0.40), indicating both models fit equally well.

Early segment showed rapid decline (slope = -0.432 theta/day, 95% CI [-0.572, -0.292]), while Late segment showed much slower decline (slope = -0.070 theta/day, 95% CI [-0.121, -0.018]). This 6.2-fold difference in forgetting rate indicates dramatically different dynamics across consolidation windows. The Late forgetting rate represents only 16% of the Early rate, providing strong quantitative support for phase differentiation.

**Theoretical Implications:** Results support the existence of two-phase forgetting dynamics but suggest continuous consolidation processes rather than discrete phase transitions. The pattern aligns with continuous consolidation models (Wixted & Ebbesen, 1991) where memories undergo graded stabilization over days, producing smooth deceleration rather than sharp inflection at 48 hours. Alternative explanations include Multiple Trace Theory (Nadel & Moscovitch, 1997) proposing episodic traces remain hippocampal-dependent but strengthen gradually through reactivation, or extended systems consolidation timescales (Frankland & Bontempi, 2005) where cortical integration requires days to weeks beyond initial sleep-dependent consolidation.

**Critical Limitation:** Cannot distinguish consolidation-driven deceleration from repeated testing effects. Four test sessions (Days 0, 1, 3, 6) may induce retrieval practice effects that strengthen memories over time, counteracting forgetting and producing apparent deceleration. Without no-test control group, the observed two-phase pattern may reflect testing artifact rather than genuine consolidation dynamics.

**Assumption Violations:** Both quadratic and piecewise models failed homoscedasticity (p = 0.031, 0.049) and autocorrelation tests (ACF = -0.22), potentially inflating Type I error rates. However, primary effects remained highly significant (p < 0.001), suggesting conclusions robust despite violations.

**Figure 5.1.2:** [results/ch5/5.1.2/plots/piecewise_comparison.png](results/ch5/5.1.2/plots/piecewise_comparison.png)

*Comparison of continuous vs piecewise forgetting models (N=100, 400 observations). **Left panel:** Quadratic model shows smooth continuous deceleration from θ ≈ +0.6 (encoding) to θ ≈ -0.5 (Day 6), with red curve and pink 95% CI band. No visible inflection point—smooth concave-up curvature throughout. **Right panel:** Piecewise model shows discrete phase transition at 48 hours (vertical dashed gray line). Blue segment (Early, 0-48h): steep negative slope (θ drops from +0.66 to -0.21). Green segment (Late, 48-240h): shallow negative slope (θ drops from -0.20 to -0.76 over 4× longer duration). Black points with error bars show observed means at 4 test sessions. Both models fit observed data equally well (confidence bands contain all observations), explaining neutral AIC comparison (ΔAIC = -0.40). Visual inspection reveals why triangulation is partial: deceleration pattern exists (supports Test 1 and Test 3), but data do not demand sharp inflection over smooth curve (explains Test 2 neutrality). Plot demonstrates that forgetting exhibits two-phase dynamics regardless of modeling approach, but underlying mechanism (gradual vs abrupt transition) remains ambiguous.*

---

### 5.1.3 Age Effects on Baseline Memory and Forgetting Rate

**Research Question:** Do older adults show lower baseline episodic memory (intercept) and/or faster forgetting (steeper slope) compared to younger adults?

**Hypothesis:** Age will negatively predict both intercept and slope, consistent with hippocampal aging effects (Raz et al., 2005) and dual deficit hypothesis (Nyberg et al., 2012).

**Analysis:** (§4.3.1)
- Sample: N = 100, 400 observations, age range 20-70 years (M = 44.57, SD = 14.52)
- Model: Theta ~ (Time + log(Time+1)) × Age_c + (Time | UID)
- Predictor: Age_c (grand-mean centered)
- Bonferroni correction: α = 0.0167 (3 age-related tests)

**Results:**

Age effects on forgetting trajectories were minimal and non-significant after correction. Age showed marginal negative effect on baseline memory (β = -0.012, p = 0.061 uncorrected, p = 0.182 Bonferroni), suggesting weak baseline disadvantage for older adults that failed to reach significance. Critically, both Age × Time interactions were near-zero and non-significant: linear interaction β = 0.000015 (p = 0.831), logarithmic interaction β = 0.001 (p = 0.761). Effect sizes were trivial: comparing average-aged adults (44.6 years) to +1 SD older adults (59.1 years) revealed only 0.098 theta unit difference at Day 6 (Cohen's d ≈ 0.10, far below predicted d = 0.2-0.5).

**Critical Anomaly:** Both slope interactions were positive (older adults appeared to forget slower), contradicting four decades of hippocampal aging literature. This wrong-direction effect likely reflects practice effect confound: younger adults may benefit more from repeated testing (steeper learning curves), making their trajectories appear as "faster forgetting resistance" relative to older adults. If younger adults show larger practice gains across the four test sessions, their net trajectory (forgetting minus practice) appears shallower than genuinely declining older adults. Meta-analytic evidence documents mean retest effects ~0.60 SD in longitudinal memory studies, sufficient to mask age-related forgetting differences.

Alternative explanations include sample selection bias (healthy older participants aged 50-70 may represent "super-agers" with above-average cognitive function, while younger participants 20-30 include full ability range), VR contextual scaffolding equalizing forgetting across ages through rich environmental cues, or IRT theta scaling artifacts where latent ability estimates remove age-related variance by accounting for item difficulty.

**Recommendation:** Analyze T1-T2 only (first retest, minimal practice) to test practice confound hypothesis, and compare raw accuracy vs theta scores to test IRT artifact hypothesis.

**Figure 5.1.3:** [results/ch5/5.1.3/plots/age_tertile_trajectory.png](results/ch5/5.1.3/plots/age_tertile_trajectory.png)

*Age tertile forgetting trajectories with LMM predictions (N=100, 400 observations). Scatter plot shows individual observations colored by age tertile: green (Young, 20-38 years, N=33), orange (Middle, 38-55 years, N=34), red (Older, 55-70 years, N=33). Dashed lines show LMM predictions for each tertile. High scatter within each age group (theta range spans ~4 units) with substantial overlap across tertiles throughout retention interval (0-250 hours). No clear vertical separation between age groups (contrast with domain-specific RQ 5.2 where What/Where/When showed clear ordering). LMM prediction lines show anomalous patterns: Young (green) shows counterintuitive upturn after 100h, Middle (orange) shows extreme dip to θ ≈ -2.3 (beyond observed data range), suggesting prediction instability from near-zero Age × Time interactions. Visual inspection corroborates statistical conclusion: individual variability dominates age-related variance, producing null age effects on forgetting rate.*

---

### 5.1.4 Individual Differences in Forgetting Rate: Trait vs State

**Research Question:** What proportion of variance in forgetting rate (slopes) is between-person (stable trait) vs within-person (measurement error)?

**Hypothesis:** ICC_slope > 0.40, indicating forgetting rate is a stable trait-like individual difference.

**Analysis:** (§4.3.1, §4.4.2)
- Sample: N = 100, 400 observations
- Method: Variance decomposition of LMM random effects with ICC computation
- Model: Lin+Log model from RQ 5.1.1 with random intercepts + random slopes

**Results:**

Forgetting rate showed minimal stable individual differences, decisively rejecting the trait hypothesis. ICC_slope = 0.0005 (0.05%), falling 800× below the 40% threshold. In stark contrast, baseline memory showed high trait stability (ICC_intercept = 60.6%), creating a 1,212× asymmetry between intercept and slope individual differences. Variance decomposition revealed random slope variance (σ² = 0.000157, SD = 0.0125 theta units) was 47× smaller than random intercept variance (σ² = 0.476, SD = 0.690 theta units). This indicates 99.95% of slope variance is within-person (situational factors, measurement error), with only 0.05% between-person (stable trait).

Random slopes spanned narrow range [-0.0103, +0.0128], representing only 2.1% coefficient of variation around the population mean forgetting rate (β = -0.591 theta/day). The intercept-slope correlation was very strong and negative (r = -0.973, p < 0.001 after Bonferroni), indicating participants with higher baseline ability showed slower forgetting rates, maintaining their advantage over time. This magnitude (r = -0.973) implies 94.7% of slope variance is predicted by intercepts, leaving only 5.3% independent variation in forgetting rate beyond baseline differences.

**Theoretical Implications:** Results contradict trait models of memory decline—forgetting rate is primarily state-dependent (situational/measurement factors) rather than trait-like in healthy young adults using VR episodic memory. The 47:1 asymmetry between baseline ability and forgetting rate variability suggests episodic memory assessment should focus on encoding efficiency (highly stable individual difference) rather than forgetting dynamics (minimal stable variance). The very strong negative intercept-slope correlation (r = -0.973) suggests forgetting rate may not be independent cognitive construct but rather reflects baseline ability, aligning with cognitive reserve theories where better encoding produces more durable traces.

**Critical Caveat:** Findings may reflect methodological constraints (4 timepoints, 6-day retention, homogeneous sample, young age) rather than true biological absence of forgetting rate variability. Replication needed with longer retention (28-90 days), more timepoints (6-8 sessions), and clinically diverse samples (MCI, dementia) where pathological forgetting may show greater individual differences.

**Figure 5.1.4:** [results/ch5/5.1.4/plots/step05_random_slopes_histogram.png](results/ch5/5.1.4/plots/step05_random_slopes_histogram.png)

*Distribution of random slopes showing individual differences in forgetting rate (N=100). Histogram with normal distribution overlay (red curve, mean=0.0000, SD=0.0045) and mean reference line (black dashed). Random slopes span narrow range (-0.010 to +0.013), approximately normally distributed with slight positive skew (more participants with slower-than-average forgetting). Visual confirms Lin+Log model improvement: slope range expanded 42-fold from Log-only model (±0.0007 to ±0.013), but distribution remains very narrow compared to intercepts. ICC_slope = 0.05% indicates this variance is minimal relative to within-person error. Population mean forgetting rate β = -0.591 theta/day; individual variation (SD = 0.0125) represents only 2.1% coefficient of variation. Q-Q plot (not shown) demonstrates strong linearity with minor lower-tail deviation and one upper-tail outlier at +2.7 SD, validating LMM normality assumption.*

---

### 5.1.5 Latent Class Analysis: Forgetting Trajectory Profiles

**Research Question:** Can participants be grouped into latent classes based on their forgetting trajectories (intercepts and slopes)?

**Hypothesis:** Exploratory analysis expecting 2-3 profiles: (1) High baseline/slow forgetting, (2) Average baseline/average forgetting, (3) Low baseline/fast forgetting.

**Analysis:** (§4.3.1)
- Sample: N = 100, derived from RQ 5.1.4 random effects
- Method: K-means clustering on standardized random intercepts and slopes
- Model selection: BIC with elbow method remediation (boundary issue at K=6)
- Validation: Bootstrap stability (100 iterations), silhouette coefficient

**Results:**

K-means clustering identified two distinct trajectory profiles with strong separation and stability. Optimal K=2 selected via elbow method after BIC showed boundary minimum at K=6 (conservative remediation). Cluster 0 ("Resilient Memory", N=69, 69%) showed high baseline (intercept = 1.01, ~1 SD above mean) with slower change rate (slope = 0.074). Cluster 1 ("Vulnerable Memory", N=31, 31%) showed near-zero baseline (intercept = -0.04) with faster change rate (slope = 0.082), representing 11% faster change than Cluster 0.

Bootstrap validation demonstrated robust stability (mean Jaccard = 0.929, 95% CI [0.785, 1.000]), well exceeding the 0.75 threshold. Silhouette coefficient = 0.594 indicated strong cluster structure (≥0.50 threshold), confirming participants were 59% closer to their own cluster centroid than to the nearest other cluster. Standardized cluster centers showed clear diagonal separation: Cluster 0 at (Intercept_z = 0.553, Slope_z = -0.541) vs Cluster 1 at (Intercept_z = -1.232, Slope_z = 1.204), revealing compensatory pattern where low-baseline participants show faster change.

**Hypothesis Status:** Partially supported. Optimal K=2 fell within predicted 2-3 range, but only two profiles emerged (high/slow and low/fast) rather than three distinct groups. The absence of "average" profile suggests bimodal rather than trimodal distribution, potentially reflecting discrete biological or cognitive mechanisms (e.g., high vs low cognitive reserve, effective vs ineffective encoding strategies).

The negative correlation between intercept_z and slope_z suggests compensatory mechanism: participants starting with low baseline show faster change (potentially improving from poor start via practice effects), while high-baseline participants show slower change (maintaining advantage). This aligns with cognitive reserve theories and converges with RQ 5.1.4 finding (r = -0.973 intercept-slope correlation).

**Figure 5.1.5:** [results/ch5/5.1.5/plots/cluster_scatter.png](results/ch5/5.1.5/plots/cluster_scatter.png)

*K-means cluster scatter plot showing two distinct forgetting trajectory profiles (N=100). Axes show z-scored random effects: X-axis = Random Intercept (baseline memory), Y-axis = Random Slope (change rate). Dashed gray lines at (0,0) represent population means. Cluster 0 (coral/red, N=69) occupies lower-right quadrant with center at (0.55, -0.54): above-average baseline, below-average change rate. Cluster 1 (blue, N=31) occupies upper-left quadrant with center at (-1.23, 1.20): below-average baseline, above-average change rate. Clear diagonal separation with minimal overlap. Black stars mark cluster centers. Silhouette = 0.594 displayed (strong structure ≥0.50). Visual confirms statistical quality metrics: distinct "clouds" validate K=2 selection, Cluster 0's compact pattern vs Cluster 1's dispersion matches SD differences, diagonal separation demonstrates compensatory profile (low baseline → faster change). No participants in inconsistent quadrants (e.g., high baseline + fast change), supporting bimodal interpretation.*

---

## 5.2 Domain-Specific Forgetting Patterns

Episodic memory comprises multiple information dimensions: object identity (What), spatial location (Where), and temporal order (When). Dual-process theories propose these domains rely on dissociable neural substrates—object memory supported by perirhinal cortex via familiarity-based retrieval, spatial and temporal memory supported by hippocampus via recollection-based retrieval (Yonelinas, 2002). If domains dissociate neurally, they should show differential forgetting trajectories, consolidation dynamics, and age vulnerability. This section examines domain-specific patterns across seven research questions: baseline differences (§5.2.1), consolidation effects (§5.2.2), age interactions (§5.2.3), measurement convergence (§5.2.4-5.2.5), individual differences (§5.2.6), and latent profiles (§5.2.7).

**Critical Note:** When domain (temporal order) showed severe floor effects in initial analysis (6-9% performance, 77% item exclusion, only 6/26 items retained after IRT purification). Subsequent analyses focus on What vs Where comparisons only, limiting conclusions about temporal memory.

---

### 5.2.1 Domain-Specific Forgetting Trajectories

**Research Question:** Are there domain-specific differences in the rate and pattern of episodic forgetting over 6 days?

**Hypothesis:** Object identity (What) may be more resilient than spatial (Where) or temporal (When) memory, consistent with dual-process theories suggesting familiarity-based information is less hippocampus-dependent than contextual details.

**Analysis:** (§4.2.2, §4.3.2)
- Sample: N = 100, 1,200 observations (3 domains × 4 sessions)
- IRT: 3-dimensional GRM, 70/105 items retained (What 65.5%, Where 90.0%, When 23.1%)
- LMM: Logarithmic model (best fit, AIC = 3187.96, weight = 0.619)
- Bonferroni correction: α = 0.0167 (3 pairwise comparisons)

**Results:**

What and Where domains showed overlapping trajectories with no significant baseline or slope differences (Where-What baseline: β = 0.037, p = 0.722; slope interaction: β = -0.030, p = 0.711). Both declined logarithmically from high baseline (θ ~0.67-0.69 at Day 0) to moderate impairment (θ ~-0.34 to -0.48 at Day 6), representing 1.03-1.15 SD declines. On probability scale, What declined 16 percentage points (88%→72%), Where declined 23 percentage points (61%→38%), both remaining above chance by Day 6.

When domain showed catastrophic measurement failure: only 6/26 items retained (23% retention), with 20 items excluded for low discrimination (a < 0.4). Performance remained at floor throughout study (θ ~0.20 at baseline, declining to -0.11 at Day 6; probability 9%→6%, essentially at 0% floor). This domain is unmeasurable in current VR paradigm and excluded from subsequent domain analyses.

Post-hoc contrasts confirmed When domain differed significantly from both What (β = -0.415, p < 0.001 Bonferroni) and Where (β = -0.452, p < 0.001 Bonferroni), but What-Where comparison was non-significant (p = 0.722), indicating functional equivalence of object and spatial forgetting trajectories.

**Theoretical Implications:** Results challenge domain dissociation predictions. What and Where trajectories overlap completely, suggesting VR episodic memory engages unified encoding rather than dissociable perirhinal (What) vs hippocampal (Where) systems. When domain failure may reflect task design issues (insufficient temporal cues, guessing strategies) rather than genuine memory impairment, requiring paradigm redesign for future work.

**Figure 5.2.1:** [results/ch5/5.2.1/plots/trajectory_probability.png](results/ch5/5.2.1/plots/trajectory_probability.png)

*Domain-specific forgetting trajectories on probability scale (N=100, 1,200 observations). Red line (What): 88%→72% decline (16 pp), remaining well above chance. Blue line (Where): 61%→38% decline (23 pp), approaching chance by Day 6. Green line (When): 9%→6% decline at floor throughout study (catastrophic measurement failure, 77% item exclusion). Logarithmic decay pattern visible for What/Where. Error bands widen over time. When domain floor effect reveals task inadequacy for temporal memory assessment.*

---

### 5.2.2 Domain-Specific Consolidation Effects

**Research Question:** Do memory domains (What/Where) show different rates of forgetting during early consolidation window (Day 0→1) versus later decay (Day 1→6)?

**Hypothesis:** Sleep-dependent consolidation (Day 0→1, including one night's sleep) may benefit spatial memory (Where) more than semantic (What), based on hippocampal replay theories.

**Analysis:** (§4.3.1, §4.3.2)
- Sample: N = 100, 800 observations (2 domains × 4 sessions; When excluded)
- Model: Piecewise LMM with Early (0-48h) and Late (48-240h) segments
- Bonferroni correction: α = 0.0167 (3 planned contrasts)

**Results:**

Both What and Where domains showed robust two-phase forgetting with no differential consolidation benefit. Early segment slopes: What -0.456 theta/day, Where -0.433 theta/day (difference 0.023, p = 0.782). Late segment slopes: What -0.071 theta/day, Where -0.085 theta/day (difference -0.014, p = 0.699). Three-way interaction (Days × Segment × Domain) non-significant (β = -0.037, p = 0.671), indicating parallel consolidation dynamics.

Consolidation benefit indices (|Early slope| - |Late slope|) showed Where = 0.348 vs What = 0.385, representing OPPOSITE direction to hypothesis (Where showed slightly LESS consolidation benefit than What, though difference non-significant with overlapping 95% CIs [0.222, 0.474] vs [0.259, 0.512]). Both domains showed 5-6× steeper forgetting in Early vs Late segments, confirming two-phase pattern, but no domain-specific modulation.

All planned contrasts non-significant (p > 0.68), with negligible effect sizes (Cohen's d < 0.06). Model comparison showed piecewise and continuous models fit equally well (ΔAIC = -0.40), supporting smooth consolidation processes rather than discrete phase transitions.

**Theoretical Implications:** Results contradict hippocampal replay predictions and support domain-general consolidation. Both What (perirhinal-dependent) and Where (hippocampal-dependent) benefit equally from sleep-dependent consolidation, suggesting VR encoding creates integrated object-location bindings that consolidate as unified representations rather than dissociable streams. Converges with RQ 5.2.1 finding of overlapping What-Where trajectories.

**Figure 5.2.2:** [results/ch5/5.2.2/plots/piecewise_trajectory_theta.png](results/ch5/5.2.2/plots/piecewise_trajectory_theta.png)

*Piecewise forgetting trajectories for What (red) and Where (blue) domains (N=100, 800 observations). Both show steep Early segment decline (0-48h: slopes -0.456 and -0.433 theta/day) transitioning to shallow Late segment (48-240h: slopes -0.071 and -0.085 theta/day). Vertical dashed line at 48h marks consolidation boundary. Trajectories nearly parallel throughout retention interval. Clear two-phase pattern visible (steep-then-flat) but no domain differentiation. Visual confirms null 3-way interaction: consolidation benefit domain-general, not spatial-selective.*

---

### 5.2.3 Domain-Specific Age Effects on Forgetting

**Research Question:** Does the effect of age on forgetting rate vary by memory domain (What vs Where)?

**Hypothesis:** Spatial binding (Where) should show greater age-related vulnerability than object identity (What), consistent with hippocampal aging hypothesis (Raz et al., 2005).

**Analysis:** (§4.3.1)
- Sample: N = 100, 800 observations, age range 20-70 years (M = 44.57, SD = 14.52)
- Model: LMM with Age × Domain × Time interaction (3-way test)
- Bonferroni correction: α = 0.025 (2 three-way interactions: linear and log time)

**Results:**

Age effects on forgetting rate did not vary by domain. Both three-way interactions non-significant: TSVR_hours × Age × Where (β = -0.00006, p = 0.495 uncorrected, p = 0.990 Bonferroni), log_TSVR × Age × Where (β = 0.00246, p = 0.438 uncorrected, p = 0.876 Bonferroni). Domain-specific age slopes at Day 3 were nearly identical: What slope = -0.000014, Where slope = 0.000014 (differ only in sign, likely numerical noise).

Main effects also non-significant: Age did not predict overall memory (β = -0.009, p = 0.156), domains did not differ in baseline (Where-What: β = 0.032, p = 0.746), and no 2-way Age × Domain interaction (β = -0.003, p = 0.713). Effect sizes were essentially zero (β magnitudes < 0.003 for all age-related terms).

**Theoretical Implications:** Hippocampal aging hypothesis not supported—age effects on episodic forgetting are uniform across What and Where domains in VR for ages 20-70. Converges with RQ 5.2.2 (domain-general consolidation) and RQ 5.2.1 (overlapping trajectories), suggesting VR may engage unified episodic memory system. Alternative explanations include VR contextual scaffolding equalizing age effects, When domain exclusion limiting test sensitivity (temporal memory most hippocampal-dependent), or sample age range not capturing accelerated decline after age 70.

**Critical Limitation:** Intercepts-only random structure (convergence fix) may underestimate Age × Time effects. However, strong null result (p > 0.4, not borderline) unlikely to change with more complex random effects.

**Figure 5.2.3:** [results/ch5/5.2.3/plots/age_effects_by_domain.png](results/ch5/5.2.3/plots/age_effects_by_domain.png)

*Age tertile trajectories for What and Where domains (N=100, 800 observations). Each panel shows three age groups: Young (green, 20-38y), Middle (orange, 38-55y), Older (red, 55-70y). High scatter and substantial overlap within each domain throughout retention interval (0-250h). No vertical separation by age group in either domain. Visual confirms null 3-way interaction: individual variability dominates age-related variance in both What and Where memory. Contrasts with domain-specific RQ 5.2.1 where What/Where/When showed clear separation.*

---

### 5.2.4 IRT-CTT Convergent Validity

**Research Question:** Do IRT theta scores and CTT mean scores yield the same conclusions about domain-specific forgetting trajectories?

**Hypothesis:** Exploratory. IRT theta and CTT mean scores should converge (r > 0.70 strong threshold) demonstrating robustness of conclusions to measurement approach.

**Analysis:** (§4.2.1, §4.3.1)
- Sample: N = 100, 800 observations (2 domains)
- Comparison: Parallel LMMs with random intercepts and slopes
- Metrics: Pearson correlations, coefficient agreement, random slope variance

**Results:**

Static convergence was exceptional: What domain r = 0.906 (95% CI [0.887, 0.922]), Where domain r = 0.970 (95% CI [0.963, 0.975]), both exceeding 0.90 threshold. Overall correlation r = 0.792 (strong but below 0.90). This indicates both methods measure same latent construct at individual timepoints.

However, dynamic divergence emerged: IRT detected individual differences in forgetting rate (random slope variance = 0.021, SD = 0.145), while CTT showed zero slope variance (boundary estimate). This represents critical methodological divergence—IRT captures trajectory heterogeneity that CTT misses. Coefficient agreement was mixed: 3/4 effects agreed (75% raw agreement, Cohen's κ = 0.500 moderate), with disagreement on domain main effect (IRT: no What-Where difference, p = 0.369; CTT: Where 17 pp lower, p < 0.001).

**Theoretical Implications:** IRT's psychometric sophistication (item difficulty/discrimination weighting) enables detection of individual differences in dynamics (change over time), not just statics (ability at single timepoint). For group-level average trajectories, either method acceptable. For individual-level prediction or clinical screening requiring person-specific forgetting curves, IRT required. Divergence on domain main effect suggests domain comparisons not fully robust to measurement approach.

**Figure 5.2.4:** [results/ch5/5.2.4/plots/scatterplot_irt_ctt.png](results/ch5/5.2.4/plots/scatterplot_irt_ctt.png)

*IRT vs CTT scatterplots by domain (N=100, 800 observations). Left panel (What): r = 0.906, strong linear relationship with moderate scatter. Right panel (Where): r = 0.970, near-perfect linear relationship with tight scatter. Visual confirms exceptional static convergence. Both panels show some ceiling effect at CTT = 1.0. Where domain's tighter scatter explains highest convergence. Regression lines fit well, supporting construct validity: both methods measure same latent ability at individual timepoints.*

---

### 5.2.5 Purified CTT Convergence

**Research Question:** If we compute CTT scores using only IRT-retained items (post-purification), do conclusions differ from full-item CTT?

**Hypothesis:** Purified CTT (using only IRT-retained items) will show higher correlation with IRT theta scores compared to full CTT, demonstrating item purification removes noise rather than signal.

**Analysis:** (§4.2.2)
- Sample: N = 100, 400 observations per domain
- Item retention: What 65.5% (19/29), Where 90.0% (45/50), When 19.2% (5/26)
- Comparison: Steiger's z-test for dependent correlations
- Bonferroni correction: α = 0.0167 (3 domains)

**Results:**

What and Where domains supported hypothesis with significant correlation improvements. What domain: Full CTT-IRT r = 0.879, Purified CTT-IRT r = 0.906 (Δr = +0.027, Steiger's z = 10.06, p < 0.001 Bonferroni). Where domain: Full CTT-IRT r = 0.940, Purified CTT-IRT r = 0.955 (Δr = +0.015, z = 14.22, p < 0.001 Bonferroni). Both showed purification removed measurement noise, improving convergence with IRT.

When domain showed massive correlation improvement (Δr = +0.388, from r = 0.451 to r = 0.838) but non-significant after Bonferroni correction (p = 0.111). Full CTT-IRT correlation catastrophically low (r = 0.451), indicating severe measurement divergence with only 5 items remaining after purification. This domain unreliable regardless of scoring method.

Paradoxical model fit pattern emerged: Full CTT showed best fit (AIC = 2954), IRT intermediate (AIC = 3007), Purified CTT worst (AIC = 3109). This contradicts psychometric predictions and reflects When domain's extreme item imbalance artifact (5 vs 26 items), where balanced coverage (Full CTT) provides more stable domain-level estimates than imbalanced purified pool.

**Hypothesis Status:** Partially supported (domain-dependent). What and Where show purification improves IRT convergence (noise removal confirmed). When domain untestable (catastrophic item loss creates measurement divergence).

**Figure 5.2.5:** [results/ch5/5.2.5/plots/correlation_comparison.png](results/ch5/5.2.5/plots/correlation_comparison.png)

*CTT-IRT correlation comparison by domain (N=100, 1,200 observations). Grouped bar chart: blue bars (Full CTT), orange bars (Purified CTT). What domain: both > 0.70, Purified slightly higher (0.906 vs 0.879, * significant). Where domain: both > 0.90, Purified marginally higher (0.955 vs 0.940, * significant). When domain ANOMALY: Full at 0.451 (catastrophically poor), Purified jumps to 0.838 (dramatic improvement, not significant after Bonferroni). Horizontal reference lines at 0.70 (adequate) and 0.90 (excellent). Visual confirms What/Where purification benefits, When domain instability.*

---

### 5.2.6 Domain-Specific Variance Decomposition

**Research Question:** What proportion of variance in forgetting rate is between-person versus within-person for each memory domain (What, Where)?

**Hypothesis:** Substantial between-person variance (ICC for slopes > 0.40) exists within each domain, indicating forgetting rate is trait-like individual difference rather than measurement noise.

**Analysis:** (§4.3.1, §4.4.2)
- Sample: N = 100, 800 observations (2 domains; When excluded)
- Method: Domain-stratified LMMs with random intercepts and slopes
- ICC computation: Conditional ICC at Day 6 (accounts for intercept-slope correlation)

**Results:**

Both domains showed substantial trait-like variance in outcomes (Day 6 performance), supporting hypothesis. What domain: ICC_slope_conditional = 0.518 (51.8% of Day 6 variance between-person), exceeding 0.40 threshold. Where domain: ICC_slope_conditional = 0.531 (53.1% between-person), also exceeding threshold. Domain difference minimal (1.3 percentage points), indicating functionally equivalent trait stability.

However, ICC paradox emerged: ICC_slope_simple (slope variance alone) was low (<0.02) for both domains, appearing to contradict hypothesis. Resolution: With only 4 timepoints, slope estimates are inherently noisy in isolation, but outcome variance (where participants end after forgetting) shows substantial individual differences when baseline and rate are considered jointly (conditional ICC). This reflects design limitation (short retention, few timepoints) rather than absence of trait-like variance.

Intercept-slope correlations differed by domain: What showed positive trend (r = +0.272, p = 0.006 uncorrected, p = 0.012 Bonferroni, not significant), while Where showed significant negative correlation (r = -0.316, p = 0.001 uncorrected, p = 0.003 Bonferroni, significant). Where domain's negative correlation confirms fan effect: high baseline performers maintain advantage over time. What domain's non-significant positive trend may reflect floor effects or domain-specific encoding mechanisms.

**Theoretical Implications:** Both What and Where memory show substantial trait-like variance in 6-day outcomes (~50% between-person), supporting episodic memory assessment as reliable individual difference measure. Where domain's significant fan effect aligns with hippocampal consolidation theories (better encoding produces more durable traces). What domain's lack of fan effect may suggest perirhinal familiarity-based retrieval less dependent on initial encoding strength.

**Figure 5.2.6:** [results/ch5/5.2.6/plots/domain_icc_barplot.png](results/ch5/5.2.6/plots/domain_icc_barplot.png)

*Domain ICC barplot showing ICC_slope_conditional by domain (N=100). Green bars: What (0.518), Where (0.531). Both exceed horizontal threshold line at 0.40 (substantial reliability). Minimal domain difference (1.3%). When domain excluded (floor effect) noted in annotation. Visual confirms statistical finding: both domains show majority of Day 6 variance is between-person (trait-like individual differences), supporting episodic memory as stable cognitive construct. High absolute ICCs (>0.50) validate theta scores as reliable assessment measures.*

---

### 5.2.7 Domain-Based Latent Class Analysis

**Research Question:** Can participants be grouped into latent classes based on domain-specific forgetting trajectories (What/Where intercepts and slopes)?

**Hypothesis:** Exploratory analysis expecting 2-4 profiles, potentially showing domain-selective impairment patterns (e.g., poor spatial memory only, preserved object memory).

**Analysis:** (§4.3.1)
- Sample: N = 100, derived from RQ 5.2.6 random effects
- Method: K-means clustering on 4 standardized variables (What/Where intercepts and slopes)
- Model selection: BIC minimum at K=5 clusters
- Validation: Bootstrap stability (Jaccard = 0.88), silhouette = 0.34, Davies-Bouldin = 0.98

**Results:**

K-means identified 5 stable but fuzzy clusters. Cluster quality mixed: excellent bootstrap stability (Jaccard = 0.88, 95% CI [0.80, 0.99]), good centroid separation (Davies-Bouldin = 0.98 < 1.0), but poor member cohesion (silhouette = 0.34 < 0.40 threshold). This indicates prototypical profiles rather than discrete categories—cluster assignments stable but boundaries overlap.

Five profiles emerged: (0) Average baseline, slow decline (22%); (1) Average baseline, improving memory (26%, largest cluster with positive slopes); (2) Low baseline, stable What/improving Where (17%, domain-selective recovery); (3) High baseline, stable (21%, superior performers maintaining advantage); (4) Average What/high Where, fast decline (14%, steepest forgetting). Unexpected pattern: largest cluster (26%) showed positive slopes (memory improves over time), suggesting practice/consolidation effects dominate forgetting for substantial proportion.

Domain-specific insights: What domain showed trimodal slope distribution (26% improving, 60% stable, 14% declining), while Where domain showed higher proportion improving (43% vs 26%), suggesting VR spatial encoding benefits more from consolidation. Strong What-Where correlation (r ≈0.7-0.8) contradicts domain independence, supporting unified episodic memory system. Cluster 2 showed domain-selective pattern (improving Where, stable What), providing limited support for dual-process theory.

**Hypothesis Status:** Partially supported. Five clusters identified (more than predicted 2-4), with interpretable domain-specific patterns. However, poor silhouette (0.34) indicates continuous variation may better represent individual differences than discrete profiles. Clustering reveals prototypical forgetting patterns but should not be interpreted as hard categories.

**Figure 5.2.7:** [results/ch5/5.2.7/plots/cluster_scatter_matrix.png](results/ch5/5.2.7/plots/cluster_scatter_matrix.png)

*Cluster scatter plot matrix showing 5 latent profiles (N=100). 4×4 matrix: off-diagonal panels show pairwise scatter plots (What/Where intercepts and slopes), diagonal panels show histograms. Points colored by cluster: dark blue (Cluster 0, average/slow), orange (Cluster 1, improving), green (Cluster 2, low baseline), red (Cluster 3, high baseline), purple (Cluster 4, fast decline). Black X markers show cluster centroids. Visual patterns: strong What-Where positive correlation for both intercepts and slopes (r≈0.7-0.8), fuzzy cluster boundaries with substantial overlap (explains silhouette=0.34), well-distributed centroids (explains Davies-Bouldin=0.98). Cluster 2 (green, bottom-left) most visually distinct. Diagonal histograms show roughly normal intercepts, bimodal slopes. Visual supports dimensional interpretation over discrete categories.*

---

---

## 5.3 Age and Cognitive Predictors of Memory Performance

[TBD: Section introduction]

---

[TBD: RQs 5.3.X will be added here]

---

## 5.4 Encoding Factors and Schema Effects

[TBD: Section introduction]

---

[TBD: RQs 5.4.X will be added here]

---

## 5.5 Consolidation and Sleep-Dependent Memory

[TBD: Section introduction]

---

[TBD: RQs 5.5.X will be added here]

---

## 5.6 Chapter Summary

[TBD: 500-800 words synthesizing across all 35 RQs]

**Major Findings:**

[TBD: Bullet list of 10-12 key results]

**Convergent Evidence:**

[TBD: Where multiple RQs triangulate on same conclusion]

**Divergent Evidence:**

[TBD: Contradictions or unexpected null results]

**Theoretical Implications:**

[TBD: What do results mean for episodic memory theory?]

**Methodological Insights:**

[TBD: What did VR paradigm reveal?]

**Limitations:**

[TBD: Cross-cutting issues - floor effects, short retention interval, omnibus IRT, no practice effect control]

**Bridge to Discussion:**

[TBD: Preview Chapter 6 integration with literature]

---

**END CHAPTER 5 (Empirical Results)**
