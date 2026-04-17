{
  "role": "head-of-data-analytics",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 6,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "The six principles are high-level platitudes (e.g. “Quality Is Foundation”) rather than role-specific, actionable mantras.",
      "example_rewrite": "Replace “Quality Is Foundation” with “Trust Through Provenance: embed automated lineage and certification checks into every data pipeline to ensure verifiable data quality.”"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Handoffs reference generic groups like “Executive Team” and “All Departments” without naming specific roles or deliverable formats.",
      "example_rewrite": "Receives from CTO: ‘Data Platform Architecture Document (Confluence link)’; Delivers to Chief Marketing Officer: ‘Weekly Engagement Dashboard (Tableau workbook).’"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "No anti-patterns section is provided; role-specific pitfalls (e.g. data silos, over-engineering dashboards) are missing.",
      "example_rewrite": "Add an Anti-Patterns section: 1) ‘Data Hoarding: centralizing everything in a single lake without governance prevents data discoverability.’ 2) ‘Dashboard Sprawl: creating isolated reports for each team leads to inconsistent metrics.’"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3–5 role-specific pitfalls and remediation guidance."
}