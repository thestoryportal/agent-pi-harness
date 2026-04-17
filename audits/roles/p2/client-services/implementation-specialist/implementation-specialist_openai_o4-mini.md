```json
{
  "role": "implementation-specialist",
  "department": "client-services",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 8,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "The six principles are generic platitudes without concrete, measurable guidance.",
      "example_rewrite": "Replace “Documentation Discipline” with “Use the ‘Five Ws’ template to record setup decisions in Confluence within 24 hours of each configuration change.”"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No anti-patterns are defined; the role lacks guidance on common implementation pitfalls.",
      "example_rewrite": "Add: “Anti-Pattern: Skipping data validation – bypassing quality checks on migrated records leads to reporting errors and client frustration.”"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix lists areas but doesn’t specify actionable steps or reference actual Story Portal tools.",
      "example_rewrite": "For Festival Integration, specify: “Run `sp-cli festival import --file festival_schedule.csv` to create sessions, then trigger email invites via `sp-api send-invite --template festival_invite.json`.”"
    }
  ],
  "top_improvement": "Define a concise, role-specific anti-patterns section with 3–5 concrete bad practices and remedies."
}
```