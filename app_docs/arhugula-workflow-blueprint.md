# ArhuGula Agent Harness — Comprehensive Workflow Blueprint

**Generated:** 2026-04-14  
**Branch:** `audit/identicality-2026-04-13`  
**Architecture:** Four-layer (Skill → Subagent → Command → Justfile)  
**Technology:** Python (uv), TypeScript (pi extensions), Swift (steer), Claude Code CLI

---

## Technology Stack Detection

| Layer | Technology | Entry Point |
|-------|-----------|------------|
| Runtime | Claude Code CLI (`claude`) | Interactive + headless |
| Hook engine | Python 3.12+ via `uv run --script` (PEP 723) | Event-driven — no persistent process |
| Programmatic layer | Python 3.11+ (`run-claude.py`) | `subprocess.run(["claude", "--bare", "-p", ...])` |
| Drop Zones | Python 3.10+ (single-file UV script) | File watcher → Claude subprocess |
| SP8 apps | Python (uv per-app packages) | CLI entry: `cd apps/<app> && uv run python main.py` |
| Pi extensions | TypeScript (pi framework) | `pi -e extensions/<name>.ts` |
| GUI automation | Swift CLI (steer) | `.build/release/steer <cmd>` |
| Persistence | JSONL flat files (`.claude/logs/`) | Append-only; SQLite planned (Observe) |
| Security | `patterns.yaml` + Python hooks | Loaded on every tool call |

---

## Workflow 1 — Interactive Feature Development (Scout → Build → Review)

### 1.1 Overview

**Name:** Scout-Plan-Build pipeline  
**Business purpose:** Decompose a spec into atomic tasks, implement them sequentially with validation gates, and verify against source of truth.  
**Trigger:** User runs `just scout` or `/scout <spec-path>` in a Claude Code session.  
**Files involved:**

```
.claude/commands/scout.md          ← Scout workflow spec
.claude/commands/architect.md      ← Plan generation (optional)
.claude/commands/build.md          ← Implementation command
.claude/commands/harness-review.md ← Post-build verification
.claude/agents/team/builder.md     ← Implementation subagent
.claude/agents/team/validator.md   ← Read-only verification subagent
.claude/agents/security.md         ← Security review subagent
~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md
```

### 1.2 Entry Point — `/scout`

```
just scout
  └─ claude "/scout"
       └─ Skill: .claude/skills/scout/SKILL.md
            ├─ allowed-tools: Read, Glob, Grep  (read-only enforcement via frontmatter)
            ├─ Step 1: Locate spec ($ARGUMENTS path or interactive input)
            ├─ Step 2: Read CLAUDE.md for conventions + source-of-truth path
            ├─ Step 3: Identify implementation units
            │          Each unit: { id, title, type, artifacts, source_repo,
            │                       dependencies, validation, risk }
            ├─ Step 4: Build dependency graph (topological sort → parallelizable groups)
            └─ Step 5: Output structured JSON task list
```

**Unit types:** `hook`, `skill`, `agent`, `command`, `config`, `test`, `script`  
**Risk levels:** `low` (additive) | `medium` (modifies) | `high` (destructive/security)

### 1.3 Plan Stage — `/architect`

```
just architect
  └─ claude "/architect"       ← architect agent (read-only)
       ├─ Reads scout JSON output
       ├─ Adds file-level implementation detail to each unit
       └─ Returns ordered plan with dependency-resolved phase groupings
```

### 1.4 Build Stage — `/build`

```
just build
  └─ claude "/build"           ← builder subagent (all tools)
       ├─ Reads plan + source-of-truth section
       ├─ Implements unit-by-unit (one task → one commit pattern)
       ├─ Each implementation validated against upstream full-clone byte-identical rule
       └─ Stops on damage-control block or harness-review gate
```

### 1.5 Review Stage — `/harness-review`

```
just harness-review
  └─ claude "/harness-review"
       ├─ Step 1: git diff --stat / git diff --staged
       ├─ Step 2: Load spec + extract all MUST/SHALL requirements
       └─ Step 3: Fan out in parallel to:
            ├─ @validator  (convention + spec compliance, requirements coverage)
            └─ @security   (injection vectors, path traversal, hook bypass, data exposure)
       └─ Step 4: Aggregate → unified Priority report (P0/P1/P2/P3)
```

### 1.6 Sequence Diagram

