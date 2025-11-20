# REMEMVR Tools Naming System

**Purpose:** Formulaic naming patterns for all tools/ functions
**Version:** 2.0
**Date:** 2025-11-22
**Status:** Active

---

## Core Principle

**Every function name must be self-documenting using a strict formulaic pattern.**

Function names follow ONE of 8 core patterns based on function purpose. No exceptions.

---

## The 8 Formulaic Patterns

### 1. **CONVERT** - Transform data from one format to another
**Pattern:** `convert_<source>_to_<target>()`

```python
# Data format transformations
convert_wide_to_long()              # Wide → long format
convert_long_to_wide()              # Long → wide format
convert_theta_to_probability()      # IRT theta → probability scale
convert_hours_to_days()             # Time unit conversion
```

**When to use:** Any A→B transformation where input/output types differ
**Key feature:** Both source and target are explicit in name

---

### 2. **LOAD** - Read data from storage
**Pattern:** `load_<noun>_from_<source>()`

```python
# Configuration loading
load_config_from_yaml()             # Read config from YAML file
load_config_from_file()             # Read config from file path
load_data_from_csv()                # Read CSV data
load_lineage_from_file()            # Read provenance metadata
```

**When to use:** Any file I/O that reads from disk
**Key feature:** Source (file type or location) is always specified

---

### 3. **RESOLVE** - Compute or derive values
**Pattern:** `resolve_<noun>_from_<source>()`

```python
# Configuration lookups with computation
resolve_path_from_config()          # Compute path using config + project root
resolve_irt_params_from_config()    # Extract IRT parameters from config
resolve_timestamp_from_log()        # Parse timestamp from log file
```

**When to use:** When function computes/derives rather than just retrieves
**Key feature:** Implies computation/logic, not just simple lookup

---

### 4. **SET** - Configure or modify state
**Pattern:** `set_<noun>_<qualifier>()`

```python
# State modification
set_plot_style_defaults()           # Apply default matplotlib style
set_model_parameters()              # Configure model before fitting
set_cache_size()                    # Modify cache configuration
reset_cache()                       # Clear cache state
```

**When to use:** Configuration actions that modify state
**Key feature:** "set" for modification, "reset" for clearing

---

### 5. **COMPUTE** - Calculate derived metrics
**Pattern:** `compute_<metric>_<method>()`

```python
# Statistical calculations
compute_contrasts_pairwise()        # Post-hoc pairwise comparisons
compute_effect_sizes_cohens()       # Cohen's d/f effect sizes
compute_icc_from_model()            # Intraclass correlation
compute_aic_from_models()           # AIC for model comparison
```

**When to use:** Any calculation/analysis that derives new metrics
**Key feature:** Method/approach is specified when multiple exist

---

### 6. **FIT** - Estimate statistical models
**Pattern:** `fit_<model>_<design>()`

```python
# Statistical model estimation
fit_irt_grm()                       # Fit IRT Graded Response Model
fit_lmm_trajectory()                # Fit LMM for trajectory analysis
fit_lmm_trajectory_tsvr()           # Fit LMM with TSVR time variable
fit_glm_logistic()                  # Fit generalized linear model
```

**When to use:** Statistical model parameter estimation
**Key feature:** Model type + analysis design are both explicit

---

### 7. **PREPARE** - Data wrangling for analysis
**Pattern:** `prepare_<target>_from_<source>()`

```python
# Data preparation pipelines
prepare_irt_input_from_wide()       # Transform wide data → IRT format
prepare_lmm_input_from_theta()      # Transform theta scores → LMM format
prepare_plot_data_from_model()      # Extract data for plotting
```

**When to use:** Data wrangling/transformation for specific analysis
**Key feature:** Shows pipeline flow (source → target)

---

### 8. **COMPARE** - Model selection
**Pattern:** `compare_<entities>_by_<criterion>()`

```python
# Model comparison
compare_lmm_models_by_aic()         # Select best LMM via AIC
compare_irt_models_by_bic()         # Select best IRT via BIC
compare_participants_by_age()       # Group comparison
```

**When to use:** Selection among alternatives using explicit criterion
**Key feature:** What is compared + criterion are both explicit

---

## Special Cases

### Extract (from fitted models)
**Pattern:** `extract_<result>_from_<model>()`

```python
extract_theta_from_irt()            # Get theta scores from fitted IRT
extract_fixed_effects_from_lmm()    # Get fixed effects from fitted LMM
extract_parameters_from_model()     # Get parameters from any model
```

**When to use:** Retrieving computed results from fitted model objects

---

### Plot (visualization)
**Pattern:** `plot_<type>_<scale>()`

