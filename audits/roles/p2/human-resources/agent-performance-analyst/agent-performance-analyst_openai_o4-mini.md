{
  "role": "agent-performance-analyst",
  "department": "human-resources",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 8,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "Principles (e.g. “Continuous Optimization”) are high-level and generic, lacking actionable specificity for this role.",
      "example_rewrite": "Replace “Continuous Optimization” with “Run bi-weekly agent performance sprints using A/B metric testing to validate incremental improvements.”"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "The anti-patterns section is missing entirely, so there are no role-specific pitfalls to avoid.",
      "example_rewrite": "Add Anti-Patterns:\n| Anti-Pattern              | Impact                                                  |\n|---------------------------|---------------------------------------------------------|\n| Vanity Metric Obsession   | Focus on irrelevant KPIs leads to misguided optimizations|\n| Analysis Paralysis        | Excessive deep dives delay actionable insights          |\n| One-Size-Fits-All Benchmarking | Ignoring unique agent contexts skews performance targets |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix lists broad performance areas but lacks project-specific metrics, thresholds, or next-step guidance.",
      "example_rewrite": "Refine “Task completion” to “Story Portal Task Agents achieve ≥95% success rate within a 2-hour SLA per sprint, tracked in the central dashboard with alerts for deviations.”"
    }
  ],
  "top_improvement": "Define role-specific anti-patterns to guide behavior and avoid common pitfalls."
}