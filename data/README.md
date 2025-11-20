# REMEMVR Data Extraction API

**Version:** 2.0 (TDD Rewrite)
**Created:** 2025-01-05
**Test Coverage:** 14/14 tests passing (100%)

---

## Overview

This module provides a clean, validated API for extracting data from `master.xlsx` using a tag-based system. It replaces the legacy `variables.xlsx` regex approach with direct tag extraction.

**Key Benefits:**
- ✅ **Simple API** - Easy to understand and explain
- ✅ **Built-in Validation** - Expected dimensions, missing data rules
- ✅ **Real Data Tested** - All functions tested with actual master.xlsx
- ✅ **Flexible Input** - Supports lists, dicts, wildcards
- ✅ **Comprehensive Errors** - Clear error messages for debugging

---

## Quick Start

### Basic Tag Extraction

```python
from data.data import extract_tag

# Extract RPM scores for all 100 participants
rpm_scores = extract_tag(
    tag_pattern="{UID}-COG-X-RPM-Scor",
    expected_count=100
)
# Returns: DataFrame with ['UID', 'value'] columns
```

### Multiple Tags

```python
from data.data import extract_tags

# Extract multiple cognitive scores
cognitive_data = extract_tags(
    tag_patterns={
        'RPM_Score': '{UID}-COG-X-RPM-Scor',
        'NART_Score': '{UID}-COG-X-NART-Scor',
        'Age': '{UID}-DEM-X-Age'
    },
    expected_rows=100,
    expected_cols=4  # UID + 3 scores
)
# Returns: DataFrame with ['UID', 'RPM_Score', 'NART_Score', 'Age']
```

### VR Data Across Tests

```python
from data.data import extract_vr_tags

# Extract Item 1 accuracy across all 4 tests
item1_accuracy = extract_vr_tags(
    paradigm='IFR',
    domain='N',
    item='i1CM',
    measure='ANS',
    expected_rows=400  # 100 participants × 4 tests
)
# Returns: Long-format DataFrame with ['UID', 'test', 'value']
```

---

## API Reference

### Core Functions

| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| **`load_master()`** | Load master.xlsx with caching | `use_cache` (bool) | Master DataFrame |
| **`extract_tag()`** | Extract single tag pattern | Tag pattern string | DataFrame with UID + value |
| **`extract_tags()`** | Extract multiple tag patterns | List or dict of patterns | Wide-format DataFrame |
| **`validate_extraction()`** | Validate extracted data | DataFrame + validation rules | Validation report dict |

### Advanced Functions

| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| **`extract_vr_tags()`** | VR data with test wildcards | Paradigm, domain, item, measure | Long-format DataFrame |
| **`extract_cognitive_scores()`** | Computed cognitive totals | Test name, components | DataFrame with computed scores |
| **`load_rq_output()`** | Load previous RQ results | File path + validation rules | Previous RQ DataFrame |
| **`combine_data_sources()`** | Merge all data sources | Master tags, RQ outputs, computed | Combined DataFrame |

### Exception Classes

| Exception | Purpose | When Raised |
|-----------|---------|-------------|
| **`ValidationError`** | Data validation failure | Dimension mismatch, missing data violations, tag not found |

---

## Common Usage Patterns

### Pattern 1: Basic RQ Data Preparation

**Use Case:** Extract demographic and cognitive data for simple analysis

```python
from data.data import extract_tags

# Prepare input data for RQ
input_data = extract_tags(
    tag_patterns={
        'Age': '{UID}-DEM-X-Age',
        'Education': '{UID}-DEM-X-Education',
        'RPM_Score': '{UID}-COG-X-RPM-Scor',
        'NART_Score': '{UID}-COG-X-NART-Scor'
    },
    expected_rows=100,
    expected_cols=5  # UID + 4 variables
)

# Save to RQ folder
input_data.to_csv('results/ch7/rq1/data/input.csv', index=False)
```

### Pattern 2: VR Data Extraction

**Use Case:** Extract VR accuracy/confidence across multiple tests

