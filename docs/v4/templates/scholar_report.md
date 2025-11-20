# Scholar Validation Report Template

**File:** `docs/v4/templates/scholar_report.md`
**Last Updated:** 2025-11-16
**Purpose:** Template specification for rq_scholar agent scholarly validation feedback
**Version:** 4.0
**Status:** Template Specification

---

## Overview

### Purpose

This template specifies the format for **scholarly validation feedback** that the `rq_scholar` agent writes to standalone `1_scholar.md` file. The feedback uses a **10-point rubric system** (preserved from v3.0 for production-proven rigor) to systematically evaluate theoretical grounding, literature support, interpretation guidelines, theoretical implications, and reviewer rebuttals.

### Key Features

- **10-Point Rubric:** 5 weighted categories (Theoretical Grounding 3pts, Literature Support 2pts, Interpretation Guidelines 2pts, Theoretical Implications 2pts, Devil's Advocate Analysis 1pt)
- **Decision Thresholds:** APPROVED (≥9.25), CONDITIONAL (≥9.0), REJECTED (<9.0)
- **Literature Table:** Systematic citation format (Citation | Relevance | Key Finding | How to Use)
- **Actionable Recommendations:** Required changes vs suggested improvements with exact locations
- **Metadata Footer:** Audit trail (agent version, date, papers reviewed, duration)

### Workflow Integration

1. **rq_scholar reads this template** (step 5 of agent workflow)
2. **rq_scholar evaluates 1_concept.md** against rubric criteria
3. **rq_scholar reads thesis/methods.md** for experimental context (step 7)
4. **rq_scholar conducts literature search** via WebSearch tool
5. **rq_scholar writes formatted feedback** to standalone 1_scholar.md file (step 10 using Write tool)
6. **User reviews 1_scholar.md** before proceeding to statistical validation

---

## Report Structure

### Section Sequence (in 1_scholar.md)

When `rq_scholar` writes validation feedback to 1_scholar.md, it creates this structure:

```markdown
---

## Scholar Validation Report

**Validation Date:** YYYY-MM-DD HH:MM
**Agent:** rq_scholar v4.0
**Status:** ✅ APPROVED / ⚠️ CONDITIONAL / ❌ REJECTED
**Overall Score:** X.X / 10.0

---

### Rubric Scoring Summary

| Category | Score | Max | Status |
|----------|-------|-----|--------|
| Theoretical Grounding | X.X | 3.0 | ✅/⚠️/❌ |
| Literature Support | X.X | 2.0 | ✅/⚠️/❌ |
| Interpretation Guidelines | X.X | 2.0 | ✅/⚠️/❌ |
| Theoretical Implications | X.X | 2.0 | ✅/⚠️/❌ |
| Devil's Advocate Analysis | X.X | 1.0 | ✅/⚠️/❌ |
| **TOTAL** | **X.X** | **10.0** | **STATUS** |

---

### Detailed Rubric Evaluation

[Sections 1-5: One per rubric category]

---

### Literature Search Results

[Table format with citations]

---

### Scholarly Criticisms & Rebuttals

[Devil's advocate analysis with 4 subsections]

---

### Recommendations

[Required changes and suggested improvements]

---

### Validation Metadata

[Agent version, papers reviewed, duration]

---
```

---

## Section Specifications

### Section 1: Header

**Required Fields:**
- Validation Date (YYYY-MM-DD HH:MM format)
- Agent version (rq_scholar v4.0)
- Status badge (✅ APPROVED / ⚠️ CONDITIONAL / ❌ REJECTED)
- Overall score (X.X / 10.0)

**Format:**
```markdown
**Validation Date:** 2025-11-16 14:30
**Agent:** rq_scholar v4.0
**Status:** ✅ APPROVED
**Overall Score:** 9.5 / 10.0
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
| Theoretical Grounding | 2.9 | 3.0 | ✅ |
| Literature Support | 1.8 | 2.0 | ✅ |
| Interpretation Guidelines | 2.0 | 2.0 | ✅ |
| Theoretical Implications | 2.0 | 2.0 | ✅ |
| Devil's Advocate Analysis | 0.8 | 1.0 | ⚠️ |
| **TOTAL** | **9.5** | **10.0** | **✅ APPROVED** |
```

---

### Section 3: Detailed Rubric Evaluation

**Purpose:** In-depth analysis for each of the 5 rubric categories.

**Structure (Repeat for Each Category):**

```markdown
#### [Category Name] (X.X / Y.0)

**Criteria Checklist:**
- [ ] Criterion 1 description
- [x] Criterion 2 description
- [x] Criterion 3 description

**Assessment:**
[Paragraph evaluating this category against criteria]

**Strengths:**
- Bullet point 1
- Bullet point 2

**Weaknesses / Gaps:**
- Bullet point 1 (if any)
- Bullet point 2 (if any)

**Score Justification:**
[Why this specific score was assigned]
```

**Categories (see "10-Point Rubric System" section for detailed criteria):**
1. Theoretical Grounding (0-3 points)
2. Literature Support (0-2 points)
3. Interpretation Guidelines (0-2 points)
4. Theoretical Implications (0-2 points)
5. Devil's Advocate Analysis (0-1 point)

---

### Section 4: Literature Search Results

**Purpose:** Document literature validation findings with systematic table format.

**Structure:**

```markdown
### Literature Search Results

**Search Strategy:**
- **Search Queries:** [List of search terms used, e.g., "dual-process theory episodic memory", "consolidation VR recall"]
- **Date Range:** Prioritized 2020-2024, supplemented with 2015-2019 seminal works
- **Total Papers Reviewed:** [N]
- **High-Relevance Papers:** [N]

**Key Papers Found:**

| Citation | Relevance | Key Finding | How to Use |
|----------|-----------|-------------|------------|
| Author et al. (YYYY) | High | [Brief summary of finding relevant to RQ] | [Action: Add to Section X, cite in hypothesis, etc.] |
| Author et al. (YYYY) | Medium | [Brief summary] | [Action] |
| Author et al. (YYYY) | Low | [Brief summary] | [Optional: Background reading] |

**Citations to Add (Prioritized):**

**High Priority:**
1. Full citation - **Location:** [Section name in 1_concept.md] - **Purpose:** [Why this citation strengthens the RQ]

**Medium Priority:**
1. Full citation - **Location:** [Section name] - **Purpose:** [Why helpful]

**Low Priority (Optional):**
1. Full citation - **Location:** [Section name] - **Purpose:** [Why useful for completeness]

**Citations to Remove (If Any):**
1. Citation - **Reason:** [Why it's not appropriate, e.g., outdated, not relevant, methodologically flawed]
```

---

### Section 5: Scholarly Criticisms & Rebuttals (Devil's Advocate Analysis)

**Purpose:** Generate potential reviewer concerns and scholarly objections with evidence-based rebuttals.

**Philosophy:** Don't just validate what IS written - also critique what ISN'T written. Search for counterevidence, alternative theories, known limitations, and missing context. Ground ALL criticisms in literature (via WebSearch).

**Structure:**

```markdown
### Scholarly Criticisms & Rebuttals

**Analysis Approach:**
- **Two-Pass WebSearch Strategy:**
  1. **Validation Pass:** Verify claims are accurate (support)
  2. **Challenge Pass:** Search for counterevidence, alternative theories, limitations
- **Focus:** Both commission errors (what's wrong) and omission errors (what's missing)
- **Grounding:** All criticisms cite specific literature sources

---

#### Commission Errors (Critiques of Claims Made)

**Definition:** Claims in concept.md that are incorrect, misleading, outdated, or mischaracterized.

**Format per Error:**

**[#] [Error Title]**
- **Location:** 1_concept.md - [Section name, paragraph/line if helpful]
- **Claim Made:** "[Quote or paraphrase what concept.md says]"
- **Scholarly Criticism:** "[What's wrong with this claim - be specific]"
- **Counterevidence:** [Citation from WebSearch with specific finding that contradicts or challenges claim]
- **Strength:** CRITICAL / MODERATE / MINOR
- **Suggested Rebuttal:** "[How you could address this concern - evidence-based response]"

**Example:**
**1. Temporal Memory Domain Characterized as Uniformly Fragile**
- **Location:** Section 3: Memory Domains - Temporal Domain paragraph
- **Claim Made:** "Temporal memory is particularly susceptible to rapid decay"
- **Scholarly Criticism:** This oversimplifies temporal memory - research shows temporal discrimination (when) decays differently than temporal order (sequence)
- **Counterevidence:** Diamond & Lewis (2021, *Cognition*) found temporal order memory remained stable over 7 days while absolute time judgments deteriorated within 24 hours in VR navigation tasks
- **Strength:** MODERATE
- **Suggested Rebuttal:** "Distinguish between temporal order (sequence) and temporal discrimination (absolute time). Hypothesis should specify which aspect of temporal memory is being measured and predicted to decay."

---

#### Omission Errors (Missing Context or Claims)

**Definition:** Important theoretical context, alternative explanations, known confounds, or methodological limitations that are NOT mentioned in concept.md but SHOULD be for scholarly completeness.

**Format per Omission:**

**[#] [Omission Title]**
- **Missing Content:** "[What's not mentioned]"
- **Why It Matters:** "[Why this omission is problematic for scholarly rigor]"
- **Supporting Literature:** [Citation from WebSearch showing this is an established concern in the field]
- **Potential Reviewer Question:** "[What a skeptical reviewer might ask about this omission]"
- **Strength:** CRITICAL / MODERATE / MINOR
- **Suggested Addition:** "[Where and how to address this in concept.md]"

**Example:**
**1. No Discussion of Test-Retest Practice Effects**
- **Missing Content:** Concept.md doesn't acknowledge that participants complete the same VR test 4 times (Days 0, 1, 3, 6)
- **Why It Matters:** Practice effects could confound forgetting curves - improvements from familiarity might mask memory decay
- **Supporting Literature:** Stark et al. (2023, *Nature Neuroscience*) demonstrated significant practice effects in VR spatial memory across repeated testing, even with 7-day gaps
- **Potential Reviewer Question:** "How do you distinguish genuine memory decay from practice-related improvements masking that decay?"
- **Strength:** CRITICAL
- **Suggested Addition:** "Add to Section 4: Analysis Strategy - discuss IRT theta scoring advantages for practice effects (separates item difficulty from ability) and/or mention inclusion of test session as covariate in LMM"

---

#### Alternative Theoretical Frameworks (Not Considered)

**Definition:** Competing theories or alternative explanations that could account for expected results but are not discussed in concept.md.

**Format per Alternative:**

**[#] [Alternative Framework Title]**
- **Alternative Theory:** "[Name and brief description]"
- **How It Applies:** "[How this theory could explain the RQ phenomenon differently]"
- **Key Citation:** [Source from WebSearch]
- **Why Concept.md Should Address It:** "[Risk of ignoring this alternative]"
- **Strength:** CRITICAL / MODERATE / MINOR
- **Suggested Acknowledgment:** "[How to incorporate or rule out this alternative]"

**Example:**
**1. Encoding Quality Differences Not Considered**
- **Alternative Theory:** Differences attributed to "memory decay" might actually reflect encoding quality differences across domains (spatial encoded better initially)
- **How It Applies:** If spatial information is encoded more richly during initial VR experience, observed "decay trajectories" might reflect ceiling effects (spatial starts higher) rather than differential forgetting rates
- **Key Citation:** Bonnici et al. (2022, *Hippocampus*) showed spatial context encoded with greater hippocampal engagement than temporal context in VR, suggesting initial encoding differences
- **Why Concept.md Should Address It:** Reviewers will ask whether domain differences are about forgetting or encoding quality
- **Strength:** MODERATE
- **Suggested Acknowledgment:** "Add to Section 2: Theoretical Background - acknowledge encoding quality differences, explain why Day 0 serves as baseline (captures initial encoding state), and why longitudinal trajectory slopes (not intercepts) test forgetting rates"

---

#### Known Methodological Confounds (Unaddressed)

**Definition:** Established methodological issues in VR memory research that could affect interpretation but are not mentioned in concept.md.

**Format per Confound:**

**[#] [Confound Title]**
- **Confound Description:** "[What methodological issue exists]"
- **How It Could Affect Results:** "[Potential impact on findings]"
- **Literature Evidence:** [Citation showing this is a known issue]
- **Why Relevant to This RQ:** "[Specific application to current study]"
- **Strength:** CRITICAL / MODERATE / MINOR
- **Suggested Mitigation:** "[How concept.md should address this limitation]"

**Example:**
**1. VR Simulator Sickness as Dropout Confounder**
- **Confound Description:** Participants with higher simulator sickness may drop out of longitudinal study, creating selection bias
- **How It Could Affect Results:** If spatial memory tasks induce more sickness (navigation-heavy), differential dropout could bias spatial domain trajectories
- **Literature Evidence:** Mittelstaedt et al. (2019, *Human Factors*) found 15-30% dropout in multi-session VR studies due to simulator sickness, non-random across task types
- **Why Relevant to This RQ:** 4-session design across 6 days provides multiple dropout opportunities
- **Strength:** MODERATE
- **Suggested Mitigation:** "Add to Section 7: Limitations - acknowledge potential dropout bias, state whether REMEMVR tracked simulator sickness, discuss whether dropout rates differed across domains (if data available)"

---

#### Scoring Summary

**Total Concerns Identified:**
- Commission Errors: [N] ([N] CRITICAL, [N] MODERATE, [N] MINOR)
- Omission Errors: [N] ([N] CRITICAL, [N] MODERATE, [N] MINOR)
- Alternative Frameworks: [N] ([N] CRITICAL, [N] MODERATE, [N] MINOR)
- Methodological Confounds: [N] ([N] CRITICAL, [N] MODERATE, [N] MINOR)

**Overall Devil's Advocate Assessment:**
[Paragraph summarizing whether concept.md adequately anticipates scholarly criticism, acknowledges limitations, and provides sufficient rebuttals]

---
```

**Strength Rating Criteria:**

**CRITICAL:**
- Fundamental theoretical flaw or major omission
- Likely to be raised by multiple reviewers
- Could result in rejection if unaddressed
- Requires substantive revision to concept.md

**MODERATE:**
- Important consideration but not fatal
- Scholarly reviewers might raise this
- Strengthens argument if addressed
- Could be addressed in rebuttal or discussion

**MINOR:**
- Optional consideration for completeness
- Unlikely to affect acceptance
- Nice to acknowledge but not essential
- Could be addressed in future work

---

### Section 6: Recommendations

**Purpose:** Provide actionable guidance for improving 1_concept.md.

**Structure:**

```markdown
### Recommendations

#### Required Changes (Must Address for Approval)

[Only if status is CONDITIONAL or REJECTED]

1. **[Change Title]**
   - **Location:** 1_concept.md - [Section name, line number if helpful]
   - **Issue:** [What's wrong or missing]
   - **Fix:** [Specific text to add/change/remove]
   - **Rationale:** [Why this change is necessary for scholarly validity]

2. **[Change Title]**
   - [Same structure]

#### Suggested Improvements (Optional but Recommended)

[Always provide, even if APPROVED]

1. **[Suggestion Title]**
   - **Location:** 1_concept.md - [Section name]
   - **Current:** [What it says now]
   - **Suggested:** [What it could say instead]
   - **Benefit:** [Why this would enhance quality]

2. **[Suggestion Title]**
   - [Same structure]

#### Literature Additions

[Cross-reference to Section 4 citations to add]

See "Literature Search Results" section above for prioritized citation list.
```

---

### Section 7: Validation Metadata

**Purpose:** Audit trail and accountability.

**Structure:**

```markdown
### Validation Metadata

- **Agent Version:** rq_scholar v4.0
- **Rubric Version:** 10-point system (v4.0)
- **Validation Date:** YYYY-MM-DD HH:MM
- **Search Tools Used:** WebSearch (via Claude Code)
- **Total Papers Reviewed:** [N]
- **High-Relevance Papers:** [N]
- **Validation Duration:** ~[X] minutes
- **Context Dump:** [Terse summary for status.yaml - 1 sentence]
```

---

## 10-Point Rubric System

### Category 1: Theoretical Grounding (0-3 points)

**Weight:** 30% (most important category)

**Criteria:**
1. **Alignment with episodic memory theory** (0-1 pt)
   - Does the hypothesis align with established episodic memory frameworks?
   - Are theoretical constructs (encoding, consolidation, retrieval, forgetting) used correctly?

2. **Domain-specific theoretical rationale** (0-1 pt)
   - Is there clear rationale for why domains (spatial, temporal, contextual) might differ?
   - Does the hypothesis draw on domain-specific memory theories?

3. **Theoretical coherence** (0-1 pt)
   - Is the theoretical framework internally consistent?
   - Are all theoretical claims supported by the cited framework?

**Scoring Guide:**
- **2.7-3.0:** Exceptional - Sophisticated theoretical integration with novel synthesis
- **2.3-2.6:** Strong - Clear theoretical grounding with appropriate frameworks
- **1.8-2.2:** Adequate - Basic theoretical rationale present
- **1.0-1.7:** Weak - Superficial theoretical connection
- **0.0-0.9:** Insufficient - Lacks theoretical grounding

---

### Category 2: Literature Support (0-2 points)

**Weight:** 20%

**Criteria:**
1. **Recent citations** (0-0.7 pts)
   - Are recent papers (2020-2024) cited?
   - Are seminal works (2010-2019) also included for context?

2. **Citation appropriateness** (0-0.7 pts)
   - Are citations relevant to the specific RQ claims?
   - Are citations from high-quality sources (peer-reviewed journals)?

3. **Coverage completeness** (0-0.6 pts)
   - Are all major claims supported by literature?
   - Are counter-evidence or alternative theories acknowledged?

**Scoring Guide:**
- **1.8-2.0:** Exceptional - Comprehensive recent literature with seminal works
- **1.5-1.7:** Strong - Good balance of recent and foundational citations
- **1.2-1.4:** Adequate - Basic literature coverage, some gaps
- **0.8-1.1:** Weak - Outdated or sparse citations
- **0.0-0.7:** Insufficient - Major literature gaps

---

### Category 3: Interpretation Guidelines (0-2 points)

**Weight:** 20%

**Criteria:**
1. **Scenario coverage** (0-0.7 pts)
   - Are interpretation guidelines provided for ALL expected result patterns?
   - If Domain×Day interaction significant: guidance provided?
   - If Domain×Day interaction null: guidance provided?
   - If unexpected patterns emerge: guidance provided?

2. **Theoretical connection** (0-0.7 pts)
   - Do interpretation guidelines connect results back to theory?
   - Are alternative theoretical explanations considered?

3. **Practical clarity** (0-0.6 pts)
   - Are guidelines clear and actionable for results-inspector?
   - Do guidelines specify what to look for in data?

**Scoring Guide:**
- **1.8-2.0:** Exceptional - Comprehensive scenario-based guidelines with theoretical grounding
- **1.5-1.7:** Strong - Good coverage of major scenarios with clear guidance
- **1.2-1.4:** Adequate - Basic guidelines present, some scenarios missing
- **0.8-1.1:** Weak - Vague or incomplete guidance
- **0.0-0.7:** Insufficient - No interpretation guidelines

---

### Category 4: Theoretical Implications (0-2 points)

**Weight:** 20%

**Criteria:**
1. **Clear contribution** (0-0.7 pts)
   - Does the RQ state what it will contribute to episodic memory theory?
   - Is the contribution novel or incremental?

2. **Implications specificity** (0-0.7 pts)
   - Are theoretical implications clearly stated?
   - Are implications testable and falsifiable?

3. **Broader impact** (0-0.6 pts)
   - Does the RQ explain implications for VR memory assessment?
   - Are clinical or applied implications mentioned?

**Scoring Guide:**
- **1.8-2.0:** Exceptional - Novel contribution with broad implications
- **1.5-1.7:** Strong - Clear contribution to theory and practice
- **1.2-1.4:** Adequate - Basic implications stated
- **0.8-1.1:** Weak - Vague or limited implications
- **0.0-0.7:** Insufficient - No clear implications

---

### Category 5: Devil's Advocate Analysis (0-1 point)

**Weight:** 10% (bonus category)

**Purpose:** Evaluate the quality of the rq_scholar agent's generated scholarly criticisms and rebuttals.

**NOTE:** This category scores the AGENT'S devil's advocate analysis, not the user's concept.md content. The agent generates criticisms via two-pass WebSearch (validation + challenge).

**Criteria:**
1. **Criticism thoroughness** (0-0.4 pts)
   - Did agent conduct two-pass WebSearch strategy (Pass 1: validation 5+ queries, Pass 2: challenge 5+ queries)?
   - Did agent identify 3-5+ substantive concerns via challenge-pass WebSearch?
   - Are criticisms grounded in specific literature citations (not hallucinated)?
   - Are both commission errors (what's wrong) and omission errors (what's missing) covered?

2. **Rebuttal quality** (0-0.4 pts)
   - Are suggested rebuttals evidence-based (cite supporting literature)?
   - Do rebuttals directly address each criticism?
   - Are strength ratings (CRITICAL/MODERATE/MINOR) appropriate?

3. **Alternative frameworks coverage** (0-0.2 pts)
   - Did agent search for and identify competing theoretical explanations?
   - Are methodological confounds from VR memory literature identified?
   - Does analysis demonstrate sophisticated scholarly thinking beyond surface validation?

**Scoring Guide:**
- **0.9-1.0:** Exceptional - Comprehensive criticisms with literature-grounded rebuttals, multiple alternatives/confounds identified
- **0.7-0.8:** Strong - Good coverage of commission + omission errors, solid rebuttals, 1-2 alternatives identified
- **0.5-0.6:** Adequate - Basic criticisms present, rebuttals generic but reasonable
- **0.3-0.4:** Weak - Superficial criticisms, weak rebuttals, no alternatives considered
- **0.0-0.2:** Insufficient - No meaningful devil's advocate analysis or rebuttals hallucinated (not literature-based)

---

## Literature Search Table Format

### Table Structure

**Required Columns:**
1. **Citation:** Full APA-style citation (Author et al., Year)
2. **Relevance:** High / Medium / Low
3. **Key Finding:** 1-2 sentence summary of finding relevant to this RQ
4. **How to Use:** Specific action (add to Section X, cite in hypothesis, use in interpretation, etc.)

### Relevance Criteria

**High Relevance:**
- Directly addresses this RQ's research question or hypothesis
- Recent publication (2020-2024) in high-impact journal
- Methodologically rigorous and relevant to REMEMVR design

**Medium Relevance:**
- Related to broader topic but not directly on this RQ's focus
- Older seminal work (2010-2019) providing foundational context
- Relevant findings but different methodology or population

**Low Relevance:**
- Tangentially related (background reading)
- May be useful for discussion but not central to hypothesis
- Optional citation for completeness

---

## Recommendations Structure

### Required Changes (Conditional/Rejected Status Only)

**When to Use:**
- Status is CONDITIONAL (9.0 ≤ score < 9.25): Minor required changes
- Status is REJECTED (score < 9.0): Major required changes

**Format per Change:**
```markdown
1. **[Descriptive Title of Change]**
   - **Location:** 1_concept.md - [Exact section name, e.g., "Section 2: Theoretical Background, paragraph 3"]
   - **Issue:** [What's wrong - be specific about the scholarly/theoretical problem]
   - **Fix:** [Exact text to add/change/remove - provide the actual wording if possible]
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
   - **Benefit:** [Why this would enhance scholarly quality - what it adds]
```

---

## Decision Thresholds

### Threshold System

**APPROVED Status: ≥9.25 / 10.0**
- **Meaning:** Gold standard scholarly quality
- **Action:** Proceed to planning phase without required changes
- **Suggested improvements:** Optional enhancements provided but not mandatory

**CONDITIONAL Status: 9.0-9.24 / 10.0**
- **Meaning:** Acceptable quality with minor gaps
- **Action:** Address required changes before proceeding (typically 1-3 changes)
- **Typical changes:** Add 1-2 recent citations, specify interpretation scenario, strengthen one rebuttal

**REJECTED Status: <9.0 / 10.0**
- **Meaning:** Requires substantial rework
- **Action:** Address required changes and request re-validation
- **Typical changes:** Major theoretical gaps, insufficient literature, missing interpretation guidance, unclear implications

### Decision Report Format

```markdown
### Decision

**Final Score:** X.X / 10.0

**Status:** ✅ APPROVED

**Threshold:** ≥9.25 (gold standard)

**Reasoning:**
[Paragraph explaining overall assessment. For APPROVED: Why this RQ demonstrates gold standard quality. For CONDITIONAL: Why acceptable but needs minor improvements. For REJECTED: Why substantial rework is needed.]

**Next Steps:**

**✅ APPROVED (≥9.25):**
- Proceed to planning phase (rq_planner agent)
- Suggested improvements are optional but recommended for publication quality
- No re-validation required

**⚠️ CONDITIONAL (9.0-9.24):**
[If applicable]
- Address [N] required changes listed above
- No re-validation required - proceed after changes implemented
- Master can verify changes or proceed with planning

**❌ REJECTED (<9.0):**
[If applicable]
- Address [N] required changes listed above
- Request re-validation after changes implemented
- rq_scholar must re-evaluate before proceeding to planning phase
```

---

## v3.0 vs v4.X Differences

### Key Changes from v3.0

| Aspect | v3.0 Scholar | v4.X rq_scholar |
|--------|-------------|-----------------|
| **Output Location** | Separate file: `validation/scholar_report.md` | Standalone file: `results/chX/rqY/docs/1_scholar.md` |
| **Agent Scope** | Monolithic scholar agent (reads info.md, writes validation report, updates status.md) | Atomic rq_scholar agent (focused on claim validation only) |
| **File Editing** | READ-ONLY (never edits core files) | Uses Write tool to create standalone validation report |
| **Input Document** | info.md (universal 10-section RQ specification) | 1_concept.md (extracted thesis section via rq_concept agent) |
| **Rubric System** | ✅ 10-point rubric (5 categories) | ✅ 10-point rubric (PRESERVED for rigor) |
| **Decision Thresholds** | ✅ APPROVED ≥9.25 / CONDITIONAL ≥9.0 / REJECTED <9.0 | ✅ Same thresholds (PRESERVED) |
| **Literature Table** | ✅ Table format (Citation \| Relevance \| Finding \| Use) | ✅ Same format (PRESERVED) |
| **Context Management** | Large context window (full info.md + template + literature) | Leaner context (concept.md + template + targeted literature) |
| **Status Tracking** | Updates status.md with validation decision | Updates status.yaml context_dump with terse summary |

### Design Rationale

**Why Preserve v3.0 Rubric System?**
- **Production-proven:** RQ 5.1 achieved 9.5/10 (gold standard) using v3.0 rubric
- **Thesis-appropriate rigor:** 10-point system provides systematic scholarly evaluation expected in PhD research
- **Actionable feedback:** Rubric breakdown identifies specific gaps (e.g., "Devil's Advocate Analysis: 0.7/1.0") guiding improvements

**Why Standalone File Instead of Appending?**
- **Prevents context bloat:** Validation reports can be 10-20k tokens; keeping separate prevents 1_concept.md from bloating
- **Modular review:** User can review concept and validation independently
- **Clean separation of concerns:** Concept creation (rq_concept) vs validation (rq_scholar) outputs remain distinct
- **Downstream efficiency:** rq_planner reads lean 1_concept.md (~5-7k tokens) instead of bloated merged file (~20k+ tokens)

---

## Implementation Notes

### For rq_scholar Agent Developers

**Agent Prompt Must:**
1. Read this template at step 5 (structure reference)
2. Evaluate 1_concept.md against 10-point rubric (5 categories)
3. Read thesis/methods.md at step 7 (experimental context for validation)
4. Conduct literature search via WebSearch at step 9 (two-pass: validation + challenge, 6-10 queries total, prioritize 2020-2024)
5. Calculate final score (sum of 5 categories)
6. Determine status (APPROVED ≥9.25, CONDITIONAL ≥9.0, REJECTED <9.0)
7. Format feedback following this template structure
8. **Use Write tool to create standalone 1_scholar.md file** at step 10
9. Update status.yaml context_dump with terse summary at step 11 (condensed 1-line format, score/status convey all critical info)

### Critical Formatting Rules

**When Creating Standalone 1_scholar.md:**
- Start with horizontal rule separator (three dashes)
- Use level-2 heading for "Scholar Validation Report" (main document title)
- Use level-3 headings for major sections (Rubric Scoring, Detailed Evaluation, etc.)
- Use level-4 headings for rubric categories (1. Theoretical Grounding, 2. Literature Support, etc.)
- Include metadata footer at end (agent version, date, papers reviewed, duration)
- End with horizontal rule separator

**Example Write Operation:**
The agent creates a new standalone file at `results/chX/rqY/docs/1_scholar.md` using Write tool. The file contains ONLY the Scholar Validation Report (not a copy of 1_concept.md). User reviews 1_concept.md and 1_scholar.md separately.

### Quality Assurance Checklist

Before rq_scholar reports success, verify:
- [ ] All 5 rubric categories scored (Theoretical Grounding, Literature Support, Interpretation Guidelines, Theoretical Implications, Devil's Advocate Analysis)
- [ ] Final score calculated correctly (sum of 5 categories)
- [ ] Status determined correctly based on thresholds (≥9.25 APPROVED, ≥9.0 CONDITIONAL, <9.0 REJECTED)
- [ ] Literature search conducted (5+ queries minimum)
- [ ] Literature table includes High/Medium/Low relevance classifications
- [ ] Required changes provided if CONDITIONAL or REJECTED status
- [ ] Suggested improvements provided regardless of status (always optional enhancements)
- [ ] Metadata footer complete (agent version, date, papers reviewed, duration)
- [ ] Context dump created for status.yaml (1 sentence terse summary)
- [ ] Write tool used successfully (created standalone 1_scholar.md file)

---

## Version History

### v4.2 (2025-11-21)
- **Architecture Change:** Switched from appending to 1_concept.md (Edit tool) to standalone file 1_scholar.md (Write tool)
- **Rationale:** Prevents context bloat (validation reports 10-20k tokens kept separate from 5-7k concept.md)
- **Benefit:** Downstream agents (rq_planner) read lean concept.md, validation available for user review/thesis writeup
- **Updated:** Output Location, v3.0 vs v4.X table, Design Rationale, Implementation Notes, Critical Formatting Rules, Quality Assurance Checklist
- **Integration:** Added thesis/methods.md reading at step 7 for experimental context grounding

### v4.1 (2025-11-18)
- **Enhanced:** Added Section 5 "Scholarly Criticisms & Rebuttals (Devil's Advocate Analysis)"
- **New Features:**
  - Two-pass WebSearch strategy (validation + challenge)
  - Commission Errors subsection (critiques of claims made)
  - Omission Errors subsection (missing context or claims)
  - Alternative Theoretical Frameworks subsection
  - Known Methodological Confounds subsection
  - Strength ratings (CRITICAL/MODERATE/MINOR) for all concerns
  - Evidence-based suggested rebuttals with literature citations
- **Rubric Update:** Category 5 renamed from "Reviewer Rebuttals" to "Devil's Advocate Analysis"
- **Philosophy:** Agent now generates scholarly criticisms (not just validates user's), searches for counterevidence, identifies omissions, considers alternative theories
- **Impact:** Reduces hallucinations by grounding ALL criticisms in WebSearch results, provides comprehensive reviewer preparation

### v4.0 (2025-11-16)
- **Created:** Initial v4.X template specification
- **Design:** Preserves v3.0 10-point rubric system for production-proven rigor
- **Format:** Adapted for v4.X appending workflow (Edit tool to 1_concept.md)
- **Features:** 5 rubric categories, decision thresholds (≥9.25/≥9.0/<9.0), literature table, actionable recommendations, metadata footer
- **Difference from v3.0:** Appended to concept document instead of separate validation/scholar_report.md file
- **Status:** Template specification (agent implementation pending)

---

**End of Template Specification**
