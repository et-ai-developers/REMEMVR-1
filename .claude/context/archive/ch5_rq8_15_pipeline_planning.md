# Archive: ch5_rq8_15_pipeline_planning

**Topic:** RQ 5.8-5.15 Pipeline Execution Preparation - Planning and TDD Tool Detection
**Created:** 2025-11-26
**Last Updated:** 2025-11-26

---

## RQ 5.8-5.15 Pipeline Planning and TDD Tool Detection (2025-11-26 20:00)

**Task:** RQ 5.8-5.15 Pipeline Execution Preparation - TDD Tool Development Strategy

**Objective:** User accepted 9.1/10 CONDITIONAL scores as publication-quality. Transition from concept validation to pipeline execution phase. Execute rq_planner and rq_tools in parallel for all 8 RQs, identify missing tools via TDD detection, create comprehensive tool development roadmap.

**User Decision:** "9 scores are acceptable. Run rq_planner on ch5/rq8-15 in parallel" then "Yes, run rq_tools in parallel on ch5/rq8-15"

**Archived from:** state.md Session (2025-11-26 20:00)
**Original Date:** 2025-11-26 20:00
**Reason:** Session complete, planning phase finished, execution transitioned to tool development

---

### Key Accomplishments

**1. Parallel Pipeline Planning (8 RQs - ALL COMPLETE)**

Executed rq_planner for all 8 RQs (5.8-5.15) simultaneously. All agents succeeded creating 2_plan.md files:

**RQ 5.8 - Two-Phase Forgetting (7 steps, 30-60min):**
- Pipeline: LMM-only (reuses RQ 5.7 theta/TSVR/model)
- 3 convergent tests: quadratic term, piecewise vs continuous AIC, slope ratio
- Cross-RQ dependency: RQ 5.7 required (theta, TSVR, best model)
- Bonferroni α=0.0033

**RQ 5.9 - Age Effects (6 steps, 10-20min):**
- Pipeline: LMM-only (reuses RQ 5.7 theta/TSVR)
- 3-way interaction: Age × Domain × Time
- D068 dual p-values, D070 TSVR time variable

**RQ 5.10 - Age × Domain × Time (6 steps, 5-15min):**
- Pipeline: LMM-only (reuses RQ 5.1 theta/TSVR)
- Grand-mean centered age, Tukey HSD post-hoc
- Bonferroni α=0.025 (fewer tests)

**RQ 5.11 - IRT vs CTT Convergence (8 steps, 20-40min):**
- Pipeline: Correlation + Parallel LMM (IRT model, CTT model)
- 4 Pearson correlations (Holm-Bonferroni), Cohen's κ agreement
- Cross-RQ dependency: RQ 5.1 required (theta, TSVR, purified items)
- 6-part assumption validation for BOTH models

**RQ 5.12 - Methodological Comparison (9 steps, ~60min):**
- Pipeline: CTT-IRT comparison (Full CTT vs Purified CTT vs IRT)
- Steiger's z-test, Cronbach's α with bootstrap CIs
- Z-score standardization for valid AIC comparison
- Cross-RQ dependency: RQ 5.1 required (IRT params, theta, TSVR)

**RQ 5.13 - Individual Differences (5 steps, 10-15min):**
- Pipeline: Variance decomposition (NO new model fitting)
- Uses RQ 5.7 saved LMM model .pkl
- ICC for intercepts & slopes, intercept-slope correlation
- Outputs random effects for RQ 5.14 clustering

**RQ 5.14 - Clustering (6 steps, 35-50min):**
- Pipeline: K-means with 4-part validation (BIC + silhouette ≥0.5 + gap statistic + bootstrap Jaccard ≥0.75)
- First clustering RQ in thesis (0% method reuse)
- Cross-RQ dependency: RQ 5.13 required (random effects)

**RQ 5.15 - Item Difficulty × Time (6 steps, 30-60min):**
- Pipeline: Cross-classified LMM (UID × Item random effects)
- Requires pymer4 package
- Cross-RQ dependency: RQ 5.1 required (difficulty, TSVR)

**Execution Order Constraints:**
- Tier 1 (already complete): RQ 5.1, 5.7
- Tier 2 (can run in parallel): RQ 5.8, 5.9, 5.10, 5.11, 5.12, 5.15
- Tier 3 (requires RQ 5.7 model): RQ 5.13
- Tier 4 (requires RQ 5.13 random effects): RQ 5.14

**2. TDD Tool Detection (8 RQs - 1 SUCCESS, 7 FAILURES)**

Executed rq_tools for all 8 RQs simultaneously. Expected behavior: agents FAIL when tools missing from tools_inventory.md (TDD detection point).

**Success:** RQ 5.11 (1/8) - All tools exist (fit_lmm_trajectory_tsvr, validate_lmm_convergence, standard library)

