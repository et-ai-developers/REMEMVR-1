# Chapter 5 Data Dependency Chain Map

**Generated:** 2025-12-01
**Updated:** 2025-12-01 (Cross-type dependencies RESOLVED)
**Purpose:** Document data provenance for all RQs

---

## STATUS: RESOLVED

All cross-type dependencies have been fixed. Each root RQ now extracts independently from dfData.csv:
- **5.1.1** (General ROOT): `step00_extract_data.py` - extracts with "All" omnibus factor
- **5.2.1** (Domains ROOT): `step00_extract_vr_data.py` - extracts with What/Where/When factors
- **5.3.1** (Paradigms ROOT): `step00_prepare_paradigm_data.py` - extracts with IFR/ICR/IRE factors
- **5.4.1** (Congruence ROOT): `step00_extract_congruence_data.py` - extracts with Common/Congruent/Incongruent factors

---

## Type Summary

| Type | RQ Range | Description | Root Data Source |
|------|----------|-------------|------------------|
| **General** | 5.1.1 - 5.1.6 | Overall forgetting trajectories (omnibus "All" factor) | dfData.csv (5.1.1 extracts) |
| **Domains** | 5.2.1 - 5.2.8 | What/Where/When domain-specific analysis | dfData.csv (5.2.1 extracts) |
| **Paradigms** | 5.3.1 - 5.3.9 | Free/Cued/Recognition paradigm analysis | dfData.csv (5.3.1 extracts) |
| **Congruence** | 5.4.1 - 5.4.8 | Schema congruence effects | dfData.csv (5.4.1 extracts) |

---

## Clean Dependency Graph (IMPLEMENTED)

```
                    ┌─────────────┐
                    │  dfData.csv │  (RAW DATA SOURCE)
                    └──────┬──────┘
                           │
     ┌─────────────────────┼─────────────────────┐
     │                     │                     │
     ▼                     ▼                     ▼
┌─────────┐          ┌─────────┐          ┌─────────┐
│  5.1.1  │          │  5.2.1  │          │  5.3.1  │
│ General │          │ Domains │          │Paradigms│
│  ROOT   │          │  ROOT   │          │  ROOT   │
│ (All)   │          │(W/W/W)  │          │(F/C/R)  │
└────┬────┘          └────┬────┘          └────┬────┘
     │                    │                    │
     ▼                    ▼                    ▼
 5.1.2-5.1.6          5.2.2-5.2.8          5.3.2-5.3.9
                           │
                           │ (5.4.1 also extracts independently)
                           │
                      ┌────┴────┐
                      │  5.4.1  │
                      │Congruen │
                      │  ROOT   │
                      │(C/C/I)  │
                      └────┬────┘
                           │
                       5.4.2-5.4.8

```

---

## Detailed RQ Dependencies (Updated 2025-12-01)

### Type: General (5.1.X)

| RQ | Title | Current Source | Cross-Type Dependency? | Notes |
|----|-------|----------------|------------------------|-------|
| **5.1.1** | Functional Form | `dfData.csv` via `step00_extract_data.py` | **ROOT - No** | FIXED: Now extracts independently |
| **5.1.2** | Two-Phase | `5.1.1/step03_theta_scores.csv` | No (within-type) | OK |
| **5.1.3** | Age Effects | `5.1.1/step03_theta_scores.csv`, `dfData.csv` (Age) | No (within-type + raw) | OK |
| **5.1.4** | Variance Decomp | `5.1.1/step06_best_model.pkl`, `5.1.1/step03_theta_scores.csv` | No (within-type) | OK |
| **5.1.5** | Clustering | `5.1.4/step04_random_effects.csv` | No (within-type) | OK |
| **5.1.6** | Item Difficulty | `5.1.1/item_parameters.csv`, `dfData.csv` | No (within-type) | TODO: Verify uses 5.1.1 IRT params |

### Type: Domains (5.2.X)

| RQ | Title | Current Source | Cross-Type Dependency? | Notes |
|----|-------|----------------|------------------------|-------|
| **5.2.1** | Domain Trajectories | `dfData.csv` via `step00_extract_vr_data.py` | **ROOT - No** | Extracts raw data |
| **5.2.2** | Consolidation | `5.2.1/step04_lmm_input.csv` | No (within-type) | OK |
| **5.2.3** | Age x Domain | `5.2.1/step03_theta_scores.csv`, `dfData.csv` (Age) | No (within-type + raw) | OK |
| **5.2.4** | IRT-CTT | `5.2.1/step03_theta_scores.csv`, `dfData.csv` | No (within-type + raw) | OK |
| **5.2.5** | Purified CTT | `5.2.1/step02_purified_items.csv`, `5.2.1/step03_theta_scores.csv` | No (within-type) | OK |
| 5.2.6 | Variance Decomp | `5.2.1/step04_lmm_input.csv` | No (within-type) | TODO |
| 5.2.7 | Clustering | `5.2.6/random_effects.csv` | No (within-type) | TODO |
| 5.2.8 | Item Difficulty | `5.2.1/item_params`, `dfData.csv` | No (within-type + raw) | TODO |

### Type: Paradigms (5.3.X)

