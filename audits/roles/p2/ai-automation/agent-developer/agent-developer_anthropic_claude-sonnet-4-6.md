```json
{
  "role": "agent-developer",
  "department": "ai-automation",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 5,
    "anti_pattern_quality": 3,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic agent-development platitudes that could appear in any AI textbook. 'Tool Use Is Power' and 'Fail Gracefully' say nothing specific about how THIS agent developer operates within Story Portal's festival context. 'Safety First' is a universal cliché with no grounding in what safety actually means here. None of the principles reference the offline-first constraint, the audio-centric pipeline, or the child-safety dimension of a storytelling festival.",
      "example_rewrite": "Replace generic principles with role-specific ones: | **Offline-First Resilience** | Every agent must degrade gracefully when festival WiFi drops — local fallback logic is not optional, it is the baseline | **Audio Is the Primary Signal** | Agents in Story Portal receive transcribed speech, not typed text; tool chains start with audio fidelity, not text quality | **Child-Safe Bounds Are Hard Limits** | Content moderation agents must refuse ambiguous cases rather than pass them — false positives are acceptable, false negatives are not | **Trace Before You Ship** | No agent reaches staging without a full ReAct trace log attached to the PR — reasoning must be auditable by a non-engineer | **Tool Contracts Over Tool Cleverness** | A tool with a clear input/output contract and error envelope is worth more than a sophisticated tool with undocumented failure modes | **Human Review Gates Capability Expansion** | Any new agent capability that touches user-facing output requires AI Ethics Specialist sign-off before the tool is added to the library |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoffs name role titles but the artifacts are one-word labels with no format, schema, or content specification. 'Agent requirements' from Product Manager could mean a Slack message or a 50-page spec — the agent receiving this role cannot distinguish. 'Production agents' delivered to AI Operations Engineer has no mention of what container format, health-check endpoint, or runbook is expected. The 'QA' role listed as a recipient does not appear to exist in a typical AI & Automation charter and may be a hallucinated role.",
      "example_rewrite": "Receives From — Product Manager: 'Signed-off Agent Brief (Notion doc) containing: use-case narrative, success criteria with measurable KPIs, safety classification (Green/Amber/Red), and list of approved tool categories. No development begins without a Red-stamped brief countersigned by CAO.' | Delivers To — AI Operations Engineer: 'Packaged agent artifact: Dockerized Python service with /health endpoint, .env.example, runbook.md covering restart procedures and known failure modes, and a behavioral test report showing >95% pass rate on the standard harness. Handoff happens via PR into the ops/agents repo, not Slack.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 3,
      "finding": "There is no dedicated Anti-Patterns section in this role file — it is entirely absent as a named section. The DON'T list in Boundaries functions as a weak proxy but lists domain-boundary violations only ('don't optimize prompts', 'don't build ML models'), not actual failure modes specific to agent development. There is no mention of agent-specific failure patterns like infinite reasoning loops, tool call storms, prompt injection via tool outputs, or over-autonomous production deployments without STOP gates.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: | **Runaway Tool Loop** | Agent calls a tool, gets an ambiguous result, re-calls the same tool in a tighter loop until rate-limited. Mitigation: every tool invocation chain has a max_iterations cap of 5 and a forced STOP with human escalation. | **Trusting Tool Output Blindly** | Agent passes raw tool output directly into the next prompt without validation, opening prompt injection via analytics API responses. Mitigation: all tool outputs pass through a sanitization wrapper before re-entering the reasoning chain. | **Skipping the Safety STOP for 'Small' Changes** | Developer adds a new content classifier flag and ships directly to production because it 'only changes a label.' Mitigation: any change to a safety-critical agent path requires the full Iteration Protocol STOP regardless of change size. | **Monolithic Agent Replacing Workflow** | Developer builds one agent that does moderation + prompt generation + analytics because it is faster. Mitigation: each agent owns exactly one capability domain; cross-domain work is handled by multi-agent orchestration with explicit handoff contracts. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol loop is present and correctly placed, and the classification section clearly separates AI actions from human review gates. The role is loadable and actionable. Minor gaps: the STOP point in Workflow 1 is implicit (buried in the iteration protocol appendix) rather than marked with an explicit STOP label at step 3-4 of each workflow, and the agent capabilities table lists 'Deployment' as an autonomous capability without clarifying that production deployment requires prior human approval — contradicting the iteration protocol.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix names four real agents and four real tools, which is a solid foundation. However, it lacks actionable specificity: the Content Moderator agent has no mention of what audio safety categories it screens for, the 'offline operation' constraint is listed but no implementation guidance is given (local model? cached rules?), and the agent priorities list has no rationale explaining why content moderation outranks support. A developer loading this role mid-sprint cannot make architecture decisions from this appendix alone.",
      "example_rewrite": "Expand the Content Moderator entry: | **Content Moderator** | Screens transcribed story audio for: (1) personal information disclosure (child names, addresses), (2) distressing content (violence, fear themes above age-appropriate threshold), (3) profanity. Operates offline using a locally cached classifier model (max 50MB) loaded at festival startup. Defaults to REJECT on classifier confidence <0.85 — never defaults to PASS. Escalates REJECT decisions to the Festival Moderator role via the support queue, not silently. Target latency: <2s per story submission. |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4-5 agent-specific failure modes (tool loops, prompt injection via tool output, skipped safety gates, monolithic agent creep) — the current DON'T list covers only domain boundaries and leaves the agent with no guidance on the most dangerous technical failure modes it will actually encounter in production."
}
```