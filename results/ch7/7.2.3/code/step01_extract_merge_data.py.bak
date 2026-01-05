#!/usr/bin/env python3
"""
Step 1: Extract and Merge Data for RQ 7.2.3
Purpose: Extract mean theta_all scores from Ch5 and cognitive test data, then merge

Scientific Context:
- Testing Age x Cognitive Test interactions on REMEMVR performance
- Cognitive Reserve Theory predicts stronger test prediction in older adults
- VR Scaffolding Hypothesis predicts equal prediction across ages
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

# Define paths
RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch7/7.2.3
CH5_DIR = PROJECT_ROOT / "results" / "ch5" / "5.1.1"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = RQ_DIR / "data"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

def extract_theta_scores():
    """Extract and aggregate theta_all scores from Ch5 5.1.1."""
    
    # Load Ch5 theta scores
    theta_file = CH5_DIR / "data" / "step03_theta_scores.csv"
    theta_df = pd.read_csv(theta_file)
    
    print(f"Loaded {len(theta_df)} theta scores from Ch5 5.1.1")
    print(f"Unique participants: {theta_df['UID'].nunique()}")
    
    # Aggregate to mean theta per participant
    theta_means = theta_df.groupby('UID')['Theta_All'].mean().reset_index()
    theta_means.columns = ['UID', 'theta_all']
    
    print(f"\nAggregated to {len(theta_means)} participant means")
    print(f"Theta_all range: [{theta_means['theta_all'].min():.3f}, {theta_means['theta_all'].max():.3f}]")
    print(f"Theta_all mean (SD): {theta_means['theta_all'].mean():.3f} ({theta_means['theta_all'].std():.3f})")
    
    return theta_means

def extract_cognitive_tests():
    """Extract cognitive test scores and demographics from dfnonvr.csv."""
    
    # Load participant data
    df = pd.read_csv(DATA_DIR / "dfnonvr.csv")
    
    print(f"\nLoaded {len(df)} participants from dfnonvr.csv")
    
    # Extract required variables
    cognitive_df = pd.DataFrame()
    cognitive_df['UID'] = df['UID']
    
    # Age
    cognitive_df['Age'] = df['Age in years']
    
    # Cognitive tests - raw scores
    cognitive_df['NART_raw'] = df['NART Score']
    cognitive_df['RPM_raw'] = df['RPM Score']
    cognitive_df['BVMT_raw'] = df['BVMT total recall']
    
    # RAVLT total = sum of trials 1-5
    ravlt_cols = ['RAVLT trial 1 score', 'RAVLT trial 2 score', 
                  'RAVLT trial 3 score', 'RAVLT trial 4 score', 
                  'RAVLT trial 5 score']
    cognitive_df['RAVLT_raw'] = df[ravlt_cols].sum(axis=1)
    
    # Convert to T-scores (M=50, SD=10)
    # Using population norms for standardization
    def to_t_score(x):
        """Convert raw scores to T-scores."""
        return 50 + 10 * (x - x.mean()) / x.std()
    
    cognitive_df['RAVLT_T'] = to_t_score(cognitive_df['RAVLT_raw'])
    cognitive_df['BVMT_T'] = to_t_score(cognitive_df['BVMT_raw'])
    cognitive_df['NART_T'] = to_t_score(cognitive_df['NART_raw'])
    cognitive_df['RPM_T'] = to_t_score(cognitive_df['RPM_raw'])
    
    # Keep only needed columns
    final_cols = ['UID', 'Age', 'RAVLT_T', 'BVMT_T', 'NART_T', 'RPM_T']
    cognitive_df = cognitive_df[final_cols]
    
    print(f"\nExtracted cognitive test data:")
    print(f"Age range: [{cognitive_df['Age'].min():.0f}, {cognitive_df['Age'].max():.0f}]")
    print(f"Age mean (SD): {cognitive_df['Age'].mean():.1f} ({cognitive_df['Age'].std():.1f})")
    
    for test in ['RAVLT_T', 'BVMT_T', 'NART_T', 'RPM_T']:
        print(f"{test} mean (SD): {cognitive_df[test].mean():.1f} ({cognitive_df[test].std():.1f})")
    
    return cognitive_df

def merge_datasets(theta_df, cognitive_df):
    """Merge theta scores with cognitive test data."""
    
    # Merge on UID
    merged_df = pd.merge(cognitive_df, theta_df, on='UID', how='inner')
    
    print(f"\nMerged dataset: {len(merged_df)} participants")
    
    # Check for missing data
    missing_count = merged_df.isnull().sum()
    if missing_count.any():
        print("WARNING: Missing data detected:")
        print(missing_count[missing_count > 0])
    else:
        print("No missing data - dataset complete")
    
    return merged_df

def compute_descriptives(df):
    """Compute descriptive statistics for all variables."""
    
    vars_to_describe = ['Age', 'theta_all', 'RAVLT_T', 'BVMT_T', 'NART_T', 'RPM_T']
    
    desc_stats = pd.DataFrame()
    for var in vars_to_describe:
        desc_stats = pd.concat([desc_stats, pd.DataFrame({
            'variable': [var],
            'mean': [df[var].mean()],
            'std': [df[var].std()],
            'min': [df[var].min()],
            'max': [df[var].max()],
            'n_missing': [df[var].isnull().sum()]
        })])
    
    return desc_stats

def main():
    """Main execution function."""
    
    print("=" * 60)
    print("STEP 1: EXTRACT AND MERGE DATA FOR RQ 7.2.3")
    print("=" * 60)
    
    # Extract theta scores from Ch5
    theta_means = extract_theta_scores()
    
    # Extract cognitive tests from dfnonvr
    cognitive_df = extract_cognitive_tests()
    
    # Merge datasets
    merged_df = merge_datasets(theta_means, cognitive_df)
    
    # Compute descriptives
    descriptives = compute_descriptives(merged_df)
    
    print("\n" + "=" * 60)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 60)
    print(descriptives.to_string(index=False))
    
    # Check correlations between predictors
    print("\n" + "=" * 60)
    print("PREDICTOR CORRELATIONS")
    print("=" * 60)
    corr_vars = ['Age', 'RAVLT_T', 'BVMT_T', 'NART_T', 'RPM_T']
    corr_matrix = merged_df[corr_vars].corr()
    print(corr_matrix.round(3))
    
    # Save outputs
    merged_df.to_csv(OUTPUT_DIR / "step01_merged_data.csv", index=False)
    descriptives.to_csv(OUTPUT_DIR / "step01_descriptives.csv", index=False)
    
    print(f"\nOutputs saved:")
    print(f"  - {OUTPUT_DIR / 'step01_merged_data.csv'}")
    print(f"  - {OUTPUT_DIR / 'step01_descriptives.csv'}")
    
    print("\nStep 1 complete: Data extracted and merged successfully")
    
    return merged_df

if __name__ == "__main__":
    main()