# proactive_context_finding_before_execution

**Topic Description:** Using context_finder agent BEFORE RQ execution to gather historical patterns, identify bug patterns from past RQs, apply fixes proactively, reduce debugging time by referencing known solutions

**Related Topics:**
- `rq_6.4.1_step00_complete_paradigm_extraction` (Session 2025-12-07 19:45)
- `g_code_multidimensional_irt_bug_pattern` (Session 2025-12-07 19:45)
- `context_system_overhaul_planning` (archived earlier - established proactive context-finding workflow)

---

## Proactive Context-Finding Strategy (2025-12-07 19:45)

**Archived from:** state.md Session (2025-12-07 19:45)
**Original Date:** 2025-12-07 19:45
**Reason:** Strategy validated and applied successfully, serves as reference for future RQ executions

### Strategy Overview

**Before starting RQ execution:**
1. Think: What questions do I have about this RQ?
2. Invoke context_finder agent to search archives/ and docs/
3. Review findings to identify relevant patterns and past decisions
4. Apply known fixes proactively during code generation
5. Ask user only truly unanswered questions

### RQ 6.4.1 Context-Finding Results

**Invocation:** Before Step 00 execution
**Query:** g_code bug patterns, 3-factor GRM execution, MIRT format handling

**Found 8 highly relevant archived topics:**
1. mc_samples=1/100 pattern (98% relevance) - prevents 7000+ epoch hang
2. Factor-specific probability conversion (95% relevance) - paradigm-specific discrimination/difficulty
3. RQ 6.1.1 complete execution (92% relevance) - 3 systematic fixes
4. Wide format paradigm parsing (88% relevance) - TC_{PARADIGM}-{DOMAIN}-{ITEM}
5. statsmodels cov_re DataFrame fix (85% relevance) - hasattr check
6. Coefficient extraction pattern (78% relevance) - slice fixed effects
7. mc_samples pattern discovery (90% relevance) - historical rationale
8. Ch6 mass parallelization (70% relevance) - RQ 6.4.1 infrastructure

**All topics current (v4.X), none obsolete**

### Key Insight from Context-Finding

**Pattern recognition:** RQ 6.1.1 (1-factor), RQ 6.3.1 (3-factor domain), RQ 6.4.1 (3-factor paradigm) all share **identical statistical structure** → same bug patterns will occur → proactively apply known fixes

**Impact:** Reduced debugging time by referencing existing solutions from archived topics instead of discovering bugs from scratch

### Efficiency Gains

**Time saved:** Uncertain exact hours, but context-finder search (<2 min) identified 8 relevant patterns that would have taken hours to rediscover through trial-and-error debugging

**Example application:**
- mc_samples=1/100 pattern: Prevented 7000+ epoch hang (would have wasted ~30 minutes)
- 5 systematic IRT bugs: Known from RQ 6.3.1, applied during debugging iterations
- Wide format parsing: TC_{PARADIGM}-{DOMAIN}-{ITEM} pattern already documented

### Validation of Proactive Workflow

**Evidence that strategy works:**
1. All 8 found topics were ACTUALLY relevant (98-70% relevance scores accurate)
2. Patterns from RQ 6.1.1 and 6.3.1 directly applied to RQ 6.4.1
3. No obsolete v3.0 content returned (context_finder correctly filtered by timestamps)
4. Reduced back-and-forth with user (already had answers from archives)

**Contrast with reactive approach:**
- Reactive: Encounter bug → debug → fix → repeat for each bug
- Proactive: Search archives → apply known fixes → encounter ONLY new bugs

### Integration with CLAUDE.md Principles

**From CLAUDE.md Section "Proactive Context-Finding Workflow":**
```
1. User: "Do XYZ"
2. I think: "What questions do I have?"
3. I invoke context-finder agent
4. I review findings: what answered? what unanswered?
5. I ask user ONLY unanswered questions
6. I proceed with full context
```

**RQ 6.4.1 execution followed this workflow:**
- User: "Execute RQ 6.4.1"
- I thought: What bugs will occur? What patterns exist?
- I invoked context-finder (found 8 topics)
- I reviewed: Bugs documented from 6.3.1, mc_samples pattern critical
- I asked user: (no remaining questions, all answered by archives)
- I proceeded with debugging (applied fixes referencing archived patterns)

### Recommendations for Future RQ Executions

**Always invoke context_finder BEFORE execution when:**
1. RQ has similar structure to past RQs (e.g., all Ch6 GRM RQs)
2. Complex statistical workflow (IRT, LMM, GLMM)
3. Previous RQs had systematic bugs
4. Methodology decisions may have been archived (e.g., dual-scale plots, TSVR pipeline)

**Search terms to use:**
- "RQ [similar number] complete execution"
- "g_code bug pattern"
- "[statistical method] systematic fixes"
- "code-copying strategy"

**Expected benefit:** 50-75% reduction in debugging time vs reactive approach

---

### Related Archived Topics Referenced

**From context-finder search:**
- `ch6_grm_irt_pattern_mc_samples_1_100` (CRITICAL: mc_samples=1 for fitting, 100 for scoring)
- `rq_6.1.1_complete_execution_logarithmic_best` (first Ch6 ROOT RQ, 3 systematic fixes)
- `ch6_dfdata_wide_format_paradigm_parsing` (TC_{PARADIGM}-{DOMAIN}-{ITEM} parsing)
- `ch6_lmm_statsmodels_cov_re_fix` (hasattr check for DataFrame vs ndarray)
- `multidimensional_irt_probability_conversion_bug_fix` (factor-specific parameters for plots)
- `statsmodels_coefficient_extraction_pattern` (slice fixed effects only)
- `irt_mc_samples_pattern_discovery` (historical rationale for 1/100 pattern)
- `ch6_mass_parallelization_186_agents` (RQ 6.4.1 infrastructure complete)

---
