{
  "role": "data-quality-engineer",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 8,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "Missing an Anti-Patterns section. The role fails to call out common pitfalls like over-alerting, symptom patching, or ignoring upstream context.",
      "example_rewrite": "## Anti-Patterns\n- Over-Alerting: triggering notifications for minor deviations within expected thresholds, causing alert fatigue.\n- Symptom Patching: applying quick fixes without investigating the underlying root cause.\n- Ignoring Data Context: running validations without updating rules to reflect recent business logic changes.\n- Stale Thresholds: never revisiting alert thresholds, leading to wasted effort on obsolete rules."
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3–5 role-specific pitfalls (e.g., over-alerting, symptom patching) to guide behavior and avoid common mistakes."
}