# Circuit Breakers - Hallucination Prevention (Mandatory Protocols)

## Hallucination Discovery and Circuit Breaker Implementation (2025-12-29 ~18:00)

**Context:** During PLATINUM certification batch execution for Ch6 RQs, discovered critical hallucination where I accepted agent claim that "item-level calibration data doesn't exist" for RQ 6.3.2, but user corrected that accuracy and confidence ARE measured concurrently. This triggered comprehensive assumption verification revealing 5 systematic errors.

**Archived from:** state.md Session (2025-12-29 ~18:00)
**Original Date:** 2025-12-29 ~18:00
**Reason:** Hallucination prevention protocols now integrated into CLAUDE.md Core Operating Principles #0

---

### Hallucination Discovery Event

**Initial Error:** Accepted agent claim that "item-level calibration data doesn't exist" for RQ 6.3.2

**User Correction:** "Accuracy and confidence WERE measured concurrently. Does this conflict with your understanding?"

**Circuit Breaker #3 Activated:** User correction signal → STOP → List ALL assumptions → Verify systematically

**Assumption Verification Results:**

**❌ WRONG ASSUMPTIONS (5 discovered):**

1. **Item count:** 72 items/test → **ACTUAL: ~115 items/test** (6 paradigms × ~18-20 items each)
   - Source: data_structure.md correctly lists all 6 paradigms
   - Error: Only counted 3 paradigms somehow

2. **Paradigm count:** 3 paradigms (IFR, ICR, IRE) → **ACTUAL: 6 paradigms** (IFR, ICR, IRE, BIFR, BICR, BIRE)
   - Source: data_structure.md line 187-222 lists all 6
   - Error: Forgot bounded paradigms exist

3. **Confidence scale:** 0-100 continuous → **ACTUAL: 0/25/50/75/100 discrete** (5-point scale)
   - Source: data_structure.md line 246-255
   - Error: Assumed continuous when it's Likert-like ordinal

4. **Concurrent measurement:** Accuracy and confidence measured separately → **ACTUAL: Concurrent** (same trial, same item)
   - Source: data_structure.md line 246-248 "Each recall trial is rated 0/25/50/75/100"
   - Error: Agent blocker claim accepted without verification

5. **Item-level calibration data:** Doesn't exist → **ACTUAL: Exists** (accuracy + confidence measured per item per trial)
   - Source: Master.xlsx has tags like `2--IFR--1-C` (confidence) and `2--IFR--1` (accuracy) for same item
   - Error: Agent blocker claim accepted without verification

**✅ CORRECT ASSUMPTIONS (3 verified):**

1. **Tests:** 4 test sessions (0, 1, 3, 6 days post-encoding) ✅
2. **Participants:** N=100 ✅
3. **VR encoding:** Single encoding session with multiple item types ✅

**Root Cause:** Accepted agent blocker claims without verification (Circuit Breaker #2 violated)

---

### Circuit Breakers Added to CLAUDE.md

**Added 4 mandatory hallucination prevention protocols to Core Operating Principles #0 (highest priority):**

#### Circuit Breaker #1: Fundamental Assumptions Check

- **TRIGGER:** Before ANY factual claims about study design, data structure, analysis capabilities, file locations
- **MANDATORY:** STOP → invoke context-finder → READ primary source → VERIFY → THEN state with citation
- **Example:** Don't say "study has 72 items" → Search docs/ → Find data_structure.md → Cite "115 items per test (6 paradigms)"
- **Purpose:** Prevent stating incorrect "facts" that user must correct

#### Circuit Breaker #2: Agent Blocker Verification

- **TRIGGER:** When agent reports "data doesn't exist" or "analysis not possible"
- **MANDATORY:** STOP → invoke context-finder → search for solutions/precedents → VERIFY blocker is real
- **Example:** Agent says "no item-level calibration" → Search → Find concurrent measurement exists → Correct the misunderstanding
- **Purpose:** Prevent accepting false limitations that block valid work

#### Circuit Breaker #3: User Correction Signal

- **TRIGGER:** User says "What?", "Does this conflict?", "That's wrong", "Actually..."
- **MANDATORY:** HALLUCINATION RECOVERY PROTOCOL → List ALL assumptions → Invoke context-finder systematically → Compare findings → Report corrections
- **Example:** User says "Accuracy and confidence WERE measured concurrently" → List 8 assumptions → Verify each → Report 5 errors found
- **Purpose:** Prevent compounding errors, waste time on wrong assumptions

#### Circuit Breaker #4: Secondary Source Alert

- **TRIGGER:** Relying on agent outputs, state.md summaries, memory/inference (not primary docs)
- **MANDATORY:** IF making factual claims → Identify primary vs secondary source → Use context-finder for primary → Verify → Cite primary
- **Example:** Don't cite "state.md says RQ 6.3.2 can't run GLMM" → Check actual RQ files and glmm_candidates.md → Report real situation
- **Purpose:** Prevent propagating errors from summaries/agent interpretations

---

### Hallucination Recovery Workflow

**WHEN:** Circuit breaker triggers (especially #3 - user correction)

**STEPS:**
1. **STOP** - Acknowledge error, no defensiveness
2. **LIST** - Enumerate ALL related assumptions explicitly
3. **VERIFY** - Invoke context-finder with specific verification questions
4. **COMPARE** - Findings vs assumptions (what's right/wrong/missing?)
5. **REPORT** - Transparent correction with explanation
6. **PROCEED** - Use corrected information

**Template for context-finder during recovery:**
```
Search archives/ and docs/ to verify these assumptions:

1. [Assumption 1 to verify with evidence needed]
2. [Assumption 2 to verify with evidence needed]
3. [What might I be missing about X?]

Return evidence with file paths, timestamps, and corrections to any errors.
```

---

### Integration with CLAUDE.md

**Location:** Core Operating Principles #0 (before TDD, before User Understanding)

**Total additions:** ~500 lines to Core Operating Principles section

**Impact:**
- ALL future tasks will trigger circuit breakers before making factual claims
- Systematic assumption verification prevents hallucinations
- User corrections trigger comprehensive fixes
- Agent blocker claims require verification before acceptance

---

### Files Modified

**CLAUDE.md:**
- Added Circuit Breaker #1: Fundamental Assumptions Check
- Added Circuit Breaker #2: Agent Blocker Verification
- Added Circuit Breaker #3: User Correction Signal
- Added Circuit Breaker #4: Secondary Source Alert
- Updated Core Operating Principles to make circuit breakers #0 (highest priority)
- Added Hallucination Recovery Workflow template

---

### Lesson Learned

**Hallucination Pattern:**
- Agent reports blocker → I accept at face value → User corrects → Discover systematic errors

**Prevention:**
- NEVER accept agent blocker claims without verification
- ALWAYS invoke context-finder to search for solutions/precedents
- ALWAYS verify fundamental assumptions against primary sources (data_structure.md, Master.xlsx)
- User corrections are CRITICAL SIGNALS for systematic review

**Recovery:**
- Acknowledge error immediately
- List ALL assumptions explicitly
- Verify each systematically
- Report transparently
- Implement safeguards to prevent recurrence

---

**Last Updated:** 2025-12-29 ~18:00
**Status:** Circuit breakers now MANDATORY for all future work
**Related Topics:** agent_blocker_verification_pattern_historical, study_design_verification_assumptions_corrected
