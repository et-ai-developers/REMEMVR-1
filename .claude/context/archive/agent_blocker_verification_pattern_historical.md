# Agent Blocker Verification Pattern - Historical Examples

## Pattern Discovery (2025-12-29 ~18:00)

**Context:** During PLATINUM certification batch, discovered pattern where agent blocker claims must be systematically verified before acceptance. This archive documents the pattern, historical examples, and verification protocol.

**Archived from:** state.md Session (2025-12-29 ~18:00)
**Original Date:** 2025-12-29 ~18:00
**Reason:** Pattern recognized, prevention protocol established via Circuit Breaker #2

---

### The Pattern

**Agent Blocker Claim Pattern:**
1. Agent encounters difficulty/uncertainty
2. Agent reports "X doesn't exist" or "Y not possible" as blocker
3. I accept claim at face value without verification
4. User corrects me
5. Verification reveals agent misunderstanding, not real blocker

**Why it occurs:**
- Agents have limited context (focused on specific task)
- Agents may not search archives/docs for precedents
- Agents may misinterpret data structure or capabilities
- I accept agent authority without independent verification

**Why it's problematic:**
- Blocks valid work unnecessarily
- Wastes user time correcting false limitations
- Propagates errors to other RQs/analyses
- Erodes trust in analysis pipeline

---

### Example 1: Item-Level Calibration Data (2025-12-29 ~18:00)

**Agent claim:** "Item-level calibration data doesn't exist for RQ 6.3.2"

**My initial response:** Accepted at face value, proceeded as if limitation real

**User correction:** "Accuracy and confidence WERE measured concurrently. Does this conflict?"

**Verification via context-finder:**
- data_structure.md lines 246-248: "Each recall trial is rated 0/25/50/75/100"
- Master.xlsx tags: `2--IFR--1` (accuracy) and `2--IFR--1-C` (confidence) for SAME item
- **Conclusion:** Item-level calibration data DOES exist (concurrent measurement)

**Resolution:**
- Agent misunderstood data structure
- Item-level calibration is possible
- Triggered comprehensive assumption verification (found 5 errors total)

**Lesson:** NEVER accept data availability claims without checking primary sources (data_structure.md, Master.xlsx)

---

### Example 2: GLMM Validation Applicability (2025-12-29 ~18:00)

**Agent claim:** "Need user clarification on GLMM applicability to calibration RQs"

