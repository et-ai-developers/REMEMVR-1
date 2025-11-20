# 1_concept.md Format Specification

**Last Updated:** 2025-11-16
**Version:** 4.0
**Purpose:** Defines the mandatory structure for 1_concept.md (RQ concept document)
**Audience:** rq_concept agent when creating 1_concept.md from thesis

---

## How to Use This Template

This template specifies the **exact structure** that rq_concept agent must create for the `1_concept.md` document. The rq_concept agent extracts RQ information from the thesis file (ANALYSES_CHX.md) and formats it into 1_concept.md according to these specifications.

**Agent Implementation (rq_concept agent):**
- Reads this template in Step 4
- Reads thesis file ANALYSES_CHX.md in Steps 5-6
- Maps thesis content to template format in Step 7 (Ultrathink)
- Creates 1_concept.md in Step 8 (Bash)
- Fills 1_concept.md with mapped content in Step 9 (Write)

**Validation Workflow:**
- rq_scholar agent reads 1_concept.md, appends scholarly validation feedback
- rq_stats agent reads 1_concept.md, appends statistical validation feedback
- User reviews validated 1_concept.md at workflow step 7 (SINGLE USER APPROVAL GATE)

---

## File Location

**Path:** `results/chX/rqY/docs/1_concept.md` (inside docs/ subfolder)

**Created By:** rq_concept agent (workflow step 4)

**Validated By:** rq_scholar agent (workflow step 5), rq_stats agent (workflow step 6)

**User-Approved:** Workflow step 7 (only user approval gate in entire 17-step workflow)

**Read By:** rq_planner (step 9), rq_tools (step 11), rq_analysis (step 12), g_conflict (steps 10 & 13)

---

## Document Structure Overview

**7 Required Sections:**
1. RQ Title and ID
2. Research Question Statement
3. Theoretical Background
4. Hypothesis
5. Memory Domains
6. Analysis Approach
7. Data Source

**Validation Feedback (Appended Later):**
- Scholarly Validation Feedback (appended by rq_scholar agent)
- Statistical Validation Feedback (appended by rq_stats agent)

**Total Structure:** 7 concept sections + 2 validation sections = 9 sections when complete

---

## Section 1: RQ Title and ID

**Purpose:** Clearly identify which research question this document describes

**Required Content:**
- Chapter number (5, 6, or 7)
- RQ number within chapter (1-15 for ch5/ch6, 1-20 for ch7)
- Descriptive title summarizing the RQ focus

**Format:**
```markdown
# RQ X.Y: [Descriptive Title]

**Chapter:** X
**RQ Number:** Y
**Full ID:** X.Y
```

**Example:**
```markdown
# RQ 5.1: Domain-Specific Forgetting Trajectories (What/Where/When)

**Chapter:** 5
**RQ Number:** 1
**Full ID:** 5.1
```

**Extraction Guidance for rq_concept:**
- Read ANALYSES_CHX.md TABLE OF CONTENTS
- Locate RQ X.Y entry
- Extract chapter, number, and title
- Format according to template

---

## Section 2: Research Question Statement

**Purpose:** State the central research question in clear, answerable form

**Required Content:**
- Main research question (interrogative sentence)
- Scope clarification (what is being examined)
- Theoretical framing (why this question matters)

**Format:**
```markdown
## Research Question

**Primary Question:**
[State the main research question as an interrogative sentence]

**Scope:**
[Clarify what is being examined - variables, population, timeframe]

**Theoretical Framing:**
[Explain why this question matters for episodic memory theory]
```

**Example:**
```markdown
## Research Question

**Primary Question:**
Do episodic memory domains (What, Where, When) show differential forgetting trajectories across a 6-day retention interval?

**Scope:**
This RQ examines forgetting rates for three episodic memory components using IRT-derived ability estimates across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6). Time variable uses TSVR (actual hours since encoding), not nominal days. Focuses on VR-based memory test items requiring binding of object identity, spatial location, and temporal order.

**Theoretical Framing:**
Dual-process theory predicts domain-specific forgetting patterns due to differential reliance on familiarity vs. recollection processes. Understanding domain-specific trajectories informs theoretical models of episodic memory consolidation and retrieval.
```

**Extraction Guidance for rq_concept:**
- Read RQ section from ANALYSES_CHX.md
- Extract primary research question (usually first paragraph)
- Identify scope elements (variables, population, timeframe)
- Extract theoretical context (why this matters)
- Format according to template

