{
  "role": "channel-partner-sales-manager",
  "department": "sales",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 8,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "The six principles are generic platitudes and not tailored to the unique challenges of channel partner management.",
      "example_rewrite": "Replace 'Quality Over Quantity' with 'Selective Partner Profiling: Prioritize partners based on a standardized 10-point fit and potential revenue score—only onboard those scoring 8+.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no anti-pattern section. The role lacks 3–5 specific pitfalls such as overloading partners or failing to align incentives.",
      "example_rewrite": "Anti-Pattern: “Chasing Partner Count Over Quality” – Adding partners without revenue forecasts leads to low ROI and wasted enablement effort."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "AI deployment guidance is high-level and doesn’t define concrete AI tasks, data sources, or output formats.",
      "example_rewrite": "Under AI assists with tracking, add: “AI weekly action: Query the Partner Portal API every Monday at 8 AM, generate a performance dashboard in CSV, and post alerts for any partner below 75% of target in the #partner-alerts Slack channel.”"
    }
  ],
  "top_improvement": "Add a dedicated, role-specific Anti-Pattern section with 3–5 unique pitfalls."
}