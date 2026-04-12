/**
 * Agent Forge — Evolutionary runtime tool building
 *
 * Allows the agent to BUILD new Pi tools at runtime by writing TypeScript
 * and storing them in a registry. Forged tools persist across sessions via
 * forge-registry.json.
 *
 * SCAFFOLD STATUS: Types, registration points, and tool stubs defined.
 * Full implementation requires: jiti dynamic loading, TypeBox schema parsing,
 * sandbox execution with stack trace feedback for self-healing.
 *
 * SECURITY WARNING: forge-registry.json stores arbitrary TypeScript source code
 * submitted by LLM agents. DO NOT implement jiti dynamic loading without:
 *   1. Human review gate — forged tools must be approved before execution
 *   2. Cryptographic signing — verify tool source has not been tampered with
 *   3. Sandbox execution — run forged code in an isolated context, not the main Pi process
 * Without these gates, any agent session can pre-position persistent arbitrary code
 * that executes with full Node.js privileges when loading is wired in.
 *
 * Usage: pi -e extensions/agent-forge.ts
 *
 * Tools provided:
 *   forge_tool      — Build a new tool from TypeScript source
 *   forge_list      — List all forged tools in registry
 *   forge_remove    — Remove a forged tool from registry
 *   forge_test      — Test a forged tool with sample input (stub)
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import * as fs from "fs";
import * as path from "path";
import { applyExtensionDefaults } from "./themeMap.ts";

// ── Types ────────────────────────────────────────────────────

interface ForgedTool {
	name: string;
	description: string;
	source: string;       // TypeScript source code of the tool implementation
	schema: object;       // TypeBox schema for parameters
	created: string;
	lastRun: string | null;
	runCount: number;
	lastError: string | null;
}

interface ForgeRegistry {
	version: 1;
	tools: ForgedTool[];
}

// ── Registry I/O ─────────────────────────────────────────────

const REGISTRY_FILE = ".pi/forge-registry.json";

function loadRegistry(cwd: string): ForgeRegistry {
	const registryPath = path.join(cwd, REGISTRY_FILE);
	try {
		if (fs.existsSync(registryPath)) {
			return JSON.parse(fs.readFileSync(registryPath, "utf-8")) as ForgeRegistry;
		}
	} catch {}
	return { version: 1, tools: [] };
}

function saveRegistry(cwd: string, registry: ForgeRegistry): void {
	const registryPath = path.join(cwd, REGISTRY_FILE);
	fs.mkdirSync(path.dirname(registryPath), { recursive: true });
	fs.writeFileSync(registryPath, JSON.stringify(registry, null, 2));
}

// ── Extension ────────────────────────────────────────────────

export default function (pi: ExtensionAPI) {
	let registry: ForgeRegistry = { version: 1, tools: [] };
	let cwd = process.cwd();

	pi.on("session_start", async (_event, ctx) => {
		applyExtensionDefaults(import.meta.url, ctx);
		cwd = ctx.cwd;
		registry = loadRegistry(cwd);
		ctx.ui.setStatus("agent-forge", `Forge: ${registry.tools.length} tools`);
		ctx.ui.notify(
			`Agent Forge loaded — ${registry.tools.length} forged tool(s)\n\n` +
			`forge_tool   — Build a new tool from TypeScript\n` +
			`forge_list   — List forged tools\n` +
			`forge_remove — Remove a forged tool\n` +
			`forge_test   — Test a forged tool\n\n` +
			`SCAFFOLD: Dynamic tool loading via jiti not yet implemented.\n` +
			`Forged tools are stored in ${REGISTRY_FILE} but not auto-registered.\n` +
			`Full implementation: load forged TS via jiti, register with pi.registerTool().`,
			"info",
		);
	});

	pi.registerTool({
		name: "forge_tool",
		label: "Forge Tool",
		description: `Build a new Pi tool at runtime from TypeScript source. The tool is stored in forge-registry.json. SCAFFOLD: Tools are stored but not yet dynamically loaded into Pi. They serve as a registry of evolved capabilities.`,
		parameters: Type.Object({
			name: Type.String({ description: "Tool name (lowercase-with-hyphens)" }),
			description: Type.String({ description: "What this tool does" }),
			source: Type.String({ description: "TypeScript implementation. Must export a default async function(params) returning a string result." }),
			schema_json: Type.String({ description: 'JSON string of the parameter schema, e.g. {"input": {"type": "string"}}' }),
		}),
		async execute(_toolCallId, params, _signal, _onUpdate, _ctx) {
			const { name, description, source, schema_json } = params as any;

			if (!/^[a-z][a-z0-9_-]*$/.test(name)) {
				return { content: [{ type: "text", text: `Error: Tool name must be lowercase with hyphens/underscores. Got: ${name}` }] };
			}

			let schema: object;
			try {
				schema = JSON.parse(schema_json);
			} catch {
				return { content: [{ type: "text", text: "Error: schema_json must be valid JSON" }] };
			}

			const existing = registry.tools.findIndex(t => t.name === name);
			const forgedTool: ForgedTool = {
				name, description, source, schema,
				created: existing >= 0 ? registry.tools[existing].created : new Date().toISOString(),
				lastRun: null,
				runCount: 0,
				lastError: null,
			};

			if (existing >= 0) {
				registry.tools[existing] = forgedTool;
			} else {
				registry.tools.push(forgedTool);
			}

			saveRegistry(cwd, registry);

			return {
				content: [{ type: "text", text: `Forged tool "${name}" saved to registry. ${existing >= 0 ? "Updated." : "New tool."}\n\nSCAFFOLD NOTE: Dynamic loading not yet implemented. Tool stored for future use.` }],
				details: { tool: forgedTool },
			};
		},
	});

	pi.registerTool({
		name: "forge_list",
		label: "Forge List",
		description: "List all forged tools in the registry.",
		parameters: Type.Object({}),
		async execute() {
			if (registry.tools.length === 0) {
				return { content: [{ type: "text", text: "No forged tools in registry." }] };
			}
			const list = registry.tools.map(t =>
				`${t.name}: ${t.description} (runs: ${t.runCount}, last error: ${t.lastError ? "yes" : "none"})`
			).join("\n");
			return { content: [{ type: "text", text: `Forged tools:\n${list}` }] };
		},
	});

	pi.registerTool({
		name: "forge_remove",
		label: "Forge Remove",
		description: "Remove a forged tool from the registry.",
		parameters: Type.Object({
			name: Type.String({ description: "Name of the tool to remove" }),
		}),
		async execute(_toolCallId, params, _signal, _onUpdate, _ctx) {
			const { name } = params as any;
			const idx = registry.tools.findIndex(t => t.name === name);
			if (idx === -1) {
				return { content: [{ type: "text", text: `Tool "${name}" not found in registry.` }] };
			}
			registry.tools.splice(idx, 1);
			saveRegistry(cwd, registry);
			return { content: [{ type: "text", text: `Tool "${name}" removed from registry.` }] };
		},
	});

	pi.registerTool({
		name: "forge_test",
		label: "Forge Test",
		description: "SCAFFOLD: Test stub — returns the stored source for review. Full implementation executes via jiti with stack trace feedback.",
		parameters: Type.Object({
			name: Type.String({ description: "Name of the forged tool to test" }),
			input_json: Type.String({ description: "JSON input parameters for the tool" }),
		}),
		async execute(_toolCallId, params, _signal, _onUpdate, _ctx) {
			const { name } = params as any;
			const tool = registry.tools.find(t => t.name === name);
			if (!tool) {
				return { content: [{ type: "text", text: `Tool "${name}" not found.` }] };
			}
			return {
				content: [{ type: "text", text: `SCAFFOLD: forge_test not yet implemented (jiti dynamic loading required).\n\nStored source for "${name}":\n\`\`\`typescript\n${tool.source}\n\`\`\`` }],
			};
		},
	});
}
