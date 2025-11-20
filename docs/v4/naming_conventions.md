# REMEMVR Naming Conventions

**Purpose:** Unified naming system for tools, functions, files, and documentation across 50 RQs
**Version:** 1.0
**Date:** 2025-11-22
**Status:** DRAFT (for user review)

---

## Design Principles

1. **Minimize Cognitive Load:** Names should be self-documenting and predictable
2. **Prevent Agent Confusion:** Clear verb-noun patterns with consistent grammar
3. **Enable Discovery:** Related functions cluster alphabetically
4. **Scale Across 50 RQs:** Patterns work for both common and rare operations
5. **Avoid Redundancy:** Module name should not repeat in function name

---

## Module Naming

### Pattern: `tools.<domain>`

**Current Modules (Approved):**
```
tools.analysis_irt      # IRT calibration and item analysis
tools.analysis_lmm      # Linear Mixed Models for trajectories
tools.plotting          # Visualization functions
tools.validation        # Data quality and statistical validation
tools.config            # Configuration management
```

**Future Modules (As Needed):**
```
tools.analysis_ctt      # Classical Test Theory (if needed)
tools.data              # Data extraction/transformation (separate from analysis)
tools.reporting         # Results summary and export
```

**Rules:**
- Use `analysis_X` for statistical methodologies (irt, lmm, ctt)
- Use singular nouns (plotting, validation, config)
- No abbreviations except standard stats terms (irt, lmm, ctt)

---

## Function Naming

### Core Pattern: `<verb>_<noun>_[<qualifier>]`

**Example:** `calibrate_irt_model` → verb=calibrate, noun=irt_model, qualifier=none

---

## Verb Taxonomy (Standardized)

### 1. **Data Operations**

| Verb | Meaning | Use When | Example |
|------|---------|----------|---------|
| `prepare` | Transform data for analysis | Converting formats, adding derived columns | `prepare_irt_data`, `prepare_lmm_data` |
| `extract` | Retrieve computed results | Getting parameters/scores from fitted models | `extract_theta_scores`, `extract_fixed_effects` |
| `merge` | Combine datasets | Joining tables | `merge_theta_with_tsvr` |
| `reshape` | Change data structure | Wide↔long, pivot | `reshape_wide_to_long` |
| `filter` | Subset data | Removing rows/columns | `filter_participants_by_age` |

### 2. **Model Operations**

| Verb | Meaning | Use When | Example |
|------|---------|----------|---------|
| `fit` | Estimate model parameters | Running statistical models | `fit_irt_model`, `fit_lmm_model` |
| `calibrate` | **Pipeline wrapper** for fit+extract | End-to-end model workflow | `calibrate_irt`, `calibrate_lmm` |
| `configure` | Build unfitted model | Creating model objects before fitting | `configure_irt_model`, `configure_candidate_models` |
| `compare` | Select best model | AIC/BIC comparison across candidates | `compare_models` |
| `score` | Predict from fitted model | Applying model to new data | `score_new_participants` |

### 3. **Analysis Operations**

| Verb | Meaning | Use When | Example |
|------|---------|----------|---------|
| `compute` | Calculate derived metric | Effect sizes, statistics | `compute_effect_sizes`, `compute_aic` |
| `test` | Run hypothesis test | Statistical tests | `test_normality`, `test_convergence` |
| `contrast` | Compare groups | Post-hoc pairwise comparisons | `contrast_domains`, `contrast_timepoints` |

### 4. **Validation Operations**

| Verb | Meaning | Use When | Example |
|------|---------|----------|---------|
| `validate` | Check correctness | Convergence, assumptions, data quality | `validate_irt_convergence`, `validate_lmm_residuals` |
| `check` | Simple existence test | File exists, column present | `check_missing_data`, `check_file_exists` |

### 5. **I/O Operations**

| Verb | Meaning | Use When | Example |
|------|---------|----------|---------|
| `load` | Read from disk | Loading files | `load_config`, `load_lineage` |
| `save` | Write to disk | Saving files | `save_lineage`, `save_plot_with_data` |
| `read` | Parse data | Reading specific format | `read_master_xlsx` |
| `write` | Create file | Writing specific format | `write_validation_report` |

