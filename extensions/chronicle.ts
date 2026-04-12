/**
 * Chronicle — Temporal state machine workflows
 *
 * Manages long-running, state-aware workflows that span multiple Pi sessions.
 * Each workflow is a formal state machine with:
 *   - Named states (e.g., planning → building → reviewing → done)
 *   - Specialized agent per state (dispatched via agent-team)
 *   - Persistent ledger (.pi/chronicles/<workflow-id>.jsonl) for recovery
 *   - Anti-looping guards (max 3 transitions between same two states)
 *
 * SCAFFOLD STATUS: State machine types, ledger I/O, and tool registration defined.
 * State transitions and agent dispatch are stubs — chronicle_advance records the
 * transition but does not automatically dispatch the next agent.
 * Full implementation: integrate with agent-team dispatch, implement transition guards.
 *
 * Usage: pi -e extensions/chronicle.ts -e extensions/agent-team.ts
 *
 * Tools provided:
 *   chronicle_start    — Start a new workflow
 *   chronicle_advance  — Advance to next state
 *   chronicle_status   — Check workflow status
 *   chronicle_history  — Show full ledger
 *   chronicle_list     — List active workflows
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import * as fs from "fs";
import * as path from "path";
import { applyExtensionDefaults } from "./themeMap.ts";

// ── Types ────────────────────────────────────────────────────

interface StateDefinition {
	name: string;
	agent: string;          // agent name that handles this state
	description: string;
	terminal: boolean;      // if true, workflow ends here
}

interface WorkflowDefinition {
	id: string;
	name: string;
	states: StateDefinition[];
	created: string;
}

interface LedgerEntry {
	timestamp: string;
	fromState: string | null;
	toState: string;
	agentOutput: string;
	outcome: "success" | "failure" | "skipped";
}

interface WorkflowInstance {
	workflowId: string;
	definition: WorkflowDefinition;
	currentState: string;
	ledger: LedgerEntry[];
	transitionCounts: Record<string, number>;  // "from->to" => count
	status: "active" | "complete" | "failed";
}

const CHRONICLES_DIR = ".pi/chronicles";
const MAX_SAME_TRANSITION = 3;  // anti-looping guard

// ── Ledger I/O ───────────────────────────────────────────────

function getLedgerPath(cwd: string, workflowId: string): string {
	return path.join(cwd, CHRONICLES_DIR, `${workflowId}.jsonl`);
}

function appendLedger(cwd: string, workflowId: string, entry: LedgerEntry): void {
	const ledgerPath = getLedgerPath(cwd, workflowId);
	fs.mkdirSync(path.dirname(ledgerPath), { recursive: true });
	fs.appendFileSync(ledgerPath, JSON.stringify(entry) + "\n");
}

// ── Extension ────────────────────────────────────────────────

export default function (pi: ExtensionAPI) {
	const instances: Map<string, WorkflowInstance> = new Map();
	let cwd = process.cwd();

	pi.on("session_start", async (_event, ctx) => {
		applyExtensionDefaults(import.meta.url, ctx);
		cwd = ctx.cwd;
		ctx.ui.setStatus("chronicle", `Chronicle: ${instances.size} active`);
		ctx.ui.notify(
			`Chronicle loaded — ${instances.size} active workflow(s)\n\n` +
			`chronicle_start    — Start a new state machine workflow\n` +
			`chronicle_advance  — Advance to next state (stub — manual dispatch)\n` +
			`chronicle_status   — Check current workflow status\n` +
			`chronicle_history  — Show full ledger\n` +
			`chronicle_list     — List all workflows\n\n` +
			`SCAFFOLD: State transitions are recorded but agent dispatch is manual.\n` +
			`Anti-looping guard: max ${MAX_SAME_TRANSITION} same-pair transitions enforced.`,
			"info",
		);
	});

	pi.registerTool({
		name: "chronicle_start",
		label: "Chronicle Start",
		description: "Start a new state machine workflow. Define the states and which agent handles each.",
		parameters: Type.Object({
			name: Type.String({ description: "Human-readable workflow name" }),
			states_json: Type.String({
				description: `JSON array of state definitions. Example:
[
  {"name": "planning", "agent": "planner", "description": "Define the work", "terminal": false},
  {"name": "building", "agent": "builder", "description": "Implement it", "terminal": false},
  {"name": "reviewing", "agent": "reviewer", "description": "Verify quality", "terminal": false},
  {"name": "done", "agent": "", "description": "Workflow complete", "terminal": true}
]`
			}),
		}),
		async execute(_toolCallId, params, _signal, _onUpdate, _ctx) {
			const { name, states_json } = params as any;

			let states: StateDefinition[];
			try {
				states = JSON.parse(states_json);
			} catch {
				return { content: [{ type: "text", text: "Error: states_json must be valid JSON" }] };
			}

			const workflowId = `${name.toLowerCase().replace(/\s+/g, "-")}-${Date.now()}`;
			const definition: WorkflowDefinition = {
				id: workflowId,
				name,
				states,
				created: new Date().toISOString(),
			};

			const instance: WorkflowInstance = {
				workflowId,
				definition,
				currentState: states[0]?.name || "unknown",
				ledger: [],
				transitionCounts: {},
				status: "active",
			};

			instances.set(workflowId, instance);

			const entry: LedgerEntry = {
				timestamp: new Date().toISOString(),
				fromState: null,
				toState: states[0]?.name || "unknown",
				agentOutput: "Workflow started",
				outcome: "success",
			};
			appendLedger(cwd, workflowId, entry);
			instance.ledger.push(entry);

			return {
				content: [{ type: "text", text: `Workflow "${name}" started (ID: ${workflowId})\nCurrent state: ${instance.currentState}\nStates: ${states.map(s => s.name).join(" → ")}` }],
				details: { workflowId, instance },
			};
		},
	});

	pi.registerTool({
		name: "chronicle_advance",
		label: "Chronicle Advance",
		description: `Advance workflow to the next state. Checks anti-looping guard (max ${MAX_SAME_TRANSITION} same-pair transitions). SCAFFOLD: Does not auto-dispatch the next agent — call dispatch_agent manually.`,
		parameters: Type.Object({
			workflow_id: Type.String({ description: "Workflow ID to advance" }),
			outcome: Type.String({ description: "Outcome of current state: 'success' or 'failure'" }),
			agent_output: Type.String({ description: "Summary of what the current state's agent produced" }),
		}),
		async execute(_toolCallId, params, _signal, _onUpdate, _ctx) {
			const { workflow_id, outcome, agent_output } = params as any;
			const instance = instances.get(workflow_id);
			if (!instance) {
				return { content: [{ type: "text", text: `Workflow "${workflow_id}" not found.` }] };
			}

			const currentStateIdx = instance.definition.states.findIndex(s => s.name === instance.currentState);
			if (currentStateIdx === -1 || instance.definition.states[currentStateIdx].terminal) {
				return { content: [{ type: "text", text: `Workflow is already in terminal state: ${instance.currentState}` }] };
			}

			const nextState = instance.definition.states[currentStateIdx + 1];
			if (!nextState) {
				instance.status = "complete";
				return { content: [{ type: "text", text: `Workflow "${workflow_id}" complete.` }] };
			}

			// Anti-looping guard
			const transitionKey = `${instance.currentState}->${nextState.name}`;
			instance.transitionCounts[transitionKey] = (instance.transitionCounts[transitionKey] || 0) + 1;
			if (instance.transitionCounts[transitionKey] > MAX_SAME_TRANSITION) {
				instance.status = "failed";
				return {
					content: [{ type: "text", text: `BLOCKED: Anti-looping guard triggered. Transition ${transitionKey} has occurred ${instance.transitionCounts[transitionKey]} times (max ${MAX_SAME_TRANSITION}). Workflow failed.` }],
				};
			}

			const entry: LedgerEntry = {
				timestamp: new Date().toISOString(),
				fromState: instance.currentState,
				toState: nextState.name,
				agentOutput: agent_output,
				outcome: outcome as "success" | "failure",
			};

			appendLedger(cwd, workflow_id, entry);
			instance.ledger.push(entry);
			instance.currentState = nextState.name;

			return {
				content: [{ type: "text", text: `Advanced to "${nextState.name}" (${transitionKey})\nAgent for this state: ${nextState.agent || "none (terminal)"}\n\nSCAFFOLD: Dispatch to ${nextState.agent} not yet automated. Call dispatch_agent manually.` }],
				details: { entry, nextState },
			};
		},
	});

	pi.registerTool({
		name: "chronicle_status",
		label: "Chronicle Status",
		description: "Check the current status of a workflow.",
		parameters: Type.Object({
			workflow_id: Type.String({ description: "Workflow ID" }),
		}),
		async execute(_toolCallId, params, _signal, _onUpdate, _ctx) {
			const { workflow_id } = params as any;
			const instance = instances.get(workflow_id);
			if (!instance) {
				return { content: [{ type: "text", text: `Workflow "${workflow_id}" not found.` }] };
			}
			return {
				content: [{ type: "text", text: `Workflow: ${instance.definition.name}\nID: ${instance.workflowId}\nStatus: ${instance.status}\nCurrent state: ${instance.currentState}\nTransitions: ${instance.ledger.length}` }],
			};
		},
	});

	pi.registerTool({
		name: "chronicle_history",
		label: "Chronicle History",
		description: "Show the full ledger of a workflow.",
		parameters: Type.Object({
			workflow_id: Type.String({ description: "Workflow ID" }),
		}),
		async execute(_toolCallId, params, _signal, _onUpdate, _ctx) {
			const { workflow_id } = params as any;
			const instance = instances.get(workflow_id);
			if (!instance) {
				return { content: [{ type: "text", text: `Workflow "${workflow_id}" not found.` }] };
			}
			const lines = instance.ledger.map(e =>
				`[${e.timestamp}] ${e.fromState ?? "START"} → ${e.toState} (${e.outcome}): ${e.agentOutput.slice(0, 80)}`
			).join("\n");
			return { content: [{ type: "text", text: `Ledger for "${instance.definition.name}":\n${lines}` }] };
		},
	});

	pi.registerTool({
		name: "chronicle_list",
		label: "Chronicle List",
		description: "List all active workflows.",
		parameters: Type.Object({}),
		async execute() {
			if (instances.size === 0) {
				return { content: [{ type: "text", text: "No active workflows." }] };
			}
			const list = Array.from(instances.values()).map(inst =>
				`${inst.workflowId}: ${inst.definition.name} [${inst.status}] @ ${inst.currentState}`
			).join("\n");
			return { content: [{ type: "text", text: `Workflows:\n${list}` }] };
		},
	});
}
