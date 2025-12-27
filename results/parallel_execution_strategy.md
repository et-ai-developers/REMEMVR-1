# Parallel Execution Strategy - Option B (PUBLICATION-READY)

**Document Purpose:** Maximize parallelization for 66 RQs → PLATINUM status
**Goal:** 6-8 weeks calendar time (vs 19-35 weeks sequential)
**Date Created:** 2025-12-27
**Based On:** ch5-6-finalization-steps.md + context-finder analysis of parallel execution precedents

---

## EXECUTIVE SUMMARY

### Parallelization Potential

**Proven at Scale:**
- 186 parallel agent invocations (31 Ch6 RQs) in ~45 minutes ✅
- 18 RQs processed in 12 minutes (12× speedup) ✅
- ROOT RQs fully parallelizable after dependency resolution ✅

**Our Situation:**
- **Total RQs:** 66 (35 Ch5 + 31 Ch6)
- **Sequential estimate:** 154-278 hours (19-35 working days)
- **With parallelization:** **6-8 weeks calendar time** (10-15 working days actual effort)

**Strategy:** Tiered execution with **maximum parallel batches** within each tier

---

## DEPENDENCY ANALYSIS

### Critical Upstream Dependencies (MUST BE SEQUENTIAL)

**Blocker Chain:**
```
5.4.1 (Schema GLMM) → 6.5.1, 6.5.2, 6.5.3 (schema series)
5.1.3 (Age GLMM) → 6.1.3 (parallel finding)
6.1.1 (Alt IRT) → 6.1.2, 6.1.3, 6.1.4, 6.1.5 (theta dependency)
6.4.2 (Diff score) → 6.3.2 (same methodology)
```

**Impact:** 4 upstream blockers affect 10 downstream RQs

### Independent Tracks (CAN BE PARALLELIZED)

**Ch5 Age Effects:** 5.2.3, 5.3.4, 5.4.3, 5.5.3 (4 RQs) - **Fully parallel**
**Ch6 Age Effects:** 6.2.5, 6.3.3, 6.4.3 (3 RQs) - **Fully parallel**
**Ch5 Domains:** 5.2.2-5.2.8 (7 RQs) - **Parallel after 5.2.1**
**Ch5 Paradigms:** 5.3.2-5.3.9 (8 RQs) - **Parallel after 5.3.1**
**Ch5 Source-Dest:** 5.5.2-5.5.5 (4 RQs) - **Fully parallel**
**Ch6 Calibration:** 6.2.x series (6 RQs) - **Parallel after diff score check**

**Total parallelizable:** ~50 RQs (76% of all RQs)

---

## THREE-PHASE PARALLEL STRATEGY

### PHASE 1: BLOCKERS (Week 1) - Mixed Parallel

**Goal:** Resolve all upstream dependencies + integrate critical findings

#### Day 1-2: Critical GLMM Integration (SEQUENTIAL - dependencies exist)

**Sequential Block 1 (Schema):**
```
[5.4.1 GLMM integration] (5-6.5h)
  ↓
[Search thesis "quadruple null"] (2-3h)
  ↓
[Update archive entries] (30 min)
```
**Total:** 8-10 hours

**Can run PARALLEL while Schema integrating:**
- 5.1.3 Age GLMM integration (4h) - **No dependency on 5.4.1**
- 5.2.2 Re-run steps + power (4-5h) - **No dependency on 5.4.1**

**Day 1-2 Outcome:** 3 blockers complete in parallel

#### Day 3: Calibration Reliability (PARALLEL)

**Parallel Block 2:**
```
[6.4.2 Diff score + Lord's Paradox] (1.5-2h) || [6.3.2 Diff score + time contrasts] (1-1.5h)
```
**Total:** Max 2 hours (parallel execution)

**PHASE 1 TOTAL:** 10-12 hours actual work, **2-3 days calendar** (vs 5 days sequential)

---

### PHASE 2: HIGH PRIORITY (Week 2) - Massive Parallel

**Goal:** Complete TIER 2 + early TIER 3 RQs with GLMM validation

#### Day 4: Confidence Series Start (SEQUENTIAL - theta dependency)

