{
  "role": "support-research-analyst",
  "department": "support",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 6,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "The six principles are clear but read as generic platitudes rather than tightly tied to support research specifics.",
      "example_rewrite": "Change “Synthesis Over Volume” to “Synthesis Over Volume: Prioritize high-impact support insights by filtering out low-severity ticket noise.”"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Handoffs use generic terms like “Product” and “Users” instead of precise roles or named artifacts (e.g., ‘Head of Product’ or ‘Raw ticket export’).",
      "example_rewrite": "Delivers To: Head of Product → “Quarterly feature request report (PDF with annotated priority matrix).”"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No anti-patterns section is provided; role-specific pitfalls (e.g., overfocusing on ticket counts instead of root causes) are missing.",
      "example_rewrite": "Anti-Patterns:\n1. “Chasing Volume Over Value”: Prioritizing ticket count spikes without assessing impact.\n2. “Single-Source Analysis”: Relying solely on help desk data and ignoring user interviews.\n3. “Report Dumping”: Delivering raw data without actionable recommendations."
    }
  ],
  "top_improvement": "Define and include role-specific anti-patterns to guide what NOT to do."
}