```
User          just scout       Scout Skill     Source of Truth     just build      Builder Agent   Harness Review
  │               │                │                 │                 │                 │               │
  │──just scout──►│                │                 │                 │                 │               │
  │               │──claude /scout─►                 │                 │                 │               │
  │               │                │──Read CLAUDE.md─►                 │                 │               │
  │               │                │◄────────────────│                 │                 │               │
  │               │                │──Read spec──────────────────────► │                 │               │
  │               │                │◄──────────────────────────────────│                 │               │
  │               │                │──Decompose + JSON output          │                 │               │
  │               │◄───────────────│                 │                 │                 │               │
  │◄──────────────│                │                 │                 │                 │               │
  │               │                │                 │                 │                 │               │
  │──just build──────────────────────────────────────►                 │                 │               │
  │               │                │                 │                 │──claude /build──►               │
  │               │                │                 │                 │                 │               │
  │               │                │                 │                 │                 │──implement──► │
  │               │                │                 │                 │                 │  (per unit)   │
  │               │                │                 │                 │◄────────────────│               │
  │               │                │                 │                 │                 │               │
  │──just harness-review────────────────────────────────────────────────────────────────────────────────►│
  │               │                │                 │                 │                 │  git diff     │
  │               │                │                 │                 │                 │  fan-out──►   │
  │               │                │                 │                 │                 │  @validator   │
  │               │                │                 │                 │                 │  @security    │
  │◄──────────────────────────────────────────────────────────────────────────────────────────── P-report│
```

### 1.7 Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Hook files | `snake_case.py` | `pre_tool_use.py` |
| Commands | `lowercase-with-hyphens.md` | `harness-review.md` |
| Agents | `lowercase-with-hyphens.md` | `scout-agent.md` |
| Skills | `lowercase-with-hyphens/` dir | `damage-control/` |
| Apps | `lowercase/` in `apps/` | `apps/listen/` |
| Unit IDs | `SP{N}-U{NN}` | `SP2-U01` |
| Exception IDs | Sequential integer | Exception 30 |

### 1.8 Implementation Template — Adding a New Feature

```bash
# 1. Verify feature is in source of truth (Section 4, status = GAP)
grep -n "GAP" ~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md

# 2. Scout the spec section
just scout ~/Projects/.../arhugula-source-of-truth.md#SP_N

# 3. Build
just build

# 4. Review
just harness-review

# 5. Update source of truth: move feature from GAP → BUILT with date
```

---

## Workflow 2 — Hook Execution Pipeline (Per-Tool Safety Gate)

### 2.1 Overview

**Name:** Pre-tool safety gate  
**Business purpose:** Block dangerous operations before Claude Code executes any tool call. Defense-in-depth — three specialized hooks plus a catch-all.  
**Trigger:** Claude Code prepares to call ANY tool (automatic, ~every tool use).  
**Files involved:**

```
.claude/settings.json                                  ← Hook wiring
.claude/hooks/pre_tool_use.py                          ← Catch-all: Read/Glob/Grep + MCP gates
.claude/hooks/damage-control/hooks/damage-control-python/
    bash_damage_control.py                             ← Bash command gate
    edit_damage_control.py                             ← Edit/MultilineEdit/NotebookEdit gate
    write_damage_control.py                            ← Write gate
.claude/hooks/damage-control/patterns.yaml            ← Rule config (blocklist + allowlist)
.claude/hooks/_base.py                                 ← Shared Logger + emit_event + run_hook
```

### 2.2 Hook Dispatch (settings.json)

```json
PreToolUse handlers (in order):
  1. Bash → bash_damage_control.py     (patterns.yaml blocklist)
  2. Edit|MultilineEdit|NotebookEdit → edit_damage_control.py
  3. Write → write_damage_control.py
  4. ∅ (catch-all) → pre_tool_use.py   (Read/Glob/Grep + MCP gate)
```

### 2.3 Pre-tool Decision Tree

