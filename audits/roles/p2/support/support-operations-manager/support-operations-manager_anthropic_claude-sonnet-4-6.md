```json
{
  "role": "support-operations-manager",
  "department": "support",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic operations platitudes that could apply to any ops role in any industry. 'Efficiency Enables Quality' and 'Continuous Optimization' are interchangeable with boilerplate. None reference Story Portal's specific context — festival surges, AI-first automation, multi-channel complexity, or the music platform domain. The meaning column compounds the problem by restating the principle in fewer words ('Streamlined ops = better support') rather than explaining the role's specific operational philosophy.",
      "example_rewrite": "| **Surge-First Design** | Operations infrastructure is architected for festival peak loads, not average days. A system that breaks at 3x volume is a failed system regardless of normal-day performance. | | **Automate Tier 1, Humanize Tier 2** | Routine ticket routing, status replies, and SLA alerts are automation targets. Any human touching a task a rule can handle is waste. Any automation touching a nuanced artist complaint is a risk. | | **SLA Integrity Over Vanity Metrics** | A 98% SLA score achieved by downgrading ticket priority classifications is worse than a 91% score honestly measured. Metrics exist to surface truth, not to report well. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs name roles but describe artifacts in the vaguest possible terms. 'Operational priorities' received from Head of Support, 'Operations reports' delivered to Head of Support, and 'Tools and processes' delivered to Support Team are not artifacts — they are categories. There is no indication of format, frequency, trigger condition, or what specifically constitutes the artifact. An AI agent cannot act on 'Operations reports' without knowing if that means a weekly Zendesk export, a Slack summary, or a formal deck. The Support Research Analyst appears in 'Works With' but is absent from handoffs entirely despite being listed as a data source.",
      "example_rewrite": "| Delivers To | Artifact | Format | Trigger | \n|---|---|---|---| \n| Head of Support | Weekly Ops Report | Structured doc: queue volumes, SLA compliance %, breach count, top routing failures, one recommended action | Every Monday 9am or post-festival within 24hrs | \n| Support Team | Routing Change Notice | Changelog entry in help desk + Slack #support-ops: what changed, why, effective time | Any routing rule modification | \n| IT Manager | Tool Requirements Brief | Written spec: tool name, integration needed, access level, timeline, business justification | Prior to any new tool procurement request |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There are zero anti-patterns in this role file. The Boundaries section lists DO/DON'T/ESCALATE items, but these are domain ownership boundaries, not behavioral anti-patterns. Anti-patterns should describe failure modes specific to this role — the ways a Support Operations Manager specifically goes wrong. Nothing here warns against over-automating sensitive escalations, optimizing for SLA compliance scores rather than actual resolution quality, implementing routing rules without TSE input on technical ticket classification, or scaling festival capacity too late because surge signals were misread.",
      "example_rewrite": "### Anti-Patterns to Avoid \n| Anti-Pattern | Why It Fails | Correct Behavior | \n|---|---|---| \n| **SLA Theater** | Reclassifying P1 tickets as P2 to improve compliance percentages. Reports look good; customer experience degrades. | Report SLA performance accurately; escalate target misalignment to Head of Support rather than gaming classifications. | \n| **Premature Automation** | Automating ticket routing before TSE has validated technical ticket taxonomy. Misfiled technical issues reach wrong queues at scale. | Validate routing logic with TSE on any category touching technical issues before deploying rules. | \n| **Festival Prep Lag** | Building surge capacity after ticket volume spikes rather than on historical festival calendar signals. | Pull prior festival data from Support Research Analyst 4 weeks before known events and pre-scale by week 3. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol and Hybrid split are present, which gives an AI agent a basic operational loop. However, the Context Requirements section is completely unfilled — '[Context item 1]' and '[Context item 2]' are literal placeholders, and the Required Skills table has no entries. An AI agent loading this role cannot determine what context files to load, what data sources to access, or what constitutes a valid starting state. The STOP points in workflows lack specification of who reviews and what constitutes approval to continue — 'STOP → Analysis complete' is a pause, not a checkpoint with a defined human approver.",
      "example_rewrite": "### Required Context \n- [ ] Current Zendesk routing rules export \n- [ ] Active SLA definitions by ticket tier \n- [ ] Festival calendar for current quarter \n- [ ] Last weekly ops report \n- [ ] Open IT tickets affecting support tooling \n\n### Required Skills \n| Skill | When to Load | \n|---|---| \n| zendesk-admin.md | Any routing or queue task | \n| sla-framework.md | Any SLA monitoring or breach task | \n| festival-surge-playbook.md | Any capacity planning or event-prep task | \n\nAnd update STOP points: 'STOP → Queue analysis complete. Share findings with Head of Support. Wait for confirmation to proceed to design phase.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix identifies the right operational scenarios — festival surge, channel mix, AI automation, SLA management — and the scenario table adds some useful specificity (pre-scaled capacity, priority routing). However, the priorities table is not actionable: 'Festival surge capacity' as Priority 1 does not tell an AI agent what action to take, what threshold triggers escalation, or what 'ready' looks like. The channel optimization row mentions 'chat, email, social balance' without specifying Story Portal's actual channel stack or relative volume distribution. No SLA targets are specified despite SLA management being a core responsibility.",
      "example_rewrite": "### Story Portal SLA Targets \n| Ticket Type | First Response | Resolution Target | Breach Action | \n|---|---|---|---| \n| Artist technical (P1) | 1 hour | 4 hours | Auto-escalate to TSE + notify Head of Support | \n| Festival period all tiers | 50% of standard target | — | Pre-approval to pull overflow routing | \n| Standard user inquiry | 8 business hours | 3 business days | Weekly breach report to Head of Support | \n\n### Festival Readiness Checklist \n- Surge routing rules activated (T-7 days) \n- Overflow queue configured and tested (T-5 days) \n- SLA breach alerts threshold lowered to 70% of limit (T-3 days) \n- TSE on-call schedule confirmed with IT Manager (T-2 days)"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 3-5 role-specific failure modes. This role file has zero anti-patterns — the single largest gap. Generic DO/DON'T boundary lists do not substitute for behavioral failure modes. Without anti-patterns, an AI agent has no guardrails against the most common ways this role goes wrong: gaming SLA metrics, automating without TSE validation, and missing festival surge windows. This is a one-line template section that is entirely absent and would immediately raise the role's operational safety profile."
}
```