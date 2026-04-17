```json
{
  "role": "client-success-manager",
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
      "finding": "All 6 principles are one-line platitudes with no operational meaning. 'Results matter', 'Act before problems', 'Use creates success' — these could apply to any role in any industry. None are specific to a CSM navigating the tension between client advocacy and commercial goals, or to the Story Portal context (e.g., what does 'value' mean for a festival partner vs. a community storyteller?). The table format masks the emptiness: the 'Meaning' column simply restates the principle name in fewer words.",
      "example_rewrite": "| **Adoption Precedes Renewal** | A client who uses fewer than 3 core features in month 2 will not renew regardless of relationship quality. CSM intervention priority is always usage gaps before sentiment gaps. | | **Churn Signals Appear 90 Days Early** | By the time a client says they are leaving, the CSM has already missed the intervention window. Health score drops, declining login frequency, and unanswered check-in emails are the real renewal conversation. | | **Success Plans Are Contracts, Not Documents** | A success plan with no named milestones, no client signatory, and no consequence for missed checkpoints is a filing exercise. Every plan must include a 60-day mutual commit reviewed in QBR."
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs name roles but not artifacts with enough specificity to be actionable. 'Receives from Sales: Client goals' does not tell an AI agent what format, what fields, or what constitutes a complete handoff. 'Delivers to Account Manager: Health status' is ambiguous — is this a Gainsight scorecard export, a written narrative, a slide deck? Critically, the role references 'Sales' and 'Implementation Specialist' in handoffs and collaboration but these may not exist in the Organizational Charter under those exact names, which violates the template standard against hallucinated roles. No handoff specifies a trigger condition or SLA.",
      "example_rewrite": "| Receives From | Artifact | Format | Trigger | SLA | | Sales (Account Executive) | Closed-Won Handoff Package: named goals from discovery, committed use cases, stakeholder map, contract start date | Salesforce Opportunity record + attached Goals Doc (PDF) | Contract executed | Within 5 business days of close | | Implementation Specialist | Graduation Report: completed onboarding checklist, active user count, configured features, open technical risks | Implementation Tracker (Google Sheet, shared link) | Go-live confirmed | Day of go-live handoff call |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There are no anti-patterns section in this role file at all. The DO/DON'T boundary list exists but it describes role boundaries (ownership), not behavioral failure modes. Anti-patterns should describe the specific wrong behaviors a CSM AI agent might drift into — e.g., becoming a glorified scheduler, conflating activity completion with value realization, avoiding difficult health conversations to preserve relationship comfort. None of these appear. The DON'T list ('Don't own relationship strategy') is a jurisdiction map, not an anti-pattern catalog.",
      "example_rewrite": "### Anti-Patterns to Avoid | Anti-Pattern | Why It Fails | Correct Behavior | | **Check-in Theater** | Conducting regular calls with no health data reviewed beforehand and no outcome recorded afterward. Feels like success work but produces no intervention signal. | Every client touchpoint must open with current health score, last usage pull, and a specific question tied to a success plan milestone. | | **Adoption Vanity Metrics** | Reporting 'login rate up 15%' without connecting logins to feature adoption or goal progress. Looks good in reports, masks stagnation. | Adoption metrics must always be reported as: feature X used by Y% of licensed seats, tied to use case Z from success plan. | | **Escalation Avoidance** | Delaying churn-risk escalation to Account Manager because the CSM hopes to resolve it independently and protect the relationship perception. | Any client with two consecutive declining health scores must be escalated to AM within 24 hours regardless of CSM confidence in resolution."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Iteration Protocol exists and the Hybrid split is defined, but an AI agent loading this role still cannot answer basic operational questions: What does 'monitor health' mean in practice — which data sources, which thresholds trigger a risk flag? What does the AI produce when it 'generates reports' — what fields, what format, delivered where? The Context Requirements section contains unfilled placeholders ('[Context item 1]', '[Context item 2]') and the Required Skills table is empty. These are not minor gaps — they are the exact fields an AI agent reads to initialize. The STOP points in workflows do not specify who reviews or what approval looks like.",
      "example_rewrite": "### Required Context | Context Item | Source | When Required | | Client health scores (last 30 days) | Gainsight dashboard export | Every success cycle trigger | | Product usage data (feature-level, per seat) | Analytics platform (Mixpanel/Amplitude) | Before any adoption review | | Open support tickets (P1/P2 only) | Support queue | Before risk intervention workflow | ### Iteration Protocol STOP Clarification: At each STOP point, AI must output a structured status block: current health score, adoption percentage vs. plan, risks flagged (Y/N), and a single recommended next action for human approval before proceeding."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 3,
      "finding": "The Story Portal appendix lists four outcome rows and four milestone rows but they are surface-level labels with no operational content. 'First story: Initial engagement' does not tell a CSM what counts as success, what the target timeframe is, what intervention triggers if it does not happen, or how it maps to the client's success plan. 'Festival partner success' is listed as Priority 1 with no definition of what success means for a festival partner versus a community user. The appendix reads as a placeholder dressed in table formatting rather than genuine project-specific guidance.",
      "example_rewrite": "### Story Portal Success Thresholds | Milestone | Definition of Success | Target Timeframe | At-Risk Signal | CSM Action if At-Risk | | First Story Published | Client's designated storyteller publishes and shares at least 1 story with a minimum audience of 10 | Within 14 days of onboarding completion | No story draft created by Day 7 | CSM schedules 30-min story creation session with storyteller, shares Story Starter template | | Festival Partner Activation | Partner has submitted festival brief, confirmed 3+ participating storytellers, and scheduled community preview event | 45 days before festival date | Brief not submitted 60 days before festival | Escalate to Account Manager; CSM delivers pre-filled brief template to reduce friction |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific behavioral failure modes. This role file currently has zero anti-patterns, which means an AI agent has no guardrails against the most common CSM failure modes (check-in theater, adoption vanity metrics, escalation avoidance). This is the highest-risk gap because the DO/DON'T boundary list only covers jurisdiction — it provides no behavioral correction signal for an AI operating autonomously in the Hybrid classification."
}
```