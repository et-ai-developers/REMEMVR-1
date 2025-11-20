# REMEMVR Variables System Reference (LEGACY)

**Purpose:** Documentation of OLD variables.xlsx system for reference.

**Status:** DEPRECATED - New method uses direct data.py interaction per RQ.

**Audience:** Historical reference only.

**Last Updated:** 2025-01-04

---

## ⚠️ IMPORTANT: THIS METHOD IS DEPRECATED

**Old Workflow:**
- Define all variables in variables.xlsx with regex patterns
- Run data.py to generate dfData with all variables
- Use dfData for all analyses

**New Workflow (Active):**
- Data-prep agent reads RQ requirements
- Agent calls data.py functions directly to extract needed tags
- Creates RQ-specific input.csv (not a universal dfData)
- Each RQ gets only the data it needs

**Why changed:**
- Variables.xlsx became unwieldy (~480 rows)
- Many variables unused in final analyses
- Hard to track which variables belong to which RQ
- Difficult to maintain and debug
- New method: one RQ at a time, transparent, validated at each step

---

## VARIABLES.XLSX STRUCTURE (HISTORICAL)

### Columns:

#### 1. Name
**Purpose:** The column name in the output dfData

**Format:** No spaces, use underscores

**Examples:**
- `Theta_All`
- `TQ_IFR_N_i1`
- `Age`
- `RAVLT_Total`

#### 2. Label
**Purpose:** Human-readable description of the variable

**Examples:**
- "IRT theta score for all items"
- "Accuracy for Item 1 in Items Free Recall, What domain"

#### 3. Function
**Purpose:** How to combine multiple matched datapoints

**Options:**
- **sum** = Add all matched values
- **mean** = Calculate arithmetic mean
- **string** = Keep as text (no aggregation)

#### 4. Type
**Purpose:** Data category

**Options:**
- **dem** = Demographic data (1 timepoint)
- **cog** = Cognitive test data (1 timepoint)
- **vr** = REMEMVR data (4 timepoints)

#### 5. Regex
**Purpose:** Regular expression pattern to match tags in master.xlsx

**Format:** Python regex syntax

---

## REGEX PATTERNS (HISTORICAL REFERENCE)

### Example Patterns:

#### Match NART score:
```regex
.*-COG-X-NAR-Scor
```

#### Match all Items Free Recall "What" accuracy scores:
```regex
.*-RVR-T[1-4]-IFR-N-i[1-6].*-ANS
```

#### Match confidence scores for Item 1 in all paradigms:
```regex
.*-RVR-T[1-4]-(IFR|ICR|IRE)-.-i1CM-.*-CON
```

---

## WHY THIS METHOD WAS ABANDONED

### Problems with OLD Method:

1. **Maintenance Burden:**
   - 480+ rows in variables.xlsx
   - Hard to find/edit specific variables
   - Unclear which variables are actually used

2. **Lack of Traceability:**
   - Which RQ uses which variables?
   - Why was this variable created?
   - When was it last used?

3. **All-or-Nothing Approach:**
   - Had to compute ALL variables even if only needed 5
   - Slow data loading
   - Difficult to test individual variable extraction

4. **Error-Prone:**
   - Regex errors silently produce wrong results
   - Hard to debug which regex caused issue
   - No validation at variable level

5. **Not RQ-Specific:**
   - dfData included all participants, all tests, all variables
   - Each RQ had to filter down from massive dataframe
   - Harder to understand data flow

### Advantages of NEW Method:

1. **Transparency:**
   - Data-prep agent explicitly states what data is being extracted
   - User can review and approve

2. **Validation:**
   - Each RQ's input.csv validated before analysis starts
   - Errors caught immediately

3. **Maintainability:**
   - Data extraction logic lives with the RQ
   - Easy to modify for one RQ without affecting others

4. **Flexibility:**
   - Can use previous RQ outputs as inputs
   - Can combine multiple data sources
   - Not limited to master.xlsx tags

5. **Auditability:**
   - Full record of data preparation in RQ folder
   - Can regenerate input.csv at any time

---

## MIGRATION NOTES

**If you need to recreate a variable from OLD system in NEW system:**

1. Find the variable definition in variables.xlsx (if it still exists)
2. Note the regex pattern
3. In NEW system, data-prep agent will:
   - Parse the regex to understand what tags are needed
   - Call data.py functions to extract those tags directly
   - Apply the same aggregation function (sum/mean/string)
   - Validate the result

**Example:**

**OLD:** Variable `Mean_Accuracy_IFR` with regex `.*-RVR-T1-IFR-.*-ANS` and function `mean`

**NEW:** Data-prep agent code:
```python
# Extract all IFR accuracy scores for Test 1
tags_to_extract = [
    f"{uid}-RVR-T1-IFR-N-i1CM-.*-ANS",
    f"{uid}-RVR-T1-IFR-N-i2CM-.*-ANS",
    # ... etc for all items/domains
]
data = extract_tags_from_master(tags_to_extract)
mean_accuracy = data.mean()
```

---

**End of Legacy Variables System Reference**
