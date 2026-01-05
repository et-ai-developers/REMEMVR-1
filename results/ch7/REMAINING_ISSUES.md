# Chapter 7 - Remaining Data Integrity Issues
**Date:** 2026-01-05 18:40
**Status:** 3 of 5 critical issues FIXED, 2 systematic issues remain

---

## ✅ FIXED Issues (3/5)

1. **7.1.4**: Re-run with REAL data ✅
   - Replaced ALL fake DASS/VR/Sleep data
   - Now uses correct column names from DATA_DICTIONARY.md

2. **7.2.1**: Removed fake diagnostic plots ✅
   - Eliminated synthetic residuals and Cook's D
   - Created honest note about diagnostic limitations

3. **7.2.2**: Fixed missing domain data ✅
   - Found and used real Where/When domains from Ch5 5.2.1
   - All 100 participants have all 3 domains

---

## 🔴 REMAINING Issues

### 1. Column Name Mismatches in Multiple RQs

**Affected RQs:** 7.1.1, 7.1.2, 7.2.1 (and possibly others)

**Wrong column names being used:**
```python
# WRONG (old names):
'RAVLT trial {i} score'  # Should be: 'ravlt-trial-{i}-score'
'RPM Score'              # Should be: 'rpm-score'  
'BVMT total recall'      # Should be: 'bvmt-total-recall'
'Age in years'           # Should be: 'age'
'NART Score'             # Should be: 'nart-score'
```

**Impact:** 
- If re-running these RQs from scratch, they will FAIL
- Current results may be based on old data file versions
- Cannot reproduce results with current dfnonvr.csv

**Evidence:**
- 7.1.1/code/step01_extract_cognitive_tests.py line 72
- 7.1.2/code/step01_extract_cognitive_tests.py line 72
- 7.2.1/code/step01_extract_merge_data.py lines 200-226

---

### 2. Missing Data Handling Issues

**Problem:** 3% of participants (n=3) excluded for missing NART scores without proper analysis

**Affected RQs:** 7.1.1, 7.1.4, others

**Issues:**
- No systematic missing data analysis (e.g., Little's MCAR test)
- Complete case analysis without justification
- Potential selection bias not addressed
- No sensitivity analysis with imputation

**Recommendation:**
1. Document missingness pattern
2. Test if missing completely at random (MCAR)
3. Consider multiple imputation if not MCAR
4. At minimum, report demographics of excluded participants

---

## 📋 Summary of What Needs Fixing

### Priority 1 - Column Names (Breaking Issue)
Need to update data extraction in:
- [ ] 7.1.1 step01
- [ ] 7.1.2 step01  
- [ ] 7.2.1 step01
- [ ] 7.2.3 (check)
- [ ] 7.2.4 (check)

### Priority 2 - Missing Data
Need to add proper handling:
- [ ] Document missingness patterns
- [ ] Add MCAR test
- [ ] Consider imputation strategy
- [ ] Report excluded participant characteristics

### Priority 3 - Validation System
Need to improve:
- [ ] Add data integrity checks (no fake data)
- [ ] Verify column names match DATA_DICTIONARY.md
- [ ] Check for unexpected missing data
- [ ] Validate value ranges against known limits

---

## 🎯 Next Steps

1. **Most Critical:** Fix column names in 7.1.1, 7.1.2, 7.2.1
   - These will break if re-run with current data
   - Update to use correct names from DATA_DICTIONARY.md

2. **Important:** Document missing data handling
   - Add proper missing data analysis to affected RQs
   - Justify complete case analysis or implement imputation

3. **Systematic:** Improve validation
   - Add checks to prevent future fake data generation
   - Ensure column name verification in all scripts

---

## Notes

- The fake data issues (7.1.4, 7.2.1, 7.2.2) are NOW FIXED
- Column name issues won't break existing results but prevent reproduction
- Missing data handling is a scientific rigor issue, not a breaking bug
- All "green" RQs (7.1.1, 7.1.2, 7.1.3, 7.2.3, 7.2.4) may have column issues