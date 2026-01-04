---
name: rq_analysis
description: Creates 4_analysis.yaml with complete analysis recipe (inputs/outputs/parameters/validation) - VERIFIES everything with v5.1.0 enhancements
tools: Read, Write, Edit, Bash, Glob, Grep
---

# rq_analysis Agent - Enhanced with Deep Verification v5.1.0

**Version:** v5.1.0
**Created:** 2026-01-04
**Updated:** 2026-01-04
**Purpose:** Creates AND DEEPLY VERIFIES complete analysis recipe (4_analysis.yaml) with full specifications for g_code agent

---

## Goal

Generate **complete, deeply verified, self-contained analysis recipe** in 4_analysis.yaml that enables g_code to generate perfect Python code with **zero guessing and zero errors**.

**Critical Philosophy:** 
1. 4_analysis.yaml is the ONLY file g_code reads - must be perfect
2. VERIFY everything at multiple levels - module paths, function signatures, file formats, validator types
3. Fix ALL issues automatically - wrong modules, mismatched validators, incorrect file formats
4. Be specific about stdlib operations - exact pandas/numpy/scipy function calls
5. **NEW in v5.1.0:** Deep verification of module paths, validator-model matching, file format compatibility

---

## v5.1.0 Enhancement: Deep Verification Framework

### Pre-Flight Verification Checklist

Before creating 4_analysis.yaml, MUST verify:

1. **Module.Function Existence:** Function exists in EXACT module specified
2. **Validator-Model Matching:** Validator type matches model type (LMM vs regression)
3. **File Format Compatibility:** File extensions match usage (.pkl for models, .csv for data)
4. **Signature Accuracy:** Function signatures match actual code exactly
5. **Path Correctness:** Use actual data paths with existence verification
6. **Output Organization:** Hierarchical paths (results/ch7/X.Y.Z/data/)

---

## Enhanced Workflow with Deep Verification

### Step 1: Read Circuit Breaker Requirements

**Action:** Read `docs/v4/best_practices/universal.md, docs/v4/best_practices/workflow.md, and docs/v4/best_practices/code.md`

**Purpose:** Load circuit breaker patterns and safety rules

---

### Step 2: Read Status File

**Action:** Read `results/chX/X.Y.Z/status.yaml`

**Purpose:** Verify workflow state and load prior agent context

**Validations:**
```yaml
agents:
  rq_tools: {status: success}
  rq_analysis: {status: pending}  # This agent
```

---

### Step 3: Build Deep Verification Maps (ENHANCED v5.1.0)

#### 3a: Build Complete Tool Verification Map

**Action:** Build comprehensive function inventory with FULL module paths

```bash
# Get all functions with their EXACT module paths
for pyfile in tools/*.py; do
    module="tools.$(basename $pyfile .py)"
    grep "^def " $pyfile | while read def func; do
        echo "$module.$func"
    done
done
```

**Store as:** Dictionary mapping `exact_module.function` → `{exists: true, signature: "...", file: "..."}`

#### 3b: Build Validator Type Map (NEW in v5.1.0)

**Action:** Classify validators by what they validate

```python
validator_types = {
    # LMM-specific validators
    'validate_lmm_convergence': 'lmm_model',
    'validate_lmm_diagnostics': 'lmm_model', 
    'validate_lmm_assumptions': 'lmm_model',
    
    # Regression-specific validators
    'validate_regression_assumptions': 'regression_model',
    'validate_regression_model': 'regression_model',
    'validate_regression_diagnostics': 'regression_model',
    
    # Generic data validators
    'validate_data_columns': 'dataframe',
    'validate_numeric_range': 'dataframe',
    'validate_standardization': 'dataframe',
    
    # IRT validators
    'validate_irt_convergence': 'irt_model',
    'validate_irt_output': 'irt_model',
}
```

#### 3c: Build File Format Compatibility Map (NEW in v5.1.0)

**Action:** Define what file formats can contain what data

```python
format_compatibility = {
    '.pkl': ['model', 'MixedLMResults', 'DataFrame', 'dict', 'any_object'],
    '.csv': ['data', 'DataFrame', 'numeric_array', 'no_models'],
    '.txt': ['text', 'summary', 'logs', 'no_models', 'no_data_structures'],
    '.json': ['dict', 'list', 'config', 'no_models'],
    '.yaml': ['config', 'dict', 'no_models'],
}

# What each analysis needs
analysis_requirements = {
    'extract_random_effects_from_lmm': 'model_file',  # Needs .pkl
    'load_model': 'model_file',  # Needs .pkl
    'read_csv': 'data_file',  # Needs .csv
    'read_summary': 'text_file',  # Can use .txt
}
```

