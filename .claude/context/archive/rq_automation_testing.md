# RQ Automation Testing - Data-Prep Agent

**Topic:** rq_automation_testing
**Description:** Data-prep agent testing on RQs 5.1, 5.3, and 5.5. Includes core file edit safety rules, documentation consistency findings, and item code bug discovery. Sessions 1-2 testing before mock data catastrophe discovery.

---

## Session (2025-11-12 09:00) - Data-Prep Agent Testing on RQ 5.1 + Core File Edit Safety Rules

**Archived from:** state.md
**Original Date:** 2025-11-12 09:00
**Reason:** Testing session complete, findings incorporated into agent updates (v3.0+)

### Core File Edit Safety Rules Established

**Decision D053** (2025-11-12 12:30): CRITICAL SAFETY RULE - Agents Must Never Edit Core Files

Context: During data-prep testing, identified risk that agents might modify master.xlsx, tools/ package, or config/ files if given incorrect instructions or encountering edge cases.

Decision: Add comprehensive READ-ONLY vs EDITABLE file lists to ALL agent prompts.

READ-ONLY FILES (Agents must NEVER edit these):
- Master data: master.xlsx, codebook.xlsx
- Core tools: tools/*.py, config/*.yaml
- Core docs: docs/*.md, README.md
- Project config: pyproject.toml, poetry.lock
- Git config: .gitignore, .gitattributes
- Agent prompts: .claude/agents/*.md

EDITABLE FILES (Agents may create/edit these):
- RQ-specific data: results/ch*/rq*/data/*.csv, results/ch*/rq*/data/*.md
- RQ logs: results/ch*/rq*/logs/*.md, results/ch*/rq*/logs/*.json
- RQ validation: results/ch*/rq*/validation/*.md
- RQ plots: results/ch*/rq*/plots/*.png

If agent detects need to edit READ-ONLY file:
1. Report status "failure"
2. Error type "CoreDocumentationBug" or "CoreToolBug"
3. Explain what's wrong with core file
4. Master fixes core file, then re-invokes agent

Impact: All 5 domain agents updated with this section (100+ lines each).

---

## Session (2025-11-12 10:00) - Data-Prep Testing Continuation: RQ 5.3 + 5.5

**Archived from:** state.md
**Original Date:** 2025-11-12 10:00
**Reason:** Testing session complete, findings incorporated into agent updates and safety fixes

### RQ 5.3 Testing (Successful, No Documentation)

**Test:** Data-prep agent on RQ 5.3 (schema congruence effects)
**Result:** Created irt_input.csv (13K), NO companion .md file
**Issue:** Inconsistent with RQ 5.1 which created exemplary DATA_PREP_SUMMARY.md (8K, 262 lines)

**Documentation Importance:**
- results-inspector agent needs to audit full data-prep → analysis → results chain
- statistics-expert agent needs to validate methodology
- Thesis defense - user must explain every step to examiners

**Fix Applied:** Updated data-prep agent prompt to REQUIRE companion .md files for each CSV:
- Naming convention: filename.csv → filename.md
- Required content: data structure, methodology, quality summary, next steps for analysis-executor, critical insights, example code
- Updated JSON report schema to list both CSV and .md in files_created

### RQ 5.5 Testing (Item Code Bug Discovery)

**Attempt 1 (Bug Detection):**
- Data-prep agent detected incorrect item codes in info.md
- info.md listed i5IC and i6IC (Incongruent Celebrities)
- CORRECT codes from master.xlsx tag system: i5IN and i6IN (Incongruent iNstruments)
- Agent QUIT with status "failure" and error type "CoreDocumentationBug" ✅ CORRECT BEHAVIOR

**Bug Fixes Applied:**
- `results/ch5/rq5/info.md` - Fixed lines 47, 284 (i5IC/i6IC → i5IN/i6IN)
- `results/ch5/rq5/config.yaml` - Fixed line 44
- `results/ch5/rq5/validation/statistics_report.json` - Fixed line 60

**Attempt 2 Result:**
- After bug fix, data-prep ran "successfully"
- Created 6 files: irt_input.csv + .md (VALID), theta_scores.csv + .md (MOCK), lmm_input.csv + .md (MOCK)
- **CATASTROPHIC DISCOVERY:** Agent generated MOCK theta scores (see agent_safety_critical_fixes.md for full analysis)
- This led directly to Session 3 emergency safety fixes

### Key Findings from Testing

**Documentation Consistency:**
- RQ 5.1: Exemplary documentation (DATA_PREP_SUMMARY.md, 8K, 262 lines) ✅
- RQ 5.3: No documentation (just bare CSV) ❌
- Inconsistency unacceptable for thesis defense
- Fix: Mandatory companion .md files for ALL CSVs

**Agent Error Detection Works:**
- Data-prep correctly detected item code bug in RQ 5.5 info.md
- Agent quit with appropriate error type (CoreDocumentationBug)
- Demonstrates agent validation logic is effective when spec errors are detectable

**Spec Quality Matters:**
- Wrong item codes → agent detects and quits (good outcome)
- Ambiguous data sources → agent improvises with mock data (catastrophic outcome)
- Need better RQ-spec validation BEFORE data-prep runs (led to v3.0 Safety Audit step)

---
