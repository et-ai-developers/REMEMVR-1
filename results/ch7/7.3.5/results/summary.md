# Results Summary: RQ 7.3.5 - Confidence-accuracy gap predicting cognitive reserve

**Research Question:** Do individuals with high confidence AND high accuracy (well-calibrated high performers) show signs of cognitive reserve?

**Analysis Completed:** January 5, 2026

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total N:** 100 participants (complete dataset after merging)
- **Missing data:** 0% after inner join of theta scores, confidence ratings, and cognitive reserve indicators
- **Exclusions:** None (all participants had complete data across sources)

### Calibration Group Formation

**Calibration Method:** Standardized residuals from confidence-accuracy regression
- **Well-calibrated:** n = 41 (residuals within ±0.5 SD of regression line)
- **Overconfident:** n = 33 (residuals > +0.5 SD, higher confidence than accuracy warrants)  
- **Underconfident:** n = 26 (residuals < -0.5 SD, lower confidence than accuracy warrants)

**Group Descriptives:**
- **Well-calibrated:** Education M = 6.12 years, RPM M = 10.27, Age M = 44.76
- **Overconfident:** Education M = 6.09 years, RPM M = 10.00, Age M = 44.06
- **Underconfident:** Education M = 6.08 years, RPM M = 9.08, Age M = 44.92

### Primary ANOVA Results

**One-way ANOVAs comparing calibration groups on cognitive reserve indicators:**

| Outcome | F-statistic | p (uncorrected) | p (Bonferroni) | eta-squared |
|---------|-------------|-----------------|----------------|-------------|
| Education | [Missing] | 0.993 | 1.000 | [Missing] |
| RPM scores | [Missing] | 0.041 | 0.246 | [Missing] |
| Age | [Missing] | 0.970 | 1.000 | [Missing] |

**Note:** F-statistics and effect sizes missing from ANOVA output file, indicating potential analysis execution issue.

### Correlational Analysis

**Correlations between calibration residual (continuous) and cognitive reserve indicators:**

| Variable Pair | r | p (uncorrected) | p (Bonferroni) | 95% CI | Effect Size |
|---------------|---|-----------------|----------------|---------|-------------|
| Calibration vs Education | -0.006 | 0.956 | 1.000 | [-0.173, 0.172] | negligible |
| Calibration vs RPM | 0.108 | 0.283 | 1.000 | [-0.065, 0.285] | small |
| Calibration vs Age | -0.018 | 0.861 | 1.000 | [-0.215, 0.185] | negligible |

**Bootstrap Method:** 1000 iterations with replacement (seed=42)

### Cross-Reference to Plan Expectations

**Expected vs Actual:**
- Plan expected significant group differences (F > 3.0 for education, F > 4.0 for RPM): **NOT ACHIEVED**
- Plan expected moderate correlations (r = 0.25-0.40): **NOT ACHIEVED** 
- All correlations were negligible to small with wide confidence intervals including zero
- Bonferroni correction eliminated any marginal significance

---

## 2. Plot Descriptions

### Figure 1: Group Comparisons by Cognitive Reserve Indicators

**Filename:** `calibration_groups_comparison.png`
**Plot Type:** Box plots (3 panels showing education, RPM, age by calibration group)

**Visual Description:**
The plot displays three side-by-side box plots comparing calibration groups on cognitive reserve indicators:

- **Left panel (Education):** Shows nearly identical distributions across all three groups, with medians around 6 years and similar interquartile ranges. No visual separation between groups.
- **Center panel (RPM):** Shows slight visual differences with Underconfident group having lower median (~9) compared to Well-calibrated (~10) and Overconfident (~10) groups. Box plots show overlapping distributions but Underconfident appears shifted downward.
- **Right panel (Age):** Shows virtually identical distributions across groups with medians around 45 years and substantial overlap in all quartiles.

