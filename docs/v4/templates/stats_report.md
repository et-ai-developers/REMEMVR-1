# Statistical Validation Report Template

**File:** `docs/v4/templates/stats_report.md`
**Last Updated:** 2025-11-21
**Purpose:** Template specification for rq_stats agent statistical validation feedback
**Version:** 4.2
**Status:** Template Specification

---

## Overview

### Purpose

This template specifies the format for **statistical validation feedback** that the `rq_stats` agent writes to standalone `1_stats.md` file. The feedback uses a **10-point rubric system** (enhanced from v3.0 for production-proven rigor + devil's advocate challenges) to systematically evaluate statistical appropriateness, tool availability, parameter specification, validation procedures, and thoroughness of statistical criticism generation.

### Key Features

- **10-Point Rubric:** 5 weighted categories (Statistical Appropriateness 3pts, Tool Availability 2pts, Parameter Specification 2pts, Validation Procedures 2pts, Devil's Advocate Analysis 1pt)
- **Decision Thresholds:** APPROVED (≥9.25), CONDITIONAL (≥9.0), REJECTED (<9.0)
- **Devil's Advocate Analysis:** Two-pass WebSearch (validation + challenge) generating statistical criticisms with literature citations
- **Tool Availability Tables:** Systematic checklist format (Step | Tool Function | Status | Notes)
- **Validation Checklists:** IRT/LMM assumption tables (Assumption | Test | Threshold | Assessment)
- **Actionable Recommendations:** Required changes vs suggested improvements with exact locations
- **Metadata Footer:** Audit trail (agent version, date, tools validated, duration)

**Workflow Integration:** rq_stats reads this template (step 4), evaluates 1_concept.md against rubric criteria, reads thesis/methods.md for experimental context (step 6), conducts methodology validation, then writes standalone 1_stats.md file (step 10 using Write tool).

---

## Report Structure

### Section Sequence

Standalone file `1_stats.md` structure:

```markdown
---

## Statistical Validation Report

**Validation Date:** YYYY-MM-DD HH:MM
**Agent:** rq_stats v4.0
**Status:** ✅ APPROVED / ⚠️ CONDITIONAL / ❌ REJECTED
**Overall Score:** X.X / 10.0

---

### Rubric Scoring Summary

| Category | Score | Max | Status |
|----------|-------|-----|--------|
| Statistical Appropriateness | X.X | 3.0 | ✅/⚠️/❌ |
| Tool Availability | X.X | 2.0 | ✅/⚠️/❌ |
| Parameter Specification | X.X | 2.0 | ✅/⚠️/❌ |
| Validation Procedures | X.X | 2.0 | ✅/⚠️/❌ |
| Devil's Advocate Analysis | X.X | 1.0 | ✅/⚠️/❌ |
| **TOTAL** | **X.X** | **10.0** | **STATUS** |

---

### Detailed Rubric Evaluation

[Sections 1-5: One per rubric category]

---

### Tool Availability Validation

[Table format with tool status]

---

### Validation Procedures Checklists

[IRT and LMM assumption tables]

---

### Recommendations

[Required changes and suggested improvements]

---

### Validation Metadata

[Agent version, tools validated, duration]

---
```

---

## Section Specifications

### Section 1: Header

**Required Fields:**
- Validation Date (YYYY-MM-DD HH:MM format)
- Agent version (rq_stats v4.0)
- Status badge (✅ APPROVED / ⚠️ CONDITIONAL / ❌ REJECTED)
- Overall score (X.X / 10.0)

**Format:**
```markdown
**Validation Date:** 2025-11-16 15:00
**Agent:** rq_stats v4.0
**Status:** ✅ APPROVED
**Overall Score:** 10.0 / 10.0
```

---

### Section 2: Rubric Scoring Summary

**Purpose:** Quick overview of all 5 rubric categories with scores.

**Table Format:**
- Column 1: Category name
- Column 2: Score earned (decimal precision)
- Column 3: Maximum possible (3.0, 2.0, 2.0, 2.0, 1.0)
- Column 4: Status icon (✅ excellent ≥90%, ⚠️ acceptable ≥70%, ❌ needs work <70%)

**Example:**
```markdown
| Category | Score | Max | Status |
|----------|-------|-----|--------|
| Statistical Appropriateness | 3.0 | 3.0 | ✅ |
| Tool Availability | 2.0 | 2.0 | ✅ |
| Parameter Specification | 2.0 | 2.0 | ✅ |
| Validation Procedures | 2.0 | 2.0 | ✅ |
| Devil's Advocate Analysis | 1.0 | 1.0 | ✅ |
| **TOTAL** | **10.0** | **10.0** | **✅ APPROVED** |
```

---

### Section 3: Detailed Rubric Evaluation

**Purpose:** In-depth analysis for each of the 5 rubric categories.

**Structure (Repeat for Each Category):**

```markdown
#### [Category Name] (X.X / Y.0)

**Criteria Checklist:**
- [x] Criterion 1 description
- [x] Criterion 2 description
- [ ] Criterion 3 description (if not met)

**Assessment:**
[Paragraph evaluating this category against criteria]

**Strengths:**
- Bullet point 1
- Bullet point 2

**Concerns / Gaps:**
- Bullet point 1 (if any)
- Bullet point 2 (if any)

**Score Justification:**
[Why this specific score was assigned]
```

**Categories (see Section 5 for detailed criteria):**
1. Statistical Appropriateness (0-3 points) - includes complexity assessment
2. Tool Availability (0-2 points)
3. Parameter Specification (0-2 points)
4. Validation Procedures (0-2 points)
5. Devil's Advocate Analysis (0-1 point) - meta-scores thoroughness of criticism generation

---

### Section 4: Tool Availability Validation

**Purpose:** Document which analysis tools are available and which need implementation.

**Structure:**

```markdown
### Tool Availability Validation

**Source:** `docs/tools_inventory.md`

**Analysis Pipeline Steps:**

| Step | Tool Function | Status | Notes |
|------|---------------|--------|-------|
| Step 1: IRT Calibration | `tools.analysis_irt.calibrate_grm` | ✅ Available | Tested 49/49, API verified |
| Step 2: Item Purification | `tools.analysis_irt.purify_items` | ✅ Available | Decision D039 implementation |
| Step 3: Theta Extraction | `tools.analysis_irt.extract_theta_scores` | ✅ Available | Composite_ID stacking supported |
| Step 4: TSVR Merge | `tools.data.merge_tsvr` | ⚠️ Missing | Needs implementation (Decision D070) |
| Step 5: LMM Fitting | `tools.analysis_lmm.fit_lmm_with_tsvr` | ✅ Available | TSVR time variable support |
| Step 6: Post-Hoc Tests | `tools.analysis_lmm.post_hoc_contrasts` | ✅ Available | Decision D068 dual reporting |
| Step 7: Effect Sizes | `tools.analysis_lmm.compute_effect_sizes` | ✅ Available | Cohen's d, partial eta-squared |
| Step 8: Trajectory Plots | `tools.plotting.plot_trajectory_probability` | ✅ Available | Decision D069 dual-scale |

**Tool Reuse Rate:** [N]/[Total] tools ([X]%)

**Missing Tools (If Any):**
1. **Tool Name:** `tools.data.merge_tsvr`
   - **Required For:** Step 4 - Merge TSVR time variable with theta scores
   - **Priority:** High (required for Decision D070 compliance)
   - **Specifications:** Read TSVR from master.xlsx, merge with theta scores by composite_ID
   - **Recommendation:** Implement before rq_analysis phase

**Tool Availability Assessment:**
- ✅ Excellent (100% tool reuse): All required tools exist
- ⚠️ Acceptable (≥90% tool reuse): 1-2 tools need implementation
- ❌ Insufficient (<90% tool reuse): Multiple tools missing, significant implementation required
```

---

### Section 5: Validation Procedures Checklists

**Purpose:** Document how statistical assumptions will be validated.

**Structure:**

```markdown
### Validation Procedures Checklists

#### IRT Validation Checklist

| Assumption | Test | Threshold | Assessment |
|------------|------|-----------|------------|
| Local Independence | Q3 statistic | <0.2 | ✅ Appropriate threshold (Christensen et al., 2017) |
| Unidimensionality | Eigenvalue ratio | >3.0 | ✅ Appropriate (first eigenvalue / second eigenvalue) |
| Model Fit | RMSEA | <0.08 | ✅ Appropriate for N=400 (Hu & Bentler, 1999) |
| Item Fit | S-X² | p>0.01 (Bonferroni) | ✅ Appropriate (Orlando & Thissen, 2000) |
| Person Fit | lz statistic | \|lz\| < 2.0 | ✅ Standard threshold (Drasgow et al., 1985) |

**IRT Validation Assessment:**
[Paragraph evaluating comprehensiveness of IRT validation procedures]

**Concerns:**
- [Specific issues if any, e.g., missing assumption check, inappropriate threshold]

**Recommendations:**
- [Suggestions for improving validation procedures]

---

#### LMM Validation Checklist

| Assumption | Test | Threshold | Assessment |
|------------|------|-----------|------------|
| Residual Normality | Shapiro-Wilk | p>0.05 | ⚠️ Liberal (better: Q-Q plot visual inspection) |
| Homoscedasticity | Residual plot | Visual inspection | ✅ Appropriate (Pinheiro & Bates, 2000) |
| Random Effects Normality | Q-Q plot | Visual inspection | ✅ Standard practice |
| Independence | ACF plot | Lag-1 ACF < 0.1 | ✅ Appropriate for repeated measures |
| Linearity | Partial residual plots | Visual inspection | ✅ Appropriate |
| Outliers | Cook's distance | D > 4/n | ✅ Standard threshold (n = sample size) |

**LMM Validation Assessment:**
[Paragraph evaluating comprehensiveness of LMM validation procedures]

**Concerns:**
- [Specific issues if any]

**Recommendations:**
- [Suggestions for improving validation procedures]

---

#### Decision Compliance Validation

[If project has mandatory statistical decisions like D039, D068, D069, D070]

| Decision | Requirement | Implementation | Compliance |
|----------|-------------|----------------|------------|
| D039: 2-Pass IRT | Purify items before Pass 2 | Step 2: `purify_items()` with thresholds \|b\| ≤3.0, a ≥0.4 | ✅ FULLY COMPLIANT |
| D068: Dual Reporting | Report both uncorrected and Bonferroni p-values | Step 6: `post_hoc_contrasts()` returns both | ✅ FULLY COMPLIANT |
| D069: Dual-Scale Plots | Plot theta + probability scales | Step 8: `plot_trajectory_probability()` dual y-axes | ✅ FULLY COMPLIANT |
| D070: TSVR Pipeline | Use TSVR (hours) not nominal days | Step 5: `fit_lmm_with_tsvr()` time variable | ✅ FULLY COMPLIANT |

**Decision Compliance Assessment:**
[Paragraph evaluating compliance with project-wide mandatory decisions]
```

---

### Section 6: Recommendations

**Purpose:** Provide actionable guidance for improving 1_concept.md.

**Structure:**

```markdown
### Recommendations

#### Required Changes (Must Address for Approval)

[Only if status is CONDITIONAL or REJECTED]

1. **[Change Title]**
   - **Location:** 1_concept.md - [Section name, e.g., "Section 6: Analysis Approach, LMM subsection"]
   - **Issue:** [What's wrong or missing - be specific about statistical/methodological problem]
   - **Fix:** [Specific text to add/change/remove - provide actual wording if possible]
   - **Rationale:** [Why this change is necessary for methodological validity - reference rubric criteria]

2. **[Change Title]**
   - [Same structure]

#### Suggested Improvements (Optional but Recommended)

[Always provide, even if APPROVED]

1. **[Suggestion Title]**
   - **Location:** 1_concept.md - [Section name]
   - **Current:** [What the section says now - brief quote or summary]
   - **Suggested:** [What it could say instead - provide alternative wording]
   - **Benefit:** [Why this would enhance methodological quality - what it adds]

2. **[Suggestion Title]**
   - [Same structure]

#### Missing Tools (For Master/User Implementation)

[If any tools are missing per Tool Availability table]

1. **Tool Name:** `tools.module.function_name`
   - **Required For:** Step X - [Task description]
   - **Priority:** High / Medium / Low
   - **Specifications:** [What the tool should do - inputs, outputs, parameters]
   - **Recommendation:** Implement before [which phase]
```

---

### Section 7: Validation Metadata

**Purpose:** Audit trail and accountability.

**Structure:**

```markdown
### Validation Metadata

- **Agent Version:** rq_stats v4.0
- **Rubric Version:** 10-point system (v4.0)
- **Validation Date:** YYYY-MM-DD HH:MM
- **Tools Inventory Source:** docs/tools_inventory.md
- **Total Tools Validated:** [N]
- **Tool Reuse Rate:** [X]% ([N]/[Total] tools available)
- **Validation Duration:** ~[X] minutes
- **Context Dump:** [Terse summary for status.yaml - condensed 1-line format, exception to general 5-line rule, includes all 5 category scores]
```

---

## 10-Point Rubric System

### Category 1: Statistical Appropriateness (0-3 points)

**Weight:** 30% (most important category)

**Criteria:**
1. **Statistical approach appropriate for RQ** (0-1 pt)
   - Does the proposed method match the research question type?
   - Is the model structure appropriate for the data structure (hierarchical, longitudinal, cross-sectional)?
   - Is the analysis the simplest method that answers the RQ (appropriate complexity)?
   - Are alternatives considered and justified?

2. **Assumptions checkable with available data** (0-1 pt)
   - Can statistical assumptions be tested with REMEMVR data (N=100, 4 time points)?
   - Are sample size requirements met for proposed methods?
   - Are missing data patterns compatible with method assumptions?

3. **Methodological soundness** (0-1 pt)
   - Is the proposed approach methodologically rigorous?
   - Are known methodological pitfalls avoided?
   - Does the approach align with current statistical best practices?
   - Is unnecessary complexity avoided (parsimony)?
   - **Does NOT require Likert bias correction for confidence ratings** (per solution.md section 1.4 - preserves interpretability)

**Scoring Guide:**
- **2.7-3.0:** Exceptional - Optimal method choice with thorough justification, appropriate complexity
- **2.3-2.6:** Strong - Appropriate method with good rationale, justified complexity
- **1.8-2.2:** Adequate - Acceptable method, minor concerns about appropriateness/complexity
- **1.0-1.7:** Weak - Questionable method choice or poor justification, potential over/under-complexity
- **0.0-0.9:** Insufficient - Inappropriate method for RQ or unjustified complexity

---

### Category 2: Tool Availability (0-2 points)

**Weight:** 20%

**Criteria:**
1. **Required tools exist** (0-0.7 pts)
   - Are all required analysis tools available in `tools/` package?
   - Do tool signatures match proposed usage?
   - Is API documentation complete in `docs/tools_inventory.md`?

2. **Tool reuse rate** (0-0.7 pts)
   - What percentage of analysis steps use existing tools?
   - Are novel tool requests justified by genuinely different methodology?
   - Target: ≥90% tool reuse rate (prevents tool proliferation)

3. **Missing tools identified** (0-0.6 pts)
   - Are any missing tools clearly identified?
   - Are specifications provided for missing tools?
   - Is implementation priority assessed?

**Scoring Guide:**
- **1.8-2.0:** Exceptional - 100% tool reuse, all tools available
- **1.5-1.7:** Strong - ≥90% tool reuse, 1-2 missing tools with clear specs
- **1.2-1.4:** Adequate - 80-89% tool reuse, missing tools identified
- **0.8-1.1:** Weak - <80% tool reuse or poorly specified missing tools
- **0.0-0.7:** Insufficient - Major tool availability gaps

---

### Category 3: Parameter Specification (0-2 points)

**Weight:** 20%

**Criteria:**
1. **Parameters clearly specified** (0-0.7 pts)
   - Are all model parameters explicitly stated?
   - Are parameter choices justified by literature or data characteristics?
   - Are default parameters acknowledged when used?

2. **Parameters appropriate** (0-0.7 pts)
   - Are parameter values appropriate for REMEMVR data?
   - Do parameters align with cited literature standards?
   - Are sensitivity analyses considered for key parameters?

3. **Validation thresholds justified** (0-0.6 pts)
   - Are validation thresholds (e.g., RMSEA <0.08, p>0.05) appropriate?
   - Are thresholds cited from methodological literature?
   - Are multiple criteria used (not single-criterion validation)?

**Scoring Guide:**
- **1.8-2.0:** Exceptional - All parameters specified, justified, and appropriate
- **1.5-1.7:** Strong - Parameters well-specified with minor gaps
- **1.2-1.4:** Adequate - Basic parameter specification present
- **0.8-1.1:** Weak - Vague or poorly justified parameters
- **0.0-0.7:** Insufficient - Parameters unspecified or inappropriate

---

### Category 4: Validation Procedures (0-2 points)

**Weight:** 20%

**Criteria:**
1. **Assumption validation comprehensive** (0-0.7 pts)
   - Are all statistical assumptions explicitly checked?
   - Are appropriate tests specified for each assumption?
   - Are thresholds for assumption violations stated?

2. **Remedial actions specified** (0-0.7 pts)
   - If assumptions violated, are remedial actions specified?
   - Are alternative models considered for assumption violations?
   - Is sensitivity analysis planned for questionable assumptions?

3. **Validation procedures documented** (0-0.6 pts)
   - Are validation procedures clear enough for implementation?
   - Are validation reports planned (e.g., assumption test results table)?
   - Are validation failures handled (e.g., FAIL with explanation, not proceed)?

**Scoring Guide:**
- **1.8-2.0:** Exceptional - Comprehensive validation with remedial actions
- **1.5-1.7:** Strong - Good validation coverage with minor gaps
- **1.2-1.4:** Adequate - Basic validation present
- **0.8-1.1:** Weak - Incomplete or vague validation procedures
- **0.0-0.7:** Insufficient - No validation procedures or major gaps

---

### Category 5: Devil's Advocate Analysis (0-1 point)

**Weight:** 10% (meta-scoring category)

**Purpose:** Evaluate rq_stats agent's thoroughness in generating statistical criticisms via two-pass WebSearch.

**Criteria:**
1. **Coverage of criticism types** (0-0.4 pts)
   - Are all 4 subsections populated (Commission Errors, Omission Errors, Alternative Approaches, Known Pitfalls)?
   - Is each subsection comprehensive (not cursory)?
   - Are criticisms balanced across subsections?

2. **Quality of criticisms** (0-0.4 pts)
   - Are criticisms grounded in methodological literature (all cited)?
   - Are criticisms specific and actionable (not vague)?
   - Do criticisms demonstrate understanding of statistical methodology?
   - Are strength ratings appropriate (CRITICAL/MODERATE/MINOR)?

3. **Meta-thoroughness** (0-0.2 pts)
   - Did the agent search for counterevidence (challenge pass)?
   - Are suggested rebuttals evidence-based?
   - Total concerns ≥5 across all subsections?

**Scoring Guide:**
- **0.9-1.0:** Exceptional - Generated 5+ concerns across all subsections with literature citations, comprehensive devil's advocate analysis
- **0.7-0.8:** Strong - Generated 3-4 well-cited concerns, good coverage of 3 subsections
- **0.5-0.6:** Adequate - Generated 2-3 concerns with some citations, partial coverage
- **0.3-0.4:** Weak - Generated 1-2 vague concerns or poor literature support
- **0.0-0.2:** Insufficient - Failed to generate meaningful statistical criticisms

---

## Tool Availability Table Format

### Table Structure

**Required Columns:**
1. **Step:** Step name/number from analysis plan
2. **Tool Function:** Full module.function path (e.g., `tools.analysis_irt.calibrate_grm`)
3. **Status:** ✅ Available / ⚠️ Missing / 🔄 Needs Update
4. **Notes:** API verification, test results, concerns

### Status Icons

**✅ Available:**
- Tool exists in `tools/` package
- API signature verified against `docs/tools_inventory.md`
- Tests passing (if applicable)
- Ready for use

**⚠️ Missing:**
- Tool does not exist
- Needs implementation before analysis phase
- Specifications should be provided

**🔄 Needs Update:**
- Tool exists but API signature changed
- Tool exists but lacks required features
- Needs modification before use

---

## Validation Procedures Checklists

### IRT Validation Checklist Structure

**Table Format:**

| Assumption | Test | Threshold | Assessment |
|------------|------|-----------|------------|
| Local Independence | Q3 statistic | <0.2 | ✅ Appropriate (cite Christensen et al., 2017) |
| Unidimensionality | Eigenvalue ratio | >3.0 | ✅ Appropriate |
| Model Fit | RMSEA | <0.08 | ✅ Appropriate for N=400 |
| Item Fit | S-X² | p>0.01 (Bonferroni) | ✅ Appropriate |
| Person Fit | lz statistic | \|lz\| < 2.0 | ✅ Standard |

**Assessment Column Options:**
- ✅ Appropriate - Test and threshold are methodologically sound
- ⚠️ Questionable - Test or threshold may be too liberal/conservative
- ❌ Inappropriate - Test or threshold not suitable for this context

---

### LMM Validation Checklist Structure

**Table Format:**

| Assumption | Test | Threshold | Assessment |
|------------|------|-----------|------------|
| Residual Normality | Shapiro-Wilk / Q-Q plot | Visual + p>0.05 | ✅ Appropriate |
| Homoscedasticity | Residual vs fitted plot | Visual inspection | ✅ Appropriate |
| Random Effects Normality | Q-Q plot | Visual inspection | ✅ Standard |
| Independence | ACF plot | Lag-1 ACF < 0.1 | ✅ Appropriate |
| Linearity | Partial residual plots | Visual inspection | ✅ Appropriate |
| Outliers | Cook's distance | D > 4/n | ✅ Standard |

**Assessment Column Options:**
- ✅ Appropriate / ⚠️ Questionable / ❌ Inappropriate (same as IRT)

---

## Statistical Criticisms & Rebuttals (Devil's Advocate)

### Purpose

Generate potential reviewer concerns and statistical objections with evidence-based rebuttals. This section parallels rq_scholar's devil's advocate analysis but focuses on **statistical/methodological** validity instead of theoretical validity.

### Philosophy

Don't just validate what IS written - also critique what ISN'T written. Search for:
- Questionable statistical assumptions
- Missing methodological considerations
- Alternative statistical approaches not considered
- Known statistical pitfalls in proposed methods

Ground ALL criticisms in methodological literature (via WebSearch).

---

### Two-Pass WebSearch Strategy

**Pass 1: Validation** (3-5 queries)
- Verify proposed methods are appropriate for the RQ
- Find supporting methodological literature
- Check current statistical best practices

**Pass 2: Challenge** (3-5 queries)
- Search for known limitations of proposed methods
- Find alternative statistical approaches
- Identify common pitfalls in the literature
- Look for counterarguments to methodological choices

**Total:** 6-10 queries (realistic for 20-30 minute validation)

---

### Section Structure

When appending to 1_concept.md, this section should follow validation checklists and precede recommendations:

```markdown
### Statistical Criticisms & Rebuttals

**Analysis Approach:**
- **Two-Pass WebSearch Strategy:**
  1. **Validation Pass:** Verify methods are appropriate (support)
  2. **Challenge Pass:** Search for limitations, alternatives, pitfalls
- **Focus:** Both commission errors (what's wrong) and omission errors (what's missing)
- **Grounding:** All criticisms cite specific methodological literature sources

---

#### Commission Errors (Questionable Statistical Assumptions/Claims)

[Subsection content...]

---

#### Omission Errors (Missing Statistical Considerations)

[Subsection content...]

---

#### Alternative Statistical Approaches (Not Considered)

[Subsection content...]

---

#### Known Statistical Pitfalls (Unaddressed)

[Subsection content...]

---

#### Scoring Summary

**Total Concerns Identified:**
- Commission Errors: [N] ([N] CRITICAL, [N] MODERATE, [N] MINOR)
- Omission Errors: [N] ([N] CRITICAL, [N] MODERATE, [N] MINOR)
- Alternative Approaches: [N] ([N] CRITICAL, [N] MODERATE, [N] MINOR)
- Known Pitfalls: [N] ([N] CRITICAL, [N] MODERATE, [N] MINOR)

**Overall Devil's Advocate Assessment:**
[Paragraph summarizing whether concept.md adequately anticipates statistical criticism, acknowledges methodological limitations, and provides sufficient justification]

---
```

---

### Subsection 1: Commission Errors

**Definition:** Statistical assumptions or claims in concept.md that are questionable, unjustified, or potentially incorrect.

**Format per Error:**

```markdown
**[#] [Error Title]**
- **Location:** 1_concept.md - [Section name, paragraph/line if helpful]
- **Claim Made:** "[Quote or paraphrase what concept.md says]"
- **Statistical Criticism:** "[What's questionable about this assumption/claim - be specific]"
- **Methodological Counterevidence:** [Citation from WebSearch with specific finding that challenges this assumption]
- **Strength:** CRITICAL / MODERATE / MINOR
- **Suggested Rebuttal:** "[How to address this concern - evidence-based response or acknowledgment]"
```

**Example:**

```markdown
**1. Normality Assumption Stated Without Justification**
- **Location:** Section 6: Analysis Approach - LMM subsection, paragraph 2
- **Claim Made:** "Residuals are assumed to be normally distributed"
- **Statistical Criticism:** Normality assumption stated but no justification provided. With N=100 and 4 time points, small sample size may make normality assumption critical, yet no diagnostic tests specified.
- **Methodological Counterevidence:** Schielzeth et al. (2020, *Methods in Ecology and Evolution*) showed LMM residual normality violations can substantially affect Type I error rates with N<200, recommend Q-Q plots + Shapiro-Wilk test as minimum diagnostics
- **Strength:** MODERATE
- **Suggested Rebuttal:** "Add to Section 7: Validation Procedures - specify Q-Q plot visual inspection + Shapiro-Wilk test for residual normality. State remedial action if violated (e.g., robust standard errors or transformation)."
```

**CRITICAL CHECK (Per Solution.md Section 1.4):**
Always check if concept.md proposes Likert bias correction for confidence ratings. If found, FLAG as Commission Error:
- **Claim:** "Correct Likert response bias before analysis" (or similar)
- **Criticism:** Contradicts solution.md section 1.4 architectural decision - bias correction reduces interpretability more than measurement quality
- **Counterevidence:** Cite solution.md section 1.4 rationale (preserves direct interpretability, response style may be meaningful variance)
- **Strength:** CRITICAL
- **Rebuttal:** "Remove Likert bias correction requirement. Document response style patterns (% using full range vs extremes) in results instead. Per solution.md section 1.4, preserve raw 1-5 ratings for interpretability."

---

### Subsection 2: Omission Errors

**Definition:** Important statistical considerations, assumption checks, sensitivity analyses, or methodological limitations that are NOT mentioned in concept.md but SHOULD be for methodological completeness.

**Format per Omission:**

```markdown
**[#] [Omission Title]**
- **Missing Content:** "[What's not mentioned]"
- **Why It Matters:** "[Why this omission is problematic for methodological rigor]"
- **Supporting Literature:** [Citation from WebSearch showing this is an established methodological concern]
- **Potential Reviewer Question:** "[What a skeptical statistician might ask about this omission]"
- **Strength:** CRITICAL / MODERATE / MINOR
- **Suggested Addition:** "[Where and how to address this in concept.md]"
```

**Example:**

```markdown
**1. No Discussion of Multiple Testing Correction**
- **Missing Content:** Concept.md proposes post-hoc pairwise comparisons (4 domains × 4 time points = multiple tests) but doesn't mention correction for multiple comparisons
- **Why It Matters:** Without correction, inflated Type I error rate could lead to false positive findings (family-wise error rate >>0.05)
- **Supporting Literature:** Bender & Lange (2001, *BMJ*) recommend Bonferroni or Holm-Bonferroni for post-hoc tests in repeated measures designs. REMEMVR thesis uses Bonferroni per Decision D068.
- **Potential Reviewer Question:** "How will you control for inflated Type I error from multiple pairwise comparisons?"
- **Strength:** CRITICAL
- **Suggested Addition:** "Add to Section 6: Analysis Approach - specify Decision D068 dual reporting approach (both uncorrected and Bonferroni-corrected p-values). State family-wise error rate correction method explicitly."
```

---

### Subsection 3: Alternative Statistical Approaches

**Definition:** Competing statistical methods or alternative analytical approaches that could address the RQ but are not discussed in concept.md.

**Format per Alternative:**

```markdown
**[#] [Alternative Approach Title]**
- **Alternative Method:** "[Name and brief description]"
- **How It Applies:** "[How this method could address the RQ differently]"
- **Key Citation:** [Source from WebSearch]
- **Why Concept.md Should Address It:** "[Risk of ignoring this alternative]"
- **Strength:** CRITICAL / MODERATE / MINOR
- **Suggested Acknowledgment:** "[How to incorporate or rule out this alternative]"
```

**Example:**

```markdown
**1. Bayesian LMM Not Considered**
- **Alternative Method:** Bayesian mixed-effects models with weakly informative priors (instead of frequentist LMM)
- **How It Applies:** Bayesian approach could provide more stable estimates with N=100 (small sample), incorporates uncertainty in random effects, avoids convergence issues common in frequentist LMM with complex random structures
- **Key Citation:** Nicenboim et al. (2023, *Journal of Memory and Language*) demonstrated Bayesian LMM advantages for small-N longitudinal memory studies - better uncertainty quantification and no convergence failures
- **Why Concept.md Should Address It:** Reviewers familiar with Bayesian methods might question why frequentist approach chosen
- **Strength:** MODERATE
- **Suggested Acknowledgment:** "Add to Section 6: Analysis Approach - briefly justify frequentist LMM choice (e.g., alignment with prior REMEMVR publications, interpretability for broader audience, tool availability). Acknowledge Bayesian alternative as potential future extension."
```

---

### Subsection 4: Known Statistical Pitfalls

**Definition:** Established methodological issues or statistical pitfalls that could affect the proposed analysis but are not mentioned in concept.md.

**Format per Pitfall:**

```markdown
**[#] [Pitfall Title]**
- **Pitfall Description:** "[What statistical issue exists]"
- **How It Could Affect Results:** "[Potential impact on findings]"
- **Literature Evidence:** [Citation showing this is a known issue]
- **Why Relevant to This RQ:** "[Specific application to current study]"
- **Strength:** CRITICAL / MODERATE / MINOR
- **Suggested Mitigation:** "[How concept.md should address this limitation]"
```

**Example:**

```markdown
**1. Overfitting Risk with Small Sample Size**
- **Pitfall Description:** Complex LMM with multiple random effects (random intercepts + slopes) risks overfitting with N=100 participants
- **How It Could Affect Results:** Overfitted models may capture sample-specific noise rather than population effects, leading to poor generalizability and inflated effect sizes
- **Literature Evidence:** Bates et al. (2015, *arXiv*) recommend ≥200 observations for complex random structures. With N=100 × 4 = 400 observations but only 100 independent units, power for random slopes limited.
- **Why Relevant to This RQ:** Concept.md proposes random slopes for time effects - may not be estimable with current sample size
- **Strength:** MODERATE
- **Suggested Mitigation:** "Add to Section 6: Analysis Approach - state model selection strategy (compare random intercept vs random intercept+slope via likelihood ratio test, only retain random slopes if significantly improve fit AND converge). Acknowledge sample size limitation for complex random structures."
```

---

### Strength Rating Criteria

**CRITICAL:**
- Fundamental statistical flaw or major omission
- Likely to be raised by statistical reviewers
- Could result in rejection if unaddressed
- Requires substantive revision to concept.md

**MODERATE:**
- Important methodological consideration but not fatal
- Strengthens argument if addressed
- Could be addressed in limitations or discussion
- Statistical reviewers might raise this

**MINOR:**
- Optional consideration for completeness
- Unlikely to affect acceptance
- Nice to acknowledge but not essential
- Could be addressed in future work

---

## Recommendations Structure

### Required Changes (Conditional/Rejected Status Only)

**When to Use:**
- Status is CONDITIONAL (9.0 ≤ score < 9.25): Minor required changes
- Status is REJECTED (score < 9.0): Major required changes

**Format per Change:**
```markdown
1. **[Descriptive Title of Change]**
   - **Location:** 1_concept.md - [Exact section name, e.g., "Section 6: Analysis Approach, IRT subsection, paragraph 2"]
   - **Issue:** [What's wrong - be specific about the statistical/methodological problem]
   - **Fix:** [Exact text to add/change/remove - provide actual wording if possible]
   - **Rationale:** [Why this change is necessary for approval - reference rubric criteria]
```

---

### Suggested Improvements (Always Provide)

**When to Use:**
- ALL statuses (APPROVED, CONDITIONAL, REJECTED)
- Optional enhancements that improve quality but not required for approval

**Format per Suggestion:**
```markdown
1. **[Descriptive Title of Suggestion]**
   - **Location:** 1_concept.md - [Section name]
   - **Current:** [What the section says now - brief quote or summary]
   - **Suggested:** [What it could say instead - provide alternative wording]
   - **Benefit:** [Why this would enhance methodological quality - what it adds]
```




---

### v4.2 (2025-11-21)
- **Architecture Change:** Standalone file approach - Write 1_stats.md (not append to 1_concept.md) to prevent context bloat
- **Experimental Context:** Added thesis/methods.md reading (step 6) for grounded validation
- **Template Cleanup:** Removed 66% bloat (TOC, workflow descriptions, examples, design history)

---

**End of Template Specification**
