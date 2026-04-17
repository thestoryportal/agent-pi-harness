```json
{
  "role": "chief-operating-officer",
  "department": "operations",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 6,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "The six principles are generic platitudes (e.g., “Efficiency Is Everything”) without concrete, role-specific guidance.",
      "example_rewrite": "| Principle                  | Meaning                                                   |\n|----------------------------|-----------------------------------------------------------|\n| **Vendor Efficiency Focus**| Ensure 98% SLA compliance and negotiate quarterly reviews |\n| **Scale-through-Automation**| Automate 60% of recurring tasks by Q2 2025               |\n| **Uptime as Priority**     | Maintain 99.9% system availability month over month       |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Uses “All Departments” and vague artifact names instead of specifying actual roles and deliverables.",
      "example_rewrite": "| Receives From      | Artifact                        |\n|--------------------|---------------------------------|\n| CPO (Product)      | New feature launch checklist    |\n| CTO (Technology)   | Monthly uptime & incident report|\n| Marketing Head     | Campaign readiness requirements |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No Anti-Patterns section is defined; missing role-specific pitfalls like “Process Paralysis” or “Vendor Overdependence.”",
      "example_rewrite": "## Anti-Patterns\n\n- **Process Paralysis**: Over-engineering every workflow and delaying execution.\n- **Vendor Overdependence**: Failing to diversify suppliers, leading to single-point failures.\n- **Data Hoarding**: Collecting metrics without actionable review cycles.\n- **Scope Creep**: Allowing ad hoc requests to expand process boundaries without governance."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "AI role is described only at a high level; lacks specific tasks, data sources, thresholds, and workflows for the AI component.",
      "example_rewrite": "### AI Responsibilities\n- Ingest ProcessMetricsDB daily and flag >10% deviation from KPI thresholds.\n- Generate weekly “Process Improvement Scorecard” PDF and email to COO@company.com.\n- Run vendor performance analysis each month and auto-suggest contract renegotiations when SLA < 95%."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "Story Portal appendix lists focus areas but doesn’t tie them to specific actions, metrics, or timelines.",
      "example_rewrite": "| Area                  | Action Item                                    | Success Metric                          |\n|-----------------------|------------------------------------------------|-----------------------------------------|\n| Festival Operations   | Deploy mobile POS units by D-30                 | <2% transaction downtime at event       |\n| Platform Operations   | Implement auto-scaling rules for peak traffic   | <1 minute response time under 10k RPS   |\n| Community Operations  | Launch 24/7 ticketing chatbot                   | ≤1 hour resolution for 80% community tickets |\n| Partner Operations    | Quarterly enablement workshops for top 5 partners | 90% partner satisfaction in post-survey |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific pitfalls (e.g., “Process Paralysis,” “Vendor Overdependence”) to guide avoidable mistakes."
}
```