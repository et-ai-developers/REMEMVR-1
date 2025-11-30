# 1_concept.md Format Specification

**Last Updated:** 2025-11-16
**Version:** 4.0
**Purpose:** Defines the mandatory structure for 1_concept.md (RQ concept document)
**Audience:** rq_concept agent when creating 1_concept.md from thesis

---

## Document Structure

**7 Required Sections (created by rq_concept):**
1. RQ Title and ID
2. Research Question Statement
3. Theoretical Background
4. Hypothesis
5. Memory Domains
6. Analysis Approach
7. Data Source

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
[Any unusual or project-specific methods mentioned in thesis? E.g., 2-pass IRT purification, TSVR time variable, dual reporting]
```

**Example:**
```markdown
## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation + LMM (Linear Mixed Models) for trajectory modeling

**High-Level Workflow:**

**Step 1:** IRT Pass 1 - Calibrate GRM on all VR items (What/Where/When combined)
**Step 2:** Item Purification - Remove items with extreme difficulty (|b| > 3.0) or low discrimination (a < 0.4)
**Step 3:** IRT Pass 2 - Re-calibrate GRM on purified items
**Step 4:** Theta Extraction - Extract ability estimates per participant × test × domain
**Step 5:** TSVR Merge - Merge theta scores with Time Since VR (actual hours, not nominal days)
**Step 6:** LMM Trajectory Modeling - Fit Domain × Time interaction with random slopes

**Data Preprocessing (Per Solution Section 1.4):**
- **Accuracy Scores:** Dichotomize before IRT (1 = 1, <1 = 0) - items with partial scores converted to binary
- **Confidence Ratings:** Use raw 1-5 Likert (no bias correction) - preserves direct interpretability
- **IRT Model:** GRM handles both dichotomous (accuracy: 2 categories) and polytomous (confidence: 5 categories) in single calibration
- **Likert Response Bias:** Document % participants using full 1-5 range vs extremes only, do NOT correct

**Special Methods:**
- **2-Pass IRT Purification:** Mandatory for all IRT analyses to remove psychometrically problematic items
- **TSVR Time Variable:** Use actual hours since encoding, not nominal days (0, 1, 3, 6)
- **Dual-Scale Trajectory Plots:** Plot theta + probability scales for interpretability
- **GRM Model Clarification:** GRM (Graded Response Model) handles BOTH dichotomous (2 categories: 0, 1) and polytomous (5 categories: 1-5) items. For dichotomized accuracy, GRM reduces to 2PL dichotomous IRT mathematically. No conflict with thesis "dichotomous IRT" terminology - same model.
```

**Extraction Guidance for rq_concept:**
- Read RQ section from ANALYSES_CHX.md for analysis approach
- Extract analysis type (IRT, LMM, etc.)
- Identify step-by-step workflow
- Extract any special methods or project-wide requirements mentioned in thesis
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
[Exact file paths, e.g., "results/ch5/5.2.1/data/step03_theta_scores.csv"]

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
- `results/ch5/5.2.1/data/step03_theta_scores.csv` (IRT ability estimates)
- Columns: composite_ID, domain, test, theta

**Dependencies:**
RQ 5.2.1 must complete Steps 1-3 (IRT calibration, purification, theta extraction) before this RQ can run.

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

---

**End of Template Specification**
