{
  "role": "data-engineer",
  "department": "engineering",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 8,
    "anti_pattern_quality": 5,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "anti_pattern_quality",
      "score": 5,
      "finding": "Most listed anti-patterns are generic engineering pitfalls rather than data engineering-specific issues like schema drift, manual backfills, or missing lineage capture.",
      "example_rewrite": "| Don’t skip schema versioning | Causes downstream failures | Implement semantic versioning for data contracts and migrations |\n| Avoid manual one-off backfills | Not reproducible or idempotent | Write automated, idempotent backfill scripts |\n| Ignore data lineage | Makes root-cause analysis difficult | Integrate automated lineage tracking in pipeline executions |\n| Hardcode retention policies | Leads to inconsistent data lifecycle | Enforce retention via centralized ETL configuration |"
    }
  ],
  "top_improvement": "Refine the anti-pattern section to include data engineering-specific scenarios such as schema drift and lineage gaps."
}