```python
from data.data import extract_vr_tags
import pandas as pd

# Extract Item 1 accuracy for all 4 tests
item1_data = extract_vr_tags(
    paradigm='IFR',
    domain='N',
    item='i1CM',
    measure='ANS',
    expected_rows=400
)

# Pivot to wide format for analysis
item1_wide = item1_data.pivot(
    index='UID',
    columns='test',
    values='value'
).reset_index()
item1_wide.columns = ['UID', 'T1', 'T2', 'T3', 'T4']
```

### Pattern 3: Computed Cognitive Scores

**Use Case:** Calculate RAVLT_Total from individual trial scores

```python
from data.data import extract_cognitive_scores

# Compute RAVLT total score (sum of T1-T5)
ravlt_totals = extract_cognitive_scores(
    test_name='RAVLT',
    scores_to_compute={
        'RAVLT_Total': ['T1Sc', 'T2Sc', 'T3Sc', 'T4Sc', 'T5Sc']
    },
    expected_count=100
)

# Returns: DataFrame with ['UID', 'RAVLT_Total']
```

### Pattern 4: Combining Multiple Data Sources

**Use Case:** Merge demographics + previous RQ results + computed scores

```python
from data.data import combine_data_sources

# Combine master tags, previous RQ output, and computed scores
full_data = combine_data_sources(
    master_tags={
        'Age': '{UID}-DEM-X-Age',
        'Education': '{UID}-DEM-X-Education'
    },
    rq_outputs=[
        'results/ch5/rq1/data/output.csv'  # Theta scores from previous RQ
    ],
    expected_rows=100
)

# Result contains: UID, Age, Education, theta_what, theta_where, theta_when
```

### Pattern 5: Validation with Missing Data Rules

**Use Case:** Allow specific amounts of missing data per variable

```python
from data.data import extract_tags

# Extract data with explicit missing data rules
data = extract_tags(
    tag_patterns={
        'RAVLT_T4': '{UID}-COG-X-RAV-T4Sc',
        'RAVLT_T5': '{UID}-COG-X-RAV-T5Sc',
        'Age': '{UID}-DEM-X-Age'
    },
    allow_missing={
        'RAVLT_T4': 5,  # Allow up to 5 missing
        'RAVLT_T5': 5,  # Allow up to 5 missing
        'Age': 0        # No missing allowed
    },
    expected_rows=100
)
```

---

## Advanced Workflows

### Workflow 1: Full RQ Data Pipeline

**Steps:**
1. Extract master.xlsx tags
2. Load previous RQ outputs
3. Compute derived scores
4. Combine all sources
5. Validate final dataframe
6. Save to RQ folder

```python
from data.data import (
    extract_tags,
    load_rq_output,
    combine_data_sources,
    validate_extraction
)
import pandas as pd

# Step 1: Extract master tags
master_data = extract_tags(
    tag_patterns={
        'Age': '{UID}-DEM-X-Age',
        'Education': '{UID}-DEM-X-Education'
    }
)

# Step 2: Load previous RQ output
theta_scores = load_rq_output(
    file_path='results/ch5/rq1/data/output.csv',
    required_cols=['UID', 'theta_what', 'theta_where', 'theta_when']
)

# Step 3: Compute derived scores
age_mean = master_data['Age'].mean()
age_centered = master_data['Age'] - age_mean

# Step 4: Combine all sources
full_data = combine_data_sources(
    master_tags={
        'Age': '{UID}-DEM-X-Age',
        'Education': '{UID}-DEM-X-Education'
    },
    rq_outputs=['results/ch5/rq1/data/output.csv'],
    computed_scores={
        'Age_Centered': age_centered
    },
    expected_rows=100,
    expected_cols=7  # UID + Age + Education + 3 thetas + Age_Centered
)

# Step 5: Validate
validation = validate_extraction(
    full_data,
    expected_rows=100,
    expected_cols=7,
    required_cols=['UID', 'Age', 'Education', 'theta_what']
)

if not validation['valid']:
    print("Validation errors:", validation['errors'])
else:
    print("Validation passed!")
    # Step 6: Save
    full_data.to_csv('results/ch5/rq2/data/input.csv', index=False)
```

### Workflow 2: Extract All Items for One Domain

**Use Case:** Extract accuracy for all 6 items (What domain) across all 4 tests