**Sequential Block 3:**
```
[6.1.1 Response patterns + alt IRT] (5-6h)
  ↓ (if theta changes)
[Re-fit 6.1.2, 6.1.3, 6.1.4, 6.1.5] (8-16h contingency)
```

**Best case:** 6.1.1 alt IRT yields similar theta → No refit needed
**Worst case:** Refit 4 RQs → Budget 1-2 extra days

#### Day 5-7: MASSIVE PARALLEL BATCH (15+ RQs simultaneously)

**After 6.1.1 complete, launch in parallel:**

**TIER 2 Remaining:**
- 6.1.3: Power + TOST + diagnostics (3-4h)
- 6.5.3: Power + 5.4.1 cross-check (12h) - **5.4.1 now complete**
- 5.5.2: Power + TOST + breakpoints (5-8h)
- 5.1.1: Documentation polish (1-1.5h)

**TIER 3 HIGH-GLMM (8 RQs):**
- 6.3.2: GLMM T1 baseline (10 min)
- 6.4.2: GLMM paradigm (10 min)
- 6.5.1: GLMM schema→confidence (10 min)
- 6.5.2: GLMM schema→calibration (10 min)
- 5.2.3: GLMM age×domain (10 min)
- 5.3.4: GLMM age×paradigm (10 min)
- 5.4.3: GLMM age×schema (10 min)
- 5.5.3: GLMM age×source-dest (10 min)

**Total RQs in parallel:** 4 TIER 2 + 8 GLMM = **12 RQs**

**Execution approach:**
```python
# Launch all 12 RQs with task-specific scripts
# Each RQ runs independently
# Max time = longest RQ (6.5.3 at 12h)
# Sequential estimate: 35+ hours
# Parallel execution: 12 hours (3× speedup)
```

**PHASE 2 TOTAL:** 18-22 hours actual work, **3-4 days calendar** (vs 10+ days sequential)

---

### PHASE 3: SYSTEMATIC PROCESSING (Weeks 3-6) - Batch Parallelization

**Goal:** Process remaining 46 RQs in systematic batches

#### Strategy: Type-Based Batching

**Batch 1 (Ch5 Domain Series - 6 RQs):**
```
Parallel: 5.2.4, 5.2.5, 5.2.6, 5.2.7, 5.2.8, 5.3.2
Each: Power analysis + GLMM if intercepts + diagnostics (2-3h)
Total: 3 hours (parallel) vs 18 hours (sequential) = 6× speedup
```

**Batch 2 (Ch5 Paradigm Series - 6 RQs):**
```
Parallel: 5.3.3, 5.3.5, 5.3.6, 5.3.7, 5.3.8, 5.3.9
Each: Power analysis + GLMM if intercepts + diagnostics (2-3h)
Total: 3 hours (parallel)
```

**Batch 3 (Ch5 Schema Series - 4 RQs):**
```
Parallel: 5.4.2, 5.4.4, 5.4.5, 5.4.6
Each: Power + cross-check with 5.4.1 baseline finding (2-3h)
Total: 3 hours (parallel)
```

**Batch 4 (Ch5 Source-Dest Series - 2 RQs):**
```
Parallel: 5.5.4, 5.5.5
Each: Power + TOST + breakpoint sensitivity (2-3h)
Total: 3 hours (parallel)
```

**Batch 5 (Ch5 Trajectory/Model Selection - 5 RQs):**
```
Parallel: 5.1.2, 5.1.4, 5.1.5, 5.1.6, 5.2.1
Each: Model completeness check + MA if needed + diagnostics (3-4h)
Total: 4 hours (parallel)
```

**Batch 6 (Ch6 Calibration Series - 6 RQs):**
```
Parallel: 6.2.1, 6.2.2, 6.2.3, 6.2.4, 6.2.6, 6.3.1
Each: Diff score reliability + response patterns + diagnostics (2-3h)
Total: 3 hours (parallel)
```

**Batch 7 (Ch6 Domain/Paradigm - 6 RQs):**
```
Parallel: 6.3.4, 6.3.5, 6.4.1, 6.4.4, 6.4.5, 6.4.6
Each: Calibration checks + power analysis + diagnostics (2-3h)
Total: 3 hours (parallel)
```

