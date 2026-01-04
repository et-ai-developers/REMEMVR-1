#!/usr/bin/env python3
"""
Recreate dfnonvr.csv from cache/dfData.csv with ALL needed columns including NART
This extracts participant-level data (TEST=1 only, non-VR data)
"""

import pandas as pd
import numpy as np

def create_dfnonvr_from_cache():
    """
    Create dfnonvr.csv from cache/dfData.csv
    Extracts TEST=1 data (participant-level, non-VR measures)
    """
    
    # Load the original cached data
    df_orig = pd.read_csv('cache/dfData.csv')
    print(f"Original data shape: {df_orig.shape}")
    
    # Filter to TEST=1 only (participant-level data, measured once)
    df_nonvr = df_orig[df_orig['TEST'] == 1].copy()
    print(f"TEST=1 data shape: {df_nonvr.shape}")
    
    # Columns to keep from the original (non-VR, participant-level measures)
    keep_columns = [
        'UID',
        
        # Cognitive tests - these are measured once, not per test
        'NART Score',  # THIS WAS MISSING BEFORE!
        'RPM Score',
        'RPM Tr01 answer', 'RPM Tr02 answer', 'RPM Tr03 answer', 'RPM Tr04 answer',
        'RPM Tr05 answer', 'RPM Tr06 answer', 'RPM Tr07 answer', 'RPM Tr08 answer',
        'RPM Tr09 answer', 'RPM Tr10 answer', 'RPM Tr11 answer', 'RPM Tr12 answer',
        
        # BVMT columns
        'BVMT Form Number',
        'BVMT trial 1 score', 'BVMT trial 2 score', 'BVMT trial 3 score',
        'BVMT delayed recall delay period', 'BVMT delayed recall score',
        'BVMT total recall', 'BVMT learning', 'BVMT percent retained',
        'BVMT recognition hits', 'BVMT recognition falsealarms',
        'BVMT recognition discrimination index', 'BVMT recognition response bias',
        
        # RAVLT columns  
        'RAVLT trial 1 score', 'RAVLT trial 2 score', 'RAVLT trial 3 score',
        'RAVLT trial 4 score', 'RAVLT trial 5 score',
        'RAVLT distraction trial score', 'RAVLT free recall score',
        'RAVLT delayed recall delay period', 'RAVLT delayed recall score',
        'RAVLT recognition hits ', 'RAVLT recognition semantic misses',
        'RAVLT recognition phonetic misses', 'RAVLT recognition semantic phonetic misses',
        'RAVLT recognition distraction misses', 'RAVLT recognition distract phonetic misses',
        'RAVLT recognition distract semantic misses', 'RAVLT recognition distract smenaitc and pohonetic misses',
        
        # REMEMVR task durations (these might be VR-specific but let's check)
        'REMEMVR bathroom task 01 duration', 'REMEMVR bathroom task 02 duration',
        'REMEMVR bathroom task 03 duration', 'REMEMVR bathroom task 04 duration',
        'REMEMVR bathroom task 05 duration', 'REMEMVR bathroom task 06 duration',
        'REMEMVR bathroom task 07 duration', 'REMEMVR bathroom task 08 duration',
        'REMEMVR bathroom task 09 duration', 'REMEMVR bathroom task 10 duration',
        'REMEMVR bathroom task 11 duration', 'REMEMVR bathroom task 12 duration',
        
        'REMEMVR bedroom task 01 duration', 'REMEMVR bedroom task 02 duration',
        'REMEMVR bedroom task 03 duration', 'REMEMVR bedroom task 04 duration',
        'REMEMVR bedroom task 05 duration', 'REMEMVR bedroom task 06 duration',
        'REMEMVR bedroom task 07 duration', 'REMEMVR bedroom task 08 duration',
        'REMEMVR bedroom task 09 duration', 'REMEMVR bedroom task 10 duration',
        'REMEMVR bedroom task 11 duration', 'REMEMVR bedroom task 12 duration',
        
        'REMEMVR kitchen task 01 duration', 'REMEMVR kitchen task 02 duration',
        'REMEMVR kitchen task 03 duration', 'REMEMVR kitchen task 04 duration',
        'REMEMVR kitchen task 05 duration', 'REMEMVR kitchen task 06 duration',
        'REMEMVR kitchen task 07 duration', 'REMEMVR kitchen task 08 duration',
        'REMEMVR kitchen task 09 duration', 'REMEMVR kitchen task 10 duration',
        'REMEMVR kitchen task 11 duration', 'REMEMVR kitchen task 12 duration',
        
        'REMEMVR livingroom task 01 duration', 'REMEMVR livingroom task 02 duration',
        'REMEMVR livingroom task 03 duration', 'REMEMVR livingroom task 04 duration',
        'REMEMVR livingroom task 05 duration', 'REMEMVR livingroom task 06 duration',
        'REMEMVR livingroom task 07 duration', 'REMEMVR livingroom task 08 duration',
        'REMEMVR livingroom task 09 duration', 'REMEMVR livingroom task 10 duration',
        'REMEMVR livingroom task 11 duration', 'REMEMVR livingroom task 12 duration',
        
        # Demographics
        'Age in years', 'Sex 0=female 1=male',
        'Education level ( High school (Year 9 or lower)\n High school (Year 10)\n High school (Year 12)\n Certificate 1 & 2\n Certificate 3 & 4\n Diploma / Advanced Diploma\n Bachelors Degree\n Graduate Certificate / Diploma\n Masters Degree\n Doctoral Degree)',
        'VR Usage (Never\n Less than 1 hour\n 1 - 10 hours\n 10 - 50 hours\n More than 50 hours)',
        'Typical sleep hours',
        
        # DASS
        'Total DASS Anxiety Items',
        'Total DASS Stress Items',
        
        # Strategy questionnaire
        'Describe your technique here'
    ]
    
    # Filter to columns that exist
    existing_columns = [col for col in keep_columns if col in df_nonvr.columns]
    missing_columns = [col for col in keep_columns if col not in df_nonvr.columns]
    
    if missing_columns:
        print(f"\nWarning: Missing columns in source data:")
        for col in missing_columns:
            print(f"  - {col}")
    
    # Create the final dataframe
    df_final = df_nonvr[existing_columns].copy()
    
    # Reset index since we filtered to TEST=1
    df_final = df_final.reset_index(drop=True)
    
    print(f"\nFinal shape: {df_final.shape}")
    print(f"Columns included: {len(df_final.columns)}")
    
    # Verify NART is included
    if 'NART Score' in df_final.columns:
        print(f"✅ NART Score successfully included")
        print(f"   NART range: {df_final['NART Score'].min():.0f} - {df_final['NART Score'].max():.0f}")
        print(f"   NART mean: {df_final['NART Score'].mean():.1f}")
    else:
        print("❌ NART Score NOT included!")
    
    # Check for DASS Depression
    dass_cols = [col for col in df_orig.columns if 'DASS' in col and 'Depres' in col]
    if dass_cols:
        print(f"\nFound DASS Depression columns: {dass_cols}")
    else:
        print("\n⚠️ DASS Depression not found in source data")
    
    return df_final

