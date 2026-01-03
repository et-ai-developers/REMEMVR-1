# Thesis Writing System v2 Modular Stateless Restructure

**Topic Description:** Complete restructuring of thesis writing system from monolithic write.md into 5 modular stateless instruction files (write.md + write4/5/6/7.md). Implements "Engaging, Not Exhausting" philosophy with Dinner Party Test principle. Includes conflicts analysis revealing NO major blockers, chapters.md update with current execution status, and flagship vs integrated RQ strategy documentation.

---

## Session (2026-01-02 Afternoon - Thesis Writing System Restructure) (2026-01-02 15:30)

**Task:** RESTRUCTURE thesis/write.md INTO MODULAR STATELESS CHAPTER-SPECIFIC INSTRUCTIONS + ANALYZE CONFLICTS WITH EXISTING THESIS STRUCTURE

**Context:** After rq_report v1.0.0 completion (65/65 RQs documented, 2.1MB reports), user requested: "split write.md into 4 files: write4.md write5.md write6.md write7.md. These are stateless instructions agents must read when writing thesis sections. Include overall thesis context to establish narrative. HATE for thesis to be dense/exhausting - want interesting/engaging read to keep assessors in good mood. Keep all thesis stuff in ./thesis/ (NOT ./reports/)."

**OUTCOME:** THESIS WRITING SYSTEM v2.0 COMPLETE + CONFLICTS ANALYSIS COMPLETE + CHAPTERS.MD UPDATED + 5 MODULAR INSTRUCTION FILES CREATED

**Archived from:** state.md
**Original Date:** 2026-01-02 Afternoon  
**Reason:** Session completed - thesis writing system v2.0 restructuring finished, can reference archive for implementation details

---

### 1. Context-Finder Research Phase (~10 min)

**Pre-Restructure Research:**

Invoked context-finder to search for:
1. Previous thesis writing plans or chapter organization strategies
2. Agent design patterns for prose generation (rq_results, context-finder)
3. Writing style guidelines or narrative structure decisions
4. Existing thesis structure documents (introduction.md, methods.md, rationale.md, chapters.md)
5. Conflicts between different thesis structure versions

**Key Findings:**

**Existing Thesis Structure (from context-finder + Read operations):**
- **thesis/introduction.md** - Ch1 partial draft (176 lines, S1.1-S1.6 complete, S1.7 placeholder)
- **thesis/methods.md** - Ch2 partial draft (137 lines, complete through S2.3.10)
- **thesis/rationale.md** - Ch3 partial draft (136 lines, complete through S3.11)
- **thesis/chapters.md** - Old RQ catalog (685 lines, TYPE-based RQ numbering, outdated status)

**Old Write Plan (discovered in search):**
- `results/ch5/write.md` - Stateless execution paradigm from OLD location (wrong directory)
- Monolithic approach (Ch4 + Ch5 mixed in single file)
- Designed for /clear --> Read write.md --> Execute workflow (NO /save, NO /refresh)

**Conflicts Identified:**
- RQ numbering evolved (TYPE-based "5.1-5.2" --> SPECIFIC "5.1.1, 5.1.2")
- Partial credit description outdated (methods.md says 0.5/0.25, user abandoned it)
- Ch4 strategy ambiguous (not addressed in write.md, needs user decision)

**Design Patterns Extracted (from rq_results, rq_report):**
- Stateless agents read instructions fresh each invocation
- Multi-source synthesis (6+ file types integrated per output)
- Circuit breakers (5 types, quit on uncertainty)
- Multimodal inspection (Read PNG files visually)
- 10-section report template (rq_report precedent)

---

### 2. Conflicts Analysis (~20 min)

**Created:** `thesis/conflicts_analysis.md` (217 lines)

**Analysis Approach:**
1. Read all existing thesis structure files (introduction, methods, rationale, chapters.md)
2. Compare with write.md execution plan (Ch5-Ch6 targets)
3. Identify conflicts (structural, content, methodology)
4. Classify severity (NO CONFLICTS / MINOR / MAJOR)

**Findings:**

**NO MAJOR CONFLICTS (Thesis structure consistent):**
- Chapter numbering aligned (Ch1-8 as expected)
- Theoretical framework consistent (framework-agnostic, PMAT acknowledged as robust)
- Study design basics match (N=100, ages 20-70, Day 0/1/3/6, What/Where/When, 5-star confidence)

**3 MINOR CONFLICTS (Easy to resolve):**