```
Tool call arrives
        │
        ├─ tool == "Bash" ────────────────► bash_damage_control.py
        │                                        ├─ load patterns.yaml
        │                                        ├─ check command against blocklist patterns
        │                                        │    (rm -rf, curl piped to sh, etc.)
        │                                        ├─ check pathExclusions (audit carve-outs)
        │                                        ├─ EXIT 0 → allow
        │                                        └─ EXIT 2 → block + stderr error msg
        │
        ├─ tool in Edit|MultilineEdit
        │  |NotebookEdit ─────────────────► edit_damage_control.py
        │                                        ├─ check file path against immutablePaths
        │                                        ├─ check file path against zeroAccessPaths
        │                                        ├─ EXIT 0 → allow
        │                                        └─ EXIT 2 → block
        │
        ├─ tool == "Write" ───────────────► write_damage_control.py
        │                                        └─ same path/immutable check as Edit
        │
        └─ ANY tool (catch-all) ──────────► pre_tool_use.py
                 │
                 ├─ tool.startswith("mcp__") ?
                 │        ├─ atomize tool name (split on __, -, _)
                 │        ├─ check for JS exec primitives (eval, execute_script,
                 │        │   run_code, javascript, etc.) as token subsequences
                 │        ├─ length > 512 → block (loop amplification)
                 │        ├─ non-ASCII → block (homoglyph bypass)
                 │        └─ ALLOW: emit PreToolUse event, EXIT 0
                 │
                 ├─ tool in Read|Glob|Grep ?
                 │        ├─ load patterns.yaml → zeroAccessPaths
                 │        │   (.env, ~/.ssh/*, credentials)
                 │        ├─ check pathExclusions (short-circuit for audit templates)
                 │        ├─ match_path() using PurePath.match() (path-segment-aware)
                 │        ├─ BLOCK: emit event, EXIT 2
                 │        └─ ALLOW: emit event, EXIT 0
                 │
                 └─ anything else → EXIT 0 (pass-through)
```

### 2.4 Security Model

| Rule | Behavior |
|------|---------|
| Security hook crash | EXIT 2 (fail-closed) — blocks the tool |
| Non-security hook crash | EXIT 1 (fail-open) — passes through, logs |
| `pre_tool_use.py` crash | EXIT 2 — fails closed always |
| `permission_request.py` crash | EXIT 2 — fails closed always |
| All other hooks crash | EXIT 1 — logs, passes through |
| `patterns.yaml` load failure | EXIT 2 in `pre_tool_use.py` (fail-closed) |

### 2.5 Event Logging

Every decision (allow or block) emits a structured JSONL event via `emit_event()`:

```python
emit_event(
    event_type="PreToolUse",
    hook_name="pre_tool_use.py",
    exit_code=0 or 2,
    payload={"tool": tool_name, "decision": "allow|block", "reason": "..."},
    duration_ms=elapsed
)
# → appended to .claude/logs/events.jsonl
```

### 2.6 Implementation Template — Adding a New Block Rule

```yaml
# In .claude/hooks/damage-control/patterns.yaml

# Block a dangerous Bash pattern:
dangerousPatterns:
  - pattern: "my-dangerous-command"
    description: "Why this is dangerous"
    category: "destructive"

# Block a file path from Read/Glob/Grep:
zeroAccessPaths:
  - ".my-sensitive-file"

# Allow an audit-workflow exception (temporary):
pathExclusions:
  - ".my-file.example"   # document why in audits/exceptions.md
```

---

## Workflow 3 — Session Lifecycle (Start → Work → Stop)

### 3.1 Overview

**Name:** Session lifecycle management  
**Business purpose:** Initialize secure context, correlate all events to a session ID, run TTS notifications, summarize on exit.  
**Trigger:** `claude` session opens (`SessionStart`) and closes (`Stop`/`SessionEnd`).  
**Files involved:**

```
.claude/hooks/session_start.py     ← .env whitelist + session_id + health check
.claude/hooks/session_end.py       ← Cleanup + session JSONL record
.claude/hooks/stop.py              ← TTS summary + completion message
.claude/hooks/notification.py      ← Async TTS for mid-session notifications
.claude/hooks/user_prompt_submit.py← User input pre-processing
.claude/hooks/pre_compact.py       ← Context save before compaction
.claude/hooks/_base.py             ← Logger, emit_event, run_hook
.env                               ← Secrets (never injected into child processes)
.env.example                       ← Declares which vars are INJECT-safe
.claude/logs/                      ← JSONL events + session metadata
```

### 3.2 SessionStart Flow

