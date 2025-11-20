# V4.X Orchestrator - Phase 2 Automation Concept

**File:** orchestrator.md
**Location:** docs/v4/
**Last Updated:** 2025-11-16
**Purpose:** Conceptual design for Phase 2 automated orchestration
**Audience:** Future developer building orchestrator script
**Status:** Phase 2 (conceptual reference only, not implemented yet)
**Version:** 4.X (atomic agent architecture)

---

## Overview

This document describes the **concept** for automating the v4.X 17-step RQ pipeline workflow. This is a **design document**, not implementation code. The actual orchestrator script will be built **after** Phase 12 testing (RQ 5.1) proves the workflow stable.

**What This Document Provides:**
- Automation concept and requirements
- Blueprint for future implementation
- Agent invocation mechanism design
- Error recovery integration strategy
- Status tracking automation approach

**What This Document Does NOT Provide:**
- Actual Python/bash implementation code
- Specific library/framework choices
- Command-line interface design
- Configuration file formats

**When to Build Actual Orchestrator:**
- **After Phase 12:** RQ 5.1 tested successfully end-to-end
- **After workflow stabilizes:** All agents proven reliable
- **After iterations complete:** Lessons learned applied to agent prompts
- **Phase 2 development:** When ready to scale to 49 remaining RQs

---

## Phase 1 vs Phase 2 Orchestration

### Phase 1: Manual Orchestration (Current)

**Who:** Master (main claude)

**Process:**
1. User runs /refresh
2. User requests: "Begin chX/rqY"
3. Master reads automation.md (step 2)
4. Master manually invokes each agent (steps 3-17)
5. Master handles agent responses individually
6. Master manages CODE EXECUTION LOOP manually
7. Master responds to errors immediately

**Benefits:**
- **Debugging flexibility:** Step-by-step execution control
- **Immediate error response:** Master identifies and fixes issues
- **Agent testing:** Validate each agent works correctly
- **Workflow refinement:** Discover and fix workflow issues
- **Understanding:** User and master learn system deeply

**Use Cases:**
- v4.X development (Phases 5-10: building agents)
- Testing new agents
- RQ 5.1 first run (Phase 12)
- Debugging workflow issues
- Understanding system behavior

---

### Phase 2: Automated Orchestration (Future)

**Who:** Orchestrator script

**Process:**
1. User runs orchestrator script: `poetry run python orchestrator.py ch5 rq1`
2. Script reads automation.md (workflow blueprint)
3. Script invokes agents sequentially per workflow
4. Script handles CODE EXECUTION LOOP automatically
5. Script integrates g_debug for error recovery
6. Script tracks status via status.yaml
7. Script reports completion or errors to user

**Benefits:**
- **Efficiency:** Run RQ without manual intervention
- **Consistency:** Identical execution across all 50 RQs
- **Scalability:** Process remaining 49 RQs after RQ 5.1
- **Reduced human error:** Automation prevents forgotten steps
- **User freedom:** User focuses on analysis, not orchestration

**Use Cases:**
- Production runs for remaining 49 RQs (after RQ 5.1 proven)
- Batch processing multiple RQs
- Consistent workflow execution
- Minimizing manual overhead

---

### Both Modes Available

**Important Design Principle:**
- Manual mode remains available even after Phase 2
- Some scenarios require manual control (debugging, testing new agents)
- Orchestrator is optional efficiency tool, not replacement
- User chooses mode based on needs

---

## Automation Concept

### High-Level Architecture

**Orchestrator Script Responsibilities:**

1. **Read Workflow Specification:**
   - Parse automation.md for 17-step workflow
   - Understand agent invocation order
   - Know user approval gate location (step 7)
   - Understand CODE EXECUTION LOOP complexity (step 14)

2. **Sequential Agent Invocation:**
   - Invoke agents in order (steps 3-6, 9, 11-12, 14, 15, 17)
   - Pass appropriate parameters (chX/rqY, descriptive strings)
   - Wait for agent completion reports
   - Parse agent responses (success vs circuit breaker errors)

3. **User Interaction:**
   - Prompt user at step 7 (approval gate)
   - Wait for user response ("Looks good. Continue" or changes requested)
   - If changes requested: Loop back to step 4 (rq_concept)

