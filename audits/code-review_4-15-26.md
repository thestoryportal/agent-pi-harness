# ArhuGula Agent Harness — Comprehensive Code Review

**Date:** 2026-04-15  
**Branch:** `audit/identicality-2026-04-13`  
**Scope:** Full codebase — hooks, agents, commands, skills, scripts, apps  
**Method:** Three parallel read-only Explore agents (hooks/security, agents/commands/skills, scripts/apps)  
**Mandate:** READ-ONLY — no code was modified during this review

---

## Executive Summary

The ArhuGula harness is a well-structured, multi-layered agent development environment with
sophisticated security controls. The damage-control hook layer and session lifecycle management
demonstrate solid defensive design. However, several critical issues were identified — primarily
in the browser/device automation agents, the listen worker app, and the infinite command — that
require resolution before any production or multi-user deployment.

| Severity | Count | Immediate Action Required |
|----------|:-----:|:-------------------------:|
| **P0 Critical** | 6 | Yes |
| **P1 High** | 15 | This sprint |
| **P2 Medium** | 13 | Before release |
| **P3 Low** | 25 | Best effort |
| **Code Quality** | 10 | Maintenance backlog |
| **Total** | **69** | |

**Overall Grade: B (Solid foundation; critical agent-layer hardening needed)**

### Top 5 Findings

1. **P0** — `claude-bowser-agent.md`: Authenticated identity exposure — no domain control over real Chrome session
2. **P0** — `apps/listen/worker.py`: Shell injection via unescaped `session_name` in `osascript` + insecure `/tmp/` files
3. **P0** — `listen-drive-and-steer-system-prompt.md`: Full device automation with no operational constraints
4. **P0** — `commands/infinite.md`: Unbounded resource consumption (iterations, disk, parallelism)
5. **P1** — `apps/voice/voice_to_claude_code.py`: Ambient audio prompt injection → full tool access (Exception 28)

---

## Section 1: Hook & Security Layer

*Coverage: `.claude/hooks/`, `.claude/settings.json`, `.claude/skills/damage-control/`*

### S-01 — MCP Homoglyph Bypass in Token-Sequence Check (P2)

**File:** `.claude/hooks/pre_tool_use.py:174–187`

The `_atomize()` function splits on `__` before normalizing segments. A Unicode homoglyph placed
in a segment (e.g., Cyrillic `е` in `mcp__еxecute_script`) passes the top-level `isascii()` check
(which only checks the full tool name string) but produces a non-matching token after splitting.
The inconsistency means the defense is incomplete — the check should run on the flattened token
list post-atomization.

**Fix:** Apply `isascii()` after tokenization:
```python
tokens = _atomize(tool_name)
if not all(t.isascii() for t in tokens):
    return "block", "Non-ASCII token in tool name"
```

---

### S-02 — ALLOWED_BASH_PREFIXES Out of Sync with settings.json (P2)

**File:** `.claude/hooks/permission_request.py:30–31`

`ALLOWED_BASH_PREFIXES` lists `["mkdir", "uv", "find", "grep", "npm", "ls", "chmod", "touch"]`
but `settings.json` permissions allow `Bash(mv:*)`, `Bash(cp:*)`, `Bash(cat:*)`, `git`, `just`,
`node`, `brew`, `tmux`, and others. The hook would block these permitted commands, causing spurious
user-facing permission prompts.

**Fix:** Synchronize the list with settings.json allowlist, or derive it programmatically.

---

### S-03 — Transcript Path Injection in subagent_stop.py (P1)

**File:** `.claude/hooks/subagent_stop.py:234–253`

The hook reads `transcript_path` directly from stdin JSON without validating the path is within
`PROJECT_DIR`. An attacker with control over hook input could specify `../../.env` and read
arbitrary existing files from the filesystem.

