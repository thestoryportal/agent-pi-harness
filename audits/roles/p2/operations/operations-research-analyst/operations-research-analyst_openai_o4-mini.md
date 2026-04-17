{
  "role": "operations-research-analyst",
  "department": "operations",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 6,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "The six principles are high-level platitudes (e.g. “Efficiency Focus”) rather than specific statements tied to the Operations Research Analyst’s unique remit.",
      "example_rewrite": "| Principle                          | Meaning                                                        |\n|------------------------------------|----------------------------------------------------------------|\n| **Order-to-Delivery Optimization** | Reduce average order fulfillment time by 15% each quarter.    |\n| **Data-Driven Bottleneck ID**      | Use process mining to detect top 3 daily constraints by 5 PM. |\n| **Quarterly Best-Practice Score**   | Benchmark against top 3 peers and raise our score by 10%.     |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Handoffs list generic artifacts like “operational data” instead of named deliverables and versions, making downstream expectations vague.",
      "example_rewrite": "| Delivers To      | Artifact                               |\n|------------------|----------------------------------------|\n| COO              | Q1 Operational Efficiency Dashboard v1.0 |\n| Process Manager  | Bottleneck Analysis Report – Feb 2025   |\n| Operations Team  | Weekly Anomaly Alert Bulletin (v2.3)    |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "The role file omits a dedicated Anti-Patterns section. There are no role-specific warnings about common analytical missteps.",
      "example_rewrite": "## Anti-Patterns\n\n1. Ignoring seasonal variance in demand analysis — leads to false efficiency gains.\n2. Treating correlation as causation in bottleneck identification.\n3. Overloading dashboards with every metric instead of focusing on top-5 KPIs.\n4. Failing to validate data extracts from legacy systems before reporting."
    }
  ],
  "top_improvement": "Add a role-specific Anti-Patterns section detailing 3–5 common analytical missteps"
}