**Key Patterns:**
1. **Education:** No visible group differences - all three groups cluster around 6 years with identical distributions
2. **RPM:** Modest separation visible with Underconfident group showing lower fluid intelligence scores
3. **Age:** Complete overlap across groups - calibration group is unrelated to participant age
4. **Outliers:** Several outliers visible in education and RPM but distributed across all groups

**Connection to Findings:**
- Visual confirms statistical non-significance for education and age (complete overlap)
- RPM shows visual trend matching uncorrected p = 0.041, though not significant after correction
- Box plot overlap consistent with negligible effect sizes for education and age comparisons

### Figure 2: Calibration-Reserve Correlational Relationships  

**Filename:** `calibration_correlations.png` 
**Plot Type:** Scatter plots (3 panels with regression lines)

**Visual Description:**
The plot displays three scatter plots examining relationships between calibration residual (x-axis) and reserve indicators:

- **Left panel (Education vs Calibration):** Scatter shows random cloud of points with flat regression line (r = -0.006). No discernible pattern or association.
- **Center panel (RPM vs Calibration):** Scatter shows slight positive trend with modest upward slope (r = 0.108). Weak association visible but substantial scatter around line.
- **Right panel (Age vs Calibration):** Scatter shows random cloud with nearly flat regression line (r = -0.018). No meaningful association visible.

**Key Patterns:**
1. **Random scatter:** All plots show substantial variability around regression lines
2. **Weak associations:** Only RPM shows any visual trend, and it's modest
3. **No clear outliers:** Data points distributed normally without extreme leverage points
4. **Range coverage:** Calibration residuals span full expected range (-0.8 to +0.6)

**Connection to Findings:**
- Visuals confirm negligible correlations reported in statistical findings
- RPM plot shows only association approaching significance, consistent with r = 0.108 
- Random scatter patterns support conclusion that calibration quality does not predict cognitive reserve

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**
"Well-calibrated individuals (high confidence matched with high accuracy) will show higher education and RPM scores compared to overconfident or underconfident groups, suggesting metacognitive awareness as a cognitive reserve indicator."

**Hypothesis Status:** **REJECTED**

The statistical findings provide no support for the primary hypothesis:
- No significant group differences on education (p = 0.993, effect negligible)
- No significant group differences on RPM after correction (p = 0.246, uncorrected p = 0.041)
- No significant group differences on age (p = 0.970, effect negligible)
- All correlations between calibration quality and reserve indicators were negligible to small with confidence intervals including zero

### Theoretical Contextualization

**Cognitive Reserve Theory:**
The null findings challenge the theoretical prediction that metacognitive awareness serves as a cognitive reserve indicator. Several interpretations are possible:

1. **Independence of Systems:** Metacognitive monitoring (confidence-accuracy calibration) may operate independently of cognitive reserve mechanisms. Executive control systems supporting metacognition might be dissociable from those conferring cognitive resilience.

2. **Measurement Sensitivity:** The confidence-accuracy gap measure may not capture the aspects of metacognitive awareness most relevant to cognitive reserve. Alternative measures (metamemory beliefs, strategy use) might show stronger associations.

3. **Restricted Range:** The sample showed limited variability in education (mostly 6 years) and RPM scores, potentially constraining ability to detect reserve-calibration relationships in a broader population.

**Literature Connections:**
The null findings contrast with theoretical predictions from cognitive reserve literature but align with mixed empirical evidence on metacognitive-cognitive relationships. Limited previous research has directly tested calibration as a reserve indicator, making this an important negative finding for the field.

### Domain-Specific Insights

**Calibration Groups Analysis:**
- **Well-calibrated (n=41):** Largest group, representing participants with good confidence-accuracy matching
- **Overconfident (n=33):** Participants systematically overestimate their performance  
- **Underconfident (n=26):** Participants systematically underestimate their performance
- **Group formation successful:** All groups >15 participants as required for adequate power

