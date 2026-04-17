```json
{
  "role": "head-of-design",
  "department": "design",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 6,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "The six principles are high-level and could apply to any design org, lacking Story Portal–specific context.",
      "example_rewrite": "Steampunk Strategy: Embed the Story Portal’s brass-and-gear aesthetic into user flows to differentiate our product at every touchpoint."
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Handoffs list generic artifacts like “vision” and “standards” but don’t name concrete deliverables (e.g., Figma files, token libraries).",
      "example_rewrite": "Delivers To CPO: ‘Annotated Figma mockups of wheel interaction patterns’ and ‘Design System Token JSON export for developer handoff’."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no anti-patterns section; missing role-specific pitfalls to avoid.",
      "example_rewrite": "**Anti-Pattern: Design-by-Committee** — Allowing too many stakeholders to drive visual decisions leads to diluted steampunk coherence and slows approval cycles."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "AI involvement is described broadly; lacks specific AI tasks, prompts, and expected outputs.",
      "example_rewrite": "AI Task: ‘Generate a steampunk moodboard PDF using prompt “Victorian brass, leather textures, gear mechanics”’ and deliver images with annotations for design review."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The appendix ties priorities and aesthetic focus to the Story Portal context and is actionable."
    }
  ],
  "top_improvement": "Add a role-specific anti-patterns section with 3–5 concrete examples to highlight common pitfalls."
}
```