1. **RQ Numbering Scheme Evolution:**
   - OLD: chapters.md has RQ TYPES ("5.1-5.2: Domain trajectories")
   - NEW: write.md references SPECIFIC RQs ("5.1.1, 5.2.1, 5.3.1")
   - Resolution: RQs EXPANDED (each type became 2-7 specific RQs), update chapters.md

2. **Partial Credit Scoring:**
   - methods.md S2.3.7: "partial credit 0.5/0.25"
   - User statement: "too problematic, stick with dichotomous 0/1"
   - Resolution: Update methods.md to reflect final decision (dichotomous only)

3. **Chapter 4 Strategy Ambiguity:**
   - write.md targets Ch5-Ch6 only
   - Ch5-Ch6 need cross-refs to Ch4 (e.g., "S4.2.2 IRT purification")
   - Ch4 doesn't exist yet
   - Resolution: Ask user - Write Ch4 FIRST or use PLACEHOLDERS?

**MAJOR GAPS (Not conflicts, just missing work):**
- Ch4 (Analysis Methods) - NOT written
- Ch7 (Individual Differences) - 0/20 RQs executed
- S1.7 (Thesis Aims) - Placeholder only (no content)

**Recommendation:** PROCEED with write.md execution after resolving 3 minor conflicts

---

### 3. Chapters.md Update (~30 min)

**Created:** `thesis/chapters_UPDATED.md` (815 lines, comprehensive RQ catalog)

**Purpose:** Update old chapters.md with current execution status, major findings, X.Y.Z numbering

**Updates Applied:**

**Execution Status:**
- Ch1-3: Partial drafts exist (introduction, methods, rationale)
- Ch4: Not written (analytical methods)
- **Ch5: 35/35 RQs PLATINUM certified + 35 reports generated** --> Ready for thesis writing
- **Ch6: 30/30 RQs PLATINUM certified + 30 reports generated** --> Ready for thesis writing
- Ch7: 0/20 RQs executed (deferred, 9/20 preliminary CTT analyses exist)
- Ch8: Not written (discussion)

**RQ Numbering Updated:**
- OLD: "RQ 5.1-5.2: Domain trajectories"
- NEW: "RQ 5.1.1 (General), 5.2.1 (Domain What/Where/When), 5.2.2 (consolidation), 5.2.3 (age), etc."
- 15 RQ types (Ch5) --> became 35 specific RQs
- 15 RQ types (Ch6) --> became 30 specific RQs

**Major Findings Documented (per theme):**

**Ch5 Findings:**
- **Power-Law Paradigm Shift:** alpha_eff=0.41 dominates, Log model ranked #33/66 (DAIC=+3.10), evidence ratio 4.7:1
- **Age-Invariant VR Forgetting:** AgexTime beta=0.000022 p=.96 (VR scaffolding hypothesis)
- **Model Averaging Paradigm Shift:** ICC_slope 0.05% --> 21.61% = 432-fold increase
- **Content-Invariant Mechanisms:** Theta-scale trajectories parallel (encoding strength != decay rate)
- **IRT-CTT Convergence:** r>0.90 exceptional (When domain shows 77% exclusion = measurement failure)

**Ch6 Findings:**
- **824x ICC Ratio:** Ordinal confidence ICC=54.1%, Binary accuracy ICC=0.07% (54-221x trait variance)
- **Overconfidence Persistent:** Calibration shows overconfidence across all delays
- **HCE Mechanism:** 15-20% error rate stable (monitoring failure, NOT false memory reconstruction)
- **Dunning-Kruger NOT Supported:** Low performers do NOT show overconfidence (double null)
- **Spatial Dissociation:** Opposite correlations (accuracy +0.99/-0.90 vs confidence -0.24/-0.40)

**Next Steps Section:** Execute thesis/write.md plan (9-15 hours estimated)

**File Status:** Saved as `thesis/chapters_UPDATED.md` (preserve old chapters.md, user can replace when ready)

---

### 4. Modular Writing Instructions Creation (~60 min)

**Goal:** Split monolithic write.md into general + chapter-specific stateless instructions with engaging narrative focus

**Philosophy:** "Make it INTERESTING and ENGAGING - keep assessors in good mood. Not dense exhausting tome."

**Created 5 Files (all in ./thesis/):**

---

**File 1: thesis/write.md (GENERAL INSTRUCTIONS, 422 lines)**

**Purpose:** Universal thesis writing principles, applicable to ALL chapters

**Key Sections:**