```python
from data.data import extract_vr_tags
import pandas as pd

# Items: i1CM, i2CM, i3CG, i4CG, i5IC, i6IC
items = ['i1CM', 'i2CM', 'i3CG', 'i4CG', 'i5IC', 'i6IC']

all_items_data = []

for item in items:
    item_data = extract_vr_tags(
        paradigm='IFR',
        domain='N',
        item=item,
        measure='ANS',
        expected_rows=400
    )
    item_data['item'] = item  # Add item identifier
    all_items_data.append(item_data)

# Combine all items
combined = pd.concat(all_items_data, ignore_index=True)
# Result: Long-format with columns ['UID', 'test', 'value', 'item']
```

### Workflow 3: Extract Multiple VR Domains

**Use Case:** Extract What, Where-Up, Where-Down, When for one item

```python
from data.data import extract_vr_tags
import pandas as pd

domains = {
    'What': 'N',
    'Where_Up': 'U',
    'Where_Down': 'D',
    'When': 'O'
}

domain_data = {}

for domain_name, domain_code in domains.items():
    data = extract_vr_tags(
        paradigm='IFR',
        domain=domain_code,
        item='i1CM',
        measure='ANS',
        expected_rows=400
    )
    # Pivot to wide format
    data_wide = data.pivot(
        index='UID',
        columns='test',
        values='value'
    ).reset_index()
    data_wide.columns = ['UID', f'{domain_name}_T1', f'{domain_name}_T2',
                         f'{domain_name}_T3', f'{domain_name}_T4']
    domain_data[domain_name] = data_wide

# Merge all domains
result = domain_data['What']
for domain_name in ['Where_Up', 'Where_Down', 'When']:
    result = result.merge(domain_data[domain_name], on='UID', how='left')

# Result: Wide-format with UID + 16 columns (4 domains × 4 tests)
```

---

## Error Handling

### Common Errors and Solutions

#### 1. ValidationError: Tag not found

```python
# ERROR: Tag 'A010-COG-X-RPM-Score' not found (note "Score" vs "Scor")
rpm = extract_tag("{UID}-COG-X-RPM-Score")  # WRONG

# SOLUTION: Use exact tag spelling (check docs/data_structure.md)
rpm = extract_tag("{UID}-COG-X-RPM-Scor")  # CORRECT (note "Scor")
```

**Tip:** Always use EXACT tag spelling with dashes. Check `docs/data_structure.md` or `docs/cognitive_tests.md` for correct tag names.

#### 2. ValidationError: Expected count mismatch

```python
# ERROR: Expected 100 values, got 95
data = extract_tag("{UID}-COG-X-RAV-T5Sc", expected_count=100)

# SOLUTION: Allow missing data or adjust expected count
data = extract_tag("{UID}-COG-X-RAV-T5Sc", allow_missing=True, expected_count=100)
```

**Tip:** Use `allow_missing=True` for cognitive test scores (some participants have missing trials).

#### 3. ValidationError: Missing data found

```python
# ERROR: Missing data found for A015 at tag (value='x')
age = extract_tag("{UID}-DEM-X-Age", allow_missing=False)

# SOLUTION: Set allow_missing=True or investigate data quality
age = extract_tag("{UID}-DEM-X-Age", allow_missing=True)
```

**Tip:** For critical variables like Age, investigate missing data manually before allowing it.

#### 4. ValidationError: Dimension mismatch

```python
# ERROR: Expected 4 columns, got 5
data = extract_tags(
    tag_patterns={'RPM': '{UID}-COG-X-RPM-Scor', 'Age': '{UID}-DEM-X-Age'},
    expected_cols=4  # Wrong! Should be 3 (UID + RPM + Age)
)

# SOLUTION: Correct the expected_cols parameter
data = extract_tags(
    tag_patterns={'RPM': '{UID}-COG-X-RPM-Scor', 'Age': '{UID}-DEM-X-Age'},
    expected_cols=3  # Correct! UID + 2 variables
)
```

**Tip:** Always count UID column when specifying expected_cols.

---

## Best Practices

### 1. Always Validate Expectations

**WHY:** Catch silent failures early (incorrect tags, missing data, dimension mismatches)

