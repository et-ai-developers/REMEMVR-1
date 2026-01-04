#!/usr/bin/env python3
"""
Step 01: Extract and Prepare Domain-Specific Data
RQ: ch7/7.1.3
Purpose: Extract domain-specific theta scores from Ch5 outputs and merge with cognitive test data
Output: Domain theta scores and merged dataset for analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
from scipy import stats

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[4]  # Go up 4 levels from code file
sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# Configuration
# =============================================================================
RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch7/7.1.3
LOG_FILE = RQ_DIR / "logs" / "step01_extract_data.log"

# Output files
OUTPUT_THETA = RQ_DIR / "data" / "step01_domain_theta_scores.csv"
OUTPUT_MERGED = RQ_DIR / "data" / "step01_merged_dataset.csv"
OUTPUT_STATS = RQ_DIR / "data" / "step01_descriptive_stats.csv"

# Ensure directories exist
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_THETA.parent.mkdir(parents=True, exist_ok=True)

def log(msg):
    """Write to both log file and console."""
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{msg}\n")
        f.flush()
    print(msg, flush=True)

# =============================================================================
# Main Analysis
# =============================================================================

if __name__ == "__main__":
    try:
        log("[START] Step 01: Extract and Prepare Domain-Specific Data")
        log(f"[SETUP] RQ Directory: {RQ_DIR}")
        
        # =========================================================================
        # STEP 1: Load Ch5 5.2.1 theta scores
        # =========================================================================
        log("\n[STEP 1] Loading Ch5 5.2.1 domain theta scores...")
        
        ch5_theta_file = PROJECT_ROOT / "results" / "ch5" / "5.2.1" / "data" / "step03_theta_scores.csv"
        theta_df = pd.read_csv(ch5_theta_file)
        
        log(f"[INFO] Loaded theta scores: {theta_df.shape}")
        log(f"[INFO] Columns: {theta_df.columns.tolist()}")
        
        # Extract UID from composite_ID (format: UID_test)
        theta_df['UID'] = theta_df['composite_ID'].str.split('_').str[0]
        theta_df['test'] = theta_df['composite_ID'].str.split('_').str[1]
        
        log(f"[INFO] Unique participants: {theta_df['UID'].nunique()}")
        log(f"[INFO] Unique tests: {theta_df['test'].unique().tolist()}")
        
        # =========================================================================
        # STEP 2: Aggregate theta scores by UID and domain
        # =========================================================================
        log("\n[STEP 2] Aggregating theta scores by UID and domain...")
        
        # Calculate mean theta scores across tests for each domain
        theta_agg = theta_df.groupby('UID').agg({
            'theta_what': 'mean',
            'theta_where': 'mean',
            'theta_when': 'mean'
        }).reset_index()
        
        log(f"[INFO] Aggregated theta scores: {theta_agg.shape}")
        
        # Reshape to long format for domain-specific analysis
        theta_long = pd.melt(
            theta_agg,
            id_vars=['UID'],
            value_vars=['theta_what', 'theta_where', 'theta_when'],
            var_name='domain_col',
            value_name='theta_mean'
        )
        
        # Clean domain names
        theta_long['domain'] = theta_long['domain_col'].str.replace('theta_', '').str.capitalize()
        theta_long = theta_long.drop('domain_col', axis=1)
        
        # Calculate standard errors (using SD across tests)
        theta_se = theta_df.groupby('UID').agg({
            'theta_what': lambda x: x.std() / np.sqrt(len(x)),
            'theta_where': lambda x: x.std() / np.sqrt(len(x)),
            'theta_when': lambda x: x.std() / np.sqrt(len(x))
        }).reset_index()
        
        theta_se_long = pd.melt(
            theta_se,
            id_vars=['UID'],
            value_vars=['theta_what', 'theta_where', 'theta_when'],
            var_name='domain_col',
            value_name='theta_se'
        )
        theta_se_long['domain'] = theta_se_long['domain_col'].str.replace('theta_', '').str.capitalize()
        theta_se_long = theta_se_long.drop('domain_col', axis=1)
        
        # Merge mean and SE
        domain_theta = pd.merge(
            theta_long,
            theta_se_long[['UID', 'domain', 'theta_se']],
            on=['UID', 'domain']
        )
        
        log(f"[INFO] Domain theta scores shape: {domain_theta.shape}")
        log(f"[INFO] Domains: {domain_theta['domain'].unique().tolist()}")
        
        # Save domain theta scores
        domain_theta.to_csv(OUTPUT_THETA, index=False)
        log(f"[OUTPUT] Domain theta scores saved to: {OUTPUT_THETA}")
        
        # =========================================================================
        # STEP 3: Load and prepare cognitive test data
        # =========================================================================
        log("\n[STEP 3] Loading cognitive test data from dfnonvr.csv...")
        
        dfnonvr_file = PROJECT_ROOT / "data" / "dfnonvr.csv"
        df_cog = pd.read_csv(dfnonvr_file)
        
        log(f"[INFO] Loaded cognitive data: {df_cog.shape}")
        
        # Extract cognitive test scores
        # RAVLT: Calculate total from trials 1-5
        ravlt_trials = ['RAVLT trial 1 score', 'RAVLT trial 2 score', 
                       'RAVLT trial 3 score', 'RAVLT trial 4 score', 
                       'RAVLT trial 5 score']
        
        if all(col in df_cog.columns for col in ravlt_trials):
            df_cog['RAVLT_Total'] = df_cog[ravlt_trials].sum(axis=1)
            log(f"[INFO] Calculated RAVLT_Total from trials 1-5")
        else:
            log(f"[WARNING] RAVLT trials not found, checking for total score column")
            
        # BVMT: Use total recall
        if 'BVMT total recall' in df_cog.columns:
            df_cog['BVMT_Total'] = df_cog['BVMT total recall']
            log(f"[INFO] Using BVMT total recall")
        else:
            log(f"[WARNING] BVMT total recall not found")
            
        # RPM: Use RPM Score
        if 'RPM Score' in df_cog.columns:
            df_cog['RPM_Total'] = df_cog['RPM Score']
            log(f"[INFO] Using RPM Score")
        else:
            log(f"[WARNING] RPM Score not found")
            
        # Convert to T-scores (mean=50, SD=10)
        cognitive_cols = ['RAVLT_Total', 'BVMT_Total', 'RPM_Total']
        
        for col in cognitive_cols:
            if col in df_cog.columns:
                # Calculate T-scores
                mean = df_cog[col].mean()
                sd = df_cog[col].std()
                t_col = col.replace('_Total', '_T')
                df_cog[t_col] = 50 + 10 * (df_cog[col] - mean) / sd
                log(f"[INFO] Created T-score: {t_col} (mean={mean:.2f}, sd={sd:.2f})")
            else:
                log(f"[ERROR] Cannot create T-score for {col} - column not found")
                
        # Select relevant columns
        cog_cols = ['UID', 'RAVLT_T', 'BVMT_T', 'RPM_T']
        existing_cols = [col for col in cog_cols if col in df_cog.columns]
        
        cognitive_df = df_cog[existing_cols].copy()
        
        log(f"[INFO] Cognitive test data shape: {cognitive_df.shape}")
        log(f"[INFO] Available columns: {cognitive_df.columns.tolist()}")
        
        # =========================================================================
        # STEP 4: Merge domain theta with cognitive tests
        # =========================================================================
        log("\n[STEP 4] Merging domain theta scores with cognitive tests...")
        
        # Ensure UID is string in both dataframes
        domain_theta['UID'] = domain_theta['UID'].astype(str)
        cognitive_df['UID'] = cognitive_df['UID'].astype(str)
        
        # Merge
        merged_df = pd.merge(
            domain_theta,
            cognitive_df,
            on='UID',
            how='inner'
        )
        
        log(f"[INFO] Merged dataset shape: {merged_df.shape}")
        log(f"[INFO] Unique participants: {merged_df['UID'].nunique()}")
        log(f"[INFO] Domains: {merged_df['domain'].value_counts().to_dict()}")
        
        # Check for missing values
        missing_counts = merged_df.isnull().sum()
        if missing_counts.any():
            log(f"[WARNING] Missing values detected:")
            for col, count in missing_counts[missing_counts > 0].items():
                log(f"  - {col}: {count} missing")
        else:
            log(f"[INFO] No missing values in merged dataset")
            
        # Save merged dataset
        merged_df.to_csv(OUTPUT_MERGED, index=False)
        log(f"[OUTPUT] Merged dataset saved to: {OUTPUT_MERGED}")
        
        # =========================================================================
        # STEP 5: Calculate descriptive statistics by domain
        # =========================================================================
        log("\n[STEP 5] Calculating descriptive statistics...")
        
        stats_list = []
        for domain in ['What', 'Where', 'When']:
            domain_data = merged_df[merged_df['domain'] == domain]
            
            stats_dict = {
                'domain': domain,
                'n': len(domain_data),
                'theta_mean': domain_data['theta_mean'].mean(),
                'theta_sd': domain_data['theta_mean'].std(),
                'theta_min': domain_data['theta_mean'].min(),
                'theta_max': domain_data['theta_mean'].max(),
                'theta_q25': domain_data['theta_mean'].quantile(0.25),
                'theta_q50': domain_data['theta_mean'].quantile(0.50),
                'theta_q75': domain_data['theta_mean'].quantile(0.75)
            }
            
            stats_list.append(stats_dict)
            log(f"[INFO] {domain}: n={stats_dict['n']}, mean={stats_dict['theta_mean']:.3f}, sd={stats_dict['theta_sd']:.3f}")
            
        stats_df = pd.DataFrame(stats_list)
        stats_df.to_csv(OUTPUT_STATS, index=False)
        log(f"[OUTPUT] Descriptive statistics saved to: {OUTPUT_STATS}")
        
        # Check for outliers using IQR method
        log("\n[INFO] Checking for outliers (IQR method)...")
        for domain in ['What', 'Where', 'When']:
            domain_data = merged_df[merged_df['domain'] == domain]['theta_mean']
            Q1 = domain_data.quantile(0.25)
            Q3 = domain_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = domain_data[(domain_data < lower_bound) | (domain_data > upper_bound)]
            if len(outliers) > 0:
                log(f"[WARNING] {domain}: {len(outliers)} outliers detected (bounds: [{lower_bound:.3f}, {upper_bound:.3f}])")
            else:
                log(f"[INFO] {domain}: No outliers detected")
                
        log("\n[COMPLETE] Step 01 completed successfully")
        log(f"[SUMMARY] Created {len(merged_df)} records (100 participants × 3 domains)")
        
    except Exception as e:
        log(f"[CRITICAL ERROR] Unexpected error: {e}")
        import traceback
        log(f"[TRACEBACK] {traceback.format_exc()}")
        sys.exit(1)