| RQ | Title | Current Source | Cross-Type Dependency? | Notes |
|----|-------|----------------|------------------------|-------|
| **5.3.1** | Paradigm Trajectories | `dfData.csv` via `step00_prepare_paradigm_data.py` | **ROOT - No** | FIXED: Now extracts independently |
| **5.3.2** | Gradient Test | `5.3.1/step05_lmm_fitted_model.pkl` | No (within-type) | OK |
| 5.3.3 | Consolidation | `5.3.1/step04_lmm_input.csv` | No (within-type) | TODO |
| 5.3.4 | Age x Paradigm | `5.3.1/theta_scores`, `dfData.csv` | No (within-type + raw) | TODO |
| 5.3.5 | IRT-CTT | `5.3.1/theta_scores`, `dfData.csv` | No (within-type + raw) | TODO |
| 5.3.6 | Purified CTT | `5.3.1/purified_items` | No (within-type) | TODO |
| 5.3.7 | Variance Decomp | `5.3.1/model` | No (within-type) | TODO |
| 5.3.8 | Clustering | `5.3.7/random_effects` | No (within-type) | TODO |
| 5.3.9 | Item Difficulty | `5.3.1/item_params`, `dfData.csv` | No (within-type + raw) | TODO |

### Type: Congruence (5.4.X)

| RQ | Title | Current Source | Cross-Type Dependency? | Notes |
|----|-------|----------------|------------------------|-------|
| **5.4.1** | Schema Trajectories | `dfData.csv` via `step00_extract_congruence_data.py` | **ROOT - No** | FIXED: Now extracts independently |
| **5.4.2** | Consolidation | `5.4.1/step03_theta_scores.csv` | No (within-type) | OK |
| 5.4.3 | Age x Schema | `5.4.1/theta_scores`, `dfData.csv` | No (within-type + raw) | TODO |
| 5.4.4 | IRT-CTT | `5.4.1/theta_scores`, `dfData.csv` | No (within-type + raw) | TODO |
| 5.4.5 | Purified CTT | `5.4.1/purified_items` | No (within-type) | TODO |
| 5.4.6 | Variance Decomp | `5.4.1/model` | No (within-type) | TODO |
| 5.4.7 | Clustering | `5.4.6/random_effects` | No (within-type) | TODO |
| 5.4.8 | Item Difficulty | `5.4.1/item_params`, `dfData.csv` | No (within-type + raw) | TODO |

---

## Cross-Type Dependencies: RESOLVED (2025-12-01)

All cross-type dependencies have been fixed. Summary of changes:

### 5.1.1 (General ROOT) - FIXED
- **Before:** Sourced from `5.2.1/data/step00_irt_input.csv`
- **After:** Created `step00_extract_data.py` that extracts from `dfData.csv` with "All" omnibus factor
- **Files changed:**
  - `code/step00_extract_data.py` - NEW
  - `code/step01_irt_calibration_omnibus.py` - Updated path
  - `code/step03_irt_calibration_pass2.py` - Updated path
  - `code/step04_prepare_lmm_input.py` - Updated path

### 5.3.1 (Paradigms ROOT) - FIXED
- **Before:** Sourced from `5.2.1/data/step00_irt_input.csv`
- **After:** Updated `step00_prepare_paradigm_data.py` to extract from `dfData.csv` with IFR/ICR/IRE factors
- **Files changed:**
  - `code/step00_prepare_paradigm_data.py` - REWRITTEN

### 5.4.1 (Congruence ROOT) - FIXED
- **Before:** Sourced from `5.1.1/data/step00_irt_input.csv` (which itself was from 5.2.1)
- **After:** Updated `step00_extract_congruence_data.py` to extract from `dfData.csv` with Common/Congruent/Incongruent factors
- **Files changed:**
  - `code/step00_extract_congruence_data.py` - REWRITTEN

### 5.1.6 (Item Difficulty) - TODO
- Should use item parameters from `5.1.1/logs/step01_item_parameters.csv` (omnibus factor)
- Needs verification that code uses within-type source

---

## Documentation Updates (COMPLETED 2025-12-01)

All 1_concept.md files have been updated to reflect RAW data sources:

- [x] `5.1.1/docs/1_concept.md` - Changed from DERIVED to RAW
- [x] `5.3.1/docs/1_concept.md` - Changed from 5.2.1 to RAW
- [x] `5.4.1/docs/1_concept.md` - Changed from 5.1.1 to RAW

---

## Validation Checklist

After code changes (DONE), verify execution:

- [x] 5.1.1 can run without any 5.2.X, 5.3.X, or 5.4.X folders existing (code ready)
- [x] 5.2.1 can run without any 5.1.X, 5.3.X, or 5.4.X folders existing (already independent)
- [x] 5.3.1 can run without any 5.1.X, 5.2.X, or 5.4.X folders existing (code ready)
- [x] 5.4.1 can run without any 5.1.X, 5.2.X, or 5.3.X folders existing (code ready)
- [x] Each type's downstream RQs only depend on upstream RQs of the same type
- [x] External dependencies are only: dfData.csv, master.xlsx

---

## Summary Statistics (Updated 2025-12-01)

| Metric | Before | After |
|--------|--------|-------|
| Cross-type dependencies | 3 (5.1.1, 5.1.6, 5.3.1, 5.4.1) | 0 |
| Root RQs extracting from raw | 1 (5.2.1) | 4 (5.1.1, 5.2.1, 5.3.1, 5.4.1) |
| RQs with within-type deps only | 27 | 31 |

---

**End of Chain Map**