```python
# GOOD: Explicit expectations
data = extract_tag("{UID}-COG-X-RPM-Scor", expected_count=100)

# BAD: No validation
data = extract_tag("{UID}-COG-X-RPM-Scor")
```

### 2. Use Descriptive Column Names

**WHY:** Makes output data self-documenting

```python
# GOOD: Clear column names
cognitive = extract_tags({
    'RPM_Score': '{UID}-COG-X-RPM-Scor',
    'NART_Score': '{UID}-COG-X-NART-Scor'
})

# BAD: Auto-generated names
cognitive = extract_tags([
    '{UID}-COG-X-RPM-Scor',
    '{UID}-COG-X-NART-Scor'
])
# Results in: COG_X_RPM_Scor, COG_X_NART_Scor (less clear)
```

### 3. Specify Missing Data Rules Explicitly

**WHY:** Different variables have different missing data tolerances

```python
# GOOD: Explicit per-variable rules
data = extract_tags(
    tag_patterns={
        'RAVLT_T5': '{UID}-COG-X-RAV-T5Sc',
        'Age': '{UID}-DEM-X-Age'
    },
    allow_missing={'RAVLT_T5': 5, 'Age': 0}  # T5 can have 5 missing, Age cannot
)

# BAD: Same rule for all
data = extract_tags(
    tag_patterns={...},
    allow_missing=True  # Allows unlimited missing for everything
)
```

### 4. Load Master Once for Multiple Extractions

**WHY:** Faster performance (avoid reloading 3.9 MB Excel file)

```python
from data.data import load_master, extract_tag

# GOOD: Load once, reuse
df_master = load_master()
rpm = extract_tag("{UID}-COG-X-RPM-Scor", df_master=df_master)
nart = extract_tag("{UID}-COG-X-NART-Scor", df_master=df_master)

# BAD: Load multiple times
rpm = extract_tag("{UID}-COG-X-RPM-Scor")  # Loads master.xlsx
nart = extract_tag("{UID}-COG-X-NART-Scor")  # Loads master.xlsx again
```

### 5. Save Intermediate Results

**WHY:** Easier debugging, reproducibility

```python
# GOOD: Save after each major step
master_data = extract_tags({...})
master_data.to_csv('results/ch5/rq1/data/intermediate_master.csv', index=False)

theta_scores = load_rq_output('results/ch5/rq1/data/output.csv')

combined = combine_data_sources(...)
combined.to_csv('results/ch5/rq2/data/input.csv', index=False)

# BAD: No intermediate saves (hard to debug if final step fails)
```

### 6. Validate Before Saving

**WHY:** Catch issues before analysis begins

```python
# GOOD: Validate then save
data = combine_data_sources(...)
validation = validate_extraction(
    data,
    expected_rows=100,
    expected_cols=7,
    required_cols=['UID', 'Age', 'theta_what']
)

if validation['valid']:
    data.to_csv('results/ch5/rq2/data/input.csv', index=False)
    print("✅ Data validated and saved")
else:
    print("❌ Validation failed:", validation['errors'])
    # Fix issues before proceeding

# BAD: Save without validation
data.to_csv('results/ch5/rq2/data/input.csv', index=False)
# Might save corrupted data!
```

---

## Tag Reference

### Tag Format

**Standard Format:** `{UID}-{Section}-{Subsection}-{Variable}-{Details}`

**Examples:**
- Cognitive: `A010-COG-X-RPM-Scor`
- Demographic: `A010-DEM-X-Age`
- VR: `A010-RVR-T1-IFR-N-i1CM-n3s2f1-ANS`

### Common Tag Patterns

| Category | Example Tag | Description |
|----------|-------------|-------------|
| **Demographics** | `{UID}-DEM-X-Age` | Age in years |
| | `{UID}-DEM-X-Education` | Education years |
| | `{UID}-DEM-X-Gender` | Gender (M/F) |
| **Cognitive Tests** | `{UID}-COG-X-RPM-Scor` | RPM total score |
| | `{UID}-COG-X-NART-Scor` | NART total score |
| | `{UID}-COG-X-RAV-T1Sc` | RAVLT Trial 1 |
| | `{UID}-COG-X-BVM-T1Sc` | BVMT Trial 1 |
| **VR Questions** | `{UID}-RVR-T{test}-{paradigm}-{domain}-{item}-{details}-{measure}` | VR data |

