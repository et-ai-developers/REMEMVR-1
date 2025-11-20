"""
REMEMVR Data Extraction Examples

This file contains runnable examples demonstrating common data extraction workflows.
Each example is self-contained and can be run independently.

Usage:
    python data/examples.py

Author: REMEMVR Project
Created: 2025-01-05
"""

import pandas as pd
import sys
import os

# Add parent directory to path to import data module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data import (
    load_master,
    extract_tag,
    extract_tags,
    validate_extraction,
    extract_vr_tags,
    extract_cognitive_scores,
    load_rq_output,
    combine_data_sources,
    ValidationError
)


def example_1_single_tag():
    """
    Example 1: Extract a single tag (RPM scores)

    This is the simplest use case - extracting one variable for all participants.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Extract Single Tag (RPM Scores)")
    print("="*70)

    # Extract RPM scores
    rpm_scores = extract_tag(
        tag_pattern="{UID}-COG-X-RPM-Scor",
        expected_count=100
    )

    print(f"\nExtracted {len(rpm_scores)} RPM scores")
    print(f"Columns: {list(rpm_scores.columns)}")
    print(f"\nFirst 5 participants:")
    print(rpm_scores.head())
    print(f"\nBasic statistics:")
    print(rpm_scores['value'].describe())


def example_2_multiple_tags():
    """
    Example 2: Extract multiple demographic variables

    Shows how to extract several variables at once with custom column names.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Extract Multiple Tags (Demographics)")
    print("="*70)

    # Extract age, sex, education
    demographics = extract_tags(
        tag_patterns={
            'Age': '{UID}-DEM-X-Age',
            'Sex': '{UID}-DEM-X-Sex',
            'Education': '{UID}-DEM-X-Education',
            'VR_Experience': '{UID}-DEM-X-VR_Exp'
        },
        expected_rows=100,
        expected_cols=5  # UID + 4 variables
    )

    print(f"\nExtracted {len(demographics)} participants")
    print(f"Columns: {list(demographics.columns)}")
    print(f"\nFirst 5 participants:")
    print(demographics.head())

    # Show age distribution
    print(f"\nAge distribution:")
    print(f"  Mean: {demographics['Age'].mean():.1f} years")
    print(f"  Range: {demographics['Age'].min():.0f}-{demographics['Age'].max():.0f} years")


def example_3_computed_scores():
    """
    Example 3: Compute RAVLT total score from individual trials

    Demonstrates computing derived scores from multiple components.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Compute RAVLT Total Score")
    print("="*70)

    # Compute RAVLT total (sum of Trials 1-5)
    ravlt_totals = extract_cognitive_scores(
        test_name='RAVLT',
        scores_to_compute={
            'RAVLT_Total': ['T1Sc', 'T2Sc', 'T3Sc', 'T4Sc', 'T5Sc']
        },
        expected_count=100
    )

    print(f"\nComputed RAVLT_Total for {len(ravlt_totals)} participants")
    print(f"Columns: {list(ravlt_totals.columns)}")
    print(f"\nFirst 5 participants:")
    print(ravlt_totals.head())

    # Show distribution
    print(f"\nRAVLT_Total distribution:")
    print(f"  Mean: {ravlt_totals['RAVLT_Total'].mean():.1f}")
    print(f"  SD: {ravlt_totals['RAVLT_Total'].std():.1f}")
    print(f"  Range: {ravlt_totals['RAVLT_Total'].min():.0f}-{ravlt_totals['RAVLT_Total'].max():.0f}")


def example_4_vr_data():
    """
    Example 4: Extract VR item accuracy across all 4 tests

    Shows how to extract VR data with wildcards (automatically handles item details).
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Extract VR Item Accuracy Across Tests")
    print("="*70)

    # Extract Item 1 (common) accuracy across all tests
    item1_accuracy = extract_vr_tags(
        paradigm='IFR',      # Items Free Recall
        domain='N',          # What domain
        item='i1CM',         # Item 1, Common
        measure='ANS',       # Accuracy
        expected_rows=400    # 100 participants × 4 tests
    )

    print(f"\nExtracted {len(item1_accuracy)} data points")
    print(f"  {item1_accuracy['UID'].nunique()} participants × {item1_accuracy['test'].nunique()} tests")
    print(f"Columns: {list(item1_accuracy.columns)}")
    print(f"\nFirst 8 rows (first 2 participants, all tests):")
    print(item1_accuracy.head(8))

    # Calculate mean accuracy by test
    print(f"\nMean accuracy by test:")
    for test_num in [1, 2, 3, 4]:
        test_data = item1_accuracy[item1_accuracy['test'] == test_num]
        mean_acc = test_data['value'].mean()
        print(f"  Test {test_num}: {mean_acc:.3f}")


