{
  "role": "ai-trainer-evaluator",
  "department": "ai-automation",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 8,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "The role’s philosophy principles are accurate but remain high-level and could be more distinctive by linking them to specific evaluation scenarios or advanced quality challenges.",
      "example_rewrite": "Add a principle like 'Bias Audit Focus: Systematically probe outputs for demographic fairness issues across underrepresented groups.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "No role-specific anti-patterns are defined, missing an opportunity to warn against common evaluator missteps like overly narrow sampling or feedback delays.",
      "example_rewrite": "Include anti-patterns such as: 'Overfitting to Benchmarks: Prioritizing test-set scores over real-world robustness.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The AI deployment section outlines tools and an iteration loop but lacks direct, step-by-step agent instructions to operationalize the role programmatically.",
      "example_rewrite": "Specify: 'Step 1: call evaluate_outputs(batch) → returns scores; Step 2: log_scores(scores) → updates dashboard; Step 3: generate_feedback_report() → email to AI/ML Engineer.'"
    }
  ],
  "top_improvement": "Define clear, role-specific anti-patterns to guide evaluators and prevent common mistakes."
}