4. **CODE EXECUTION LOOP Automation:**
   - Read status.yaml to determine next analysis step
   - Invoke g_code for step N
   - Run generated script via bash
   - If traceback: Invoke g_debug → Apply fix → Re-run
   - Invoke rq_inspect after successful execution
   - Update status.yaml
   - Repeat until all analysis steps complete

5. **Error Recovery:**
   - Detect circuit breaker errors (agent quits)
   - Detect execution errors (tracebacks)
   - Invoke g_debug for execution errors
   - Apply fixes to code/templates/agents
   - Re-run failed step
   - Track fix history (prevent infinite loops)

6. **Status Tracking:**
   - Read status.yaml before each agent invocation
   - Verify previous steps marked success
   - Update status.yaml after user approval (step 7)
   - Track analysis_steps progress (step 14 loop)
   - Report overall RQ progress to user

7. **Logging & Reporting:**
   - Log all agent invocations
   - Capture agent responses
   - Log errors and fixes applied
   - Report final status (success/failure with details)

---

### Workflow Automation Mapping

**From automation.md 17-Step Workflow:**

| Step | Type | Automation Challenge |
|------|------|---------------------|
| 1 | User Input | Accept chX/rqY from command line |
| 2 | Read File | Parse automation.md |
| 3-6 | Agent Invocations | Invoke rq_builder, rq_concept, rq_scholar, rq_stats |
| 7 | User Approval Gate | Prompt user, wait for response, handle changes |
| 8 | User Response | Parse user input ("continue" vs "change") |
| 9-13 | Agent Invocations | Invoke rq_planner, g_conflict, rq_tools, rq_analysis, g_conflict |
| 14 | **CODE EXECUTION LOOP** | **Most complex - see detailed section below** |
| 15-17 | Agent Invocations + Bash | Invoke rq_plots, run plots.py, invoke rq_results |

**Complexity Levels:**
- **Simple:** Steps 3-6, 9, 11-12, 15, 17 (agent invocations)
- **Medium:** Steps 10, 13 (g_conflict with conditional re-runs)
- **Complex:** Step 7 (user approval gate with loop-back)
- **Very Complex:** Step 14 (CODE EXECUTION LOOP with g_debug integration)

---

## Agent Invocation Mechanism

### Invocation Pattern

**From Manual Phase 1:**
- Master uses Task tool to invoke agents
- Passes descriptive string prompts: "Build ch5/rq1", "Create 1_concept.md"
- Agents report informal text confirmations

**For Automated Phase 2:**
- Orchestrator uses same Task tool mechanism
- Invocation format: `Task(subagent_type="agent_name", prompt="descriptive_string")`
- Parse agent responses for success vs errors

### Agent Response Parsing

**Success Response:**
- Agent reports: "Successfully created X"
- Orchestrator: Continue to next step

**Circuit Breaker Error:**
- Agent reports: "EXPECTATIONS circuit breaker - rq_builder not success, quitting"
- Orchestrator: Identify root cause, fix, re-invoke agent

**Example Code (Conceptual):**

```python
def invoke_agent(agent_name, prompt):
    """Invoke agent and parse response"""
    result = task_tool.invoke(
        subagent_type=agent_name,
        prompt=prompt
    )

    if "circuit breaker" in result.lower():
        # Handle circuit breaker error
        return {"status": "error", "type": "circuit_breaker", "message": result}
    elif "successfully" in result.lower():
        # Success
        return {"status": "success", "message": result}
    else:
        # Unknown response
        return {"status": "unknown", "message": result}
```

**Note:** Actual implementation details (libraries, error parsing regex, etc.) determined during Phase 2 development.

---

## CODE EXECUTION LOOP Automation

### Challenge

**Step 14 is the most complex automation challenge:**
- Iterative loop (not fixed number of steps)
- Bash execution with error detection
- g_debug integration (sandbox debugging)
- Fix application (to code OR templates)
- Re-run verification
- Multiple iterations possible (5-10 for first RQ)

### Automation Strategy

**Loop Structure (9 Sub-Steps):**

1. **Check status.yaml:** Which analysis step is next (pending)?
2. **Invoke g_code:** Generate code for step N
3. **Run script:** `poetry run python results/chX/rqY/code/stepN_name.py`
4. **Detect errors:** Parse output for tracebacks
5. **If error:** Invoke g_debug with code/log paths
6. **Apply fix:** g_debug reports solution → orchestrator applies to code/templates
7. **Re-run:** Verify fix works (traceback gone?)
8. **If still fails:** Repeat steps 5-7 (iterative debugging)
9. **After success:** Invoke rq_inspect → Update status.yaml → Next step

