#!/usr/bin/env python3
"""
Step 02: Extract Demographics
RQ 7.1.4: Unique REMEMVR variance unexplained by all predictors

Extract age, sex, and education from dfnonvr.csv
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
LOG_FILE = RQ_DIR / "logs" / "step02_extract_demographics.log"
LOG_FILE.parent.mkdir(exist_ok=True)

def log(msg):
    """Log to both console and file."""
    print(msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{msg}\n")
        f.flush()

def main():
    """Main execution."""
    log("[START] Step 02: Extract demographics")
    
    # Load participant data
    log("[LOAD] Reading dfnonvr.csv...")
    df = pd.read_csv(PROJ_ROOT / "data" / "dfnonvr.csv")
    log(f"[INFO] Loaded {len(df)} participants")
    
    # Initialize output dataframe
    demographics = pd.DataFrame()
    demographics['uid'] = df['UID'].astype(str)
    
    # Extract age
    if 'Age in years' in df.columns:
        demographics['age'] = df['Age in years']
        log(f"[EXTRACT] Age: M={demographics['age'].mean():.1f}, SD={demographics['age'].std():.1f}, Range=[{demographics['age'].min():.0f}, {demographics['age'].max():.0f}]")
    else:
        log("[WARNING] Age column not found")
        demographics['age'] = np.nan
    
    # Extract sex (already coded as 0=female, 1=male)
    if 'Sex 0=female 1=male' in df.columns:
        demographics['sex'] = df['Sex 0=female 1=male']
        demographics['sex_binary'] = demographics['sex']  # Already binary
        n_female = (demographics['sex'] == 0).sum()
        n_male = (demographics['sex'] == 1).sum()
        log(f"[EXTRACT] Sex: {n_female} female, {n_male} male")
    else:
        log("[WARNING] Sex column not found")
        demographics['sex'] = np.nan
        demographics['sex_binary'] = np.nan
    
    # Extract education - need to find the right column
    education_cols = [col for col in df.columns if 'education' in col.lower() or 'educ' in col.lower()]
    if education_cols:
        # Use the first education column found
        edu_col = education_cols[0]
        log(f"[INFO] Found education column: {edu_col}")
        
        # Map education levels to numeric scale if needed
        # Common mapping: High school=12, Some college=14, Bachelor's=16, Graduate=18
        demographics['education'] = df[edu_col]
        
        # If education is categorical, try to convert to years
        if demographics['education'].dtype == 'object':
            log("[INFO] Converting categorical education to years of education...")
            edu_mapping = {
                'high school': 12,
                'some college': 14,
                'associate': 14,
                'bachelor': 16,
                'master': 18,
                'doctorate': 20,
                'phd': 20
            }
            
            # Try to map values
            demographics['education_years'] = demographics['education'].apply(
                lambda x: next((v for k, v in edu_mapping.items() if k in str(x).lower()), np.nan) if pd.notna(x) else np.nan
            )
            
            # If mapping didn't work well, use ordinal encoding
            if demographics['education_years'].isna().sum() > len(demographics) * 0.5:
                log("[INFO] Categorical mapping failed, using ordinal encoding")
                demographics['education_years'] = pd.Categorical(demographics['education']).codes
                demographics['education_years'] = demographics['education_years'].replace(-1, np.nan)
        else:
            demographics['education_years'] = demographics['education']
        
        valid_edu = demographics['education_years'].dropna()
        if len(valid_edu) > 0:
            log(f"[EXTRACT] Education: M={valid_edu.mean():.1f}, SD={valid_edu.std():.1f}, Range=[{valid_edu.min():.0f}, {valid_edu.max():.0f}]")
    else:
        log("[WARNING] Education column not found")
        demographics['education'] = np.nan
        demographics['education_years'] = np.nan
    
    # Select final columns for output
    output_cols = ['uid', 'age', 'sex', 'sex_binary']
    if 'education_years' in demographics.columns:
        output_cols.append('education_years')
        # Rename for consistency
        demographics['education'] = demographics['education_years']
        output_cols = ['uid', 'age', 'sex', 'sex_binary', 'education']
    else:
        output_cols.append('education')
    
    demographics = demographics[output_cols]
    
    # Check for missing values
    log("[CHECK] Missing values:")
    for col in demographics.columns:
        n_missing = demographics[col].isna().sum()
        if n_missing > 0:
            log(f"  - {col}: {n_missing} missing")
    
    # Save output
    output_path = RQ_DIR / "data" / "step02_demographics.csv"
    output_path.parent.mkdir(exist_ok=True)
    demographics.to_csv(output_path, index=False)
    log(f"[SAVE] Saved demographics to {output_path}")
    log(f"[INFO] Shape: {demographics.shape}")
    
    log("[SUCCESS] Step 02 complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())