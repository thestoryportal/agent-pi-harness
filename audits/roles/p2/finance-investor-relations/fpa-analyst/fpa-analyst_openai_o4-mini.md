```json
{
  "role": "fpa-analyst",
  "department": "finance-investor-relations",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 8,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Principles include generic platitudes (e.g., ‘Continuous Improvement’) rather than FP&A-specific guidelines.",
      "example_rewrite": "Replace 'Continuous Improvement' with 'Iteratively refine forecast accuracy by analyzing monthly variance trends and updating model drivers accordingly.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "Anti-patterns section is missing; lacks FP&A-specific pitfalls like overfitting historic data or ignoring business drivers.",
      "example_rewrite": "Add anti-pattern: 'Chasing exact variance reconciliation daily instead of focusing on material month-end drivers – leads to distracted FP&A cycles.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "Story Portal appendix lists priorities but doesn’t tie deliverables to Story Portal metrics or sprints.",
      "example_rewrite": "Link 'Runway forecasting' to Story Portal by adding: 'Map cash runway forecasts to monthly active story counts and forecast development spend per sprint.'"
    }
  ],
  "top_improvement": "Define and include FP&A-specific anti-patterns to guide Analysts in avoiding common forecasting and analysis pitfalls."
}
```