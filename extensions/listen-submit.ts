/**
 * Listen Submit — Pi extension for ArhuGula Listen (HTTP job server)
 *
 * Registers tools that let Pi agents submit and monitor jobs on ArhuGula's
 * Listen server (apps/listen/main.py). Pi operates above Layer 4 — it
 * submits prompts to Listen, which spawns Claude Code workers.
 *
 * Environment:
 *   LISTEN_PORT    — Listen server port (default: 8420)
 *   LISTEN_API_KEY — Required API key for X-API-Key header
 *
 * Tools:
 *   listen_submit  — Submit a job to the Listen server
 *   listen_status  — Check status of a specific job
 *   listen_jobs    — List all jobs
 *   listen_stop    — Stop a running job
 *
 * Usage: pi -e extensions/listen-submit.ts
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import { Text } from "@mariozechner/pi-tui";
import { applyExtensionDefaults } from "./themeMap.ts";

// ── Helpers ─────────────────────────────────────────

function getBaseUrl(): string {
	const port = process.env.LISTEN_PORT || "8420";
	return `http://127.0.0.1:${port}`;
}

function getHeaders(): Record<string, string> {
	const headers: Record<string, string> = {
		"Content-Type": "application/json",
	};
	const apiKey = process.env.LISTEN_API_KEY;
	if (apiKey) {
		headers["X-API-Key"] = apiKey;
	}
	return headers;
}

async function listenFetch(
	path: string,
	options: RequestInit = {},
): Promise<{ data: any; error: string | null; status: number }> {
	const url = `${getBaseUrl()}${path}`;
	try {
		const response = await fetch(url, {
			...options,
			headers: { ...getHeaders(), ...((options.headers as Record<string, string>) || {}) },
		});
		const data = await response.json();
		if (!response.ok) {
			return {
				data,
				error: data.error || `HTTP ${response.status}`,
				status: response.status,
			};
		}
		return { data, error: null, status: response.status };
	} catch (err: any) {
		return {
			data: null,
			error: `Connection failed: ${err.message}. Is Listen running? (just listen)`,
			status: 0,
		};
	}
}

// ── Extension ───────────────────────────────────────

export default function (pi: ExtensionAPI) {
	// ── listen_submit tool ──────────────────────────

	pi.registerTool({
		name: "listen_submit",
		label: "Listen Submit",
		description:
			"Submit a job to the ArhuGula Listen server. The server spawns a Claude Code worker to execute the command.",
		parameters: Type.Object({
			command: Type.String({
				description: "Command/prompt for the Listen job server to execute",
			}),
			args: Type.Optional(
				Type.Array(Type.String(), {
					description: "Optional arguments for the command",
				}),
			),
		}),

		async execute(_toolCallId, params, _signal, onUpdate) {
			const { command, args } = params as {
				command: string;
				args?: string[];
			};

			if (onUpdate) {
				onUpdate({
					content: [{ type: "text", text: "Submitting job to Listen..." }],
					details: { command, status: "submitting" },
				});
			}

			const result = await listenFetch("/job", {
				method: "POST",
				body: JSON.stringify({ command, args: args || [] }),
			});

			if (result.error) {
				return {
					content: [{ type: "text", text: `Error: ${result.error}` }],
					details: { command, status: "error", error: result.error },
				};
			}

			const jobId = result.data.id;
			const summary = `Job submitted: ${jobId} (status: ${result.data.status})`;
			return {
				content: [{ type: "text", text: summary }],
				details: {
					jobId,
					command,
					status: result.data.status,
				},
			};
		},

		renderCall(args, theme) {
			const p = args as { command?: string };
			const cmd = p.command || "";
			const preview = cmd.length > 60 ? cmd.slice(0, 57) + "..." : cmd;
			return new Text(
				theme.fg("toolTitle", theme.bold("listen_submit ")) +
					theme.fg("muted", preview),
				0,
				0,
			);
		},

		renderResult(result, options, theme) {
			const details = result.details as any;
			if (!details) {
				const text = result.content[0];
				return new Text(
					text?.type === "text" ? text.text : "",
					0,
					0,
				);
			}

			if (details.status === "submitting") {
				return new Text(
					theme.fg("accent", "● submitting..."),
					0,
					0,
				);
			}

			const icon = details.error ? "✗" : "✓";
			const color = details.error ? "error" : "success";
			const header = theme.fg(color, `${icon} job:${details.jobId || "?"}`);
			return new Text(header, 0, 0);
		},
	});

	// ── listen_status tool ──────────────────────────

	pi.registerTool({
		name: "listen_status",
		label: "Listen Status",
		description: "Check the status of a specific Listen job by ID.",
		parameters: Type.Object({
			job_id: Type.String({ description: "Job ID to check" }),
		}),

		async execute(_toolCallId, params) {
			const { job_id } = params as { job_id: string };
			// Validate job_id to prevent path traversal / header injection
			if (!/^[a-zA-Z0-9_-]+$/.test(job_id)) {
				return { content: [{ type: "text", text: `Error: Invalid job_id format. Must be alphanumeric with hyphens/underscores.` }] };
			}
			const result = await listenFetch(`/job/${encodeURIComponent(job_id)}`);

			if (result.error) {
				return {
					content: [{ type: "text", text: `Error: ${result.error}` }],
				};
			}

			const job = result.data;
			const output = [
				`Job: ${job.id}`,
				`Command: ${job.command}`,
				`Status: ${job.status}`,
				`Created: ${job.created_at}`,
				job.started_at ? `Started: ${job.started_at}` : null,
				job.completed_at ? `Completed: ${job.completed_at}` : null,
				job.exit_code !== null ? `Exit code: ${job.exit_code}` : null,
			]
				.filter(Boolean)
				.join("\n");

			return { content: [{ type: "text", text: output }] };
		},
	});

	// ── listen_jobs tool ────────────────────────────

	pi.registerTool({
		name: "listen_jobs",
		label: "Listen Jobs",
		description: "List all jobs on the ArhuGula Listen server.",
		parameters: Type.Object({}),

		async execute() {
			const result = await listenFetch("/jobs");

			if (result.error) {
				return {
					content: [{ type: "text", text: `Error: ${result.error}` }],
				};
			}

			if (!result.data || result.data.length === 0) {
				return {
					content: [{ type: "text", text: "No jobs found." }],
				};
			}

			const lines = result.data.map(
				(j: any) => `${j.id}  ${j.status.padEnd(10)}  ${j.command}`,
			);
			return {
				content: [{ type: "text", text: lines.join("\n") }],
			};
		},
	});

	// ── listen_stop tool ────────────────────────────

	pi.registerTool({
		name: "listen_stop",
		label: "Listen Stop",
		description: "Stop a running job on the Listen server.",
		parameters: Type.Object({
			job_id: Type.String({ description: "Job ID to stop" }),
		}),

		async execute(_toolCallId, params) {
			const { job_id } = params as { job_id: string };
			// Validate job_id to prevent path traversal / header injection
			if (!/^[a-zA-Z0-9_-]+$/.test(job_id)) {
				return { content: [{ type: "text", text: `Error: Invalid job_id format. Must be alphanumeric with hyphens/underscores.` }] };
			}
			const result = await listenFetch(`/job/${encodeURIComponent(job_id)}`, {
				method: "DELETE",
			});

			if (result.error) {
				return {
					content: [{ type: "text", text: `Error: ${result.error}` }],
				};
			}

			return {
				content: [
					{ type: "text", text: `Stopped job: ${result.data.deleted}` },
				],
			};
		},
	});

	// ── Session Start ───────────────────────────────

	pi.on("session_start", async (_event, ctx) => {
		applyExtensionDefaults(import.meta.url, ctx);
		const port = process.env.LISTEN_PORT || "8420";
		const hasKey = !!process.env.LISTEN_API_KEY;

		ctx.ui.setStatus(
			"listen",
			`📡 Listen: 127.0.0.1:${port}${hasKey ? "" : " (no API key!)"}`,
		);
		ctx.ui.notify(
			`Listen Submit loaded.\n` +
				`Tools: listen_submit, listen_status, listen_jobs, listen_stop\n` +
				`Endpoint: http://127.0.0.1:${port}\n` +
				`API Key: ${hasKey ? "configured" : "NOT SET — set LISTEN_API_KEY"}`,
			hasKey ? "info" : "warning",
		);
	});
}
