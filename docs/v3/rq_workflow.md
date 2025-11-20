# RQ Specification Workflow

**Last Updated:** 2025-01-11
**Purpose:** Documents the flat agent architecture for RQ specification and validation
**Audience:** Main claude when creating/executing RQs
**Status:** Current

---

## RQ SPECIFICATION WORKFLOW (FLAT ARCHITECTURE)

**Architecture:** Flat - all agents report to master agent, no nesting

**Why Flat:** Claude Code sub-agents cannot invoke other sub-agents. All agents must report directly to the master agent.

**Communication Method:** File-based - agents write instruction files and reports, pass file paths instead of full content

### Workflow Sequence for Single RQ Specification:

**Step 1: User Initiates**
```
User tells master agent: "Specify RQ ch5/rq10"
```

**Step 2: Master Invokes RQ-Specification Agent (Draft Phase)**
```
Master invokes: Task(subagent_type="rq_specification", ...)
RQ-Spec agent:
  - Creates info.md draft (11 sections)
  - Creates config.yaml draft (complete YAML)
  - Writes instruction file for Scholar: results/chX/rqY/validation/scholar_instructions.md
  - Writes instruction file for Statistics: results/chX/rqY/validation/statistics_instructions.md
  - Reports back to master with instruction file paths
```

**Step 3: Master Invokes Scholar Agent**
```
Master invokes: Task(subagent_type="scholar", prompt="Read instructions from: results/chX/rqY/validation/scholar_instructions.md")
Scholar agent:
  - Reads instruction file
  - Loads info.md
  - Validates theoretical grounding
  - Uses WebSearch for recent literature
  - Writes validation report: results/chX/rqY/validation/scholar_report.json
  - Reports back to master with report file path
```

**Step 4: Master Invokes Statistics Expert Agent**
```
Master invokes: Task(subagent_type="statistics_expert", prompt="Read instructions from: results/chX/rqY/validation/statistics_instructions.md")
Statistics agent:
  - Reads instruction file
  - Loads info.md + config.yaml + tools_inventory.yaml
  - Validates statistical methodology
  - Assesses tool requirements
  - Uses Context7 MCP for package docs if needed
  - Writes validation report: results/chX/rqY/validation/statistics_report.json
  - Updates tool inventory
  - Reports back to master with report file path
```

**Step 5: Master Invokes RQ-Specification Agent (Finalization Phase)**
```
Master invokes: Task(subagent_type="rq_specification", prompt="Finalize RQ chX/rqY. Scholar report: <path>. Statistics report: <path>")
RQ-Spec agent:
  - Reads both validation reports
  - Reviews validation scores and issues
  - Updates Status section in info.md with scores
  - Saves final rq_specification_report.json
  - Updates status.json to "specified"
  - Reports back to master with summary (what's good/bad/critical)
```

**Step 6: Master Reports to User**
```
Master presents summary table with:
  - RQ ID
  - Scholar score
  - Statistics score
  - Tool assessment
  - Issues found
  - Overall status
```

### Iteration Handling:

If validation scores < 9.0 or issues flagged:
- Master invokes RQ-Spec agent again with instructions to address issues
- RQ-Spec agent revises drafts
- Loop back to Step 3 (re-validate with Scholar + Statistics)
- Maximum 2 iterations before flagging for user review

### File Structure for Communication:

```
results/chX/rqY/
├── info.md (draft created by RQ-Spec)
├── config.yaml (draft created by RQ-Spec)
├── status.json (tracking)
├── rq_specification_report.json (final report from RQ-Spec)
└── validation/
    ├── scholar_instructions.md (written by RQ-Spec, read by Scholar)
    ├── scholar_report.json (written by Scholar, read by RQ-Spec)
    ├── statistics_instructions.md (written by RQ-Spec, read by Statistics)
    └── statistics_report.json (written by Statistics, read by RQ-Spec)
```

### Benefits of Flat Architecture:

1. **Context Efficiency:** Master doesn't load full validation reports into context - only file paths
2. **No Nesting Issues:** Agents never need to invoke other agents
3. **Clear Audit Trail:** All communication via files, easy to trace
4. **Parallel Execution:** Master can invoke Scholar + Statistics in parallel (Step 3 + 4 together)
5. **Stateless Agents:** Each agent invocation is independent
