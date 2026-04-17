```json
{
  "role": "operations-coordinator",
  "department": "management",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 4,
    "anti_pattern_quality": 4,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "All 6 principles are generic operational platitudes that could apply to any coordinator role in any industry. 'Document Everything', 'Single Source of Truth', and 'Automate the Mundane' appear verbatim in dozens of generic ops templates. None are specific to an AI-native organization, multi-agent coordination, or the Story Portal context. There is no principle addressing the unique challenge of coordinating between AI agents and humans, managing role handoff artifacts, or maintaining context across sessions — the actual hard problems this role faces.",
      "example_rewrite": "| **Context Continuity** | Session handoffs are where AI workflows die. Every operation must produce a artifact that lets the next agent — or human — resume without debriefing. A task that exists only in chat history is a task that will be repeated or lost. | | **Right-Sized Documentation** | A 40-page process doc for a 3-step workflow creates its own friction. Match documentation depth to process complexity and change frequency — CLAUDE.md gets a paragraph, deployment guides get a full spec. | | **Agent-Readable Structure** | Documents exist for two audiences: humans skimming for context and AI agents parsing for instructions. Every doc must satisfy both — headers that index, examples that disambiguate, and explicit scope boundaries that prevent an agent from over-reading authority it wasn't granted. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "The handoff tables are the weakest section in the file. 'Receives From: All Roles — Artifact: Documentation updates, resource requests' is not a handoff specification — it is a category description. No handoff names a concrete file, a specific schema, or a defined state that triggers the handoff. 'Delivers To: All Roles — Artifact: Updated docs, resources, templates' tells an AI agent nothing about what file to write, where to put it, or what format to use. The Project Orchestrator handoff lacks the artifact name entirely — 'Priority guidance, strategic direction' is a conversation, not an artifact. The Technical Coordinator handoff references 'Technical specs for documentation' without specifying which specs or where they live.",
      "example_rewrite": "| Receives From | Artifact | Location | Trigger |\n|---|---|---|---|\n| **Technical Coordinator** | `technical-spec-[feature].md` draft | `docs/references/` | Feature branch opened |\n| **Project Orchestrator** | `sprint-priorities.md` update | `docs/status/` | Sprint planning session |\n| **Any Role** | Resource request via `resource-request-template.md` | `docs/requests/` | Submitted to #ops channel |\n\n| Delivers To | Artifact | Location | SLA |\n|---|---|---|---|\n| **Project Orchestrator** | `ops-status-[YYYY-WW].md` | `docs/status/` | Every Monday 9am |\n| **New Team Members** | `onboarding-checklist-[name].md` | `docs/onboarding/` | Before day 1 |\n| **Technical Coordinator** | Updated `DEVELOPMENT_GUIDE.md` | `docs/` | Within 48h of spec receipt |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 4,
      "finding": "All four anti-patterns are universal project management warnings that appear in entry-level PM courses. 'Let docs go stale', 'Hoard information', 'Over-process everything', and 'Ignore small requests' have zero specificity to an AI-native operations role. They do not address the failure modes unique to this context: an AI agent over-documenting AI-generated content that no human will read, treating every role file as requiring an update when a new agent is deployed, silently updating docs without versioning so agents on previous context windows operate on stale canonical files, or creating process templates so generic they get ignored in favor of ad-hoc behavior.",
      "example_rewrite": "| Don't | Why | Instead |\n|---|---|---|\n| Auto-update docs after every AI session | Creates version noise that drowns signal; agents on cached context diverge from 'current' | Version-gate updates — only commit doc changes that reflect a decision or state change, not a conversation |\n| Create process templates without an owner | Orphaned templates get used once, drift from reality, and mislead the next agent that loads them as authoritative | Every template must have a named owner role in its header and a review date — if no owner exists, don't create the template |\n| Treat 'document everything' as backup for unclear roles | Over-documentation is a symptom of unclear authority, not a solution to it — escalate boundary disputes rather than documenting around them | When documenting a process that touches two roles, STOP and confirm ownership before writing; ambiguous docs are worse than no docs |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol is present and correctly placed for a Hybrid role. The DO/DON'T/ESCALATE boundaries are clear enough for an agent to self-check. The Required Skills table with specific filenames is a genuine strength. Score is held at 7 because the STOP points in workflows are inconsistently placed — Workflow 1 has a STOP only at step 5 (after publishing, which is too late for approval), Workflow 2 has no STOP before procurement initiation (a cost-incurring action), and the Required Skills list includes `code-review-checklist.md` with no explanation of why an Operations Coordinator needs a code review checklist, which will cause an agent to either load irrelevant context or question its own scope.",
      "example_rewrite": "In Workflow 2, add: '3a. STOP → If new resource requires cost approval: present options, estimated cost, and justification to human approver. DO NOT initiate procurement without explicit approval. Resume only on written confirmation.' Also remove `code-review-checklist.md` from Required Skills or replace with a context note: '`process-compliance-checklist.md` — for verifying workflow adherence during audits (NOT for reviewing code; escalate code questions to Technical Coordinator).'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix correctly identifies the actual file paths (`docs/`, `~/.claude/skills/`, etc.) and names real files like `APP_SPECIFICATION.md` and `DEVELOPMENT_GUIDE.md`, which is meaningfully better than generic placeholders. However, the 'Key Priorities' section lists four items that restate the role definition rather than providing Story Portal-specific operational guidance. There is no mention of session handoff files (the `sessions/` directory is listed in the tree but never explained), no guidance on when to update `CLAUDE.md` versus role files, and no protocol for handling the specific problem of skill/role version drift — which is the most operationally critical issue for this role in this project.",
      "example_rewrite": "### Session Handoff Protocol\nThe `docs/sessions/` directory is the continuity layer for multi-session work. After any session that produces decisions, changes, or open items:\n1. Write `docs/sessions/session-[YYYY-MM-DD]-[topic].md` using the session handoff template\n2. Update `docs/status/CURRENT_STATE.md` if project state changed\n3. If a role or skill file was modified, bump its version in Document Control and post to #ops\n\n### CLAUDE.md Update Triggers\nOnly update `~/.claude/CLAUDE.md` when: (a) a new role is added to the charter, (b) a deployment pattern changes, or (c) a cross-role boundary is formally redefined. Do NOT update it to reflect session-level decisions — that belongs in `docs/sessions/`."
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. An AI agent loading this role cannot determine what file to produce, where to put it, or what state must exist before handing off — meaning every inter-role transition requires a human to bridge the gap that the role file should have closed. Rewriting the handoff tables with concrete artifact names, file paths, and trigger conditions would immediately reduce coordination overhead and make the Hybrid iteration loop functional without constant clarification prompts."
}
```