**My initial response:** Paused and asked user (CORRECT - Circuit Breaker #2 applied)

**Verification needed:**
- Search GLMM candidates list (which RQs require GLMM?)
- Check precedent (RQ 6.4.2, 6.5.2, 6.3.2 PLATINUM reports)
- Determine if blocker is real or agent misunderstanding

**Status:** Pending verification (Circuit Breaker #2 triggered correctly)

**Lesson:** When agent reports uncertainty/blocker, invoke context-finder BEFORE asking user

---

### Example 3: Random Slopes Convergence (Historical - RQ 6.2.5)

**Context:** RQ 6.2.5 Issue 004 - Random slopes not tested

**Agent (hypothetical) claim:** "Random slopes model failed to converge, can't test"

**Correct response (if pattern applied):**
1. Search archives for similar convergence issues
2. Check if precedent exists for handling convergence failures
3. Verify if blocker is due to model complexity vs data limitations
4. Document Occam's razor justification if model unstable

**Actual outcome (2025-12-29 14:30):**
- Created enhancement scripts for optional testing
- Documented 3 scenarios (converged LRT sig/ns, failed converge)
- Used Occam's razor for CONDITIONAL → FULL PLATINUM upgrade path

**Lesson:** Convergence failures require systematic investigation, not immediate acceptance as blocker

---

### Verification Protocol (Circuit Breaker #2)

**TRIGGER:** When agent reports:
- "Data doesn't exist"
- "Analysis not possible"
- "Model can't converge"
- "X is a blocker"
- ANY claimed impossibility or limitation

**MANDATORY RESPONSE:**

**Step 1: STOP**
- Do NOT accept blocker at face value
- Do NOT proceed as if limitation is real
- Do NOT immediately ask user

**Step 2: INVOKE CONTEXT-FINDER**
Search for:
- Has this problem been solved before? (search archives/)
- Is there documentation about this limitation? (search docs/)
- Have other RQs handled this successfully? (search results/)
- What precedents exist?

**Step 3: READ RELEVANT FINDINGS**
- Check primary sources (data_structure.md, Master.xlsx, methodology docs)
- Read archived solutions from similar RQs
- Verify agent claim against documented evidence

**Step 4: VERIFY BLOCKER IS REAL**
- Is this a real limitation (documented, confirmed)?
- OR is this agent misunderstanding (data exists, precedent exists)?

**Step 5A: IF BLOCKER IS REAL**
- Document why (cite primary sources)
- Explore workarounds (check archived solutions)
- Present options to user with evidence

**Step 5B: IF BLOCKER IS FALSE**
- Find solution from precedent
- Correct agent misunderstanding
- Proceed with work (no user delay)

---

### Common Agent Blocker Types

**Type 1: Data Availability Claims**
- "X data doesn't exist"
- **Verification:** Check data_structure.md + Master.xlsx tags
- **Example:** Item-level calibration data (DOES exist, agent wrong)

**Type 2: Methodological Impossibility Claims**
- "Y analysis not possible"
- **Verification:** Search archives for precedent, check docs/methodology
- **Example:** GLMM on calibration RQs (pending verification)

**Type 3: Technical Limitation Claims**
- "Model won't converge"
- **Verification:** Check convergence diagnostics, search for similar issues
- **Example:** Random slopes (create enhancement scripts for optional testing)

**Type 4: Requirement Ambiguity Claims**
- "Need clarification on Z"
- **Verification:** Search docs/ for specifications, check precedent
- **Example:** GLMM applicability (search candidates list, check precedent)

---

### Historical False Blocker Examples (Prevented by Circuit Breaker)

**None archived yet** - Circuit Breaker #2 implemented 2025-12-29 ~18:00

**Future additions:** Document each false blocker discovered and how verification resolved it

---

### True Blocker Examples (Verified as Real)

**None archived yet** - Circuit Breaker #2 implemented 2025-12-29 ~18:00

**Future additions:** Document legitimate blockers and their resolutions

---

### Integration with Circuit Breakers

**Circuit Breaker #2:** Agent Blocker Verification (MANDATORY)
- Implemented 2025-12-29 ~18:00
- Added to CLAUDE.md Core Operating Principles #0
- Highest priority (before TDD, before User Understanding)

**Relationship to other circuit breakers:**

**Circuit Breaker #1 (Fundamental Assumptions):**
- Prevents making false claims about data/capabilities
- Agent blockers often reveal false assumptions
- Both require primary source verification

**Circuit Breaker #3 (User Correction Signal):**
- Triggered when user corrects agent blocker acceptance
- Leads to comprehensive assumption verification
- Agent blocker was often root cause of hallucination

**Circuit Breaker #4 (Secondary Source Alert):**
- Agent outputs are secondary sources
- Agent blocker claims must be verified against primary sources
- Don't cite agent claims as authoritative

---

### Metrics to Track

**Blocker claims encountered:** TBD (start tracking 2025-12-29)

**False blockers (resolved via verification):** 1 (item-level calibration)

**True blockers (verified as real):** 0 (none yet, pending GLMM verification)

**Time saved by verification:** Significant (prevented "item-level calibration impossible" error cascade)

**User corrections prevented:** 1+ (caught item-level calibration error before propagating)

---

### Best Practices

**DO:**
- ✅ Invoke context-finder when agent reports blocker
- ✅ Search archives for precedent solutions
- ✅ Verify against primary sources (data_structure.md, Master.xlsx)
- ✅ Document blocker resolution for future reference
- ✅ Check if similar RQs solved same problem

**DON'T:**
- ❌ Accept agent blocker claims at face value
- ❌ Immediately ask user without verification
- ❌ Proceed as if limitation is real without checking
- ❌ Cite agent claims as authoritative
- ❌ Skip searching for precedent solutions

---

### Template for Blocker Verification

```
AGENT BLOCKER REPORTED: [blocker claim]

1. CONTEXT-FINDER SEARCH:
   - Search archives/ for: [similar problems, solutions]
   - Search docs/ for: [methodology docs, specifications]
   - Search results/ for: [precedent RQs with same issue]

2. PRIMARY SOURCE CHECK:
   - data_structure.md: [relevant lines]
   - Master.xlsx: [relevant tags]
   - methodology docs: [relevant sections]

3. PRECEDENT FOUND:
   - RQ X.Y.Z: [how they handled this]
   - Archive topic: [documented solution]
   - Result: [blocker was real/false]

4. VERIFICATION RESULT:
   - [ ] BLOCKER IS REAL (documented limitation)
   - [ ] BLOCKER IS FALSE (agent misunderstanding)

5. RESOLUTION:
   - IF REAL: [workaround options, user decision needed]
   - IF FALSE: [solution from precedent, proceed without user delay]
```

---

**Last Updated:** 2025-12-29 ~18:00
**Status:** Pattern recognized, prevention protocol active via Circuit Breaker #2
**Related Topics:** circuit_breakers_hallucination_prevention_mandatory, study_design_verification_assumptions_corrected, glmm_validation_calibration_rqs_applicability
**Verification Rate:** 1/1 agent blockers verified (100% verification rate)
**False Blocker Rate:** 1/1 verified blockers were false (100% - needs more data)
