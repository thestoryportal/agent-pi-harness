{
  "role": "cap-table-manager",
  "department": "finance-investor-relations",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 8,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Principles are present but still generic; they lack concrete, role-specific guidelines such as handling reconciliation failures or edge-case triggers.",
      "example_rewrite": "Accuracy Is Critical: Run daily cap table reconciliation by 9 AM, log any variance over 0.1% in the audit trail, and automatically alert the CFO with root-cause analysis."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No anti-patterns are defined; missing common pitfalls like stale data imports, forgotten vesting updates, or unvalidated scenario assumptions.",
      "example_rewrite": "Anti-Pattern: Stale Cap Table Snapshot — Relying on month-end exports causes outdated ownership views; enforce hourly data syncs and automated validation checks after each import."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is descriptive but does not map cap table activities to actual portal stories, tasks, or triggers.",
      "example_rewrite": "Story Portal Task: Round Modeling — After a funding round closes, create story CAP-102 in Story Portal, attach the updated cap table CSV and dilution chart, and assign to the Investor Relations lead."
    }
  ],
  "top_improvement": "Define and document anti-patterns specific to cap table management to prevent common data and process errors."
}