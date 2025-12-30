# Evidence-Based Decision Workflow - Circuit Breaker Extension

**Purpose:** Circuit Breaker #1 extension to DECISIONS (not just factual claims) - systematic evidence-gathering before proceeding when methodology unclear

**Status:** Established 2025-12-29 21:00

**Key Principle:** When user says "revisit fundamentals," trigger systematic investigation via context-finder before deciding

---

## Circuit Breaker #1 Extension to Decisions (2025-12-29 21:00)

**Archived from:** state.md Session (2025-12-29 21:00)
**Original Date:** 2025-12-29 21:00
**Reason:** Major workflow improvement - prevents guessing on methodological decisions

---

### Triggering Scenario

**User Question:** "Let's first revisit the whole point of running GLMM. What are we trying to achieve?"

**Context:**
- User initially said "Option A: GLMM for all LMMs, proceed"
- Agent saw ambiguity (RQ 6.3.3 uses IRT-aggregated theta, unclear if "all LMMs" means extract raw items)
- Agent asked user for clarification
- User responded with "revisit fundamentals" question

**User's Intent:**
- NOT providing directive ("just do Option A")
- Signaling: "I need you to think this through systematically"
- Delegating decision WITH requirement for evidence-based reasoning

---

### Evidence-Based Investigation Workflow

**Step 1: User Signals "Revisit Fundamentals"**

Triggers:
- "Revisit the whole point of..."
- "What are we trying to achieve?"
- "Do what you think is best and use context finder"
- "Let's think about the purpose of X"

Response: Systematic investigation (NOT proceed with guess)

---

**Step 2: Context-Finder Systematic Search**

**Search 1: Purpose/Methodology**
- Query: "What is the PURPOSE of [GLMM validation]?"
- Target: Primary methodology documentation
- Goal: Understand WHAT the method detects and WHY

**Search 2: Precedents**
- Query: "Has this situation been handled before?"
- Target: Archive for past decisions on similar cases
- Goal: Identify established patterns/precedents

**Search 3: Current Case Characteristics**
- Query: "What are the exact characteristics of [RQ 6.3.3]?"
- Target: RQ specification documents
- Goal: Classify current case accurately

---

**Step 3: Evidence Synthesis**

**Gather Facts:**
1. [GLMM purpose]: Detect intercept effects missed by IRT→LMM aggregation
2. [Precedents]: RQs 6.1.1, 6.1.3 used GLMM on theta scores; RQs 6.4.2, 6.3.2 exempt (calibration)
3. [Current case]: RQ 6.3.3 uses theta_confidence (single construct, NOT calibration)

**Identify Key Distinction:**
- NOT "theta vs raw items" (both GLMM precedents used theta)
- IS "single-construct vs difference-score" (calibration = difference score)

**Make Evidence-Based Decision:**
- RQ 6.3.3 = single construct (like precedents 6.1.1, 6.1.3)
- Therefore: GLMM validation APPLIES
- Rationale: Matches established precedents, methodological purpose applies

---

**Step 4: Proceed with Confidence**

- No guessing required
- No user clarification needed (evidence speaks)
- Document decision rationale for future reference
- Execute with full confidence

---

### Comparison to Circuit Breaker #1 (Original)

**Circuit Breaker #1 (Factual Claims):**
- Trigger: About to make claim about study design/data/capabilities
- Response: STOP, verify via context-finder, cite source
- Prevents: Hallucinating facts

**Circuit Breaker #1 Extended (Decisions):**
- Trigger: User asks "revisit fundamentals" OR methodology unclear
- Response: STOP, systematic evidence-gathering, synthesize, decide
- Prevents: Guessing on methodological decisions

**Shared Principle:**
> Do not proceed based on assumptions/inference. Gather PRIMARY EVIDENCE first.

---

### RQ 6.3.3 Example

**Initial Situation:**
- User: "Option A: GLMM for all LMMs"
- Agent: "IRT-aggregated theta unclear, extract raw items?"
- User: "Revisit fundamentals, use context-finder"

