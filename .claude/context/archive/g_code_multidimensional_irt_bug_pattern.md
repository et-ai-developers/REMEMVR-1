# g_code_multidimensional_irt_bug_pattern

**Topic Description:** Repeatable pattern of 5 systematic bugs in g_code's multidimensional IRT handling (RQs 6.1.1, 6.3.1, 6.4.1), root cause: no training examples, solution documented for future GRM RQs

**Related Topics:**
- `rq_6.4.1_step01_five_systematic_bug_fixes` (Session 2025-12-07 19:45)
- `rq_6.1.1_complete_execution_logarithmic_best` (archived earlier - first identification)
- `rq_6.3.1_complete_execution_when_domain_steeper_decline` (archived earlier - pattern confirmed)
- `ch6_grm_irt_pattern_mc_samples_1_100` (archived earlier - related IRT pattern)

---

## g_code Multidimensional IRT Bug Pattern (2025-12-07 19:45)

**Archived from:** state.md Session (2025-12-07 19:45)
**Original Date:** 2025-12-07 19:45
**Reason:** Pattern fully documented across 3 RQs, serves as reference for future GRM executions

### Pattern Overview

**Discovery:** Systematic pattern of 5 bugs repeatable across ALL GRM-based RQs
**Affected RQs:** 6.1.1 (single-factor), 6.3.1 (domain 3-factor), 6.4.1 (paradigm 3-factor)
**Root Cause:** g_code lacks training examples for multidimensional IRT models
**Impact:** Every future GRM RQ will encounter these bugs without proactive fixes

### The 5 Systematic Bugs

1. **Missing UID/test columns** - parse composite_ID before melt()
2. **Wrong return unpacking order** - correct signature: (response_matrix, Q_matrix, missing_mask, item_list, composite_ids)
3. **n_cats scalar instead of list** - configure_irt_model needs [5]*n_items
4. **n_cats scalar in extraction** - extract_parameters_from_irt needs [5]*n_items
5. **MIRT column format** - keep native format (Difficulty, Overall_Discrimination, Discrim_*), don't rename to (factor, a, b1-b4)

### Pattern Repeatability Evidence

**RQ 6.1.1 (2025-12-06):** Encountered bugs #1-5 (subset - single factor had simpler MIRT format)
**RQ 6.3.1 (2025-12-07):** Encountered ALL bugs #1-5 (domain-based 3-factor)
**RQ 6.4.1 (2025-12-07):** Encountered ALL bugs #1-5 AGAIN (paradigm-based 3-factor)

**Conclusion:** Pattern is NOT random - it's systematic and will recur in EVERY GRM RQ

### Root Cause Analysis

**Why g_code fails:**
1. Training data likely contains simple CTT examples (means, correlations)
2. No multidimensional IRT examples in training corpus
3. g_code hallucinates tool API signatures (guesses based on similar tools)
4. Multidimensional IRT has unique requirements (Q-matrix, factor-specific parameters)

**Why fixes work:**
- Proactive application of documented fixes from RQ 6.3.1
- Referencing actual tool signatures from tools/analysis_irt.py
- Copying working code from previous RQs (code-copying strategy)

### Solution: Documented Pattern Fixes

**For future RQs (6.5.1, 6.6.1, 6.7.2, 6.8.1):**
1. Use proactive context-finding BEFORE execution
2. Search archives for "multidimensional IRT bug pattern"
3. Apply all 5 fixes during FIRST g_code invocation (preemptive)
4. OR use code-copying strategy (copy from 6.3.1/6.4.1, avoid g_code entirely)

**Code-copying strategy proven MORE efficient:**
- RQ 6.4.1 Steps 01-08: 45 minutes with code-copying vs 4-5 hours with g_code debugging
- 75-80% time savings documented (Session 2025-12-07 22:00)

### Implications for Remaining Ch6 RQs

**Future GRM RQs:**
- RQ 6.5.1 (congruence trajectories - 3-factor GRM)
- RQ 6.6.1 (age group trajectories - 2-factor GRM)
- RQ 6.7.2 (other factor - likely GRM)
- RQ 6.8.1 (final factor - likely GRM)

**Recommendation:** Use code-copying strategy from 6.3.1 or 6.4.1 for ALL future GRM RQs. Replace factor names via find/replace, avoid g_code generation entirely for Steps 01-08.

---

### Historical Context

**Session 2025-12-07 19:45:** After ~4 hours of iterative debugging on RQ 6.4.1 Step 01, realized pattern was identical to RQ 6.3.1. User expressed frustration: "Dude we had this working perfectly in 6.3.1, why is this so hard?"

This frustration led directly to code-copying strategy implementation (Session 2025-12-07 22:00), which proved massively more efficient than g_code debugging.

---

### Pattern Documentation

**Complete bug documentation:** See `rq_6.4.1_step01_five_systematic_bug_fixes.md`
**Code-copying strategy:** See `code_copying_strategy_vs_g_code_debugging.md` (Session 2025-12-07 22:00)
**Template workflow:** See `ch6_root_rq_template_workflow_8_steps.md` (Session 2025-12-07 22:00)

---