if __name__ == "__main__":
    print("=" * 80)
    print("RECREATING dfnonvr.csv WITH COMPLETE DATA")
    print("=" * 80)
    
    # Create the new dataframe
    df_nonvr = create_dfnonvr_from_cache()
    
    # Save it
    output_path = 'dfnonvr.csv'
    df_nonvr.to_csv(output_path, index=False)
    
    print(f"\n✅ Saved to {output_path}")
    print(f"Shape: {df_nonvr.shape}")
    print(f"\nFirst 5 column names:")
    for i, col in enumerate(df_nonvr.columns[:5]):
        print(f"  {i+1}. {col}")
    print(f"\nLast 5 column names:")
    for i, col in enumerate(df_nonvr.columns[-5:]):
        print(f"  {i+len(df_nonvr.columns)-4}. {col}")
    
    # Quick validation
    print(f"\n📊 Quick stats:")
    print(f"  Participants: {len(df_nonvr)}")
    print(f"  Has NART: {'NART Score' in df_nonvr.columns}")
    print(f"  Has RPM: {'RPM Score' in df_nonvr.columns}")
    print(f"  Has RAVLT: {'RAVLT trial 1 score' in df_nonvr.columns}")
    print(f"  Has BVMT: {'BVMT trial 1 score' in df_nonvr.columns}")
    print(f"  Has DASS Anxiety: {'Total DASS Anxiety Items' in df_nonvr.columns}")
    print(f"  Has STR: {'Describe your technique here' in df_nonvr.columns}")