**Batch 8 (Ch6 Remaining - 5 RQs):**
```
Parallel: 6.6.1, 6.7.1, 6.8.1, 6.9.1, 6.10.1
Each: Context-specific analyses + diagnostics (2-4h)
Total: 4 hours (parallel)
```

**Batch 9 (Ch5 Trajectory Completion - 6 RQs):**
```
Parallel: 5.6.1, 5.6.2, 5.6.3, 5.6.4, 5.6.5, 5.6.6
Each: Model selection + MA + diagnostics (3-4h)
Total: 4 hours (parallel)
```

#### PHASE 3 Execution Calendar

**Week 3 (Days 11-15):**
- Day 11: Batch 1 (Domain series) - 3h
- Day 12: Batch 2 (Paradigm series) - 3h
- Day 13: Batch 3 (Schema series) - 3h
- Day 14: Batch 4+5 (Source-Dest + Trajectory) - 7h
- Day 15: Batch 6 (Calibration) - 3h

**Week 4 (Days 16-20):**
- Day 16: Batch 7 (Domain/Paradigm Ch6) - 3h
- Day 17: Batch 8 (Ch6 remaining) - 4h
- Day 18: Batch 9 (Trajectory completion) - 4h
- Day 19-20: Buffer for any re-runs (10h contingency)

**PHASE 3 TOTAL:** 30-40 hours actual work, **10 days calendar** (vs 30+ days sequential)

---

## IMPLEMENTATION MECHANICS

### How to Execute Parallel Batches

#### Option 1: Manual Parallel Scripting (FASTEST)

**For each RQ in batch, create standalone script:**
```bash
# Example: Batch 1 (6 RQs)
# Create 6 scripts that can run simultaneously

# scripts/batch1_rq5.2.4.py
# scripts/batch1_rq5.2.5.py
# scripts/batch1_rq5.2.6.py
# scripts/batch1_rq5.2.7.py
# scripts/batch1_rq5.2.8.py
# scripts/batch1_rq5.3.2.py

# Execute in parallel terminals or via GNU parallel:
ls scripts/batch1_*.py | parallel -j 6 poetry run python {}
```

**Advantages:**
- True parallelization (6 RQs complete in max-time, not sum-time)
- No inter-RQ blocking
- Easy to monitor (6 terminal windows)

**Disadvantages:**
- Requires scripting setup (30-60 min per batch)
- Need 6+ CPU cores for optimal performance

---

#### Option 2: Sequential with Rapid Cycling (SAFER)

**For each RQ in batch, process in rapid sequence:**
```bash
# Process RQs 5.2.4 → 5.2.5 → 5.2.6 → 5.2.7 → 5.2.8 → 5.3.2
# No waiting between RQs, just chaining

# Total time: 6 RQs × 2.5h = 15h (sequential)
# vs Option 1: 2.5h (parallel)
```

**Advantages:**
- Simpler to implement (no parallel infrastructure)
- Easier to debug (one at a time)
- Still faster than casual sequential (no breaks, systematic)

**Disadvantages:**
- 5-6× slower than true parallelization
- No CPU core utilization

---

#### Option 3: Agent-Based Parallelization (HYBRID)

**Use proven rq_* agent workflow from context-finder:**

```bash
# For each batch, launch parallel agents:

# Phase 1: Generate power analysis specs
rq_planner → writes plan.md with power analysis requirements (31 RQs || parallel)

# Phase 2: Generate tool scripts
rq_tools → writes scripts for power/TOST/diagnostics (31 RQs || parallel)

# Phase 3: Execute analyses
g_code → runs scripts and validates (can parallelize if independent)

# Phase 4: Validate results
rq_inspect → checks outputs against plan.md (31 RQs || parallel)
```

**Proven results from context-finder:**
- rq_planner: 31 RQs in ~3 minutes
- rq_tools: 31 RQs in ~4 minutes
- g_code: Not parallelizable (actual computation), but can batch
- rq_inspect: 31 RQs in ~5 minutes

