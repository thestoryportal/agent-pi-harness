{
  "role": "head-of-support",
  "department": "support",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 6,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Principles like Fast Resolution and Empathy First remain high-level and lack measurable support metrics or actions.",
      "example_rewrite": "Proactive Escalation Boundaries: Escalate any P1 ticket unresolved within 15 minutes to engineering on-call, with automated notification to the Head of Support."
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Handoffs use generic roles and unspecified artifacts instead of naming deliverable versions and target recipients.",
      "example_rewrite": "When delivering user feedback to the Head of Product, submit 'Q1 Support Insights Report v1.0' including categorized feature requests and CSAT trend analysis."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "Anti-patterns section is missing; the role guidance lacks common pitfalls like firefighting mode or knowledge base neglect.",
      "example_rewrite": "Anti-patterns:\n1. Firefighting Mode: reacting to tickets without proactive triage.\n2. Knowledge Stagnation: failing to update FAQs after recurring issues.\n3. Escalation Overuse: escalating Tier 1 issues without documented rationale."
    }
  ],
  "top_improvement": "Add a specific Anti-Patterns section with 3-5 role-specific pitfalls and avoidance strategies."
}