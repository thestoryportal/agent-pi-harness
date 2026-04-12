# TOOLS.md — Pi Agent Tool Signatures

## Standard Pi Tools

```ts
// Read the contents of a file. Supports text files and images.
// Output is truncated to 2000 lines or 50KB.
function read(
  path: string,         // Path to the file to read (relative or absolute)
  limit?: number,       // Maximum number of lines to read
  offset?: number       // Line number to start reading from (1-indexed)
): string;

// Execute a bash command in the current working directory.
// Returns stdout and stderr.
function bash(
  command: string,      // Bash command to execute
  timeout?: number      // Timeout in seconds (optional, no default timeout)
): string;

// Edit a file by replacing exact text.
// The oldText must match exactly (including whitespace).
function edit(
  path: string,         // Path to the file to edit (relative or absolute)
  oldText: string,      // Exact text to find and replace (must match exactly)
  newText: string       // New text to replace the old text with
): void;

// Write content to a file. Creates the file if it doesn't exist,
// overwrites if it does. Automatically creates parent directories.
function write(
  path: string,         // Path to the file to write (relative or absolute)
  content: string       // Content to write to the file
): void;

// Search file contents with regex pattern. Returns matching lines.
function grep(
  pattern: string,      // Regex pattern to search for
  path?: string,        // File or directory to search in
  glob?: string         // Glob pattern to filter files
): string;

// Find files matching a pattern.
function find(
  path: string,         // Directory to search in
  pattern?: string      // Glob pattern to match filenames
): string;

// List directory contents.
function ls(
  path: string          // Directory to list
): string;
```

## Custom Extension Tools

| Tool | Extension | Description |
|------|-----------|-------------|
| `dispatch_agent` | agent-team.ts | Dispatch a task to a specialist agent |
| `run_chain` | agent-chain.ts | Execute a named agent chain pipeline |
| `query_experts` | pi-pi.ts | Query Pi domain experts in parallel |
| `subagent_create` | subagent-widget.ts | Spawn a background subagent |
| `subagent_continue` | subagent-widget.ts | Continue an existing subagent conversation |
| `subagent_remove` | subagent-widget.ts | Kill and remove a subagent |
| `subagent_list` | subagent-widget.ts | List all active subagents |
| `drive_session` | drive-dispatch.ts | Manage tmux sessions (create/list/kill) |
| `drive_run` | drive-dispatch.ts | Execute command in tmux with Sentinel |
| `drive_send` | drive-dispatch.ts | Send raw text to tmux session |
| `drive_logs` | drive-dispatch.ts | Tail output from tmux session |
| `drive_poll` | drive-dispatch.ts | Poll for Sentinel completion |
| `listen_submit` | listen-submit.ts | Submit job to Listen HTTP server |
| `listen_status` | listen-submit.ts | Check job status |
| `listen_jobs` | listen-submit.ts | List all jobs |
| `listen_stop` | listen-submit.ts | Stop a running job |
| `send_agent_message` | agent-im.ts | Send message to another agent |
| `check_agent_messages` | agent-im.ts | Check incoming messages |
| `forge_tool` | agent-forge.ts | Build a new tool from TypeScript (scaffold) |
| `forge_list` | agent-forge.ts | List forged tools (scaffold) |
| `chronicle_start` | chronicle.ts | Start a state machine workflow (scaffold) |
| `chronicle_advance` | chronicle.ts | Advance workflow to next state (scaffold) |

## Tool Access by Agent Role

| Role | Tools |
|------|-------|
| Orchestrator | `dispatch_agent` only |
| Team Lead | `read`, `grep`, `find`, `ls`, `delegate` |
| Worker (code) | `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls` |
| Worker (read-only) | `read`, `grep`, `find`, `ls` |
| Worker (docs) | `read`, `write`, `edit`, `grep`, `find`, `ls` |