**Fix:**
```python
safe = Path(transcript_path).resolve().is_relative_to(Path(PROJECT_DIR).resolve())
if not safe:
    logger.log("SECURITY: transcript_path outside PROJECT_DIR — blocked")
    sys.exit(1)
```

---

### S-04 — Relative Subprocess Path in user_prompt_submit.py (P2)

**File:** `.claude/hooks/user_prompt_submit.py:78–109`

LLM utility scripts are invoked via relative path (`.claude/hooks/utils/llm/ollama.py`) with no
explicit `cwd`. If the working directory changes, the subprocess call silently fails. Failure is
caught and suppressed, meaning the agent-name generation is silently skipped.

**Fix:** Use absolute path derived from `CLAUDE_PROJECT_DIR`:
```python
cwd = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
script = os.path.join(cwd, ".claude/hooks/utils/llm/ollama.py")
result = subprocess.run(["uv", "run", script], cwd=cwd, ...)
```

---

### S-05 — Backtick Escaping in split_chained_commands (P2)

**File:** `.claude/hooks/bash_damage_control.py:166–221`

The chained-command splitter does not handle escaped quotes (`\"`). At `\"`, the function toggles
`in_double`, causing misparse: a string like `cat .env && echo "test\" && echo hi"` has its second
`&&` treated as a command separator rather than part of the string.

**Fix:**
```python
if i > 0 and command[i - 1] == '\\':
    current.append(c)
    i += 1
    continue
```

---

### S-06 — Case-Insensitive Path Matching on Case-Sensitive FS (P3)

**Files:** `.claude/hooks/pre_tool_use.py:68–71`, all damage-control hooks

`case_sensitive=False` is passed to `PurePath.match()`. On Linux (case-sensitive filesystem),
`.Claude` would incorrectly match `.claude` patterns, creating false protection. Conversely, on
macOS (case-insensitive), the behavior is correct. The default should match the host OS.

**Fix:** `case_sensitive = platform.system() == 'Linux'`

---

### S-07 — Glob Pattern ReDoS in bash_damage_control.py (P3)

**File:** `.claude/hooks/bash_damage_control.py:108–119`

`glob_to_regex()` converts `*` to `[^\s/]*`, which is a negation class. A pathological filename
with many characters and no match could cause exponential backtracking.

**Fix:** Add a timeout on `re.match()` or use `fnmatch` for glob expansion.

---

### S-08 — Setup Hook Runs Without uv run Prefix (P2)

**File:** `.claude/settings.json:189–190`

All other hooks use `uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/...`. The setup hooks are called
directly via shebang without `uv run`. If `CLAUDE_PROJECT_DIR` contains shell-special characters
that slip past `session_start.py` validation, this creates an injection surface.

**Fix:** Use `uv run` prefix consistently, or document the explicit dependency on `session_start.py` validation.

---

### S-09 — Hook Ordering Dependencies Undocumented (P3)

**File:** `.claude/settings.json:35–72`

Damage-control hooks must run before `pre_tool_use.py` for the security model to be coherent.
This ordering is implicit and fragile — if someone reorders hooks, the security guarantee breaks
silently.

**Fix:** Add inline comments explaining the required order.

---

### S-10 — Hard-coded REQUIRED_HOOKS List (P3)

**File:** `.claude/hooks/session_start.py:81–94`

The health check validates a hard-coded list of hook filenames. Adding a new hook requires
manually updating this list.

**Fix:** Discover hooks dynamically from `settings.json` or from the `.claude/hooks/` directory.

---

### S-11 — Relative Path for Session Directory (P3)

**File:** `.claude/hooks/user_prompt_submit.py:56–70`

`Path(".claude/data/sessions")` uses a relative path. Should be `Path(PROJECT_DIR) / ".claude" / "data" / "sessions"`.

---

### S-12 — Bare except in setup_maintenance.py (Code Quality)

**File:** `.claude/hooks/setup_maintenance.py:46`

