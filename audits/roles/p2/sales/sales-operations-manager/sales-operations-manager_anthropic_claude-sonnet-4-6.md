```json
{
  "role": "sales-operations-manager",
  "department": "sales",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are generic sales ops platitudes that could apply to any operations role in any industry. 'Data Drives Decisions,' 'Continuous Improvement,' and 'Simplicity Wins' are textbook buzzwords with zero operational specificity. There is no principle that reflects the unique tension this role navigates — serving sellers without becoming a bottleneck, maintaining data discipline in a high-velocity environment, or balancing CRM rigor against rep adoption resistance.",
      "example_rewrite": "| **Rep Time Is Sacred** | Every process added must demonstrably reduce rep administrative burden, not just satisfy leadership reporting needs — if it costs reps time, it must return more time elsewhere | | **Adoption Over Architecture** | A perfect process no one follows is worse than a flawed process everyone uses — measure process health by field adoption rate, not design elegance | | **Single Source of Truth** | All revenue data resolves to CRM; when dashboards conflict with gut feel, CRM wins — credibility of analytics depends on zero-exception data discipline |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but deliver vague artifact labels. 'Strategic direction' from CRO is not an artifact — it is a conversation. 'Process and tools' delivered to Sales Team is meaningless. 'Lead data' from Marketing Ops does not specify format, cadence, or quality threshold. No handoff specifies file format, delivery frequency, or what triggers the handoff. The Deal Desk Analyst and Proposal Writer appear in Works With but never appear in handoff tables, making those relationships decorative.",
      "example_rewrite": "| Receives From | Artifact | Format | Cadence | Trigger | | Marketing Ops | Qualified lead export with UTM source, lead score, and MQL date | CSV synced to CRM via Zapier integration | Weekly, Monday 8am | MQL threshold crossed | | CRO | Quota guidance memo with FY targets by segment and rep | PDF + CRM goal field update | Annually, Q4 planning cycle | Board approval of revenue plan | | Delivers To | Artifact | Format | Cadence | | CRO | Pipeline health report with stage conversion rates, velocity, and forecast vs. actuals | Tableau dashboard + PDF summary | Weekly, Friday 3pm |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "This role file contains no Anti-Patterns section whatsoever. The template standard requires 3-5 role-specific anti-patterns, and this section is entirely absent. The DO/DON'T boundary table partially substitutes but only addresses ownership disputes, not behavioral failure modes. There is no guidance on what this role characteristically does wrong — such as over-engineering processes, building dashboards nobody reads, or making CRM so complex that data quality collapses.",
      "example_rewrite": "### Anti-Patterns to Avoid | Anti-Pattern | What It Looks Like | Why It Fails | | **Dashboard Proliferation** | Building a new report for every leadership request until no one knows which numbers are authoritative | Destroys single-source-of-truth credibility; leadership stops trusting data | | **Process Theater** | Designing elaborate multi-stage workflows in CRM that reps route around via spreadsheet or Slack | Zero adoption means zero data quality; ops looks busy while pipeline goes dark | | **Analysis Paralysis on Territory Design** | Running 12 scenario models without publishing a territory plan because the data is never clean enough | Reps operate without clarity; Q1 pipeline suffers while ops perfects the model | | **Tool Sprawl Justification** | Adding point solutions to the stack to solve problems that better CRM configuration would fix | Integration debt compounds; data fragmentation worsens the problem ops was hired to solve |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The iteration protocol exists and is structurally sound, but the Context Requirements section is left as unfilled placeholders ('[Context item 1]', '[Context item 2]', '[Use placeholder format: skill-name.md]'). This means an AI agent loading this role has no idea what context files to pull, what CRM credentials or data sources to expect, or what prior artifacts define the current operational state. The STOP points in workflows do not specify who reviews or what approval looks like. An AI agent could begin work but would immediately stall on first context request.",
      "example_rewrite": "### Required Context | Context Item | Why Required | | Current CRM configuration export (fields, stages, workflows) | AI must understand existing data model before suggesting process changes | | Active territory and quota plan (current fiscal year) | Required for attainment analysis and reallocation recommendations | | Last 3 pipeline health reports | Establishes trend baseline for anomaly detection | | Sales process documentation (current version) | AI must reference approved process before recommending changes | ### Required Skills | Skill | When to Load | | salesforce-admin.md | Any CRM workflow or data quality task | | pipeline-analytics.md | Any reporting or forecast support task |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix correctly identifies that this is a festival/partnership context, which is a meaningful differentiation from a standard B2B SaaS sales ops role. However, the table entries are still generic descriptions rather than actionable operational definitions. 'Track partnership deals' does not tell an AI agent what pipeline stages exist, what a partner deal looks like versus a sponsor deal, or what metrics define success. 'Mission alignment metrics' is undefined. The priorities table ranks items 1-4 without explaining what work is currently in flight or what blocking issues exist.",
      "example_rewrite": "### Story Portal Operations Context | Area | Specific Definition | Current State | | **Partnership Pipeline** | Festival co-presenter and venue partner deals tracked through 5 stages: Identified → Outreach → Proposal → Negotiation → Signed. Target: 12 signed partners per festival cycle | Stage 3-4 deals require manual follow-up reminder; automation not yet built | | **Sponsor Tiers** | Three sponsor tiers (Presenting, Supporting, Community) with distinct deliverable packages defined in Sponsor Deck v2.3 | HubSpot properties for tier assignment exist but 40% of records missing tier tag | | **Impact Metrics** | Mission alignment reported as: communities reached, artist fees paid, accessible tickets issued — reported to board quarterly | No dashboard exists; currently assembled manually from event debrief docs |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section — this is the only template section entirely missing, and its absence means there is zero guardrail against the most common Sales Ops failure modes (process theater, dashboard proliferation, tool sprawl). A role with no anti-patterns gives an AI agent no way to self-correct when it drifts toward locally reasonable but organizationally harmful behavior."
}
```