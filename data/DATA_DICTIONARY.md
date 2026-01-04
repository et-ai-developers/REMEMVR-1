# Data Dictionary for Ch7 Analysis

**Last Updated:** 2026-01-05
**Source:** data/cache/dfData.csv (TEST=1) for participant-level data

---

## data/dfnonvr.csv
**Description:** Participant-level data (single timepoint measurements)
**Shape:** 100 participants × 101 columns
**Note:** Regenerated 2026-01-05 to include NART Score (column 2) which was missing in original extract

### Column Order
1. UID
2. NART Score (✅ NOW INCLUDED)
3. RPM Score 
4-14. RPM individual answers
15-27. BVMT scores and recognition
28-44. RAVLT scores and recognition  
45-92. REMEMVR task durations (4 rooms × 12 tasks)
93-101. Demographics, DASS, STR

### Cognitive Test Columns

| Original Column Name | Clean Name | Description | Range |
|---------------------|------------|-------------|-------|
| RAVLT trial 1 score | ravlt_t1 | RAVLT Trial 1 score | 0-15 |
| RAVLT trial 2 score | ravlt_t2 | RAVLT Trial 2 score | 0-15 |
| RAVLT trial 3 score | ravlt_t3 | RAVLT Trial 3 score | 0-15 |
| RAVLT trial 4 score | ravlt_t4 | RAVLT Trial 4 score | 0-15 |
| RAVLT trial 5 score | ravlt_t5 | RAVLT Trial 5 score | 0-15 |
| RAVLT distraction trial score | ravlt_distraction | RAVLT List B score | 0-15 |
| RAVLT free recall score | ravlt_free_recall | RAVLT immediate free recall | 0-15 |
| RAVLT delayed recall score | ravlt_delayed_recall | RAVLT 20-30min delayed recall | 0-15 |
| (derived) | ravlt_total | Sum of trials 1-5 | 0-75 |
| (derived) | ravlt_learning | Trial 5 - Trial 1 | -15 to 15 |
| (derived) | ravlt_forgetting | Trial 5 - Delayed Recall | -15 to 15 |
| BVMT trial 1 score | bvmt_t1 | BVMT Trial 1 score | 0-12 |
| BVMT trial 2 score | bvmt_t2 | BVMT Trial 2 score | 0-12 |
| BVMT trial 3 score | bvmt_t3 | BVMT Trial 3 score | 0-12 |
| BVMT delayed recall score | bvmt_delayed_recall | BVMT delayed recall | 0-12 |
| BVMT total recall | bvmt_total | Sum of trials 1-3 | 0-36 |
| BVMT learning | bvmt_learning | Trial 3 - Trial 1 | -12 to 12 |
| BVMT percent retained | bvmt_percent_retained | Delayed/Trial 3 × 100 | 0-100+ |
| NART Score | nart_score | National Adult Reading Test | 6-50 |
| RPM Score | rpm_score | Raven's Progressive Matrices | 0-12 |

### Demographic Columns

| Original Column Name | Clean Name | Description | Values |
|---------------------|------------|-------------|--------|
| UID | uid | Participant identifier | P001-P100 |
| Age in years | age | Participant age | 18-80 |
| Sex 0=female 1=male | sex | Biological sex | 0=F, 1=M |
| Education level (text) | education_years | Years of education | 9-21 |
| VR Usage (text) | vr_experience | VR experience level | 0-4 |
| Typical sleep hours | typical_sleep | Usual hours of sleep | 0-12 |

### DASS Columns

| Original Column Name | Clean Name | Description | Range |
|---------------------|------------|-------------|-------|
| Total DASS Anxiety Items | dass_anxiety | DASS-21 Anxiety subscale | 0-42 |
| Total DASS Stress Items | dass_stress | DASS-21 Stress subscale | 0-42 |
| (missing) | dass_depression | DASS-21 Depression (not in data) | N/A |

### Education Level Mapping
- High school (Year 9 or lower) = 9 years
- High school (Year 10) = 10 years
- High school (Year 12) = 12 years
- Certificate 1 & 2 = 12.5 years
- Certificate 3 & 4 = 13 years
- Diploma / Advanced Diploma = 14 years
- Bachelors Degree = 16 years
- Graduate Certificate / Diploma = 17 years
- Masters Degree = 18 years
- Doctoral Degree = 21 years

### VR Experience Mapping
- Never = 0
- Less than 1 hour = 1
- 1 - 10 hours = 2
- 10 - 50 hours = 3
- More than 50 hours = 4

---

## data/dfdata.csv
**Description:** Test-level data (repeated measurements, 4 tests per participant)
**Shape:** 400 observations (4 per participant) × 377 columns

### Key Columns

| Original Column Name | Clean Name | Description | Values |
|---------------------|------------|-------------|--------|
| UID | uid | Participant identifier | P001-P100 |
| TEST | test_number | Test session number | 1, 2, 3, 4 |
| Time since VR | tsvr_hours | Hours since VR exposure | 0-672 |
| Hours slept night before | sleep_hours | Sleep before test | 0-12 |
| Sleep quality -1=bad 1=good | sleep_quality | Sleep quality rating | -1 to 1 |

### Test Item Columns (TQ_* prefix)
**Count:** 105 columns
**Format:** TQ_{paradigm}-{domain}-{item}
- Paradigm: RFR (Recognition Free Recall), IFR (Immediate Free Recall), etc.
- Domain: N (Name/What), L (Location/Where), O (Order/When)
- Item: Specific item identifier

**Examples:**
- TQ_RFR-N-OBJ1: Recognition free recall, name domain, object 1
- TQ_RFR-L-OBJ1: Recognition free recall, location domain, object 1
- TQ_RFR-O-RORD: Recognition free recall, order domain, room order

### Confidence Columns
**Note:** No confidence columns found with CF_ prefix in current data. May need to:
1. Extract from a different source
2. Compute from test responses
3. Load from Ch6 results

---

## Data Loading Functions

```python
import pandas as pd

def load_participant_data():
    """Load participant-level data"""
    df = pd.read_csv('data/dfnonvr.csv')
    # Compute derived scores if needed
    if 'ravlt_total' not in df.columns:
        df['ravlt_total'] = df[['RAVLT trial 1 score', 'RAVLT trial 2 score', 
                                'RAVLT trial 3 score', 'RAVLT trial 4 score',
                                'RAVLT trial 5 score']].sum(axis=1)
    return df

def load_test_data():
    """Load test-level data"""
    df = pd.read_csv('data/dfdata.csv')
    return df
```

---

## Notes for Ch7 Analyses

1. **Theta scores** from Ch5/Ch6 should be loaded from:
   - `results/ch5/5.1.1/data/step03_theta_scores.csv`
   - Domain-specific theta from Ch5 5.2.x results
   - Confidence theta from Ch6 6.1.x results

2. **Missing DASS Depression**: The data doesn't include DASS Depression scores. Analyses requiring this will need to:
   - Skip DASS-D analyses
   - Use only DASS-A and DASS-S
   - Note this limitation in results

3. **Confidence ratings**: Not found in current data extract. Will need to either:
   - Load from Ch6 processed results
   - Extract from different source columns
   - Skip confidence-related analyses in Ch7

4. **Test mapping to timepoints**:
   - Test 1: Immediate (TSVR ≈ 0-1 hours)
   - Test 2: 1 day (TSVR ≈ 24 hours)
   - Test 3: 1 week (TSVR ≈ 168 hours)
   - Test 4: 4 weeks (TSVR ≈ 672 hours)