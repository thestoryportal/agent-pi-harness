{
  "role": "agent-onboarding-specialist",
  "department": "human-resources",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 8,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "The six principles are phrased as high-level platitudes rather than concrete guidelines for how this role operates differently from others.",
      "example_rewrite": "• Contextual Precision: Provide exactly the project’s data schema, business rules, and stakeholder preferences so agents respond with tailored recommendations."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "No anti-patterns are defined. Without role-specific warnings, the specialist may repeat common mistakes like overloading agents with stale context or skipping human checkpoints.",
      "example_rewrite": "Anti-pattern: ‘Context Dumping’ – Injecting all historical project files without filtering, causing agents to misinterpret priorities. Instead, curate only current sprint documents and stakeholder briefs."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "Placeholders in the Context Requirements section (e.g. [Context item 1]) leave an AI agent uncertain which artifacts to gather and how to verify readiness.",
      "example_rewrite": "Required Context: • project-charter.md • sprint-backlog.csv • stakeholder-map.xlsx • compliance-checklist.pdf"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix lists deployment areas but gives no actionable steps or metrics tied to these priorities (e.g., target headcount, SLAs).",
      "example_rewrite": "Festival surge: Ramp up 30 seasonal agents with event-specific scripts within 48 hrs; track daily readiness rate ≥ 95%."
    }
  ],
  "top_improvement": "Add a dedicated Anti-Pattern section with 3–5 role-specific warnings and corrective examples."
}