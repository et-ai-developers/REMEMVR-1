# Status.yaml Structure Specification

**Last Updated:** 2025-11-16
**Version:** 4.0
**Purpose:** Defines the mandatory status.yaml structure for v4.X research questions
**Audience:** rq_builder agent when creating status.yaml file

---

## How to Use This Template

This template specifies the **exact YAML structure** that rq_builder agent must create for the `status.yaml` file. The status.yaml file tracks agent execution statuses and maintains context dumps for pseudo-stateful operation across all RQ-specific agents.

**Agent Implementation (rq_builder agent):**
- Reads this template in Step 3
- Creates `status.yaml` in Step 6 according to these specifications
- Reports success after status.yaml created

**Pseudo-Statefulness:**
- Each RQ-specific agent reads `status.yaml` in Step 2 of its workflow
- Agents check prior agents' statuses and read their context_dumps
- Agents update their own status + write context_dump in final step
- This enables continuity without persistent agent state

---

## File Location

**Path:** `results/chX/rqY/status.yaml` (root level of RQ directory)

**Created By:** rq_builder agent (workflow step 3, agent step 6)

**Updated By:** All 10 RQ-specific agents (each updates their section after execution)

**Read By:** All 10 RQ-specific agents (each reads prior context in Step 2)

---

## YAML Structure Overview

**Top-level sections:**
1. **Agent Statuses** - 10 RQ-specific agents (each with status + context_dump)
2. **analysis_steps** - Per-step execution tracking (added by rq_analysis agent, NOT by rq_builder)

**Status Values:** `pending` or `success` (only two valid values)

**Context Dump Format:** Multiline string (max 5 lines per universal.md)

---

## Agent Names (10 RQ-Specific Agents - In Order)

The following 10 agents MUST have sections in status.yaml:

1. `rq_builder`
2. `rq_concept`
3. `rq_scholar`
4. `rq_stats`
5. `rq_planner`
6. `rq_tools`
7. `rq_analysis`
8. `rq_inspect`
9. `rq_plots`
10. `rq_results`

**EXCLUDED:** Do NOT create sections for `g_code`, `g_conflict`, or `g_debug` (general-purpose agents).

---

## Initial Values (Created by rq_builder)

**When rq_builder creates status.yaml:**

**All agent statuses:** `pending` (no agents have run yet)

**All context_dumps:** Empty multiline strings (no context yet)

**analysis_steps section:** NOT created by rq_builder (rq_analysis creates this later)

**Example initial state:**
```yaml
rq_builder:
  status: pending
  context_dump: |

rq_concept:
  status: pending
  context_dump: |

# ... all 10 agents start pending with empty context_dumps
```

**After rq_builder runs:** rq_builder updates its own section to `status: success` and writes its context_dump (5 lines max).

**NOTE:** Do NOT create the `analysis_steps` section initially. The rq_analysis agent creates this later.

---

## Initial YAML Template (For rq_builder)

**Create this exact structure:**

```yaml
rq_builder:
  status: pending
  context_dump: |

rq_concept:
  status: pending
  context_dump: |

rq_scholar:
  status: pending
  context_dump: |

rq_stats:
  status: pending
  context_dump: |

rq_planner:
  status: pending
  context_dump: |

rq_tools:
  status: pending
  context_dump: |

rq_analysis:
  status: pending
  context_dump: |

rq_inspect:
  status: pending
  context_dump: |

rq_plots:
  status: pending
  context_dump: |

rq_results:
  status: pending
  context_dump: |
```

**After creating this template, rq_builder updates its own section to `status: success` with a 5-line context_dump.**

---

**End of Template Specification**
