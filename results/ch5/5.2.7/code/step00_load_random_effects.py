#!/usr/bin/env python3
"""
RQ 5.2.7 Step 00: Load Random Effects from RQ 5.2.6

Purpose: Load domain-specific random effects (intercepts and slopes) from RQ 5.2.6
         and pivot from long to wide format for clustering.

Input:
  - results/ch5/5.2.6/data/step04_random_effects.csv (200 rows: 100 UID × 2 domains)

Output:
  - data/step00_random_effects_from_rq526.csv (100 rows × 5 cols: UID + 4 clustering variables)

When Domain Exclusion: When domain was excluded in RQ 5.2.6 due to floor effect (RQ 5.2.1).
"""

import sys
from pathlib import Path

import pandas as pd

# Setup paths
SCRIPT_DIR = Path(__file__).parent
RQ_DIR = SCRIPT_DIR.parent
DATA_DIR = RQ_DIR / "data"
LOG_DIR = RQ_DIR / "logs"

# Source file from RQ 5.2.6
SOURCE_FILE = RQ_DIR.parent / "5.2.6" / "data" / "step04_random_effects.csv"


def main():
    print("=" * 60)
    print("RQ 5.2.7 Step 00: Load Random Effects from RQ 5.2.6")
    print("=" * 60)

    # Circuit breaker: Check dependency file exists
    if not SOURCE_FILE.exists():
        print(f"\nERROR: Dependency file not found: {SOURCE_FILE}")
        print("RQ 5.2.6 must complete Step 4 (extract random effects) before RQ 5.2.7 can run")
        sys.exit(1)

    # Load source data
    print(f"\nLoading: {SOURCE_FILE}")
    df = pd.read_csv(SOURCE_FILE)
    print(f"Loaded {len(df)} rows from RQ 5.2.6")

    # Validate structure
    expected_cols = ['UID', 'domain', 'Total_Intercept', 'Total_Slope']
    missing_cols = [c for c in expected_cols if c not in df.columns]
    if missing_cols:
        print(f"\nERROR: Missing columns: {missing_cols}")
        sys.exit(1)

    # Check domains
    domains = df['domain'].unique()
    print(f"Domains found: {list(domains)}")

    # Validate: Only What and Where expected (When excluded)
    expected_domains = {'What', 'Where'}
    if set(domains) != expected_domains:
        print(f"\nERROR: Expected domains {expected_domains}, found {set(domains)}")
        sys.exit(1)

    # Check row count
    n_rows = len(df)
    n_uids = df['UID'].nunique()
    n_domains = len(domains)
    expected_rows = 200  # 100 UIDs × 2 domains

    print(f"\nValidation:")
    print(f"  - Total rows: {n_rows} (expected: {expected_rows})")
    print(f"  - Unique UIDs: {n_uids} (expected: 100)")
    print(f"  - Domains: {n_domains} (expected: 2)")

    if n_rows != expected_rows:
        print(f"\nERROR: Expected {expected_rows} rows, found {n_rows}")
        sys.exit(1)

    if n_uids != 100:
        print(f"\nERROR: Expected 100 UIDs, found {n_uids}")
        sys.exit(1)

    # Pivot from long to wide format
    print("\nPivoting from long to wide format...")

    # Select only needed columns for pivot
    df_pivot = df[['UID', 'domain', 'Total_Intercept', 'Total_Slope']].copy()

    # Pivot: rows=UID, columns=domain, values=Intercept and Slope
    df_wide = df_pivot.pivot(
        index='UID',
        columns='domain',
        values=['Total_Intercept', 'Total_Slope']
    )

    # Flatten column names: (metric, domain) -> metric_domain
    df_wide.columns = [f'{metric}_{domain}' for metric, domain in df_wide.columns]
    df_wide = df_wide.reset_index()

    print(f"Pivoted to wide format: {len(df_wide)} rows x {len(df_wide.columns)} columns")

    # Validate wide format
    expected_wide_cols = [
        'UID',
        'Total_Intercept_What', 'Total_Intercept_Where',
        'Total_Slope_What', 'Total_Slope_Where'
    ]

    # Reorder columns to expected order
    df_wide = df_wide[expected_wide_cols]

    print(f"\nWide format columns: {list(df_wide.columns)}")

    # Check for missing values
    n_missing = df_wide.isnull().sum().sum()
    if n_missing > 0:
        print(f"\nERROR: {n_missing} missing values detected after pivot")
        print(df_wide.isnull().sum())
        sys.exit(1)
    else:
        print("No missing values detected")

    # Check for duplicate UIDs
    n_duplicates = df_wide['UID'].duplicated().sum()
    if n_duplicates > 0:
        print(f"\nERROR: {n_duplicates} duplicate UIDs detected")
        sys.exit(1)

    # Value range validation
    print("\nValue ranges:")
    for col in df_wide.columns:
        if col != 'UID':
            min_val = df_wide[col].min()
            max_val = df_wide[col].max()
            print(f"  - {col}: [{min_val:.3f}, {max_val:.3f}]")

            # Check reasonable ranges
            if 'Intercept' in col and (min_val < -3 or max_val > 3):
                print(f"    WARNING: Intercepts outside typical [-3, 3] range")
            if 'Slope' in col and (min_val < -2 or max_val > 2):
                print(f"    WARNING: Slopes outside typical [-2, 2] range")

    # Save output
    output_file = DATA_DIR / "step00_random_effects_from_rq526.csv"
    df_wide.to_csv(output_file, index=False)
    print(f"\nSaved: {output_file}")
    print(f"  - Rows: {len(df_wide)}")
    print(f"  - Columns: {len(df_wide.columns)}")

    print("\n" + "=" * 60)
    print("Step 00 COMPLETE: Random effects loaded and pivoted successfully")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
