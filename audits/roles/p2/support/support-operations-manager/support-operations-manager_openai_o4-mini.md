{
  "role": "support-operations-manager",
  "department": "support",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 8,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Principles are articulated but remain generic; they lack examples tying them to support operations contexts like peak periods or multi-channel routing.",
      "example_rewrite": "Principle: Festival Surge Resilience — Predefine queue thresholds and backup staffing plans to maintain SLA during high-volume events."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No anti-patterns are defined, leaving operators without guidance on pitfalls like over-automation or SLA threshold misconfigurations.",
      "example_rewrite": "Anti-Pattern: Auto-Closure Overreach — Automatically closing tickets after one response without human review leads to unresolved inquiries; always include a final manual check for critical accounts."
    }
  ],
  "top_improvement": "Define role-specific anti-patterns to guide operators on common pitfalls such as over-automation, SLA misconfiguration, and ticket misrouting."
}