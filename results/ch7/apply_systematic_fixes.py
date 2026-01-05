#!/usr/bin/env python3
"""
Apply systematic fixes to all Chapter 7 RQs
Fixes column names and adds missing data handling
"""

import sys
from pathlib import Path
import shutil

# Column replacements to make
REPLACEMENTS = [
    # Old column names -> New column names
    ("'RAVLT trial 1 score'", "'ravlt-trial-1-score'"),
    ("'RAVLT trial 2 score'", "'ravlt-trial-2-score'"),
    ("'RAVLT trial 3 score'", "'ravlt-trial-3-score'"),
    ("'RAVLT trial 4 score'", "'ravlt-trial-4-score'"),
    ("'RAVLT trial 5 score'", "'ravlt-trial-5-score'"),
    ('f"RAVLT trial {i} score"', 'f"ravlt-trial-{i}-score"'),
    ("f'RAVLT trial {i} score'", "f'ravlt-trial-{i}-score'"),
    ("'RAVLT delayed recall score'", "'ravlt-delayed-recall-score'"),
    ("'BVMT total recall'", "'bvmt-total-recall'"),
    ("'BVMT trial 1 score'", "'bvmt-trial-1-score'"),
    ("'BVMT trial 2 score'", "'bvmt-trial-2-score'"),
    ("'BVMT trial 3 score'", "'bvmt-trial-3-score'"),
    ("'NART Score'", "'nart-score'"),
    ("'RPM Score'", "'rpm-score'"),
    ("'Age in years'", "'age'"),
    ("'Sex 0=female 1=male'", "'sex'"),
    ("'Education'", "'education'"),
    ("'Total DASS Depression Items'", "'total-dass-depression-items'"),
    ("'Total DASS Anxiety Items'", "'total-dass-anxiety-items'"),
    ("'Total DASS Stress Items'", "'total-dass-stress-items'"),
    ("'VR Exposure'", "'vr-exposure'"),
    ("'Typical sleep hours'", "'typical-sleep-hours'"),
]

def fix_file(file_path):
    """Fix column names in a Python file."""
    
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if fixes are needed
    needs_fix = False
    for old, new in REPLACEMENTS:
        if old in content:
            needs_fix = True
            break
    
    if not needs_fix:
        return False
    
    # Backup original
    backup_path = file_path.with_suffix('.py.bak')
    shutil.copy2(file_path, backup_path)
    print(f"  Backed up to: {backup_path}")
    
    # Apply replacements
    fixed_content = content
    for old, new in REPLACEMENTS:
        if old in fixed_content:
            fixed_content = fixed_content.replace(old, new)
            print(f"    Replaced: {old} → {new}")
    
    # Add import for missing data handler if not present
    if 'from missing_data_handler import' not in fixed_content and 'step01' in file_path.name:
        # Add import after the sys.path manipulations
        import_line = """
# Import missing data utilities
try:
    sys.path.insert(0, str(PROJECT_ROOT / "results" / "ch7"))
    from missing_data_handler import analyze_missing_pattern, create_missing_data_report
except ImportError:
    # Utilities not available - continue without
    pass
"""
        # Find a good place to insert (after PROJECT_ROOT definition)
        if 'PROJECT_ROOT = ' in fixed_content:
            lines = fixed_content.split('\n')
            for i, line in enumerate(lines):
                if 'PROJECT_ROOT = ' in line:
                    # Insert after next sys.path.insert
                    for j in range(i, min(i+10, len(lines))):
                        if 'sys.path.insert' in lines[j]:
                            lines.insert(j+1, import_line)
                            fixed_content = '\n'.join(lines)
                            print("    Added missing data handler import")
                            break
                    break
    
    # Save fixed version
    with open(file_path, 'w') as f:
        f.write(fixed_content)
    
    return True

def main():
    """Apply fixes to all affected RQs."""
    
    print("Applying systematic fixes to Chapter 7 RQs")
    print("=" * 60)
    
    # RQs to fix
    rqs_to_fix = ['7.1.2', '7.1.3', '7.2.1', '7.2.3', '7.2.4']
    
    ch7_dir = Path(__file__).parent
    
    for rq in rqs_to_fix:
        print(f"\nProcessing RQ {rq}...")
        rq_dir = ch7_dir / rq / 'code'
        
        if not rq_dir.exists():
            print(f"  Directory not found: {rq_dir}")
            continue
        
        # Fix step01 and step02 files (data extraction)
        for step in ['step01', 'step02', 'step00']:
            files = list(rq_dir.glob(f'{step}*.py'))
            for file_path in files:
                if 'FIXED' in file_path.name or 'OLD' in file_path.name:
                    continue
                print(f"  Checking: {file_path.name}")
                if fix_file(file_path):
                    print(f"    ✓ Fixed column names")
                else:
                    print(f"    - No changes needed")
    
    print("\n" + "=" * 60)
    print("Systematic fixes complete!")
    print("\nNotes:")
    print("- Original files backed up with .bak extension")
    print("- Column names updated to match DATA_DICTIONARY.md")
    print("- Missing data handler imports added where appropriate")

if __name__ == "__main__":
    main()