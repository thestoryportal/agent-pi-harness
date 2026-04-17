```json
{
  "role": "head-of-support",
  "department": "support",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 3,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic support platitudes that could appear in any customer service job description from 2005. 'Empathy First', 'Fast Resolution', and 'Continuous Learning' carry zero role-specific signal. None reference Story Portal's unique context: emotionally sensitive oral history content, festival surge conditions, or the distinction between technical audio troubleshooting and community grief/memory support. 'User Success Is Our Success' is circular and meaningless as written.",
      "example_rewrite": "Replace generic principles with role-specific ones. Example: 'Emotional Content Protocol — Story Portal users share grief, memory, and identity; every support interaction must be treated as emotionally loaded by default, not escalated only when a user signals distress.' Or: 'Festival-First Resourcing — On-site festival support is a live, irreversible moment; staffing, tooling, and escalation paths must be pre-staged before each event, not reactive.' Or: 'Audio Fidelity Is The Product — A lost or corrupted recording is not a ticket; it is a permanent loss of a user's story. Recording troubleshooting must have a dedicated escalation path with Engineering SLAs measured in minutes, not days.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs name roles but not actual artifacts with enough specificity to be actionable. 'User feedback' delivered to Product could mean anything from a Slack message to a quarterly report. 'Bug reports' to Engineering has no format, severity taxonomy, or SLA attached. 'Support requests' received from Users is not a handoff — it is a job description. No handoff specifies the medium, template, cadence, or triggering condition. The template standard explicitly requires 'what artifact is passed, not just works with' — this section fails that test on every row.",
      "example_rewrite": "Receives From Engineering: 'Resolved-Issue Notification — structured JSON or Zendesk webhook containing ticket ID, root cause summary, and recommended KB update trigger, delivered within 2 hours of issue closure.' Delivers To Product: 'Weekly User Friction Report — Notion page using the Support Feedback Template, filed every Monday by 10am, containing top 5 recurring issue patterns, verbatim user quotes, and a severity × frequency matrix, tagged to relevant product areas.' Delivers To COO: 'Monthly Support Health Dashboard — Looker report link plus executive summary doc, covering CSAT, FCR, ticket volume by category, and one escalation case study.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file. The template standard explicitly requires 3-5 role-specific anti-patterns. The DO/DON'T boundary list in Core Identity partially substitutes but lists domain boundaries (do not fix bugs, do not set roadmap), which are ownership rules, not behavioral failure modes. No anti-pattern addresses how a Head of Support specifically fails — over-indexing on CSAT scores at the expense of root cause elimination, absorbing Engineering's bug backlog into support workarounds, or treating festival surge as a surprise rather than a planned event.",
      "example_rewrite": "Add a dedicated Anti-Patterns section with entries such as: 'CSAT Vanity — Optimizing for satisfaction scores by over-apologizing and over-compensating users without fixing the underlying product issue. Symptom: CSAT is high but the same ticket category appears in the top 5 every week for three months.' Or: 'Workaround Accumulation — Writing KB articles and support scripts to route around a broken product feature instead of escalating a fix request to Engineering. This hides product debt behind support labor.' Or: 'Festival Reactivity — Treating on-site festival support as a normal queue instead of a pre-planned surge operation with dedicated staff, offline-capable tools, and a 15-minute escalation SLA to Engineering.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 3,
      "finding": "The Deployment Notes section lists what AI handles (ticket routing, knowledge suggestions, pattern analysis, report generation) but provides no actionable instruction for how an AI agent would actually operate in this role. There is no iteration protocol despite the role being classified as Hybrid, which the template standard explicitly requires. The Context Requirements section is completely unfilled — placeholder brackets '[Context item 1]' and '[Context item 2]' were left in. Required Skills has no entries. An AI agent loading this role has no context files to load, no decision rules for ticket routing, no threshold for when to escalate versus self-serve, and no iteration loop.",
      "example_rewrite": "Fill Context Requirements: 'Required Context: [ ] story-portal-product-overview.md — load to understand platform features and known issue taxonomy. [ ] support-escalation-matrix.md — load before handling any ticket rated Severity 2 or above. [ ] festival-support-runbook.md — load 72 hours before any scheduled festival event.' Add Iteration Protocol: 'AI Support Agent Cycle — For each shift: (1) Pull open ticket queue from Zendesk. (2) Classify by issue type using the Support Taxonomy doc. (3) Auto-route Tier 1 issues to KB suggestion flow. (4) Flag Tier 2+ for human review with a one-sentence severity rationale. (5) STOP — human Head of Support reviews flagged tickets before AI responds. (6) After resolution, trigger KB gap check: if no article matches the issue, draft a KB stub and route to Knowledge Manager for review.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies the right support domains (Platform, Festival, Recording, Community) and correctly prioritizes festival on-site support as Priority 1. However, the considerations column is too thin to be actionable. 'Surge support during events' does not tell the team what surge means — no ticket volume multiplier, no staffing ratio, no tool requirement. 'Emotional content — empathetic handling' is a platitude with no protocol. The appendix does not address Story Portal's most distinctive support challenge: a user whose recording is lost or corrupted has lost something irreplaceable, which requires a response protocol that is fundamentally different from standard SaaS support.",
      "example_rewrite": "Expand the Story Portal Support Considerations table with operational specifics. Example row: 'Lost or corrupted recording | Immediate escalation to Engineering within 15 minutes regardless of queue depth; Head of Support personally contacts user within 1 hour; standard CSAT process suspended and replaced with recovery-focused follow-up at 24h and 7d post-incident.' Add a Festival Surge Protocol subsection: 'During festival events, support team operates in War Room mode: dedicated Slack channel #festival-support-live, ticket SLA reduced from 4h to 30 minutes, Engineering on-call engineer assigned to support bridge, Head of Support holds 30-minute syncs every 2 hours.' Add a note on community moderation distinguishing grief-related content from policy violations, since these require different response tracks.'"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section — this is the only dimension scoring below 3 because the section does not exist at all. Every other low-scoring dimension has partial content that can be improved; anti-patterns require creation from scratch. A Head of Support without documented failure modes (CSAT vanity, workaround accumulation, festival reactivity) will systematically make those errors because the role file provides no behavioral guardrails against them. Draft 3-5 role-specific anti-patterns before any other revision."
}
```