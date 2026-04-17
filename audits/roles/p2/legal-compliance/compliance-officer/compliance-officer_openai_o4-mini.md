```json
{
  "role": "compliance-officer",
  "department": "legal-compliance",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 8,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Principles like 'Continuous Improvement' and 'Transparent Reporting' are generic and lack role-specific context or examples.",
      "example_rewrite": "Add a compliance-centric principle: 'Embedded Risk Culture: Partner with product teams to integrate real-time risk dashboards into feature sprints, ensuring regulatory inputs drive architecture decisions.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No Anti-Pattern section is defined; missing role-specific compliance anti-patterns.",
      "example_rewrite": "Anti-Pattern: 'Checkbox Auditing' — Performing audits by strictly following templates without assessing emerging risks or tailoring controls to unique business units."
    }
  ],
  "top_improvement": "Introduce a dedicated Anti-Pattern section with 3–5 Compliance Officer–specific scenarios (e.g., 'Checkbox Auditing', 'Policy Paralysis') to highlight what to avoid."
}
```