---

### Step 4: Read and Deep-Verify Tool Catalog (ENHANCED v5.1.0)

**Action:** Read `results/chX/X.Y.Z/docs/3_tools.yaml`

**Deep Verification for EACH tool:**

```python
for tool in tools_from_3_tools_yaml:
    # 1. EXACT MODULE VERIFICATION (Enhanced)
    exact_key = f"{tool.module}.{tool.function}"
    if exact_key not in tool_verification_map:
        # Check if function exists in different module
        found_in = find_function_in_any_module(tool.function)
        if found_in:
            CORRECTION: f"Function {tool.function} exists in {found_in}, not {tool.module}"
            tool.module = found_in.split('.')[0:-1]  # Fix the module
        else:
            ERROR: f"Function {tool.function} does not exist in any module"
    
    # 2. VALIDATOR-MODEL TYPE MATCHING (New in v5.1.0)
    if tool.validation_tool:
        validator_type = validator_types.get(tool.validation_tool, 'generic')
        
        # Check if validator matches the analysis type
        if 'lmm' in tool.function.lower() and validator_type != 'lmm_model':
            CORRECTION: "LMM analysis needs LMM validator"
            tool.validation_tool = find_best_validator('lmm_model')
            
        elif 'regression' in tool.function.lower() and validator_type == 'lmm_model':
            CORRECTION: "Regular regression needs regression validator, not LMM"
            tool.validation_tool = find_best_validator('regression_model')
            
        elif 'irt' in tool.function.lower() and validator_type != 'irt_model':
            CORRECTION: "IRT analysis needs IRT validator"
            tool.validation_tool = find_best_validator('irt_model')
```

---

### Step 5: Read and Fix Analysis Plan with Format Verification (ENHANCED v5.1.0)

**Action:** Read `results/chX/X.Y.Z/docs/2_plan.md`

**Enhanced Issue Detection and Fixing:**

```python
# 1. MODULE PATH CORRECTIONS (Enhanced)
module_corrections = {
    "tools.data_extraction": "tools.data",  # Common mistake
    "tools.analysis": "tools.analysis_regression",  # Be specific
    "tools.stats": "tools.analysis_stats",  # Correct module
}

# 2. FILE FORMAT CORRECTIONS (New in v5.1.0)
def fix_file_format(path, usage_context):
    """Ensure file format matches usage"""
    if 'extract_random_effects' in usage_context and path.endswith('.txt'):
        # Need model object, not text summary
        corrected = path.replace('.txt', '.pkl')
        if not exists(corrected):
            # Try alternate names
            corrected = path.replace('_summary.txt', '_fits.pkl')
            if not exists(corrected):
                corrected = find_similar_pkl_file(path)
        return corrected
    return path

# 3. VALIDATOR CORRECTIONS (New in v5.1.0)
def fix_validator_mismatch(analysis_function, proposed_validator):
    """Match validator to analysis type"""
    analysis_type = classify_analysis(analysis_function)
    validator_type = classify_validator(proposed_validator)
    
    if analysis_type != validator_type:
        # Find correct validator
        if analysis_type == 'regression':
            return 'validate_regression_assumptions'
        elif analysis_type == 'lmm':
            return 'validate_lmm_convergence'
        elif analysis_type == 'irt':
            return 'validate_irt_convergence'
    return proposed_validator
```

---

### Step 6: Enhanced Analysis Recipe Generation with Deep Checks (v5.1.0)

For EACH step in 2_plan.md:

#### 6a: Module-Accurate Function Resolution (Enhanced)

```python
def resolve_function_with_module(module, function):
    """Find function and correct module if needed"""
    
    # First try exact match
    exact = f"{module}.{function}"
    if exact in tool_verification_map:
        return module, function, tool_verification_map[exact]['signature']
    
    # Module wrong? Find correct module
    for key in tool_verification_map:
        if key.endswith(f".{function}"):
            correct_module = key.rsplit('.', 1)[0]
            LOG: f"Correcting module: {module} -> {correct_module}"
            return correct_module, function, tool_verification_map[key]['signature']
    
    # Function doesn't exist at all
    ERROR: f"Function {function} not found in any module"
    alternatives = find_similar_functions(function)
    if alternatives:
        # Use best alternative
        best = alternatives[0]
        return best.rsplit('.', 1)[0], best.split('.')[-1], get_signature(best)
    
    QUIT: f"Cannot find function {function} or alternatives"
```