### Traceback Detection

**Example Code (Conceptual):**

```python
def run_analysis_step(step_num):
    """Run analysis step with error detection"""
    script_path = f"results/{chapter}/rq{num}/code/step{step_num:02d}_name.py"

    # Run script
    result = bash(f"poetry run python {script_path}")

    # Check for traceback
    if "Traceback" in result.output:
        # Error detected - invoke g_debug
        return debug_and_fix(script_path, result.output)
    else:
        # Success - validate outputs
        return validate_step(step_num)
```

### g_debug Integration

**Debugging Workflow:**

1. **Orchestrator detects error:** Traceback in script output
2. **Orchestrator invokes g_debug:**
   - Passes: code path, log path with traceback
   - g_debug creates sandbox, tests fix, reports solution
3. **Orchestrator applies fix:**
   - Parse g_debug solution
   - Determine fix location (code vs templates vs agent prompts)
   - Apply fix using Edit tool
4. **Orchestrator re-runs script:**
   - Verify traceback gone
   - If still fails: Re-invoke g_debug (iteration)
5. **After success:**
   - Invoke rq_inspect for output validation
   - Update status.yaml (step N success)
   - Continue to next step

### Loop Termination

**Exit Conditions:**

- **Success:** All analysis steps in status.yaml marked success
- **Max Iterations:** Prevent infinite loops (e.g., 20 iterations per step limit)
- **Critical Error:** g_debug can't fix (user intervention required)

---

## Error Recovery Integration

### Error Types & Responses

**1. Circuit Breaker Errors (Agent Quits)**

**Detection:**
- Agent reports circuit breaker type (EXPECTATIONS, STEP, TOOL, CLARITY, SCOPE)
- Agent quits without producing output

**Response:**
1. Orchestrator identifies circuit breaker type from agent report
2. Determines root cause (e.g., EXPECTATIONS = prior step not success)
3. Fixes root cause (e.g., re-run prior step, fix specification)
4. Re-invokes agent after fix
5. If repeated circuit breaker: Escalate to user intervention

---

**2. Execution Errors (Tracebacks)**

**Detection:**
- Script execution produces traceback in output
- Python error messages present

**Response:**
1. Invoke g_debug with code/log paths
2. g_debug reports: Root cause + solution + improvement suggestions
3. Apply fix to code/templates/agents
4. Re-run script to verify fix
5. If still fails: Re-invoke g_debug (iterative)
6. After success: Continue workflow

---

**3. Validation Failures (rq_inspect Reports Error)**

**Detection:**
- rq_inspect reports outputs don't match plan.md expectations
- Status.yaml not updated (step still pending)

**Response:**
1. Review rq_inspect report (what failed validation?)
2. Determine if code error (wrong calculation) or plan error (wrong expectation)
3. Fix code OR fix plan.md
4. Re-run analysis step
5. Re-invoke rq_inspect
6. If validation passes: Continue

---

**4. g_conflict Detections (Contradictions)**

**Detection:**
- g_conflict reports conflicts (count > 0, line numbers provided)

**Response:**
1. Review conflicts reported
2. Determine which document to fix
3. Re-invoke relevant agent to fix (e.g., rq_planner if plan.md contradicts concept.md)
4. Re-invoke g_conflict to verify conflicts resolved
5. Continue only after 0 conflicts

---

### Infinite Loop Prevention

**Safeguards:**

1. **Iteration Limits:**
   - Max iterations per analysis step (e.g., 20)
   - Max total iterations per RQ (e.g., 100)
   - After limit: Pause, report to user, request intervention

2. **Fix History Tracking:**
   - Record all fixes applied
   - Detect repeated fixes (same error → same fix → same error)
   - After 3 identical cycles: Pause, escalate to user

3. **Progress Verification:**
   - Track which steps completed successfully
   - Verify forward progress (not stuck in early steps)
   - Report stuck status after 10 failures on same step

---

## Status Tracking Automation

### status.yaml Structure

**Agent Steps Section:**
- 10 RQ-specific agents
- Each: status (pending/success), context_dump (multiline string)
- General-purpose agents (g_code, g_conflict, g_debug) NOT tracked

**Analysis Steps Section:**
- Created by rq_analysis (step 12)
- Contains: step01, step02, ..., stepN
- Each: status (pending/success)
- Updated by rq_inspect after each step validation

