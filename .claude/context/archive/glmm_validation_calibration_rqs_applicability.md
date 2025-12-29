# GLMM Validation - Calibration RQs Applicability Question

## Agent Blocker on GLMM Applicability (2025-12-29 ~18:00)

**Context:** During PLATINUM certification batch, rq_platinum agent processing RQ 6.3.3 (Domain × Time calibration random slopes ICC) reported blocker requiring user clarification on whether GLMM validation applies to calibration RQs with SEM-validated latent scores.

**Archived from:** state.md Session (2025-12-29 ~18:00)
**Original Date:** 2025-12-29 ~18:00
**Reason:** User decision needed, batch paused pending clarification

---

### Blocker Description

**RQ affected:** RQ 6.3.3 (Domain × Time calibration random slopes ICC)

**Agent message:** "BLOCKER: Need user clarification on GLMM applicability to calibration RQs"

**Question:** "Do calibration RQs with SEM-validated latent scores qualify for GLMM validation, or only accuracy/confidence RQs with raw IRT theta scores?"

---

### Background: GLMM Validation Purpose

**GLMM validation tests:** Whether random slopes are **trait-like** (ICC ≥ 0.30)

**Requirements:**
1. Longitudinal LMM with random slopes (time-varying predictor with individual trajectories)
2. Extract random slope variance from LMM
3. Compute ICC = σ²_slope / (σ²_slope + σ²_residual)
4. Threshold: ICC ≥ 0.30 = trait-like (consistent individual differences)

**Purpose:** Determine if individual differences in change rates are stable traits

**Typical use:** Accuracy/confidence trajectories over time (IRT theta scores)

---

### The Question

**RQ 6.3.2 context:**
- Has SEM-validated latent calibration scores (NOT raw IRT theta)
- Dependent variable: `latent_calibration` (SEM-corrected difference scores)
- Model: `latent_calibration ~ Domain × TSVR_centered + (TSVR_centered | Domain | UID)`
- Random slopes: TSVR_centered (time effect) varies by Domain and UID

**Unclear:** Does GLMM validation apply to latent calibration DV, or only raw theta?

---

### Option A: GLMM Applies to ALL LMMs with Random Slopes

**Rationale:**
- Random slopes are random slopes regardless of DV type
- If individual differences in trajectories exist, they could be trait-like
- Latent calibration is still a person-level construct (just error-corrected)

**Implication:**
- Run GLMM on RQ 6.3.2 latent_calibration scores
- Extract random slope variance for TSVR_centered effect
- Compute ICC to test trait-like hypothesis

**Consequence:**
- May need to create GLMM validation workflow for calibration RQs
- Extends GLMM methodology beyond accuracy/confidence to calibration
- Sets precedent for other calibration RQs with random slopes

**Pros:**
- Comprehensive validation (all random slopes tested)
- Theoretical consistency (individual differences could be traits)
- Parallel to accuracy/confidence GLMM validation

**Cons:**
- GLMM candidates list doesn't mention calibration RQs (may not be planned)
- Latent scores have different properties than raw theta (SEM-corrected)
- May add complexity without theoretical necessity

---

### Option B: GLMM ONLY Applies to Raw IRT Theta RQs

**Rationale:**
- GLMM candidates list specifically mentions accuracy/confidence RQs only
- Latent calibration is derived/composite (not raw measurement)
- SEM correction may alter individual difference structure
- Different measurement properties than raw theta scores

**Implication:**
- Skip GLMM for calibration RQs
- Mark RQ 6.3.3 (and similar) as N/A for GLMM validation
- PLATINUM certification proceeds without GLMM check

**Consequence:**
- Calibration RQs with random slopes don't get GLMM validation
- Simpler workflow (fewer analyses)
- Potential gap: don't know if calibration slopes are trait-like

**Pros:**
- Aligns with existing GLMM candidates list
- Avoids complexity of GLMM on derived scores
- Faster PLATINUM certification

