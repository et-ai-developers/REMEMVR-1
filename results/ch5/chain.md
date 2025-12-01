# Chapter 5 Data Dependency Chain Map

**Generated:** 2025-12-01
**Purpose:** Document data provenance for all RQs to identify cross-type dependencies that need resolution

---

## Overview

This document maps data flow between RQs to identify:
1. Which RQs extract from raw data (dfData.csv)
2. Which RQs depend on other RQs
3. **CRITICAL:** Cross-type dependencies (e.g., 5.1.X depending on 5.2.X)

---

## Type Summary

| Type | RQ Range | Description | Root Data Source |
|------|----------|-------------|------------------|
| **General** | 5.1.1 - 5.1.6 | Overall forgetting trajectories (omnibus "All" factor) | Should be: dfData.csv |
| **Domains** | 5.2.1 - 5.2.8 | What/Where/When domain-specific analysis | dfData.csv (5.2.1 extracts) |
| **Paradigms** | 5.3.1 - 5.3.9 | Free/Cued/Recognition paradigm analysis | Should be: dfData.csv |
| **Congruence** | 5.4.1 - 5.4.8 | Schema congruence effects | Should be: dfData.csv |

---

## Current Dependency Graph

```
                    ┌─────────────┐
                    │  dfData.csv │  (RAW DATA SOURCE)
                    │  master.xlsx│
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
      ┌────────┐      ┌────────┐      ┌────────┐
      │ 5.2.1  │      │ 5.3.1  │      │ 5.4.1  │
      │Domains │      │Paradigm│      │Congruen│
      │ ROOT   │      │ ROOT   │      │  ROOT  │
      └───┬────┘      └───┬────┘      └───┬────┘
          │               │               │
    ┌─────┼─────┐   ┌─────┼─────┐   ┌─────┼─────┐
    │     │     │   │     │     │   │     │     │
    ▼     ▼     ▼   ▼     ▼     ▼   ▼     ▼     ▼
  5.2.2 5.2.3 5.2.4 5.3.2 5.3.3 5.3.4 5.4.2 5.4.3 5.4.4
  5.2.5 5.2.6 5.2.7 5.3.5 5.3.6 5.3.7 5.4.5 5.4.6 5.4.7
  5.2.8       5.2.8 5.3.8 5.3.9     5.4.8

                    ┌────────────────────┐
                    │      5.1.1         │
                    │  CROSS-DEPENDENCY  │
                    │  Sources: 5.2.1    │ <-- PROBLEM!
                    └─────────┬──────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
                  5.1.2     5.1.3     5.1.4
                    │                   │
                    │                   ▼
                    │                 5.1.5
                    │
                  5.1.6 <-- Also sources 5.2.1 item params!
```

---

## Detailed RQ Dependencies

### Type: General (5.1.X)

| RQ | Title | Current Source | Cross-Type Dependency? | Notes |
|----|-------|----------------|------------------------|-------|
| **5.1.1** | Functional Form | `5.2.1/step00_irt_input.csv`, `5.2.1/step00_tsvr_mapping.csv` | **YES - CRITICAL** | Needs own extraction from dfData |
| **5.1.2** | Two-Phase | `5.1.1/step03_theta_scores.csv` | No (within-type) | OK |
| **5.1.3** | Age Effects | `5.1.1/step03_theta_scores.csv`, `dfData.csv` (Age) | No (within-type + raw) | OK |
| **5.1.4** | Variance Decomp | `5.1.1/step06_best_model.pkl`, `5.1.1/step03_theta_scores.csv` | No (within-type) | OK |
| **5.1.5** | Clustering | `5.1.4/step04_random_effects.csv` | No (within-type) | OK |
| **5.1.6** | Item Difficulty | `5.2.1/step03_item_parameters.csv`, `dfData.csv` | **YES - CRITICAL** | Needs own IRT or uses omnibus params |

### Type: Domains (5.2.X)

| RQ | Title | Current Source | Cross-Type Dependency? | Notes |
|----|-------|----------------|------------------------|-------|
| **5.2.1** | Domain Trajectories | `dfData.csv` (extracts) | **ROOT - No** | Extracts raw data |
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
| **5.3.1** | Paradigm Trajectories | `5.2.1 data filtered` (per TSV) | **AMBIGUOUS** | Says "RQ 5.2.1 data filtered" - needs clarification |
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
| **5.4.1** | Schema Trajectories | `5.2.1 data filtered` (per TSV) | **AMBIGUOUS** | Says "RQ 5.2.1 data filtered" - needs clarification |
| **5.4.2** | Consolidation | `5.4.1/step03_theta_scores.csv` | No (within-type) | OK |
| 5.4.3 | Age x Schema | `5.4.1/theta_scores`, `dfData.csv` | No (within-type + raw) | TODO |
| 5.4.4 | IRT-CTT | `5.4.1/theta_scores`, `dfData.csv` | No (within-type + raw) | TODO |
| 5.4.5 | Purified CTT | `5.4.1/purified_items` | No (within-type) | TODO |
| 5.4.6 | Variance Decomp | `5.4.1/model` | No (within-type) | TODO |
| 5.4.7 | Clustering | `5.4.6/random_effects` | No (within-type) | TODO |
| 5.4.8 | Item Difficulty | `5.4.1/item_params`, `dfData.csv` | No (within-type + raw) | TODO |

