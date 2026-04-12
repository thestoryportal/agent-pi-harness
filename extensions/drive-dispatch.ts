/**
 * Drive Dispatch — Pi extension for ArhuGula Drive (tmux terminal control)
 *
 * Registers tools that let Pi agents control tmux sessions via ArhuGula's
 * Drive CLI (apps/drive/main.py). Pi operates above Layer 4 — it dispatches
 * terminal work to Drive, which manages tmux sessions.
 *
 * Tools:
 *   drive_session  — Create, list, or kill tmux sessions
 *   drive_run      — Execute a command in a tmux session (Sentinel-wrapped)
 *   drive_send     — Send raw text to a session (no Sentinel)
 *   drive_logs     — Tail output from a session
 *   drive_poll     — Poll a session for Sentinel completion
 *
 * Usage: pi -e extensions/drive-dispatch.ts
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import { Text } from "@mariozechner/pi-tui";
import { spawn } from "child_process";
import { applyExtensionDefaults } from "./themeMap.ts";

// ── Helpers ─────────────────────────────────────────

function runDrive(
	args: string[],
	cwd: string,
): Promise<{ stdout: string; stderr: string; exitCode: number }> {
	return new Promise((resolve) => {
		const proc = spawn("uv", ["run", "apps/drive/main.py", ...args], {
			cwd,
			stdio: ["ignore", "pipe", "pipe"],
			env: { ...process.env },
		});

		const stdout: string[] = [];
		const stderr: string[] = [];

		proc.stdout!.setEncoding("utf-8");
		proc.stdout!.on("data", (chunk: string) => stdout.push(chunk));
		proc.stderr!.setEncoding("utf-8");
		proc.stderr!.on("data", (chunk: string) => stderr.push(chunk));

		proc.on("close", (code) => {
			resolve({
				stdout: stdout.join(""),
				stderr: stderr.join(""),
				exitCode: code ?? 1,
			});
		});

		proc.on("error", (err) => {
			resolve({
				stdout: "",
				stderr: `Error spawning drive: ${err.message}`,
				exitCode: 1,
			});
		});
	});
}

// ── Extension ───────────────────────────────────────

export default function (pi: ExtensionAPI) {
	let projectDir = "";

	// ── drive_session tool ──────────────────────────

	pi.registerTool({
		name: "drive_session",
		label: "Drive Session",
		description:
			"Manage tmux sessions via ArhuGula Drive. Actions: create (requires name), list, kill (requires name).",
		parameters: Type.Object({
			action: Type.String({ description: "create | list | kill" }),
			name: Type.Optional(
				Type.String({ description: "Session name (required for create/kill)" }),
			),
		}),

		async execute(_toolCallId, params) {
			const { action, name } = params as { action: string; name?: string };

			if ((action === "create" || action === "kill") && !name) {
				return {
					content: [
						{ type: "text", text: `Error: '${action}' requires a session name` },
					],
				};
			}

			let args: string[];
			switch (action) {
				case "create":
					args = ["session", "create", "--name", name!];
					break;
				case "list":
					args = ["session", "list"];
					break;
				case "kill":
					args = ["session", "kill", "--name", name!];
					break;
				default:
					return {
						content: [
							{
								type: "text",
								text: `Unknown action: ${action}. Use create, list, or kill.`,
							},
						],
					};
			}

			const result = await runDrive(args, projectDir);
			const output = result.stdout || result.stderr || "(no output)";
			return { content: [{ type: "text", text: output.trim() }] };
		},

		renderCall(args, theme) {
			const p = args as { action?: string; name?: string };
			return new Text(
				theme.fg("toolTitle", theme.bold("drive_session ")) +
					theme.fg("accent", p.action || "?") +
					(p.name ? theme.fg("dim", ` ${p.name}`) : ""),
				0,
				0,
			);
		},
	});

	// ── drive_run tool ──────────────────────────────

	pi.registerTool({
		name: "drive_run",
		label: "Drive Run",
		description:
			"Execute a command in a tmux session with Sentinel wrapping for reliable completion detection. Returns a JSON token for polling.",
		parameters: Type.Object({
			session: Type.String({ description: "Target tmux session name" }),
			command: Type.String({ description: "Command to execute" }),
		}),

		async execute(_toolCallId, params) {
			const { session, command } = params as {
				session: string;
				command: string;
			};
			const result = await runDrive(
				["run", "--session", session, command],
				projectDir,
			);
			const output = result.stdout || result.stderr || "(no output)";
			return { content: [{ type: "text", text: output.trim() }] };
		},

		renderCall(args, theme) {
			const p = args as { session?: string; command?: string };
			const cmd = p.command || "";
			const preview = cmd.length > 50 ? cmd.slice(0, 47) + "..." : cmd;
			return new Text(
				theme.fg("toolTitle", theme.bold("drive_run ")) +
					theme.fg("accent", p.session || "?") +
					theme.fg("dim", " — ") +
					theme.fg("muted", preview),
				0,
				0,
			);
		},
	});

	// ── drive_send tool ─────────────────────────────

	pi.registerTool({
		name: "drive_send",
		label: "Drive Send",
		description: "Send raw text to a tmux session (no Sentinel wrapping).",
		parameters: Type.Object({
			session: Type.String({ description: "Target tmux session name" }),
			text: Type.String({ description: "Text to send" }),
		}),

		async execute(_toolCallId, params) {
			const { session, text } = params as { session: string; text: string };
			const result = await runDrive(
				["send", "--session", session, text],
				projectDir,
			);
			const output = result.stdout || result.stderr || "(no output)";
			return { content: [{ type: "text", text: output.trim() }] };
		},
	});

	// ── drive_logs tool ─────────────────────────────

	pi.registerTool({
		name: "drive_logs",
		label: "Drive Logs",
		description: "Tail output from a tmux session.",
		parameters: Type.Object({
			session: Type.String({ description: "Target tmux session name" }),
			lines: Type.Optional(
				Type.Number({ description: "Number of lines (default 50)" }),
			),
		}),

		async execute(_toolCallId, params) {
			const { session, lines } = params as {
				session: string;
				lines?: number;
			};
			const args = ["logs", "--session", session];
			if (lines) args.push("--lines", String(lines));
			const result = await runDrive(args, projectDir);
			const output = result.stdout || result.stderr || "(no output)";
			return { content: [{ type: "text", text: output.trim() }] };
		},
	});

	// ── drive_poll tool ─────────────────────��───────

	pi.registerTool({
		name: "drive_poll",
		label: "Drive Poll",
		description: "Poll all sessions with active tokens for Sentinel completion.",
		parameters: Type.Object({}),

		async execute() {
			const result = await runDrive(["poll"], projectDir);
			const output = result.stdout || result.stderr || "(no output)";
			return { content: [{ type: "text", text: output.trim() }] };
		},
	});

	// ── Session Start ───────────────────────────────

	pi.on("session_start", async (_event, ctx) => {
		applyExtensionDefaults(import.meta.url, ctx);
		projectDir = ctx.cwd;
		ctx.ui.setStatus(
			"drive",
			"🚗 Drive: tmux dispatch active",
		);
		ctx.ui.notify(
			"Drive Dispatch loaded.\n" +
				"Tools: drive_session, drive_run, drive_send, drive_logs, drive_poll\n" +
				"Backend: uv run apps/drive/main.py",
			"info",
		);
	});
}