**Cons:**
- Incomplete validation (random slopes not tested for trait-like property)
- Theoretical gap (don't know if individual calibration trajectories are stable)
- Inconsistent (why validate accuracy/confidence slopes but not calibration?)

---

### Option C: User Decides Case-by-Case

**Rationale:**
- Different RQs may have different requirements
- Theoretical necessity varies by research question
- Flexibility allows best decision per RQ

**Implication:**
- Ask user for each calibration RQ with random slopes
- User evaluates theoretical importance of trait-like test
- Some calibration RQs get GLMM, others don't

**Consequence:**
- More user interaction (less automation)
- Clearer guidance per RQ
- Avoids blanket policy that may not fit all cases

**Pros:**
- Flexibility (case-by-case decision)
- User control over validation depth
- Theoretical appropriateness per RQ

**Cons:**
- More user questions (interrupts batch execution)
- Less consistent (different RQs treated differently)
- Harder to document standard procedure

---

### Related Information

**GLMM candidates list location:** (needs verification via context-finder)
- Likely in docs/ or tools/glmm_validation/
- Should specify which RQ types require GLMM

**Precedent:**
- RQ 6.4.2 (Paradigm calibration) - was GLMM tested?
- RQ 6.5.2 (Schema calibration) - was GLMM tested?
- If NO precedent → suggests Option B (GLMM only for raw theta)
- If YES precedent → suggests Option A (GLMM for all LMMs)

**RQ 6.3.2 status:**
- Already PLATINUM certified (2025-12-11)
- SEM validated (2025-12-29 Session 06:00)
- Classification: PLATINUM-SUPER-ROBUST
- Uncertain: Was GLMM validation performed?

---

### Circuit Breaker #2 Application

**Trigger:** Agent blocker claim ("Need clarification on GLMM applicability")

**Mandatory response:**
1. STOP - Don't guess
2. Invoke context-finder to search:
   - GLMM candidates list (which RQs need GLMM?)
   - RQ 6.4.2 and 6.5.2 PLATINUM reports (was GLMM tested for calibration RQs?)
   - docs/glmm_methodology.md (if exists)
3. Verify: Is this a real blocker or agent misunderstanding?
4. Report findings to user

**Current status:** Paused, awaiting context-finder search results

---

### Recommended Next Steps

**1. Search for GLMM candidates list:**
- Find definitive list of which RQs require GLMM validation
- Check if calibration RQs are included

**2. Check precedent:**
- Read RQ 6.4.2 PLATINUM_REPORT.md (paradigm calibration)
- Read RQ 6.5.2 PLATINUM_REPORT.md (schema calibration)
- Did either undergo GLMM validation?

**3. Check RQ 6.3.2:**
- Read RQ 6.3.2 PLATINUM_REPORT.md
- Was GLMM validation performed?
- If YES → precedent for calibration GLMM (Option A likely)
- If NO → suggests calibration excluded from GLMM (Option B likely)

**4. Report findings + ask user:**
- Present evidence from steps 1-3
- Recommend option based on findings
- User makes final decision

---

### Potential Resolution

**IF precedent exists (6.4.2 or 6.5.2 had GLMM):**
→ Option A: Run GLMM on calibration RQs (consistent with precedent)

**IF no precedent (neither had GLMM):**
→ Option B: Skip GLMM for calibration RQs (consistent with existing practice)

**IF uncertain/conflicting evidence:**
→ Option C: Ask user case-by-case

---

### Files to Check (Context-Finder Search Needed)

1. **docs/glmm_methodology.md** (if exists) - GLMM validation criteria
2. **docs/glmm_candidates.md** or similar - List of RQs requiring GLMM
3. **results/ch6/6.4.2/PLATINUM_REPORT.md** - Check for GLMM section
4. **results/ch6/6.5.2/PLATINUM_REPORT.md** - Check for GLMM section
5. **results/ch6/6.3.2/PLATINUM_REPORT.md** - Check if GLMM performed
6. **tools/glmm_validation/** or similar - GLMM validation scripts/docs

---

**Last Updated:** 2025-12-29 ~18:00
**Status:** BLOCKER - Paused pending context-finder search + user decision
**Related Topics:** platinum_certification_batch_ch6_24_rqs_started, agent_blocker_verification_pattern_historical
**Decision Needed:** Which option (A, B, or C) should be followed?
**Next Action:** Context-finder search for precedent + GLMM candidates list