---

## Section 3: Theoretical Background

**Purpose:** Establish theoretical grounding and episodic memory literature basis

**Required Content:**
- Relevant episodic memory theories (dual-process, consolidation, etc.)
- Key citations and empirical findings
- Theoretical predictions for this RQ
- Gaps in literature this RQ addresses

**Format:**
```markdown
## Theoretical Background

**Relevant Theories:**
[List and briefly describe theories relevant to this RQ]

**Key Citations:**
[Seminal papers and empirical findings supporting the theoretical framework]

**Theoretical Predictions:**
[What do these theories predict for this specific RQ?]

**Literature Gaps:**
[What gaps does this RQ address? Why is this RQ needed?]
```

**Example:**
```markdown
## Theoretical Background

**Relevant Theories:**
- **Dual-Process Theory** (Yonelinas, 2002): Memory retrieval relies on familiarity (fast, automatic) and recollection (slow, effortful). What domain can rely on familiarity, while Where/When require recollection.
- **Consolidation Theory** (Dudai, 2004): Hippocampal-dependent memories (Where, When) consolidate more slowly and show greater vulnerability during consolidation compared to perirhinal-dependent memories (What).

**Key Citations:**
- Tulving (1972): Episodic memory as "mental time travel" requiring binding of What/Where/When
- Baddeley (2000): Working memory model with distinct visuospatial and phonological components
- Eichenbaum (1999): Hippocampal role in spatial and temporal binding

**Theoretical Predictions:**
Dual-process theory predicts What will show slowest forgetting (familiarity-based), Where intermediate, and When fastest (recollection-dependent). Consolidation theory predicts divergence increases after ~24 hours (consolidation period, T2 nominal Day 1).

**Literature Gaps:**
Most episodic memory studies examine What and Where separately. Few studies test all three WWW domains together in immersive VR with longitudinal trajectories. This RQ fills the gap.
```

**Extraction Guidance for rq_concept:**
- Read RQ section from ANALYSES_CHX.md for theoretical context
- Extract theory names and brief descriptions
- Identify key citations mentioned
- Extract theoretical predictions for this RQ
- Identify what makes this RQ novel/needed
- Format according to template

**Validation Note:**
rq_scholar agent will validate this section, check citations, and append feedback.

---

## Section 4: Hypothesis

**Purpose:** State directional predictions with theoretical justification

**Required Content:**
- Primary hypothesis (directional prediction)
- Secondary hypotheses (if applicable)
- Theoretical rationale (why these predictions)
- Expected effect patterns (interaction, main effects, etc.)

**Format:**
```markdown
## Hypothesis

**Primary Hypothesis:**
[State main directional prediction]

**Secondary Hypotheses (if applicable):**
[State additional predictions]

**Theoretical Rationale:**
[Explain WHY you expect these patterns based on Section 3 theories]

**Expected Effect Pattern:**
[Describe expected interaction or main effects in statistical terms]
```

**Example:**
```markdown
## Hypothesis

**Primary Hypothesis:**
Memory domains will show differential forgetting trajectories, with What showing slowest forgetting (shallowest slope), Where intermediate, and When fastest forgetting (steepest slope).

**Secondary Hypotheses:**
1. Divergence will increase after ~24 hours (consolidation period, T2)
2. All domains will show non-linear forgetting (logarithmic or quadratic better than linear)

**Theoretical Rationale:**
Dual-process theory suggests What can rely on familiarity (perirhinal cortex), while Where and When require hippocampal binding. Consolidation theory predicts hippocampal-dependent memories are more vulnerable during early consolidation (T1→T2, ~0-24h). Non-linear forgetting reflects consolidation + retrieval dynamics.

**Expected Effect Pattern:**
Significant Domain × Time interaction in LMM analysis. Post-hoc contrasts should show: What ≠ When (p < 0.001), Where intermediate. Quadratic or log time terms should improve model fit (ΔAIC > 10).
```

**Extraction Guidance for rq_concept:**
- Read RQ section from ANALYSES_CHX.md for hypothesis statements
- Extract primary and secondary hypotheses
- Identify theoretical justification from Section 3
- Extract expected statistical patterns
- Format according to template

**Validation Note:**
rq_stats agent will validate hypotheses are testable and statistically appropriate.

---

## Section 5: Memory Domains

**Purpose:** Specify which WWW episodic memory domains this RQ examines