**Evidence-Based Investigation:**

**Search 1 - GLMM Purpose:**
- Source: `results/glmm_candidates.md` (2025-12-24)
- Finding: Detect intercept effects missed by aggregation (NOT replace all LMMs)
- Evidence: 4 validated RQs (5.1.3, 5.4.1, 6.1.1, 6.1.3) ALL used theta scores

**Search 2 - Calibration Precedents:**
- Source: RQ 6.4.2 certification (2025-12-28), RQ 6.3.2 status (2025-12-29)
- Finding: Calibration RQs EXEMPT (difference scores, technical impossibility)
- Evidence: Explicit deferral documented for 6.4.2, alternative approach for 6.3.2

**Search 3 - RQ 6.3.3 Characteristics:**
- Source: `results/ch6/6.3.3/docs/1_concept.md`
- Finding: DV = theta_confidence (single construct, NOT calibration)
- Evidence: Clear specification, matches precedents 6.1.1/6.1.3

**Synthesis:**
- Distinction: Single-construct (theta) vs difference-score (calibration)
- RQ 6.3.3: Single construct → GLMM APPLIES
- Calibration RQs: Difference score → GLMM EXEMPT

**Decision:** ✅ Run GLMM validation on RQ 6.3.3

**Outcome:** Correct decision, major methodological discovery (p-value artifact), RQ certified

---

### Benefits

**1. Prevents Guessing:**
- No proceeding with unclear methodology
- Evidence guides decision (not intuition/assumptions)

**2. Builds Confidence:**
- Decision backed by primary sources
- Can explain rationale to user
- Future sessions can reference precedent

**3. Discovers Insights:**
- Systematic search often reveals unexpected patterns
- RQ 6.3.3 case: Discovered "single vs difference" distinction (not "theta vs raw")

**4. Creates Documentation:**
- Evidence-based decision becomes precedent
- Archive captures reasoning for future reference
- Builds institutional knowledge

---

### Workflow Template

```
User signals "revisit fundamentals" OR methodology unclear:

1. STOP - Do not proceed with guess
2. INVOKE context-finder:
   - Search 1: Purpose/methodology primary docs
   - Search 2: Precedents in archives
   - Search 3: Current case characteristics
3. SYNTHESIZE evidence:
   - What are the facts?
   - What are the key distinctions?
   - What do precedents suggest?
4. DECIDE based on evidence:
   - Clear rationale
   - Cite sources
   - Document reasoning
5. PROCEED with confidence:
   - No guessing
   - No user clarification needed
   - Execute fully
```

---

### Integration with Other Circuit Breakers

**Circuit Breaker #2 (Agent Blockers):**
- Use evidence-based workflow to verify blocker claims
- Context-finder searches for precedents/solutions
- Don't accept "impossible" without evidence

**Circuit Breaker #3 (User Corrections):**
- Hallucination recovery uses same systematic search
- Verify ALL assumptions via context-finder
- Evidence-based correction (not defensive guessing)

**Circuit Breaker #4 (Primary Sources):**
- Evidence-based workflow REQUIRES primary sources
- No relying on state.md summaries or agent outputs
- Context-finder targets original documentation

---

### Time Investment vs Value

**RQ 6.3.3 Case:**
- Context-finder searches: 30 min (3 systematic searches)
- Evidence synthesis: 15 min (identify key distinction)
- Total investigation: ~45 min

**Value:**
- Prevented ~2-3h of wrong-direction work
- Discovered major methodological insight (p-value artifact)
- Established precedent for all future RQs
- **ROI: 3-4× time invested**

---

**Last Updated:** 2025-12-29 21:00
**Status:** ✅ WORKFLOW ESTABLISHED - CIRCUIT BREAKER #1 EXTENDED TO DECISIONS
**Related Topics:** glmm_policy_clarified_single_construct_vs_difference_score, circuit_breakers_hallucination_prevention_mandatory