```
claude (session opens)
  └─ SessionStart hook → session_start.py
       ├─ 1. load_env_whitelist()
       │       ├─ Read .env.example → collect # INJECT-marked keys
       │       ├─ Read .env → filter to INJECT keys
       │       ├─ DENY any key matching SECRET/TOKEN/KEY/PASSWORD/CREDENTIAL/AUTH
       │       └─ os.environ[k] = v for safe vars only
       │
       ├─ 2. resolve_session_id()
       │       ├─ Use CLAUDE_SESSION_ID (built-in) or generate UUID4
       │       ├─ Set ARHUGULA_SESSION_ID env var
       │       └─ Write .claude/logs/session-start-{id}.json
       │
       └─ 3. Health check all hooks
               ├─ Invoke each hook with --health-check flag
               ├─ Verify exit code == 0
               └─ Log any failures to session_start.log
```

**Secret injection rule:** API keys (`*_API_KEY`, `*_TOKEN`, etc.) are never injected into `os.environ`, preventing inheritance by subprocesses (hooks, drive sessions, subagents).

### 3.3 Stop Hook — TTS Completion

```
claude (agent stops)
  └─ Stop hook → stop.py
       ├─ Check ELEVENLABS_API_KEY → elevenlabs_tts.py
       ├─ Fallback: OPENAI_API_KEY → openai_tts.py
       ├─ Fallback: pyttsx3 (no API key needed)
       └─ Speak random completion message:
            "Work complete!" | "All done!" | "Task finished!" | etc.
```

### 3.4 Event Correlation

All events include `session_id` from `get_session_id()` (resolves via `CLAUDE_SESSION_ID` → `ARHUGULA_SESSION_ID` → latest `session-start-*.json`). This allows correlating all hook events, tool calls, and cost records across a session:

```
.claude/logs/
  ├── events.jsonl              ← All PreToolUse/PostToolUse events (session-correlated)
  ├── session-start-{id}.json  ← Session metadata
  ├── pre_tool_use.log          ← Per-hook plain text log
  ├── post_tool_use.log
  ├── stop.log
  └── invocations.jsonl         ← run-claude.py cost records
```

### 3.5 Sequence Diagram

```
User          Claude Code     session_start   _base.py       stop.py         TTS
  │               │                │              │               │             │
  │──claude───────►               │              │               │             │
  │               │──SessionStart─►              │               │             │
  │               │                │─load_env────►              │             │
  │               │                │─resolve_id──►              │             │
  │               │                │─health_check (all 13 hooks) │             │
  │               │◄───────────────│              │               │             │
  │               │  [work happens — hook events emitted to events.jsonl]       │
  │               │                │              │               │             │
  │               │──Stop──────────────────────────────────────► │             │
  │               │                │              │               │─pick TTS───►│
  │               │                │              │               │             │─speak()
  │               │◄───────────────────────────────────────────── │             │
  │◄──────────────│
```

---

## Workflow 4 — Headless Programmatic Invocation

### 4.1 Overview

**Name:** External orchestrator → Claude Code subprocess  
**Business purpose:** Drive Claude Code sessions from scripts, CI, n8n, or other orchestrators without a human at the keyboard. Captures structured JSON output + cost telemetry.  
**Trigger:** `python3 scripts/run-claude.py --prompt "..." --tools Read Grep Glob`  
**Files involved:**

```
scripts/run-claude.py              ← subprocess wrapper + ClaudeResult dataclass
.claude/logs/invocations.jsonl     ← Cost telemetry (JSONL append)
justfile                           ← prime-headless, scout-headless, review-headless recipes
```

### 4.2 Invocation Flow

```
Orchestrator (n8n / CI / script)
  └─ python3 scripts/run-claude.py
       │  --prompt "..."
       │  --tools Read Grep Glob          (tool whitelist)
       │  --approved-tools Read Grep Glob (auto-approved subset)
       │  --permission-mode dontAsk
       │  --max-turns 10
       │  --workflow-id prime
       │  --invocation-type headless
       │
       ├─ InvocationConfig (dataclass)
       ├─ _build_command() → ["claude", "--bare", "-p", prompt, "--output-format", "json",
       │                       "--max-turns", "10", "--tools", "Read,Grep,Glob",
       │                       "--permission-mode", "dontAsk"]
       ├─ subprocess.run(cmd, capture_output=True, timeout=120)
       │
       ├─ Success path:
       │    └─ _parse_output() → ClaudeResult {
       │             success, result_text, cost_usd, duration_ms,
       │             duration_api_ms, num_turns, session_id, subtype
       │         }
       │
       ├─ Error paths:
       │    ├─ TimeoutExpired → ClaudeResult(subtype="error_timeout")
       │    ├─ FileNotFoundError → ClaudeResult(subtype="error_binary_not_found")
       │    └─ Non-zero exit → ClaudeResult(subtype="error_exit_{code}")
       │
       ├─ log_cost() → appends to .claude/logs/invocations.jsonl
       └─ print(json.dumps(asdict(result)))  ← structured output for orchestrator
```

