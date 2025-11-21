# Tools Inventory (v4.X)

**Version:** 4.0
**Last Updated:** 2025-11-22
**Purpose:** Authoritative API reference for VALIDATED analysis tools (ORANGE/GREEN only)

**Status Legend:**
- 🔴 **RED:** Function exists but untested (NOT DOCUMENTED HERE)
- 🟠 **ORANGE:** Inspected, refactored, documented - READY FOR USE
- 🟢 **GREEN:** Successfully used in live RQ with perfect results

**Source of Truth:** `/home/etai/projects/REMEMVR/docs/tools_status.tsv`

---

## Quick Reference

**Total Functions in Codebase:** 51
**Documented Here (ORANGE/GREEN only):** 0

**Status Breakdown:**
- 🔴 RED: 51 (100%) - See tools_status.tsv, NOT documented here
- 🟠 ORANGE: 0 (0%)
- 🟢 GREEN: 0 (0%)

---

## ORANGE/GREEN Functions

*No functions have been validated yet. Functions will be added here as they progress through TDD:*

**Testing Workflow:**
1. **RED → ORANGE:** Inspect code, write tests, refactor, document signature → ADD TO THIS FILE
2. **ORANGE → GREEN:** Use in live RQ successfully → Update status in this file

---

## Module: tools.analysis_irt

*No ORANGE/GREEN functions yet.*

---

## Module: tools.analysis_lmm

*No ORANGE/GREEN functions yet.*

---

## Module: tools.config

*No ORANGE/GREEN functions yet.*

---

## Module: tools.plotting

*No ORANGE/GREEN functions yet.*

---

## Module: tools.validation

*No ORANGE/GREEN functions yet.*

---

## Migration Notes

**Current Status (2025-11-22):**
- All 51 functions salvaged from legacy code
- ALL functions are RED status (untested in v4.X)
- None ready for agent use
- Functions will be promoted to ORANGE during RQ 5.1 testing as needed

**Next Steps:**
- Begin RQ 5.1 execution
- When rq_tools requests a function, promote it RED → ORANGE
- Document ORANGE functions here
- After successful RQ use, promote ORANGE → GREEN

---

**End of Tools Inventory v4.0**

*This file will grow as functions are validated. Check tools_status.tsv for complete list of RED functions.*
