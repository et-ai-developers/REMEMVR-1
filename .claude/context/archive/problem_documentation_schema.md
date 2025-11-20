# Problem Documentation Schema - Description/Cause/Effect Format

## Problem Documentation Schema Establishment (2025-11-15 17:00)

**Context:** Created standardized schema for documenting automation pipeline problems. Format used for all 24 problems in comprehensive problem list. Enforces clarity and conciseness.

**Archived from:** state.md Session (2025-11-15 17:00)
**Original Date:** 2025-11-15 17:00
**Reason:** Methodology archived, schema established and reusable for future problem documentation

---

## Schema Format

### Standard Template

```markdown
## Problem {n} - {2/3 word descriptor}
**Description:** One-sentence description of what the problem is
**Cause:** One-sentence explanation of what causes it
**Effect:** One-sentence description of consequences
```

### Field Requirements

**Problem Number:** Sequential numbering (1-24 in comprehensive list)

**Descriptor:** 2-3 word short name for quick reference
- Examples: "API Documentation Ignorance", "Cascading Failures", "Platform Assumptions"

**Description Field:** What IS the problem?
- Single sentence
- Objective statement of the issue
- No solutions, just facts

**Cause Field:** What CAUSES the problem?
- Single sentence
- Explains root cause, not symptoms
- Links to systemic issues when possible

**Effect Field:** What are the CONSEQUENCES?
- Single sentence
- Real-world impact (time wasted, errors produced, data loss)
- Quantify when possible

---

## Example Applications

### Example 1: API Documentation Ignorance

```markdown
## Problem 6 - API Documentation Ignorance
**Description:** Analysis-executor does not read tools_inventory.md before generating function calls.
**Cause:** Agent prioritizes config.yaml structure over actual tool function signatures documented in tools_inventory.md.
**Effect:** 6 distinct API mismatches discovered (purify_items, fit_lmm_with_tsvr, post_hoc_contrasts, compute_effect_sizes, variable naming, encoding).
```

**Why This Works:**
- Description: Objective fact about agent behavior
- Cause: Explains WHY (prioritization issue)
- Effect: Quantified impact (6 mismatches)

---

### Example 2: Cascading Failures

```markdown
## Problem 3 - Cascading Failures
**Description:** Single architectural error triggers 5+ downstream errors discovered sequentially.
**Cause:** No validation layer catches issues before runtime; errors only appear after previous error fixed.
**Effect:** 60+ minutes wasted debugging; script still not working after 6 fixes.
```

**Why This Works:**
- Description: Pattern observed (single → multiple)
- Cause: Absence of validation (systemic gap)
- Effect: Time quantified (60+ minutes)

---

### Example 3: Monolithic Design

```markdown
## Problem 20 - Monolithic Design
**Description:** Single-script, single-invocation design prevents resumability.
**Cause:** All 9 steps bundled into one script with no checkpointing between steps.
**Effect:** Bug in Step 5 requires re-running Steps 1-4 (60-minute IRT calibration wasted).
```

**Why This Works:**
- Description: Architectural constraint
- Cause: Design decision (no checkpointing)
- Effect: Concrete waste example (60 minutes)

---

## Schema Benefits

### 1. Enforces Clarity
- Single-sentence requirement prevents rambling
- Three fields force structured thinking
- No ambiguity about what/why/impact

### 2. Enables Pattern Recognition
- 24 problems documented with same format
- Collapse into 5 meta-patterns
- Similarities visible across problems

### 3. Facilitates Communication
- User and Claude share vocabulary
- Problem references by number (Problem #6 = API Ignorance)
- Compressed format for quick scanning

### 4. Prevents Solution Bias
- Schema documents problems, not solutions
- Solutions proposed separately
- Allows multiple solution approaches per problem

### 5. Reusable Methodology
- Can be applied to ANY problem domain
- Not specific to automation pipeline
- Generalizable to entire project

---

## Application to 24 Problems

**Used for ALL 24 problems in:** `docs/user/analysis_pipeline_problems.md`

### Categories Documented
1. API & Contract Issues (6 problems using schema)
2. Workflow & Process Issues (5 problems using schema)
3. Code Quality Issues (6 problems using schema)
4. Documentation & Tooling (3 problems using schema)
5. Meta-Patterns (5 patterns using schema)

**Result:** Comprehensive problem list, zero ambiguity, clear communication

---

## Integration with V4.X

### How V4.X Addresses Schema-Documented Problems

**Problem Schema** → **V4.X Solution**

- Problem 6 (API Ignorance) → g_code signature enforcement
- Problem 3 (Cascading Failures) → Multi-layer validation gates
- Problem 20 (Monolithic Design) → Atomic step agents
- Problem 16 (Platform Assumptions) → agent_best_practices.md platform rules
- Problem 12 (Wide vs Long Format) → rq_tools specifies exact formats

**Schema Enabled:** Clear problem-solution mapping for v4.X design

---

## Lessons Learned

1. **Schema Enforces Discipline** - Single-sentence requirement prevents verbosity
2. **Structure Reveals Patterns** - 24 problems collapse into 5 meta-patterns
3. **Separation of Concerns** - Problems documented independently of solutions
4. **Reusable Across Domains** - Methodology applicable beyond automation pipeline
5. **Communication Improvement** - Shared vocabulary enables precise discussion

---

## Future Use

**This schema can be reused for:**
- New problems discovered during v4.X implementation
- Problems in other parts of project (data prep, results inspection, plotting)
- Any systematic problem documentation task

**Template Location:** Referenced in this archive entry, can be extracted for future use

---

**Archive Entry Complete**
