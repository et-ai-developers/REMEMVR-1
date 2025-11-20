# Tools Function Rename Reference

**Purpose:** Quick reference for all function renames during naming convention standardization
**Date:** 2025-11-22
**Status:** Complete - All 33 functions renamed

---

## Summary

- **Total functions renamed:** 33/51 (65%)
- **Functions unchanged:** 18/51 (35%) - Already followed naming conventions
- **Modules affected:** 5/5 (100%)

---

## tools/config.py (12 renames)

```
load_config()           → load_config_from_file()
get_config()            → load_config_from_yaml()
get_path()              → resolve_path_from_config()
get_plot_config()       → load_plot_config_from_yaml()
get_irt_config()        → load_irt_config_from_yaml()
get_lmm_config()        → load_lmm_config_from_yaml()
validate_paths()        → validate_paths_exist()
validate_irt_config()   → validate_irt_params()
deep_merge()            → merge_config_dicts()
load_rq_config()        → load_rq_config_merged()
expand_env_vars()       → expand_env_vars_in_path()
reset_cache()           → reset_config_cache()
```

---

## tools/plotting.py (2 renames)

```
setup_plot_style()      → set_plot_style_defaults()
theta_to_probability()  → convert_theta_to_probability()
```

**Unchanged (already follow conventions):**
- plot_trajectory()
- plot_diagnostics()
- plot_histogram_by_group()
- save_plot_with_data()
- plot_trajectory_probability()

---

## tools/analysis_lmm.py (10 renames)

```
prepare_lmm_data()          → prepare_lmm_input_from_theta()
fit_lmm_model()             → fit_lmm_trajectory()
compare_models()            → compare_lmm_models_by_aic()
extract_fixed_effects()     → extract_fixed_effects_from_lmm()
extract_random_effects()    → extract_random_effects_from_lmm()
post_hoc_contrasts()        → compute_contrasts_pairwise()
compute_effect_sizes()      → compute_effect_sizes_cohens()
fit_lmm_with_tsvr()         → fit_lmm_trajectory_tsvr()
```

**Unchanged (already follow conventions):**
- configure_candidate_models()
- run_lmm_analysis()

---

## tools/analysis_irt.py (5 renames)

```
prepare_irt_data()          → prepare_irt_input_from_wide()
fit_irt_model()             → fit_irt_grm()
extract_theta_scores()      → extract_theta_from_irt()
extract_item_parameters()   → extract_parameters_from_irt()
purify_items()              → filter_items_by_quality()
```

**Unchanged (already follow conventions):**
- calibrate_irt()
- configure_irt_model()
- validate_irt_convergence()

---

## tools/validation.py (3 renames)

```
load_lineage()          → load_lineage_from_file()
save_lineage()          → save_lineage_to_file()
validate_file_exists()  → check_file_exists()
```

**Unchanged (already follow conventions):**
- create_lineage_metadata()
- validate_lineage()
- validate_irt_convergence()
- validate_irt_parameters()
- check_missing_data()
- validate_lmm_convergence()
- validate_lmm_residuals()
- validate_data_columns()
- validate_numeric_range()
- generate_validation_report()
- save_validation_report()

---

## Pattern Distribution

### By Pattern Type:

**LOAD (8 functions):**
- load_config_from_file()
- load_config_from_yaml()
- load_plot_config_from_yaml()
- load_irt_config_from_yaml()
- load_lmm_config_from_yaml()
- load_rq_config_merged()
- load_lineage_from_file()

**RESOLVE (1 function):**
- resolve_path_from_config()

**SET (2 functions):**
- set_plot_style_defaults()
- reset_config_cache()

**CONVERT (1 function):**
- convert_theta_to_probability()

**PREPARE (2 functions):**
- prepare_lmm_input_from_theta()
- prepare_irt_input_from_wide()

**FIT (3 functions):**
- fit_lmm_trajectory()
- fit_lmm_trajectory_tsvr()
- fit_irt_grm()

**EXTRACT (4 functions):**
- extract_theta_from_irt()
- extract_parameters_from_irt()
- extract_fixed_effects_from_lmm()
- extract_random_effects_from_lmm()

**COMPUTE (2 functions):**
- compute_contrasts_pairwise()
- compute_effect_sizes_cohens()

**COMPARE (1 function):**
- compare_lmm_models_by_aic()

**VALIDATE (2 functions):**
- validate_paths_exist()
- validate_irt_params()

**CHECK (1 function):**
- check_file_exists()

**FILTER (1 function):**
- filter_items_by_quality()

**SAVE (1 function):**
- save_lineage_to_file()

**MERGE (1 function):**
- merge_config_dicts()

**EXPAND (1 function):**
- expand_env_vars_in_path()

---

## Migration Notes

### For Users:

1. **Update imports:**
   ```python
   # OLD
   from tools.config import get_config, get_path
   from tools.plotting import setup_plot_style, theta_to_probability
   from tools.analysis_lmm import prepare_lmm_data, fit_lmm_model

   # NEW
   from tools.config import load_config_from_yaml, resolve_path_from_config
   from tools.plotting import set_plot_style_defaults, convert_theta_to_probability
   from tools.analysis_lmm import prepare_lmm_input_from_theta, fit_lmm_trajectory
   ```

2. **Update function calls:**
   - All parameters remain the same
   - Only function names changed
   - No behavioral changes

3. **Search and replace:**
   - Use this document as reference
   - Update any scripts/notebooks that use old names
   - Update any documentation that references old names

### For Agents:

**rq_planner:**
- Update step names in plans to use new function names
- Use pipeline wrappers (2 words): `calibrate_irt()`, `run_lmm_analysis()`

**rq_tools:**
- Update 3_tools.yaml specifications with new atomic function names
- Use full module paths: `tools.analysis_lmm.fit_lmm_trajectory()`

**rq_analysis:**
- Update 4_analysis.yaml code blocks with new function names
- Copy-paste exact names from this document

**g_code:**
- Zero improvisation - use exact names from 4_analysis.yaml

---

## Verification Commands

```bash
# Check for old function names (should return nothing)
grep -r "def get_config\|def get_path\|def setup_plot_style" tools/
grep -r "def prepare_lmm_data\|def fit_lmm_model" tools/
grep -r "def prepare_irt_data\|def purify_items" tools/

# Check for new function names (should find all)
grep -r "def load_config_from_yaml\|def resolve_path_from_config" tools/
grep -r "def prepare_lmm_input_from_theta\|def fit_lmm_trajectory" tools/
grep -r "def prepare_irt_input_from_wide\|def filter_items_by_quality" tools/
```

---

## Related Documentation

- **Naming System:** [docs/v4/tools_naming.md](tools_naming.md) - Complete naming convention specification
- **API Reference:** [docs/tools_inventory.md](../tools_inventory.md) - Full function signatures (needs update)
- **Status Tracking:** [docs/tools_status.csv](../tools_status.csv) - Migration tracking (needs update)

---

## Version History

- **2025-11-22:** Initial creation - All 33 renames documented
- **Next:** Update tools_inventory.md, tools_status.csv, agent prompts

---

**Status:** Complete - Ready for documentation updates and git commit