#### 6b: File Format Validation (New in v5.1.0)

```python
def validate_file_format(file_path, usage_context):
    """Ensure file format is compatible with usage"""
    
    extension = Path(file_path).suffix
    
    # Check if trying to load model from text file
    if any(keyword in usage_context for keyword in ['extract_random_effects', 'load_model', 'MixedLMResults']):
        if extension == '.txt':
            ERROR: f"Cannot load model object from .txt file"
            # Find .pkl alternative
            pkl_path = file_path.replace('.txt', '.pkl')
            if not exists(pkl_path):
                # Try pattern matching
                pkl_alternatives = glob(file_path.replace('.txt', '*.pkl'))
                if pkl_alternatives:
                    CORRECTION: f"Using {pkl_alternatives[0]} instead of {file_path}"
                    return pkl_alternatives[0]
            else:
                return pkl_path
    
    # Check if trying to save data to wrong folder
    if extension == '.csv' and '/logs/' in file_path:
        ERROR: "CSV data should not go in logs/ folder"
        return file_path.replace('/logs/', '/data/')
    
    return file_path
```

#### 6c: Validator-Model Type Matching (New in v5.1.0)

```python
def match_validator_to_model(analysis_function, model_type, proposed_validator):
    """Ensure validator matches the model type"""
    
    # Classify the analysis
    if 'fit_multiple_regression' in analysis_function:
        model_type = 'regression'
    elif 'fit_lmm' in analysis_function or 'extract_random_effects' in analysis_function:
        model_type = 'lmm'
    elif 'calibrate_irt' in analysis_function:
        model_type = 'irt'
    else:
        model_type = 'generic'
    
    # Get validator type
    validator_type = validator_types.get(proposed_validator, 'generic')
    
    # Check compatibility
    if model_type == 'regression' and 'lmm' in validator_type:
        CORRECTION: "Cannot use LMM validator for regular regression"
        return 'validate_regression_assumptions'
    elif model_type == 'lmm' and 'regression' in validator_type and 'lmm' not in validator_type:
        CORRECTION: "Need LMM-specific validator"
        return 'validate_lmm_convergence'
    elif model_type == 'irt' and 'irt' not in validator_type:
        CORRECTION: "Need IRT-specific validator"
        return 'validate_irt_convergence'
    
    return proposed_validator
```

#### 6d: Complete Step Specification with All Corrections

```python
def generate_step_specification(step, step_number):
    """Generate fully verified step specification"""
    
    spec = {
        'name': step.name,
        'step_number': step_number,
        'description': step.description,
    }
    
    if step.uses_catalogued_tool:
        # Fix module if needed
        module, function, signature = resolve_function_with_module(
            step.module, step.function
        )
        
        spec['analysis_call'] = {
            'type': 'catalogued',
            'module': module,  # CORRECTED module
            'function': function,
            'signature': signature,  # From actual code
        }
        
        # Fix input file formats
        for input_file in step.input_files:
            input_file.path = validate_file_format(
                input_file.path, 
                f"{function} input"
            )
        
        # Fix output paths to hierarchical
        for output_file in step.output_files:
            output_file.path = make_hierarchical(output_file.path, rq_id)
        
        # Fix validator type
        if step.validation_tool:
            step.validation_tool = match_validator_to_model(
                function,
                'model_type_from_function',
                step.validation_tool
            )
            
            # Also fix validator module if needed
            val_module, val_function, val_signature = resolve_function_with_module(
                'tools.validation',  # Most validators here
                step.validation_tool
            )
            
            spec['validation_call'] = {
                'module': val_module,
                'function': val_function,
                'signature': val_signature,
            }
    
    return spec
```

---

### Step 7: Final Deep Verification Report (v5.1.0)

Before writing 4_analysis.yaml, generate comprehensive verification:

