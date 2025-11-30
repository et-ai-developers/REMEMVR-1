# Refresh Command

**Purpose:** Reload working context after /clear

---

## Steps

1. Read `.claude/context/current/state.md` (state memory - current task, max 20k tokens)
2. **Know that these exist** (but do NOT read them unless specifically needed):
   - `.claude/context/current/archive_index.md` (available archived context)
   - `docs/docs_index.md` (available documentation)
3. Use TodoWrite to restore task list from state.md
4. Announce to user:
   - What we were doing (current task)
   - Current progress summary
   - Next 3 actions
   - Token budget reset (now ~5-10k after loading, just state.md)
   - Last /save timestamp
   - Reminder: Archive and docs indexes available if needed via context_finder

**Note:** CLAUDE.md is automatically loaded by Claude Code system, so do NOT read it explicitly

---

## Do NOT

- Load archived context automatically (wait until needed)
- Load full documentation (use on-demand only)
- Explain the refresh process (just do it)
- Make assumptions about current task

---

**Expected time:** <10 seconds
**Expected tokens after refresh:** ~5-10k (state.md only - CLAUDE.md auto-loaded, indexes not loaded)
