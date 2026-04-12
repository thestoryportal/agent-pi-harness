/**
 * Agent IM — Chat Room interface for agent-to-agent coordination
 *
 * Pillar 5 of the 6-pillar multi-agent orchestration pattern.
 * Provides a shared message bus where agents can send messages to each other,
 * check for messages, and coordinate without going through the orchestrator.
 *
 * Current implementation: single-session in-memory bus with JSONL log file.
 * Messages are lost on /new (in-memory only). The JSONL log at
 * .pi/agent-im-log.jsonl provides observability but not cross-process delivery.
 *
 * Full implementation would use: persistent file polling or SQLite for
 * cross-session, cross-process delivery.
 *
 * Commands:
 *   /im-send <agent> <message>  — send a message to an agent
 *   /im-inbox                   — check your messages
 *   /im-clear                   — clear message queue
 *
 * Usage: pi -e extensions/agent-im.ts
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import * as fs from "fs";
import * as path from "path";
import { applyExtensionDefaults } from "./themeMap.ts";

interface AgentMessage {
	id: string;
	from: string;
	to: string;
	content: string;
	timestamp: string;
	read: boolean;
}

export default function (pi: ExtensionAPI) {
	const messageQueue: AgentMessage[] = [];
	let selfName = "unknown";
	const MESSAGE_LOG_PATH = ".pi/agent-im-log.jsonl";

	pi.on("session_start", async (_event, ctx) => {
		applyExtensionDefaults(import.meta.url, ctx);

		// Detect self from system prompt DOMAIN_OWNER tag
		const systemPrompt = ctx.getSystemPrompt();
		const match = systemPrompt.match(/DOMAIN_OWNER:\s*(\S+)/);
		selfName = match ? match[1].trim() : "orchestrator";

		ctx.ui.setStatus("agent-im", `IM: ${selfName}`);
		ctx.ui.notify(
			`Agent IM loaded — identity: ${selfName}\n\n` +
			`/im-send <agent> <message>  Send a message\n` +
			`/im-inbox                   Check incoming messages\n` +
			`/im-clear                   Clear message queue\n\n` +
			`NOTE: Messages are in-memory only in this scaffold. ` +
			`Full implementation requires persistent cross-process bus.`,
			"info",
		);
	});

	// Tool: send_agent_message
	pi.registerTool({
		name: "send_agent_message",
		label: "Send Agent Message",
		description: "Send a message to another agent in the team. The message is queued for delivery.",
		parameters: Type.Object({
			to: Type.String({ description: "Recipient agent name (e.g., 'builder', 'planner')" }),
			content: Type.String({ description: "Message content" }),
		}),
		async execute(_toolCallId, params, _signal, _onUpdate, ctx) {
			const { to, content } = params as { to: string; content: string };
			const msg: AgentMessage = {
				id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
				from: selfName,
				to,
				content,
				timestamp: new Date().toISOString(),
				read: false,
			};
			messageQueue.push(msg);

			// Append to log file for observability (not cross-process delivery)
			try {
				const logPath = path.join(ctx.cwd, MESSAGE_LOG_PATH);
				fs.mkdirSync(path.dirname(logPath), { recursive: true });
				fs.appendFileSync(logPath, JSON.stringify(msg) + "\n");
			} catch {}

			return {
				content: [{ type: "text", text: `Message queued for ${to}: "${content.slice(0, 100)}"` }],
				details: { msg },
			};
		},
	});

	// Tool: check_agent_messages
	pi.registerTool({
		name: "check_agent_messages",
		label: "Check Agent Messages",
		description: "Check messages addressed to you in the agent IM queue.",
		parameters: Type.Object({}),
		async execute(_toolCallId, _params, _signal, _onUpdate, _ctx) {
			const incoming = messageQueue.filter(m => m.to === selfName && !m.read);
			incoming.forEach(m => { m.read = true; });

			if (incoming.length === 0) {
				return { content: [{ type: "text", text: "No new messages." }], details: { messages: [] } };
			}

			const formatted = incoming.map(m =>
				`[${m.timestamp}] FROM ${m.from}: ${m.content}`
			).join("\n\n");

			return {
				content: [{ type: "text", text: `${incoming.length} message(s):\n\n${formatted}` }],
				details: { messages: incoming },
			};
		},
	});

	// Commands
	pi.registerCommand("im-send", {
		description: "Send a message to an agent: /im-send <agent> <message>",
		handler: async (args, ctx) => {
			const trimmed = args?.trim() ?? "";
			const spaceIdx = trimmed.indexOf(" ");
			if (spaceIdx === -1) {
				ctx.ui.notify("Usage: /im-send <agent> <message>", "error");
				return;
			}
			const to = trimmed.slice(0, spaceIdx);
			const content = trimmed.slice(spaceIdx + 1).trim();
			const msg: AgentMessage = {
				id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
				from: selfName,
				to,
				content,
				timestamp: new Date().toISOString(),
				read: false,
			};
			messageQueue.push(msg);
			ctx.ui.notify(`Message sent to ${to}: "${content.slice(0, 60)}"`, "success");
		},
	});

	pi.registerCommand("im-inbox", {
		description: "Check messages addressed to you",
		handler: async (_args, ctx) => {
			const incoming = messageQueue.filter(m => m.to === selfName);
			if (incoming.length === 0) {
				ctx.ui.notify("Inbox empty.", "info");
				return;
			}
			const lines = incoming.map(m =>
				`[${m.read ? "read" : "NEW"}] FROM ${m.from}: ${m.content}`
			).join("\n");
			ctx.ui.notify(`Inbox (${incoming.length}):\n${lines}`, "info");
		},
	});

	pi.registerCommand("im-clear", {
		description: "Clear all messages from the queue",
		handler: async (_args, ctx) => {
			const count = messageQueue.length;
			messageQueue.length = 0;
			ctx.ui.notify(`Cleared ${count} message(s).`, "info");
		},
	});
}