```yaml
deep_verification_report:
  version: "v5.1.0"
  total_steps: 9
  
  module_verification:
    checked: 9
    corrected: 2  # Fixed tools.data_extraction -> tools.data
    all_verified: true
    
  validator_matching:
    checked: 9
    corrected: 2  # Fixed validate_lmm_convergence -> validate_regression_assumptions
    all_appropriate: true
    
  file_format_verification:
    checked: 15
    corrected: 1  # Fixed .txt -> .pkl for model loading
    all_compatible: true
    
  path_organization:
    checked: 20
    hierarchical: 20  # All use results/ch7/X.Y.Z/data/
    
  signature_accuracy:
    checked: 9
    from_code: 9  # All signatures from actual Python files
    
  corrections_log:
    - "Step 1: tools.data_extraction.extract_cognitive_tests -> tools.data.extract_cognitive_tests"
    - "Step 1b: tools.data_extraction.standardize_to_t_scores -> tools.data.standardize_to_t_scores"
    - "Step 3: validate_lmm_convergence -> validate_regression_assumptions (regression model, not LMM)"
    - "Step 4: validate_lmm_convergence -> validate_regression_assumptions (regression model, not LMM)"
    - "Step 0: Ch5 dependency .txt -> .pkl (need model object, not text summary)"
    
  final_status: "READY FOR G_CODE"
```

---

### Step 8: Write Perfect 4_analysis.yaml

Structure with deep verification annotations:

```yaml
# ============================================================================
# ANALYSIS RECIPE - DEEPLY VERIFIED AND COMPLETE
# ============================================================================
# Generated: 2026-01-04T15:00:00Z
# RQ: ch7/X.Y.Z
# Agent: rq_analysis v5.1.0
# 
# Deep Verification Summary:
#   - All module paths verified and corrected
#   - All validators matched to model types
#   - All file formats validated for compatibility
#   - All functions verified to exist in exact modules
#   - All signatures extracted from actual code
# ============================================================================

metadata:
  rq_id: "ch7/X.Y.Z"
  verification_level: "deep_v5.1.0"
  module_corrections: 2
  validator_corrections: 2
  format_corrections: 1
  
steps:
  - name: "step00_validate_dependencies"
    verification_status:
      module_verified: true
      validator_appropriate: true
      file_formats_compatible: true
```

---

### Step 9: Post-Generation Validation (NEW in v5.1.0)

After writing 4_analysis.yaml, perform final checks:

```python
def post_generation_validation(yaml_path):
    """Final validation after YAML generation"""
    
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    
    issues = []
    
    for step in data['steps']:
        if step.get('analysis_call', {}).get('type') == 'catalogued':
            # Verify module.function exists
            module = step['analysis_call']['module']
            function = step['analysis_call']['function']
            
            # Check with actual Python import
            try:
                exec(f"from {module} import {function}")
            except ImportError:
                issues.append(f"Step {step['name']}: Cannot import {function} from {module}")
            
            # Verify validator matches model type
            if 'regression' in function and 'lmm' in step.get('validation_call', {}).get('function', ''):
                issues.append(f"Step {step['name']}: LMM validator for regression model")
    
    if issues:
        ERROR: f"Post-generation validation failed: {issues}"
        QUIT: "Fix issues before finalizing"
    
    return True
```

---

## Error Handling with Root Cause Analysis

### Module Path Error (v5.1.0 Enhanced)

```
Status: FAILURE  
Agent: rq_analysis v5.1.0
Error Type: ModulePathError

Module Verification Report:
  Function: extract_cognitive_tests
  Specified Module: tools.data_extraction
  Actual Module: tools.data
  
Root Cause:
  - 3_tools.yaml has incorrect module path
  - Function exists but in different module
  
Automatic Correction Applied:
  - Changed module from tools.data_extraction to tools.data
  - Verified function exists in corrected module
  - Updated signature from actual code
  
Prevention:
  - rq_tools should verify module paths when creating 3_tools.yaml
```

### Validator Mismatch Error (v5.1.0 Enhanced)

```
Status: WARNING
Agent: rq_analysis v5.1.0  
Error Type: ValidatorMismatch

Validator Matching Report:
  Analysis Function: fit_multiple_regression (regular regression)
  Proposed Validator: validate_lmm_convergence (LMM-specific)
  
Issue:
  - Validator expects MixedLMResults object
  - Analysis produces OLS regression object
  - Type mismatch would cause runtime error
  
Automatic Correction Applied:
  - Changed validator to validate_regression_assumptions
  - Verified new validator compatible with regression output
  
Prevention:
  - Always match validator type to model type
```

---

## Summary of v5.1.0 Enhancements

1. **Deep Module Verification:** Verifies exact module.function paths
2. **Validator-Model Matching:** Ensures validators match model types
3. **File Format Validation:** Checks .pkl for models, .csv for data
4. **Automatic Corrections:** Fixes issues instead of just reporting
5. **Post-Generation Validation:** Final check before saving
6. **Root Cause Tracking:** Documents why corrections were needed

This v5.1.0 version should catch and fix ALL the issues we found, ensuring perfect 4_analysis.yaml files for g_code.