Bare `except:` catches `KeyboardInterrupt` and `SystemExit`. Should be `except Exception:`.

---

### S-13 — Redundant except Block in stop.py (Code Quality)

**File:** `.claude/hooks/stop.py:149–154`

Two `except` clauses where the second `except Exception` is never reached. Remove or document.

---

### S-14 — File Locking Windows Incompatibility (Code Quality)

**File:** `.claude/hooks/_base.py:93–98`

`fcntl.flock()` is POSIX-only. Will crash on Windows during concurrent hook writes. Add
platform-conditional locking or document Windows-unsupported status.

---

### S-15 — Hardcoded Validator Timeout (Code Quality)

**Files:** `.claude/hooks/validators/ruff_validator.py:66`, `ty_validator.py:84`

`timeout=120` is hard-coded. Should be configurable: `int(os.getenv("VALIDATOR_TIMEOUT", "120"))`.

---

## Section 2: Agents, Commands & Skills

*Coverage: `.claude/agents/`, `.claude/commands/`, `.claude/skills/`*

### A-01 — claude-bowser-agent: Authenticated Identity Exposure (P0)

**File:** `.claude/agents/claude-bowser-agent.md`

This agent accesses the user's real Chrome profile, meaning all existing authentication cookies,
session tokens, localStorage API keys, and browser extensions are available to it. There is:

- No domain allowlist — it can navigate anywhere credentials are valid
- No page-instruction blocking — a malicious page can direct the agent further
- No sensitive-data filtering in screenshots — captures passwords, API keys, banking UIs

**Fix (required before any use on sensitive machines):**
```yaml
# Add to agent definition:
allowedDomains: [explicitly-listed domains only]
blockPageInstructions: true
screenshotRedaction: [password-field, form-input]
```

---

### A-02 — listen-drive-and-steer: Full Device Control Without Guardrails (P0)

**Files:** `.claude/agents/listen-drive-and-steer-system-prompt.md`, `.claude/commands/listen-drive-and-steer-user-prompt.md`

The agent is granted full access to macOS GUI (steer) and terminal (drive) with `$ARGUMENTS` taken
from user prompt with no sanitization. There are no explicit prohibitions against:
- Exfiltrating files via clipboard or email
- Accessing open sensitive applications (banking, password manager)
- System configuration modification
- Keylogging via accessibility API

**Fix:** Add a "DO NOT" constraint block:
```
DO NOT: read or transmit file contents outside PROJECT_DIR, interact with
financial/healthcare apps, modify system preferences, access password manager
windows, or write to clipboard without explicit user confirmation.
```

---

### A-03 — infinite Command: Unbounded Resource Consumption (P0)

**File:** `.claude/commands/infinite.md:41–110`

The command deploys waves of 3–5 parallel agents with no hard cap on:
- Total iterations (stops only when "approaching context limits")
- Wave count
- Disk write volume (accumulates all generations in `output_dir`)

**Attack scenario:** `/infinite /tmp/evil-spec.md /tmp/output infinite` → fills disk indefinitely.

**Fix:**
```
MAX_ITERATIONS = min(count, 100)
MAX_WAVE_TIMEOUT = 300s per wave
DISK_QUOTA_CHECK: refuse if output_dir > 1GB
```

---

### A-04 — generic-browser-test: Port Collision in Parallel Agents (P0)

**File:** `.claude/commands/generic-browser-test.md:100–104`

Deterministic port assignment uses `9222 + workflow_index`. If two instances run simultaneously
with overlapping indices, agents silently fail to bind and tests produce false results.

**Fix:** Check port availability before spawning:
```bash
until ! lsof -i ":$PORT" > /dev/null 2>&1; do PORT=$((PORT + 1)); done
```

---

### A-05 — docs-scraper Agent: SSRF + Path Traversal (P1)

**File:** `.claude/agents/docs-scraper.md`

