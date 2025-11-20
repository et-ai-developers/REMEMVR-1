# Analysis Pipeline Problems - Comprehensive List

## Complete Problem Documentation Process (2025-11-15 17:00)

**Context:** User requested comprehensive documentation of ALL automation pipeline problems encountered during RQ 5.1 execution. Used context-finder agent to search archives and current state for systematic patterns. Created comprehensive 24-problem list with meta-patterns.

**Archived from:** state.md Session (2025-11-15 17:00)
**Original Date:** 2025-11-15 17:00
**Reason:** v3.0 problems documented, v4.X architecture created to solve them, this is historical record

---

## Context-Finder Analysis Results

**Searched:** archives/ and docs/ for automation problems
**Discovered:** 7 archived topics documenting past API issues
**Root Cause Identified:** analysis-executor guesses from config.yaml instead of reading tools_inventory.md
**Cascading Pattern Confirmed:** 1 root error → 5+ downstream failures

---

## Comprehensive Problem List Created

**Reformatted:** User's 5 original problems into Description/Cause/Effect schema
**Added:** 19 additional problems discovered through context-finder + current session
**Total:** 24 distinct problems organized into 5 meta-patterns
**File Created:** `docs/user/analysis_pipeline_problems.md` (comprehensive reference, 146 lines)

---

## Problem Categories Identified

### API & Contract Issues (6 problems)
- API ignorance
- Config assumptions
- Case sensitivity
- Format mismatch
- Missing columns
- Wide vs long

### Workflow & Process Issues (5 problems)
- Cascading errors
- Git workflow
- Incomplete commits
- No testing
- No validation

### Code Quality Issues (6 problems)
- Index vs column
- Signature guessing
- Encoding
- Unbuffered output
- No error recovery
- Hardcoding

### Documentation & Tooling (3 problems)
- Documentation bloat
- No format auto-detection

### Meta-Patterns (5 patterns)
- Documentation-reality gap
- Cascading failures
- Platform assumptions
- Monolithic design
- Quality vs scope tradeoff

---

## Problem Documentation Schema

**Format used for all 24 problems:**
```markdown
## Problem {n} - {2/3 word descriptor}
**Description:** One-sentence description of what the problem is
**Cause:** One-sentence explanation of what causes it
**Effect:** One-sentence description of consequences
```

**Example:**
```markdown
## Problem 6 - API Documentation Ignorance
**Description:** Analysis-executor does not read tools_inventory.md before generating function calls.
**Cause:** Agent prioritizes config.yaml structure over actual tool function signatures documented in tools_inventory.md.
**Effect:** 6 distinct API mismatches discovered (purify_items, fit_lmm_with_tsvr, post_hoc_contrasts, compute_effect_sizes, variable naming, encoding).
```

---

## Meta-Patterns Observed

### Pattern 1 - Documentation-Reality Gap
- Agent reads documentation (tools_inventory.md, config schema) inadequately or not at all
- Generates code based on assumptions about how tools "should" work
- Result: Function signatures don't match actual implementations

### Pattern 2 - Cascading Failures
- Single architectural mismatch (e.g., wide vs long format) triggers 5+ downstream errors
- Each error discovered only after fixing previous error
- No validation catches issues before runtime

### Pattern 3 - Platform Assumptions
- Agent generates code for generic UNIX/UTF-8 environment
- Breaks on Windows-specific constraints (cp1252 encoding, path separators)
- No platform-aware code generation

### Pattern 4 - Monolithic Design
- Single-script, single-invocation design prevents resumability
- No checkpointing or partial execution
- Bug requires full restart (60+ minutes wasted)

### Pattern 5 - Quality vs Scope Tradeoff
- Larger agent tasks (8-step RQ spec, 9-step analysis execution) correlate with lower quality outputs
- Higher error rates as task complexity increases
- Agent exhaustion/truncation on huge workloads

---

## Lessons Learned

1. **Documentation is Critical** - Context-finder reveals systematic patterns across archived sessions
2. **Problem List Must Be Comprehensive** - Found 19 additional problems beyond user's initial 5
3. **Schema Enforces Clarity** - Description/Cause/Effect format keeps explanations focused and single-sentence
4. **Patterns Emerge from Data** - 24 discrete problems collapse into 5 meta-patterns
5. **Cascading Errors Are Predictable** - Wide vs long format mismatch was discoverable through static analysis
6. **Defensive Programming Works** - Auto-detection (test vs Test, tsvr vs TSVR_hours) prevents fragility

---

## V4.X Architecture Response

**User's Solution:** Complete redesign from 7 monolithic agents to 13 atomic agents
**Key Insight:** "Agents don't follow documentation because context windows are BLOATED"
**Result:** v4.X specification created to solve all 24 problems systematically
**Status:** This problem list is v3.0 historical record, v4.X prevents these issues via atomic design

---

**Archive Entry Complete**
