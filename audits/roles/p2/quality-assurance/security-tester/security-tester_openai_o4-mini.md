```json
{
  "role": "security-tester",
  "department": "quality-assurance",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 9,
    "anti_pattern_quality": 6,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "anti_pattern_quality",
      "score": 6,
      "finding": "The listed anti-patterns are generic security testing clichés and don’t surface role-specific pitfalls (e.g., overreliance on a single tool or missing hybrid attack scenarios).",
      "example_rewrite": "\"Don't over-rely on OWASP ZAP for all test phases\" | Why: it misses chained business-logic exploits | Instead: \"Combine OWASP ZAP scans with manual exploit chaining against new microservices to uncover logic flaws\""
    }
  ],
  "top_improvement": "Enhance the anti-patterns section with unique, role-specific pitfalls—e.g., warn against relying solely on one scanner and missing hybrid adversarial tactics."
}
```