`mcp__firecrawl-mcp__firecrawl_scrape` and `WebFetch` are called with no domain allowlist.
The agent writes fetched content to arbitrary filenames derived from user input, with no path
traversal check. Running this agent inside an internal network creates an SSRF vector.

**Fix:** Restrict domains (anthropic.com, github.com docs only), validate output paths with
`Path(filename).resolve().is_relative_to(PROJECT_DIR)`.

---

### A-06 — meta-agent: Fetches Docs at Runtime (P1)

**File:** `.claude/agents/meta-agent.md:15–17`

Fetches Anthropic documentation from the live internet during agent-config generation. A MITM or
compromised CDN could inject malicious instructions into the documentation, which the agent would
then bake into generated `.claude/agents/*.md` files. Additionally, no agent name validation means
`../../malicious.md` is a valid write target.

**Fix:** Hardcode the docs snippets. Validate agent name: `re.match(r'^[a-z0-9][a-z0-9-]*$', name)`.

---

### A-07 — builder PostToolUse Hooks: Non-Blocking Lint (P1)

**File:** `.claude/agents/team/builder.md:8–15`

`ruff_validator.py` and `ty_validator.py` are wired as PostToolUse hooks, but the builder
continues regardless of validator exit codes (fail-open). Lint and type failures are logged but
don't stop the agent from proceeding.

**Fix:** Confirm validators use `sys.exit(2)` on failure, or add a PostToolUse gate that reads
the hook result and halts the builder on non-zero.

---

### A-08 — load_ai_docs: Unvalidated URLs from README (P2)

**File:** `.claude/commands/load_ai_docs.md`

URLs are read from `ai_docs/README.md` without validation. Any URL in that file is fetched,
creating an SSRF vector if the file is tampered with.

**Fix:** Hardcode approved documentation URLs or validate against a whitelist regex
(`^https://(docs\.anthropic\.com|raw\.githubusercontent\.com)/`).

---

### A-09 — work-completion-summary: Bash Constraint Not Enforced in Tool Definition (P2)

**File:** `.claude/agents/work-completion-summary.md:37`

The prompt says "only use bash: 'pwd'", but the agent's tool definition allows unrestricted Bash.
A prompt injection in the summary context could abuse the Bash access.

**Fix:** Add `allowedTools: [Bash(pwd), mcp__ElevenLabs__text_to_speech, mcp__ElevenLabs__play_audio]`
to the agent YAML header.

---

### A-10 — bowser Commands: Arbitrary URL Access (P2)

**Files:** `.claude/commands/bowser/blog-summarizer.md`, `amazon-add-to-cart.md`

`blog-summarizer` passes raw `{PROMPT}` URLs directly to the headless browser with no domain
validation. `amazon-add-to-cart` uses real Chrome with Amazon auth cookies — the agent accesses
a real user account. The "stop before checkout" safeguard is documented but not technically enforced.

**Fix:** Add URL validation (allowlist or at minimum TLD check). Document amazon-add-to-cart
account-access risk explicitly in SKILL.md.

---

### A-11 — hop-automate: Workflow Content Not Validated (P2)

**File:** `.claude/commands/bowser/hop-automate.md:44–45`

Workflow name is validated correctly (`^[a-z0-9][a-z0-9-]*$`), but the workflow file *contents*
are not scanned before execution. A compromised workflow file could contain injected instructions.

**Fix:** Add content validation or signature check before executing workflow.

---

### A-12 — Agents: No Cost Budget on Model Selection (P2)

Several agents specify `model: opus` (builder, validator) with no per-session cost budget.
The `infinite` command compounds this — spawning many opus agents in parallel is expensive with
no guardrail.

**Fix:** Add session-level model budget or warn when opus agents are spawned in parallel.

---

### A-13 — Agent Tool Access is Opt-Out (Architectural) (P2)

`settings.json` defines a global permission allowlist, and agents restrict via `disallowedTools`.
This is an opt-out model — new agents inherit all global permissions unless explicitly restricted.