**Advantages:**
- Proven at scale (186 parallel invocations successful)
- Automated validation (rq_inspect catches errors)
- TDD safety (rq_tools blocks on missing tools)

**Disadvantages:**
- Agent overhead (planning/tooling phases don't save time if analyses are short)
- Best for RQs needing NEW code (not just running existing scripts)

---

### RECOMMENDATION: Mixed Strategy

**TIER 1-2 (10 RQs):** Option 2 (Sequential rapid cycling)
- Reason: Critical blockers, need careful validation, complex integration
- Time: 45-55 hours actual → 2-3 weeks calendar (with integration work)

**TIER 3 Batches (46 RQs):** Option 1 (Manual parallel scripting)
- Reason: Systematic tasks (power/diagnostics), highly parallelizable, proven safe
- Time: 30-40 hours actual → 10 days calendar (batches of 5-6 RQs)

**Alternative for TIER 3:** Option 3 (Agent-based) if new tools needed
- Example: If power analysis tool doesn't exist → use rq_tools to generate it
- Then apply to all RQs needing power analysis

---

## CALENDAR TIMELINE (Option B with Parallelization)

### Conservative Estimate (8 Weeks)

**Week 1:** TIER 1 blockers (10-12h work, 5 days calendar with integration)
**Week 2:** TIER 2 high-priority (18-22h work, 5 days calendar with contingency)
**Week 3:** TIER 3 Batches 1-3 (9h work, 5 days calendar with validation)
**Week 4:** TIER 3 Batches 4-6 (10h work, 5 days calendar with validation)
**Week 5:** TIER 3 Batches 7-9 (11h work, 5 days calendar with validation)
**Week 6:** Final validation, diagnostics, re-runs (15h work, 5 days calendar)
**Week 7-8:** Thesis integration, cross-validation, PLATINUM certification (20h work, 10 days calendar)

**Total:** 8 weeks calendar, **95-105 hours actual work** (vs 154-278 sequential)

---

### Aggressive Estimate (6 Weeks)

**Week 1:** TIER 1 blockers (10-12h work, 3 days calendar, rapid cycling)
**Week 2:** TIER 2 high-priority (18-22h work, 4 days calendar, rapid cycling)
**Week 3-4:** TIER 3 all batches (30h work, 10 days calendar, true parallelization)
**Week 5:** Final validation, re-runs (10h work, 5 days calendar)
**Week 6:** Thesis integration, PLATINUM certification (15h work, 5 days calendar)

**Total:** 6 weeks calendar, **85-95 hours actual work**

---

## CRITICAL SUCCESS FACTORS

### 1. Dependency Mapping (MANDATORY)

**Before any parallel batch:**
- Verify no cross-RQ dependencies
- Check if any RQ uses outputs from another in the batch
- Confirm all upstream blockers complete

**Example violation:**
```
Batch: [5.1.2, 5.1.3, 5.1.4] ← WRONG
Reason: 5.1.2-5.1.4 may depend on 5.1.1 theta
Solution: Complete 5.1.1 first, THEN parallelize 5.1.2-5.1.4
```

---

### 2. Tool Pre-Development

**Before TIER 3 batches:**
- Ensure all tools exist (power analysis, TOST, diagnostics)
- Create template scripts for common tasks
- Test on 1-2 RQs before batching

**If tools missing:**
- Use rq_tools agent to generate them (TDD workflow)
- Batch tool development (e.g., all 4 power analysis variants together)

---

### 3. Quality Gates (NO SKIPPING)

**After each phase:**
- ✅ All RQs in phase pass validation checklist
- ✅ No convergence failures
- ✅ All plots regenerated
- ✅ summaries updated

**If ANY RQ fails gate:** STOP, fix before next phase

---

### 4. Contingency Buffering

**Build in 20% time buffer:**
- TIER 1: Budget 12-14h (vs 10-12h estimate)
- TIER 2: Budget 25-30h (vs 18-22h estimate)
- TIER 3: Budget 36-48h (vs 30-40h estimate)

**Reason:** Unexpected issues (alternative IRT theta changes, diff score < 0.70, etc.)

---

## RISK MITIGATION (Updated for Parallelization)

### Risk 1: Parallel Batch Has Cross-Dependencies (MISSED)

**Scenario:** Launch 6 RQs in parallel, discover RQ4 needs output from RQ2

**Impact:** RQ4 fails, must re-run after RQ2 completes (wasted time)

**Mitigation:**
- Explicit dependency check before EACH batch
- Conservative approach: If uncertain, run sequential
- Use rq_specification docs to verify independence

---

### Risk 2: Tool Failures Block Entire Batch

**Scenario:** Power analysis script has bug, affects all 6 RQs in batch

**Impact:** Entire batch fails, must debug and re-run

**Mitigation:**
- Test tools on 1 RQ before batching
- Use TDD validation (rq_inspect catches failures)
- Keep batch size moderate (6 RQs max, not 20)

---

### Risk 3: Parallel Execution Exhausts Resources

**Scenario:** 6 Python processes running LMM on 28,800 observations each = RAM overload

**Impact:** System crashes, all 6 RQs fail

**Mitigation:**
- Monitor system resources (RAM, CPU)
- Reduce batch size if needed (3 RQs instead of 6)
- Use sequential for memory-intensive tasks (GLMM with 28k obs)

---

## WORK SESSION STRUCTURE

### Daily Workflow (Example: Week 3 Day 11 - Batch 1)

**Morning (2 hours):**
1. Review Batch 1 RQs (5.2.4-5.2.8, 5.3.2)
2. Verify dependencies (all independent ✅)
3. Create 6 power analysis scripts (or use template)
4. Test on RQ 5.2.4 (validate script works)

**Afternoon (3 hours):**
5. Launch 6 scripts in parallel (or sequential if safer)
6. Monitor execution (check for errors)
7. Validate outputs (power computed, diagnostics run)

**Evening (1 hour):**
8. Update summaries for all 6 RQs
9. Regenerate plots with annotations
10. Check off batch in tracking sheet

**Total:** 6 hours calendar for 6 RQs (vs 18 hours sequential = 3× speedup)

---

## FINAL RECOMMENDATION

**For Option B (PUBLICATION-READY):**

### Phase 1 (Week 1): BLOCKERS - Careful Sequential
- 5 RQs, complex integration, upstream dependencies
- **Strategy:** Sequential with rapid cycling (Option 2)
- **Time:** 10-12h work, 5 days calendar

### Phase 2 (Week 2): HIGH PRIORITY - Mixed Parallel
- 5 TIER 2 + 8 GLMM validations = 13 RQs
- **Strategy:** Launch 12 RQs in parallel after 6.1.1 complete (Option 1)
- **Time:** 18-22h work, 5 days calendar

### Phase 3 (Weeks 3-6): SYSTEMATIC - Batch Parallelization
- 46 RQs in 9 batches of 5-6 RQs
- **Strategy:** Manual parallel scripting (Option 1) OR agent-based if tools needed (Option 3)
- **Time:** 30-40h work, 20 days calendar

### Phase 4 (Weeks 7-8): INTEGRATION - Sequential
- Thesis updates, cross-validation, PLATINUM certification
- **Strategy:** Sequential (no parallelization possible)
- **Time:** 20h work, 10 days calendar

---

**TOTAL ESTIMATE:**
- **Calendar time:** 8 weeks (conservative) to 6 weeks (aggressive)
- **Actual work:** 80-95 hours (vs 154-278 sequential)
- **Speedup:** 1.6-3.5× faster with parallelization

---

**Next Steps:**

1. User reviews this parallel strategy
2. User confirms comfort level with parallel execution (Option 1 vs 2 vs 3)
3. Begin TIER 1 Day 1: Launch 5.4.1, 5.1.3, 5.2.2 in parallel where possible
4. Validate Phase 1 complete before Phase 2
5. Scale up parallelization in Phase 3

---

**Document Prepared By:** Claude Code
**Date:** 2025-12-27
**Version:** 1.0 - Parallel Execution Strategy for Option B
**Based On:**
- ch5-6-finalization-steps.md (roadmap)
- context-finder analysis (186 parallel agents precedent)
- Proven tiered execution patterns from Ch5/Ch6 mass parallelization

**Status:** READY FOR USER REVIEW