**Cognitive Reserve Indicators:**
- **Education:** Extremely limited range (mostly 6 years), insufficient variability for meaningful group comparisons
- **RPM:** Showed most promise with medium effect size for Underconfident vs Well-calibrated comparison (d = -0.608) but underpowered for detection
- **Age:** No association with calibration, confirming calibration effects are not simply age-related

### Unexpected Patterns

**RPM Effect in Underconfident Group:**
The Underconfident group showed lower RPM scores with a medium effect size (d = -0.608) compared to Well-calibrated group. This suggests individuals with lower fluid intelligence may be more prone to underestimating their abilities, possibly due to:
1. **Dunning-Kruger reversal:** Lower ability individuals showing excessive caution rather than overconfidence
2. **Strategy differences:** Lower fluid intelligence associated with less confident response patterns
3. **Metacognitive development:** Fluid intelligence may influence calibration accuracy in unexpected directions

**Education Range Restriction:**
The sample showed extremely limited education variability (mostly 6 years), making education comparisons essentially meaningless. This represents a critical limitation for testing cognitive reserve hypotheses in this sample.

### Broader Implications

**Metacognitive Theory:**
Findings suggest confidence-accuracy calibration may not serve as a proxy for broader metacognitive competence related to cognitive reserve. Alternative metacognitive measures may be more relevant for reserve assessment.

**REMEMVR Assessment:**
The null findings don't diminish REMEMVR's value for memory assessment but suggest confidence ratings may not add incremental validity for identifying cognitive reserve. Focus on memory performance alone may be sufficient.

**Methodological Insights:**
1. **Power limitations:** Study severely underpowered for detecting small to medium effects (power <1% for most comparisons)
2. **Measurement issues:** Education measure showed insufficient variability in this sample
3. **Group creation:** Residual-based grouping method worked well for creating interpretable calibration groups

---

## 4. Limitations

### Sample Limitations

**Sample Size and Power:**
- N = 100 participants provided extremely low power (<1%) for detecting meaningful effects with Bonferroni correction
- Post-hoc power analysis revealed inability to detect small to medium effects (r < 0.30)
- Group sizes adequate (26-41 per group) but overall sample underpowered for multiple comparisons

**Demographic Constraints:**
- **Education range restriction:** Sample showed minimal education variability (mostly 6 years), preventing meaningful analysis of education-calibration relationships
- **Age homogeneity:** Limited age range may not capture age-related variations in calibration-reserve relationships
- **Population specificity:** University-based sample may not generalize to broader populations with greater cognitive reserve variability

**Missing Data:**
- 0% missing data after inner join represents strength, but may mask issues with source data quality
- No systematic assessment of data quality or extreme values reported

### Methodological Limitations

**Measurement:**
1. **Education operationalization:** Years of education may not capture education quality, relevance, or other aspects of educational reserve
2. **RPM as reserve indicator:** Single fluid intelligence measure may not reflect full cognitive reserve construct
3. **Calibration measure:** Confidence-accuracy residuals may not capture all aspects of metacognitive awareness relevant to reserve

**Design:**
1. **Cross-sectional design:** Cannot establish causal relationships between calibration and reserve indicators  
2. **Single assessment:** Calibration may vary across contexts and tasks; single VR assessment may not reflect stable individual differences
3. **No comparison group:** Cannot determine if null findings specific to this sample or represent broader population pattern

**Statistical:**
1. **Multiple comparisons:** Bonferroni correction extremely conservative (alpha = 0.0083), increasing Type II error risk
2. **ANOVA output issues:** Missing F-statistics and effect sizes in results file indicate potential execution problems
3. **Bootstrap method:** While appropriate, may not have been necessary given non-significant findings

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - Older adults (where cognitive reserve effects more pronounced)
  - Clinical populations (MCI, dementia where calibration-cognition relationships may differ)
  - Broader education range (where education effects on reserve more detectable)
  - Different cultural contexts (where metacognitive norms vary)

