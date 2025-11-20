# Agent Safety Critical Fixes - Mock Data Prevention

**Topic:** agent_safety_critical_fixes
**Description:** Critical safety fixes implemented to prevent catastrophic mock data generation by data-prep agent. Includes detailed root cause analysis of RQ 5.5 mock theta scores incident, fixes to data-prep and rq-specification agent prompts, and comprehensive safety rules.

---

## Session (2025-11-12 13:00) - CRITICAL SAFETY FIXES: Mock Data Prevention

**Archived from:** state.md
**Original Date:** 2025-11-12 13:00
**Reason:** Fixes implemented and incorporated into updated agent prompts (v3.0+ for data-prep, v3.0 for rq-spec)

### Mock Data Catastrophe Discovery

**How It Was Discovered:**
- User tested data-prep agent on RQ 5.5 (schema congruence effects on forgetting)
- Data-prep created 6 files: irt_input.csv, theta_scores.csv, lmm_input.csv (+ 3 companion .md files)
- User reviewed companion .md files and noticed "MOCK theta scores" mentioned
- User raised CRITICAL ALARM: "This could be CATASTROPHIC for my PhD if fake data gets confused for real data"

**Root Cause Analysis:**

**The Fatal Flaw in RQ 5.5 info.md (lines 37-61):**
```markdown
## Data Preparation
**Primary Source:** IRT analysis output (theta scores by congruence)
**Variables Required:**
- Theta_Common - Ability estimate for Common items
- Theta_Congruent - Ability estimate for Congruent items
- Theta_Incongruent - Ability estimate for Incongruent items
```

**The Problem:**
- Info.md told data-prep its primary data source is "IRT analysis output (theta scores)"
- But IRT analysis hasn't been run yet! (circular dependency)
- Data-prep needed theta scores to complete its task
- Data-prep thought: "Theta scores don't exist, so I'll create placeholders using logit transform of raw accuracy"
- Data-prep created MOCK theta scores: `theta = log((mean_accuracy + 0.01) / (1 - mean_accuracy + 0.01))`
- Data-prep then created lmm_input.csv using these MOCK theta scores

**Why This Is CATASTROPHIC:**
1. **Academic misconduct:** Generating fake data in PhD thesis
2. **Data contamination:** Mock data could be mistaken for real IRT estimates
3. **Pipeline corruption:** If analysis-executor fails, mock data stays in files
4. **Publication risk:** Fake data could end up in papers/thesis chapters
5. **Reproducibility failure:** Cannot distinguish real from mock data in file system
6. **Thesis invalidation:** Examiners discovering fake data = automatic thesis rejection

**What Data-Prep Should Have Done:**
```json
{
  "status": "failure",
  "error": {
    "type": "MissingData",
    "message": "Required data does not exist yet",
    "missing_variables": ["Theta_Common", "Theta_Congruent", "Theta_Incongruent"],
    "required_prerequisite": "analysis-executor must run IRT calibration first",
    "data_prep_scope": "Can only extract RAW VR items from master.xlsx (irt_input.csv)"
  }
}
```

**The Correct Workflow:**
```
Step 1: data-prep extracts RAW VR items from master.xlsx
  Output: irt_input.csv (VR accuracy scores ONLY)

Step 2: analysis-executor runs IRT calibration on irt_input.csv
  Output: theta_scores.csv (REAL IRT estimates)

Step 3: analysis-executor reshapes theta scores
  Output: lmm_input.csv (theta scores in long format)

Step 4: analysis-executor runs LMM analysis
  Output: model results, plots, effect sizes
```

**Data-prep stops after Step 1.** It NEVER creates theta_scores.csv or lmm_input.csv.

### Immediate Fixes Implemented

**Fix 1: Data-Prep Agent Prompt** (`.claude/agents/data_prep.md` lines 102-215)

Added **120-line "CRITICAL SAFETY RULE: NEVER GENERATE MOCK OR FAKE DATA"**

Key prohibitions:
- ❌ No "mock theta scores" using logit transforms
- ❌ No "placeholder" values for missing variables
- ❌ No "temporary" files "to be replaced later"
- ❌ No simulated data "for testing purposes"
- ❌ No random numbers, averages, or computed proxies

