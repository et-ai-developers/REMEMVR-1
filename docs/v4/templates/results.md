# V4.X Template: results.md

**Purpose:** Results summary template specification for rq_results agent
**Audience:** rq_results agent when creating summary.md
**Status:** Current (v4.X)
**Version:** 1.0 (2025-11-17)

---

## Table of Contents

1. [Overview](#overview)
2. [How to Use This Template](#how-to-use-this-template)
3. [Workflow Integration](#workflow-integration)
4. [Required Sections](#required-sections)
   - 4.1 [Section 1: Statistical Findings](#section-1-statistical-findings)
   - 4.2 [Section 2: Plot Descriptions](#section-2-plot-descriptions)
   - 4.3 [Section 3: Interpretation](#section-3-interpretation)
   - 4.4 [Section 4: Limitations](#section-4-limitations)
   - 4.5 [Section 5: Next Steps](#section-5-next-steps)
5. [Summary Structure Checklist](#summary-structure-checklist)
6. [Complete Summary Example Skeleton](#complete-summary-example-skeleton)
7. [Common Patterns](#common-patterns)
8. [Error Handling](#error-handling)
9. [Integration with Other V4.X Components](#integration-with-other-v4x-components)
10. [V3.0 vs V4.X Differences](#v30-vs-v4x-differences)
11. [Implementation Notes](#implementation-notes)
12. [Version History](#version-history)

---

## Overview

### Purpose

This template specifies the structure and content requirements for **summary.md** - the final narrative synthesis document created by the rq_results agent (Step 17 in the v4.X workflow).

**Specification Compliance:** Per docs/user/analysis_pipeline_solution.md section 4.4.2, summary.md MUST contain exactly 5 sections (no more, no fewer):
1. Statistical Findings (the WHAT)
2. Plot Descriptions (the VISUAL WHAT)
3. Interpretation (the WHY and SO WHAT)
4. Limitations (the CAVEATS) - MUST include confidence rating response patterns per section 1.4
5. Next Steps (the WHAT'S NEXT)

**Key Goals:**
1. Synthesize statistical findings from analysis outputs
2. Describe visualizations and their insights
3. Interpret results theoretically (what do findings mean?)
4. Acknowledge study limitations transparently
5. Identify follow-up questions and next research steps

### File Naming Clarification

**IMPORTANT:**
- **This template file:** `docs/v4/templates/results.md` (specification)
- **Agent output file:** `results/chX/rqY/results/summary.md` (actual summary)

The rq_results agent reads **results.md template** to understand structure, then creates **summary.md** containing the actual results narrative.

### Audience

- **Primary:** rq_results agent (Step 17 workflow)
- **Secondary:** Master claude when reviewing RQ completion
- **Tertiary:** Thesis readers (summary.md is publication-ready narrative)

### Document Status

- **Created:** 2025-11-17 (Phase 2 Templates completion)
- **Validated:** Spec 4.4.2 compliant
- **Dependencies:** rq_results agent (spec 2.5.2), D069 dual-scale interpretation

---

## How to Use This Template

### For rq_results Agent

**Workflow Position:** Step 17 (final step in 17-step RQ pipeline)

**Read This Template To:**
1. Understand the 5 required sections for summary.md
2. Learn what content each section should contain
3. See examples of well-structured results narratives
4. Identify which input sources to use for each section
5. Follow dual-scale interpretation guidance (Decision D069)

**Then Create:** `results/chX/rqY/results/summary.md` following this structure

### For Master Claude

**When Reviewing:**
- Check summary.md has all 5 required sections
- Verify statistical findings match analysis outputs
- Confirm plots are described accurately
- Validate theoretical interpretation aligns with 1_concept.md
- Ensure limitations are acknowledged honestly
- Approve next steps are logical follow-ups

---

## Workflow Integration

### rq_results Agent Context (Spec 2.5.2)

The rq_results agent is invoked at **Step 17** in the v4.X workflow, after all analysis and plotting complete.

**Agent File:** `.claude/agents/rq_results.md`

**10-Step Workflow:**
1. Read: `agent_best_practices.md` (circuit breakers, platform rules)
2. Read: `status.yaml` (all prior context_dumps from 10 agents)
3. Check: All prior steps = success, this onwards = pending (circuit breaker)
4. **Read: `docs/v4/templates/results.md`** ← This template
5. Read/Bash: Result files using pandas.head() (data/*.csv, plots/*.png)
6. Ultrathink: Synthesize results from 6 input sources (below)
7. Bash: Create `results/chX/rqY/results/summary.md` (output file)
8. Write: Populate summary.md with 5 required sections
9. Edit: Update status.yaml (rq_results success, context_dump)
10. Report: "Successfully created summary.md for chX/rqY"

### 6 Input Sources for Synthesis

The rq_results agent synthesizes information from:

1. **status.yaml context_dumps:**
   - rq_concept: RQ ID/title, domains, analysis approach, data source
   - rq_scholar: Theoretical grounding claims, literature citations
   - rq_stats: Methods appropriateness, tool availability
   - rq_planner: Analysis steps overview
   - rq_tools: Tool specifications used
   - rq_analysis: Analysis calls executed
   - rq_inspect: Validation results per step
   - rq_plots: Plot types generated

2. **Data files (results/chX/rqY/data/):**
   - *.csv outputs (theta_scores.csv, item_parameters.csv, lmm_results.csv, etc.)
   - Use pandas.head() to preview, summarize key values
   - Extract statistical values (coefficients, p-values, effect sizes, etc.)

3. **Plot files (results/chX/rqY/plots/):**
   - *.png visualizations
   - Consult rq_plots context_dump for plot purposes
   - Describe what each plot shows visually

4. **Log files (results/chX/rqY/logs/):**
   - Execution logs per step (stepNN_name.log)
   - Check for warnings, convergence issues, sample sizes
   - Note any anomalies affecting interpretation

5. **Concept document (results/chX/rqY/docs/1_concept.md):**
   - Original research question statement
   - Hypothesis to test against results
   - Theoretical background informing interpretation
   - Memory domains analyzed

6. **Plan document (results/chX/rqY/docs/2_plan.md):**
   - Expected outputs per step
   - Cross-check: Did results match expectations?
   - Note any deviations from plan

**Synthesis Strategy:**
- **Section 1 (Statistical Findings):** Sources 2, 4, 6 (data files, logs, plan)
- **Section 2 (Plot Descriptions):** Sources 3, 8 context_dump (plots, rq_plots)
- **Section 3 (Interpretation):** Sources 1, 5 (concept for theory, scholar for literature)
- **Section 4 (Limitations):** Sources 4, 5, 6 (logs for issues, concept for scope, plan for constraints)
- **Section 5 (Next Steps):** Sources 5, 1 (concept for broader goals, context_dumps for follow-ups)

---

## Required Sections

### Section 1: Statistical Findings

**Purpose:** Report key statistical results from analysis outputs (the WHAT).

**Content Requirements:**

1. **Primary Results:**
   - Main statistical test outcomes (IRT parameters, LMM coefficients, group comparisons)
   - Effect sizes with confidence intervals
   - p-values (BOTH uncorrected and Bonferroni-corrected per Decision D068)
   - Model fit statistics (AIC, BIC, convergence status)

2. **Secondary Results:**
   - Post-hoc contrasts (if applicable)
   - Purification outcomes (items retained/excluded, per Decision D039)
   - Trajectory parameters (slopes, intercepts, variance components)

3. **Sample Characteristics:**
   - N participants included
   - Missing data patterns
   - Test sessions analyzed (Day 0, 1, 3, 6 or TSVR if longitudinal)

**Data Sources:**
- Read data/*.csv files using pandas.head()
- Extract values from lmm_results.csv, item_parameters.csv, theta_scores.csv, etc.
- Consult logs/*.log for sample sizes and warnings
- Cross-reference 2_plan.md expected outputs

**Formatting Guidelines:**

- **Tables:** Use Markdown tables for multi-value comparisons
- **Precision:** Report statistics to 2-3 decimal places (p=0.001, β=1.23, 95% CI [0.45, 2.01])
- **Clarity:** Define abbreviations on first use (LMM = Linear Mixed Model)
- **Honesty:** Report non-significant findings (don't hide null results)

**Example (Section 1 - Statistical Findings):**

```markdown
## Statistical Findings

### IRT Calibration Results

**Pass 1 Calibration:**
- Model: Graded Response Model (GRM) with 3 dimensions (What, Where, When)
- Items analyzed: 102 total VR items
- Model fit: AIC = 12345.67, BIC = 12678.90
- Convergence: Successful after 1200 iterations

**Item Purification (Decision D039):**
- Purification criteria: Discrimination (a ≥ 0.4), Difficulty (|b| ≤ 3.0)
- Items retained: 43/102 (42.2%)
- Items excluded: 59 items (35 temporal items with extreme difficulty, 24 items with low discrimination)

**Pass 2 Calibration:**
- Items: 43 purified items
- Model fit improved: AIC = 8901.23, BIC = 9123.45
- Convergence: Successful after 800 iterations

**Theta Score Reliability:**
- What domain: α = 0.89 (N=43 items, M=-0.15, SD=0.78)
- Where domain: α = 0.92 (N=43 items, M=0.03, SD=0.82)
- When domain: α = 0.85 (N=43 items, M=-0.22, SD=0.71)

### Longitudinal Trajectory Analysis

**Linear Mixed Model:**
- Outcome: Theta scores (latent memory ability)
- Time variable: TSVR (hours since VR encoding, Decision D070)
- Fixed effects: Time, Domain, Time×Domain interaction
- Random effects: Participant intercepts + slopes

**Fixed Effect Estimates:**

| Effect | β | SE | t | p (uncorr) | p (Bonf) | 95% CI |
|--------|---|----|---|------------|----------|---------|
| Time (TSVR) | -0.023 | 0.004 | -5.75 | <.001 | <.001 | [-0.031, -0.015] |
| Domain (Where vs What) | 0.18 | 0.06 | 3.00 | .003 | .009 | [0.06, 0.30] |
| Domain (When vs What) | -0.07 | 0.05 | -1.40 | .162 | .486 | [-0.17, 0.03] |
| Time×Domain (Where) | -0.008 | 0.005 | -1.60 | .110 | .330 | [-0.018, 0.002] |
| Time×Domain (When) | -0.015 | 0.006 | -2.50 | .013 | .039 | [-0.027, -0.003] |

**Variance Components:**
- Participant intercepts: σ² = 0.45 (substantial individual differences in baseline ability)
- Participant slopes: σ² = 0.012 (moderate individual differences in forgetting rate)
- Residual: σ² = 0.31

**Sample:**
- N = 100 participants
- Observations: 400 total (100 participants × 4 test sessions)
- Missing data: 3 participants excluded from Day 6 due to dropout

### Post-Hoc Contrasts

**Domain Comparisons at Day 6 (TSVR = 144 hours):**
- What vs Where: β = -0.18, p < .001 (Bonferroni-corrected)
- What vs When: β = 0.07, p = .162 (n.s.)
- Where vs When: β = 0.25, p < .001 (Bonferroni-corrected)

**Interpretation:** Spatial memory (Where) significantly better than object memory (What) at 6-day retention, temporal memory (When) intermediate.
```

---

### Section 2: Plot Descriptions

**Purpose:** Describe visualizations and what they show (the VISUAL WHAT).

**Content Requirements:**

1. **Plot Inventory:**
   - List all plots generated (by filename)
   - State plot type (trajectory, diagnostic, histogram, etc.)
   - Indicate which analysis step generated each plot

2. **Visual Descriptions:**
   - What the plot displays (axes, groups, trajectories)
   - Key patterns visible (trends, differences, outliers)
   - Notable features (confidence intervals, scatter, convergence)

3. **Plot-to-Finding Mapping:**
   - How each plot supports statistical findings from Section 1
   - What insights plots reveal beyond numbers

**Data Sources:**
- List plots/*.png files
- Read rq_plots context_dump for plot purposes
- Consult 2_plan.md for expected visualizations
- Reference tools/plotting.py for plot types (via rq_plots)

**Formatting Guidelines:**

- **Organization:** One subsection per plot or logical plot grouping
- **Filenames:** Reference exact filename (e.g., `trajectory_theta_by_domain.png`)
- **Accessibility:** Describe visuals for readers who can't see plots
- **Integration:** Connect visual patterns to Section 1 statistics

**Special Requirement (Decision D069 - Dual-Scale Trajectories):**

For trajectory plots, ALWAYS describe BOTH scales:
1. **Theta scale:** Latent trait forgetting trajectory (abstract, standardized)
2. **Probability scale:** Performance likelihood trajectory (practical, interpretable)

**Example:**
"Figure shows dual-scale trajectory where theta decreases from 0.5 to -0.3 (left y-axis, 0.8 SD decline) corresponding to performance probability drop from 75% to 55% (right y-axis, 20 percentage point decline over 6 days)."

**Example (Section 2 - Plot Descriptions):**

```markdown
## Plot Descriptions

### Figure 1: Dual-Scale Trajectory by Memory Domain

**Filename:** `trajectory_dual_scale_by_domain.png`
**Plot Type:** Line plot with dual y-axes (theta + probability scales)
**Generated By:** Step 8 plotting (Decision D069 compliance)

**Visual Description:**

The plot displays forgetting trajectories across 4 test sessions (Day 0, 1, 3, 6) for three memory domains:

- **X-axis:** TSVR (Time Since VR, hours): 0, 24, 72, 144
- **Left Y-axis:** Theta scores (latent memory ability): -1.5 to 1.5
- **Right Y-axis:** Performance probability: 0% to 100%

**Domain Trajectories (Theta Scale):**
- **What (objects):** Starts at θ = 0.2 (Day 0), declines to θ = -0.4 (Day 6) - 0.6 SD decline
- **Where (locations):** Starts at θ = 0.5 (Day 0), declines to θ = 0.1 (Day 6) - 0.4 SD decline
- **When (temporal):** Starts at θ = -0.1 (Day 0), declines to θ = -0.7 (Day 6) - 0.6 SD decline

**Domain Trajectories (Probability Scale):**
- **What:** 65% → 45% (20 percentage point decline)
- **Where:** 75% → 60% (15 percentage point decline)
- **When:** 55% → 35% (20 percentage point decline)

**Key Patterns:**
1. All domains show monotonic decline (forgetting over time)
2. Where domain consistently highest performance (both scales)
3. When domain consistently lowest performance (both scales)
4. Steeper decline Day 0→1 than Day 3→6 (rapid initial forgetting)
5. Confidence intervals (shaded) widen over time (increasing uncertainty)

**Connection to Findings:**
- Visual confirms statistical Time main effect (β = -0.023, p < .001)
- Domain separation visible matches Where > What > When contrasts
- Probability scale shows practical significance: 15-20% performance drops matter for real-world memory assessment

---

### Figure 2: IRT Item Difficulty Distribution (Pass 2)

**Filename:** `item_difficulty_histogram_pass2.png`
**Plot Type:** Histogram with density overlay
**Generated By:** Step 4 purification output

**Visual Description:**

Histogram shows distribution of item difficulty (b parameters) for 43 retained items after purification:

- **X-axis:** Difficulty (b): -3.0 to 3.0
- **Y-axis:** Count of items: 0 to 12
- **Overlay:** Kernel density estimate (smooth curve)

**Distribution Shape:**
- Mean difficulty: b = -0.12 (slightly easier than average)
- SD: 0.85 (moderate spread)
- Range: -2.8 to 2.6 (within purification thresholds |b| ≤ 3.0)
- Skew: Nearly symmetric (slight negative skew)

**Notable Features:**
- Bimodal distribution (peaks at b = -0.8 and b = 0.5)
- Few items in extreme difficulty range (b < -2.5 or b > 2.5)
- No items beyond |b| = 3.0 (purification successful per Decision D039)

**Connection to Findings:**
- Confirms 59 items excluded for extreme difficulty (temporal items had b > 5.0)
- Retained items span ability range for reliable theta estimation
- Bimodal pattern may reflect What/Where vs When domain difficulty differences

---

### Figure 3: Model Diagnostics (Residual Plot)

**Filename:** `lmm_residuals_vs_fitted.png`
**Plot Type:** Scatter plot
**Generated By:** Step 6 LMM validation

**Visual Description:**

Residual plot for LMM model fit assessment:

- **X-axis:** Fitted values (predicted theta): -1.5 to 1.5
- **Y-axis:** Residuals (observed - predicted): -2.0 to 2.0
- **Reference line:** Horizontal line at y = 0 (perfect fit)

**Patterns:**
- Random scatter around y = 0 (no systematic bias)
- Homoscedasticity: Residual spread consistent across fitted value range
- No outliers beyond ±2.5 SD (all points within normal range)
- LOESS curve (red) nearly flat (assumptions met)

**Connection to Findings:**
- Supports LMM assumptions (linearity, homogeneity of variance)
- No evidence of model misspecification
- Validates interpretation of fixed effects as unbiased estimates
```

---

### Section 3: Interpretation

**Purpose:** Explain what results MEAN theoretically (the WHY and SO WHAT).

**Content Requirements:**

1. **Theoretical Contextualization:**
   - How findings relate to original hypothesis (from 1_concept.md)
   - Connection to theoretical background (episodic memory theory, VR assessment)
   - Consistency with prior literature (from rq_scholar validation)

2. **Dual-Scale Interpretation (Decision D069 - Trajectory RQs Only):**
   - **Theta scale interpretation:** What latent trait changes mean
   - **Probability scale interpretation:** What performance changes mean practically
   - **Why both matter:** Abstract rigor + practical accessibility

3. **Domain-Specific Insights:**
   - What findings reveal about each memory domain (What, Where, When)
   - Domain differences and their theoretical implications
   - Unexpected patterns and possible explanations

4. **Broader Implications:**
   - How results contribute to REMEMVR validation
   - Clinical relevance (if applicable)
   - Methodological insights (IRT, LMM, VR assessment)

**Data Sources:**
- Read 1_concept.md for original hypothesis and theory
- Read rq_scholar context_dump for literature connections
- Synthesize statistical findings (Section 1) with theoretical framework
- Consider rq_stats context_dump for methodological insights

**Formatting Guidelines:**

- **Hypothesis Testing:** Explicitly state whether hypothesis supported/rejected
- **Literature Links:** Cite key references from scholar validation
- **Nuance:** Acknowledge alternative interpretations
- **Accessibility:** Explain technical findings in plain language

**Decision D069: Dual-Scale Interpretation Guidance (Trajectory RQs)**

**When to Use:** Any RQ analyzing forgetting trajectories over time (~40 RQs in thesis)

**Why Dual-Scale Matters:**

1. **Theta Scale (Latent Trait):**
   - **What it is:** Standardized memory ability score (mean = 0, SD = 1)
   - **Strengths:** Psychometrically rigorous, comparable across studies, interval scale properties
   - **Limitation:** Abstract, not intuitive to non-psychometricians

2. **Probability Scale (Performance Likelihood):**
   - **What it is:** Estimated probability of correct recall (0% to 100%)
   - **Strengths:** Intuitive, clinically meaningful, practical interpretation
   - **Limitation:** Non-linear transformation of theta, less precise at extremes

3. **IRT Transformation Formula:**
   ```
   P(correct) = 1 / (1 + exp(-(a × (θ - b))))
   ```
   - a = item discrimination
   - θ = person ability (theta)
   - b = item difficulty

**Interpretation Template (Use for Trajectory RQs):**

```markdown
### Dual-Scale Trajectory Interpretation (Decision D069)

**Theta Scale Findings:**
[Report theta decline in SD units, e.g., "Memory ability declined 0.6 SD from Day 0 (θ=0.2) to Day 6 (θ=-0.4)"]

**Statistical Interpretation:**
[What the standardized decline means: effect size classification (small/medium/large), comparison to norms if available]

**Probability Scale Findings:**
[Report performance decline in percentage points, e.g., "Recall probability dropped from 65% to 45% (20 percentage point decline)"]

**Practical Interpretation:**
[What the performance decline means: clinical significance, real-world impact, accessibility for non-experts]

**Why Both Scales Matter:**
- **Theta:** Provides psychometric rigor for scientific conclusions (standardized effect sizes, cross-study comparisons)
- **Probability:** Provides practical meaning for applied contexts (clinical cutoffs, performance benchmarks)
- **Together:** Ensure findings are both scientifically rigorous AND accessible to broader audiences
```

**Example Usage:**

```markdown
### Dual-Scale Trajectory Interpretation

**Theta Scale Findings:**
Spatial memory (Where domain) showed the shallowest decline trajectory, decreasing 0.4 SD from baseline (θ = 0.5) to 6-day retention (θ = 0.1). Object memory (What) and temporal memory (When) both declined 0.6 SD over the same period.

**Statistical Interpretation:**
A 0.4 SD decline represents a small-to-medium effect (Cohen's d), while 0.6 SD represents a medium effect. Where domain's resilience is statistically meaningful: the Time×Domain interaction was significant (β = -0.008, p = .039 Bonferroni-corrected), indicating slower forgetting for spatial information.

**Probability Scale Findings:**
Translating to performance probabilities, Where domain recall dropped from 75% to 60% (15 percentage points), while What and When domains both dropped approximately 20 percentage points (65%→45% and 55%→35%, respectively).

**Practical Interpretation:**
The probability scale reveals clinically meaningful differences: a participant with average spatial memory has 60% chance of correct recall after 6 days—well above chance (33% for 3-option tasks). In contrast, temporal memory drops to 35%, barely above chance performance. For VR-based cognitive assessment applications, this suggests spatial memory tasks provide more reliable signal at longer retention intervals.

**Why Both Scales Matter:**
- **Theta:** The 0.2 SD difference in forgetting rates (0.4 vs 0.6) is statistically robust and comparable to prior episodic memory research showing spatial advantage (Bird & Burgess, 2008).
- **Probability:** The 15 vs 20 percentage point decline difference has practical implications: clinicians can interpret "60% retention" without psychometric training, whereas "θ = 0.1" requires IRT literacy.
- **Together:** We demonstrate both scientific rigor (standardized effect sizes for meta-analysis) and practical utility (interpretable performance metrics for assessment tools).
```

**Example (Section 3 - Interpretation):**

```markdown
## Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**
"Spatial memory (Where) will show slower forgetting than object (What) or temporal (When) memory due to enhanced encoding in immersive VR environments, which provide richer spatial context cues."

**Hypothesis Status:** **SUPPORTED**

The statistical findings confirm slower forgetting for Where domain:
- Theta decline: 0.4 SD (Where) vs 0.6 SD (What/When)
- Time×Domain interaction: β = -0.008, p = .039 (Bonferroni-corrected)
- Post-hoc contrasts: Where > What at Day 6 (p < .001)

### Dual-Scale Trajectory Interpretation (Decision D069)

[Example from above included here - full dual-scale interpretation with theta + probability scales, statistical + practical meaning, why both matter]

### Theoretical Contextualization

**Episodic Memory Theory:**

The differential forgetting rates across domains align with dual-process theories of episodic memory (Rugg & Vilberg, 2013):

1. **Spatial Memory Advantage:**
   - Hippocampal spatial processing networks more robust than object/temporal encoding (Ekstrom & Ranganath, 2018)
   - VR immersion enhances spatial encoding through active navigation (Montefinese et al., 2015)
   - Slower Where domain forgetting replicates lab findings in ecological VR context

2. **Temporal Memory Vulnerability:**
   - When domain's steepest decline (0.6 SD, 20 percentage points) consistent with temporal order memory being most fragile episodic component (Friedman, 1993)
   - Lack of external temporal cues in VR (no real-world time passage) may exacerbate temporal forgetting
   - Suggests VR assessments should prioritize spatial/object tasks for longer retention intervals

**Literature Connections (from rq_scholar validation):**

- **Bird & Burgess (2008):** "Spatial memory shows retention advantage in navigation tasks" - our VR findings extend this to multi-domain episodic assessment
- **Ekstrom et al. (2003):** "Hippocampal place cells encode spatial locations during virtual navigation" - neural substrate for Where domain resilience
- **Tulving (2002):** "Episodic memory components (what/where/when) differentially vulnerable to forgetting" - confirmed in immersive VR context

### Domain-Specific Insights

**What Domain (Object Memory):**
- Moderate forgetting rate (0.6 SD decline, 65%→45% probability)
- Consistent with object recognition memory literature (Squire, Wixted, & Clark, 2007)
- VR object encoding may lack distinctiveness of real-world object interactions (tactile, motor)

**Where Domain (Spatial Memory):**
- Slowest forgetting (0.4 SD decline, 75%→60% probability)
- VR's strength: immersive spatial context enhances encoding durability
- Clinical potential: spatial memory tasks reliable at 6-day retention for VR assessment

**When Domain (Temporal Memory):**
- Fastest forgetting (0.6 SD decline, 55%→35% probability)
- Lack of naturalistic temporal cues in VR (compressed encoding, no circadian anchors)
- Suggests VR temporal assessments require shorter retention intervals or enhanced temporal cues

### Unexpected Patterns

**Bimodal Item Difficulty Distribution:**

The IRT purification revealed bimodal difficulty pattern (Figure 2: peaks at b = -0.8 and b = 0.5). Possible explanations:

1. **Domain-Driven:** What/Where items easier (negative b) than When items (positive b)
2. **Encoding Salience:** Spatially distinct landmarks easier than temporally ambiguous events
3. **Methodological:** VR encoding order effects (earlier items easier due to novelty)

Further investigation needed: Examine difficulty by domain explicitly in follow-up RQ.

**Individual Differences in Slopes:**

Substantial variance in participant forgetting rates (slope variance σ² = 0.012) suggests:
- Not all participants forget at same rate (individual differences matter)
- Potential for subgroup analyses (fast vs slow forgetters)
- Clinical relevance: forgetting rate may be more sensitive cognitive marker than baseline ability

### Broader Implications

**REMEMVR Validation:**

Findings support REMEMVR as valid episodic memory assessment tool:
- Multi-domain sensitivity (detects domain differences)
- Temporal resolution (captures forgetting trajectories)
- Ecological validity (VR spatial advantage mirrors real-world navigation)

**Methodological Insights:**

1. **IRT Purification Necessary (Decision D039):**
   - Excluding 59/102 items improved model fit (AIC reduced by 27%)
   - Temporal items particularly problematic (extreme difficulty b > 5.0)
   - Future VR test development: pilot test temporal item difficulty

2. **TSVR as Time Variable (Decision D070):**
   - Using actual hours (not nominal days) captures continuous forgetting
   - Enables more precise trajectory estimation
   - Generalizable to studies with variable retention intervals

3. **Dual-Scale Reporting (Decision D069):**
   - Balances scientific rigor (theta) with practical utility (probability)
   - Makes findings accessible to non-psychometrician audiences
   - Recommended best practice for applied IRT research

**Clinical Relevance:**

For cognitive assessment applications:
- Spatial tasks optimal for 6-day retention (60% performance)
- Temporal tasks require shorter intervals (35% near chance at 6 days)
- Individual forgetting rates may index cognitive health better than cross-sectional scores
```

---

### Section 4: Limitations

**Purpose:** Acknowledge study constraints honestly and transparently (the CAVEATS).

**Content Requirements:**

1. **Sample Limitations:**
   - Sample size constraints (N, power considerations)
   - Demographic restrictions (age, education, recruitment source)
   - Attrition/missing data (dropout patterns, bias concerns)
   - **Confidence rating response patterns** (per solution.md section 1.4): Document % participants using full 1-5 range vs extremes only (1s and 5s). Note: No bias correction applied (transparency priority). May limit interpretability of confidence-accuracy relationships.

2. **Methodological Limitations:**
   - Measurement constraints (item coverage, domain definitions)
   - Design limitations (no control group, confounds, limited sessions)
   - Statistical limitations (assumptions, model constraints)

3. **Generalizability Constraints:**
   - Population generalizability (who findings apply to)
   - Context generalizability (VR vs real-world, lab vs field)
   - Task generalizability (specific VR paradigm vs broader episodic memory)

4. **Technical Limitations:**
   - IRT model choices (GRM vs alternatives, dimensionality assumptions)
   - LMM specification (random effects structure, missing data handling)
   - Purification impact (information loss from excluding items)

**Data Sources:**
- Read logs/*.log for warnings, convergence issues, sample size notes
- Consult 1_concept.md for acknowledged scope constraints
- Review 2_plan.md for design decisions (tradeoffs made)
- Check rq_stats context_dump for methodological considerations

**Formatting Guidelines:**

- **Honesty:** Don't minimize serious limitations
- **Specificity:** Quantify where possible (e.g., "limited to N=100, power=0.80 for medium effects")
- **Constructive:** Suggest how limitations could be addressed in future work
- **Balance:** Acknowledge constraints without undermining findings

**Example (Section 4 - Limitations):**

```markdown
## Limitations

### Sample Limitations

**Sample Size:**
- N = 100 participants provides adequate power (0.80) for medium effects (d = 0.5) but underpowered for small effects (d = 0.2, power = 0.45)
- Subgroup analyses (e.g., fast vs slow forgetters) constrained by limited N per group
- Confidence intervals wide for some estimates (e.g., Time×Domain interactions)

**Demographic Constraints:**
- University undergraduate sample (age: M = 20.3, SD = 1.8) limits generalizability to older adults
- Restricted education range (all current college students) prevents examining education effects
- Predominantly female (68%) may not represent male episodic memory patterns

**Attrition:**
- 3% dropout by Day 6 (3/100 participants) modest but introduces potential bias
- Dropout reasons unknown (no systematic tracking)
- Missing data assumed MAR (missing at random), but MNAR (missing not at random) cannot be ruled out

### Methodological Limitations

**Measurement:**

1. **Item Coverage:**
   - Only 43 items retained after purification (limited domain sampling)
   - When domain particularly sparse (estimated 12 items retained based on difficulty exclusions)
   - Reliability estimates potentially inflated due to homogeneous item pool

2. **Domain Definitions:**
   - What/Where/When dimensions conceptual (not empirically validated)
   - Assumed orthogonal but may have correlated components (e.g., spatial-temporal binding)
   - Multidimensional IRT assumes simple structure (each item loads one dimension)

3. **VR Paradigm Specificity:**
   - Findings specific to desktop VR (not fully immersive HMD)
   - Encoding task highly structured (may not reflect naturalistic episodic encoding)
   - Short encoding duration (10 minutes) may not engage deep episodic processing

**Design:**

1. **No Control Condition:**
   - Cannot isolate VR-specific effects (no 2D comparison)
   - Forgetting rates may differ in non-VR episodic tasks
   - Spatial advantage could be VR-enhanced or general episodic memory pattern

2. **Test Session Timing:**
   - Fixed retention intervals (0, 1, 3, 6 days) may miss critical forgetting dynamics
   - No immediate post-encoding test (Day 0 is encoding, not retrieval baseline)
   - Day 6 may be insufficient to observe asymptotic forgetting

3. **Practice Effects:**
   - Four repeated retrievals may alter forgetting trajectory (testing effect)
   - No way to separate forgetting from practice effects with current design
   - LMM assumes linear time effect (may not capture testing-induced non-linearity)

**Statistical:**

1. **IRT Model:**
   - GRM assumes monotonic item response functions (may not hold for all items)
   - Three-dimension structure assumed (not compared against 1D, 2D, or 4D+ models)
   - Local independence assumption may be violated for semantically related items

2. **LMM Specification:**
   - Random slopes model assumes linear trajectories (no quadratic/cubic forgetting curves tested)
   - Unstructured covariance may not be optimal (AR1, compound symmetry not compared)
   - Fixed effects only (no random Domain effects, limiting individual difference modeling)

3. **Multiple Comparisons:**
   - Bonferroni correction conservative (may miss true effects with p = .01-.05)
   - Family-wise error rate controlled, but inflation still possible with many contrasts
   - No pre-registered analysis plan (exploratory analyses risk Type I error)

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - Older adults (episodic memory declines with age, forgetting rates may differ)
  - Clinical populations (MCI, dementia, TBI patients have different forgetting profiles)
  - Children/adolescents (developing episodic memory systems)
  - Non-WEIRD samples (cross-cultural episodic memory differences documented)

**Context:**
- VR desktop paradigm differs from:
  - Fully immersive HMD VR (greater presence, embodiment)
  - Real-world navigation (tactile, vestibular, olfactory cues)
  - Standard neuropsychological tests (2D stimuli, verbal responses)

**Task:**
- REMEMVR specific encoding task may not reflect:
  - Naturalistic episodic memory (spontaneous, unstructured encoding)
  - Emotional episodic memories (neutral VR content, no affective salience)
  - Semantic memory (facts vs events)

### Technical Limitations

**IRT Purification Impact (Decision D039):**
- Excluding 59/102 items (58%) raises concerns:
  - Information loss (reduced item pool limits precision)
  - Potential domain imbalance (if exclusions uneven across What/Where/When)
  - Generalizability to full item set uncertain (retained items may be "easy subset")

**TSVR Variable (Decision D070):**
- TSVR (hours since encoding) assumes continuous forgetting
- May not capture day-specific consolidation effects (sleep, interference)
- Treats time linearly (exponential or logarithmic time scaling not tested)

**Dual-Scale Reporting (Decision D069):**
- Probability scale transformation assumes specific IRT parameters (a, b from calibration)
- If item parameters unstable, probability estimates unreliable
- Transformation non-linear (extremes compressed, reducing sensitivity at high/low abilities)

### Limitations Summary

Despite these constraints, findings are **robust within scope:**
- Spatial memory advantage consistent across analytical approaches (IRT, LMM, plots)
- Effect sizes medium-to-large (not reliant on marginal significance)
- Results align with prior literature (replication strengthens conclusions)

Limitations indicate **directions for future work** (see Section 5: Next Steps).
```

---

### Section 5: Next Steps

**Purpose:** Identify logical follow-up research questions and analyses (the WHAT'S NEXT).

**Content Requirements:**

1. **Immediate Follow-Ups:**
   - Analyses using current data (alternative models, subgroups, exploratory)
   - Clarifications needed from this RQ (additional plots, sensitivity tests)

2. **Planned RQs:**
   - Subsequent RQs in thesis that build on these findings
   - How this RQ sets up future chapters (e.g., RQ 5.2 will examine...)

3. **Methodological Extensions:**
   - Improved designs to address limitations
   - Alternative statistical approaches to test robustness
   - Enhanced measurement (more items, different paradigms)

4. **Theoretical Questions:**
   - Unanswered questions raised by findings
   - Alternative explanations to test
   - Broader research programs implied by results

**Data Sources:**
- Review Section 4 limitations (what to address next)
- Consider 1_concept.md broader research context
- Check thesis chapter plans (docs/v4/thesis/ANALYSES_CHX.md for subsequent RQs)
- Synthesize unexpected findings needing follow-up

**Formatting Guidelines:**

- **Specificity:** Concrete next steps (not vague "future research needed")
- **Prioritization:** Distinguish critical vs optional follow-ups
- **Feasibility:** Note which next steps are planned vs aspirational
- **Connections:** Link to specific thesis RQs where applicable

**Example (Section 5 - Next Steps):**

```markdown
## Next Steps

### Immediate Follow-Ups (Current Data)

**1. Domain-Specific Item Difficulty Analysis:**
- **Why:** Bimodal difficulty distribution (Figure 2) suggests domain-driven clustering
- **How:** Re-run IRT calibration with domain-specific difficulty constraints, compare AIC
- **Expected Insight:** Quantify whether What/Where items systematically easier than When items
- **Timeline:** Can be done immediately (same data, alternative model specification)

**2. Individual Difference Clustering:**
- **Why:** Substantial slope variance (σ² = 0.012) indicates forgetting rate heterogeneity
- **How:** Extract participant-specific slope BLUPs, perform k-means clustering (2-3 groups)
- **Expected Insight:** Identify "fast forgetters" vs "slow forgetters," explore demographic predictors
- **Timeline:** Immediate (data available from LMM random effects)

**3. Sensitivity Analysis for Purification Thresholds:**
- **Why:** Decision D039 used |b| ≤ 3.0 and a ≥ 0.4 (somewhat arbitrary cutoffs)
- **How:** Test alternative thresholds (|b| ≤ 2.5, a ≥ 0.5) to assess robustness
- **Expected Insight:** Determine whether domain effects depend on purification severity
- **Timeline:** ~2 days (requires re-running IRT Pass 2 with different item sets)

### Planned Thesis RQs (Chapter 5 Continuation)

**RQ 5.2: Domain-Specific Forgetting Curves (Planned):**
- **Focus:** Estimate separate forgetting trajectories per domain (3 LMMs instead of 1 interaction model)
- **Why:** Current RQ assumes linear forgetting; domain-specific curves may reveal non-linearity
- **Builds On:** Uses purified items from this RQ (43 items), adds quadratic time terms
- **Expected Timeline:** Next RQ in analysis pipeline

**RQ 5.3: Test-Retest Reliability of Theta Scores (Planned):**
- **Focus:** Correlate Day 0 vs Day 1 theta estimates (24-hour stability)
- **Why:** Reliability essential for VR assessment validation; this RQ establishes baseline estimates
- **Builds On:** Uses theta_scores.csv from this RQ, extracts Day 0 and Day 1 values
- **Expected Timeline:** Two RQs ahead (after RQ 5.2)

**RQ 5.4: Item-Level Forgetting Patterns (Exploratory):**
- **Focus:** Which specific items show steepest forgetting? Landmark vs non-landmark, salient vs mundane?
- **Why:** Findings showed temporal items excluded due to difficulty, but object/spatial item heterogeneity unexplored
- **Builds On:** Item parameters from this RQ, requires item-level metadata (currently unavailable)
- **Expected Timeline:** Dependent on item metadata coding (not yet complete)

### Methodological Extensions (Future Data Collection)

**1. Expand Retention Interval:**
- **Current Limitation:** Day 6 may not reach asymptotic forgetting
- **Extension:** Add Day 14 and Day 28 test sessions (N = 50 subsample)
- **Expected Insight:** Determine long-term retention curves, identify floor effects
- **Feasibility:** Requires new data collection (not in current dataset)

**2. Test Alternative IRT Dimensionality:**
- **Current Limitation:** Three dimensions (What/Where/When) assumed, not empirically validated
- **Extension:** Fit 1D, 2D, 4D models, compare via AIC/BIC
- **Expected Insight:** Determine if conceptual domains align with statistical dimensions
- **Feasibility:** Immediate (same data, different mirt() specifications)

**3. Compare VR vs 2D Control:**
- **Current Limitation:** Cannot isolate VR-specific encoding effects
- **Extension:** Recruit N = 50 matched controls, administer 2D slideshow version of REMEMVR task
- **Expected Insight:** Test if spatial memory advantage is VR-enhanced or general episodic pattern
- **Feasibility:** Requires new participants and 2D task development (~3 months)

**4. Incorporate HMD Immersive VR:**
- **Current Limitation:** Desktop VR lacks full immersion (no head tracking, limited FOV)
- **Extension:** Replicate with Oculus Quest 2 HMD (N = 100 new sample)
- **Expected Insight:** Test if immersion enhances encoding (stronger spatial advantage expected)
- **Feasibility:** Requires HMD acquisition and IRB amendment (~6 months)

### Theoretical Questions Raised

**1. Neural Mechanisms of Spatial Memory Advantage:**
- **Question:** Is Where domain's slower forgetting due to hippocampal place cell encoding (Ekstrom et al., 2003)?
- **Next Steps:** Collaborate with neuroimaging lab, fMRI study during VR encoding
- **Expected Insight:** Identify neural signatures predicting domain-specific forgetting rates
- **Feasibility:** Long-term collaboration (1-2 years)

**2. Ecological Validity of VR Episodic Memory:**
- **Question:** Do VR forgetting trajectories mirror real-world episodic memory (e.g., remembering actual events)?
- **Next Steps:** Diary study comparing VR recall to naturalistic event recall (e.g., "Where did you park yesterday?")
- **Expected Insight:** Establish VR-to-real-world generalizability coefficients
- **Feasibility:** Moderate (requires diary method development, ~6 months)

**3. Individual Differences in Forgetting Rates:**
- **Question:** What predicts fast vs slow forgetting? Cognitive ability? Sleep quality? Interference?
- **Next Steps:** Collect additional measures (working memory, sleep logs, daily activities) in new sample
- **Expected Insight:** Build predictive model of forgetting vulnerability
- **Feasibility:** Requires expanded assessment battery (~1 year for new cohort)

### Priority Ranking

**High Priority (Do First):**
1. RQ 5.2 (domain-specific curves) - natural next step in thesis
2. Alternative IRT dimensionality - tests assumption, uses current data
3. Individual difference clustering - addresses slope variance finding

**Medium Priority (Subsequent):**
1. RQ 5.3 (test-retest reliability) - validation essential, but after trajectories
2. Sensitivity analysis for purification - robustness check, not primary question
3. Domain-specific item difficulty - explains bimodal pattern, informs future test development

**Lower Priority (Aspirational):**
1. VR vs 2D control - ideal but requires new data collection
2. HMD immersive VR - interesting but not critical for current thesis
3. fMRI neural mechanisms - long-term collaboration, outside thesis scope

### Next Steps Summary

The findings establish **spatial memory advantage in VR forgetting**, raising three critical questions for immediate follow-up:

1. **RQ 5.2:** Are domain trajectories non-linear? (Planned next RQ)
2. **Clustering:** Can we identify fast vs slow forgetters? (Exploratory, current data)
3. **Dimensionality:** Do statistical dimensions match conceptual domains? (Validation, current data)

Methodological extensions (VR vs 2D, HMD, extended retention) are valuable but require new data collection beyond current thesis scope.
```

---

## Summary Structure Checklist

Before finalizing summary.md, verify all required elements present:

### Section 1: Statistical Findings ✓
- [ ] Primary statistical results (effect estimates, p-values, CIs)
- [ ] Model fit statistics (AIC, BIC, convergence)
- [ ] Sample characteristics (N, missing data)
- [ ] Tables formatted correctly (Markdown)
- [ ] Precision appropriate (2-3 decimal places)
- [ ] Non-significant results reported (not hidden)

### Section 2: Plot Descriptions ✓
- [ ] All plots listed (by filename)
- [ ] Visual descriptions (axes, patterns, features)
- [ ] Connection to statistical findings
- [ ] D069 dual-scale described (if trajectory plot)
- [ ] Accessible language (describe visuals for non-viewers)

### Section 3: Interpretation ✓
- [ ] Hypothesis tested explicitly (supported/rejected)
- [ ] Theoretical contextualization (literature connections)
- [ ] D069 dual-scale interpretation (if trajectory RQ)
- [ ] Domain-specific insights
- [ ] Unexpected patterns explained
- [ ] Broader implications discussed

### Section 4: Limitations ✓
- [ ] Sample limitations (N, demographics, attrition)
- [ ] Methodological limitations (design, measurement)
- [ ] Generalizability constraints (population, context, task)
- [ ] Technical limitations (IRT, LMM, purification)
- [ ] Honest and specific (quantified where possible)
- [ ] Constructive (linked to next steps)

### Section 5: Next Steps ✓
- [ ] Immediate follow-ups (current data)
- [ ] Planned thesis RQs (subsequent analyses)
- [ ] Methodological extensions (future data)
- [ ] Theoretical questions raised
- [ ] Priority ranking (high/medium/low)
- [ ] Specific and feasible (not vague "future research")

---

## Complete Summary Example Skeleton

Below is a skeleton showing the full summary.md structure (sections only, not full content):

```markdown
# RQ 5.1: Forgetting Trajectories Across Memory Domains

**Research Question:** Do forgetting rates differ across memory domains (What, Where, When) in immersive VR episodic memory assessment?

**Analysis Date:** 2025-11-17
**Analyst:** [Name]
**Status:** Complete

---

## Statistical Findings

### IRT Calibration Results
[Pass 1, purification, Pass 2 model fit and parameters]

### Longitudinal Trajectory Analysis
[LMM fixed effects table, variance components, post-hoc contrasts]

---

## Plot Descriptions

### Figure 1: Dual-Scale Trajectory by Memory Domain
[Filename, plot type, visual description, theta + probability scales, patterns, connection to findings]

### Figure 2: IRT Item Difficulty Distribution (Pass 2)
[Filename, plot type, distribution shape, connection to purification]

### Figure 3: Model Diagnostics (Residual Plot)
[Filename, plot type, diagnostic patterns, assumption validation]

---

## Interpretation

### Hypothesis Testing
[Hypothesis statement, supported/rejected, evidence]

### Dual-Scale Trajectory Interpretation (Decision D069)
[Theta scale findings + statistical interpretation]
[Probability scale findings + practical interpretation]
[Why both scales matter]

### Theoretical Contextualization
[Episodic memory theory, literature connections, domain-specific insights]

### Unexpected Patterns
[Bimodal difficulty, individual differences, explanations]

### Broader Implications
[REMEMVR validation, methodological insights, clinical relevance]

---

## Limitations

### Sample Limitations
[N, demographics, attrition]

### Methodological Limitations
[Measurement, design, statistical]

### Generalizability Constraints
[Population, context, task]

### Technical Limitations
[IRT, LMM, purification impact]

---

## Next Steps

### Immediate Follow-Ups (Current Data)
[Specific analyses to run next]

### Planned Thesis RQs
[RQ 5.2, 5.3, 5.4 connections]

### Methodological Extensions
[Future data collection needs]

### Theoretical Questions Raised
[Unanswered questions for long-term research]

### Priority Ranking
[High/medium/low priority sequencing]

---

**End of Summary**
```

---

## Common Patterns

### Pattern 1: Null Result Reporting

**When:** Statistical test non-significant (p > .05)

**How to Report:**
- State result transparently: "No significant Time×Domain interaction (β = 0.003, p = .421)"
- Report effect size and CI: "Effect small (d = 0.12, 95% CI [-0.15, 0.39])"
- Interpret null: "Findings suggest forgetting rates similar across domains" (not "no effect")
- Distinguish from underpowered: "Power analysis indicates 0.80 power for medium effects (d ≥ 0.5), but only 0.25 power for small effects (d = 0.2), limiting ability to detect subtle differences"

### Pattern 2: Contradictory Results

**When:** Statistical test says one thing, plot shows another (e.g., significant p-value but small effect size)

**How to Report:**
- Acknowledge discrepancy: "Although statistically significant (p = .032), effect size is small (d = 0.18) and CI wide (95% CI [-0.05, 0.41])"
- Contextualize: "Significance driven by large N (100 participants), not necessarily practical importance"
- Integrate: "Visual inspection (Figure 2) shows minimal separation between domain trajectories, consistent with small effect interpretation"

### Pattern 3: Expected Failure (TDD Philosophy)

**When:** Analysis fails due to missing validation tool, naming convention, or specification gap

**How to Report:**
- Expected per TDD: "Analysis step failed due to missing validation tool (validate_lmm_assumptions not yet implemented)"
- Document in summary.md: "Step 6 required manual validation (residual plots inspected visually), automated validation to be added in validation tool migration (Phase 4)"
- Next steps: "Add validate_lmm_assumptions() to tools/validation.py before RQ 5.2 to automate assumption checking"

### Pattern 4: Multi-Source Synthesis

**When:** Statistical findings + plots + context_dumps all contribute to interpretation

**How to Integrate:**
- Section 1 (Findings): Report statistics from data/*.csv
- Section 2 (Plots): Describe visual patterns from plots/*.png
- Section 3 (Interpretation): Synthesize using 1_concept.md (theory) + rq_scholar (literature) + all above
- Cross-reference: "The significant Time effect (β = -0.023, Section 1) is visually evident in Figure 1 (monotonic decline across all domains)"

### Pattern 5: Decision Compliance Documentation

**When:** RQ implements project-wide decision (D039, D068, D069, D070)

**How to Document:**
- Cite decision: "Item purification followed Decision D039 thresholds (a ≥ 0.4, |b| ≤ 3.0)"
- Report compliance: "43/102 items retained (42.2%), within expected range (40-50% per D039)"
- Explain rationale: "D069 dual-scale reporting ensures both scientific rigor (theta) and practical accessibility (probability)"
- Connect to findings: "TSVR as time variable (D070) enabled continuous forgetting estimation with higher precision than nominal days"

---

## Error Handling

### Common Errors and Solutions

**Error 1: Missing Required Section**

**Symptom:** Agent creates summary.md with only 4 sections (e.g., omits Limitations)

**Diagnosis:** Agent didn't follow template structure checklist

**Solution:**
1. Master reads summary.md, identifies missing section
2. Master prompts rq_results agent: "Regenerate summary.md including all 5 required sections per results.md template (Section 4: Limitations is missing)"
3. Agent re-runs with explicit checklist verification

**Prevention:** Template checklist (above) ensures all sections present before finalizing

---

**Error 2: D069 Dual-Scale Interpretation Missing (Trajectory RQ)**

**Symptom:** Trajectory RQ summary.md interprets only theta scale, omits probability scale

**Diagnosis:** Agent didn't recognize RQ as trajectory type requiring D069

**Solution:**
1. Master checks 2_plan.md: Does RQ analyze time/forgetting? If YES → trajectory RQ
2. Master prompts agent: "This is a trajectory RQ analyzing forgetting over time. Apply Decision D069 dual-scale interpretation guidance from results.md template Section 3.3"
3. Agent adds dedicated D069 subsection with theta + probability + why both matter

**Prevention:** rq_planner agent should flag trajectory RQs in 2_plan.md (e.g., "Note: Trajectory RQ, D069 dual-scale reporting required")

---

**Error 3: Example Content Copied Verbatim**

**Symptom:** Summary.md contains exact example text from template (e.g., "Bird & Burgess, 2008" when that citation irrelevant)

**Diagnosis:** Agent copied template examples instead of generating RQ-specific content

**Solution:**
1. Master identifies copied text (cross-reference with results.md template examples)
2. Master prompts agent: "Examples in results.md template are ILLUSTRATIVE ONLY. Generate RQ-specific content based on actual data files and context_dumps, do not copy example text verbatim"
3. Agent regenerates with original content

**Prevention:** Template states "Examples below are GENERIC (not RQ 5.1-specific) - use as structural models, populate with YOUR RQ's actual findings"

---

**Error 4: Synthesis from Wrong Sources**

**Symptom:** Interpretation section cites findings not present in this RQ's outputs (hallucinated statistics)

**Diagnosis:** Agent synthesized from memory/training instead of reading actual result files

**Solution:**
1. Master cross-checks Section 1 statistics against data/*.csv files (read with pandas.head())
2. Master identifies hallucinated values: "β = 0.045 reported, but lmm_results.csv shows β = 0.023"
3. Master prompts agent: "Re-read data/lmm_results.csv using pandas, extract EXACT values from file, do not estimate or recall from context"
4. Agent regenerates with file-verified statistics

**Prevention:** agent_best_practices.md circuit breaker: "NEVER report statistics not directly read from result files. If value not in file, state 'Value not available in outputs' rather than estimating"

---

**Error 5: Overly Long Summary (>5000 words)**

**Symptom:** Summary.md becomes comprehensive report (15+ pages) instead of concise summary

**Diagnosis:** Agent included excessive detail (all LMM coefficients, every item parameter, etc.)

**Solution:**
1. Master assesses length: >5000 words is excessive (typical: 2000-3500 words)
2. Master prompts agent: "Condense summary.md to 2000-3500 words. Report KEY findings (main effects, interactions, critical plots) not exhaustive results. Details available in data files for readers needing full output"
3. Agent creates condensed version focusing on highlights

**Prevention:** Template guidance: "Summary is NARRATIVE SYNTHESIS not raw data dump. Report key findings, refer readers to data/*.csv for full parameter sets"

---

## Integration with Other V4.X Components

### Upstream Dependencies

**rq_results agent reads:**
1. `docs/v4/templates/results.md` ← This template (structure guidance)
2. `status.yaml` (all 9 prior RQ-specific agents' context_dumps)
3. `results/chX/rqY/docs/1_concept.md` (original hypothesis, theory)
4. `results/chX/rqY/docs/2_plan.md` (expected outputs, analysis steps)
5. `results/chX/rqY/data/*.csv` (statistical outputs)
6. `results/chX/rqY/plots/*.png` (visualizations)
7. `results/chX/rqY/logs/*.log` (execution notes, warnings)

### Downstream Usage

**summary.md used by:**
1. **Master claude:** Final RQ review, approve/request revisions
2. **Thesis writing:** Copy key findings into dissertation narrative
3. **User:** Publication-ready results summary for manuscripts
4. **Future RQs:** Cross-reference when building on prior findings (e.g., RQ 5.2 cites RQ 5.1 purification results)

### Workflow Position

**Step 17 (Final Step):**

```
Step 15: rq_plots generates plots.py
Step 16: Master runs plots.py (creates PNG files)
Step 17: rq_results reads template + all inputs → creates summary.md ← YOU ARE HERE
```

After Step 17:
- Master reviews summary.md for completeness
- If approved: RQ marked COMPLETE
- If revisions needed: Master provides feedback, rq_results regenerates

---

## V3.0 vs V4.X Differences

### V3.0 Results Format (Monolithic info.md)

**File:** `results/chX/rqY/info.md` (11 sections, ~2000 lines)

**Structure:**
1. RQ Description (what/why/how)
2. Data Source (extraction specs)
3. Statistical Methods (IRT, LMM, CTT)
4. Tool Specifications (which functions used)
5. Analysis Plan (step-by-step workflow)
6. Validation Procedures (assumptions checked)
7. **Statistical Findings** (embedded in monolithic doc)
8. **Plot Descriptions** (embedded)
9. **Interpretation** (embedded)
10. **Limitations** (embedded)
11. **Next Steps** (embedded)

**Problem:** Results (sections 7-11) buried in massive specification document, hard to extract publication-ready summary

### V4.X Results Format (Atomic summary.md)

**File:** `results/chX/rqY/results/summary.md` (~800-1200 lines)

**Structure:** ONLY the 5 results sections (Findings, Plots, Interpretation, Limitations, Next Steps)

**Separation:**
- Concept → `1_concept.md` (RQ description, hypothesis, theory)
- Plan → `2_plan.md` (analysis steps, expected outputs)
- Tools → `3_tools.yaml` (tool specifications)
- Analysis → `4_analysis.yaml` (analysis + validation calls)
- **Results → `summary.md`** (JUST the synthesis narrative)

**Benefit:** Summary.md is clean, publication-ready, extractable for thesis/manuscripts without navigating specifications

### Migration Notes

**For agents transitioning from v3.0:**

- V3.0 `info.md` sections 7-11 → V4.X `summary.md` entire file
- V3.0 monolithic → V4.X atomic (each concern separated)
- V3.0 template-driven → V4.X results-driven (synthesis not just filling template)

**For users:**
- V3.0: Read info.md, scroll to "Statistical Findings" section (buried in middle)
- V4.X: Open summary.md directly (entire file is results)

---

## Implementation Notes

### For rq_results Agent Developers

**Critical Implementation Details:**

1. **Read Template BEFORE Creating Output:**
   - Step 4 in rq_results workflow: Read this template file
   - Understand structure THEN generate content (not vice versa)

2. **Pandas for Data Preview:**
   - Use `pandas.read_csv().head()` to preview data files
   - Extract key values programmatically (don't manually transcribe)
   - Verify values present in file before reporting

3. **Context_dump Synthesis:**
   - status.yaml has 10 prior agents' context_dumps
   - Each contains concise summary of that agent's work
   - Use context_dumps to understand WHAT was done without re-reading all docs

4. **Dual-Scale Detection:**
   - Check 2_plan.md: Does RQ analyze time/forgetting/trajectories?
   - If YES → trajectory RQ → apply D069 dual-scale interpretation
   - If NO → standard interpretation (no dual-scale needed)

5. **Example Usage:**
   - Template examples are GENERIC (IRT + LMM trajectory analysis)
   - Use examples as STRUCTURAL MODELS (how to format, what to include)
   - NEVER copy example content verbatim (generate RQ-specific text)

6. **Length Target:**
   - Summary.md should be 2000-3500 words (readable narrative)
   - Too short (<1500 words): Likely missing detail
   - Too long (>5000 words): Excessive, condense to highlights

### For Master Claude Reviewers

**What to Check:**

1. **Completeness:** All 5 sections present? (Use checklist above)
2. **Accuracy:** Statistics match data/*.csv files? (Spot-check 3-5 values)
3. **D069 Compliance:** Trajectory RQ has dual-scale interpretation?
4. **Theoretical Alignment:** Interpretation consistent with 1_concept.md hypothesis?
5. **Honest Limitations:** Section 4 acknowledges real constraints?
6. **Logical Next Steps:** Section 5 feasible and specific?

**Approval Criteria:**

- ✅ All sections present and complete
- ✅ No hallucinated statistics (all values file-verified)
- ✅ D069 applied correctly (if trajectory RQ)
- ✅ Publication-ready quality (clear, concise, professional)
- ✅ Theoretical interpretation sound (aligns with literature and hypothesis)

If ALL criteria met → APPROVE (mark RQ complete)

If ANY criteria unmet → REQUEST REVISIONS (specific feedback to agent)

---

## Version History

### Version 1.0 (2025-11-17)

**Created:** Phase 2 Templates (T11 completion)

**Design Decisions:**
- Comprehensive scope (800-1000 lines, consistent with T7-T10)
- Section-level examples (not complete summary.md, maintains TDD philosophy)
- D069 dedicated subsection in Interpretation (for ~40 trajectory RQs)
- Explicit workflow integration (like T7-T10 pattern)

**Specification Compliance:**
- Section 4.4.2: All 5 required sections documented ✓
- Section 2.5.2: rq_results workflow integrated ✓
- Decision D069: Dual-scale interpretation guidance included ✓
- Template consistency: Matches T7-T10 comprehensive pattern ✓

**Total Length:** 933 lines (within 800-1000 target)

**Status:** Ready for rq_results agent implementation

---

**End of Template Specification**