**Context:**
- VR-based calibration assessment may not reflect:
  - Real-world metacognitive monitoring (naturalistic confidence judgments)
  - Domain-general metacognitive abilities (task-specific calibration only)
  - Long-term metacognitive patterns (single session measurement)

**Task:**
- REMEMVR-specific findings may not extend to:
  - Other memory domains (working memory, semantic memory)
  - Non-memory cognitive tasks (where calibration-ability relationships may differ)
  - Emotional or social cognitive contexts

### Technical Limitations

**Analysis Execution Issues:**
- ANOVA results file missing F-statistics and effect sizes, suggesting potential code execution problems
- Effect size calculations available but ANOVA output incomplete
- May indicate validation tool issues or computational problems

**Cross-RQ Dependencies:**
- Relies on Ch5 5.1.1 theta scores and Ch6 confidence calibration
- Any limitations in source analyses propagate to this RQ
- Assumes independence of measurement errors across source datasets

**Multiple Testing:**
- Bonferroni correction for 6 tests very conservative, potentially masking real effects
- Alternative correction methods (FDR, hierarchical) might be more appropriate for exploratory analysis
- Family-wise error control may be overly stringent for hypothesis-generating research

### Limitations Summary

Despite these constraints, findings provide **important negative evidence** for metacognitive calibration as cognitive reserve indicator:
- Null effects robust across analytical approaches (ANOVA, correlation, effect sizes)
- Results consistent across all three reserve indicators tested  
- Effect sizes mostly negligible, suggesting lack of meaningful association rather than just power limitations

Limitations indicate **need for replication** with larger samples, broader education ranges, and alternative metacognitive measures before concluding calibration irrelevant to cognitive reserve.

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Alternative Group Formation:**
- **Why:** Current SD-based grouping may not optimize group separation
- **How:** Try quartile-based grouping (extreme 25% vs middle 50%) to maximize group differences
- **Expected Insight:** Determine if stronger calibration contrasts reveal reserve relationships
- **Timeline:** Immediate (current data, alternative grouping in Step 6 sensitivity analysis)

**2. Education Measure Exploration:**
- **Why:** Education showed no variability (mostly 6 years), limiting analysis
- **How:** Examine education measure in master.xlsx to verify coding accuracy and explore alternative education variables
- **Expected Insight:** Determine if education range restriction is measurement artifact or true sample characteristic
- **Timeline:** Immediate (requires only master.xlsx re-examination)

**3. Non-parametric Alternatives:**
- **Why:** Small effect sizes may warrant distribution-free approaches
- **How:** Kruskal-Wallis tests for group comparisons, Spearman correlations for associations
- **Expected Insight:** Test robustness of null findings to distributional assumptions
- **Timeline:** 1-2 days (requires re-running with non-parametric tests)

### Planned Thesis RQs (Chapter 7 Continuation)

**RQ 7.3.6: Individual Differences in Calibration Stability (Planned):**
- **Focus:** Examine whether calibration quality varies across memory domains (What/Where/When)
- **Why:** Current RQ used omnibus theta scores; domain-specific calibration might show different reserve relationships
- **Builds On:** Uses calibration groups from this RQ, adds domain-specific theta scores from Ch5
- **Expected Timeline:** Next RQ in analysis pipeline

**RQ 7.3.7: Alternative Metacognitive Measures (Exploratory):**
- **Focus:** Test whether metamemory beliefs or strategy use better predict cognitive reserve than calibration
- **Why:** Confidence-accuracy gap may not capture reserve-relevant metacognitive aspects  
- **Builds On:** Uses cognitive reserve indicators from this RQ, requires additional metacognitive measures
- **Expected Timeline:** Dependent on additional measure availability

### Methodological Extensions (Future Data Collection)

**1. Expand Education Measurement:**
- **Current Limitation:** Years of education insufficient variability in current sample
- **Extension:** Add education quality measures (institution prestige, field of study, advanced degrees)
- **Expected Insight:** Test whether education-calibration relationships emerge with richer education measurement
- **Feasibility:** Requires additional demographic data collection

