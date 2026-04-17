{
  "role": "release-manager",
  "department": "platform-engineering",
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
      "finding": "Anti-patterns are generic release best practices and not tailored to specific pitfalls the Release Manager might face, such as maintenance window conflicts or version metadata drift.",
      "example_rewrite": "| Don't | Why | Instead |\n|------|-----|---------|\n| Release during maintenance blackout | Causes unplanned downtime and stakeholder conflict | Confirm and respect scheduled maintenance windows before release |"
    }
  ],
  "top_improvement": "Make anti-patterns more role-specific by including release-manager-specific pitfalls like neglecting maintenance windows or version metadata consistency."
}