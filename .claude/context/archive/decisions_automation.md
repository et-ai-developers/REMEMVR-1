# Automation Decisions - Historical Context

**Topic:** Key automation architecture decisions (D037-D047, November 2025)
**Created:** 2025-11-11
**Maintained by:** context-manager agent (via Phase 10 migration)

**Note:** Refactor decisions (D001-D027) predate this system and are not archived here

---

## Automation Architecture Decisions (2025-11-07 to 2025-11-08)

**Source File:** `.context/decisions.md`

### D037: Agent-Based Automation Architecture (2025-11-07)

**Decision:** Agents WRITE CODE (not execute hardcoded pipelines)

**Architecture:**
- Analysis-Executor: Writes Python script, SAVES to `code/run_analysis.py`
- Results-Inspector: Validates correctness, returns quality scores
- Results-Finisher: Generates plots, interprets results, writes thesis text

**Key Principles:**
1. Agents write code, master runs as background task, agents review
2. Circuit breakers: Stop if tool missing/unexpected
3. Tool inventory: Agents know available tools via system prompt
4. Prompts are code: Refine prompts when agents fail
5. RQs are tests: Use real RQs for agent refinement

### D039: 2-Pass IRT as Standard Methodology (2025-11-07)

**Decision:** ALL 50 RQs use 2-pass IRT calibration with item purification

**Method:**
1. Pass 1: Calibrate all items, identify problematic ones
2. Purification: Flag items with |b| > 3.0 OR a < 0.4
3. Pass 2: Re-calibrate with purified item set

**RQ 5.1 Results:** 105 items → 46 retained (43.8%), When domain effect revealed: 26.5% slower forgetting (p=0.007)

**Rationale:** Standard psychometric practice, dramatically improves interpretability

### D040: Transparent Reporting of Measurement Limitations (2025-11-07)

**Decision:** When item purification reveals severe issues (e.g., <10 items retained), report as LIMITATION, not failure

**Frame as Contribution:**
- Identifies measurement challenges
- Provides guidance for future studies
- Demonstrates rigorous quality control

### D041: Probability Remapping for Supplementary Plots (2025-11-07)

**Decision:** Generate BOTH theta-scale and probability-scale plots

**Thesis Structure:**
- Main text: Theta-scale plots (statistical inference)
- Appendix: Probability-scale plots (descriptive, intuitive)

**Important:** Primary analysis ALWAYS uses theta (LMM on θ), probability is for interpretation only

### D042: Logarithmic Model as Primary Candidate (2025-11-07)

**Decision:** Test 5 candidate models (Linear, Quadratic, Logarithmic, Linear+Log, Quadratic+Log), expect logarithmic to dominate

**RQ 5.1:** Logarithmic best (AIC=2365.96, 68.1% weight)

### D043: RQ 5.1 as Comprehensive Template (2025-11-07)

**Decision:** RQ 5.1 workflow is OFFICIAL TEMPLATE for all 49 remaining RQs

**9-Stage Workflow:**
1. Data Preparation
2. IRT Pass 1 (~60 min)
3. Item Purification
4. IRT Pass 2 (~20-30 min)
5. Pass Comparison
6. LMM Analysis (5 models)
7. Primary Plots (theta-scale)
8. Supplementary Plots (probability-scale)
9. Results Documentation

### D044: Automation-Robust Tool Design (2025-11-08)

**Decision:** Tools should prevent agent errors, not rely on agents knowing implementation details

**Example:** `analysis_irt.py` returns item_name as regular column (not index)
- Agents can save with `index=False` without data loss
- Standard pandas practice
- Self-documenting
- Prevents entire class of errors

### D045: Analysis-Executor Strict Tool-Only Rules (2025-11-08)

**Decision:** Analysis-executor agent NEVER writes custom functions, ONLY uses tools from `tools/` package

**Agent Behavior:**
- ✅ Imports tools from `tools/` package
- ✅ Calls functions with appropriate parameters
- ❌ NEVER writes custom functions
- 🛑 STOPS if tool missing → reports to master → we add tool → re-run

**Rationale:** Custom functions bypass TDD, multiple scripts harder to manage

### D046: Embed Critical Knowledge in Agent Prompts (2025-11-08)

**Context:** Data-prep v2.0 used wrong tags, accepted 73% empty data as normal

**Decision:** Critical knowledge that would corrupt results if wrong must be EMBEDDED in system prompts, not just referenced

**Example:** Data-prep v3.0 has 150-line "CRITICAL: Master.xlsx Tag System Reference" section embedded

**Decision Framework:**
- ✅ Embed in prompt: Critical knowledge that would corrupt results
- 📚 External reference: Examples, supplementary context, edge cases

**Impact:** Prevented corruption of all 50 RQs in thesis

### D047: Context Management Protocol Non-Compliance (2025-11-08)

**Context:** Codebase audit revealed 19 issues, root cause = context management failures

**Decision:** Manual context management had 100% failure rate → Automated solution required

**Evidence:**
- No execution.log (no audit trail)
- No phase.json (no phase tracking)
- session.json stale (not updated)
- No checkpoints (no recovery points)
- No /clear between phases (token bloat: 162k/200k = 81%)

**Outcome:** Initiated Memory System Overhaul (2025-11-11) to implement automated context management

**Archived from:** `.context/decisions.md`
**Original Date:** 2025-11-07 to 2025-11-08
**Reason:** Historical automation architecture decisions

---

**End of decisions_automation_historical topic**
**Token Count:** ~2k tokens (key automation decisions D037-D047)
