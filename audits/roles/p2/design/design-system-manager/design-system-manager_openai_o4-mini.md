{
  "role": "design-system-manager",
  "department": "design",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 9,
    "anti_pattern_quality": 4,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "anti_pattern_quality",
      "score": 4,
      "finding": "The role file lacks a dedicated Anti-Patterns section; anti-patterns are only mentioned generically under workflows rather than as role-specific missteps to avoid.",
      "example_rewrite": "Add an Anti-Patterns section listing concrete missteps, for example:\n- \"Token Sprawl\": introducing undocumented tokens without governance leads to inconsistent styles.\n- \"Component Drift\": allowing unauthorized variant additions outside the system.\n- \"Spec Drift\": failing to update documentation when component APIs change.\n- \"Bypass Governance\": merging token updates without review, breaking backward compatibility."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The AI deployment notes are too high-level; they don’t specify which AI tasks to automate, trigger conditions, or how to integrate with the CLI/CI pipeline.",
      "example_rewrite": "Clarify AI agent responsibilities and triggers, for example:\n```\nAI Agent Tasks:\n  - On commit to `src/tokens/`: run `npm run gen-token-docs` and open a PR with updated docs.\n  - On PR for component changes: execute `npm run lint-design` and post a Slack summary of mismatches.\n  - After merge to `main`: trigger `yarn storybook:build` and publish preview link to #design-system channel.\n```"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with specific design system missteps and concrete examples."
}