**Failures:** RQ 5.8, 5.9, 5.10, 5.12, 5.13, 5.14, 5.15 (7/8) - Missing 26 tools across 3 categories

**Category 1: LMM Validation Tools (4 RQs blocked: 5.8, 5.9, 5.10, 5.15)**
- validate_lmm_assumptions_comprehensive - 7 diagnostic checks (normality, homoscedasticity, Q-Q, ACF, linearity, outliers, convergence)
- select_lmm_random_structure_via_lrt - LRT for random effects model selection
- validate_hypothesis_test_dual_pvalues - D068 compliance for hypothesis tests
- validate_contrasts_dual_pvalues - D068 compliance for post-hoc tests
- Plus 6 minor validators (data_format, effect_sizes, probability_range, numeric_range, contrasts_d068, plot_data_completeness)

**Category 2: Specialized Analysis Modules (2 RQs blocked: 5.12, 5.13)**

**CTT Analysis (RQ 5.12):**
- compute_cronbachs_alpha - Reliability with bootstrap CIs
- compare_correlations_dependent - Steiger's z-test
- NOTE: tools/analysis_ctt.py file doesn't exist yet (NEW MODULE required)

**Variance Decomposition (RQ 5.13):**
- compute_icc_from_variance_components - 3 ICC methods including conditional ICC
- test_intercept_slope_correlation_d068 - Correlation with dual p-values

**Category 3: Clustering Validation (1 RQ blocked: 5.14)**
- validate_dataframe_structure, validate_standardization, validate_cluster_assignment, validate_bootstrap_stability, validate_cluster_summary_stats
- First clustering RQ revealing new infrastructure needs

**3. Tools Status System Updates**

Created comprehensive tool tracking system across 3 files:

**tools_status.tsv Updates:**
- Marked 21 tools as GREEN (production-validated via RQ 5.1-5.7 executions)
  - IRT tools (8): Full pipeline from calibration to theta extraction
  - LMM tools (8): Model fitting, comparison, contrasts, effect sizes
  - Plotting (1): convert_theta_to_probability (D069)
  - Validation (4): IRT/LMM convergence, residuals, parameters
- Added 25 tools as ORANGE (flagged for development via rq_tools failures)
- Kept 28 tools as RED (not implemented / legacy)

**Final distribution:** GREEN 21, ORANGE 25, RED 28 (74 total tools tracked)

**Evidence for GREEN status:** context-finder agent searched archives/, found RQ 5.1-5.7 execution evidence, 4 critical bugs fixed during RQ 5.1 execution, pipeline stabilized (RQ 5.1: 4 bugs → RQ 5.3: 0 bugs → RQ 5.5: 0 bugs), validated IRT settings crisis (mc_samples 1→100), all 4 Decisions working (D039 purification 40-66% retention, D068 dual p-values, D069 dual-scale plots, D070 TSVR time variable)

**4. TDD Tool Development Roadmap**

Created docs/v4/tools_todo.yaml - comprehensive tracker for 25 ORANGE tools:

**Structure:**
- Each tool: name, module, priority (HIGH/MEDIUM/LOW), blocks_rqs, description, requirements, inputs, outputs, done status
- 9-step workflow per tool: context_finder → WebSearch → AskUser → Implement → Test (TDD) → Document inventory → Document catalog → Status YELLOW → Track done

**Priorities:**
- HIGH (6 tools, 6-8 hours): Blocks multiple RQs or creates new modules
  - check_file_exists (blocks ALL 8 RQs)
  - validate_lmm_assumptions_comprehensive (blocks 3 RQs: 5.8, 5.10, 5.15)
  - compute_cronbachs_alpha, compare_correlations_dependent (creates CTT module, blocks RQ 5.12)
  - Plus 2 LMM extensions

- MEDIUM (10 tools, 12-16 hours): Blocks 1-2 RQs, important validators
  - LMM extensions (4): random structure selection, age effects plotting, ICC computation, correlation testing
  - D068 validators (4): dual p-value compliance checkers
  - Other validators (2)

- LOW (9 tools, 6-9 hours): Nice-to-have validators (can use inline assertions)
  - Simple validators for bounds, formats, consistency

**Recommended Build Order:**
- Phase 1 Critical (4 tools, 6-8 hours): check_file_exists, validate_lmm_assumptions_comprehensive, CTT module (2 tools)
  - Unblocks 50% of RQs (5.8, 5.11, 5.12, 5.15)
- Phase 2 Medium (12 tools, 12-16 hours): LMM/validation extensions
  - Unblocks remaining RQs (5.9, 5.10, 5.13, 5.14)
- Phase 3 Low (9 tools, 6-9 hours): Simple validators
  - Optional refinements