```python
plot_trajectory_theta()             # Trajectory on theta scale
plot_trajectory_probability()       # Trajectory on probability scale
plot_diagnostics_residuals()        # Diagnostic plots for residuals
plot_histogram_by_group()           # Grouped histogram
```

**When to use:** All visualization functions

---

### Validate (quality checks)
**Pattern:** `validate_<aspect>_<method>()`

```python
validate_irt_convergence()          # Check IRT model convergence
validate_lmm_assumptions()          # Check LMM statistical assumptions
validate_data_completeness()        # Check for missing data
```

**When to use:** Quality control and assumption checking

---

## Hierarchy: Pipeline vs Atomic

**Pipeline Functions (2 words):**
```python
calibrate_irt()                     # Calls: prepare + configure + fit + extract
run_lmm_analysis()                  # Calls: prepare + compare + fit + extract
```

**Atomic Functions (3+ words):**
```python
prepare_irt_input_from_wide()       # Single atomic step
fit_irt_grm()                       # Single atomic step
extract_theta_from_irt()            # Single atomic step
```

**Rule:** Pipeline wrappers are shorter (2 words), atomics are longer (3+ words)

---

## Applying the System: 5 Current Renames

| Current Name | New Name | Pattern | Rationale |
|--------------|----------|---------|-----------|
| `get_config()` | `load_config_from_yaml()` | LOAD | Explicit I/O operation |
| `get_path()` | `resolve_path_from_config()` | RESOLVE | Computes path, not just retrieves |
| `theta_to_probability()` | `convert_theta_to_probability()` | CONVERT | A→B transformation |
| `post_hoc_contrasts()` | `compute_contrasts_pairwise()` | COMPUTE | Calculates derived metric |
| `setup_plot_style()` | `set_plot_style_defaults()` | SET | Configuration action |

---

## Full Module Audit (51 Functions → Patterns)

### tools.config (13 functions)
```python
# CURRENT → NEW
load_config()                       → load_config_from_file()        # LOAD
get_config()                        → load_config_from_yaml()        # LOAD (or keep as convenience)
get_path()                          → resolve_path_from_config()     # RESOLVE
get_plot_config()                   → load_plot_config_from_yaml()   # LOAD
get_irt_config()                    → load_irt_config_from_yaml()    # LOAD
get_lmm_config()                    → load_lmm_config_from_yaml()    # LOAD
load_rq_config()                    → load_rq_config_merged()        # LOAD (merges global+chapter+RQ)
deep_merge()                        → merge_config_dicts()           # (utility, keep as is)
validate_paths()                    → validate_paths_exist()         # VALIDATE
validate_irt_config()               → validate_irt_params()          # VALIDATE
expand_env_vars()                   → expand_env_vars_in_path()      # (utility, keep as is)
reset_cache()                       → reset_config_cache()           # SET (reset)
```

### tools.analysis_irt (8 functions)
```python
# Most IRT functions already follow patterns
calibrate_irt()                     → (keep - pipeline wrapper)
fit_irt_model()                     → fit_irt_grm()                  # FIT (be specific)
prepare_irt_data()                  → prepare_irt_input_from_wide()  # PREPARE
extract_theta_scores()              → extract_theta_from_irt()       # EXTRACT
extract_item_parameters()           → extract_parameters_from_irt()  # EXTRACT
validate_irt_convergence()          → (keep - follows VALIDATE)
purify_items()                      → filter_items_by_quality()      # (or keep, debate)
```

### tools.analysis_lmm (10 functions)
```python
# Most LMM functions already follow patterns
prepare_lmm_data()                  → prepare_lmm_input_from_theta() # PREPARE
configure_candidate_models()        → (keep - good name)
fit_lmm_model()                     → fit_lmm_trajectory()           # FIT (be specific)
compare_models()                    → compare_lmm_models_by_aic()    # COMPARE
extract_fixed_effects()             → extract_fixed_effects_from_lmm() # EXTRACT
extract_random_effects()            → extract_random_effects_from_lmm() # EXTRACT
run_lmm_analysis()                  → (keep - pipeline wrapper)
post_hoc_contrasts()                → compute_contrasts_pairwise()   # COMPUTE
compute_effect_sizes()              → compute_effect_sizes_cohens()  # COMPUTE (method)
fit_lmm_with_tsvr()                 → fit_lmm_trajectory_tsvr()      # FIT (specific design)
```

### tools.plotting (7 functions)
```python
setup_plot_style()                  → set_plot_style_defaults()      # SET
plot_trajectory()                   → (keep - follows PLOT)
plot_diagnostics()                  → (keep - follows PLOT)
plot_histogram_by_group()           → (keep - follows PLOT)
theta_to_probability()              → convert_theta_to_probability() # CONVERT
save_plot_with_data()               → (keep - good name)
plot_trajectory_probability()       → (keep - follows PLOT)
```