### 6. **Visualization Operations**

| Verb | Meaning | Use When | Example |
|------|---------|----------|---------|
| `plot` | Create visualization | All plotting functions | `plot_trajectory`, `plot_diagnostics` |
| `render` | Generate complex multi-panel plot | Dashboard-style outputs | `render_results_dashboard` |

### 7. **Utility Operations**

| Verb | Meaning | Use When | Example |
|------|---------|----------|---------|
| `get` | Retrieve config/setting | Simple lookups | `get_config`, `get_path` |
| `set` | Modify config/setting | Changing settings | `set_plot_style` |
| `reset` | Clear state | Cache clearing | `reset_cache` |
| `setup` | Initialize system | One-time configuration | `setup_plot_style` |

---

## Noun Taxonomy (Standardized)

### 1. **Data Nouns**

| Noun | Meaning | Example |
|------|---------|---------|
| `data` | Generic dataframe | `prepare_irt_data` |
| `scores` | Ability estimates | `extract_theta_scores` |
| `parameters` | Model parameters | `extract_item_parameters` |
| `residuals` | Model residuals | `validate_lmm_residuals` |
| `predictions` | Model predictions | `extract_predictions` |

### 2. **Model Nouns**

| Noun | Meaning | Example |
|------|---------|---------|
| `model` | Statistical model object | `fit_irt_model` |
| `models` | Multiple models (comparison) | `compare_models` |
| `irt` | IRT-specific | `calibrate_irt` |
| `lmm` | LMM-specific | `calibrate_lmm` |
| `grm` | Graded Response Model | `calibrate_grm` |

### 3. **Analysis Nouns**

| Noun | Meaning | Example |
|------|---------|---------|
| `effects` | Fixed/random effects | `extract_fixed_effects` |
| `contrasts` | Post-hoc comparisons | `post_hoc_contrasts` |
| `effect_sizes` | Cohen's d, f², etc. | `compute_effect_sizes` |
| `convergence` | Model convergence | `validate_irt_convergence` |

### 4. **File Nouns**

| Noun | Meaning | Example |
|------|---------|---------|
| `config` | Configuration file | `load_config` |
| `lineage` | Provenance metadata | `save_lineage` |
| `report` | Validation/summary report | `generate_validation_report` |
| `log` | Execution log | `write_analysis_log` |

### 5. **Plot Nouns**

| Noun | Meaning | Example |
|------|---------|---------|
| `trajectory` | Longitudinal plot | `plot_trajectory` |
| `diagnostics` | Model diagnostic plots | `plot_diagnostics` |
| `histogram` | Distribution plot | `plot_histogram_by_group` |
| `heatmap` | Matrix visualization | `plot_correlation_heatmap` |

---

## Qualifiers (Optional Third Component)

**Pattern:** `<verb>_<noun>_<qualifier>`

**Use qualifiers to:**
1. Distinguish variants of same operation
2. Specify methodology
3. Indicate special handling

**Examples:**
```python
# Methodology qualifiers
fit_lmm_with_tsvr         # TSVR time variable (vs nominal days)
plot_trajectory_probability  # Probability scale (vs theta scale)

# Variant qualifiers
prepare_data_wide         # Wide format
prepare_data_long         # Long format

# Decision qualifiers
purify_items_d039         # Per Decision D039 (if multiple purification methods)
contrast_domains_bonferroni  # Bonferroni correction
```

---

## Anti-Patterns (AVOID)

### ❌ 1. Module-Function Redundancy
```python
# BAD
tools.config.get_config()      # "config" appears twice

# GOOD
tools.config.get()             # Module name implicit
tools.config.load()            # Or use different verb
```

**Exception:** When avoiding namespace collision with Python builtins:
```python
# OK (load is builtin)
tools.config.load_config()
```

