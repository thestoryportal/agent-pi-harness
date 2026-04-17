```json
{
  "role": "documentation-specialist",
  "department": "operations",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 8,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Principles are stated too generically and lack actionable specificity tied to documentation workflows.",
      "example_rewrite": "| Principle                  | Meaning                                                                        |\n|-----------------------------|--------------------------------------------------------------------------------|\n| Lifecycle Versioning        | Archive or review docs older than 6 months unless updated in weekly sprints     |\n| Metadata Taxonomy Alignment | Tag docs with standardized metadata across teams for unified search and retrieval |\n| Feedback-Driven Updates     | Integrate user feedback within 3 business days to keep content relevant         |\n| Accessibility Compliance    | Ensure all docs meet WCAG AA standards and include alt-text for images          |\n| Role-Based Navigation       | Organize content by user personas (e.g., engineer, marketer, support)           |\n| Continuous Improvement      | Schedule quarterly audits with contributors to refine style and accuracy        |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No Anti-Patterns section provided; missing role-specific pitfalls like fragmented docs and stale content.",
      "example_rewrite": "## Anti-Patterns\n- Fragmentation Overload: Creating multiple overlapping mini-guides instead of a unified reference leads to redundancy.\n- Stale Content Accumulation: Failing to archive or update legacy docs results in outdated or conflicting information.\n- Terminology Drift: Using inconsistent vocabulary across articles confuses readers; enforce a controlled glossary.\n- Versioning Conflicts: Allowing edits outside the central repo causes merge issues; mandate single-source version control.\n- Template Divergence: Ignoring established templates yields inconsistent formatting; enforce template usage in reviews."
    }
  ],
  "top_improvement": "Introduce a dedicated Anti-Patterns section with 3–5 role-specific pitfalls and remediation guidelines."
}
```