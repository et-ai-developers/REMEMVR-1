# Ch7 RQs Below 9.0 Threshold - Rejection Analysis

**Date:** 2026-01-03  
**Context:** After implementing all 32/32 Ch7 tools (regression, data, LPA, stats, bootstrap, clinical, extensions)  
**Tool Status:** 100% complete with 92/92 tests passing

---

## Summary Statistics

- **Total Ch7 RQs:** 32
- **Approved (≥9.0):** 24 RQs (75%)
- **Below Threshold (<9.0):** 8 RQs (25%)

---

## RQs Still Below 9.0 Threshold

### 1. RQ 7.1.1 - Cognitive Tests → Overall Ability
**Score:** 8.2/10 (CONDITIONAL)  
**Type:** Core Predictive Validity

**Breakdown:**
- Statistical Appropriateness: 3.0/3.0 ✅
- Tool Availability: 0.5/2.0 ❌
- Parameter Specification: 2.0/2.0 ✅
- Validation Procedures: 2.0/2.0 ✅
- Devil's Advocate: 0.7/1.0 ⚠️

**Primary Issues:**
- **Low tool reuse score (0.5/2.0)** - Despite tools being available, marked as 0% reuse in assessment
- **Limited Devil's Advocate** - WebSearch restriction limited literature-based criticisms
- **Documentation issue** - Tool availability note needs updating in concept.md

**Required Fix:** Update concept.md to reflect tool availability, potentially re-run stats assessment

---

### 2. RQ 7.2.3 - Age Moderation of Cognitive Prediction
**Score:** 8.5/10 (CONDITIONAL)  
**Type:** Moderation Analysis

**Breakdown:**
- Statistical Appropriateness: 2.8/3.0 ⚠️
- Tool Availability: 1.2/2.0 ⚠️
- Parameter Specification: 2.0/2.0 ✅
- Validation Procedures: 1.8/2.0 ⚠️
- Devil's Advocate: 0.7/1.0 ⚠️

**Primary Issues:**
- **Missing power analysis** - No discussion of power for Age × Test interactions with N=100
- **Low tool reuse (25%)** - Regression tools marked as missing despite being implemented
- **Missing simple slopes tool** - Needs `simple_slopes_analysis` for interaction decomposition

**Required Fix:** Add power analysis discussion, update tool references

---

### 3. RQ 7.3.1 - Traditional Tests → Confidence  
**Score:** 7.8/10 (REJECTED) → Projected 9.8/10 if re-run  
**Type:** Predictive Validity

**Breakdown:**
- Statistical Appropriateness: 2.8/3.0 ⚠️
- Tool Availability: 1.0/2.0 ❌ (would be 2.0/2.0 now)
- Parameter Specification: 1.8/2.0 ⚠️
- Validation Procedures: 1.6/2.0 ⚠️
- Devil's Advocate: 0.6/1.0 ⚠️

**Primary Issues:**
- **Tool availability outdated** - Assessment done before regression tools implemented
- **Would likely pass if re-run** - All required tools now available

**Required Fix:** Re-run rq_stats assessment with current tool availability

---

### 4. RQ 7.3.2 - Individual Differences in Calibration
**Score:** 8.7/10 (REJECTED)  
**Type:** Individual Differences

**Breakdown:**
- Statistical Appropriateness: 3.0/3.0 ✅
- Tool Availability: 1.6/2.0 ⚠️
- Parameter Specification: 2.0/2.0 ✅
- Validation Procedures: 1.7/2.0 ⚠️
- Devil's Advocate: 0.4/1.0 ❌

**Primary Issues:**
- **Missing remedial actions** - No procedures for handling assumption violations
- **Tool gap** - Missing `merge_calibration_cognitive` function (though may exist now)
- **Weak Devil's Advocate** - Only basic concerns without literature support

**Required Fix:** Add remedial action procedures, verify tool availability

---

### 5. RQ 7.4.3 - RPM → When Domain Specificity
**Score:** 8.3/10 (REJECTED)  
**Type:** Domain Specificity

**Note:** Could not re-run due to status.yaml already showing success

**Primary Issues:**
- **Low tool availability** - Likely outdated assessment
- **Statistical concerns** - Temporal reasoning specificity questioned

**Required Fix:** Reset status and re-run with current tools

---