**Recommendation:** Move to opt-in for write-capable tools. Require agents to explicitly declare
`allowedTools` rather than only declaring `disallowedTools`.

---

### A-14 — drive Skill: Process Kill Without Ownership Tracking (P2)

**File:** `.claude/skills/drive/SKILL.md:99–102`

`drive proc kill --name "claude"` kills any process matching the name, not just ones the agent
started. `drive proc kill 12345 --tree` terminates all children regardless of ownership.

**Fix:** Track PIDs started within the agent session; only permit killing those.

---

### A-15 — steer Skill: Sensitive Field Detection Not Enforced (P3)

**File:** `.claude/skills/steer/SKILL.md:136–154`

The SKILL.md correctly documents that `steer clipboard read` and `steer see` can capture
passwords. However, this is advisory only — no technical enforcement prevents it.

**Recommendation:** Document that steer should never be invoked on sessions with sensitive
applications open, and consider adding a pre-flight check for active password manager windows.

---

### A-16 — agent-sandboxes: Template Name Not Validated (P3)

**File:** `.claude/skills/agent-sandboxes/SKILL.md:64–65`

Sandbox template name taken from user input with no validation before passing to `sbx` CLI.

**Fix:** Validate against a known template list or apply `^[a-z0-9][a-z0-9-]*$` regex.

---

### A-17 — Architect/Scout/Security/Validator Agents: All Safe (Pass)

`architect.md`, `scout-agent.md`, `security.md`, `team/validator.md` are all correctly
configured as read-only (Read, Grep, Glob; `disallowedTools: Write, Edit`). No issues.

---

## Section 3: Scripts, Apps & Justfile

*Coverage: `justfile`, `scripts/`, `apps/`, `tests/`, `.env.example`*

### B-01 — listen/worker.py: Shell Injection via session_name in osascript (P0)

**File:** `apps/listen/worker.py:34–40`

```python
tmux_cmd = f"cd '{cwd}' && tmux new-session -A -s {session_name}"
escaped = tmux_cmd.replace("\\", "\\\\").replace('"', '\\"')
subprocess.run(["osascript", "-e", f'tell application "Terminal" to do script "{escaped}"'], ...)
```

`session_name` is inserted into the f-string before double-quote escaping. If `session_name`
contains a single quote, the `cd '{cwd}'` clause breaks and arbitrary shell commands can be
injected. The double-quote escaping only protects the outer osascript string, not the inner
tmux command.

**Fix:** Validate `session_name` against `^[a-z0-9][a-z0-9_-]+$` before use, and use shlex
quoting for the inner `tmux` arguments.

---

### B-02 — listen/worker.py: Insecure Temp Files at /tmp/ (P0)

**File:** `apps/listen/worker.py:96–100`

```python
sys_prompt_tmp = Path(f"/tmp/steer-sysprompt-{job_id}.txt")
sys_prompt_tmp.write_text(sys_prompt)
```

Temp files are world-readable by default in `/tmp/` and names are predictable (job_id is
sequential). Any local process can read system prompt contents.

**Fix:**
```python
import tempfile, stat
fd, path = tempfile.mkstemp(prefix="steer-sysprompt-", dir="/var/tmp")
os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 0600
with os.fdopen(fd, 'w') as f:
    f.write(sys_prompt)
```

---

### B-03 — voice/voice_to_claude_code.py: Ambient Prompt Injection (P1)

**File:** `apps/voice/voice_to_claude_code.py:84, 426`

*Documented as Exception 28 (upstream byte-identical)*

Trigger-word check: `any(trigger.lower() in message.lower() for trigger in ["claude", "cloud", "sonnet", "sonny"])`.
Raw STT transcript is passed directly to `claude -p` with full tool access after only this
substring match. False positives ("cloudy day", "sonnet poetry") trigger arbitrary tool execution.
Subprocess inherits full parent environment including `ANTHROPIC_API_KEY`.

