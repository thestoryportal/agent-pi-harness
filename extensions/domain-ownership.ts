/**
 * Domain Ownership — Per-agent path boundary enforcement
 *
 * Pillar 4 of the 6-pillar multi-agent orchestration pattern.
 * Reads the `domain:` field from agent frontmatter and enforces
 * path-level read/upsert/delete permissions on tool calls.
 *
 * Agent identity is detected via the DOMAIN_OWNER tag in the system prompt
 * (set by agent-team.ts via --append-system-prompt from the agent .md body).
 *
 * When no DOMAIN_OWNER tag is found (e.g., running in the orchestrator session),
 * enforcement is inactive — the orchestrator has no code tools anyway.
 *
 * Usage: pi -e extensions/domain-ownership.ts
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { isToolCallEventType } from "@mariozechner/pi-coding-agent";
import { parse as yamlParse } from "yaml";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { applyExtensionDefaults } from "./themeMap.ts";

// ── Types ────────────────────────────────────────────────────

interface DomainRule {
	path: string;
	read: boolean;
	upsert: boolean;
	delete: boolean;
}

// ── Path Helpers (adapted from damage-control.ts) ────────────

function resolvePath(p: string, cwd: string): string {
	if (p.startsWith("~")) {
		p = path.join(os.homedir(), p.slice(1));
	}
	return path.resolve(cwd, p);
}

function isPathMatch(targetPath: string, pattern: string, cwd: string): boolean {
	const resolvedPattern = pattern.startsWith("~")
		? path.join(os.homedir(), pattern.slice(1))
		: pattern;

	// Directory match (pattern ends with /)
	if (resolvedPattern.endsWith("/")) {
		const absolutePattern = path.isAbsolute(resolvedPattern)
			? resolvedPattern
			: path.resolve(cwd, resolvedPattern);
		return targetPath.startsWith(absolutePattern);
	}

	// Glob wildcard match
	const regexPattern = resolvedPattern
		.replace(/[.+^${}()|[\]\\]/g, "\\$&")
		.replace(/\*/g, ".*");

	const regex = new RegExp(
		`^${regexPattern}$|^${regexPattern}/|/${regexPattern}$|/${regexPattern}/`,
	);

	const relativePath = path.relative(cwd, targetPath);

	// "." matches everything — it's the project root wildcard
	if (resolvedPattern === ".") {
		return targetPath.startsWith(cwd) || relativePath === "." || !relativePath.startsWith("..");
	}

	return (
		regex.test(targetPath) ||
		regex.test(relativePath) ||
		targetPath.includes(resolvedPattern) ||
		relativePath.includes(resolvedPattern)
	);
}

// ── Extension ────────────────────────────────────────────────

