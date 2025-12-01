# 1_concept.md Format Specification

**Last Updated:** 2025-12-01
**Version:** 5.0
**Purpose:** Defines the mandatory structure for 1_concept.md (RQ concept document)
**Audience:** rq_concept agent when creating 1_concept.md from rq_refactor.tsv

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
- Type number within chapter (1-4 for ch5)
- RQ number within type (1-9)
- Type name (General, Domains, Paradigms, Congruence)
- Subtype name (specific analysis focus)
- Descriptive title summarizing the RQ focus

**Format:**
```markdown
# RQ X.Y.Z: [Descriptive Title]

**Chapter:** X
**Type:** [Type Name]
**Subtype:** [Subtype Name]
**Full ID:** X.Y.Z
```

**Example:**
```markdown
# RQ 5.1.1: Functional Form Comparison

**Chapter:** 5
**Type:** General
**Subtype:** Functional Form Comparison
**Full ID:** 5.1.1
```

**Hierarchical Numbering (Chapter 5):**
- **5.1.X** = General (omnibus "All" factor analysis)
- **5.2.X** = Domains (What/Where/When analysis)
- **5.3.X** = Paradigms (Free/Cued/Recognition analysis)
- **5.4.X** = Congruence (Common/Congruent/Incongruent analysis)

**Extraction Guidance for rq_concept:**
- Read rq_refactor.tsv Number column
- Parse hierarchical format: "5.1.1" -> Chapter 5, Type 1, RQ 1
- Extract Type and Subtype from TSV columns
- Extract Title from TSV Title column
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
Which functional form best describes episodic forgetting trajectories across a 6-day retention interval?

**Scope:**
This RQ examines forgetting rates using IRT-derived ability estimates across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6). Time variable uses TSVR (actual hours since encoding), not nominal days. Compares 5 candidate models (Linear, Quadratic, Logarithmic, Linear+Logarithmic, Quadratic+Logarithmic). N=100 participants x 4 tests = 400 observations.

**Theoretical Framing:**
Exploratory analysis to determine optimal functional form for subsequent analyses. Best model selected via AIC and Akaike weights. Foundation for all trajectory analyses in Chapter 5.
```

**Extraction Guidance for rq_concept:**
- Read rq_refactor.tsv Title column for primary question
- Extract scope from Data_Required column (sample size, observations)
- Extract theoretical context from Hypothesis column
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
[To be added by rq_scholar]

**Theoretical Predictions:**
[Extracted from Hypothesis column]

**Literature Gaps:**
[To be identified by rq_scholar]
```

**Extraction Guidance for rq_concept:**
- Extract theory mentions from rq_refactor.tsv Hypothesis column
- Note: This section may be minimal - rq_scholar will enhance later
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
Exploratory analysis comparing 5 candidate models (Linear, Quadratic, Logarithmic, Linear+Logarithmic, Quadratic+Logarithmic). No directional prediction. Expected: best model Akaike weight > 0.30.

**Secondary Hypotheses:**
None - exploratory analysis.

**Theoretical Rationale:**
Functional form determination is prerequisite for subsequent trajectory analyses. Non-linear forms (logarithmic) often fit forgetting data better than linear forms based on empirical forgetting curves.

**Expected Effect Pattern:**
Best model identified by lowest AIC. Akaike weights sum to 1.0 +/- 0.01. Best model weight > 0.30 indicates clear winner.
```

**Extraction Guidance for rq_concept:**
- Extract from rq_refactor.tsv Hypothesis column
- Identify primary vs secondary predictions
- Extract expected statistical patterns (p-values, effect sizes, thresholds)
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

**Domain Selection by Type (Chapter 5):**

| Type | Domains/Factors |
|------|-----------------|
| **5.1.X General** | Single "All" omnibus factor (all items combined) |
| **5.2.X Domains** | What (-N-), Where (-L-/-U-/-D-), When (-O-) |
| **5.3.X Paradigms** | Free Recall (IFR), Cued Recall (ICR), Recognition (IRE) |
| **5.4.X Congruence** | Common (i1/i2), Congruent (i3/i4), Incongruent (i5/i6) |

**Extraction Guidance for rq_concept:**
- Read rq_refactor.tsv Data_Required column for domain mentions
- Infer from Type column if Data_Required unclear
- For Where: Determine if -L-, -U-, -D- disambiguation needed
- Extract rationale for inclusions/exclusions
- Format as checkboxes (checked = included, unchecked = excluded)

---

## Section 6: Analysis Approach

**Purpose:** Describe high-level analysis strategy and methods

**Required Content:**
- Analysis type (IRT, LMM, CTT, other)
- Step-by-step analysis workflow (user's understanding)
- Expected outputs and file specifications
- Success criteria for validation

**Format:**
```markdown
## Analysis Approach

**Analysis Type:**
[Primary analysis method: IRT, LMM, CTT, Correlation, ANOVA, etc.]

**High-Level Workflow:**

**Step 0:** [Data extraction if applicable]
**Step 1:** [First analysis step in plain language]
**Step 2:** [Second step]
**Step 3:** [Third step]
**Step 4:** [Fourth step]
[Additional steps as needed]

**Expected Outputs:**
[From Expected_Output - file names and structure]

**Success Criteria:**
[From Success_Criteria - validation requirements]
```

**Example:**
```markdown
## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation + LMM (Linear Mixed Models) for trajectory modeling