### tools.validation (11 functions)
```python
# Most validation functions already follow patterns
validate_data_extraction()          → (keep - follows VALIDATE)
validate_irt_convergence()          → (keep - follows VALIDATE)
validate_lmm_residuals()            → (keep - follows VALIDATE)
validate_lmm_assumptions()          → (keep - follows VALIDATE)
validate_purification()             → (keep - follows VALIDATE)
validate_theta_distribution()       → (keep - follows VALIDATE)
check_missing_data()                → (keep - follows CHECK)
load_lineage()                      → load_lineage_from_file()       # LOAD
save_lineage()                      → save_lineage_to_file()         # (utility)
validate_lineage()                  → (keep - follows VALIDATE)
```

---

## Module Naming

### Pattern: `tools.<domain>`

**Current modules:**
```
tools.analysis_irt      # IRT calibration and item analysis
tools.analysis_lmm      # Linear Mixed Models
tools.plotting          # Visualization
tools.validation        # Quality checks
tools.config            # Configuration management
```

**Rules:**
- Use `analysis_<method>` for statistical methodologies
- Use singular nouns (plotting, not plots)
- No abbreviations except standard stats terms (irt, lmm, ctt, glm)

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
docs/tools_inventory.md    # Lowercase, underscores
docs/tools_catalog.md
docs/tools_naming.md       # THIS FILE
```

### RQ Data Files
```
results/ch5/rq1/data/
├── step00_irt_input.csv           # stepNN prefix for ordering
├── step02_purified_items.csv
├── step03_theta_scores.csv
└── step04_lmm_input.csv
```

---

## Agent Usage

**rq_planner:**
- Uses **pipeline wrappers** (2 words): `calibrate_irt()`, `run_lmm_analysis()`
- Does NOT mention atomic helpers

**rq_tools:**
- Maps pipeline → atomic functions
- Lists all atomic helpers needed

**rq_analysis:**
- Uses **atomic functions** (3+ words) with full module paths
- Example: `tools.analysis_irt.fit_irt_grm()`

**g_code:**
- Copy-pastes atomic function calls exactly
- Zero improvisation on names

---

## Adding New Functions

**Before adding a new function:**

1. **Identify purpose** → Choose 1 of 8 patterns
2. **Apply pattern** → Use exact formula
3. **Verify uniqueness** → No name collisions
4. **Document** → Add to tools_inventory.md

**Example:**
```
Need: Compute Cronbach's alpha
Purpose: Calculate metric
Pattern: COMPUTE → compute_<metric>_<method>()
Result: compute_reliability_cronbach_alpha()
```

---

## Consistency Rules

✅ **DO:**
- Use ONE of the 8 formulaic patterns
- Make source/target/method explicit in name
- Use full words (no abbreviations except stats terms)
- Keep pipeline wrappers short (2 words)
- Keep atomic functions descriptive (3+ words)

❌ **DON'T:**
- Mix patterns (e.g., `get_path` instead of `resolve_path_from_config`)
- Use vague verbs (process, analyze, handle)
- Abbreviate unnecessarily (calc, ext, proc)
- Create module-function redundancy (config.get_config)
- Use noun-only names (theta_to_probability without verb)

---

## Quick Reference Card

```python
# TRANSFORMATIONS
convert_<A>_to_<B>()               # A→B data transformation

# I/O OPERATIONS
load_<noun>_from_<source>()        # Read from disk
save_<noun>_to_<dest>()            # Write to disk

# COMPUTATION
resolve_<noun>_from_<source>()     # Compute/derive values
compute_<metric>_<method>()        # Calculate statistics
extract_<result>_from_<model>()    # Get results from fitted model

# CONFIGURATION
set_<noun>_<qualifier>()           # Modify state
reset_<noun>()                     # Clear state

# MODELING
fit_<model>_<design>()             # Estimate parameters
prepare_<target>_from_<source>()   # Wrangle data for analysis
compare_<entities>_by_<criterion>() # Select among alternatives

# QUALITY CONTROL
validate_<aspect>_<method>()       # Check correctness
check_<condition>()                # Simple existence test

# VISUALIZATION
plot_<type>_<scale>()              # Create visualization
```

---

## Version History

- **v1.0 (2025-11-22):** Initial draft with verb/noun taxonomies
- **v2.0 (2025-11-22):** Complete rewrite with 8 formulaic patterns

---

**Status:** Active - Ready for systematic application

**Next Steps:**
1. Apply systematic renames to all 51 functions
2. Update tools_inventory.md with new names
3. Update tools_catalog.md with new names
4. Update any agent prompts that reference old names
5. Git commit with complete naming system overhaul
