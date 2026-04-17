{
  "role": "prompt-engineer",
  "department": "ai-automation",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 5,
    "anti_pattern_quality": 6,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 3
  },
  "findings": [
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Uses generic terms like “Any role” and “Requester” rather than naming specific stakeholders or prompt consumers, and does not specify delivery formats.",
      "example_rewrite": "| Receives From       | Artifact                   | Format     |\n|---------------------|----------------------------|------------|\n| Content Writer      | Draft blog prompt         | MD file    |\n| Data Analyst        | Reporting prompt spec     | JSON schema|\n| HR Department       | Role template for review  | DOCX       |\n| Project Lead        | New prompt requirements   | JIRA ticket|"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 6,
      "finding": "Anti-patterns are generic (“Please kindly…”, “Try to…”) and miss role-specific pitfalls like over-nesting instructions or mis-using stop tokens.",
      "example_rewrite": "| Don't                                           | Why                                   | Instead                                         |\n|-------------------------------------------------|---------------------------------------|-------------------------------------------------|\n| Nest multiple STOP commands without context     | Breaks multi-turn flows               | Use single STOP with clear next-step hint       |\n| Use deeply nested bullet lists                  | Confuses model context window         | Flatten to 2-level lists for readability       |\n| Rely on model’s default chain-of-thought prompts| Uncontrolled verbosity                | Explicitly request “no chain-of-thought” prompt |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 3,
      "finding": "No dedicated Story Portal section – lacks project IDs, navigation links, or how prompts map to stories in the portal.",
      "example_rewrite": "## Story Portal Integration\n\n- Project: AI Content Suite (story-1234)\n- Portal Path: /projects/ai-content/prompts\n- Link to Prompt Library: https://storyportal.company.com/ai-content/prompts\n- Mapping: prompt IDs → story card IDs in JIRA\n- Update protocol: tag prompts with `portal_id` in JSON metadata"
    }
  ],
  "top_improvement": "Add a dedicated Story Portal Integration section that links to project story IDs, portal paths, and mapping conventions."
}