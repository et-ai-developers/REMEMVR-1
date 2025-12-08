# Visual Inspection Checklist - RQ 5.1.1 Plots

**Date:** 2025-12-08
**Files:** functional_form_theta.png, functional_form_probability.png

---

## Theta-Scale Plot (functional_form_theta.png)

### Data Representation
- [ ] **400 observed data points visible** as scatter plot (individual observations)
  - Points should show variation (not perfectly on line)
  - Color: Blue (#3498DB)
  - Alpha: 0.3 (semi-transparent)
  - Size: Small dots (30pt)

- [ ] **Model-averaged prediction line visible** (100 time points)
  - Color: Red (#E74C3C)
  - Linewidth: Thick (2.5pt)
  - Smooth curve (not jagged)

- [ ] **95% CI bands visible** around prediction line
  - Color: Light red (same as line, alpha=0.2)
  - Bands should be wider at extremes (less data)
  - Bands should NOT cross observed data envelope

### Curve Shape (Power-Law)
- [ ] **Rapid initial decline** (0-1 days)
  - Steep negative slope near t=0
  - More rapid than logarithmic would be

- [ ] **Gradual asymptotic approach** (3-6 days)
  - Curve flattens but does NOT become horizontal
  - Continuous decline (no plateau)
  - Characteristic of power-law (proportional decay)

- [ ] **NOT logarithmic shape**
  - Logarithmic would show sharper bend at Day 1
  - Power-law is smoother, more gradual

### Axes and Labels
- [ ] **X-axis:** "Days Since VR Encoding"
  - Range: 0 to ~10 days
  - Tick marks visible and readable
  - Font: Bold, size 12

- [ ] **Y-axis:** "Memory Ability (Theta)"
  - Range: Should span observed data (approximately -2 to +3)
  - Tick marks visible and readable
  - Font: Bold, size 12

- [ ] **Title:** "RQ 5.1.1: Functional Form of Forgetting - Theta Scale"
  - Subtitle: "Power-Law Trajectory from Multi-Model Inference"
  - Font: Bold, size 13
  - Centered above plot

### Legend
- [ ] **Three entries:**
  1. "Observed data (N=400)" - Blue scatter
  2. "Model-averaged prediction (α_eff=0.410, 16 models)" - Red line
  3. "95% CI (between-model variance)" - Red shaded band

- [ ] **Positioned:** Best location (not obscuring data)
- [ ] **Frame:** Visible with white background
- [ ] **Font:** Readable (size 10)

### Annotation Box
- [ ] **Content:**
  ```
  Multi-model inference:
    • 16 competitive models (ΔAIC<2)
    • Effective α = 0.410
    • Power-law form (Wixted & Ebbesen, 1991)
  ```

- [ ] **Position:** Bottom right (0.98, 0.02 in axes coordinates)
- [ ] **Background:** Wheat color, semi-transparent (alpha=0.5)
- [ ] **Frame:** Rounded box
- [ ] **Font:** Readable (size 9)

### Overall Quality
- [ ] **Resolution:** 300 DPI (publication quality)
- [ ] **File size:** ~471 KB (check with `ls -lh`)
- [ ] **Grid:** Light gray dashed lines (alpha=0.3)
- [ ] **Spines:** Top and right spines removed (clean look)

---

## Probability-Scale Plot (functional_form_probability.png)

### Data Representation
- [ ] **400 observed data points visible** as scatter plot
  - Same structure as theta-scale plot
  - Color: Blue (#3498DB)
  - Range: Should span 0.0 to 1.0 (some extreme values near boundaries)

- [ ] **Model-averaged prediction line visible**
  - Color: Red (#E74C3C)
  - Shape: Should match theta-scale curve (monotonic transformation)

- [ ] **95% CI bands visible**
  - Color: Light red
  - Width: Should reflect transformation (non-uniform)

### Probability Transformation
- [ ] **Y-axis values in [0, 1] range**
  - Formatted as percentages (0% to 100%)
  - No values outside this range (transformation correct)

- [ ] **Curve shape preserved**
  - Same general shape as theta-scale
  - Rapid decline then gradual asymptote
  - S-curve appearance (logistic transformation)

- [ ] **Prediction range reasonable**
  - Should span approximately 25% to 75%
  - Matches observed data envelope

### Axes and Labels
- [ ] **X-axis:** "Days Since VR Encoding" (same as theta-scale)

- [ ] **Y-axis:** "Probability Correct"
  - Range: -5% to 105% (slight padding)
  - Formatted as percentages (e.g., "50.0%")
  - Font: Bold, size 12

- [ ] **Title:** "RQ 5.1.1: Functional Form of Forgetting - Probability Scale"
  - Subtitle: "Power-Law Trajectory from Multi-Model Inference"

### Legend
- [ ] **Same three entries as theta-scale**
- [ ] **Positioned and readable**

### Annotation Box
- [ ] **Content:**
  ```
  Multi-model inference:
    • 16 competitive models (ΔAIC<2)
    • Effective α = 0.410
    • Decision D069: Dual-scale reporting
  ```

- [ ] **Position:** Bottom right
- [ ] **Readable and not obscuring data**

### Decision D069 Compliance
- [ ] **Dual-scale reporting:** BOTH theta and probability scales generated
- [ ] **Transformation documented:** IRT 2PL formula (p = 1/(1 + exp(-1.7θ)))
- [ ] **Consistency:** Probability plot conveys same scientific message as theta plot

### Overall Quality
- [ ] **Resolution:** 300 DPI
- [ ] **File size:** ~555 KB
- [ ] **Grid, spines, formatting:** Same clean style as theta-scale

---

## Cross-Plot Validation

### Consistency
- [ ] **Same data points:** Both plots show same 400 observations (just transformed scale)
- [ ] **Same prediction grid:** 100 time points in both
- [ ] **Same curve shape:** Power-law form visible in both scales
- [ ] **Same message:** α_eff=0.410, 16 models, multi-model inference

### Publication Readiness
- [ ] **High resolution:** Both files 300 DPI
- [ ] **Readable fonts:** All text legible at publication size
- [ ] **Color contrast:** Red/blue easily distinguishable
- [ ] **Professional appearance:** Clean, uncluttered, journal-quality

### Scientific Accuracy
- [ ] **Power-law functional form:** Curve shape matches θ(t) = β₀ + β₁(t+1)^(-0.410)
- [ ] **Model-averaged:** Not single best model prediction
- [ ] **Uncertainty quantified:** 95% CI bands visible
- [ ] **References cited:** Wixted & Ebbesen (1991) in annotation

---

## Common Issues to Check For

### Data Issues
- [ ] **No missing data points:** All 400 observations plotted
- [ ] **No outliers beyond CI bands:** Most points within 95% CI
- [ ] **No data artifacts:** No discontinuities or jumps in observed data

### Plotting Issues
- [ ] **No overlapping labels:** X/Y labels, title, legend all readable
- [ ] **No cut-off content:** All plot elements within figure bounds
- [ ] **No pixelation:** Smooth curves at 300 DPI
- [ ] **No color mismatch:** Legend colors match plot elements

### Scientific Issues
- [ ] **Correct functional form:** Power-law, NOT logarithmic
- [ ] **Correct model count:** 16 models (not 5 original models)
- [ ] **Correct α_eff:** 0.410 (not 0.5 or other value)
- [ ] **Correct reference:** Wixted & Ebbesen (1991), not Ebbinghaus

---

## Sign-Off

**Inspector:** _______________________  
**Date:** _______________________  
**Status:** [ ] APPROVED  [ ] REVISIONS NEEDED  

**Notes:**
___________________________________________________________________________
___________________________________________________________________________
___________________________________________________________________________

---

**If ALL checkboxes are checked, plots are publication-ready and scientifically accurate.**

**If ANY checkbox is unchecked, regenerate plots or revise plotting script accordingly.**