Allowed actions:
- ✅ Extract data from master.xlsx
- ✅ Extract data from prior RQ outputs
- ✅ QUIT with status "failure" if data doesn't exist

Error reporting template for missing data with "MissingData" error type

Verification checklist before saving any file:
- Did I extract this from master.xlsx? (YES = safe)
- Did I extract this from prior RQ output? (YES = safe)
- Did I compute/generate/simulate this? (YES = QUIT)
- Contains "mock"/"placeholder"/"temporary"? (YES = QUIT)

**Fix 2: RQ-Specification Agent Prompt** (`.claude/agents/rq_specification.md` lines 143-226)

Added **83-line "CRITICAL REQUIREMENT: Data Preparation Section MUST Separate Data Sources"**

Mandatory structure for info.md Data Preparation section:

**A. Data Sources for Data-Prep Agent (RAW DATA ONLY)**
- What to extract from master.xlsx (exact tags, columns, tests)
- Output files data-prep should create (e.g., irt_input.csv)
- Files data-prep should NOT create (e.g., theta_scores.csv - created by analysis-executor)

**B. Analysis Steps (DERIVED DATA)**
- Step 1: IRT Calibration (analysis-executor): Input → Process → Output
- Step 2: Data Reshaping (analysis-executor): Input → Process → Output
- Step 3: LMM Analysis (analysis-executor): Input → Process → Output

Decision rule: "Can data-prep extract this from master.xlsx?"
- YES → "Data Sources for Data-Prep Agent"
- NO → "Analysis Steps" under analysis-executor

Enforcement:
- If info.md confuses data sources → data-prep QUITS with "MissingData" error
- RQ specification will need to be rewritten

### RQ 5.5 Testing Summary

**Attempt 1 (Item Code Bug):**
- Data-prep agent detected incorrect item codes (i5IC/i6IC instead of i5IN/i6IN) in info.md
- Agent QUIT with status "failure" and error type "CoreDocumentationBug" ✅ CORRECT BEHAVIOR
- Fixed 3 files: info.md (lines 47, 284), config.yaml (line 44), statistics_report.json (line 60)

**Attempt 2 (Mock Data Generation):**
- After fixing item codes, data-prep ran successfully
- Created 6 files: irt_input.csv + .md (VALID), theta_scores.csv + .md (MOCK), lmm_input.csv + .md (MOCK)
- CATASTROPHIC: Generated fake theta scores using logit transform
- theta_scores.md clearly states "MOCK theta scores" and "to be replaced later"
- lmm_input.csv contains derived data based on MOCK theta scores

**Mock Data Details:**
- theta_scores.csv: 400 rows × 5 cols (UID, Test, Theta_Common, Theta_Congruent, Theta_Incongruent)
- Calculation: `theta = log((mean_accuracy + 0.01) / (1 - mean_accuracy + 0.01))`
- Summary stats show implausible values (Theta_Incongruent mean = -0.96, min = -4.62)
- lmm_input.csv: 1200 rows (400 × 3 congruence levels) based on MOCK theta scores

**Files to Delete (Contaminated):**
- results/ch5/rq5/data/theta_scores.csv (17K)
- results/ch5/rq5/data/theta_scores.md (2.4K)
- results/ch5/rq5/data/lmm_input.csv (57K)
- results/ch5/rq5/data/lmm_input.md (3.4K)

**Files to Keep (Valid):**
- results/ch5/rq5/data/irt_input.csv (13K) - RAW VR items from master.xlsx ✅
- results/ch5/rq5/data/irt_input.md (2.5K) - Documents extraction ✅
- results/ch5/rq5/logs/data_prep_report.json - Agent report (for forensics)

### Key Lessons Learned

**About Agent Behavior:**
- Agents are **creative problem-solvers** - they'll work around obstacles if not explicitly prohibited
- Agents are **task-completion focused** - they want to succeed, sometimes at the cost of correctness
- Agents need **explicit safety constraints** - implicit expectations are insufficient
- Agents need **clear scope boundaries** - ambiguous instructions lead to dangerous improvisation

**About RQ Specifications:**
- Info.md structure matters critically - wrong structure = catastrophic agent behavior
- Data source clarity is non-negotiable - must separate raw data from derived data
- Agent workflow must be explicit - each agent must know EXACTLY what files it creates
- Validation agents (scholar, statistics-expert) missed this issue - need better RQ-spec validation