### ❌ 2. Verb Inconsistency
```python
# BAD (mixing synonyms)
calibrate_irt()    # "calibrate" for IRT
fit_lmm()          # "fit" for LMM
run_ctt()          # "run" for CTT

# GOOD (consistent verb hierarchy)
calibrate_irt()    # Pipeline wrapper
calibrate_lmm()    # Pipeline wrapper
calibrate_ctt()    # Pipeline wrapper

fit_irt_model()    # Atomic operation
fit_lmm_model()    # Atomic operation
fit_ctt_model()    # Atomic operation
```

### ❌ 3. Noun Ambiguity
```python
# BAD
process_data()         # What kind of processing?
analyze_results()      # What kind of analysis?

# GOOD
prepare_irt_data()     # Clear: prepare for IRT
compute_effect_sizes() # Clear: calculate effect sizes
```

### ❌ 4. Abbreviation Overuse
```python
# BAD
calc_es()              # "calc" is informal, "es" is cryptic
ext_theta()            # Too terse

# GOOD
compute_effect_sizes() # Clear and professional
extract_theta_scores() # Clear and complete
```

### ❌ 5. Action vs Object Confusion
```python
# BAD
theta_to_probability() # Sounds like a converter, unclear if it modifies or returns

# GOOD
convert_theta_to_probability()  # Clear: returns converted values
plot_trajectory_probability()   # Clear: plots with conversion
```

---

## Hierarchy Conventions

### Pipeline vs Atomic Functions

**Pattern:** Pipeline wrappers use root verb, atomic helpers use specific verb

```python
# PIPELINE WRAPPER (calls multiple atomics)
calibrate_irt(df_long, groups, config)
  ↓ calls:
    prepare_irt_data()       # Atomic: data prep
    configure_irt_model()    # Atomic: model setup
    fit_irt_model()          # Atomic: estimation
    extract_theta_scores()   # Atomic: score extraction
    extract_item_parameters() # Atomic: parameter extraction

# PIPELINE WRAPPER (calls multiple atomics)
run_lmm_analysis(theta_scores, output_dir)
  ↓ calls:
    prepare_lmm_data()       # Atomic: data reshaping
    configure_candidate_models() # Atomic: model setup
    compare_models()         # Atomic: model selection
    extract_fixed_effects()  # Atomic: parameter extraction
```

**Rule:** Pipeline wrappers have shorter names (2 words), atomics have longer names (3+ words)

---

## File Naming Conventions

### Python Modules
```
tools/analysis_irt.py      # Lowercase, underscores
tools/analysis_lmm.py
tools/plotting.py
```

### Documentation
```
docs/tools_inventory.md     # Lowercase, underscores
docs/tools_catalog.md
docs/tools_status.csv
docs/v4/naming_conventions.md
```

### Configuration
```
config/plotting.yaml        # Lowercase, underscores
config/paths.yaml
config/irt_defaults.yaml
```

### RQ Files
```
results/ch5/rq1/
├── data/
│   ├── theta_scores.csv           # Lowercase, underscores
│   ├── item_parameters.csv
│   └── aic_comparison.csv
├── plots/
│   ├── trajectory_theta.png       # Descriptive suffixes
│   └── trajectory_probability.png
└── logs/
    └── analysis_execution.log
```

---

## Documentation Naming

### Tools Documentation
```
docs/tools_inventory.md     # Full API reference (rq_tools reads)
docs/tools_catalog.md       # Lightweight catalog (rq_planner reads)
docs/tools_status.csv       # Migration tracking (we read)
docs/v4/tool_audit.md       # Comprehensive audit (reference)
```

### Template Files
```
docs/v4/templates/
├── concept.md              # RQ concept template
├── plan.md                 # Analysis plan template
├── tools.md                # Tool specification template
├── analysis.md             # Analysis recipe template
└── results.md              # Results summary template
```

---

## Decision-Specific Functions

**Pattern:** Standard name + decision reference in docstring

```python
def purify_items(df_items, a_threshold=0.4, b_threshold=3.0):
    """
    2-pass IRT item purification.

    Implements Decision D039: Exclude items where discrimination < 0.4
    OR |difficulty| > 3.0.

    ...
    """
```

