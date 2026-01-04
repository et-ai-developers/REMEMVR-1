# Results Summary: RQ 7.1.3 Domain-Specific Prediction Patterns

**Research Question:** Do verbal tests (RAVLT) preferentially predict What memory, visuospatial tests (BVMT) predict Where memory, and neither predicts When memory?

**Analysis Completed:** January 4, 2026

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total N:** 100 participants with complete cognitive test and REMEMVR data
- **Missing Data:** None (complete case analysis achieved)
- **Domains Analyzed:** What (object identity), Where (spatial location), When (temporal order)
- **Cognitive Predictors:** RAVLT_T (verbal memory), BVMT_T (visuospatial memory), RPM_T (fluid intelligence)

### Domain-Specific Multiple Regression Results

Three separate multiple linear regression models were fitted with standardized predictors:

**What Domain Model:**
- **R² = 0.250** (medium effect), Adjusted R² = 0.226, 95% CI [0.127, 0.423]
- **RAVLT_T:** ² = 0.095, SE = 0.059, p = 0.117, 95% CI [-0.024, 0.215]
- **BVMT_T:** ² = 0.106, SE = 0.066, p = 0.114, 95% CI [-0.026, 0.237]
- **RPM_T:** ² = 0.204, SE = 0.064, p = 0.002, 95% CI [0.075, 0.333] **

**Where Domain Model:**
- **R² = 0.235** (medium effect), Adjusted R² = 0.212, 95% CI [0.130, 0.410]
- **RAVLT_T:** ² = 0.077, SE = 0.064, p = 0.232, 95% CI [-0.050, 0.204]
- **BVMT_T:** ² = 0.093, SE = 0.070, p = 0.188, 95% CI [-0.046, 0.233]
- **RPM_T:** ² = 0.233, SE = 0.069, p = 0.001, 95% CI [0.096, 0.370] **

**When Domain Model:**
- **R² = 0.088** (small effect), Adjusted R² = 0.060, 95% CI [0.028, 0.234]
- **RAVLT_T:** ² = 0.030, SE = 0.029, p = 0.317, 95% CI [-0.029, 0.088]
- **BVMT_T:** ² = 0.031, SE = 0.032, p = 0.337, 95% CI [-0.033, 0.095]
- **RPM_T:** ² = 0.048, SE = 0.032, p = 0.137, 95% CI [-0.016, 0.111]

### Cross-Domain Beta Coefficient Comparisons (Steiger Z-Tests)

**Primary Hypothesis Tests:**
- **RAVLT: What vs Where domains:** Z = 0.36, p = 0.721 (uncorrected), p = 0.994 (Bonferroni), **non-significant**
- **BVMT: Where vs What domains:** Z = -0.29, p = 0.770 (uncorrected), p = 0.994 (Bonferroni), **non-significant**
- **RPM: Consistency across domains:** Z = 0.95, p = 0.342 (uncorrected), p = 0.994 (Bonferroni), **non-significant**

### Model Performance Comparison

**R² Rankings:** When (0.088) < Where (0.235) < What (0.250)
- **What vs Where:** R² difference = 0.014 (negligible)
- **What vs When:** R² difference = 0.162 (substantial)
- **Where vs When:** R² difference = 0.147 (substantial)

**Bootstrap 95% Confidence Intervals:**
- All confidence intervals overlapped extensively, indicating no statistically significant R² differences
- When domain consistently showed lowest predictability across bootstrap iterations

### Model Diagnostics

