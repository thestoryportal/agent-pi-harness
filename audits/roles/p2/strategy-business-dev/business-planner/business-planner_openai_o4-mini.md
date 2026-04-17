{
  "role": "business-planner",
  "department": "strategy-business-dev",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 5,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "The six principles are high-level and generic rather than prescribing specific planning behaviors or metrics.",
      "example_rewrite": "| Principle | Meaning |\n|-----------|---------|\n| **Assumptions Are Testable** | Tie each assumption to a data source and review monthly |\n| **Scenario Stress-Testing** | Define at least three stress scenarios and evaluate P&L impact |\n| **Milestone Accountability** | Assign owners and deadlines to every major deliverable |\n"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Artifacts and role interfaces are named broadly (e.g., “Strategic direction”) rather than pointing to concrete documents or versioned deliverables.",
      "example_rewrite": "| Receives From | Artifact |\n|---------------|----------|\n| CSO           | CSO Strategic Objectives Memo v1.2 |\n| CFO           | Quarterly Financial Constraints Report Q1 2025 |\n| Dept Heads    | Department Budget Input Template 2025 |\n"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No anti-pattern section is provided. Role-specific pitfalls like outdated assumptions or analysis paralysis are missing.",
      "example_rewrite": "| Anti-Patterns | Impact |\n|--------------|--------|\n| **Outdated Assumptions** | Plans built on stale data lead to missed targets |\n| **Analysis Paralysis** | Overlong scenario definitions delay decisions |\n| **Single-Source Bias** | Relying on one data input skews projections |\n"
    }
  ],
  "top_improvement": "Add role-specific anti-patterns to guide and warn against common planning pitfalls"
}