---

## Cross-Type Dependencies (PROBLEMS)

### CRITICAL: 5.1.1 depends on 5.2.1

**Current State:**
```
5.1.1 (General: Functional Form)
  └── Sources from: 5.2.1/data/step00_irt_input.csv
  └── Sources from: 5.2.1/data/step00_tsvr_mapping.csv
```

**Problem:** General RQs should be independent of Domain RQs. Currently 5.1.1 cannot run without 5.2.1 completing Step 0.

**Solution:** 5.1.1 should have its own Step 0 that extracts from dfData.csv with omnibus "All" factor configuration.

---

### CRITICAL: 5.1.6 depends on 5.2.1

**Current State:**
```
5.1.6 (General: Item Difficulty Interaction)
  └── Sources from: 5.2.1/data/step03_item_parameters.csv
```

**Problem:** Uses domain-specific IRT item parameters for a general/omnibus analysis.

**Solution Options:**
1. 5.1.6 uses item parameters from 5.1.1's IRT calibration (omnibus factor)
2. 5.1.6 does its own IRT calibration with omnibus factor

---

### AMBIGUOUS: 5.3.1 and 5.4.1

**Current State (from TSV):**
```
5.3.1: "Source: RQ 5.2.1 data filtered to paradigm items"
5.4.1: "Source: RQ 5.2.1 data filtered to interactive paradigms"
```

**Interpretation:** These may mean:
- A) Use 5.2.1's extracted data and filter it (cross-dependency)
- B) Use same extraction logic as 5.2.1 but filter differently (independent)

**Recommendation:** Option B - each root RQ (5.2.1, 5.3.1, 5.4.1) should extract from dfData.csv independently with their own Q-matrix configuration.

---

## Proposed Clean Dependency Structure

### Goal: Each Type is Self-Contained

```
                    ┌─────────────┐
                    │  dfData.csv │
                    │  master.xlsx│
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

## Required Changes

### Phase 1: Add Step 0 to 5.1.1

**Files to modify:**
- `results/ch5/5.1.1/docs/1_concept.md` - Change data source from DERIVED to RAW
- `results/ch5/5.1.1/docs/2_plan.md` - Add Step 0 extraction
- `results/ch5/5.1.1/docs/4_analysis.yaml` - Add Step 0 specification
- `results/ch5/5.1.1/code/step00_extract_data.py` - CREATE NEW
- Update all subsequent steps to use `data/step00_*.csv` instead of `5.2.1/data/step00_*.csv`

**Data to extract (Step 0):**
```
Input: data/cache/dfData.csv
Output:
  - data/step00_irt_input.csv (400 rows, composite_ID + all items)
  - data/step00_tsvr_mapping.csv (400 rows, composite_ID + TSVR_hours)
  - data/step00_q_matrix.csv (all items -> "All" factor)
```

### Phase 2: Fix 5.1.6

**Options:**
1. Source item_parameters from 5.1.1's Pass 1 or Pass 2 IRT output
2. If 5.1.1 doesn't produce item_parameters.csv, add that output

### Phase 3: Clarify 5.3.1 and 5.4.1

**Ensure each extracts independently from dfData.csv:**
- 5.3.1: Extract with paradigm Q-matrix (IFR/ICR/IRE factors)
- 5.4.1: Extract with congruence Q-matrix (Common/Congruent/Incongruent factors)

---

## Validation Checklist

After changes, verify:

- [ ] 5.1.1 can run without any 5.2.X, 5.3.X, or 5.4.X folders existing
- [ ] 5.2.1 can run without any 5.1.X, 5.3.X, or 5.4.X folders existing
- [ ] 5.3.1 can run without any 5.1.X, 5.2.X, or 5.4.X folders existing
- [ ] 5.4.1 can run without any 5.1.X, 5.2.X, or 5.3.X folders existing
- [ ] Each type's downstream RQs only depend on upstream RQs of the same type
- [ ] External dependencies are only: dfData.csv, master.xlsx

---

## Summary Statistics

| Metric | Current | Target |
|--------|---------|--------|
| Cross-type dependencies | 3 (5.1.1, 5.1.6, ambiguous 5.3.1/5.4.1) | 0 |
| Root RQs extracting from raw | 1 (5.2.1) | 4 (5.1.1, 5.2.1, 5.3.1, 5.4.1) |
| RQs with within-type deps only | 28 | 31 |

---

**End of Chain Map**
