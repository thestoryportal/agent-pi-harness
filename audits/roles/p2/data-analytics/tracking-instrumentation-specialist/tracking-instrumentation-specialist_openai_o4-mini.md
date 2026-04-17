```json
{
  "role": "tracking-instrumentation-specialist",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 9,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "No anti-patterns section defined; lacks 3–5 role-specific anti-patterns to warn against common pitfalls.",
      "example_rewrite": "## Anti-Patterns\n\n| Pattern                  | Why Avoid                                                                 |\n|--------------------------|---------------------------------------------------------------------------|\n| Vanity Tracking          | Capturing metrics nobody uses floods systems with noise and wastes effort |\n| Schema-Less Implementation | Deploying events without predefined schemas causes inconsistency and rework |\n| Ignoring Consent Flows   | Sending events before explicit user consent violates privacy requirements  |\n| Over-Reliance on Defaults | Blindly using default tag settings leads to inaccurate or incomplete data  |"
    }
  ],
  "top_improvement": "Add a dedicated anti-patterns section with 3–5 specific examples (e.g., vanity tracking, schema-less implementation, ignoring consent flows)"
}
```