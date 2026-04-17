{
  "role": "ai-ml-engineer",
  "department": "engineering",
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
      "finding": "The listed anti-patterns (e.g., “Ignore latency,” “Skip quality testing”) are broadly applicable to any AI role rather than tailored to the day-to-day pitfalls of an AI/ML engineer, such as failing to version prompt templates or neglecting pipeline instrumentation.",
      "example_rewrite": "| Don't | Why | Instead |\n|-------|-----|---------|\n| Omit prompt versioning | Hard to trace regressions when prompts change silently | Store prompts in a versioned repository, tag releases, and document changes |\n| Deploy pipelines without monitoring hooks | Failures and drift go unnoticed | Integrate end-to-end instrumentation and alerting for each pipeline |"
    }
  ],
  "top_improvement": "Refine anti-patterns to spotlight AI/ML Engineer–specific failures—e.g., missing prompt version control, lack of pipeline telemetry—instead of generic platitudes."
}