**Alternative (if multiple methods exist):**
```python
def purify_items_d039(df_items):
    """Decision D039: 2-pass purification with a<0.4, |b|>3.0 thresholds."""

def purify_items_rasch(df_items):
    """Alternative: Rasch-based purification (infit/outfit)."""
```

---

## Consistency Checklist

Before adding a new function, verify:

- [ ] **Verb is from approved taxonomy** (or propose new verb with rationale)
- [ ] **Noun is from approved taxonomy** (or propose new noun with rationale)
- [ ] **No module-function redundancy** (unless avoiding builtin collision)
- [ ] **Function name is 2-3 words** (pipelines=2, atomics=3)
- [ ] **Alphabetical clustering works** (related functions sort together)
- [ ] **Pattern matches similar functions** (e.g., all `extract_X` follow same pattern)
- [ ] **Docstring includes Decision reference** (if implementing project decision)

---

## Proposed Renames (For Discussion)

### Current Issues to Fix

| Current Name | Issue | Proposed Name | Rationale |
|--------------|-------|---------------|-----------|
| `get_config` | Module-function redundancy | `load` or `fetch` | Avoid "config.get_config" |
| `get_path` | Ambiguous verb | `resolve_path` | "resolve" is standard for path operations |
| `theta_to_probability` | Unclear action | `convert_theta_to_probability` | Explicit converter |
| `post_hoc_contrasts` | Medical jargon | `contrast_pairwise` | Clearer intent |
| `setup_plot_style` | Inconsistent with `set_` pattern | `set_plot_style` | Match other setters |

### New Functions (If Needed)

When adding functions for new analyses:

| Need | Proposed Name | Pattern |
|------|---------------|---------|
| CTT scoring | `compute_ctt_scores` | `compute_<method>_scores` |
| Reliability | `compute_cronbach_alpha` | `compute_<metric>` |
| Factor analysis | `fit_efa_model` | `fit_<method>_model` |
| Clustering | `fit_kmeans_model` | `fit_<method>_model` |

---

## Summary: Quick Reference

### Standard Patterns

```python
# DATA PREP
prepare_<method>_data()          # Convert to analysis format
extract_<result>()               # Get results from model
merge_<dataset1>_with_<dataset2>() # Combine datasets

# MODEL FITTING
calibrate_<method>()             # Full pipeline wrapper
configure_<method>_model()       # Build unfitted model
fit_<method>_model()             # Estimate parameters
compare_models()                 # Select best model

# ANALYSIS
compute_<metric>()               # Calculate statistics
validate_<aspect>()              # Check quality
contrast_<groups>()              # Compare groups

# VISUALIZATION
plot_<type>()                    # Create plot
render_<dashboard>()             # Multi-panel output

# I/O
load_<resource>()                # Read from disk
save_<resource>()                # Write to disk

# UTILITIES
get_<config>()                   # Retrieve setting
set_<config>()                   # Modify setting
reset_<state>()                  # Clear state
```

---

## Agent Communication

**For rq_planner:**
- Use **pipeline wrappers** in plans (e.g., `calibrate_irt`, `run_lmm_analysis`)
- Avoid mentioning atomic helpers (agent chooses internally)

**For rq_tools:**
- Map pipeline → atomics (e.g., `calibrate_irt` → `prepare_irt_data` + `fit_irt_model` + ...)
- Specify exact atomic functions in 3_tools.yaml

**For rq_analysis:**
- Use **atomic functions** in 4_analysis.yaml (step-by-step code)
- Include full module path (e.g., `tools.analysis_irt.fit_irt_model`)

**For g_code:**
- Copy-paste atomic function calls from 4_analysis.yaml
- Zero improvisation on function names

---

## Version History

- **v1.0 (2025-11-22):** Initial draft for user review
- **Future:** Update after user feedback + add examples from first 5 RQs

---

**Status:** DRAFT - Awaiting user approval before application

**Next Steps:**
1. User reviews and approves/modifies conventions
2. Apply renames to existing 51 functions (if approved)
3. Update tools_catalog.md with approved patterns
4. Document examples from RQ 5.1 testing