**Required Content:**
- Domain selection (What, Where, When)
- Tag specifications from data_structure.md (exact domain codes)
- Domain disambiguation (for Where: -L-, -U-, -D- clarification)
- Inclusion/exclusion rationale

**Format:**
```markdown
## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming

- [ ] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy)
  - [ ] `-U-` tags (pick-up location)
  - [ ] `-D-` tags (put-down location)
  - Disambiguation: [Which Where tags included and why?]

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
[Explain why these specific domains selected for this RQ]

**Exclusion Rationale (if applicable):**
[Explain why any domains or sub-tags excluded]
```

**Example:**
```markdown
## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: **ALL Where tags included** because some items only have -L- (e.g., Room Free Recall). Excluding -L- would lose spatial items. Complete spatial coverage needed.

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ examines all three WWW episodic memory components to test differential forgetting trajectories. Complete coverage of What/Where/When binding is theoretically necessary per Tulving's episodic memory definition.

**Exclusion Rationale:**
None - all WWW domains included for comprehensive episodic memory assessment.
```

**Extraction Guidance for rq_concept:**
- Read RQ section from ANALYSES_CHX.md for domain mentions
- Identify which domains (What, Where, When)
- For Where: Determine if -L-, -U-, -D- disambiguation needed
- Extract rationale for inclusions/exclusions
- Format as checkboxes (checked = included, unchecked = excluded)

**Critical Note:**
Where domain requires explicit -L-/-U-/-D- clarification to prevent ambiguity. If thesis doesn't specify, rq_concept should trigger CLARITY ERROR circuit breaker (per agent_best_practices.md).

---

## Section 6: Analysis Approach

**Purpose:** Describe high-level analysis strategy and methods