### Orchestrator Reads status.yaml

**When:**
- Before each agent invocation (verify prior steps success)
- Before CODE EXECUTION LOOP (load analysis steps list)
- During CODE EXECUTION LOOP (which step next?)
- After rq_inspect (verify step marked success)

**What to Check:**
- Agent steps: Which agents completed (success), which pending
- Analysis steps: Which analysis steps completed, which next
- Continuity: Previous step success before starting next

### Orchestrator Updates status.yaml

**When:**
- After step 7 user approval (update rq_concept status based on user feedback)
- Indirectly via agents (agents update their own status after completion)

**Note:** Orchestrator primarily READS status.yaml. Agents UPDATE status.yaml. This maintains separation of concerns.

---

## Benefits Analysis

### Why Automate? (Phase 2 Motivation)

**Efficiency:**
- 50 RQs total (1 tested in Phase 1, 49 remaining)
- Manual: ~2-3 hours per RQ × 49 = 98-147 hours
- Automated: ~30 minutes per RQ × 49 = 24.5 hours
- **Time Savings:** ~73-122 hours (3-5 days)

**Consistency:**
- Identical workflow execution across all RQs
- No forgotten steps
- No workflow drift
- Prevents human error

**Scalability:**
- Can run multiple RQs in batch
- Overnight processing possible
- User reviews results, doesn't manage workflow

**User Freedom:**
- User focuses on analysis interpretation
- User focuses on higher-level decisions
- Orchestrator handles mechanical execution

---

### Why Manual? (Phase 1 & Ongoing)

**Debugging:**
- Step-by-step control
- Immediate error inspection
- Workflow refinement

**Testing:**
- Validate new agents
- Test workflow changes
- Understand system behavior

**Learning:**
- User understands every step
- Master learns agent behavior
- Builds mental model of workflow

**Flexibility:**
- Adapt to unexpected situations
- Make judgment calls
- Handle edge cases

---

### Both Modes Valuable

**Use Manual When:**
- Testing v4.X for first time (RQ 5.1)
- Debugging workflow issues
- Testing new agents after improvements
- Handling unusual RQs (cross-RQ dependencies)
- Learning system deeply

**Use Automated When:**
- Workflow proven stable (after RQ 5.1)
- Processing remaining 49 RQs
- Consistent, well-understood RQs
- Maximizing efficiency
- Batch processing

---

## Implementation Roadmap

### When to Build Orchestrator

**Prerequisites (All Must Be Complete):**

1. ✅ **Phase 1-4 Complete:** Foundation, templates, thesis files, validation tools
2. ✅ **Phase 5-10 Complete:** All 13 v4.X agents built and tested individually
3. ✅ **Phase 12 TEST1-TEST4 Complete:** RQ 5.1 tested successfully end-to-end
4. ✅ **Phase 12 TEST5 Complete:** All discovered issues fixed, workflow stable
5. ✅ **Workflow Proven:** RQ 5.1 completes in single run without g_debug iterations

**Only build orchestrator AFTER all prerequisites met.**

---

### Implementation Steps (Future Phase 2 Development)

**Step 1: Design Implementation Details**
- Choose language (Python recommended - already using poetry)
- Choose CLI framework (argparse, click, etc.)
- Design configuration file format (YAML, TOML, etc.)
- Design logging strategy (file-based, structured logging)

**Step 2: Implement Core Loop**
- Parse automation.md for workflow
- Implement agent invocation mechanism (Task tool wrapper)
- Implement sequential execution (steps 3-17)

**Step 3: Implement User Approval Gate**
- Prompt user at step 7
- Parse user response ("continue" vs changes)
- Loop back to step 4 if changes requested

**Step 4: Implement CODE EXECUTION LOOP**
- status.yaml parsing (which step next?)
- g_code invocation
- Bash execution with traceback detection
- g_debug integration
- Fix application mechanism
- Re-run verification
- rq_inspect invocation
- status.yaml update

**Step 5: Implement Error Recovery**
- Circuit breaker detection and handling
- g_conflict handling (re-run agents if conflicts)
- Validation failure handling (rq_inspect)
- Infinite loop prevention (iteration limits, fix history)

**Step 6: Implement Logging & Reporting**
- Comprehensive logging (all agent invocations, responses, errors)
- Progress reporting (which step executing, % complete)
- Error reporting (what failed, what fix applied)
- Final status report (success with summary, or failure with details)

