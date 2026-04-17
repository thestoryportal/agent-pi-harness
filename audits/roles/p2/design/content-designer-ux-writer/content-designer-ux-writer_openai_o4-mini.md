{
  "role": "content-designer-ux-writer",
  "department": "design",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 9,
    "anti_pattern_quality": 8,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The role mentions that AI assists with variations and stops for human review but lacks explicit instructions or prompts for the AI agent to follow.",
      "example_rewrite": "In Deployment Notes under AI assists: \"AI TASK: Given the approved feature spec and voice guidelines, generate 3–5 UI copy variations for each element in JSON format {\"element\":..., \"variation\":...}. Include rationale for each. STOP → Provide to human reviewer for selection.\""
    }
  ],
  "top_improvement": "Add explicit, step-by-step AI task instructions and prompt templates so the AI agent knows exactly when and how to contribute."
}