# RQ Status Tracker

**RQ:** X.Y - [RQ Title]
**Last Updated:** YYYY-MM-DD HH:MM
**Current Phase:** [specification / validation / data_prep / analysis / results_validation / complete]

---

## Status Table

| Phase | Status | Score | Date | Notes |
|-------|--------|-------|------|-------|
| **1. Specification (Draft)** | ✅ Complete / 🔄 In Progress / ⏸️ Pending | - | YYYY-MM-DD | rq_specification agent (draft phase) |
| **2. Scholar Validation** | ✅ Approved / ⚠️ Conditional / ❌ Rejected / ⏸️ Pending | X.X/10 | YYYY-MM-DD | Theoretical grounding validated |
| **3. Statistics Validation** | ✅ Approved / ⚠️ Conditional / ❌ Rejected / ⏸️ Pending | X.X/10 | YYYY-MM-DD | Methodology validated |
| **4. Specification (Finalization)** | ✅ Complete / 🔄 In Progress / ⏸️ Pending | - | YYYY-MM-DD | Feedback incorporated |
| **5. Safety Audit** | ✅ Passed / ❌ Blocked / ⏸️ Pending | - | YYYY-MM-DD | Master validates info.md Section 4 |
| **6. Data Preparation** | ✅ Success / ❌ Failed / 🔄 In Progress / ⏸️ Pending | - | YYYY-MM-DD | data_prep agent |
| **7. Output Verification** | ✅ Clean / ⚠️ Warnings / ❌ Contaminated / ⏸️ Pending | - | YYYY-MM-DD | Master forensic inspection |
| **8. Analysis Execution** | ✅ Success / ❌ Failed / 🔄 In Progress / ⏸️ Pending | - | YYYY-MM-DD | analysis_executor agent |
| **9. Results Validation** | ✅ Approved / ⚠️ Conditional / ❌ Rejected / ⏸️ Pending | X.X/10 | YYYY-MM-DD | results_inspector agent |
| **10. Theoretical Implications** | ✅ Complete / 🔄 In Progress / ⏸️ Pending | - | YYYY-MM-DD | scholar agent (post-results) |
| **11. Final Statistical Audit** | ✅ Approved / ⚠️ Conditional / ❌ Rejected / ⏸️ Pending | X.X/10 | YYYY-MM-DD | statistics_expert agent (post-results) |

---

## Current Status Details

**Phase:** [Current phase name]

**Last Action:** [What was just completed]

**Next Action:** [What needs to happen next]

**Blocking Issues:** [Any issues preventing progress, or "None"]

---

## Files Created

### Specification
- ✅ `info.md` (YYYY-MM-DD)
- ✅ `config.yaml` (YYYY-MM-DD)
- ✅ `logs/rq_spec_context.md` (YYYY-MM-DD)

### Validation Reports
- ✅ `validation/scholar_report.md` (YYYY-MM-DD) - Score: X.X/10
- ✅ `validation/statistics_report.md` (YYYY-MM-DD) - Score: X.X/10

### Data Files
- ✅ `data/irt_input.csv` + `.md` (YYYY-MM-DD)
- ✅ `data/theta_scores.csv` + `.md` (YYYY-MM-DD)
- ✅ `data/lmm_input.csv` + `.md` (YYYY-MM-DD)

### Analysis Results
- ✅ `data/lmm_results.csv` + `.md` (YYYY-MM-DD)
- ✅ `plots/trajectory_plot.png` + `_data.csv` (YYYY-MM-DD)

### Agent Reports
- ✅ `logs/rq_specification_report.md` (YYYY-MM-DD)
- ✅ `logs/data_prep_report.md` (YYYY-MM-DD)
- ✅ `logs/analysis_executor_report.md` (YYYY-MM-DD)
- ✅ `logs/results_inspector_report.md` (YYYY-MM-DD)

---

## Validation Scores Summary

| Validator | Phase | Score | Status | Date |
|-----------|-------|-------|--------|------|
| Scholar | Pre-execution | X.X/10 | ✅ APPROVED | YYYY-MM-DD |
| Statistics Expert | Pre-execution | X.X/10 | ✅ APPROVED | YYYY-MM-DD |
| Results Inspector | Post-execution | X.X/10 | ✅ APPROVED | YYYY-MM-DD |
| Scholar | Post-results | X.X/10 | ✅ APPROVED | YYYY-MM-DD |
| Statistics Expert | Post-analysis | X.X/10 | ✅ APPROVED | YYYY-MM-DD |

**Overall Quality:** [All ≥9.25 = Gold Standard / All ≥9.0 = Acceptable / Any <9.0 = Needs Revision]

---

## Iteration History

### Iteration 1 (YYYY-MM-DD)
- **Trigger:** [Initial specification / Scholar rejected / Statistics rejected / Analysis failed]
- **Changes Made:** [Brief description]
- **Outcome:** [Approved / Rejected again / Success]

---

## Notes for Thesis Examiners

[Human-readable summary of this RQ's status, key findings, any special considerations]

---

**How Agents Update This File:**

Each agent appends their completion status using Edit tool:
1. Find their phase row in Status Table
2. Update: Status → ✅/❌, Score (if applicable), Date, Notes
3. Update "Current Status Details" section
4. Add their output files to "Files Created" section
5. If validator: Add row to "Validation Scores Summary"
6. If iteration: Add entry to "Iteration History"

**Example Edit:**
```markdown
| **2. Scholar Validation** | ✅ Approved | 9.5/10 | 2025-11-12 | Theoretical grounding validated |
```

---

**End of Status Template**
