{
  "role": "ai-research-lead",
  "department": "ai-automation",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 8,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "The principles are broad and could apply to any research role rather than tailored to key Story Portal challenges.",
      "example_rewrite": "\"Principle: Optimize Story Portal Audio Quality — Focus research on minimizing transcription latency and noise resilience for in-field recordings.\""
    },
    {
      "dimension": "handoff_specificity",
      "score": 8,
      "finding": "Handoffs name specific artifacts and roles, though 'Engineering' should be a precise role title."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "Anti-patterns section is missing entirely, leaving no guidance on what to avoid.",
      "example_rewrite": "Anti-Patterns:\n- Avoid Benchmark Overfitting: \"Don't optimize solely for paper metrics; focus on real-world transcription accuracy under noisy conditions.\"\n- Avoid Unvalidated Hype: \"Don't adopt new models without cross-validation on Story Portal datasets.\"\n- Avoid Knowledge Silos: \"Don't withhold insights; always publish results to the research wiki.\""
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "Deployment notes clearly define AI vs human responsibilities and iteration loops."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 9,
      "finding": "The appendix aligns research areas, priorities, and festival context specifically to Story Portal needs."
    }
  ],
  "top_improvement": "Add a dedicated, role-specific anti-patterns section with concrete examples to guide research best practices."
}