**Status:** Dormant (requires microphone input). Runtime isolation required (do not run in shared spaces).

**Mitigation path:** Add a confirmation step before executing (show transcript, require "yes" keypress).

---

### B-04 — sandbox_mcp/server.py: env_vars Comma-Split Injection (P1)

**File:** `apps/sandbox_mcp/server.py:107–109, 143–145`

*Documented as Exception 29 (upstream byte-identical)*

```python
for env_pair in env_vars.split(","):
    args.extend(["--env", env_pair.strip()])
```

Agent-supplied `env_vars` like `LEGIT=val,FOO=x --root` would inject `--root` as a separate
CLI flag. No validation applied before splitting.

**Status:** Dormant (no `E2B_API_KEY` in `.env`).

**Fix:** Validate each pair: `re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', pair)`.

---

### B-05 — listen/worker.py: Headless Session Uses --dangerously-skip-permissions (P2)

**File:** `apps/listen/worker.py:108`

Worker spawns `claude --dangerously-skip-permissions`. Any prompt submitted to the listen server
(port 7600) runs with unrestricted tool access. The server has no authentication.

**Risk:** If port 7600 is reachable by untrusted callers, arbitrary tool execution is possible.

**Fix:** Add authentication token to listen server, or bind to 127.0.0.1 only and document.

---

### B-06 — listen/main.py: No Input Validation or Rate Limiting (P2)

**File:** `apps/listen/main.py:48–53`

`req.prompt` is passed to the worker subprocess via `sys.argv` with no:
- Length limit (can cause resource exhaustion)
- Character validation
- Per-IP rate limiting
- Authentication

**Fix:** Add `max_length=32768` to the prompt field, add token-bucket rate limiting.

---

### B-07 — dropzone: Filename Template Injection (P2)

**File:** `apps/dropzone/sfs_agentic_drop_zone.py`

`FILE_PATH_PLACEHOLDER = "[[FILE_PATH]]"` is substituted into prompt templates using the raw
filesystem path. A crafted filename like `file_[[SYSTEM_PROMPT]].txt` could inject into other
template slots.

**Fix:** Sanitize filenames before template substitution: strip template-syntax characters
(`[[`, `]]`, `{{`, `}}`).

---

### B-08 — dropzone: No Concurrency Locking (P2)

**File:** `apps/dropzone/sfs_agentic_drop_zone.py`

Filesystem events handled concurrently without locking. If the same file is modified while being
processed, duplicate jobs may be submitted or partial reads may occur.

**Fix:** Track in-flight file paths with a lock set; skip events for paths already being processed.

---

### B-09 — listen/worker.py: No Timeout on tmux Polling (P2)

**File:** `apps/listen/worker.py:~137`

The worker polls tmux for session completion without a timeout. If the claude session hangs, the
worker waits indefinitely, exhausting worker threads.

**Fix:** Add a wall-clock timeout (e.g., `deadline = time.time() + 3600`).

---

### B-10 — scripts/run-claude.py: Stderr Truncation Loses Context (P3)

**File:** `scripts/run-claude.py:146, 151`

Error output is truncated to 500 chars. Long compilation or lint errors lose context.

**Fix:** Log full stderr to `.claude/logs/`, return truncated version to caller.

---

### B-11 — observe/prune.py: Malformed JSONL Kept Silently (P3)

**File:** `apps/observe/prune.py:65–77`

Unparseable JSONL lines are retained ("don't lose data"). Over time, the log fills with
garbage lines that are never cleaned.

**Fix:** Write corrupt lines to `.jsonl.corrupt` sidecar file and emit a warning.

---

### B-12 — No Unit Tests for Subprocess Invocations (Code Quality)

**Files:** `scripts/run-claude.py`, `apps/listen/worker.py`, `apps/voice/voice_to_claude_code.py`

