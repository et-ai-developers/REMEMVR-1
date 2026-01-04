#!/usr/bin/env python3
"""
Step 01: Extract Cognitive Tests
RQ 7.1.4: Unique REMEMVR variance unexplained by all predictors

Extract RAVLT, BVMT, NART, and RPM scores from dfnonvr.csv
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add project root to path
RQ_DIR = Path(__file__).resolve().parents[1]
PROJ_ROOT = RQ_DIR.parents[2]
sys.path.insert(0, str(PROJ_ROOT))

# Set up logging
LOG_FILE = RQ_DIR / "logs" / "step01_extract_cognitive_tests.log"
LOG_FILE.parent.mkdir(exist_ok=True)

def log(msg):
    """Log to both console and file."""
    print(msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{msg}\n")
        f.flush()

def main():
    """Main execution."""
    log("[START] Step 01: Extract cognitive tests")
    
    # Load participant data
    log("[LOAD] Reading dfnonvr.csv...")
    df = pd.read_csv(PROJ_ROOT / "data" / "dfnonvr.csv")
    log(f"[INFO] Loaded {len(df)} participants from dfnonvr.csv")
    
    # Check column names
    log("[DEBUG] Available columns (first 20):")
    for col in df.columns[:20]:
        log(f"  - {col}")
    
    # Extract cognitive test scores with actual column names
    log("[EXTRACT] Extracting cognitive test scores...")
    
    # Initialize output dataframe
    cognitive_df = pd.DataFrame()
    cognitive_df['uid'] = df['UID'].astype(str)
    
    # RAVLT: Need to sum trials 1-5 for total, and get delayed recall
    ravlt_cols = []
    for i in range(1, 6):
        col = f'RAVLT trial {i} score'
        if col in df.columns:
            ravlt_cols.append(col)
    
    if ravlt_cols:
        cognitive_df['RAVLT_T'] = df[ravlt_cols].sum(axis=1)
        log(f"[EXTRACT] RAVLT total computed from {len(ravlt_cols)} trials")
    else:
        log("[WARNING] RAVLT trial columns not found")
        cognitive_df['RAVLT_T'] = np.nan
    
    # RAVLT Delayed Recall
    if 'RAVLT delayed recall score' in df.columns:
        cognitive_df['RAVLT_DR_T'] = df['RAVLT delayed recall score']
        log("[EXTRACT] RAVLT delayed recall extracted")
    else:
        log("[WARNING] RAVLT delayed recall not found")
        cognitive_df['RAVLT_DR_T'] = np.nan
    
    # BVMT: Use total recall
    if 'BVMT total recall' in df.columns:
        cognitive_df['BVMT_T'] = df['BVMT total recall']
        log("[EXTRACT] BVMT total recall extracted")
    else:
        log("[WARNING] BVMT total recall not found")
        cognitive_df['BVMT_T'] = np.nan
    
    # NART: Use NART Score column
    if 'NART Score' in df.columns:
        cognitive_df['NART_T'] = df['NART Score']
        log("[EXTRACT] NART score extracted")
    else:
        log("[WARNING] NART Score not found")
        cognitive_df['NART_T'] = np.nan
    
    # RPM: Use RPM Score column  
    if 'RPM Score' in df.columns:
        cognitive_df['RPM_T'] = df['RPM Score']
        log("[EXTRACT] RPM score extracted")
    else:
        log("[WARNING] RPM Score not found")
        cognitive_df['RPM_T'] = np.nan
    
    # Check for missing values
    log("[CHECK] Checking for missing values...")
    missing = cognitive_df.isnull().sum()
    for col, n_missing in missing.items():
        if n_missing > 0:
            log(f"  - {col}: {n_missing} missing values")
    
    # Summary statistics
    log("[SUMMARY] Cognitive test scores:")
    for col in ['RAVLT_T', 'RAVLT_DR_T', 'BVMT_T', 'NART_T', 'RPM_T']:
        if col in cognitive_df.columns:
            mean_val = cognitive_df[col].mean()
            std_val = cognitive_df[col].std()
            min_val = cognitive_df[col].min()
            max_val = cognitive_df[col].max()
            log(f"  - {col}: M={mean_val:.1f}, SD={std_val:.1f}, Range=[{min_val:.0f}, {max_val:.0f}]")
    
    # Save output
    output_path = RQ_DIR / "data" / "step01_cognitive_tests.csv"
    output_path.parent.mkdir(exist_ok=True)
    cognitive_df.to_csv(output_path, index=False)
    log(f"[SAVE] Saved cognitive tests to {output_path}")
    log(f"[INFO] Shape: {cognitive_df.shape}")
    
    log("[SUCCESS] Step 01 complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())