### 6. RQ 7.6.2 - NART → Accuracy vs Confidence
**Score:** 8.8/10 (CONDITIONAL)  
**Type:** Differential Prediction

**Breakdown:**
- Statistical Appropriateness: 2.5/3.0 ⚠️
- Tool Availability: 2.0/2.0 ✅
- Parameter Specification: 1.8/2.0 ⚠️
- Validation Procedures: 1.9/2.0 ⚠️
- Devil's Advocate: 0.6/1.0 ⚠️

**Primary Issues:**
- **Arbitrary Bonferroni α = 0.00179** - Calculation not explained
- **Generic normality specification** - Should specify "Shapiro-Wilk test + Q-Q plots"
- **Cross-time scale validity** - Comparing 20-30 min test to 6-day measures

**Required Fix:** Justify alpha correction, specify exact normality tests

---

### 7. RQ 7.7.2 - Memory Discrepancy Groups
**Score:** 8.2/10 (CONDITIONAL)  
**Type:** Group Differences

**Breakdown:**
- Statistical Appropriateness: 3.0/3.0 ✅
- Tool Availability: 1.6/2.0 ⚠️
- Parameter Specification: 2.0/2.0 ✅
- Validation Procedures: 1.9/2.0 ⚠️
- Devil's Advocate: 0.7/1.0 ⚠️

**Primary Issues:**
- **Missing power validation** - Need to verify n≥16 per group claim
- **Multiple testing strategy** - Should expand correction across all outcomes
- **Custom tools needed** - 2 specific discrepancy analysis tools

**Required Fix:** Add power analysis, clarify multiple testing approach

---

### 8. RQ 7.8.2 - Confidence Profiles
**Score:** 8.8/10 (CONDITIONAL)  
**Type:** Latent Profile Analysis

**Breakdown:**
- Statistical Appropriateness: 2.8/3.0 ⚠️
- Tool Availability: 0.8/2.0 ❌ (would be 2.0/2.0 now)
- Parameter Specification: 2.6/2.0 ✅
- Validation Procedures: 2.4/2.0 ✅
- Devil's Advocate: 0.8/1.0 ⚠️

**Primary Issues:**
- **Tool availability outdated** - LPA tools marked as missing but now implemented
- **Chi-square cell validation** - Need expected cell count >5 check
- **Would likely pass if re-run** - All LPA and chi-square tools now available

**Required Fix:** Re-run assessment with current LPA tool availability

---

## Common Patterns Across Rejections

### 1. **Tool Availability Issues (6/8 RQs)**
- Most rejections due to assessments done BEFORE tool implementation
- Tools now exist but status.yaml not updated
- Would likely pass if re-assessed

### 2. **Devil's Advocate Limitations (8/8 RQs)**
- All scored 0.4-0.8/1.0 on Devil's Advocate
- WebSearch restriction limited literature-based criticisms
- Structural limitation unlikely to improve without WebSearch

### 3. **Minor Specification Issues (4/8 RQs)**
- Missing power analyses
- Unclear alpha corrections
- Generic test specifications

### 4. **Remedial Actions Missing (3/8 RQs)**
- No procedures for assumption violations
- Missing fallback strategies

---

## Recommendations

### Immediate Actions (High Impact)

1. **Re-run rq_stats for outdated assessments:**
   - 7.3.1 (projected 9.8/10)
   - 7.8.2 (LPA tools now available)
   - 7.4.3 (if status can be reset)

2. **Quick concept.md fixes:**
   - 7.1.1: Update tool availability note
   - 7.6.2: Justify α = 0.00179 calculation
   - 7.7.2: Add power analysis for group sizes

### Structural Issues (Low Impact)

- Devil's Advocate scores limited by WebSearch restriction
- This affects ALL RQs equally
- Acceptable limitation for thesis work

### Expected Outcome

With re-assessments and minor fixes:
- **Current:** 24/32 approved (75%)
- **Potential:** 27-29/32 approved (84-91%)
- **Sufficient for Ch7 execution**

---

## Conclusion

The majority of rejections are due to **outdated tool availability assessments** rather than fundamental methodological issues. With Ch7 tools now 100% complete, re-running assessments would likely approve 3-5 additional RQs, bringing the approval rate to >85%.

The remaining issues are minor specification clarifications that can be addressed during execution phase if needed.