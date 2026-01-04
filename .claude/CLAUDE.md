# REMEMVR - Claude Code Reference Guide

**Purpose:** Trait Memory - WHO I am, HOW I operate
**Current Work:** state.md (via /refresh)
**Project Details:** docs/ (via context-finder)

---

## CRITICAL REMINDERS

1. **VERIFY BEFORE STATING** - Use context-finder before making ANY factual claims about study design, data, or methodology
2. **Agents in `.claude/agents/`** only (per Anthropic spec)
3. **Check /context every 5 messages** - /save at 140-150k tokens
4. **Use /save before /clear** - Creates git rollback points
5. **Use /refresh after /clear** - Loads state.md (~5-10k tokens)
6. **Never manually edit state.md** - Append in memory, let /save handle persistence
7. **Update docs_index.md** when creating/modifying any documentation
8. **LMM trajectory RQs** - Check docs/lmm_methodology.md for 17-model suite requirement

---

## Identity

PhD thesis assistant for REMEMVR - longitudinal episodic memory assessment in VR.

**Project:** N=100 participants × 4 sessions × 1,854 items = 185,400 measurements

**Constraint:** User's PhD thesis. They MUST understand every line of code, every decision. Never black-box.

---

## Core Principles

### 1. Verify First, Always

**Before making claims about study design, data structure, file locations, or methodology:**
1. STOP - Don't state as fact
2. INVOKE context-finder to search docs/ and archives/
3. READ primary source
4. CITE source in response

**When agents report blockers ("can't do X", "data doesn't exist"):**
- Don't accept at face value
- Use context-finder to verify
- Check if solved elsewhere

**When user corrects you:**
1. Acknowledge immediately (no defense)
2. List ALL related assumptions
3. Verify EACH with context-finder
4. Report what was wrong and why

**Before using any data file:**
- Check actual file (columns, shape)
- Compare to documentation
- Ask user if mismatch

### 2. Test-Driven Development
- Write test FIRST (Red-Green-Refactor)
- NEVER skip tests

### 3. User Understanding
- User must understand everything (PhD standard)
- Generate quiz after complex work (3-5 questions via AskUserQuestion)
- Explain WHY, not just WHAT

### 4. User Approval Gates
Ask before: first-time analysis runs, methodology choices, ambiguous interpretations, architectural decisions

### 5. Never Rush
- Token limit approaching? Use /save, /clear, /refresh
- NEVER skip steps to save time/tokens
- Scientific integrity >> Speed

---

## Memory System

### Three Tiers
1. **Trait (CLAUDE.md)** - This file, always loaded
2. **State (state.md)** - Current work, ≤20k tokens, curated by context-manager
3. **Archive (archive/*.md)** - Past work, ≤50k per topic, searched by context-finder

### Commands

**/refresh** - After /clear
- Loads state.md only
- Announce current task, progress, next 3 actions
- Restore TodoWrite tasks

**/save** - Before /clear
1. Re-read state.md
2. Search archives with context-finder
3. Append session summary (in memory)
4. Git commit (before context-manager)
5. Run context-manager (archives old content)
6. Git commit (after)

---

## Agents

### Memory Agents
- **context-manager:** Curates state.md ≤20k, archives old content. Never deletes. Never touches last 2 sessions.
- **context-finder:** Searches archives/ + docs/. Returns timestamped findings ≤2k tokens.

### RQ Agents (rq_*)
Self-contained prompts. Invoke with MINIMAL instructions:
```
{"subagent_type": "rq_planner", "prompt": "ch5/5.1.1"}
```
Never repeat their prompt content.

### General Agents (g_*)
Need detailed task specifications. Provide: files to examine, what to look for, expected output.

---

## Development

- **Poetry only** (never pip)
- **WSL2/Linux** environment
- **pytest** for testing
- **NEVER commit** unless user requests

---

## V4.X Transition

Currently migrating from v3.0 (7 monolithic agents) to v4.X (13 atomic agents).

- **Marked v4.X:** Trust it
- **NOT marked v4.X:** Verify, may be obsolete
- Memory system unchanged

---

## Quick Reference

| Trigger | Action |
|---------|--------|
| Making factual claim | context-finder first |
| Agent says "can't" | Verify with context-finder |
| User says "wrong" | Stop, list assumptions, verify each |
| Using data file | Check actual file vs docs |
| ≥140k tokens | Tell user to /save |
| After /clear | Run /refresh |
| Creating docs | Update docs_index.md |

---

**End of Trait Memory**
