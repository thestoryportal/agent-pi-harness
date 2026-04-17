/**
 * Listen Submit — Pi extension for ArhuGula Listen (HTTP job server)
 *
 * Registers tools that let Pi agents submit and monitor jobs on ArhuGula's
 * Listen server (apps/listen/main.py). Pi operates above Layer 4 — it
 * submits prompts to Listen, which spawns Claude Code workers.
 *
 * Post-SP8-r1 interface:
 *   - Port 7600 (was 8420 pre-revert)
 *   - No auth middleware — upstream mac-mini-agent has none
 *   - POST /job body shape: {"prompt": string}
 *   - GET /job/{id} + GET /jobs return YAML text (PlainTextResponse), not JSON
 *   - POST /jobs/clear archives all active jobs
 *   - DELETE /job/{id} stops a running job
 *
 * Environment:
 *   LISTEN_PORT — override default 7600 (optional)
 *
 * Tools:
 *   listen_submit  — Submit a prompt to the Listen server
 *   listen_status  — Fetch a job's YAML state by ID
 *   listen_jobs    — List all jobs (active or archived)
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
	const port = process.env.LISTEN_PORT || "7600";
	return `http://127.0.0.1:${port}`;
}

async function listenFetchJson(
	path: string,
	options: RequestInit = {},
): Promise<{ data: any; error: string | null; status: number }> {
	const url = `${getBaseUrl()}${path}`;
	try {
		const response = await fetch(url, {
			...options,
			headers: {
				"Content-Type": "application/json",
				...((options.headers as Record<string, string>) || {}),
			},
		});
		const text = await response.text();
		let data: any;
		try {
			data = text ? JSON.parse(text) : null;
		} catch {
			data = text;
		}
		if (!response.ok) {
			const errMsg =
				typeof data === "object" && data?.detail
					? data.detail
					: `HTTP ${response.status}`;
			return { data, error: errMsg, status: response.status };
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

async function listenFetchText(
	path: string,
	options: RequestInit = {},
): Promise<{ text: string; error: string | null; status: number }> {
	const url = `${getBaseUrl()}${path}`;
	try {
		const response = await fetch(url, {
			...options,
			headers: {
				...((options.headers as Record<string, string>) || {}),
			},
		});
		const text = await response.text();
		if (!response.ok) {
			return { text, error: `HTTP ${response.status}`, status: response.status };
		}
		return { text, error: null, status: response.status };
	} catch (err: any) {
		return {
			text: "",
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
			"Submit a prompt to the ArhuGula Listen server. The server spawns a Claude Code worker in a headed Terminal window to execute it.",
		parameters: Type.Object({
			prompt: Type.String({
				description: "Prompt for the Listen job server to execute",
			}),
		}),

		async execute(_toolCallId, params, _signal, onUpdate) {
			const { prompt } = params as { prompt: string };

			if (onUpdate) {
				onUpdate({
					content: [{ type: "text", text: "Submitting job to Listen..." }],
					details: { prompt, status: "submitting" },
				});
			}

			const result = await listenFetchJson("/job", {
				method: "POST",
				body: JSON.stringify({ prompt }),
			});

			if (result.error) {
				return {
					content: [{ type: "text", text: `Error: ${result.error}` }],
					details: { prompt, status: "error", error: result.error },
				};
			}

			const jobId = result.data.job_id;
			const summary = `Job submitted: ${jobId} (status: ${result.data.status})`;
			return {
				content: [{ type: "text", text: summary }],
				details: {
					jobId,
					prompt,
					status: result.data.status,
				},
			};
		},

		renderCall(args, theme) {
			const p = args as { prompt?: string };
			const prompt = p.prompt || "";
			const preview = prompt.length > 60 ? prompt.slice(0, 57) + "..." : prompt;
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
		description:
			"Fetch a Listen job's YAML state by ID (includes prompt, status, updates, summary).",
		parameters: Type.Object({
			job_id: Type.String({ description: "Job ID to check" }),
		}),

		async execute(_toolCallId, params) {
			const { job_id } = params as { job_id: string };
			// Validate job_id to prevent path traversal / header injection
			if (!/^[a-zA-Z0-9_-]+$/.test(job_id)) {
				return {
					content: [
						{
							type: "text",
							text: `Error: Invalid job_id format. Must be alphanumeric with hyphens/underscores.`,
						},
					],
				};
			}
			const result = await listenFetchText(`/job/${encodeURIComponent(job_id)}`);

			if (result.error) {
				return {
					content: [{ type: "text", text: `Error: ${result.error}` }],
				};
			}

			return { content: [{ type: "text", text: result.text.trim() }] };
		},
	});

	// ── listen_jobs tool ────────────────────────────

	pi.registerTool({
		name: "listen_jobs",
		label: "Listen Jobs",
		description: "List jobs on the ArhuGula Listen server (active by default; pass archived=true for archived).",
		parameters: Type.Object({
			archived: Type.Optional(
				Type.Boolean({ description: "List archived jobs instead of active (default false)" }),
			),
		}),

		async execute(_toolCallId, params) {
			const { archived } = params as { archived?: boolean };
			const path = archived ? "/jobs?archived=true" : "/jobs";
			const result = await listenFetchText(path);

			if (result.error) {
				return {
					content: [{ type: "text", text: `Error: ${result.error}` }],
				};
			}

			return { content: [{ type: "text", text: result.text.trim() }] };
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
				return {
					content: [
						{
							type: "text",
							text: `Error: Invalid job_id format. Must be alphanumeric with hyphens/underscores.`,
						},
					],
				};
			}
			const result = await listenFetchJson(`/job/${encodeURIComponent(job_id)}`, {
				method: "DELETE",
			});

			if (result.error) {
				return {
					content: [{ type: "text", text: `Error: ${result.error}` }],
				};
			}

			const stoppedId = result.data?.job_id || job_id;
			return {
				content: [
					{ type: "text", text: `Stopped job: ${stoppedId}` },
				],
			};
		},
	});

	// ── Session Start ───────────────────────────────

	pi.on("session_start", async (_event, ctx) => {
		applyExtensionDefaults(import.meta.url, ctx);
		const port = process.env.LISTEN_PORT || "7600";

		ctx.ui.setStatus(
			"listen",
			`📡 Listen: 127.0.0.1:${port}`,
		);
		ctx.ui.notify(
			`Listen Submit loaded.\n` +
				`Tools: listen_submit, listen_status, listen_jobs, listen_stop\n` +
				`Endpoint: http://127.0.0.1:${port}\n` +
				`Auth: none (upstream mac-mini-agent has no middleware)`,
			"info",
		);
	});
}
