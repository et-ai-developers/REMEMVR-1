# Tools Catalog (v4.X)

**Version:** 4.0
**Last Updated:** 2025-11-22
**Purpose:** Lightweight tool discovery for rq_planner (ORANGE/GREEN tools only)

**Format:** One-line descriptions for quick scanning

**Status:** ORANGE/GREEN tools only (validated and ready for use)

---

## Quick Reference

**Total ORANGE/GREEN Tools:** 0

*No tools have been validated yet. This catalog will be populated as tools progress through TDD validation.*

---

## Workflow

**rq_planner usage:**
1. Read this catalog to discover available tools
2. Reference tool names in 2_plan.md
3. rq_tools will look up full signatures in tools_inventory.md

**Maintenance:**
- Tools added here when status changes RED → ORANGE
- Updated when status changes ORANGE → GREEN
- Never contains RED status tools

---

## IRT Analysis Tools

*No ORANGE/GREEN tools yet.*

---

## LMM Analysis Tools

*No ORANGE/GREEN tools yet.*

---

## Plotting Tools

*No ORANGE/GREEN tools yet.*

---

## Validation Tools

*No ORANGE/GREEN tools yet.*

---

## Configuration Tools

*No ORANGE/GREEN tools yet.*

---

## Standard Library Functions (Always Available)

**Note:** The following standard library functions are used directly in analysis scripts and do NOT require tools_inventory.md documentation:

### pandas Operations
```
pd.read_csv, pd.DataFrame.melt, pd.DataFrame.merge, pd.DataFrame.pivot, pd.DataFrame.groupby, pd.DataFrame.to_csv
```

### numpy Operations
```
np.linspace, np.log, np.array, np.mean, np.std, np.median
```

### pathlib Operations
```
Path.mkdir, Path.exists, Path.read_text, Path.write_text
```

**Why stdlib exempt?** These are well-documented in official Python/pandas/numpy docs. rq_tools agent has explicit exemption rule for stdlib functions.

---

## Decision Implementations

*Functions implementing project decisions will be listed here once validated:*

- **D039 (2-pass purification):** TBD
- **D068 (dual p-values):** TBD
- **D069 (dual-scale plots):** TBD
- **D070 (TSVR time variable):** TBD

---

## Notes

**Why Empty?**
All 51 functions in the codebase are currently RED status (untested salvaged legacy code). Tools will be added here as they are validated during RQ 5.1 execution.

**See Also:**
- `tools_status.tsv` - Complete list of all 51 functions (including RED)
- `tools_inventory.md` - Detailed API reference for ORANGE/GREEN tools

---

**End of Tools Catalog v4.0**

*This file will grow organically as tools are validated through TDD.*
