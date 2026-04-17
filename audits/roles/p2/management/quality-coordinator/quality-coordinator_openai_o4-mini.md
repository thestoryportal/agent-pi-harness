{
  "role": "quality-coordinator",
  "department": "management",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 8,
    "anti_pattern_quality": 4,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "The six principles are standard QA platitudes and not tailored to the unique scope of the Quality Coordinator role.",
      "example_rewrite": "Add a principle like **Testability by Design**: ‘Enforce that every new feature includes built-in test hooks and mocks to reduce setup time and flakiness.’"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 4,
      "finding": "The listed anti-patterns are generic QA clichés rather than pitfalls specific to coordinating QA in an AI-native environment.",
      "example_rewrite": "Replace ‘Test everything manually’ with ‘Relying solely on exploratory tests for AI model drift — Instead: Implement automated drift detection suites with scheduled retraining checks.’"
    }
  ],
  "top_improvement": "Make the philosophy principles specific to this role by introducing guidelines like 'Testability by Design' that address the unique challenges of coordinating QA in an AI-native workflow."
}