### 4.3 Tool Presets

```python
SANDBOX_PRESETS = {
    "read_only":     ["Read", "Grep", "Glob"],
    "content_write": ["Read", "Grep", "Glob", "Write", "Edit"],
    "migration":     ["Read", "Grep", "Glob", "Write", "Edit", "Bash"],
    "full":          ["Read", "Grep", "Glob", "Write", "Edit", "Bash"],
}
```

### 4.4 Justfile Headless Recipes

```bash
just prime-headless              # Repository status report (read_only preset)
just scout-headless SPEC         # Spec analysis (read_only preset)
just review-headless SPEC        # Diff review against spec (read_only preset)
```

### 4.5 ClaudeResult Dataclass

```python
@dataclass
class ClaudeResult:
    success: bool
    result_text: str          # agent's final output text
    cost_usd: float           # API cost
    duration_ms: int          # wall-clock time
    duration_api_ms: int      # API-only time
    num_turns: int            # agentic turns consumed
    session_id: str           # correlates to .claude/logs/
    subtype: str              # "end_turn" | "error_*"
    raw_json: dict            # full Claude Code JSON output
    error_message: Optional[str]
```

### 4.6 Implementation Template — New Headless Recipe

```python
# In scripts/run-claude.py or as an external caller:
from run_claude import run_claude, log_cost

result = run_claude(
    prompt="Analyze the current diff and report spec violations",
    tools=["Read", "Grep", "Glob"],
    auto_approved_tools=["Read", "Grep", "Glob"],
    permission_mode="dontAsk",
    timeout=120,
    max_turns=10,
)
log_cost(result, workflow_id="my-workflow", invocation_type="ci")

if not result.success:
    sys.exit(1)
print(result.result_text)
```

```makefile
# In justfile:
my-headless-task SPEC:
    python3 scripts/run-claude.py \
        --prompt "Review {{SPEC}}" \
        --tools Read Grep Glob \
        --approved-tools Read Grep Glob \
        --permission-mode dontAsk \
        --max-turns 10 \
        --workflow-id my-task \
        --invocation-type headless
```

---

## Workflow 5 — Multi-Agent Fan-Out (Harness Review)

### 5.1 Overview

**Name:** Parallel specialist agent dispatch  
**Business purpose:** Get independent compliance + security review without a single agent's blind spots. Fan out to two read-only specialists, collect structured findings, merge into a priority-ranked report.  
**Trigger:** `just harness-review` or `/harness-review <spec>`.  
**Files involved:**

```
.claude/commands/harness-review.md    ← Fan-out orchestration command
.claude/agents/team/validator.md      ← Convention + spec compliance agent
.claude/agents/security.md            ← Adversarial security review agent
```

### 5.2 Fan-Out Flow

```
/harness-review <spec>
  │
  ├─ Step 1: Diff gathering
  │     git diff --stat
  │     git diff --stat --staged
  │     Read full diff for all changed files
  │
  ├─ Step 2: Spec loading
  │     Read <spec> → extract all MUST/SHALL/required statements
  │     Extract artifact list + naming conventions
  │
  ├─ Step 3: PARALLEL dispatch
  │     ┌──────────────────────────────┐  ┌──────────────────────────────────┐
  │     │ @validator (team/validator)  │  │ @security                        │
  │     │ Tools: Read,Grep,Glob,Bash   │  │ Tools: Read,Grep,Glob (read-only)│
  │     │ Checks:                      │  │ Checks:                          │
  │     │  - File naming conventions   │  │  - Command injection vectors     │
  │     │  - Ruff lint compliance      │  │  - Path traversal + symlinks     │
  │     │  - Schema conventions        │  │  - Secrets in logs/events        │
  │     │  - Requirements coverage     │  │  - Hook bypass scenarios         │
  │     │  - Missing spec artifacts    │  │  - MCP gate gaps                 │
  │     │  - IndyDevDan pattern match  │  │  - TOCTOU races                  │
  │     │  - Source attribution        │  │  - Homoglyph attacks             │
  │     └──────────────────────────────┘  └──────────────────────────────────┘
  │
  └─ Step 4: Aggregate report
       ## Review: <spec>
       ### Summary
         Files changed: N | Spec violations: N | Security findings: N
       ### Priority Findings
         P0 (critical): ...
         P1 (important): ...
         P2 (minor): ...
         P3 (nit): ...
       ### Detailed Findings
       ### Recommended Action Items (ordered by priority)
```

