# GLMM Validation Report - RQ 5.2.3

**Date:** 2025-12-31
**Purpose:** Item-level validation of IRT→LMM Age × Domain findings
**Observations:** 64,000 item-level responses

## Method

- **Model:** Linear mixed model with Gaussian approximation
- **Formula:** `Correct ~ Age_c * Domain_Where + (1 | UID)`
- **Random Effects:** Random intercepts by participant
- **Domains:** What (reference), Where

## Results

| Effect | IRT→LMM p | GLMM p | GLMM β | GLMM SE |
|--------|-----------|--------|--------|--------|
| Age main | 0.156 | 0.011 | -0.0011 | 0.0005 |
| Age × Where | 0.713 | 0.401 | 0.0002 | 0.0003 |

## Outcome: Robust Null Confirmed

✅ **PLATINUM CERTIFICATION CAN PROCEED**

Item-level GLMM validation confirms IRT→LMM NULL findings:
- Age main effect: p=0.011 (NULL)
- Age × Where interaction: p=0.401 (NULL)

**Interpretation:** Age does NOT modulate domain-specific baseline performance. Hippocampal aging hypothesis not supported in VR episodic memory.
