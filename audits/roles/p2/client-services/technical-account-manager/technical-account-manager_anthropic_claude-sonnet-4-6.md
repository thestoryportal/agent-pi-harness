```json
{
  "role": "technical-account-manager",
  "department": "client-services",
  "scores": {
    "philosophy_depth": 2,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 4,
    "story_portal_relevance": 3
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 2,
      "finding": "All six principles are single-phrase labels with one-line definitions that could apply to any client-facing role. 'Technical Trust: Deep expertise builds credibility' and 'Enable Success: Technical outcomes matter' are indistinguishable from generic sales or CSM platitudes. None of the principles encode TAM-specific decision-making heuristics, trade-off guidance, or behavioral rules. There is no principle that distinguishes a TAM's behavior from an Account Manager, a Solutions Engineer, or a Customer Success Manager.",
      "example_rewrite": "| **Architecture Before Escalation** | Before routing a client issue to Engineering, TAM must first reproduce the problem in a sandbox environment and document the exact call stack, config state, and expected vs. actual behavior. Engineering receives a brief, not a complaint. | | **Roadmap Honesty Over Relationship Comfort** | When a client requests a feature that conflicts with the product roadmap, TAM states the timeline reality directly rather than implying influence they don't have. False hope destroys technical trust faster than bad news. | | **Health Score Transparency** | TAM surfaces declining technical health metrics to the client before they surface them to us. Proactive disclosure of a degrading integration score preserves the trusted-advisor relationship; reactive damage control does not. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoff tables list artifact categories so vague they provide no operational guidance. 'Receives from Account Manager: Strategic accounts' does not specify what document, data structure, or format is transferred. 'Delivers to Product: Client requirements' could mean a Slack message or a 40-page PRD. No handoff names a specific template, ticket type, system of record, or minimum required field. An AI agent or new human hire cannot act on these entries.",
      "example_rewrite": "| Receives From | Artifact | Format | Minimum Content |\n|---|---|---|---|\n| Account Manager | Account Technical Onboarding Brief | Shared doc (account-brief-v[n].md) | Contract tier, named technical contacts, known integration stack, open support tickets |\n| Support | Technical Escalation Record | Zendesk ticket tagged TAM-ESCALATION | Reproduction steps, affected endpoints, client-reported business impact, SLA clock start time |\n| Product | Release Technical Delta | Confluence page linked in #product-releases Slack channel | Changed APIs, deprecated features, migration deadline, breaking-change flag (Y/N) |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "The role contains no dedicated Anti-Patterns section at all. The DON'T list in Boundaries is a boundary ownership list ('don't own business relationship') rather than behavioral failure modes. There are no role-specific anti-patterns describing how a TAM actually fails — e.g., becoming a shadow support engineer, over-promising roadmap influence, letting architecture reviews become rubber stamps, or hiding client technical debt from internal stakeholders. The template checklist explicitly requires this section and it is entirely absent.",
      "example_rewrite": "### Anti-Patterns\n| Anti-Pattern | Why It Happens | Why It's Harmful | Correct Behavior |\n|---|---|---|---|\n| **Becoming Shadow Support** | Client escalates directly; TAM resolves to build goodwill | TAM becomes a ticket queue, relationship depth collapses, Support is bypassed | Log issue in Zendesk, tag TAM-ESCALATION, coordinate resolution without owning the ticket |\n| **Roadmap Promise Creep** | Client pressure + desire to retain trust | Engineering receives undocumented client commitments; trust breaks when features don't ship | Use exact language: 'I will advocate for this in the Q3 planning cycle. I cannot commit to the roadmap.' |\n| **Architecture Review Theater** | Reviews scheduled on cadence without new data | Client perceives reviews as box-checking; TAM misses real architectural drift | Cancel review if no new metrics, incidents, or integration changes since last session; document reason |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Iteration Protocol exists and is structurally correct, but the AI/Human division of labor is stated at the category level only ('AI assists with analysis, AI generates documentation') without specifying triggers, input formats, output formats, or decision thresholds. The Context Requirements section contains literal placeholder text '[Context item 1]' and '[Context item 2]' — a template was shipped unfilled. Required Skills table has no entries. An AI agent loading this role cannot determine what data to ingest, what analysis to run, what document schema to use, or when to escalate versus continue autonomously.",
      "example_rewrite": "### Required Context\n- [ ] account-profile.md — named technical contacts, contract tier, integration stack inventory\n- [ ] technical-health-dashboard.json — current health scores by dimension (uptime, error rate, adoption %)\n- [ ] open-escalations.csv — all active TAM-tagged Zendesk tickets with SLA status\n- [ ] product-release-delta.md — latest release technical changes affecting this account\n\n### AI Task Triggers\n| Trigger | AI Action | Output Format | Human Reviews Before |\n|---|---|---|---|\n| Weekly review cycle opens | Pull health metrics, flag dimensions below threshold (< 85%) | health-summary-[account]-[date].md | Sending to client |\n| Escalation ticket tagged TAM | Draft incident timeline and impact statement | escalation-brief.md | Engaging Engineering |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 3,
      "finding": "The Story Portal appendix names four technical areas (Platform Integration, Audio Processing, Data Flows, Event Infrastructure) but provides no actionable specifics. 'Festival tech connection' and 'Recording quality' are descriptive labels, not TAM guidance. There is no mention of which clients are key accounts in the Story Portal context, what integration patterns are in use, what the known technical risks are for festival deployments, or how TAM interacts with Story Portal's specific roles (e.g., which engineering counterpart owns the audio pipeline). The section would be identical in quality if the project were a fintech SaaS.",
      "example_rewrite": "### Story Portal TAM Context\n| Area | Specific Risk | TAM Action |\n|---|---|---|\n| **Audio Processing Pipeline** | Festival venues have inconsistent upload bandwidth; recordings >2GB frequently timeout at the transcription handoff stage | TAM proactively reviews upload-success-rate.log before each festival weekend; triggers Engineering if error rate exceeds 3% |\n| **On-Site Event Infrastructure** | Clients run Story Portal on event Wi-Fi with no failover; offline capture mode has known sync conflicts after >4 hours disconnected | TAM delivers pre-event infrastructure checklist (event-readiness-checklist.md) 72 hours before festival go-live |\n| **Integration: Client CRM Sync** | Story data flows into client CRMs via webhook; schema mismatches are the #1 TAM escalation source | TAM validates webhook schema compatibility in staging environment before each client platform upgrade |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 TAM-specific behavioral failure modes (e.g., shadow support, roadmap promise creep, architecture review theater). This section is entirely missing — not merely weak — and the template standard explicitly requires it. Its absence means the role provides no guardrails against the most common ways a TAM destroys client trust and internal credibility, making it the single highest-risk gap in the file."
}
```