1. **THE REMEMVR STORY (Overall Thesis Narrative):**
   - Problem: 140-year measurement paradox (ecological validity OR experimental control)
   - Solution: VR resolves paradox (real-world-like AND standardized)
   - Discovery: Power-law forgetting, age-invariant VR, metacognitive dissociation, model averaging essential
   - Contribution: New assessment paradigm + fundamental principles

2. **WRITING PHILOSOPHY: Engaging, Not Exhausting**
   - DO: Tell story, build progressively, use transitions, synthesize, be concise, vary sentence structure, active voice
   - DON'T: Data dump, repeat yourself, hide in passive voice, assume knowledge, overwhelm with stats, walls of text
   - **"Dinner Party Test":** Could you explain this to smart non-specialist at dinner party? If yes, clear. If no, simplify.
   - **Keep Assessors Engaged:** They read 5-10 theses/year, looking for competence/judgment/communication/contribution

3. **Statistical Reporting Standards:**
   - 5-component format (beta, SE, p, CI, d) for ALL LMM results
   - Null results get equal treatment (don't hide, report with same detail)
   - Example: "Age did not predict forgetting rate (beta=0.000022, SE=0.0004, p=.96, 95% CI [-0.0008, 0.0008], d<0.01)"

4. **Flagship vs Integrated RQ Strategy:**
   - Flagship (6-8 per chapter): 600-900 words, full detail, demonstrate competence
   - Integrated (rest): Summary table + 400-600 words narrative, eliminate redundancy
   - Example: Age null findings x 7 --> reported once with table (not repeated 7 times)

5. **Figure & Table Guidelines:**
   - Figures HELP understanding (not decorative)
   - Publication-quality captions (self-contained, reader doesn't need main text)
   - Tables show cross-RQ patterns (compact presentation)

6. **Synthesis Sections ("So What?"):**
   - Answer: What pattern emerged? What does it mean theoretically? Limitations? How connect forward?
   - Example synthesis provided (Age-Invariant VR Forgetting, 3 paragraphs)

7. **Quality Checklist:**
   - Narrative coherence, analytical rigor, clarity & readability, cross-references, terminology consistency, style & tone

8. **Remember the Goal:**
   - "Would this be interesting to read at 10pm Thursday after assessor read 3 other theses today?"
   - If yes --> doing it right. If no --> simplify, clarify, synthesize.

**Style:** Informal + educational (talking to future agent writer, not formal spec)

---

**File 2: thesis/write4.md (CH4 ANALYSIS METHODS, 268 lines)**

**Purpose:** Extract analytical methodology from 65 RQ reports, write Ch4 (IRT + LMM pipeline)

**Target:** ~8,000-10,000 words

**Why Ch4 Matters:**
- Methodological foundation for Ch5-7
- Ch5-7 say "S4.2.2 IRT purification" --> Ch4 explains what that means
- External examiners verify statistical rigor HERE
- Prevents redundancy (explain each method ONCE, cross-ref from empirical chapters)

**Structure:**
- S4.1 Overview (~500 words) - Two-stage pipeline (IRT --> LMM)
- S4.2 IRT Calibration (~3,000 words) - GRM specification, purification protocol, multidimensional specs, Composite_ID stacking, assumptions/diagnostics
- S4.3 LMM (~3,000 words) - Model specification, time transformations, AIC model selection, random slopes, assumption diagnostics
- S4.4 Effect Sizes (~1,500 words) - Cohen's d, f-squared, eta-squared, ICC, marginal/conditional R-squared
- S4.5 Multiple Comparisons (~1,500 words) - Bonferroni, FDR, dual p-value reporting
- S4.6 IRT-CTT Convergence (~1,000 words) - Validation that IRT theta scores aren't noise
- S4.7 Software & Reproducibility (~500 words) - deepirtools, statsmodels, matplotlib, git repo

**Extraction Strategy:**
- Read 5-10 representative RQ reports Section 4 (Methodology)
- Identify common elements (ALL RQs use these --> document in Ch4)
- Write as GENERAL methodology (not "For RQ 5.1.1 we did X...")
- IF variation exists, note it briefly

**Unresolved Questions Flagged:**
- IRT fit indices (none reported yet - which to include?)
- DIF testing (not done - needed?)
- Monte Carlo sampling (mc_samples=1 vs 100, rationale unclear)
- Multiple comparisons (not yet corrected - apply Bonferroni or FDR?)
- Confidence bias correction (not done - needed?)

**Tone:** Precise, concise, authoritative (methods documentation, not tutorial)

---

**File 3: thesis/write5.md (CH5 FORGETTING TRAJECTORIES, 315 lines)**

**Purpose:** Convert 35 RQ reports --> cohesive Ch5 narrative (~14,000 words)

**Narrative Arc:** "Power-law forgetting challenges 140 years of Ebbinghaus tradition"

**Why Ch5 Matters:**
- Establishes WHAT HAPPENS to VR episodic memory over time
- Foundation for Ch6 (metacognition) and Ch7 (individual differences)
- Discovery: Memory doesn't fade logarithmically (Ebbinghaus wrong for VR)
- Surprise: Age doesn't affect forgetting RATE in VR (contradicts aging literature)

**5 Themes:**

1. **S5.1 Power-Law Forgetting Paradigm** (~3,500 words)
   - Flagship: RQ 5.1.1 (66-model comparison, paradigm shift), 5.1.2 (two-phase), 5.1.4 (model averaging)
   - Integrated: 5.2.1, 5.3.1, 5.4.1, 5.5.1 (power-law replication table)
   - Key Message: Power-law (alpha_eff=0.41) dominates, model averaging essential (N_eff=15 competitive)

2. **S5.2 Content Effects** (~3,000 words)
   - Flagship: 5.2.1 (domain trajectories, When measurement failure), 5.3.1-5.3.2 (retrieval support paradox)
   - Integrated: 5.4.1-5.4.7 (schema), 5.5.1-5.5.7 (spatial)
   - Key Message: Content affects WHAT (baseline), NOT HOW (theta-scale parallel)

3. **S5.3 Age-Invariant VR Forgetting** (~2,000 words)
   - Flagship: 5.1.3 (general age effects, model averaging across 40 models)
   - Integrated: 5.2.3, 5.3.4, 5.4.3, 5.5.3 (age null replication table)
   - Key Message: VR scaffolding equalizes forgetting rates ages 20-70 (AgexTime p>.40, d<0.01)

4. **S5.4 Individual Differences** (~2,500 words)
   - Flagship: 5.1.4 (variance decomposition, 432-fold paradigm shift), 5.1.5 (latent profiles, K=3)
   - Integrated: 5.2.6, 5.3.7, 5.4.6, 5.5.6 (ICC table)
   - Key Message: Forgetting rate IS trait-like (ICC=21% model-averaged), but 4-timepoint design insufficient

5. **S5.5 Methodological Validation** (~1,500 words)
   - Flagship: 5.2.4 (IRT-CTT convergence, r>0.90)
   - Integrated: 5.2.5, 5.3.5-5.3.6, 5.4.4-5.4.5, 5.5.4-5.5.5 (convergence table)
   - Key Message: IRT critical for Ch7 external validity, CTT adequate for within-study

**Cross-Chapter Connections:**
- To Ch4: "We used 2-pass IRT purification (S4.2.2)"
- To Ch6: "Ch6 tests whether confidence TRACKS these forgetting trajectories"
- To Ch7: "Age-invariant VR (S5.3) contrasts with traditional tests (Ch7 will show robust age effects)"

**Includes:** Detailed flagship RQ structure (research question, hypothesis, analysis, results, figure), integrated RQ table templates, synthesis section example

---

**File 4: thesis/write6.md (CH6 METACOGNITION, 238 lines)**

**Purpose:** Convert 30 RQ reports --> cohesive Ch6 narrative (~11,000 words)

**Narrative Arc:** "Does confidence TRACK what happens to accuracy?"

**Why Ch6 Matters:**
- Ch5 established WHAT HAPPENS to accuracy
- Ch6 asks: Does confidence TRACK it? (metacognition question)
- Discovery: Convergence (parallel decline) AND dissociation (824x ICC ratio)

**4 Themes:**

1. **S6.1 Confidence Trajectories** (~3,000 words)
   - Flagship: 6.1.1 (general), 6.3.1 (domain, When steeper), 6.1.4 (824x ICC ratio)
   - Key Message: Theta-scale parallel, but ordinal confidence detects 54-221x more trait variance

2. **S6.2 Calibration & Metacognitive Accuracy** (~3,500 words)
   - Flagship: 6.2.1 (resolution), 6.2.2 (calibration curves), 6.2.3 (Brier decomposition)
   - Key Message: Persistent overconfidence, domain-specific calibration quality

3. **S6.3 High-Confidence Errors** (~2,500 words)
   - Flagship: 6.6.1 (HCE general, 15-20% stable), 6.7.1/6.7.4 (domain/paradigm), 6.6.2 (Dunning-Kruger NOT supported)
   - Key Message: HCE stable over time (monitoring failure, NOT false memory)

4. **S6.4 Confidence-Accuracy Dissociation** (~2,000 words)
   - Flagship: 6.1.4 (measurement comparison), 6.8.3 (spatial opposite correlations)
   - Key Message: Partial dissociation (metacognitive monitoring independent from memory architecture)

**Cross-Chapter Connections:**
- To Ch5: Domain confidence vs domain accuracy (When steeper for confidence, parallel for accuracy)
- To Ch5: HCE schema null (S6.3) replicates accuracy schema null (Ch5 S5.4.1)
- To Ch7: "What predicts BOTH memory (Ch5) and metacognition (Ch6)?"

---

**File 5: thesis/write7.md (CH7 INDIVIDUAL DIFFERENCES, 140 lines)**

**Purpose:** Placeholder for future work (0/20 RQs executed)

**Status:** NOT STARTED - User decides if needed for thesis submission

**When Ready:**
- Central question: "Do RAVLT/BVMT/RPM predict REMEMVR performance?"
- Key finding to emphasize: VR age-invariance (Ch5 S5.3) vs traditional-test age-sensitivity (Ch7) = VR scaffolding hypothesis validation
- Estimated time: 14-16h for Tier 1 (70-80% coverage), 20-25h for 100%

**Proposed Themes:**
- Theme 1: Predictive Validity (~3,000 words)
- Theme 2: Age as Moderator (~2,500 words)
- Theme 3: Self-Reported Factors (~2,000 words)
- Theme 4: Latent Profiles (~2,000 words, if executed)
- Theme 5: Reverse Inference (~1,500 words, if executed)

**Action:** Execute when user decides Ch7 priority

---

### 5. File Structure Reorganization

**OLD Structure (discovered in search):**
```
/home/etai/projects/REMEMVR/results/ch5/write.md  # WRONG LOCATION
/home/etai/projects/REMEMVR/reports/thesis/write.md  # WRONG LOCATION (user moved it)
```

**NEW Structure (created this session):**
```
/home/etai/projects/REMEMVR/thesis/
|-- introduction.md          # Ch1 (partial draft exists)
|-- methods.md               # Ch2 (partial draft exists)
|-- rationale.md             # Ch3 (partial draft exists)
|-- chapters_UPDATED.md      # RQ catalog (current state)
|-- conflicts_analysis.md    # Conflict resolution (NEW)
|-- write.md                 # General instructions (NEW v2.0, 422 lines)
|-- write4.md                # Ch4-specific (NEW, 268 lines)
|-- write5.md                # Ch5-specific (NEW, 315 lines)
|-- write6.md                # Ch6-specific (NEW, 238 lines)
+-- write7.md                # Ch7-specific placeholder (NEW, 140 lines)
```

**Reports stay in:**
```
/home/etai/projects/REMEMVR/reports/
|-- 5.1.1/report.md  # RQ-level documentation (NOT thesis)
|-- 5.1.2/report.md
...
+-- 6.8.4/report.md
```

**Separation Rationale:**
- ./thesis/ = THESIS FILES (chapters, instructions, structure docs)
- ./reports/ = RQ-LEVEL DOCUMENTATION (source material for thesis)
- Clear boundaries prevent confusion

---

### 6. Key Design Decisions

**1. Stateless Modular Architecture:**
- **write.md** = General principles (ALL chapters)
- **writeX.md** = Chapter-specific context (narrative arc, themes, flagship assignments)
- Agents read BOTH (general + specific) fresh each invocation
- No state persists between invocations

**2. "Engaging, Not Exhausting" Philosophy:**
- Dinner Party Test (explain to smart non-specialist?)
- Assessor engagement priority (they read 5-10 theses/year)
- Avoid: Data dumps, verbatim repetition, passive voice walls, jargon without explanation
- Use: Story arc, transitions, synthesis, variety, active voice, visual aids

**3. Flagship vs Integrated Strategy:**
- Flagship (6-8 per chapter): 600-900 words each, full analytical depth
- Integrated (rest): Summary table + narrative, eliminate redundancy
- Total word count: Ch5 ~14k, Ch6 ~11k (not 39k if all RQs 600 words)

**4. Cross-Referencing Discipline:**
- Within-chapter: S5.3
- Across-chapter: Ch5 S5.2 <--> Ch6 S6.1
- To methodology: S4.2.2
- To reports: reports/5.1.1/report.md (full details)

**5. Quality Gates:**
- Statistical reporting: 5-component format (beta, SE, p, CI, d) enforced
- Terminology standardization: "theta" not "IRT-calibrated ability"
- Figure numbering: Sequential, publication-quality captions
- g_conflict validation: Check contradictions before user review

---

### 7. Files Created/Modified

**NEW FILES (this session):**

1. `thesis/conflicts_analysis.md` (217 lines)
   - Purpose: Identify conflicts between write.md plan and existing thesis structure
   - Finding: NO MAJOR CONFLICTS, 3 minor resolvable, Ch4 strategy decision needed

2. `thesis/chapters_UPDATED.md` (815 lines)
   - Purpose: Update old chapters.md with current RQ execution status + major findings
   - Status: 65/85 RQs PLATINUM + documented, X.Y.Z numbering, ready for execution

3. `thesis/write.md` (422 lines, v2.0)
   - Purpose: General writing instructions (ALL chapters)
   - Philosophy: Engaging not exhausting, Dinner Party Test, quality checklist

4. `thesis/write4.md` (268 lines)
   - Purpose: Ch4 Analysis Methods instructions
   - Extraction strategy from RQ report Section 4, unresolved questions flagged

5. `thesis/write5.md` (315 lines)
   - Purpose: Ch5 Forgetting Trajectories instructions
   - 5 themes, flagship assignments, key messages, cross-chapter connections

6. `thesis/write6.md` (238 lines)
   - Purpose: Ch6 Metacognition instructions
   - 4 themes, convergence & dissociation narrative, cross-chapter comparisons

7. `thesis/write7.md` (140 lines)
   - Purpose: Ch7 Individual Differences placeholder
   - Future work, VR scaffolding hypothesis emphasis when ready

**MODIFIED FILES:** None (all new creations)

---

### 8. Next Steps & Recommendations

**IMMEDIATE (User Decision Required):**

1. **Ch4 Strategy Decision:**
   - Option A: Write Ch4 BEFORE Ch5-Ch6 (2-3 hours, extract from RQ report Section 4)
   - Option B: Write Ch5-Ch6 with PLACEHOLDERS (S4.X.X), fill Ch4 later
   - Impact: Ch5-Ch6 will have cross-refs like "S4.2.2 IRT purification"
   - **ASK USER:** Which approach?

2. **Resolve 3 Minor Conflicts:**
   - Update methods.md S2.3.7 (partial credit --> dichotomous only)
   - Optionally write S1.7 Thesis Aims (500 words, can do in parallel with Phase 1)
   - Replace chapters.md with chapters_UPDATED.md (or keep both)

**THEN EXECUTE write.md Plan (9-15 hours):**

**Phase 1: Master Preparation** (2-3 hours)
- Read 65 RQ report Section 9 summaries (./reports/*/report.md)
- Build mental map (what findings? what patterns?)
- Create 9 theme_specification.md files (group RQs into themes)
- Assign flagship vs integrated (6-8 flagship per chapter)
- Document key messages per theme

**Phase 2: Create rq_theme_writer Agent** (1-2 hours)
- Design: Like rq_report but for thesis prose synthesis
- Reads: write.md, writeX.md, theme_specification.md, RQ reports
- Writes: theme_X_content.md (2-5 pages, engaging narrative)
- Validates: Statistics against reports, flags anomalies
- Output: `.claude/agents/rq_theme_writer.md`

**Phase 3: Execute Theme Agents** (3-5 hours parallel, 9 agents x 1-2h each)
- Invoke rq_theme_writer for each of 9 themes (5 Ch5 + 4 Ch6)
- Review outputs (check for circuit breakers, verify quality)
- Collect theme_X_content.md files

**Phase 4: Master Integration** (2-3 hours)
- Copy theme outputs into chapter shells
- Write transitions between themes (100-150 words each)
- Write chapter intro (500 words) + summary (800-1000 words)
- Validate cross-references
- Assign figure numbers

**Phase 5: Cohesion & Polish** (2-3 hours)
- Invoke g_conflict (check contradictions)
- Eliminate redundancy (grep for repeated findings)
- Standardize terminology (theta, Days, Free Recall first mention)
- Validate statistical format (5-component check)
- Polish prose (flow, clarity, conciseness)

**Phase 6: User Review & Revision** (2-4 hours)
- User reads chapters (~90 pages total)
- User provides feedback
- Master revises
- Iterate until approved

**DELIVERABLES:**
- thesis/chapter_5_empirical.md (~14k words, THESIS-READY)
- thesis/chapter_6_empirical.md (~11k words, THESIS-READY)

---