**CRITICAL:** Tags use DASHES throughout (e.g., `RPM-Scor` NOT `RPM_Scor`)

### VR Tag Components

| Component | Options | Example |
|-----------|---------|---------|
| **{test}** | 1, 2, 3, 4 | T1, T2, T3, T4 |
| **{paradigm}** | RFR, IFR, TCR, ICR, RRE, IRE | IFR (Items Free Recall) |
| **{domain}** | N, L, U, D, O | N (What/Name) |
| **{item}** | i1CM-i6IC, OBJ1-7, WEAT, TSK1-7 | i1CM (Item 1 Common) |
| **{details}** | n{order}s{start}f{finish} | n3s2f1 (3rd picked, from loc 2, to loc 1) |
| **{measure}** | ANS, CON | ANS (Accuracy), CON (Confidence) |

**Tip:** Use `extract_vr_tags()` to handle wildcards automatically (no need to know item details).

---

## Function Decision Tree

**"Which function should I use?"**

### 1. Single variable from master.xlsx
→ Use **`extract_tag()`**

### 2. Multiple variables from master.xlsx
→ Use **`extract_tags()`**

### 3. VR data across multiple tests
→ Use **`extract_vr_tags()`**

### 4. Computed cognitive scores (e.g., RAVLT_Total)
→ Use **`extract_cognitive_scores()`**

### 5. Previous RQ output file
→ Use **`load_rq_output()`**

### 6. Multiple data sources (master + RQ outputs + computed)
→ Use **`combine_data_sources()`**

### 7. Check if extracted data is valid
→ Use **`validate_extraction()`**

---

## Testing

All functions are covered by unit tests using **real master.xlsx data**.

**Run tests:**
```powershell
# Run all data extraction tests
poetry run pytest tests/test_data_extraction.py -v

# Run specific test class
poetry run pytest tests/test_data_extraction.py::TestExtractTag -v

# Run with coverage
poetry run pytest tests/test_data_extraction.py --cov=data --cov-report=html
```

**Test Coverage:**
- ✅ `TestExtractTag` (4 tests) - Single tag extraction
- ✅ `TestExtractTags` (1 test) - Multi-tag extraction
- ✅ `TestValidateExtraction` (2 tests) - Validation
- ✅ `TestLoadRQOutput` (2 tests) - Load previous RQ
- ✅ `TestExtractVRTags` (2 tests) - VR wildcards
- ✅ `TestExtractCognitiveScores` (1 test) - Computed scores
- ✅ `TestCombineDataSources` (2 tests) - Merge sources

**Total:** 14/14 tests passing (100%)

---

## Related Documentation

- **Tag System Details:** `docs/data_structure.md`
- **Cognitive Test Scoring:** `docs/cognitive_tests.md`
- **Legacy Variables System (DEPRECATED):** `docs/variables_system.md`
- **Data-Prep Agent Plan:** `.context/data_prep_plan.md`
- **Test Code:** `tests/test_data_extraction.py`

---

## Changelog

### Version 2.0 (2025-01-05)
- ✅ Complete TDD rewrite from scratch
- ✅ Replaced variables.xlsx regex approach with direct tag extraction
- ✅ Added 8 functions: load_master, extract_tag, extract_tags, validate_extraction, extract_vr_tags, extract_cognitive_scores, load_rq_output, combine_data_sources
- ✅ Added ValidationError exception class
- ✅ 100% test coverage with real master.xlsx data
- ✅ Comprehensive docstrings for all functions

### Version 1.0 (Legacy)
- Original data.py using variables.xlsx regex system
- Known bugs: Empty results_list issue, hardcoded paths
- Archived to `_archive/legacy_code/data.py`

---

## Support

**Questions or Issues?**
1. Check function docstrings in `data/data.py`
2. Check related documentation (see above)
3. Review test examples in `tests/test_data_extraction.py`
4. Check `.context/decisions.md` for design rationale

**Found a Bug?**
- Run tests to confirm: `poetry run pytest tests/test_data_extraction.py -v`
- Check if tag spelling is correct (use exact dashes)
- Review validation error messages (they're detailed!)

---

**End of API Documentation**
