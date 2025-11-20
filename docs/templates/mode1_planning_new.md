## MODE 1: PLANNING PHASE

**Trigger:** concept.md exists, plan.md missing

**Purpose:** Read user's concept, understand RQ intent, generate plan.md with questions

**Output:** plan.md (agent's interpretation + questions for user)

---

### Your Workflow:

**Step 0: Prerequisites Check**

1. **Verify concept.md exists:**
   - If missing → ERROR: "concept.md not found. User must create concept.md first using docs/templates/concept_template.md"
   - If exists → Continue

2. **Check for prior planning attempts:**
   - If `logs/rq_spec_context.md` exists → Read it (may be re-run after circuit breaker fix)
   - If missing → First planning attempt

---

**Step 1: Read User's Concept**

Read `results/chX/rqY/concept.md` - This is the user's description of the RQ in their own words.

**Extract:**
- Research question (user's phrasing)
- Memory domains mentioned (What/Where/When)
- Analysis approach (IRT? LMM? CTT?)
- Expected pattern (hypothesis)
- Special considerations
- User's own questions/uncertainties

**Document in internal notes:**
```markdown
## Planning Phase - Concept Analysis

**User's RQ (from concept.md):**
[Verbatim from concept.md]

**Domains Mentioned:**
- What: [Yes/No/Unclear]
- Where: [Yes/No/Unclear - which tags mentioned?]
- When: [Yes/No/Unclear]

**Analysis Type:** [IRT+LMM / CTT / etc.]

**User's Certainties:**
- [What user is clear about]

**User's Uncertainties:**
- [Questions user listed in concept.md]
```

---

**Step 2: Read Reference Documentation**

**MANDATORY READS (for cross-checking with concept.md):**

1. **docs/data_structure.md** - ALL 5 domain codes (see "Memory Domains" quick reference):
   - `-N-` = What
   - `-L-` = Where (static objects: furniture, fixtures, doors, windows)
   - `-U-` = Where (pick-up location for interactive items)
   - `-D-` = Where (put-down location for interactive items)
   - `-O-` = When

2. **docs/project_specific_stats_insights.md** - Mandatory requirements (2-pass IRT)

3. **docs/data_structure.md** - Tag patterns, UID format

4. **thesis/methods.md** - Study design (4 test sessions, VR paradigms, participant N)

5. **docs/tools_inventory.md** - Available tools (check if user's requested analysis is feasible)

6. **thesis/analyses/ANALYSES_CH5.md** (or CH6/CH7) - Original RQ specification

**CONDITIONAL READS:**
- **docs/irt_methodology.md** - If concept.md mentions IRT
- **docs/lmm_methodology.md** - If concept.md mentions LMM

---

**Step 3: Identify Questions to Ask User**

**Generate questions in these categories:**

### A. CRITICAL Questions (Must answer to proceed)

**Domain Tag Coverage:**
- If concept.md mentions "Where domain" but doesn't explicitly list -L-/-U-/-D-, ASK:
  "data_structure.md lists 3 Where tags: -L- (static objects), -U- (pick-up), -D- (put-down). Should I include all 3?"

**Paradigm Inclusion:**
- If concept.md says "VR items" without specifying paradigms, ASK:
  "Should I include all 6 paradigms (RFR, IFR, TCR, ICR, RRE, IRE) or subset?"

**Test Inclusion:**
- If concept.md doesn't specify which tests, ASK:
  "Include all 4 tests (T1, T2, T3, T4) or exclude T2 (same-day as T1)?"

**Mandatory Requirements:**
- If concept.md uses IRT but doesn't mention 2-pass purification, ASK:
  "project_specific_stats_insights.md requires 2-pass IRT. Should I include Pass 1 → Purification → Pass 2 workflow?"

### B. CLARIFICATION Questions (Help understand intent)

**Functional Form:**
- If concept.md mentions "trajectories" without specifying linear/quadratic/log, ASK:
  "Should I test multiple functional forms (linear, quadratic, log) and select via AIC?"

**Effect Sizes:**
- If concept.md mentions interaction but doesn't specify effect size metrics, ASK:
  "Which effect sizes: Cohen's f² for interaction + Cohen's d for pairwise comparisons?"

### C. OPTIONAL Questions (Can use defaults)

**Plotting:**
- If concept.md doesn't mention diagnostic plots, ASK:
  "Include IRT diagnostic plots (ICC, TCC) or just main result plot?"

**Validation Thresholds:**
- If concept.md doesn't specify CFI threshold, ASK:
  "Use CFI > 0.90 (relaxed, appropriate for dichotomous IRT) or CFI > 0.95 (traditional)?"

---

**Step 4: Create plan.md**

Use `docs/templates/plan_template.md` as base structure.

Write to: `results/chX/rqY/plan.md`

**Required sections:**
1. **My Understanding of Your Concept** - Agent's interpretation
2. **Domain Tag Mapping** - Table showing all 5 domain codes, which are mentioned in concept.md
3. **Tools Required** - List of tools from tools_inventory.md needed for this RQ
4. **Questions for You** - CRITICAL / CLARIFICATION / OPTIONAL categories
5. **Proposed File Structure** - What agent will create in Drafting mode
6. **Next Steps** - Instructions for user to answer questions
7. **YOUR ANSWERS** - Empty section for user to fill in

**Key principles:**
- Be transparent about interpretation (show agent's understanding)
- Be specific in questions (not vague "what do you want?")
- Provide options with context (Option A, B, C with explanations)
- Flag uncertainties explicitly (don't silently assume)

---

**Step 5: Create Initial Context Dump**

Write to: `results/chX/rqY/logs/rq_spec_context.md`

**Format:**
```markdown
# RQ X.Y Context Dump

**Agent:** rq_specification v3.0
**Created:** YYYY-MM-DD HH:MM

---

## Planning Phase

**Date:** YYYY-MM-DD HH:MM
**Invocation:** 1
**Status:** awaiting_user_input

### Folder Structure Scan

**Found:**
- ✅ concept.md exists
- ❌ plan.md missing (creating now)
- ❌ info.md missing (Drafting phase will create)
- ❌ validation reports missing

**Interpretation:** PLANNING MODE - Read concept.md, generate plan.md with questions

### Concept Analysis

**User's RQ:**
[Verbatim from concept.md]

**User's Analysis Approach:**
[Summarize what user described in concept.md]

**User's Uncertainties:**
[List questions user had in concept.md]

### Documents Read

1. ✅ concept.md - User's RQ description
2. ✅ data_structure.md - Verified all 5 domain codes
3. ✅ project_specific_stats_insights.md - Checked mandatory requirements
4. ✅ data_structure.md - Understood tag patterns
5. ✅ thesis/methods.md - Study design confirmed
6. ✅ tools_inventory.md - All required tools exist
7. ✅ ANALYSES_CH5.md - Cross-checked with source RQ

### Circuit Breaker Results

✅ Check 1 (concept.md vs data_structure.md): PASS - No domain tag conflicts
✅ Check 2 (concept.md vs ANALYSES_CHX.md): PASS - RQ descriptions aligned
✅ Check 3 (concept.md vs project_specific_stats_insights.md): PASS - Mandatory requirements acknowledged
✅ Check 4 (concept.md vs tools_inventory.md): PASS - All tools available
✅ Check 5 (concept.md vs thesis/methods.md): PASS - Study design compatible

### Questions Generated for User

**CRITICAL (3 questions):**
1. [Question about domain tag coverage]
2. [Question about paradigm inclusion]
3. [Question about mandatory 2-pass IRT]

**CLARIFICATION (2 questions):**
1. [Question about functional form]
2. [Question about effect sizes]

**OPTIONAL (2 questions):**
1. [Question about diagnostic plots]
2. [Question about validation thresholds]

### Files Created

- ✅ plan.md (results/chX/rqY/plan.md, ~150 lines)
- ✅ logs/rq_spec_context.md (this file, ~80 lines)

### Next Phase Trigger

**Waiting For:** User reviews plan.md, answers questions, tells master "ready for Drafting mode"

**Next Invocation:** DRAFTING MODE - Read plan.md with answers, generate info.md + config.yaml

---

**END OF PLANNING PHASE**
```

---

**Step 6: Report Back to Master**

Output concise summary:

```
PLANNING MODE COMPLETE for RQ X.Y

✅ concept.md read and analyzed
✅ Circuit breaker passed (no document conflicts)
✅ Questions generated for user (7 questions: 3 critical, 2 clarification, 2 optional)

Files Created:
- plan.md: results/chX/rqY/plan.md (~150 lines)
- Context dump: logs/rq_spec_context.md (~80 lines)

User Action Required:
1. Review plan.md (my interpretation of their concept)
2. Answer questions (especially CRITICAL questions)
3. Save plan.md with answers
4. Tell master: "Ready for rq-spec Drafting mode"

Estimated User Time: 10-15 minutes

Next Mode: DRAFTING (will read plan.md answers → generate info.md + config.yaml)
```

Terminate

---
