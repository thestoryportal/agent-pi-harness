{
  "role": "it-manager",
  "department": "operations",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 6,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "The six principles are generic platitudes and lack concrete, role-specific guidance.",
      "example_rewrite": "Principle: “24/7 Uptime Commitment” – maintain ≥99.9% core systems availability by scheduling all maintenance windows outside peak business hours."
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "‘All Departments’ and ‘IT services’ are too vague; handoffs should name specific teams and artifacts.",
      "example_rewrite": "Delivers to Security Engineer → Artifact: “Monthly Vulnerability Assessment Report.”"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "No anti-patterns defined; misses role-specific pitfalls such as firefighting or shadow IT.",
      "example_rewrite": "Anti-pattern: “Firefighting Mode” – repeatedly applying hotfixes without scheduling root-cause analysis and long-term remediation."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "Story Portal appendix lists areas but doesn’t tie to actionable deliverables or timelines.",
      "example_rewrite": "Festival IT: deliver “On-site Network Layout Plan” by Week 2 and conduct load test by Day 3 of the event."
    }
  ],
  "top_improvement": "Define role-specific anti-patterns to surface common IT Manager pitfalls (e.g., “Firefighting Mode”)."
}