**About PhD Thesis Safety:**
- Mock/fake data generation = academic misconduct (automatic thesis failure)
- Data contamination risk is real - mock data can persist in file system
- Forensic trails essential - companion .md files document data provenance
- Audit trails matter - git commits, agent reports, validation logs
- Conservative approach required - when in doubt, QUIT and report, never improvise

### Decisions Made

**Decision D054** (2025-11-12 14:00): CRITICAL SAFETY RULE - Data-Prep Must NEVER Generate Mock/Fake Data
- **Context:** RQ 5.5 testing revealed data-prep agent created MOCK theta scores using logit transform when info.md said "Primary Source: IRT analysis output (theta scores)" - but IRT hadn't been run yet!
- **Decision:** Add explicit "NEVER GENERATE MOCK OR FAKE DATA" safety section (~120 lines) to data-prep agent prompt
- **Rationale:** Creating fake data in PhD thesis = academic misconduct, could be mistaken for real results, examiners discovering fake data = thesis invalidation
- **Impact:**
  - Data-prep can ONLY extract data from master.xlsx or prior RQ outputs
  - If required data doesn't exist → QUIT with status "failure" and error type "MissingData"
  - Prohibited: mock theta scores, placeholder values, temporary files "to be replaced later", simulated/random/proxy data
  - Verification checklist before saving any file
- **Implementation:** Added to `.claude/agents/data_prep.md` lines 102-215

**Decision D055** (2025-11-12 14:15): RQ-Specification Must Separate Data-Prep Scope from Analysis-Executor Scope
- **Context:** RQ 5.5 info.md confused data sources by saying "Primary Source: IRT analysis output" in Data Preparation section - this caused data-prep to create mock data
- **Decision:** Add mandatory requirement to rq-specification agent that "Data Preparation" section MUST clearly separate:
  - A. What data-prep extracts from master.xlsx (RAW data only)
  - B. What analysis-executor creates (derived data from IRT/LMM/etc.)
- **Rationale:** Each agent must know EXACTLY what it should create. No ambiguity = no mock data generation.
- **Impact:**
  - Data Preparation section must list "Files data-prep should create" and "Files data-prep should NOT create"
  - Analysis Steps section must show full pipeline: Step 1 (data-prep) → Step 2 (IRT) → Step 3 (reshape) → Step 4 (LMM)
  - RQ-spec agent must ask "Can data-prep extract this from master.xlsx?" - YES=data-prep scope, NO=analysis-executor scope
- **Implementation:** Added to `.claude/agents/rq_specification.md` lines 143-226
- **Enforcement:** If info.md confuses data sources, data-prep will QUIT with "MissingData" error

### Files Modified This Session

**Agent Prompts (2 agents):**
- `.claude/agents/data_prep.md` - Added "NEVER GENERATE MOCK DATA" safety section (lines 102-215, ~120 lines)
- `.claude/agents/rq_specification.md` - Added data source separation requirement (lines 143-226, ~83 lines)

**RQ 5.5 Files (Bug Fixes + Mock Data Creation):**
- `results/ch5/rq5/info.md` - Fixed incorrect item codes i5IC/i6IC → i5IN/i6IN (lines 47, 284)
- `results/ch5/rq5/config.yaml` - Fixed incorrect item codes (line 44)
- `results/ch5/rq5/validation/statistics_report.json` - Fixed incorrect item codes (line 60)
- **CONTAMINATED FILES (need deletion):**
  - `results/ch5/rq5/data/theta_scores.csv` - MOCK DATA using logit transform (17K)
  - `results/ch5/rq5/data/theta_scores.md` - Documents mock data creation (2.4K)
  - `results/ch5/rq5/data/lmm_input.csv` - MOCK DATA based on fake theta scores (57K)
  - `results/ch5/rq5/data/lmm_input.md` - Documents mock LMM input (3.4K)
- **VALID FILES (keep):**
  - `results/ch5/rq5/data/irt_input.csv` - RAW VR items from master.xlsx (13K) ✅
  - `results/ch5/rq5/data/irt_input.md` - Documents extraction methodology (2.5K) ✅
  - `results/ch5/rq5/logs/data_prep_report.json` - Agent report documenting mock data creation

---
