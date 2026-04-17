{
  "role": "delivery-manager",
  "department": "client-services",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 8,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "Principles are generic platitudes and lack role-specific actionable guidance.",
      "example_rewrite": "Instead of “Continuous Improvement,” specify “Facilitate bi-weekly retrospectives with project managers to implement two process improvements per quarter.”"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No anti-patterns section present; missing role-specific pitfalls to avoid.",
      "example_rewrite": "Add anti-pattern: “Overcommitting resources across overlapping festival and onboarding projects, leading to missed SLAs.”"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "AI responsibilities are broad; lacks explicit tasks and data inputs for AI agents.",
      "example_rewrite": "Specify “AI runs weekly capacity forecast by ingesting Story Portal resource.csv and flags any project with >85% utilization.”"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "Story Portal appendix lists categories but lacks actionable links to specific project workflows or artifacts.",
      "example_rewrite": "Detail “For festival projects, use Story Portal template ‘Festival-Deploy.md’ to map resource timelines and escalate on-day-of-event issues.”"
    }
  ],
  "top_improvement": "Include a dedicated Anti-Patterns section with 3-5 delivery manager-specific pitfalls to avoid, ensuring clear guidance on what not to do."
}