{
  "role": "product-manager",
  "department": "product",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 9,
    "anti_pattern_quality": 5,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "The six principles are standard PM clichés and not tailored to Story Portal or differentiated for this context.",
      "example_rewrite": "• Festival-Metric Outcomes Over Outputs: Prioritize features that drive the ‘Completion rate >70%’ metric rather than shipping generic improvements."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 5,
      "finding": "Anti-patterns are generic PM warnings and lack Story Portal–specific scenarios (e.g. offline recording, consent flow).",
      "example_rewrite": "Don’t ship the PWA offline feature without testing network-drop recovery – instead, run simulated offline sessions to validate reconnection flows."
    }
  ],
  "top_improvement": "Customize anti-patterns to reflect Story Portal–specific risks and scenarios"
}