#!/usr/bin/env python3
"""
Step 2: Extract and Prepare RAVLT and Age Data
RQ 7.2.4 - VR Scaffolding Validation

Purpose: Extract RAVLT scores and age from dfnonvr.csv with total score calculation
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Setup paths
RQ_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = RQ_DIR / "logs" / "step02_extract_ravlt.log"

def log(msg):
    """Log to both file and stdout"""
    with open(LOG_FILE, 'a') as f:
        f.write(f"{msg}\n")
        f.flush()
    print(msg, flush=True)

def main():
    log("=" * 60)
    log("Step 2: Extract RAVLT and Age Data")
    log("=" * 60)
    
    # Read dfnonvr.csv
    dfnonvr_path = Path("data/dfnonvr.csv")
    log(f"Reading participant data from: {dfnonvr_path}")
    
    df_master = pd.read_csv(dfnonvr_path)
    log(f"Loaded {len(df_master)} rows with {len(df_master.columns)} columns")
    
    # Define RAVLT trial columns and age column
    ravlt_cols = ['RAVLT trial 1 score', 'RAVLT trial 2 score', 'RAVLT trial 3 score', 
                  'RAVLT trial 4 score', 'RAVLT trial 5 score', 'RAVLT delayed recall score']
    age_col = 'Age in years'
    
    # Verify columns exist
    missing_cols = [col for col in ravlt_cols + [age_col] if col not in df_master.columns]
    if missing_cols:
        log(f"ERROR: Missing columns: {missing_cols}")
        sys.exit(1)
    
    log("All required columns found")
    
    # Extract relevant columns
    df_ravlt = df_master[['UID'] + ravlt_cols + [age_col]].copy()
    
    # Ensure UID is string type
    df_ravlt['UID'] = df_ravlt['UID'].astype(str)
    
    # Calculate RAVLT_Total as sum of trials 1-5 + delayed recall
    log("Calculating RAVLT_Total as sum of trials 1-5 + delayed recall")
    df_ravlt['RAVLT_Total'] = df_ravlt[ravlt_cols].sum(axis=1)
    
    # Rename Age column for consistency
    df_ravlt = df_ravlt.rename(columns={'Age in years': 'Age'})
    
    # Check for missing data
    n_before = len(df_ravlt)
    df_ravlt = df_ravlt.dropna(subset=['RAVLT_Total', 'Age'])
    n_after = len(df_ravlt)
    
    if n_before != n_after:
        log(f"Removed {n_before - n_after} participants with missing data")
    
    # Standardize RAVLT scores (z-score transformation)
    ravlt_mean = df_ravlt['RAVLT_Total'].mean()
    ravlt_std = df_ravlt['RAVLT_Total'].std()
    df_ravlt['RAVLT_Total_z'] = (df_ravlt['RAVLT_Total'] - ravlt_mean) / ravlt_std
    
    # Quality checks
    n_participants = len(df_ravlt)
    age_min, age_max = df_ravlt['Age'].min(), df_ravlt['Age'].max()
    age_mean, age_std = df_ravlt['Age'].mean(), df_ravlt['Age'].std()
    age_range = age_max - age_min
    age_variance = df_ravlt['Age'].var()
    
    log(f"\nRESULTS:")
    log(f"RAVLT data extracted: {n_participants} participants")
    log(f"RAVLT descriptives: mean={ravlt_mean:.1f}, sd={ravlt_std:.1f}")
    log(f"RAVLT range: min={df_ravlt['RAVLT_Total'].min():.1f}, max={df_ravlt['RAVLT_Total'].max():.1f}")
    log(f"Age descriptives: mean={age_mean:.1f}, sd={age_std:.1f}")
    log(f"Age range: {age_min:.0f}-{age_max:.0f} years (range={age_range:.0f})")
    log(f"Age variance: {age_variance:.1f}")
    
    # Check for adequate age variance for correlation
    if age_range < 20:
        log(f"WARNING: Insufficient age variance - range only {age_range:.0f} years")
    else:
        log(f"Age range {age_range:.0f} years: adequate variance for correlation")
    
    # Check for ceiling/floor effects in RAVLT
    ravlt_min_possible = 0
    ravlt_max_possible = 90  # 15 words * 6 trials
    pct_at_floor = (df_ravlt['RAVLT_Total'] <= 10).mean() * 100
    pct_at_ceiling = (df_ravlt['RAVLT_Total'] >= 80).mean() * 100
    
    log(f"\nCeiling/floor effects check:")
    log(f"  - At floor (≤10): {pct_at_floor:.1f}%")
    log(f"  - At ceiling (≥80): {pct_at_ceiling:.1f}%")
    
    if pct_at_floor > 5 or pct_at_ceiling > 5:
        log("WARNING: Potential ceiling/floor effects detected")
    
    # Verify standardization
    z_mean = df_ravlt['RAVLT_Total_z'].mean()
    z_std = df_ravlt['RAVLT_Total_z'].std()
    log(f"\nStandardization verification: z_mean={z_mean:.6f}, z_std={z_std:.6f}")
    
    # Select final columns and save
    df_final = df_ravlt[['UID', 'RAVLT_Total', 'RAVLT_Total_z', 'Age']]
    
    output_path = RQ_DIR / "data" / "step02_ravlt_age_data.csv"
    df_final.to_csv(output_path, index=False)
    log(f"\nSaved to: {output_path}")
    log(f"Output shape: {df_final.shape}")
    
    # Final verification
    log("\nFinal data check:")
    log(f"  - Participants: {n_participants}")
    log(f"  - Columns: {list(df_final.columns)}")
    log(f"  - No missing values: {df_final.isnull().sum().sum() == 0}")
    log(f"  - All finite values: {np.isfinite(df_final.select_dtypes(include=[np.number])).all().all()}")
    
    log("\nStep 2 completed successfully")

if __name__ == "__main__":
    main()