### 5.3 Agent Tool Constraints

```markdown
# team/validator.md frontmatter
tools: Read, Grep, Glob, Bash, mcp__*, Agent, ...
disallowedTools: Write, Edit, NotebookEdit

# security.md frontmatter
tools: Read, Grep, Glob
disallowedTools: Write, Edit, Bash, ...

# Both agents:
memory:
  scope: session      ← isolated — no cross-session bleed
```

### 5.4 Sequence Diagram

```
Orchestrator   harness-review.md   @validator      @security       User
     │                │                │               │              │
     │──/harness-review►              │               │              │
     │                │─git diff──────►               │              │
     │                │─Read spec──────►              │              │
     │                │                │               │              │
     │                │══════════dispatch (parallel)═══►             │
     │                │─@validator ─────►              │              │
     │                │─────────────────────────────── ►@security    │
     │                │                │               │              │
     │                │                │─Read files──► │              │
     │                │                │─Grep patterns─►              │
     │                │◄───findings────│               │              │
     │                │◄───────────────────────────────│              │
     │                │─merge + rank findings          │              │
     │──────────────────────────────────────────────────────────────► │
     │                │                │               │    P-report  │
```

### 5.5 Adding a New Review Arm

To add a third specialist (e.g., a performance reviewer):

1. Create `.claude/agents/team/perf-reviewer.md` with `tools: Read, Grep, Glob` and `disallowedTools: Write, Edit, Bash`
2. Edit `.claude/commands/harness-review.md` Step 3 to add `@perf-reviewer` in parallel
3. Update Step 4 aggregate counts: "three specialist agents"
4. Add `Performance findings: N` to summary block

---

## Common Pitfalls

| Pitfall | Context | Avoidance |
|---------|---------|-----------|
| Inventing features | Building anything not in source of truth §4 | Check §4 classification (GAP vs REJECTED) first |
| Byte-identical violation | Adding docstrings/comments to upstream code | Zero-delta rule: copied files must match `diff -q` |
| patterns.yaml edit during damage-control stop | Self-unlocking a blocked action | Stop and ask user — never self-authorize |
| Security hook exiting 1 instead of 2 | Fail-open on crash for `pre_tool_use.py` | Always `run_hook(..., security_critical=True)` |
| `pathExclusions` entries going permanent | Audit carve-outs accumulating | Document in exceptions.md, revert post-audit |
| Maintenance hook targeting `apps/backend/` | Generic template not adapted to ArhuGula | See `audits/maintenance_4-14-26_11-30-pm-mst.md` |
| MCP tool homoglyph bypass | Unicode `е` in tool name evading token match | `pre_tool_use.py` non-ASCII check (round-10) |

---

## Extension Points

| Extension | Mechanism | Where |
|-----------|----------|-------|
| New hook event type | Add to `settings.json` hooks block | `.claude/settings.json` |
| New blocked command pattern | Append to `patterns.yaml` | `damage-control/patterns.yaml` |
| New protected path | Add to `zeroAccessPaths` | `patterns.yaml` |
| New subagent | Create `agents/*.md` with frontmatter | `.claude/agents/` |
| New slash command | Create `commands/*.md` with description | `.claude/commands/` |
| New justfile recipe | Append to `justfile` with `# comment` | `justfile` |
| New headless workflow | Add recipe + `run-claude.py` call | `justfile` + `scripts/` |
| New TTS engine | Add script, update priority in `stop.py` | `.claude/hooks/utils/tts/` |
| New SP | Verify in source of truth §4, follow SP build order | Source of truth §8 |

---

## Implementation Order for New Sub-Projects

```
1. Check source of truth §4 — feature must be GAP, not REJECTED
2. Check §8 priority order — do not skip ahead
3. Run: just scout <spec-section>
4. Run: just build
5. Run: just harness-review <spec-section>
6. Document exceptions in audits/exceptions.md (if Tier 3 carve-outs needed)
7. Update source of truth §4: GAP → BUILT + date
8. Update CLAUDE.md sub-project status table
```