**Required Content:**
- Analysis type (IRT, LMM, CTT, other)
- Step-by-step analysis workflow (user's understanding)
- Special methods (2-pass IRT, covariates, transformations, etc.)
- Expected tools from tools_inventory.md

**Format:**
```markdown
## Analysis Approach

**Analysis Type:**
[Primary analysis method: IRT, LMM, CTT, Correlation, ANOVA, etc.]

**High-Level Workflow:**

**Step 1:** [First analysis step in plain language]
**Step 2:** [Second step]
**Step 3:** [Third step]
**Step 4:** [Fourth step]
[Additional steps as needed]

**Data Preprocessing (Per Solution Section 1.4):**
[Document preprocessing requirements for this RQ]
- **Accuracy Scores (-ANS tags):** Dichotomize before IRT: 1 = 1, all <1 = 0 (no partial credit)
- **Confidence Ratings:** Use raw 1-5 Likert scale (no bias correction, preserves interpretability)
- **IRT Model:** GRM (Graded Response Model - handles both dichotomous and polytomous items)
- **Likert Response Bias:** Document response style patterns (% using full range vs extremes), do NOT correct

**Special Methods:**
[Any unusual or project-specific methods? E.g., 2-pass IRT purification (Decision D039), TSVR time variable (Decision D070), dual reporting (Decision D068)]
```

**Example:**
```markdown
## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation + LMM (Linear Mixed Models) for trajectory modeling

**High-Level Workflow:**

**Step 1:** IRT Pass 1 - Calibrate GRM on all VR items (What/Where/When combined)
**Step 2:** Item Purification - Remove items with extreme difficulty (|b| > 3.0) or low discrimination (a < 0.4) per Decision D039
**Step 3:** IRT Pass 2 - Re-calibrate GRM on purified items
**Step 4:** Theta Extraction - Extract ability estimates per participant × test × domain
**Step 5:** TSVR Merge - Merge theta scores with Time Since VR (actual hours, not nominal days) per Decision D070
**Step 6:** LMM Trajectory Modeling - Fit Domain × Time interaction with random slopes

**Data Preprocessing (Per Solution Section 1.4):**
- **Accuracy Scores:** Dichotomize before IRT (1 = 1, <1 = 0) - items with partial scores converted to binary
- **Confidence Ratings:** Use raw 1-5 Likert (no bias correction) - preserves direct interpretability
- **IRT Model:** GRM handles both dichotomous (accuracy: 2 categories) and polytomous (confidence: 5 categories) in single calibration
- **Likert Response Bias:** Document % participants using full 1-5 range vs extremes only, do NOT correct

**Special Methods:**
- **2-Pass IRT Purification** (Decision D039): Mandatory for all IRT analyses to remove psychometrically problematic items
- **TSVR Time Variable** (Decision D070): Use actual hours since encoding, not nominal days (0, 1, 3, 6)
- **Dual-Scale Trajectory Plots** (Decision D069): Plot theta + probability scales for interpretability
- **GRM Model Clarification:** GRM (Graded Response Model) handles BOTH dichotomous (2 categories: 0, 1) and polytomous (5 categories: 1-5) items. For dichotomized accuracy, GRM reduces to 2PL dichotomous IRT mathematically. No conflict with thesis "dichotomous IRT" terminology - same model.
```

**Extraction Guidance for rq_concept:**
- Read RQ section from ANALYSES_CHX.md for analysis approach
- Extract analysis type (IRT, LMM, etc.)
- Identify step-by-step workflow
- Note any Decision numbers mentioned (D039, D068, D069, D070)
- Format according to template

**WARNING: Avoid Template Contamination**
- Extract ONLY factual information from ANALYSES_CHX.md thesis section
- Do NOT copy timing examples from this template (e.g., test timing may vary per RQ)
- Do NOT invent details not present in thesis
- If thesis unclear → Trigger CLARITY ERROR (per agent_best_practices.md)

**Validation Note:**
rq_stats agent will validate analysis approach is appropriate and feasible with existing tools.

---

## Section 7: Data Source

**Purpose:** Specify exactly where data comes from (RAW vs DERIVED)

**Required Content:**
- Data type (RAW from master.xlsx OR DERIVED from other RQs/steps)
- If RAW: Tag patterns from master.xlsx
- If DERIVED: Source RQ and file paths
- Participant inclusion/exclusion criteria
- Item inclusion/exclusion criteria
- Test inclusion/exclusion criteria

**Format:**
```markdown
## Data Source

**Data Type:**
[RAW (from master.xlsx) OR DERIVED (from other RQ outputs)]

### If RAW Data:

**Tag Patterns:**
- Domain tags: [e.g., -N-, -L-/-U-/-D-, -O-]
- Paradigm codes: [e.g., IFR, ICR, IRE, RFR, etc.]
- Complete pattern: [e.g., "RVR-X-N-IFR-" for What + Interactive Free Recall]

**Extraction Method:**
[How data_prep agent extracts from master.xlsx]

### If DERIVED Data:

**Source RQ:**
[Which RQ outputs are inputs? E.g., "RQ 5.1"]

**File Paths:**
[Exact file paths, e.g., "results/ch5/rq1/data/step03_theta_scores.csv"]

**Dependencies:**
[What must complete before this RQ can run?]

### Inclusion/Exclusion Criteria:

**Participants:**
- [ ] All 100 participants
- [ ] Subset: [Criteria if subset, e.g., "≥3 test sessions"]
- [ ] Exclude: [Criteria if exclusions, e.g., ">30% missing VR data"]

**Items:**
- [ ] All VR items
- [ ] Subset: [Criteria if subset, e.g., "Interactive items only (IFR, ICR, IRE)"]
- [ ] Exclude: [Criteria if exclusions, e.g., "Room Free Recall (RFR)"]

**Tests:**
- [ ] All 4 tests (T1, T2, T3, T4)
- [ ] Subset: [Criteria if subset, e.g., "T1, T3, T4 only (exclude T2 - same day)"]
```

**Example (RAW Data):**
```markdown
## Data Source

**Data Type:**
RAW (extracted from master.xlsx)

### RAW Data Extraction:

**Tag Patterns:**
- Domain tags: `-N-` (What), `-L-/-U-/-D-` (Where), `-O-` (When)
- Paradigm codes: IFR, ICR, IRE (interactive paradigms only)
- Complete patterns:
  - What: `RVR-X-N-{IFR|ICR|IRE}-`
  - Where: `RVR-X-{L|U|D}-{IFR|ICR|IRE}-`
  - When: `RVR-X-O-{IFR|ICR|IRE}-`

**Extraction Method:**
data_prep agent uses `tools.data.extract_vr_items_wide` with tag patterns above, stacks by composite_ID (UID-Test-Domain), yields long-format CSV with columns: composite_ID, item_code, response (0-3).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)

**Items:**
- [x] Interactive paradigms only (IFR, ICR, IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED (different response format)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Note: Time variable uses TSVR (actual hours since encoding), not nominal days
```

**Example (DERIVED Data):**
```markdown
## Data Source

**Data Type:**
DERIVED (from RQ 5.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.1 (Domain-Specific Forgetting Trajectories)

**File Paths:**
- `results/ch5/rq1/data/step03_theta_scores.csv` (IRT ability estimates)
- Columns: composite_ID, domain, test, theta

**Dependencies:**
RQ 5.1 must complete Steps 1-3 (IRT calibration, purification, theta extraction) before this RQ can run.

**Usage:**
This RQ uses theta scores from RQ 5.1 as outcome variable for advanced trajectory modeling with covariates.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.1 (inherited inclusion criteria)

**Items:**
- N/A (theta scores already aggregated per domain)

**Tests:**
- [x] All 4 tests (inherited from RQ 5.1)
```

**Extraction Guidance for rq_concept:**
- Read RQ section from ANALYSES_CHX.md for data source mentions
- Determine RAW (from master.xlsx) vs DERIVED (from other RQs)
- If RAW: Extract tag patterns and inclusion/exclusion criteria
- If DERIVED: Extract source RQ and file paths
- Format according to template

**Critical Note:**
Data source ambiguity triggers CLARITY ERROR circuit breaker (per agent_best_practices.md). If thesis doesn't clearly specify RAW vs DERIVED, rq_concept must FAIL and report.

**Validation Note:**
rq_planner will read this section to create detailed data specifications in 2_plan.md.

---

## Validation Feedback Sections (Appended by Agents)

After rq_concept creates the 7 core sections, two validation agents append feedback:

### Scholarly Validation Feedback (Appended by rq_scholar)

**Workflow Step 5:** rq_scholar reads 1_concept.md, validates theoretical grounding, appends feedback

**Appended Structure (from scholar_report.md template specification):**
```markdown
---

## Scholarly Validation Feedback

**Validated By:** rq_scholar agent
**Date:** [Timestamp]

### Claims Extracted

1. [Claim from theoretical background or hypothesis]
2. [Claim from theoretical background or hypothesis]
3. [...]

### Evidence Sources

1. [Citation and supporting evidence for Claim 1]
2. [Citation and supporting evidence for Claim 2]
3. [...]

### Validation Results

- Claim 1: **SUPPORTED** [Rationale]
- Claim 2: **UNSUPPORTED** [Rationale + alternative evidence]
- Claim 3: **SUPPORTED** [Rationale]

### Recommendations

**Corrections:**
[Any claims that need correction]

**Additions:**
[Additional citations or theoretical context to strengthen]

**Clarifications:**
[Ambiguities to resolve]
```

**Purpose:** Ensure theoretical claims are grounded in episodic memory literature

---

### Statistical Validation Feedback (Appended by rq_stats)

**Workflow Step 6:** rq_stats reads 1_concept.md, validates statistical methods, appends feedback

**Appended Structure (from stats_report.md template specification):**
```markdown
---

## Statistical Validation Feedback

**Validated By:** rq_stats agent
**Date:** [Timestamp]

### Proposed Methods

1. [Method from analysis approach, e.g., "IRT GRM calibration"]
2. [Method from analysis approach, e.g., "LMM with Domain × Time interaction"]
3. [...]

### Method Appropriateness

- Method 1: **APPROPRIATE** [Rationale]
- Method 2: **INAPPROPRIATE** [Rationale + alternative]
- Method 3: **APPROPRIATE WITH CAVEATS** [Rationale + conditions]

### Alternative Considerations

[Other statistical approaches to consider for this RQ]

### Validation Results

**Overall Assessment:** APPROVED / APPROVED WITH REVISIONS / REJECTED

**Rationale:**
[Detailed justification for assessment]

**Required Revisions (if applicable):**
[Specific changes needed before proceeding]
```

**Purpose:** Ensure statistical methods are appropriate for hypothesis testing

---

## Complete 1_concept.md Example

**After rq_concept creates (7 sections):**
- Section 1: RQ Title and ID
- Section 2: Research Question Statement
- Section 3: Theoretical Background
- Section 4: Hypothesis
- Section 5: Memory Domains
- Section 6: Analysis Approach
- Section 7: Data Source

**After rq_scholar appends (+1 section):**
- Scholarly Validation Feedback

**After rq_stats appends (+1 section):**
- Statistical Validation Feedback

**Total:** 9 sections when validation complete

**User reviews at workflow step 7** → Only user approval gate in entire workflow

---

## Implementation Notes for rq_concept Agent

**What rq_concept Does:**
1. Read: agent_best_practices.md (Step 1)
2. Read: status.yaml (Step 2)
3. Check: Prior agents = success, this agent = pending (Step 3)
4. **Read: docs/v4/templates/concept.md** (Step 4) ← Reads this template
5. Read: docs/v4/thesis/ANALYSES_CHX.md TABLE OF CONTENTS (Step 5)
6. Read: docs/v4/thesis/ANALYSES_CHX.md relevant section (Step 6)
7. Ultrathink: Map thesis content to template format (Step 7)
8. Bash: Create results/chX/rqY/docs/1_concept.md (Step 8)
9. Write: Fill 1_concept.md with 7 sections mapped from thesis (Step 9)
10. Edit: status.yaml (update to success, write context_dump) (Step 10)
11. Report: Success and quit (Step 11)

**What rq_concept Does NOT Do:**
- Does NOT ask user questions (that's rq_planner's job in 2_plan.md)
- Does NOT validate scholarly claims (that's rq_scholar's job)
- Does NOT validate statistical methods (that's rq_stats's job)
- Does NOT create analysis specifications (that's rq_planner/rq_tools/rq_analysis's job)

**Extraction Strategy:**
- Parse ANALYSES_CHX.md RQ section
- Map prose to template structure (7 sections)
- Preserve user's language where possible
- Add structure/formatting from template
- If critical info missing → CLARITY ERROR circuit breaker

**Validation Workflow:**
1. rq_concept creates 1_concept.md (7 sections)
2. rq_scholar reads → validates → appends feedback
3. rq_stats reads → validates → appends feedback
4. User reviews validated 1_concept.md (9 sections total)
5. If approved → continue to rq_planner

---

## Cross-RQ Dependencies

**If RQ depends on another RQ's outputs:**

**rq_concept Responsibilities:**
1. State dependency clearly in Section 7 (Data Source)
2. Specify source RQ ID (e.g., "RQ 5.1")
3. Specify exact file paths (e.g., "results/ch5/rq1/data/step03_theta_scores.csv")
4. Note what must complete before this RQ runs

**Master Orchestrator Responsibilities:**
1. Read 1_concept.md Section 7 for dependencies
2. Verify source RQ is complete before invoking rq_planner
3. If source RQ incomplete → defer this RQ until dependency satisfied

**Example Dependency Chain:**
- RQ 5.1: Independent (RAW data from master.xlsx)
- RQ 5.2: Depends on RQ 5.1 (uses theta scores)
- RQ 5.3: Depends on RQ 5.1 (uses item parameters)

---

## Circuit Breaker Triggers

**Per agent_best_practices.md, rq_concept triggers circuit breakers for:**

### CLARITY ERROR
- **Trigger:** thesis section vague about domain tags (-L- vs -U- vs -D-)
- **Example:** "This RQ uses Where domain" (which Where tags? -L-? -U-? -D-? All?)
- **Action:** Quit, report "CLARITY ERROR: Where domain tags not specified. Need explicit -L-/-U-/-D- disambiguation."

### EXPECTATIONS ERROR
- **Trigger:** Thesis section missing required information
- **Example:** No hypothesis stated, no data source mentioned
- **Action:** Quit, report "EXPECTATIONS ERROR: Section 4 (Hypothesis) missing from thesis RQ X.Y"

### TOOL ERROR
- **Trigger:** Analysis approach mentions non-existent tool
- **Example:** "Use fancy_new_algorithm() for analysis" (not in tools_inventory.md)
- **Action:** Quit, report "TOOL ERROR: fancy_new_algorithm not found in tools_inventory.md"

**Philosophy:** rq_concept quits on uncertainty, reports to master, waits for clarification. Never guesses.

---

## Version History

**Version 4.0 (2025-11-16):**
- Initial v4.X template specification
- 7 required sections per specification 4.2.1
- Designed for rq_concept agent extraction from ANALYSES_CHX.md thesis
- Validation feedback appended by rq_scholar and rq_stats agents
- User approval gate at workflow step 7

**v3.0 → v4.0 Migration Notes:**
- v3.0: User manually filled concept.md (9 sections, user form)
- v4.0: Agent extracts from ANALYSES_CHX.md, creates 1_concept.md (7 sections, agent output)
- v3.0: concept.md at root level (results/chX/rqY/concept.md)
- v4.0: 1_concept.md in docs/ subfolder (results/chX/rqY/docs/1_concept.md)
- v3.0: Single validation phase (rq-specification agent MODE 1)
- v4.0: Dual validation (rq_scholar + rq_stats agents append feedback)

---

**End of Template Specification**
