#!/usr/bin/env python3
"""
Column Name Mapping Utility for Chapter 7
Maps old column names to correct names from DATA_DICTIONARY.md

This utility fixes the systematic column name mismatch issue across Ch7 RQs.
"""

# Column name mappings from old (incorrect) to new (correct) names
COLUMN_MAPPINGS = {
    # Demographics
    'Age in years': 'age',
    'Sex 0=female 1=male': 'sex',
    'Education': 'education',
    
    # Cognitive tests - raw scores
    'NART Score': 'nart-score',
    'RPM Score': 'rpm-score',
    'BVMT total recall': 'bvmt-total-recall',
    
    # RAVLT trials (individual)
    'RAVLT trial 1 score': 'ravlt-trial-1-score',
    'RAVLT trial 2 score': 'ravlt-trial-2-score',
    'RAVLT trial 3 score': 'ravlt-trial-3-score',
    'RAVLT trial 4 score': 'ravlt-trial-4-score',
    'RAVLT trial 5 score': 'ravlt-trial-5-score',
    'RAVLT delayed recall score': 'ravlt-delayed-recall-score',
    'RAVLT distraction trial score': 'ravlt-distraction-trial-score',
    'RAVLT free recall score': 'ravlt-free-recall-score',
    
    # BVMT trials
    'BVMT trial 1 score': 'bvmt-trial-1-score',
    'BVMT trial 2 score': 'bvmt-trial-2-score', 
    'BVMT trial 3 score': 'bvmt-trial-3-score',
    'BVMT delayed recall score': 'bvmt-delayed-recall-score',
    
    # DASS subscales
    'Total DASS Depression Items': 'total-dass-depression-items',
    'Total DASS Anxiety Items': 'total-dass-anxiety-items',
    'Total DASS Stress Items': 'total-dass-stress-items',
    
    # Other self-report
    'VR Exposure': 'vr-exposure',
    'Typical sleep hours': 'typical-sleep-hours',
}

def get_correct_column_name(old_name):
    """
    Get the correct column name from DATA_DICTIONARY.md
    
    Args:
        old_name: The old/incorrect column name
        
    Returns:
        The correct column name, or the original if no mapping exists
    """
    return COLUMN_MAPPINGS.get(old_name, old_name)

def fix_column_references_in_code(code_str):
    """
    Fix column references in Python code string.
    
    Args:
        code_str: Python code as string
        
    Returns:
        Fixed Python code with correct column names
    """
    fixed_code = code_str
    
    for old_name, new_name in COLUMN_MAPPINGS.items():
        # Fix string literals
        fixed_code = fixed_code.replace(f"'{old_name}'", f"'{new_name}'")
        fixed_code = fixed_code.replace(f'"{old_name}"', f'"{new_name}"')
        
        # Fix f-string patterns (e.g., f'RAVLT trial {i} score')
        if 'RAVLT trial' in old_name and '{i}' not in old_name:
            # Extract trial number
            import re
            match = re.search(r'(\d+)', old_name)
            if match:
                trial_num = match.group(1)
                # Fix the specific pattern
                old_pattern = f"f'RAVLT trial {{i}} score'"
                new_pattern = f"f'ravlt-trial-{{i}}-score'"
                fixed_code = fixed_code.replace(old_pattern, new_pattern)
                
                old_pattern = f'f"RAVLT trial {{i}} score"'
                new_pattern = f'f"ravlt-trial-{{i}}-score"'
                fixed_code = fixed_code.replace(old_pattern, new_pattern)
    
    return fixed_code

def validate_columns_exist(df, required_columns):
    """
    Validate that required columns exist in dataframe.
    
    Args:
        df: pandas DataFrame
        required_columns: list of column names that should exist
        
    Returns:
        tuple (all_exist: bool, missing: list)
    """
    import pandas as pd
    
    existing = set(df.columns)
    required = set(required_columns)
    missing = list(required - existing)
    
    return len(missing) == 0, missing

def report_column_usage(script_path):
    """
    Report which columns a script is trying to use.
    
    Args:
        script_path: Path to Python script
        
    Returns:
        dict with old_columns, new_columns, and needs_fixing flag
    """
    with open(script_path, 'r') as f:
        content = f.read()
    
    old_columns_used = []
    new_columns_needed = []
    
    for old_name, new_name in COLUMN_MAPPINGS.items():
        if old_name in content:
            old_columns_used.append(old_name)
            new_columns_needed.append(new_name)
    
    return {
        'old_columns': old_columns_used,
        'new_columns': new_columns_needed,
        'needs_fixing': len(old_columns_used) > 0
    }

if __name__ == "__main__":
    print("Column Name Mapping Utility")
    print("=" * 60)
    print("\nColumn Mappings (Old → New):")
    for old, new in COLUMN_MAPPINGS.items():
        print(f"  {old:40} → {new}")
    print("\n" + "=" * 60)
    print("Use this module to fix column references in Ch7 scripts.")
    print("Import and use get_correct_column_name() or fix_column_references_in_code()")