export default function (pi: ExtensionAPI) {
	let agentName = "";
	let domainRules: DomainRule[] = [];
	let enforcementActive = false;

	pi.on("session_start", async (_event, ctx) => {
		applyExtensionDefaults(import.meta.url, ctx);

		// Identify which agent we are via DOMAIN_OWNER tag in system prompt.
		// SECURITY: The tag is parsed from the system prompt which may include
		// user-controlled task text. We validate the extracted name against a
		// strict allowlist pattern AND verify a matching agent file exists.
		const systemPrompt = ctx.getSystemPrompt();
		const match = systemPrompt.match(/DOMAIN_OWNER:\s*(\S+)/);
		if (!match) {
			ctx.ui.notify(
				"Domain-Ownership: No DOMAIN_OWNER tag found — enforcement inactive.\n" +
				"(This is expected for the orchestrator session.)",
			);
			enforcementActive = false;
			return;
		}
		agentName = match[1].trim();

		// S-08/S-06: Validate agent name to prevent path traversal and identity spoofing.
		// Only lowercase letters, digits, and hyphens allowed (matches agent file naming convention).
		if (!/^[a-z][a-z0-9-]*$/.test(agentName)) {
			ctx.ui.notify(
				`Domain-Ownership: Invalid agent name "${agentName}" — must be lowercase alphanumeric with hyphens. Enforcement inactive.`,
				"error",
			);
			enforcementActive = false;
			return;
		}

		// Find this agent's .md file and parse domain: from frontmatter
		const agentsDir = path.join(ctx.cwd, ".pi", "agents");
		const agentFile = path.join(agentsDir, `${agentName}.md`);

		// Belt-and-suspenders: verify resolved path stays inside agents directory
		const resolvedAgentFile = path.resolve(agentFile);
		const resolvedAgentsDir = path.resolve(agentsDir);
		if (!resolvedAgentFile.startsWith(resolvedAgentsDir + path.sep)) {
			ctx.ui.notify(
				`Domain-Ownership: Agent file path escapes agents directory — enforcement inactive.`,
				"error",
			);
			enforcementActive = false;
			return;
		}

		if (!fs.existsSync(agentFile)) {
			ctx.ui.notify(
				`Domain-Ownership: Agent file not found for "${agentName}" — enforcement inactive.`,
				"warning",
			);
			enforcementActive = false;
			return;
		}

		try {
			const raw = fs.readFileSync(agentFile, "utf-8");
			const fmMatch = raw.match(/^---\n([\s\S]*?)\n---/);
			if (!fmMatch) {
				enforcementActive = false;
				return;
			}

			const fm = yamlParse(fmMatch[1]) as any;
			domainRules = (fm.domain || []).map((d: any) => ({
				path: d.path,
				read: d.read ?? true,
				upsert: d.upsert ?? false,
				delete: d.delete ?? false,
			}));

			enforcementActive = domainRules.length > 0;

			if (enforcementActive) {
				const rulesSummary = domainRules
					.map(
						(r) =>
							`  ${r.path}: read=${r.read} upsert=${r.upsert} delete=${r.delete}`,
					)
					.join("\n");
				ctx.ui.setStatus(
					"domain",
					`Domain: ${agentName} (${domainRules.length} rules)`,
				);
				ctx.ui.notify(
					`Domain-Ownership: ${agentName} — ${domainRules.length} rules active\n${rulesSummary}`,
				);
			}
		} catch (err) {
			ctx.ui.notify(
				`Domain-Ownership: Failed to parse domain for "${agentName}": ${err instanceof Error ? err.message : String(err)}`,
				"error",
			);
			enforcementActive = false;
		}
	});

	pi.on("tool_call", async (event, ctx) => {
		if (!enforcementActive) return { block: false };

		// Extract paths from tool call input
		const inputPaths: string[] = [];
		if (
			isToolCallEventType("read", event) ||
			isToolCallEventType("write", event) ||
			isToolCallEventType("edit", event)
		) {
			inputPaths.push(event.input.path);
		} else if (
			isToolCallEventType("grep", event) ||
			isToolCallEventType("find", event) ||
			isToolCallEventType("ls", event)
		) {
			inputPaths.push(event.input.path || ".");
		} else if (isToolCallEventType("bash", event)) {
			// Cannot reliably enforce path restrictions on bash commands
			// Log but allow — damage-control.ts handles bash safety
			return { block: false };
		}

		if (inputPaths.length === 0) return { block: false };

		const isWriteOp =
			isToolCallEventType("write", event) ||
			isToolCallEventType("edit", event);

		for (const p of inputPaths) {
			const resolved = resolvePath(p, ctx.cwd);

			// Check against each domain rule — first matching rule wins
			let allowed = false;
			for (const rule of domainRules) {
				if (isPathMatch(resolved, rule.path, ctx.cwd)) {
					if (isWriteOp && !rule.upsert) {
						ctx.ui.notify(
							`Domain violation: ${agentName} cannot write to ${p}`,
							"error",
						);
						return {
							block: true,
							reason: `Domain violation: ${agentName} cannot write to ${p} — domain rule for "${rule.path}" has upsert: false.\n\nDo NOT attempt to work around this restriction. Report it to the user.`,
						};
					}
					if (!isWriteOp && !rule.read) {
						ctx.ui.notify(
							`Domain violation: ${agentName} cannot read ${p}`,
							"error",
						);
						return {
							block: true,
							reason: `Domain violation: ${agentName} cannot read ${p} — domain rule for "${rule.path}" has read: false.\n\nDo NOT attempt to work around this restriction. Report it to the user.`,
						};
					}
					allowed = true;
					break;
				}
			}

			if (!allowed) {
				ctx.ui.notify(
					`Domain violation: ${agentName} has no access to ${p}`,
					"error",
				);
				return {
					block: true,
					reason: `Domain violation: ${agentName} is not permitted to access ${p} — path not in declared domain.\n\nDo NOT attempt to work around this restriction. Report it to the user.`,
				};
			}
		}

		return { block: false };
	});
}
