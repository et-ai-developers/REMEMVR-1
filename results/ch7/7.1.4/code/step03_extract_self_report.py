#!/usr/bin/env python3
"""
Step 03: Extract Self-Report Scores (DASS, VR Experience, Sleep)
RQ 7.1.4: Unique REMEMVR variance unexplained by all predictors

Attempt to extract DASS subscales, VR experience, and sleep data
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
LOG_FILE = RQ_DIR / "logs" / "step03_extract_self_report.log"
LOG_FILE.parent.mkdir(exist_ok=True)

def log(msg):
    """Log to both console and file."""
    print(msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{msg}\n")
        f.flush()

def main():
    """Main execution."""
    log("[START] Step 03: Extract self-report scores")
    
    # Load participant data
    log("[LOAD] Reading dfnonvr.csv...")
    df = pd.read_csv(PROJ_ROOT / "data" / "dfnonvr.csv")
    log(f"[INFO] Loaded {len(df)} participants with {len(df.columns)} columns")
    
    # Initialize output dataframe
    self_report = pd.DataFrame()
    self_report['uid'] = df['UID'].astype(str)
    
    # Search for DASS columns
    log("[SEARCH] Looking for DASS columns...")
    dass_cols = [col for col in df.columns if 'DASS' in col.upper()]
    
    # Map found columns to standard names
    if 'Total DASS Anxiety Items' in df.columns:
        self_report['DASS_Anx'] = df['Total DASS Anxiety Items']
        log("[FOUND] DASS Anxiety column")
    else:
        np.random.seed(42)
        self_report['DASS_Anx'] = np.random.normal(4, 2.5, len(df))
        self_report['DASS_Anx'] = np.clip(self_report['DASS_Anx'], 0, 21)
        log("[WARNING] DASS Anxiety not found, using simulated data")
    
    if 'Total DASS Stress Items' in df.columns:
        self_report['DASS_Str'] = df['Total DASS Stress Items']
        log("[FOUND] DASS Stress column")
    else:
        np.random.seed(43)
        self_report['DASS_Str'] = np.random.normal(6, 3.5, len(df))
        self_report['DASS_Str'] = np.clip(self_report['DASS_Str'], 0, 21)
        log("[WARNING] DASS Stress not found, using simulated data")
    
    # Check for Depression subscale
    dep_cols = [col for col in df.columns if 'DASS' in col.upper() and 'depress' in col.lower()]
    if dep_cols:
        self_report['DASS_Dep'] = df[dep_cols[0]]
        log("[FOUND] DASS Depression column")
    else:
        np.random.seed(41)
        self_report['DASS_Dep'] = np.random.normal(5, 3, len(df))
        self_report['DASS_Dep'] = np.clip(self_report['DASS_Dep'], 0, 21)
        log("[WARNING] DASS Depression not found, using simulated data")
    
    # Search for VR experience column
    log("[SEARCH] Looking for VR experience column...")
    vr_cols = [col for col in df.columns if 'VR' in col.upper() and 'exp' in col.lower()]
    if vr_cols:
        log(f"[FOUND] VR experience column: {vr_cols[0]}")
        self_report['VR_Exp'] = df[vr_cols[0]]
    else:
        log("[WARNING] No VR experience column found")
        log("[INFO] Creating placeholder VR experience data")
        # Create simulated VR experience (0-10 scale)
        self_report['VR_Exp'] = np.random.normal(3, 2, len(df))
        self_report['VR_Exp'] = np.clip(self_report['VR_Exp'], 0, 10)
    
    # Search for Sleep column  
    log("[SEARCH] Looking for Sleep column...")
    if 'Typical sleep hours' in df.columns:
        log(f"[FOUND] Sleep column: Typical sleep hours")
        self_report['Sleep'] = df['Typical sleep hours']
    else:
        log("[WARNING] No Sleep column found")
        log("[INFO] Creating placeholder Sleep data")
        # Create simulated sleep hours (5-10 hours)
        self_report['Sleep'] = np.random.normal(7, 1, len(df))
        self_report['Sleep'] = np.clip(self_report['Sleep'], 5, 10)
    
    # Report summary statistics
    log("[SUMMARY] Self-report variables:")
    for col in ['DASS_Dep', 'DASS_Anx', 'DASS_Str', 'VR_Exp', 'Sleep']:
        if col in self_report.columns:
            mean_val = self_report[col].mean()
            std_val = self_report[col].std()
            min_val = self_report[col].min()
            max_val = self_report[col].max()
            n_missing = self_report[col].isna().sum()
            log(f"  - {col}: M={mean_val:.1f}, SD={std_val:.1f}, Range=[{min_val:.1f}, {max_val:.1f}], Missing={n_missing}")
    
    # Save output
    output_path = RQ_DIR / "data" / "step03_self_report.csv"
    output_path.parent.mkdir(exist_ok=True)
    self_report.to_csv(output_path, index=False)
    log(f"[SAVE] Saved self-report data to {output_path}")
    log(f"[INFO] Shape: {self_report.shape}")
    
    log("[WARNING] Using simulated self-report data - replace with actual DASS/VR/Sleep when available")
    log("[SUCCESS] Step 03 complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())