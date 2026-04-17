```json
{
  "role": "head-of-client-services",
  "department": "client-services",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 4,
    "story_portal_relevance": 3
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are generic client services platitudes that could appear in any CSM job description from 2015. 'Client Success Is Our Success' and 'Trust Through Delivery' convey no operational instruction. None of the principles reference the Story Portal context (festivals, sponsors, community), nor do they encode any decision-making heuristics specific to this role's tension points — e.g., balancing sponsor retention against community integrity, or managing expansion pressure without overselling platform capabilities.",
      "example_rewrite": "| **Sponsor Retention Over New Acquisition** | When resource conflicts arise between onboarding new sponsors and deepening existing festival partner relationships, prioritize the existing partner. A renewed multi-year festival deal outweighs a first-year sponsor conversion in lifetime value and community credibility. | | **Escalate Churn Risk Before the Renewal Window** | Flag any account showing two consecutive months of declining engagement metrics to the CRO and CEO no later than 90 days before contract renewal — not at the 30-day mark when options are limited. | | **Value Realization Before Upsell Conversations** | No expansion discussion is initiated until the client has confirmed achievement of their original success metric in writing or on a recorded review call. Upselling an unrealized promise compounds trust damage. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs name broad functional areas rather than actual role titles or concrete artifacts. 'Receives from Sales → Closed deals' is meaningless operationally — what document, in what system, triggers what action? 'Account Managers' and 'Project Managers' are listed as collaborators but it is unclear if these are roles that exist in the Organizational Charter or are hallucinated. No handoff specifies a named artifact format (e.g., Client Success Plan, Health Score Report, Escalation Brief) or the condition that triggers the handoff.",
      "example_rewrite": "| Receives From | Role (Charter) | Artifact | Trigger | | Sales | Head of Sales | Signed Contract Package (contract PDF + discovery notes + agreed success metrics) | Deal marked Closed-Won in CRM | | Support | Head of Support | Escalation Brief (issue summary, client impact rating 1–5, steps taken, recommended owner) | Escalation tagged 'Client Services' in support queue | | Delivers To | Role (Charter) | Artifact | Trigger | | CRO | Chief Revenue Officer | Monthly Retention & Expansion Report (churn risk list, renewal pipeline, upsell opportunities with ARR estimates) | First Monday of each month |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file whatsoever. The Template Standard checklist explicitly requires 3–5 role-specific anti-patterns. The DO/DON'T boundary table exists but lists ownership rules, not behavioral failure modes. Nothing in the file warns against the specific ways a Head of Client Services typically fails — e.g., becoming a reactive escalation handler instead of a proactive health manager, or conflating client happiness with client value realization.",
      "example_rewrite": "## Anti-Patterns — What Good Looks Like vs. What This Role Gets Wrong | Anti-Pattern | Why It Fails | Correct Behavior | | **Happiness Theater** | Client says 'everything is great' on calls but NPS drops at renewal. Relationship warmth is mistaken for value realization. | Require quantified success metric confirmation every quarter — not sentiment, evidence. | | **Escalation-Only Engagement** | Head of CS only appears in client conversations when something is broken. Clients associate this role with problems, not partnership. | Schedule executive sponsor touchpoints on a fixed cadence independent of issue status. | | **Upsell Before Onboard** | Expansion conversation is opened before the client has completed onboarding or hit their first success milestone, damaging trust and increasing churn risk. | Expansion is gated behind written or recorded confirmation of original success metric achievement. | | **Absorbing Support Work** | Client Services team handles tier-1 support tickets to 'protect the relationship,' masking support volume data and burning CSM capacity. | Route all support requests through Head of Support; CS role is escalation coordination only, not resolution. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Deployment Notes section correctly identifies this as Human-Primary and lists a reasonable split of human vs. AI responsibilities. However, the Context Requirements section is entirely unfilled — two placeholder brackets '[Context item 1]' and '[Context item 2]' were left in the published role file, and the Required Skills table has no entries. An AI agent loading this role has no idea what context files to pull, what data sources to connect to, or what its specific analytical tasks are. The STOP points in workflows exist but are not labeled as human checkpoints — they read as sequential step completions rather than explicit human approval gates.",
      "example_rewrite": "### Required Context | Context File | Purpose | When to Load | | client-health-dashboard.md | Current NPS scores, health scores, renewal dates for all active accounts | Every health review cycle | | retention-playbook.md | Intervention plays by churn risk tier (Low / Medium / High / Critical) | When any account health score drops below threshold | | expansion-criteria.md | Qualification rules for initiating upsell conversations | Before any expansion recommendation is made | ### AI Task Scope When operating in AI-assist mode, AI may: generate draft health score summaries from CRM data, flag accounts meeting churn-risk criteria against retention-playbook.md thresholds, and draft Escalation Briefs for human review. AI may NOT: communicate directly with clients, approve expansion proposals, or close escalations without human sign-off. All STOP points in workflows require explicit human confirmation before proceeding."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 3,
      "finding": "The Story Portal appendix identifies four client types (Festival Partners, Community Sponsors, Platform Users, Technology Partners) and four service priorities, but provides no actionable differentiation between them. There is no indication of what success looks like for each client type, what the renewal or retention dynamics are for a festival-based business, or how the Head of CS should handle the tension between sponsor commercial relationships and community/platform user experience. The appendix could have been written by someone who read the company name but not the business model.",
      "example_rewrite": "### Client Type Playbook (Story Portal) | Client Type | Definition of Value Realized | Retention Signal | Expansion Path | Churn Risk Trigger | | **Festival Partners** | Festival ran on time, sponsor activations delivered, post-event report issued within 14 days | Partner signs LOI for next festival cycle before current event closes | Multi-year partnership agreement; co-branded community content | Partner requests refund, raises delivery complaint, or goes silent post-event | | **Community Sponsors** | Sponsor activation reached agreed community impression target; impact report delivered | Sponsor increases budget or requests additional activation slots | Premium placement; naming rights on community programs | Impression targets missed by >20%; no post-activation debrief completed | | **Platform Users** | User has completed onboarding and logged in for 3+ consecutive weeks | Monthly active usage above baseline; user submits feature request | Seat expansion; premium tier upgrade | Login frequency drops to zero for 14+ days post-onboarding |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 4 role-specific behavioral failure modes. This is the only section entirely missing from the file — the template standard explicitly requires it, and without it neither human practitioners nor AI agents have guardrails against the most predictable ways this role underperforms. Draft the section using the Happy Theater, Escalation-Only Engagement, Upsell Before Onboard, and Support Absorption patterns as a starting framework, each with a concrete corrective behavior tied to Story Portal's festival and sponsor context."
}
```