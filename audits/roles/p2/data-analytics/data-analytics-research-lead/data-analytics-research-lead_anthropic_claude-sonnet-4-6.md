```json
{
  "role": "data-analytics-research-lead",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 5,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All six principles are generic research platitudes that could apply to any analyst, researcher, or consultant role. 'Tools Enable Insight,' 'Methods Matter,' and 'Evidence-Based Decisions' carry no specificity to an analytics research scout operating inside a media/events product company. None of the principles address the unique tension this role navigates — evaluating tools you will never personally implement, convincing engineers to adopt things they didn't discover, or resisting vendor hype cycles in a fast-moving modern data stack ecosystem.",
      "example_rewrite": "Replace generic entries with role-specific tensions. Examples: | **Recommend Without Implementing** | You evaluate tools you will never put in production — your credibility depends on POC rigor, not personal preference. | **Hype Immunity** | The modern data stack produces a new 'category-defining' tool monthly. Your value is in separating durable signal from vendor marketing noise. | **Adoption Is the Finish Line** | A research report no one acts on is a failed research project. Every evaluation must end with a named owner and a clear next step. | **Engineer Empathy** | Recommendations that ignore implementation cost, migration pain, or existing contracts will be ignored — research must include adoption friction analysis. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff artifacts are named at the category level ('Research findings,' 'Tool recommendations,' 'Best practices') but not at the document level. There is no specification of format, structure, or what constitutes a complete artifact. 'Vendor Manager' appears in the Delivers To table but is not confirmed as a role in the collaboration section or the charter reference — a potential hallucinated role. The 'Receives From' table lists 'Research priorities' from the Head but does not specify whether that is a written brief, a backlog ticket, or a verbal conversation, making AI handoff behavior undefined.",
      "example_rewrite": "Tighten each handoff row to name the artifact, its format, and the trigger. Example rows: | Delivers To: Head of Data & Analytics | Artifact: Tool Evaluation Report (structured doc: criteria matrix, POC results, recommendation, adoption risk, estimated cost) — delivered after every formal evaluation cycle | | Delivers To: Analytics Engineer | Artifact: Adoption Brief (1-page doc: tool name, recommended use case, integration notes, POC environment access link) — delivered when recommendation is approved | | Receives From: Head of Data & Analytics | Artifact: Research Brief (written Notion doc: priority topic, success criteria, deadline, decision context) — triggers Workflow 1 or 2 |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "This role has no Anti-Patterns section at all. The DO/DON'T boundary list exists but serves a different function — it defines ownership scope, not behavioral failure modes. Anti-patterns are absent entirely, which is a critical template gap. The checklist standard explicitly requires role-specific anti-patterns, and none are present. This is the single largest structural deficiency in the file.",
      "example_rewrite": "Add a dedicated Anti-Patterns section with failures specific to this role. Example: **Anti-Pattern 1 — Evaluation Theater:** Conducting thorough POCs that produce detailed reports but never result in adoption decisions. Fix: Every evaluation closes with a named decision owner and a date. **Anti-Pattern 2 — Recency Bias:** Recommending the newest tool because it is new, not because it is better. Fix: Comparison matrices must include the incumbent tool as a baseline option. **Anti-Pattern 3 — Scope Creep into Implementation:** Beginning to configure or build production pipelines during a POC 'just to test it properly.' Fix: POC environments are throwaway — any production-bound work transfers to Analytics Engineer via Adoption Brief. **Anti-Pattern 4 — Research Without a Requester:** Pursuing interesting technology trends with no stakeholder request or decision on the horizon. Fix: Every active research item must map to a named priority from the Head's Research Brief."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol is present and correctly structured for Hybrid classification, which is good. However, the Context Requirements section is entirely unfilled — placeholder text '[Context item 1]' and '[Use placeholder format: skill-name.md]' was never completed. An AI agent loading this role has no idea what context files to load before starting work, what skills files augment its capabilities, or what a 'Research Brief' looks like structurally. The human/AI division of labor in Deployment Notes is clear in principle but not operationalized — 'AI assists with gathering' does not tell the agent what gathering looks like in Browser mode (which URLs, which source types, which synthesis format).",
      "example_rewrite": "Complete the Context Requirements section with actual entries. Example: **Required Context:** [ ] analytics-team-current-stack.md — current tools in production to avoid recommending duplicates [ ] story-portal-data-glossary.md — domain vocabulary for audio/event analytics [ ] vendor-evaluation-criteria-template.md — standard scoring rubric [ ] head-of-analytics-research-priorities.md — active research queue. **Required Skills:** | tool-evaluation-framework.md | Load when starting Workflow 1 | | benchmarking-methodology.md | Load when entering POC phase | | analytics-trend-sources.md | Load when conducting Trend Monitoring |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix is the strongest section in the file. It correctly identifies domain-specific research priorities (audio engagement, festival offline context, privacy-first tracking) and names actual tools relevant to the product (Amplitude, Mixpanel, PostHog, Observable, dbt). The four research priorities are ordered and product-relevant. Minor weakness: the 'Methodology Focus' table lists needs without specifying what a good answer looks like — 'Story completion metrics' is a research topic, not a methodology standard, so the distinction is blurry. No improvement rewrite required given score of 7, but tightening 'Best Practices Needed' column to name the open question rather than the topic area would sharpen it further.",
      "example_rewrite": null
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section — this is the only dimension with a structural zero (the section does not exist). Four role-specific anti-patterns covering evaluation theater, recency bias, scope creep into implementation, and research without a requester would immediately raise template compliance and provide the AI agent with the most operationally useful behavioral guardrails in the entire file."
}
```