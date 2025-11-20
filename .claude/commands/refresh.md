# Refresh Command

**Purpose:** Reload working context after /clear

---

## Steps

1. Read `.claude/context/current/state.md` (state memory - current task, max 20k tokens)
2. Read `.claude/context/current/archive_index.md` (available archived context)
3. Read `docs/docs_index.md` (available documentation)
4. Use TodoWrite to restore task list from state.md
5. Announce to user:
   - What we were doing (current task)
   - Current progress summary
   - Next 3 actions
   - Token budget reset (now ~10-15k after loading)
   - Last /save timestamp

**Note:** CLAUDE.md is automatically loaded by Claude Code system, so do NOT read it explicitly

---

## Do NOT

- Load archived context automatically (wait until needed)
- Load full documentation (use on-demand only)
- Explain the refresh process (just do it)
- Make assumptions about current task

---

**Expected time:** <30 seconds
**Expected tokens after refresh:** ~10-15k (state.md + indices only - CLAUDE.md auto-loaded)
