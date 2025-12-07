# ch6_dfdata_wide_format_paradigm_parsing

**Topic Description:** dfData.csv column structure for confidence data. Data is in WIDE format with paradigm embedded in column names (TC_{PARADIGM}-{DOMAIN}-{ITEM}), NOT long format with separate Paradigm column. Requires column name parsing to filter paradigms.

---

## dfData.csv Wide Format - Paradigm Parsing (2025-12-06 22:00)

**Context:** During RQ 6.1.1 Step 00 (Extract VR Data), g_code generated code that expected long format data with a Paradigm column, but dfData.csv is actually wide format with paradigm embedded in column names.

**Archived from:** state.md (Session 2025-12-06 22:00)
**Original Date:** 2025-12-06 22:00
**Reason:** Data structure clarified, pattern documented

---

### Data Structure

**dfData.csv structure:**
- **Format:** WIDE (one row per session, columns for each item)
- **Column naming:** `TC_{PARADIGM}-{DOMAIN}-{ITEM}`
- **Example columns:**
  - TC_IFR-What-01 (Interactive Free Recall, What domain, item 1)
  - TC_ICR-Where-01 (Interactive Cued Recall, Where domain, item 1)
  - TC_IRE-When-01 (Interactive Recognition, When domain, item 1)

**NOT this structure:**
- ❌ Long format with separate Paradigm column
- ❌ Separate columns for each paradigm property

---

### The Fix

**Original g_code assumption:**
```python
# Expected (WRONG):
df_filtered = df[df['Paradigm'].isin(['IFR', 'ICR', 'IRE'])]
```

**Actual structure requires:**
```python
# Correct:
# Parse column names
tc_cols = [col for col in df.columns if col.startswith('TC_')]

# Extract paradigm from column name
# Format: TC_{PARADIGM}-{DOMAIN}-{ITEM}
paradigms = ['IFR', 'ICR', 'IRE']
selected_cols = [col for col in tc_cols
                 if any(f'TC_{p}-' in col for p in paradigms)]

# Filter to selected columns
df_filtered = df[['composite_ID'] + selected_cols]
```

---

### Affected RQs

**Any RQ that filters confidence data by paradigm:**
- RQ 6.1.1: All interactive paradigms (IFR, ICR, IRE)
- RQ 6.3.1: All interactive paradigms (3-factor GRM)
- RQ 6.4.1: Paradigm-specific trajectories
- Others filtering by paradigm subset

**Pattern applies to:**
- TC_* columns (confidence data)
- AC_* columns (accuracy data) - same structure

---

### Key Insight

**Column naming is self-documenting:**
- Paradigm: TC_**IFR**-What-01
- Domain: TC_IFR-**What**-01
- Item: TC_IFR-What-**01**

**Parse column names to extract metadata**, don't expect separate metadata columns.

---

### Status

**Data structure pattern documented.**

Future g_code invocations for Ch6 confidence data should parse column names, not filter by separate Paradigm column.

---