No unit tests exist for subprocess construction logic. The shell injection in B-01 went
undetected for this reason.

**Fix:** Add pytest unit tests that mock `subprocess.run` and verify argument list construction.

---

### B-13 — Justfile: No Shell Quoting for Variable Interpolation (Code Quality)

**File:** `justfile`

Several recipes use unquoted `{{SPEC}}` and `{{PROMPT}}` interpolations. In `just`, these are
shell-interpolated; a value with spaces could break the invocation.

**Fix:** Quote interpolated variables: `"{{SPEC}}"`.

---

## Section 4: Cross-Cutting Findings

### X-01 — No Domain Allowlist Enforcement Across Browser Agents

The entire browser automation surface (claude-bowser-agent, playwright-bowser-agent,
bowser-qa-agent, generic-browser-test) lacks any mechanism to prevent navigation to
unintended domains. This is a systemic gap, not an individual agent issue.

**Recommendation:** Establish a harness-level browser policy:
```yaml
# .claude/browser-policy.yaml
defaultPolicy: deny
allowedDomains: []  # must be explicitly listed per task
blockExternalNavigation: true
```

---

### X-02 — Security Findings Are Well-Documented (Positive)

The exceptions audit system (`/audits/exceptions.md`, 1685+ lines) provides comprehensive
tracking of every deviation from upstream Disler repos, including security findings with
dormancy status, blast-radius analysis, and activation conditions. This is exemplary practice.

---

### X-03 — Damage-Control Layer is Well-Designed (Positive)

The three-hook damage-control layer (bash/edit/write) with explicit `zeroAccessPaths`,
`readOnlyPaths`, and `noDeletePaths` tiers, combined with the `exit 0/1/2` semantics and
fail-closed behavior on security hooks, represents a solid defensive design that should be
preserved and extended.

---

### X-04 — Fail-Open vs Fail-Closed Not Tagged in settings.json

CLAUDE.md specifies the fail-open/fail-closed distinction, but nothing in `settings.json`
marks which hooks are security-critical (fail-closed) vs diagnostic (fail-open). An operator
adding a new hook has no indication of which exit code semantics apply.

**Fix:** Add a `"securityHook": true` field convention or comment block in settings.json.

---

### X-05 — patterns.yaml Not Protected from Tampering (P1)

*Previously identified in SP2 architectural follow-up (P0 class)*

`patterns.yaml` defines the damage-control rules. The file is not integrity-checked at
runtime — a compromised agent that can write to the project directory could weaken or disable
the rules. This was flagged in the harness-review action items.

**Fix:** Add HMAC or SHA-256 hash validation of `patterns.yaml` at session start.

---

## Section 5: Priority Action Items