**High-Level Workflow:**

**Step 1:** IRT Pass 1 calibration with single omnibus "All" factor on all items using GRM, p1_med prior
**Step 2:** Item purification (Decision D039): exclude items with |b| > 3.0 OR a < 0.4
**Step 3:** IRT Pass 2 re-calibration on purified items
**Step 4:** Merge theta with TSVR, create time transformations
**Step 5:** Fit 5 LMMs with REML=False: Linear, Quadratic, Logarithmic, Lin+Log, Quad+Log; all with random slopes by UID
**Step 6:** Model selection via AIC, compute Akaike weights
**Step 7:** Prepare plot data: observed means + model predictions, theta and probability scales (Decision D069)

**Expected Outputs:**
- data/step01_theta_scores.csv
- data/step02_purified_items.csv (40-60 items)
- data/step03_theta_scores.csv (final)
- data/step04_lmm_input.csv (400 rows)
- results/step05_model_comparison.csv (5 models)
- data/step06_best_model.pkl
- results/step06_aic_comparison.csv
- plots/step07_functional_form_theta_data.csv
- plots/step07_functional_form_probability_data.csv

**Success Criteria:**
- IRT convergence: theta in [-4,4], SE in [0.1,1.5]
- Purification: 30-70% retention
- LMM: all 5 models converge, AIC finite
- Akaike weights sum to 1.0 +/- 0.01
- Best model weight > 0.30
- Plot data: probability in [0,1], no NaN
```

**Extraction Guidance for rq_concept:**
- Read rq_refactor.tsv Analysis_Specification column for workflow steps
- Read Expected_Output column for file specifications
- Read Success_Criteria column for validation requirements
- Format according to template

---

## Section 7: Data Source

**Purpose:** Specify exactly where data comes from (RAW vs DERIVED)

**Required Content:**
- Data type (RAW from dfData.csv OR DERIVED from other RQs/steps)
- If RAW: Source file and extraction method
- If DERIVED: Source RQ and file paths
- Participant inclusion/exclusion criteria
- Item inclusion/exclusion criteria
- Test inclusion/exclusion criteria

**Format:**
```markdown
## Data Source

**Data Type:**
[RAW (from dfData.csv) OR DERIVED (from other RQ outputs)]

### If RAW Data:

**Source File:**
[e.g., data/cache/dfData.csv]

**Tag Patterns:**
- Domain tags: [e.g., -N-, -L-/-U-/-D-, -O-]
- Paradigm codes: [e.g., IFR, ICR, IRE, RFR, etc.]

**Extraction Method:**
[How Step 0 extracts from source]

### If DERIVED Data:

**Source RQ:**
[Which RQ outputs are inputs? E.g., "RQ 5.1.1"]

**File Paths:**
[Exact file paths, e.g., "results/ch5/5.1.1/data/step03_theta_scores.csv"]

**Dependencies:**
[What must complete before this RQ can run?]

### Inclusion/Exclusion Criteria:

**Participants:**
- [ ] All 100 participants
- [ ] Subset: [Criteria if subset]
- [ ] Exclude: [Criteria if exclusions]

**Items:**
- [ ] All VR items
- [ ] Subset: [Criteria if subset]
- [ ] Exclude: [Criteria if exclusions]

**Tests:**
- [ ] All 4 tests (T1, T2, T3, T4)
- [ ] Subset: [Criteria if subset]
```

**Example (RAW Data - Root RQ):**
```markdown
## Data Source

**Data Type:**
RAW (extracts directly from dfData.csv)

### RAW Data Extraction:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- All interactive paradigm items (IFR, ICR, IRE)
- Excludes RFR, TCR, RRE

**Extraction Method:**
Step 0 extracts from dfData.csv, creates:
- data/step00_irt_input.csv (wide format binary responses)
- data/step00_tsvr_mapping.csv (time mapping)
- data/step00_q_matrix.csv (single "All" factor)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)

**Items:**
- [x] Interactive paradigms only (IFR, ICR, IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
```

**Example (DERIVED Data):**
```markdown
## Data Source

**Data Type:**
DERIVED (from RQ 5.1.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.1.1 (Functional Form Comparison)

**File Paths:**
- results/ch5/5.1.1/data/step06_best_model.pkl (saved LMM model)
- results/ch5/5.1.1/data/step03_theta_scores.csv (IRT ability estimates)
- results/ch5/5.1.1/data/step04_lmm_input.csv (merged data)

**Dependencies:**
RQ 5.1.1 must complete Steps 1-6 (IRT calibration, LMM fitting, model selection) before this RQ can run.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.1.1 (inherited inclusion criteria)

**Items:**
- N/A (theta scores already aggregated)

**Tests:**
- [x] All 4 tests (inherited from RQ 5.1.1)
```

**Extraction Guidance for rq_concept:**
- Read rq_refactor.tsv Data_Required column
- Determine RAW vs DERIVED:
  - If mentions "dfData.csv" or "data/cache" -> RAW
  - If mentions "results/ch5/X.Y.Z" or "from RQ X.Y.Z" -> DERIVED
- Extract file paths and inclusion/exclusion criteria
- Format according to template

**Critical Note:**
Data source ambiguity triggers CLARITY ERROR circuit breaker. If TSV doesn't clearly specify RAW vs DERIVED, rq_concept must FAIL and report.

---

**End of Template Specification**