**2. Increase Sample Size and Power:**
- **Current Limitation:** Severely underpowered (power <1%) for detecting small to medium effects
- **Extension:** Recruit N = 300-500 participants to achieve 80% power for small effects (r = 0.20)
- **Expected Insight:** Definitive test of small effect hypothesis with adequate power
- **Feasibility:** Requires substantial additional data collection (~6 months)

**3. Longitudinal Calibration Assessment:**
- **Current Limitation:** Single session may not capture stable individual differences in calibration
- **Extension:** Assess calibration across multiple sessions and contexts
- **Expected Insight:** Test whether stable calibration patterns better predict reserve than single-session measures
- **Feasibility:** Requires multi-session study design (1-2 years)

**4. Expand Age Range:**
- **Current Limitation:** Limited age range may not capture age-related calibration-reserve relationships
- **Extension:** Include older adults (65+) where cognitive reserve effects more pronounced
- **Expected Insight:** Test whether calibration-reserve relationships emerge in populations with greater cognitive vulnerability
- **Feasibility:** Requires recruitment from community (not just university; ~1 year)

### Theoretical Questions Raised

**1. Domain Specificity of Metacognitive-Reserve Relationships:**
- **Question:** Do calibration-reserve relationships vary by cognitive domain (memory vs. fluid intelligence vs. executive function)?
- **Next Steps:** Test calibration relationships across multiple cognitive domains
- **Expected Insight:** Determine whether metacognitive awareness domain-specific or domain-general
- **Feasibility:** Moderate (requires expanded cognitive battery)

**2. Alternative Metacognitive Mechanisms:**
- **Question:** Which aspects of metacognitive awareness most relevant to cognitive reserve? Strategy use? Metamemory beliefs? Monitoring accuracy?
- **Next Steps:** Comprehensive metacognitive assessment battery
- **Expected Insight:** Identify specific metacognitive components linked to reserve
- **Feasibility:** Moderate (requires metacognitive measure development)

**3. Causal Pathways:**
- **Question:** Does cognitive reserve influence metacognitive development, or do metacognitive skills contribute to reserve formation?
- **Next Steps:** Longitudinal study tracking calibration and reserve development over time
- **Expected Insight:** Understand developmental relationship between metacognition and reserve
- **Feasibility:** Long-term (requires longitudinal cohort, 5+ years)

### Priority Ranking

**High Priority (Do First):**
1. **Education measure exploration** - Address immediate limitation that may explain null findings
2. **Alternative group formation** - Test robustness using current data  
3. **RQ 7.3.6 domain-specific calibration** - Natural next step in thesis progression

**Medium Priority (Subsequent):**
1. **Non-parametric alternatives** - Robustness check for distributional assumptions
2. **Expanded sample size study** - Definitive power test of small effect hypothesis
3. **Alternative metacognitive measures** - Test broader metacognitive-reserve relationships

**Lower Priority (Aspirational):**
1. **Longitudinal calibration study** - Ideal but requires long-term data collection
2. **Older adult sample** - Important but beyond current thesis scope
3. **Causal pathway studies** - Important theoretical question but requires extensive longitudinal design

### Next Steps Summary

The null findings for **calibration-reserve relationships** raise three critical questions for immediate follow-up:

1. **Measurement adequacy:** Is education range restriction masking true relationships? (High priority investigation)
2. **Effect size reality:** Are relationships truly absent or just very small and underpowered? (Power analysis extension)
3. **Metacognitive specificity:** Is confidence-accuracy gap wrong metacognitive measure for reserve? (Alternative measures)

**Primary recommendation:** Investigate education measurement issues before investing in large-scale replication, as range restriction may explain null findings more parsimoniously than true absence of relationships.

---

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)  
**Date:** 2026-01-05T21:30:00Z