| # | Priority | Component | Finding | Action |
|---|----------|-----------|---------|--------|
| 1 | **P0** | `agents/claude-bowser-agent.md` | Auth exposure, no domain control | Add mandatory domain allowlist + page-instruction blocking |
| 2 | **P0** | `apps/listen/worker.py:34–40` | Shell injection in osascript | Validate session_name + use shlex quoting |
| 3 | **P0** | `apps/listen/worker.py:96–100` | Insecure /tmp/ temp files | Use tempfile.mkstemp + chmod 0600 |
| 4 | **P0** | `agents/listen-drive-and-steer-system-prompt.md` | Full device control, no constraints | Add explicit DO NOT constraint block |
| 5 | **P0** | `commands/infinite.md` | Unbounded resource consumption | Cap iterations, add wave timeout + disk quota |
| 6 | **P0** | `commands/generic-browser-test.md:100–104` | Port collision in parallel agents | Check port availability before spawning |
| 7 | **P1** | `hooks/subagent_stop.py:234–253` | Transcript path injection | Validate path is within PROJECT_DIR |
| 8 | **P1** | `agents/docs-scraper.md` | SSRF + path traversal | Domain allowlist + filename sanitization |
| 9 | **P1** | `agents/meta-agent.md` | Runtime doc fetch + name traversal | Hardcode docs, validate agent name regex |
| 10 | **P1** | `agents/team/builder.md` | Non-blocking lint hooks | Confirm exit 2 on failure; gate further work |
| 11 | **P1** | `apps/voice/voice_to_claude_code.py` | Ambient prompt injection (Ex. 28) | Add confirmation step before execution |
| 12 | **P1** | `apps/sandbox_mcp/server.py` | env_vars comma-split injection (Ex. 29) | Validate each pair before extending args |
| 13 | **P1** | `.claude/skills/damage-control/` + patterns.yaml | patterns.yaml unprotected (Ex. SP2) | Add hash validation at session start |
| 14 | **P2** | `hooks/permission_request.py:30–31` | ALLOWED_BASH_PREFIXES out of sync | Sync with settings.json |
| 15 | **P2** | `hooks/user_prompt_submit.py:78–109` | Relative subprocess path | Use absolute path from CLAUDE_PROJECT_DIR |
| 16 | **P2** | `hooks/bash_damage_control.py:166–221` | Backtick escaping in command split | Track escape state in split loop |
| 17 | **P2** | `apps/listen/main.py` | No auth, no rate limiting | Add token auth + rate limiting |
| 18 | **P2** | `apps/listen/worker.py:108` | --dangerously-skip-permissions in worker | Bind to 127.0.0.1, document access control |
| 19 | **P2** | `apps/dropzone/sfs_agentic_drop_zone.py` | Filename template injection | Sanitize filenames before substitution |
| 20 | **P2** | `agents/work-completion-summary.md` | Bash not constrained in tool definition | Add `allowedTools` to YAML header |
| 21 | **P2** | `hooks/settings.json` | Fail-open/closed not tagged | Add `securityHook` convention |
| 22 | **P3** | `hooks/pre_tool_use.py:174–187` | Homoglyph bypass post-atomization | Apply isascii() on flattened tokens |
| 23 | **P3** | All hooks | case_sensitive=False mismatch | Use platform-conditional case sensitivity |
| 24 | **P3** | `hooks/session_start.py:81–94` | REQUIRED_HOOKS hard-coded | Derive from settings.json dynamically |
| 25 | **P3** | `scripts/run-claude.py:146` | Stderr truncated at 500 chars | Log full stderr to file |
| 26 | **P3** | `apps/observe/prune.py:65–77` | Corrupt JSONL kept silently | Write to .jsonl.corrupt sidecar |
| 27 | **CQ** | `hooks/setup_maintenance.py:46` | Bare `except:` | Change to `except Exception:` |
| 28 | **CQ** | `hooks/_base.py:93–98` | fcntl.flock Windows incompatible | Add platform-conditional locking |
| 29 | **CQ** | `hooks/validators/` | Timeout hard-coded at 120s | `int(os.getenv("VALIDATOR_TIMEOUT", "120"))` |
| 30 | **CQ** | `justfile` | Unquoted variable interpolations | Quote `"{{SPEC}}"` etc. |

---

## Appendix: Agents Passing Review

The following agents have correct tool constraints and no findings:

| Agent | Tools | Status |
|-------|-------|--------|
| `architect.md` | Read, Grep, Glob (read-only) | ✅ Pass |
| `scout-agent.md` | Read, Grep, Glob (read-only) | ✅ Pass |
| `security.md` | Read, Grep, Glob (read-only) | ✅ Pass |
| `team/validator.md` | Read, Glob, Grep; disallows Write/Edit | ✅ Pass |
| `playwright-bowser-agent.md` | Headless, isolated sessions | ✅ Pass (no auth persistence) |
| `bowser-qa-agent.md` | Playwright skill, session nonce | ✅ Pass (minor isolation note) |

---

*Generated by three parallel read-only Explore agents — no code was modified during this review.*