**Total Estimated Effort:** 24-33 hours for all 25 tools

**Critical Path Analysis:**
- RQ 5.10 highest blocker (7 tools)
- RQ 5.9, 5.13, 5.14 (6 tools each)
- RQ 5.12 (3 tools, NEW module)
- RQ 5.8, 5.15 (2 tools each)
- RQ 5.11 (1 tool, can proceed soonest)

**5. Files Created/Modified This Session**

**Created:**
- docs/v4/tools_todo.yaml (25 ORANGE tools, 9-step workflow, 3 priority levels, estimated 24-33 hours)

**Modified:**
- docs/v4/tools_status.tsv (21 tools RED→GREEN production-validated, 1 tool RED→ORANGE, 24 new ORANGE tools added)
- results/ch5/rq{8,9,10,11,12,13,14,15}/docs/2_plan.md (8 plan files created by rq_planner agents)
- results/ch5/rq11/docs/3_tools.yaml (1 tools catalog created by rq_tools agent - ONLY success)
- results/ch5/rq{8,9,10,12,13,14,15}/status.yaml (7 RQs updated with rq_tools: fail status)

**6. Session Metrics**

**Session Duration:** ~90 minutes
**Token Usage:** ~91k / 200k (45% used)
**Agents Invoked:** 16 parallel (8 rq_planner + 8 rq_tools)
**Plans Created:** 8/8 (100% success rate)
**Tools Catalogs Created:** 1/8 (12.5% success rate - expected TDD behavior)
**Tools Identified:** 26 missing tools across 25 unique functions (1 duplicate: check_file_exists)
**Documentation Created:** 2 new tracking files (tools_status.tsv updates, tools_todo.yaml)
**Status Updates:** 21 tools GREEN, 25 tools ORANGE, 28 tools RED

**7. Lessons Learned**

**TDD Detection Working as Designed:**
- rq_tools agents correctly FAILED when tools missing from tools_inventory.md
- Prevented API guessing disaster (v3.0 problem)
- Clear inventory of missing infrastructure (25 tools documented)
- No improvised function signatures (validation-first approach)

**Pipeline Dependencies Clear:**
- Cross-RQ dependencies explicit (5.1→5.10/5.11/5.12/5.15, 5.7→5.8/5.9/5.13→5.14)
- Execution order constraints defined (4 tiers)
- Only RQ 5.11 can execute immediately (minimal tool needs)

**Tool Status Tracking Effective:**
- 4-color system (RED/ORANGE/YELLOW/GREEN) clear progression
- GREEN tools proven via RQ 5.1-5.7 (21 tools, 5 RQs, bug count decreased to 0)
- ORANGE tools flagged via TDD detection (25 tools, 7 RQs blocked)
- Prioritization based on blocking impact (HIGH/MEDIUM/LOW)

**Strategic Options Identified:**
- Option A: Execute RQ 5.11 now (1 tool needed, ~30 min)
- Option B: Build Phase 1 critical tools (4 tools, 6-8 hours) → execute 4 RQs
- Option C: Hybrid (start RQ 5.11, build tools in parallel)

**8. User Decision & Next Actions**

User directed: "we will start with option1 next" (referring to tools_todo.yaml recommended_order Phase 1 Critical)

**Phase 1 Critical Path (4 tools, 6-8 hours):**
1. check_file_exists - Unblocks ALL 8 RQs partially (~30 min)
2. validate_lmm_assumptions_comprehensive - Unblocks RQ 5.8, 5.10, 5.15 (~2 hours)
3. compute_cronbachs_alpha - Creates CTT module, unblocks RQ 5.12 (~1.5 hours)
4. compare_correlations_dependent - Completes CTT module (~1.5 hours)

**Workflow Per Tool (9 steps):**
1. context_finder: Research tool purpose from archives/docs
2. WebSearch: Implementation approaches, existing libraries
3. AskUser: Clarify ambiguities
4. Implement: Add to ./tools module (create analysis_ctt.py for CTT tools)
5. Test: Write extensive tests in ./tests (TDD: tests FIRST)
6. Document: Update docs/v4/tools_inventory.md (full API)
7. Document: Update docs/v4/tools_catalog.md (one-liner)
8. Status: Update to YELLOW in docs/v4/tools_status.tsv
9. Track: Mark done=true in docs/v4/tools_todo.yaml

**Expected Outcome:**
- After Phase 1: 4/8 RQs unblocked (5.8, 5.11, 5.12, 5.15 = 50%)
- Can execute those 4 RQs while building Phase 2 tools
- Remaining 4 RQs (5.9, 5.10, 5.13, 5.14) require Phase 2 tools

**Next Session Start:** Begin Phase 1 Tool Development with check_file_exists

---
