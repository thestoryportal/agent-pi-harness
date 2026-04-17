{
  "role": "bi-developer",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 9,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "No anti-patterns section is provided; BI-specific pitfalls (e.g., cluttered dashboards, untested performance) are not called out.",
      "example_rewrite": "## Anti-Patterns\n1. Overloading Dashboards: Packing too many metrics into one view. STOP: Limit to top 5 KPIs per dashboard.\n2. Skipping Performance Tests: Deploying without load checks. STOP: Always benchmark query times before release.\n3. Ignoring User Feedback: Launching without validating with end users. STOP: Run a feedback session before final publish."
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3–5 BI Developer–specific pitfalls and clear STOP points to prevent common mistakes."
}