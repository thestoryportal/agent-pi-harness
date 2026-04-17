{
  "role": "ai-ethics-specialist",
  "department": "ai-automation",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 6,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "The six principles are clear but read as generic platitudes rather than actionable guidelines tied to specific AI ethics tasks.",
      "example_rewrite": "Replace 'Stakeholder Voice' with 'Mandate quarterly stakeholder feedback sessions and integrate sentiment analysis on support tickets to close the feedback loop.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Artifacts like 'systems for review' and 'bias findings' are too vague—reviewers need exact documents or data schemas to execute handoffs.",
      "example_rewrite": "Receives From AI/ML Engineer: model versioned artifacts (model.pkl), training dataset schema (schema.json), fairness test suite results (fairness_report.csv)."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No anti-patterns are listed. Without role-specific pitfalls, the specialist may repeat common mistakes.",
      "example_rewrite": "- Blind trust in default metrics: Relying on off-the-shelf fairness scores without context-aware adjustments.\n- Checklist tick-boxing: Running ethics checklists perfunctorily without deeper scenario analysis.\n- Siloed assessment: Conducting ethics reviews post-deployment instead of iteratively during design."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "AI deployment notes mix human and AI tasks but lack machine-actionable steps or API triggers for an AI agent.",
      "example_rewrite": "For AI: upon 'trigger_review' event, run bias_evaluator.py with model.pkl and schema.json, output fairness_report.csv, then emit 'review_ready' event."
    }
  ],
  "top_improvement": "Add a dedicated anti-patterns section with at least three role-specific pitfalls to guide consistent, rigorous ethics reviews."
}