def example_5_pivot_vr_data():
    """
    Example 5: Pivot VR data from long to wide format

    Shows how to reshape VR data for analysis (one row per participant).
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Pivot VR Data to Wide Format")
    print("="*70)

    # Extract Item 1 accuracy (long format)
    item1_long = extract_vr_tags(
        paradigm='IFR',
        domain='N',
        item='i1CM',
        measure='ANS',
        expected_rows=400
    )

    print("Long format (first 8 rows):")
    print(item1_long.head(8))

    # Pivot to wide format
    item1_wide = item1_long.pivot(
        index='UID',
        columns='test',
        values='value'
    ).reset_index()

    # Rename columns for clarity
    item1_wide.columns = ['UID', 'Item1_T1', 'Item1_T2', 'Item1_T3', 'Item1_T4']

    print(f"\nWide format (first 5 participants):")
    print(item1_wide.head())

    print(f"\nShape change: {item1_long.shape} → {item1_wide.shape}")


def example_6_validation():
    """
    Example 6: Validate extracted data

    Demonstrates validation with expected dimensions and missing data rules.
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Validate Extracted Data")
    print("="*70)

    # Extract data
    data = extract_tags(
        tag_patterns={
            'Age': '{UID}-DEM-X-Age',
            'RPM_Score': '{UID}-COG-X-RPM-Scor'
        }
    )

    print("Data extracted (first 5 rows):")
    print(data.head())

    # Validate
    validation = validate_extraction(
        data,
        expected_rows=100,
        expected_cols=3,  # UID + Age + RPM
        required_cols=['UID', 'Age', 'RPM_Score'],
        missing_rules={'Age': 0, 'RPM_Score': 0}  # No missing allowed
    )

    print(f"\nValidation Results:")
    print(f"  Valid: {validation['valid']}")
    print(f"  Errors: {validation['errors']}")
    print(f"  Warnings: {validation['warnings']}")
    print(f"  Stats: {validation['stats']}")


def example_7_combine_sources():
    """
    Example 7: Combine multiple data sources

    Shows how to merge demographics, cognitive scores, and VR data.
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Combine Multiple Data Sources")
    print("="*70)

    # Step 1: Extract demographics
    print("Step 1: Extract demographics...")
    demographics = extract_tags(
        tag_patterns={
            'Age': '{UID}-DEM-X-Age',
            'Education': '{UID}-DEM-X-Education'
        }
    )

    # Step 2: Compute RAVLT total
    print("Step 2: Compute RAVLT total...")
    ravlt = extract_cognitive_scores(
        test_name='RAVLT',
        scores_to_compute={'RAVLT_Total': ['T1Sc', 'T2Sc', 'T3Sc', 'T4Sc', 'T5Sc']}
    )

    # Step 3: Extract VR data and pivot
    print("Step 3: Extract VR data and pivot...")
    vr_data = extract_vr_tags(
        paradigm='IFR', domain='N', item='i1CM', measure='ANS'
    )
    vr_wide = vr_data.pivot(index='UID', columns='test', values='value').reset_index()
    vr_wide.columns = ['UID', 'Item1_T1', 'Item1_T2', 'Item1_T3', 'Item1_T4']

    # Step 4: Merge all data sources
    print("Step 4: Merge all sources...")
    full_data = demographics.merge(ravlt, on='UID').merge(vr_wide, on='UID')

    print(f"\nFinal dataset shape: {full_data.shape}")
    print(f"Columns: {list(full_data.columns)}")
    print(f"\nFirst 5 participants:")
    print(full_data.head())


def example_8_error_handling():
    """
    Example 8: Error handling and debugging

    Demonstrates how errors are raised and how to handle them.
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: Error Handling")
    print("="*70)

    print("\nAttempt 1: Incorrect tag spelling")
    print("  Trying: {UID}-COG-X-RPM-Score (incorrect - should be 'Scor')")
    try:
        wrong_data = extract_tag("{UID}-COG-X-RPM-Score", expected_count=100)
    except ValidationError as e:
        print(f"  ❌ ValidationError caught: {str(e)[:80]}...")

    print("\nAttempt 2: Correct tag spelling")
    print("  Trying: {UID}-COG-X-RPM-Scor (correct)")
    try:
        correct_data = extract_tag("{UID}-COG-X-RPM-Scor", expected_count=100)
        print(f"  ✅ Success! Extracted {len(correct_data)} values")
    except ValidationError as e:
        print(f"  ❌ Unexpected error: {e}")

    print("\nAttempt 3: Wrong expected count")
    print("  Trying: expected_count=50 (incorrect - should be 100)")
    try:
        wrong_count = extract_tag("{UID}-COG-X-RPM-Scor", expected_count=50)
    except ValidationError as e:
        print(f"  ❌ ValidationError caught: {str(e)[:80]}...")

    print("\nAttempt 4: Missing data without permission")
    print("  Trying: NART scores with allow_missing=False")
    try:
        no_missing = extract_tag("{UID}-COG-X-NART-Scor", allow_missing=False)
    except ValidationError as e:
        print(f"  ❌ ValidationError caught: {str(e)[:80]}...")

    print("\nAttempt 5: Missing data with permission")
    print("  Trying: NART scores with allow_missing=True")
    try:
        with_missing = extract_tag("{UID}-COG-X-NART-Scor", allow_missing=True)
        missing_count = with_missing['value'].isna().sum()
        print(f"  ✅ Success! Extracted {len(with_missing)} values ({missing_count} missing)")
    except ValidationError as e:
        print(f"  ❌ Unexpected error: {e}")


