{
  "role": "financial-controller",
  "department": "finance-investor-relations",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 8,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Principles are broad and generic; lack measurable, role-specific targets (e.g. close deadlines, materiality thresholds).",
      "example_rewrite": "| Principle               | Meaning                                                                          |\n|-------------------------|----------------------------------------------------------------------------------|\n| **Close in 5 Days**     | Complete the monthly close and issue trial balance by the 5th business day.       |\n| **Flag >0.5% Variance** | Investigate and document any line-item variance over 0.5% within 2 business days.|"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No anti-patterns provided; teams have no guidance on what to avoid in this role.",
      "example_rewrite": "- **Delayed Reconciliations**: Waiting beyond day 10 creates backlog and error risk.\n- **Over-Reliance on Spreadsheets**: Manual Excel consolidation without controls leads to version chaos.\n- **Snapshot Reporting**: Generating one-off reports without archived templates causes inconsistency."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "AI responsibilities are high-level; lacks explicit tasks, thresholds and handoff triggers for autonomous agents.",
      "example_rewrite": "Workflow Step ‘PROCESS’: \n- **AI Task**: Auto-classify 100% of GL transactions within 1 hour of posting, flagging any unrecognized vendors.\n- **AI Task**: Generate draft trial balance and highlight variances >0.5% for human review."
    }
  ],
  "top_improvement": "Define anti-patterns specific to the Financial Controller role to guide the team on what practices to avoid."
}