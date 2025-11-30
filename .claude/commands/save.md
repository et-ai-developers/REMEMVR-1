# Save Command

**Purpose:** Persist current context before /clear with git commit

---

## Steps

### 1. Re-read state.md:

- Read `.claude/context/current/state.md` to get current state (may have been updated since /refresh)
- Understand current task context for finding relevant archived topics

### 2. Use context_finder to find relevant archived topics:

- Invoke context_finder agent to search `.claude/context/archive/` for topics relevant to current task
- Search query based on current work (keywords, RQ numbers, tools, methodologies)
- Get timestamped findings with source citations
- This ensures state.md references relevant historical context

### 3. Prepare state.md update:

- Append verbose summary of current work session to end of state.md with session timestamp header
- **Session header format:** `## Session (YYYY-MM-DD HH:MM)` using ISO 8601 format (e.g., `## Session (2025-11-11 17:30)`)
- Include under session header: what was done, decisions made, files modified, next actions
- Include "Active Topics" section (topics main claude wants context-manager to use)
- Reference relevant archived topics found by context_finder (so future sessions can find them easily)
- Don't worry about token count (context-manager will curate old sessions, keeps last 2 verbatim)
- Be verbose - context-manager archives, never condenses (zero information loss)

### 4. Git commit (BEFORE context-manager):

- Stage ALL modified files: `git add -A`
- Commit with message: "Context save: [brief summary] [timestamp]"
- This creates rollback point AND saves all uncommitted work (tools, agents, docs, etc.)

### 5. Invoke context-manager agent:

- Pass current topic context from state.md "Active Topics" section
- Context-manager will:
  - Archive content from 3+ sessions ago (if no longer relevant)
  - Keep last 2 session sections verbatim (never touched)
  - Never condense (only archive with zero information loss)
  - Conservative approach (when uncertain, keeps content)
- Wait for completion (1-2 minutes)
- DO NOT proceed if context-manager reports error

### 6. Review context-manager report:

- Check for errors
- Verify state.md is ≤20k tokens
- Verify topics archived correctly
- If error: Git revert and report to user

### 7. Final git commit (AFTER context-manager):

- Stage ALL modified files: `git add -A`
- Commit with message: "Context curated: [topics archived] [timestamp]"
- This preserves curated state AND any remaining uncommitted changes

### 8. Announce to user:

- state.md updated (X tokens → Y tokens)
- Archived content summary (topics and entry counts)
- Sessions preserved: Last 2 sessions kept verbatim
- Git commits created (ALL files committed - rollback available if needed)
- Files committed: [list modified files from git status]
- Ready for /clear
- Recommended: Run /clear now

**Example state.md after /save:**
```markdown
## What We're Doing
[Current task - updated]

## Session History

### Session (2025-11-11 14:00)
[3+ sessions old - partially archived, relevant content kept]

### Session (2025-11-11 16:00)
[N-1 session - VERBATIM]

### Session (2025-11-11 17:30)
[N session - VERBATIM - just appended]
```

---

## Do NOT

- Make archival decisions yourself (let context-manager decide)
- Condense or abbreviate your session summary (be verbose - context-manager handles curation)
- Skip git commits (critical for rollback)
- Skip context-manager invocation
- Proceed if context-manager reports error
- Forget session timestamp header (required for sliding window)

---

**Expected time:** 2-3 minutes (includes context_finder + git + context-manager execution)

**Git Integration Benefits:**
- **Rollback safety:** If context-manager makes mistake, easy revert
- **Audit trail:** Full history of ALL code and context changes
- **Two commits:** Before (raw) and after (curated) for debugging
- **User control:** User can inspect git log to see what changed
- **Work preservation:** ALL uncommitted files saved (tools, agents, docs, tests, etc.)
- **No more lost work:** Everything committed automatically, including functions/agents created during session