def example_9_workflow_rq_prep():
    """
    Example 9: Full RQ data preparation workflow

    Demonstrates a complete workflow for preparing RQ input data.
    """
    print("\n" + "="*70)
    print("EXAMPLE 9: Full RQ Data Preparation Workflow")
    print("="*70)

    print("\n📋 Simulating RQ 7.1: Age and cognitive predictors of episodic memory")
    print("\nRequired data:")
    print("  - Age (from demographics)")
    print("  - Education (from demographics)")
    print("  - RPM_Score (from cognitive tests)")
    print("  - RAVLT_Total (computed from T1-T5)")
    print("  - VR Item 1 accuracy (all 4 tests)")

    # Use combine_data_sources for clean workflow
    print("\nPreparing data using combine_data_sources()...")

    # First, prepare VR data separately (needs pivoting)
    vr_data = extract_vr_tags(
        paradigm='IFR', domain='N', item='i1CM', measure='ANS'
    )
    vr_wide = vr_data.pivot(index='UID', columns='test', values='value').reset_index()
    vr_wide.columns = ['UID', 'Item1_T1', 'Item1_T2', 'Item1_T3', 'Item1_T4']

    # Extract demographics and cognitive scores
    data = extract_tags(
        tag_patterns={
            'Age': '{UID}-DEM-X-Age',
            'Education': '{UID}-DEM-X-Education',
            'RPM_Score': '{UID}-COG-X-RPM-Scor'
        }
    )

    ravlt = extract_cognitive_scores(
        test_name='RAVLT',
        scores_to_compute={'RAVLT_Total': ['T1Sc', 'T2Sc', 'T3Sc', 'T4Sc', 'T5Sc']}
    )

    # Merge all
    full_data = data.merge(ravlt, on='UID').merge(vr_wide, on='UID')

    # Validate
    validation = validate_extraction(
        full_data,
        expected_rows=100,
        expected_cols=9,  # UID + Age + Edu + RPM + RAVLT + 4 VR tests
        required_cols=['UID', 'Age', 'RPM_Score', 'Item1_T1']
    )

    if validation['valid']:
        print("\n✅ Data preparation complete!")
        print(f"   Shape: {full_data.shape}")
        print(f"   Columns: {list(full_data.columns)}")
        print(f"\n   Preview:")
        print(full_data.head(3))
        print("\n   Ready to save to: results/ch7/rq1/data/input.csv")
    else:
        print("\n❌ Validation failed!")
        print(f"   Errors: {validation['errors']}")


def run_all_examples():
    """Run all examples in sequence"""
    print("\n" + "="*70)
    print("REMEMVR DATA EXTRACTION API - EXAMPLES")
    print("="*70)
    print("\nRunning all examples...")

    examples = [
        example_1_single_tag,
        example_2_multiple_tags,
        example_3_computed_scores,
        example_4_vr_data,
        example_5_pivot_vr_data,
        example_6_validation,
        example_7_combine_sources,
        example_8_error_handling,
        example_9_workflow_rq_prep
    ]

    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"\n❌ Example {i} failed with error: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETE")
    print("="*70)


if __name__ == "__main__":
    # Run all examples when script is executed
    run_all_examples()