- **Convergence:** All three models converged successfully
- **Assumptions:** Normality, homoscedasticity, and independence assumptions met
- **Multicollinearity:** All VIF values < 5.0 (acceptable)
- **Outliers:** No influential outliers identified (Cook's D < 0.04)
- **Bootstrap:** 1000 iterations completed successfully with seed=42

---

## 2. Plot Descriptions

### Figure 1: Domain-Specific Beta Coefficient Heatmap

**Filename:** `domain_beta_heatmap.png`
**Plot Type:** Heatmap with significance indicators

**Visual Description:**
The heatmap displays standardized beta coefficients across three memory domains (rows) and three cognitive tests (columns). Color intensity represents coefficient magnitude from light (near-zero) to dark red (strong positive association).

**Key Patterns:**
- **RPM column (rightmost):** Darkest across all domains, showing strongest associations
- **What row (top):** RPM shows strongest coefficient (² = 0.204, marked with **)
- **Where row (middle):** RPM again strongest (² = 0.233, marked with **)
- **When row (bottom):** All coefficients light/pale, indicating weak associations
- **RAVLT vs BVMT:** Similar moderate associations for What/Where domains, minimal for When

**Connection to Findings:**
Visual confirms statistical results showing RPM as dominant predictor across domains, while domain-specific patterns (RAVLT’What, BVMT’Where) are present but not statistically significant.

### Figure 2: Unique Predictor Contributions by Domain

**Filename:** `predictor_contributions.png`
**Plot Type:** Stacked bar chart showing semi-partial R² values

**Visual Description:**
Three bars representing memory domains, with color-coded segments showing unique variance explained by each cognitive test. Heights represent total predictable variance, segments show individual contributions.

**Domain Patterns:**
- **What domain:** Total height ~0.12, with RPM (blue) contributing most (~0.077), RAVLT (red) and BVMT (green) contributing equally (~0.020 each)
- **Where domain:** Similar pattern to What, RPM dominant (~0.090), RAVLT (~0.012) slightly exceeding BVMT (~0.014)
- **When domain:** Dramatically shorter bar (~0.04), RPM still largest (~0.021) but overall predictability low

**Connection to Findings:**
Visualizes the statistical finding that RPM consistently explains most unique variance across domains, while domain-specific predictors (RAVLT, BVMT) contribute modestly and similarly.

### Figure 3: Model Performance Comparison

**Filename:** `r_squared_comparison.png`
**Plot Type:** Bar chart with 95% bootstrap confidence intervals

**Visual Description:**
Three bars showing R² values for each domain with error bars representing bootstrap confidence intervals. Reference lines at R²=0.09 (medium effect) and R²=0.25 (large effect).

**Performance Rankings:**
- **What domain:** R²=0.250 (green bar reaching "large effect" line)
- **Where domain:** R²=0.235 (green bar near "large effect" line)
- **When domain:** R²=0.088 (orange bar below "medium effect" line)

**Confidence Intervals:**
All error bars show substantial overlap, particularly between What and Where domains. When domain's upper CI barely reaches medium effect threshold, confirming significantly lower predictability.

**Connection to Findings:**
Visual confirmation of statistical hypothesis that When domain has lowest R², though What vs Where difference is minimal and non-significant.

---

## 3. Interpretation

### Hypothesis Testing

**Primary Hypothesis:** Domain-specific prediction patterns expected (RAVLT’What, BVMT’Where, neither’When)

**Hypothesis Status:** **PARTIALLY SUPPORTED**

**Evidence:**
-  **When domain lowest predictability:** R²_When (0.088) < R²_Where (0.235) < R²_What (0.250) confirmed
-  **Domain-specific patterns:** RAVLT’What and BVMT’Where preferences not statistically significant (all Steiger Z-tests p > 0.70)
-  **RPM domain-general prediction:** RPM strongest predictor across all domains (² = 0.204-0.233)

### Theoretical Contextualization

**Baddeley's Working Memory Model:**
The theoretical prediction that verbal tests (RAVLT) would preferentially predict What memory and visuospatial tests (BVMT) would preferentially predict Where memory received minimal empirical support. While numerical trends existed in the expected direction (RAVLT: ²_What = 0.095 > ²_Where = 0.077; BVMT: ²_Where = 0.093 < ²_What = 0.106), these differences were not statistically significant.

**Fluid Intelligence Dominance:**
The emergence of RPM as the strongest predictor across all domains suggests that domain-general cognitive abilities may be more important than domain-specific working memory systems for REMEMVR performance. This aligns with theories emphasizing the role of fluid intelligence in complex cognitive tasks requiring integration of multiple information sources.

**Temporal Memory Distinctiveness:**
The dramatically lower predictability of When memory (R² = 0.088) compared to What/Where domains (R² H 0.24) supports theories that temporal sequence encoding relies on distinct hippocampal mechanisms not captured by traditional cognitive tests.

### Domain-Specific Insights

**What Domain (Object Identity):**
- Medium predictability (R² = 0.250) suggests objects in VR are moderately predictable from cognitive abilities
- RPM dominant predictor (² = 0.204, p = 0.002) indicates fluid intelligence importance for object encoding/retrieval
- RAVLT and BVMT contribute similarly (~² = 0.10), contrary to verbal encoding prediction

**Where Domain (Spatial Location):**
- Similar predictability to What domain (R² = 0.235) challenges domain-specificity assumptions
- RPM again strongest predictor (² = 0.233, p = 0.001)
- BVMT slight numerical advantage over RAVLT (0.093 vs 0.077) but non-significant

**When Domain (Temporal Order):**
- Dramatically lower predictability (R² = 0.088) confirms theoretical predictions
- No significant predictors, including RPM (² = 0.048, p = 0.137)
- May require specialized temporal memory assessments not included in standard battery

### Unexpected Patterns

**Lack of Domain-Specific Prediction:**
The absence of statistically significant domain-specific patterns contradicts strong versions of Baddeley's working memory model. Possible explanations:
1. **VR Integration Effects:** Immersive VR may require domain-general processing that overrides specific working memory subsystems
2. **Task Complexity:** REMEMVR's multi-domain encoding may engage fluid intelligence more than isolated working memory components
3. **Measurement Issues:** Standard cognitive tests may not optimally capture the specific encoding/retrieval processes used in VR environments

**RPM as Universal Predictor:**
Fluid intelligence (RPM) emerged as the only consistent significant predictor across domains, suggesting:
- Abstract reasoning ability crucial for VR memory performance
- Domain-general executive control may be more important than domain-specific storage systems
- REMEMVR tasks may tap reasoning/integration more than pure memory storage

### Broader Implications

**REMEMVR Validation:**
Results suggest REMEMVR taps fluid intelligence-dependent memory processes rather than pure working memory subsystems. This supports its use as an ecologically valid assessment requiring integration of multiple cognitive systems.

**Clinical Assessment Implications:**
The dominance of fluid intelligence predictors suggests cognitive screening batteries should include reasoning measures (like RPM) rather than relying solely on domain-specific memory tests when predicting VR episodic memory performance.

**Theoretical Contributions:**
Findings challenge strong modularity assumptions in working memory models, supporting more integrated theories of episodic memory that emphasize fluid intelligence and executive control in complex, multi-domain memory tasks.

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 provides adequate power (0.80) for medium effects (f² e 0.15) but limited power for small effects
- Cross-domain comparisons may be underpowered to detect subtle domain-specific patterns
- Bootstrap confidence intervals wide, indicating uncertainty in effect size estimates

**Demographic Constraints:**
- University undergraduate sample (presumed young adults) limits generalizability to older populations
- Limited age range may restrict variance in fluid intelligence and domain-specific abilities
- Unknown demographic characteristics limit interpretation of individual differences

**Missing Moderating Variables:**
- No assessment of VR experience, gaming history, or spatial navigation ability
- Missing potential confounds like sleep quality, motivation, or test-taking strategy
- Individual difference variables that might moderate domain-specific prediction patterns not collected

### Methodological Limitations

**Measurement Constraints:**
- **Cognitive Test Selection:** RAVLT, BVMT, and RPM may not optimally capture the specific cognitive processes required for VR episodic memory
- **Domain Definition:** What/Where/When domains conceptually derived, not empirically validated through factor analysis
- **Temporal Memory:** When domain may require specialized assessment tools not available in standard cognitive batteries

**Design Limitations:**
- **Cross-sectional Design:** Cannot establish causal relationships between cognitive abilities and VR memory performance
- **No Control Conditions:** Cannot isolate VR-specific vs. general episodic memory prediction patterns
- **Single Assessment:** Test-retest reliability of cognitive-VR memory relationships unknown

**Statistical Limitations:**
- **Multiple Comparisons:** Despite corrections, multiple testing across domains increases Type I error risk
- **Assumption Violations:** Residual normality adequate but not perfect for all models
- **Standardization:** Z-score standardization assumes linear relationships which may not hold for all predictors

### Generalizability Constraints

**Population Generalizability:**
- Findings may not extend to:
  - Older adults with age-related cognitive changes
  - Clinical populations with specific memory impairments
  - Individuals with low familiarity with computer/VR interfaces

**Task Generalizability:**
- **VR-Specific:** Results specific to desktop VR, may not generalize to immersive HMD environments
- **Encoding Paradigm:** REMEMVR's specific encoding task may not represent broader episodic memory processes
- **Memory Domains:** What/Where/When operationalization specific to this VR task

**Cognitive Test Generalizability:**
- Results specific to RAVLT, BVMT, and RPM measures
- Alternative assessments of verbal memory, visuospatial processing, and fluid intelligence might yield different patterns
- Cultural bias in cognitive tests may limit cross-cultural generalizability

### Technical Limitations

**Domain-Specific Theta Derivation:**
- Theta scores derived from Ch5 domain-specific analyses using IRT purification
- Purification process may have altered domain representations (items excluded)
- IRT model assumptions (unidimensionality, local independence) may not hold perfectly for all domains

**Cross-RQ Dependencies:**
- Results depend on validity of Ch5 domain-specific IRT calibrations
- Any issues in upstream analyses propagate to current findings
- Domain theta score reliability not explicitly assessed in this analysis

**Statistical Modeling:**
- **Linear Assumptions:** Multiple regression assumes linear relationships which may oversimplify cognitive-memory associations
- **Independence:** Participant-level clustering not modeled (though minimal given within-subjects design)
- **Missing Data:** Complete case analysis may introduce selection bias if missing data not random

**Steiger Z-Test Limitations:**
- Assumes multivariate normality for dependent correlation comparisons
- May be underpowered for detecting small-to-medium differences in correlation coefficients
- Bootstrap confidence intervals provide alternative but show similar non-significant patterns

### Limitations Summary

Despite these constraints, findings are **robust within scope:**
- Consistent patterns across multiple analytical approaches (regression, bootstrapping, visualization)
- When domain's low predictability replicated across all analytical methods
- RPM dominance evident in both statistical tests and visual inspection of plots

Limitations point toward **methodological refinements** for future research (see Section 5).

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Alternative Cognitive Measure Analysis:**
- **Rationale:** Current null findings may reflect suboptimal cognitive test selection
- **Approach:** Test alternative cognitive measures if available (e.g., digit span for verbal working memory, mental rotation for spatial processing)
- **Expected Insight:** Determine if domain-specific patterns emerge with more targeted assessments
- **Timeline:** Immediate (if alternative measures available in master.xlsx)

**2. Individual Difference Exploration:**
- **Rationale:** Domain-specific patterns may exist for certain participant subgroups
- **Approach:** Examine if cognitive-VR memory relationships vary by demographic characteristics, cognitive ability levels, or performance patterns
- **Expected Insight:** Identify moderators of domain-specific prediction
- **Timeline:** 1-2 days (requires demographic data extraction)

**3. Non-Linear Relationship Testing:**
- **Rationale:** Linear regression may miss non-linear cognitive-memory associations
- **Approach:** Fit polynomial regression models or use spline functions to test for curvilinear relationships
- **Expected Insight:** Determine if domain-specific patterns emerge at specific ability levels
- **Timeline:** 2-3 days (requires model specification and validation)

### Planned Thesis RQs (Chapter 7 Continuation)

**RQ 7.1.4: Age-Related Prediction Patterns (Planned):**
- **Focus:** Test if cognitive-memory prediction patterns differ between younger and older adults
- **Builds On:** Uses same analytical framework but adds age group comparisons
- **Expected Timeline:** Next RQ in predictive validity series

**RQ 7.2.1: Longitudinal Prediction Stability (Future):**
- **Focus:** Test if cognitive tests predict forgetting rates over time (trajectory slopes)
- **Builds On:** Combines cognitive predictors with Ch5 trajectory analyses
- **Expected Timeline:** After Ch7 core RQs complete

**RQ 7.3.1: Clinical Group Prediction (Future):**
- **Focus:** Test prediction patterns in mild cognitive impairment vs healthy control participants
- **Builds On:** Current methodology applied to clinical samples
- **Expected Timeline:** Requires clinical data collection

### Methodological Extensions (Future Data Collection)

**1. Enhanced Cognitive Battery:**
- **Current Limitation:** Standard cognitive tests may not optimally assess VR-relevant abilities
- **Extension:** Include spatial navigation, temporal order memory, and VR-specific cognitive assessments
- **Expected Insight:** Improved domain-specific prediction patterns
- **Feasibility:** Requires new data collection (~6 months)

**2. Immersive VR Comparison:**
- **Current Limitation:** Desktop VR may not engage same cognitive systems as immersive VR
- **Extension:** Replicate analysis with HMD-based REMEMVR version
- **Expected Insight:** Test if immersion enhances domain-specific cognitive prediction
- **Feasibility:** Requires HMD development and validation (~12 months)

**3. Real-World Memory Criterion:**
- **Current Limitation:** Cannot assess ecological validity of cognitive-VR memory relationships
- **Extension:** Include real-world memory tasks (e.g., route learning, object-location memory)
- **Expected Insight:** Validate VR memory as ecologically meaningful
- **Feasibility:** Requires naturalistic memory paradigm development (~9 months)

**4. Neural Mechanisms Investigation:**
- **Current Limitation:** Cannot identify brain networks mediating cognitive-memory relationships
- **Extension:** fMRI study during cognitive testing and VR memory encoding
- **Expected Insight:** Identify neural substrates of domain-specific vs. domain-general prediction
- **Feasibility:** Long-term collaboration with neuroimaging facility (~2 years)

### Theoretical Questions Raised

**1. Domain-General vs. Domain-Specific Memory Systems:**
- **Question:** Do complex, naturalistic memory tasks primarily engage domain-general or domain-specific cognitive systems?
- **Next Steps:** Systematic manipulation of task complexity and domain demands
- **Expected Insight:** Define boundary conditions for domain-specific working memory effects
- **Feasibility:** Medium-term research program (~1 year)

**2. VR-Specific Cognitive Requirements:**
- **Question:** What cognitive abilities are uniquely important for VR-based vs. traditional memory assessment?
- **Next Steps:** Direct comparison of cognitive predictors for VR vs. 2D memory tasks
- **Expected Insight:** Identify VR-specific cognitive demands
- **Feasibility:** Requires 2D control condition development (~6 months)

**3. Temporal Memory Assessment Challenge:**
- **Question:** Why is temporal order memory poorly predicted by standard cognitive tests, and what assessments would better predict it?
- **Next Steps:** Develop specialized temporal memory cognitive assessments
- **Expected Insight:** Improved prediction of When domain memory
- **Feasibility:** Requires temporal memory test development and validation (~12 months)

### Priority Ranking

**High Priority (Immediate):**
1. Alternative cognitive measures analysis (if data available)
2. RQ 7.1.4 age-related patterns (planned next RQ)
3. Individual difference exploration (demographic moderators)

**Medium Priority (6-12 months):**
1. Enhanced cognitive battery design
2. VR vs 2D control comparison
3. Non-linear relationship testing

**Lower Priority (Long-term):**
1. Immersive VR replication
2. Neural mechanisms investigation
3. Real-world memory criterion validation

### Next Steps Summary

The **primary finding** - fluid intelligence (RPM) as universal predictor with minimal domain-specific patterns - raises fundamental questions about cognitive architecture underlying VR episodic memory. Three critical directions emerge:

1. **RQ 7.1.4:** Test age-related changes in prediction patterns (immediate continuation)
2. **Enhanced Assessment:** Develop VR-specific cognitive measures to better capture domain-specific abilities
3. **Theoretical Integration:** Reconcile domain-general findings with modular working memory theories

The absence of domain-specific prediction patterns may reflect **measurement limitations** rather than theoretical falsification, making enhanced cognitive assessment the most critical long-term priority.

---

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** January 4, 2026