#!/usr/bin/env python3
"""
Step 02: Compute Attenuation Ratios for RQ 7.2.2
=================================================
Purpose: Calculate attenuation ratios as percentage reduction in age coefficients 
when controlling for cognitive tests

Scientific Context:
Attenuation ratio = (beta_bivariate - beta_controlled) / beta_bivariate
- >70%: Substantial attenuation (supports VR scaffolding hypothesis)  
- 30-70%: Partial attenuation
- <30%: Minimal attenuation

The VR scaffolding hypothesis predicts substantial attenuation because cognitive 
tests should capture most age-related variance if VR provides environmental support.
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
LOG_FILE = RQ_DIR / "logs" / "step02_compute_attenuation.log"

# Ensure directories exist
(RQ_DIR / "logs").mkdir(exist_ok=True)
(RQ_DIR / "data").mkdir(exist_ok=True)

def log(msg):
    """Log message to both file and console"""
    with open(LOG_FILE, 'a') as f:
        f.write(f"{msg}\n")
        f.flush()
    print(msg, flush=True)

def compute_attenuation(beta_bivariate, beta_controlled):
    """
    Compute attenuation ratio and percentage
    
    Note: Can exceed 100% in suppression effects (sign reversal)
    """
    if abs(beta_bivariate) < 1e-10:  # Essentially zero
        return np.nan, np.nan
    
    # Calculate attenuation
    attenuation_ratio = (beta_bivariate - beta_controlled) / beta_bivariate
    attenuation_percent = attenuation_ratio * 100
    
    return attenuation_ratio, attenuation_percent

def classify_attenuation(percent):
    """Classify attenuation magnitude"""
    if pd.isna(percent):
        return "undefined"
    elif percent < 0:
        return "negative_attenuation"  # Unexpected - coefficient increased
    elif percent < 30:
        return "minimal"
    elif percent < 70:
        return "partial"
    elif percent <= 100:
        return "substantial"
    else:
        return "suppression"  # >100% indicates sign reversal

def main():
    """Main attenuation computation function"""
    log("="*70)
    log("STEP 02: COMPUTE ATTENUATION RATIOS")
    log("="*70)
    
    # 1. Load merged coefficients
    log("\n1. Loading merged coefficients from Step 01...")
    
    input_file = RQ_DIR / "data" / "step01_merged_coefficients.csv"
    merged_df = pd.read_csv(input_file)
    
    log(f"Loaded {len(merged_df)} participants")
    log(f"Columns: {list(merged_df.columns)}")
    
    # 2. Compute attenuation for overall REMEMVR
    log("\n2. Computing attenuation for overall REMEMVR...")
    
    # Get unique coefficients (same for all participants in current data)
    beta_biv_all = merged_df['beta_age_bivariate_all'].iloc[0]
    beta_ctrl_all = merged_df['beta_age_controlled_all'].iloc[0]
    
    ratio_all, percent_all = compute_attenuation(beta_biv_all, beta_ctrl_all)
    class_all = classify_attenuation(percent_all)
    
    log(f"Overall REMEMVR:")
    log(f"  Bivariate beta: {beta_biv_all:.4f}")
    log(f"  Controlled beta: {beta_ctrl_all:.4f}")
    log(f"  Attenuation: {percent_all:.1f}%")
    log(f"  Classification: {class_all}")
    
    # Check for suppression effect
    if percent_all > 100:
        log("  *** SUPPRESSION EFFECT DETECTED ***")
        log("  Age coefficient reversed sign after controlling for cognitive tests")
        log("  This suggests older adults benefit MORE from VR scaffolding")
    
    # 3. Compute attenuation for What domain
    log("\n3. Computing attenuation for What domain...")
    
    beta_biv_what = merged_df['beta_age_bivariate_what'].iloc[0]
    beta_ctrl_what = merged_df['beta_age_controlled_what'].iloc[0]
    
    ratio_what, percent_what = compute_attenuation(beta_biv_what, beta_ctrl_what)
    class_what = classify_attenuation(percent_what)
    
    log(f"What domain:")
    log(f"  Bivariate beta: {beta_biv_what:.4f}")
    log(f"  Controlled beta: {beta_ctrl_what:.4f}")
    log(f"  Attenuation: {percent_what:.1f}%")
    log(f"  Classification: {class_what}")
    
    # 4. Create attenuation results dataframe
    log("\n4. Creating attenuation results...")
    
    attenuation_results = pd.DataFrame([
        {
            'domain': 'overall',
            'beta_bivariate': beta_biv_all,
            'beta_controlled': beta_ctrl_all,
            'attenuation_ratio': ratio_all,
            'attenuation_percent': percent_all,
            'classification': class_all
        },
        {
            'domain': 'what',
            'beta_bivariate': beta_biv_what,
            'beta_controlled': beta_ctrl_what,
            'attenuation_ratio': ratio_what,
            'attenuation_percent': percent_what,
            'classification': class_what
        }
    ])
    
    # Note: Currently using same coefficients for What as overall
    # This is a limitation that should be addressed with domain-specific models
    
    # 5. Save outputs
    log("\n5. Saving outputs...")
    
    # Save attenuation ratios
    output_file = RQ_DIR / "data" / "step02_attenuation_ratios.csv"
    attenuation_results.to_csv(output_file, index=False)
    log(f"Saved attenuation ratios to: {output_file}")
    
    # Save effect classification
    classification_file = RQ_DIR / "data" / "step02_effect_classification.txt"
    with open(classification_file, 'w') as f:
        f.write("ATTENUATION EFFECT CLASSIFICATION\n")
        f.write("="*60 + "\n\n")
        
        f.write("Classification Thresholds:\n")
        f.write("  <0%: Negative attenuation (unexpected)\n")
        f.write("  0-30%: Minimal attenuation\n")
        f.write("  30-70%: Partial attenuation\n")
        f.write("  70-100%: Substantial attenuation\n")
        f.write("  >100%: Suppression effect (sign reversal)\n\n")
        
        f.write("Results:\n")
        for _, row in attenuation_results.iterrows():
            f.write(f"\n{row['domain'].upper()} DOMAIN:\n")
            f.write(f"  Attenuation: {row['attenuation_percent']:.1f}%\n")
            f.write(f"  Classification: {row['classification']}\n")
            
            if row['attenuation_percent'] > 100:
                f.write("  *** SUPPRESSION EFFECT ***\n")
                f.write("  Age effect reversed from negative to positive\n")
                f.write("  Indicates older adults benefit more from VR scaffolding\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("INTERPRETATION:\n")
        
        if percent_all > 100:
            f.write("The suppression effect (>100% attenuation) strongly supports\n")
            f.write("the VR scaffolding hypothesis. After accounting for cognitive\n")
            f.write("abilities, age becomes a POSITIVE predictor, suggesting older\n")
            f.write("adults leverage VR environmental support more effectively.\n")
        elif percent_all > 70:
            f.write("The substantial attenuation (>70%) supports the VR scaffolding\n")
            f.write("hypothesis. Cognitive tests capture most age-related variance,\n")
            f.write("confirming that VR provides environmental support.\n")
        elif percent_all > 30:
            f.write("The partial attenuation (30-70%) provides moderate support for\n")
            f.write("the VR scaffolding hypothesis. Some age effects persist beyond\n")
            f.write("what cognitive tests explain.\n")
        else:
            f.write("The minimal attenuation (<30%) does not support the VR scaffolding\n")
            f.write("hypothesis. Age effects remain largely independent of cognitive abilities.\n")
    
    log(f"Saved effect classification to: {classification_file}")
    
    log("\n" + "="*70)
    log("KEY FINDING:")
    log(f"Attenuation = {percent_all:.1f}% ({class_all})")
    
    if percent_all > 100:
        log("SUPPRESSION EFFECT: Age coefficient reversed sign")
        log("This strongly supports the VR scaffolding hypothesis")
    elif percent_all > 70:
        log("Substantial attenuation supports VR scaffolding hypothesis")
    else:
        log("Further analysis needed to understand age-VR relationship")
    
    log("="*70)
    log("\nStep 02 complete: Attenuation ratios computed")
    
    return attenuation_results

if __name__ == "__main__":
    main()