**Step 7: Testing**
- Test on RQ 5.1 (already completed manually in Phase 1)
- Compare automated results to manual results (should be identical)
- Test error recovery (deliberately introduce errors, verify g_debug integration)
- Test on RQ 5.2, 5.3 (additional validation)

**Step 8: Documentation**
- User guide (how to run orchestrator)
- Developer guide (code architecture, how to modify)
- Troubleshooting guide (common issues, solutions)

**Step 9: Refinement**
- Optimize performance (parallel agent invocations if safe?)
- Enhance error messages (more helpful to user)
- Add resume capability (pick up from failure point)

**Step 10: Production Use**
- Run on remaining 47 RQs (5.4-7.20)
- Monitor for issues
- Iterate based on real-world usage

---

## Reference to automation.md

### Relationship

**automation.md:**
- **What to execute:** 17-step workflow specification
- **Manual orchestration:** Master reads this and executes manually
- **Audience:** Master (main claude) during Phase 1

**orchestrator.md (this document):**
- **How to automate:** Design for automating the 17-step workflow
- **Automated orchestration:** Script reads automation.md and executes programmatically
- **Audience:** Future developer during Phase 2

---

### Orchestrator Reads automation.md

**Why:**
- automation.md is single source of truth for workflow
- If workflow changes (add step, remove step), automation.md updated
- Orchestrator re-reads automation.md and adapts automatically
- No hardcoding of workflow in orchestrator script

**How (Conceptual):**

```python
def load_workflow():
    """Load workflow from automation.md"""
    # Read automation.md
    workflow_doc = read_file("docs/v4/automation.md")

    # Parse for steps
    steps = extract_steps(workflow_doc)  # Find "#### Step N:" headers

    # Build workflow data structure
    workflow = []
    for step in steps:
        workflow.append({
            "number": step.number,
            "description": step.description,
            "agent": step.agent if applicable,
            "type": step.type  # "agent_invocation", "user_approval", "code_loop", "bash"
        })

    return workflow
```

---

## Design Philosophy

### Prevent v3.0 Mistakes

**v3.0 Failures:**
- Monolithic agents → context bloat → hallucinations
- API guessing → mismatches → cascading errors
- Attempted automation too early → automated broken workflow

**v4.X Preventions:**
- Atomic agents (lean context <5k) → no hallucinations
- Pre-validation (g_code 4-layer validation) → no API guessing
- **Manual Phase 1 FIRST** → validate workflow BEFORE automating

**Critical Lesson:**
> "Don't automate a broken workflow. Manual Phase 1 validates, Automated Phase 2 scales."

---

### Automation After Validation

**Phase 1: Prove It Works**
- Build all 13 agents
- Test on RQ 5.1 end-to-end
- Discover and fix all workflow issues
- Iterate until stable (single run, no g_debug iterations)

**Phase 2: Scale It**
- Build orchestrator based on proven workflow
- Automate 17-step process
- Process remaining 49 RQs efficiently
- Maintain manual mode for edge cases

**This Approach:**
- Minimizes risk (validate before scale)
- Maximizes learning (understand before automate)
- Enables iteration (fix agents, not orchestrator + agents simultaneously)

---

## Conclusion

**orchestrator.md Purpose:**
- Design document for Phase 2 automation
- Blueprint for future implementation
- Conceptual reference (not code)

**When to Build:**
- After Phase 12 (RQ 5.1 tested successfully)
- After workflow stabilizes (proven reliable)
- During Phase 2 development

**Benefits:**
- Efficiency (50 RQs in ~25 hours vs ~150 hours)
- Consistency (identical execution across RQs)
- Scalability (batch processing, overnight runs)
- User freedom (focus on analysis, not orchestration)

**Philosophy:**
- Manual Phase 1 validates workflow
- Automated Phase 2 scales workflow
- Both modes available (choose based on needs)

**Reference:**
- automation.md: WHAT to execute (17-step workflow)
- orchestrator.md (this doc): HOW to automate (script concept)

---

**End of Orchestrator Concept Document**

**Version:** V4.X (atomic agent architecture)
**Specification Reference:** docs/user/analysis_pipeline_solution.md section 3.2 (orchestration modes), section 4.5.2 (orchestrator.md spec)
**Related:** docs/v4/automation.md (17-step workflow to automate)
**Last Updated:** 2025-11-16
