# Analysis-Executor Code Generation Rules

**Topic:** Enhanced analysis_executor agent with 3 critical code generation rules
**Status:** Archived from state.md
**Related Files:** .claude/agents/analysis_executor.md

---

## Analysis-Executor Enhancement - Code Generation Rules (2025-11-15 01:40)

**Archived from:** state.md Session (2025-11-15 01:40)
**Original Date:** 2025-11-15
**Reason:** Enhancement complete, rules implemented, committed to git

### Context

After discovering multiple API mismatches in generated analysis_script.py, enhanced analysis_executor agent with mandatory code generation rules to prevent future issues.

**Root Problem:** Agent guessed function parameters based on config.yaml instead of reading tools_inventory.md

---

## Enhancement Details

**File Modified:** `.claude/agents/analysis_executor.md`
**Lines Added:** +64 lines
**Section Added:** "CRITICAL CODE GENERATION RULES"

---

## Rule 1: UTF-8 Encoding (MANDATORY)

**Requirement:** Always use encoding='utf-8' for ALL file operations

**Why Critical:** Windows cp1252 default breaks on special characters in config.yaml

**Example:**
```python
# ✅ CORRECT
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# ❌ WRONG - Will fail on special characters
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
```

**Applies To:**
- All file read operations
- All file write operations
- CSV, YAML, JSON, TXT files

---

## Rule 2: DataFrame Column Names (MANDATORY)

**Requirement:** Match function expectations EXACTLY, study tools_inventory.md FIRST

**Why Critical:** Prevents API mismatches like purify_items() TypeError

**Process:**
1. Read tools_inventory.md for EXACT function signatures
2. Match parameter names precisely (not guesses from config.yaml)
3. Verify DataFrame column requirements
4. Test imports before generating script

**Example:**
```python
# ✅ CORRECT - Matches tools_inventory.md
purify_items(
    df_items=df_items,
    a_threshold=0.4,
    b_threshold=3.0
)

# ❌ WRONG - Guessed from config.yaml
purify_items(
    df_item_params=df_item_params,
    difficulty_threshold=3.0,
    discrimination_threshold=0.4
)
```

**Common Mistakes to Avoid:**
- Guessing parameter names from config.yaml
- Using wrong variable names (df_theta_pass2 vs df_theta_scores)
- Adding parameters not in signature (num_comparisons)
- Wrong parameter names (effect_type vs include_interactions)

---

## Rule 3: Python Unbuffered Output (MANDATORY)

**Requirement:** Always run with -u flag for real-time logs

**Why Critical:** Enables monitoring of long-running processes (60+ min IRT calibrations)

**Example:**
```bash
# ✅ CORRECT - Unbuffered output for monitoring
poetry run python -u code/analysis_script.py

# ❌ WRONG - Buffered output (no real-time logs)
poetry run python code/analysis_script.py
```

**Benefits:**
- Real-time progress monitoring
- Early error detection
- Better debugging for long processes

---

## Implementation Impact

**Before Enhancement:**
- Agent guessed function signatures from config.yaml
- Generated 6 API mismatches in RQ 5.1 script
- TypeError at runtime after 60-minute calibration
- Manual fixes required

**After Enhancement:**
- Agent MUST read tools_inventory.md before code generation
- Mandatory UTF-8 encoding prevents Windows issues
- Unbuffered output enables monitoring
- Future API mismatches prevented

---

## Files Modified

1. `.claude/agents/analysis_executor.md` - Added 3 critical code generation rules (+64 lines)

**Git Commit:** ce7e1f2

---

## Testing Validation

**Next RQ Analysis:** Will test enhanced agent on RQ 5.1 resume script

**Expected Outcome:**
- ✅ Correct function signatures from tools_inventory.md
- ✅ UTF-8 encoding on all file operations
- ✅ Unbuffered output for monitoring
- ✅ Zero API mismatches

---

## Related Archives

**Problem:**
- `analysis_script_api_mismatch_fixes.md` - 6 mismatches that triggered this enhancement

**Solution:**
- This archive - Prevention rules implemented

**Testing:**
- `resume_script_creation.md` - Resume script with fixes applied

---

**End of Entry**
