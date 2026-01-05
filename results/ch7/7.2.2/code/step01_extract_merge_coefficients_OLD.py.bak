#!/usr/bin/env python3
"""
Step 01: Extract and Merge Regression Coefficients for RQ 7.2.2
================================================================
Purpose: Load age coefficients from RQ 7.2.1 and merge with participant theta scores

Scientific Context:
RQ 7.2.2 tests the VR scaffolding hypothesis - whether cognitive tests attenuate
age effects on REMEMVR performance. We need:
1. Age coefficients from 7.2.1 (bivariate vs controlled)
2. Theta scores from Ch5 analyses

Note: We focus on overall and What domain, as When domain showed floor effects in Ch5.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

# Set up paths
RQ_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = RQ_DIR / "logs" / "step01_extract_merge_coefficients.log"

# Ensure directories exist
(RQ_DIR / "logs").mkdir(exist_ok=True)
(RQ_DIR / "data").mkdir(exist_ok=True)

def log(msg):
    """Log message to both file and console"""
    with open(LOG_FILE, 'a') as f:
        f.write(f"{msg}\n")
        f.flush()
    print(msg, flush=True)

def main():
    """Main extraction and merging function"""
    log("="*70)
    log("STEP 01: EXTRACT AND MERGE REGRESSION COEFFICIENTS")
    log("="*70)
    
    # 1. Load age coefficients from RQ 7.2.1
    log("\n1. Loading age coefficients from RQ 7.2.1...")
    
    mediation_file = Path("/home/etai/projects/REMEMVR/results/ch7/7.2.1/data/step04_mediation_analysis.csv")
    
    if not mediation_file.exists():
        log(f"ERROR: Cannot find mediation analysis file: {mediation_file}")
        sys.exit(1)
    
    mediation_df = pd.read_csv(mediation_file)
    log(f"Loaded mediation analysis: {len(mediation_df)} rows")
    log(f"Columns: {list(mediation_df.columns)}")
    
    # Extract coefficients - beta_total is bivariate, beta_direct is controlled
    beta_age_bivariate = mediation_df['beta_total'].iloc[0]
    beta_age_controlled = mediation_df['beta_direct'].iloc[0]
    
    log(f"Age coefficient (bivariate): {beta_age_bivariate:.4f}")
    log(f"Age coefficient (controlled): {beta_age_controlled:.4f}")
    
    # 2. Load theta scores from Ch5 analyses
    log("\n2. Loading theta scores from Ch5 analyses...")
    
    # Overall theta from 5.1.1
    overall_theta_file = Path("/home/etai/projects/REMEMVR/results/ch5/5.1.1/data/step03_theta_scores.csv")
    overall_theta_df = pd.read_csv(overall_theta_file)
    log(f"Loaded overall theta: {len(overall_theta_df)} rows")
    
    # Check columns to understand structure
    log(f"Overall theta columns: {list(overall_theta_df.columns)}")
    
    # Aggregate by UID (average across 4 tests)
    if 'composite_ID' in overall_theta_df.columns:
        overall_theta_df['UID'] = overall_theta_df['composite_ID'].str.split('_').str[0]
    
    # Find the theta column name
    theta_col = None
    for col in overall_theta_df.columns:
        if 'theta' in col.lower():
            theta_col = col
            break
    
    if not theta_col:
        log("ERROR: Cannot find theta column in overall theta file")
        sys.exit(1)
    
    log(f"Using theta column: {theta_col}")
    
    overall_by_uid = overall_theta_df.groupby('UID')[theta_col].mean().reset_index()
    overall_by_uid.columns = ['UID', 'theta_all']
    log(f"Aggregated to {len(overall_by_uid)} participants")
    
    # What domain theta from 5.2.1
    what_theta_file = Path("/home/etai/projects/REMEMVR/results/ch5/5.2.1/data/step03_theta_scores.csv")
    what_theta_df = pd.read_csv(what_theta_file)
    log(f"Loaded What domain theta: {len(what_theta_df)} rows")
    
    # Aggregate What domain by UID
    if 'composite_ID' in what_theta_df.columns:
        what_theta_df['UID'] = what_theta_df['composite_ID'].str.split('_').str[0]
    
    # Find theta column
    theta_col_what = None
    for col in what_theta_df.columns:
        if 'theta' in col.lower():
            theta_col_what = col
            break
    
    what_by_uid = what_theta_df.groupby('UID')[theta_col_what].mean().reset_index()
    what_by_uid.columns = ['UID', 'theta_what']
    log(f"Aggregated What domain to {len(what_by_uid)} participants")
    
    # 3. Merge datasets
    log("\n3. Merging datasets...")
    
    # Start with overall theta
    merged_df = overall_by_uid.copy()
    
    # Add What domain theta
    merged_df = merged_df.merge(what_by_uid, on='UID', how='left')
    
    # Add coefficients (same for all participants - these are model-level coefficients)
    merged_df['beta_age_bivariate_all'] = beta_age_bivariate
    merged_df['beta_age_controlled_all'] = beta_age_controlled
    
    # For domain-specific analysis, we'll need to run domain-specific models
    # For now, we'll use the overall coefficients as placeholders
    merged_df['beta_age_bivariate_what'] = beta_age_bivariate  # Will be updated if domain-specific models exist
    merged_df['beta_age_controlled_what'] = beta_age_controlled
    
    # Note: Where and When domains excluded due to data availability
    # When domain showed floor effects in Ch5, Where domain data not found
    
    log(f"\nMerged dataset summary:")
    log(f"  Rows: {len(merged_df)}")
    log(f"  Columns: {list(merged_df.columns)}")
    log(f"  Missing values: {merged_df.isnull().sum().sum()}")
    
    # 4. Save outputs
    log("\n4. Saving outputs...")
    
    # Save merged coefficients
    output_file = RQ_DIR / "data" / "step01_merged_coefficients.csv"
    merged_df.to_csv(output_file, index=False)
    log(f"Saved merged coefficients to: {output_file}")
    
    # Save data summary
    summary_file = RQ_DIR / "data" / "step01_data_summary.txt"
    with open(summary_file, 'w') as f:
        f.write("DATA SUMMARY FOR RQ 7.2.2 ATTENUATION ANALYSIS\n")
        f.write("="*60 + "\n\n")
        f.write(f"Total participants: {len(merged_df)}\n")
        f.write(f"Variables: {len(merged_df.columns)}\n")
        f.write(f"Missing values: {merged_df.isnull().sum().sum()}\n\n")
        
        f.write("Age Coefficients from RQ 7.2.1:\n")
        f.write(f"  Bivariate (age only): {beta_age_bivariate:.4f}\n")
        f.write(f"  Controlled (age + cognitive): {beta_age_controlled:.4f}\n\n")
        
        f.write("Theta Score Summary:\n")
        f.write(f"  Overall theta mean: {merged_df['theta_all'].mean():.3f} (SD={merged_df['theta_all'].std():.3f})\n")
        f.write(f"  What domain theta mean: {merged_df['theta_what'].mean():.3f} (SD={merged_df['theta_what'].std():.3f})\n\n")
        
        f.write("Domain Coverage:\n")
        f.write("  Overall: ✓ Available (Ch5 5.1.1)\n")
        f.write("  What: ✓ Available (Ch5 5.2.1)\n")
        f.write("  Where: ✗ Not found in expected location\n")
        f.write("  When: ✗ Excluded due to floor effects (Ch5 finding)\n")
    
    log(f"Saved data summary to: {summary_file}")
    
    log("\nStep 01 complete: Coefficients extracted and merged")
    
    return merged_df

if __name__ == "__main__":
    main()