```json
{
  "role": "analytics-operations-manager",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 6,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Several principles (e.g., \"Continuous Improvement\") are generic and lack actionable context for analytics operations.",
      "example_rewrite": "**Continuous Improvement:** Conduct bi-weekly retrospectives on tool incidents, publish a quarterly operations health report, and update runbooks within 48 hours of each incident."
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "'All Teams' is too broad. Handoffs should name specific roles and artifacts rather than catch-all groups.",
      "example_rewrite": "| Delivers To             | Artifact                              |\n|-------------------------|---------------------------------------|\n| Data Analysts           | Weekly dashboard performance report   |\n| Data Engineers          | Provisioned access logs and RBAC matrix |\n| Head of Data & Analytics | Monthly operations summary presentation |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "The role file omits any anti-patterns. Without role-specific cautions, users may repeat common mistakes like over-provisioning access.",
      "example_rewrite": "## Anti-Patterns\n\n- **Over-Provisioned Roles:** Granting broad access to reduce requests leads to PII exposure. Always follow least-privilege.\n- **Ignoring Audit Alerts:** Dismissing automated audit failures delays breach detection. Treat every alert as a potential security incident.\n- **Unversioned Runbooks:** Updating processes without version control increases recovery time. Use Git for all runbooks and tag each release."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The appendix lists general operations priorities but doesn’t tie them to Story Portal workflows or projects.",
      "example_rewrite": "### Story Portal Operations Priorities\n| Priority | Focus                                             |\n|----------|---------------------------------------------------|\n| 1        | Ensure Metabase story-triage dashboard uptime > 99.9% |\n| 2        | Automate Segment event schema enforcement for story creation events |\n| 3        | Implement consent audit for Story Portal PII fields in dbt models  |\n| 4        | Run weekly enablement workshops for data-plugin developers       |"
    }
  ],
  "top_improvement": "Define and include 3–5 role-specific anti-patterns to highlight common operational mistakes."
}
```