{
  "role": "legal-research-analyst",
  "department": "legal-compliance",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 6,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The handoff section uses generic terms like 'Legal Team' and 'External Sources' without naming specific roles or defining precise artifacts.",
      "example_rewrite": "| Receives From           | Artifact                         |\n|-------------------------|----------------------------------|\n| Regulatory Affairs Mgr. | Regulatory Change Request Form   |\n| Research Director       | Methodology Update Document      |\n\n| Delivers To             | Artifact                         |\n|-------------------------|----------------------------------|\n| General Counsel         | Formal Research Memo (PDF)       |\n| Compliance Officer      | Regulatory Impact Assessment XLS |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no Anti-Patterns section; missing role-specific pitfalls leads to ambiguity about what to avoid.",
      "example_rewrite": "## Anti-Patterns\n\n1. **Outdated Source Reliance** – Relying solely on secondary analyses rather than current statutes or opinions.\n2. **Jurisdictional Overreach** – Applying case law from one jurisdiction without confirming local applicability.\n3. **Volume over Clarity** – Dumping all findings without distilling to actionable insights.\n4. **Alert Fatigue** – Pushing every minor regulatory notice instead of prioritizing high-impact changes.\n5. **Unvalidated Summaries** – Publishing synthesis without human validation checkpoints."
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3–5 role-specific pitfalls to guide proper conduct and avoid common errors."
}