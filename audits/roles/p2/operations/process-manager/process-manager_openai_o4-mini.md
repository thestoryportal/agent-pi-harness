{
  "role": "process-manager",
  "department": "operations",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 7,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No anti-patterns section is present; missing 3–5 role-specific anti-patterns to warn against common pitfalls.",
      "example_rewrite": "Anti-Patterns:\n1. Over-engineering Flows: Adding unnecessary steps for minor tasks, e.g., 10-step approval for small budget requests.\n2. Siloed Optimization: Improving one department’s process without end-to-end alignment, causing handoff delays.\n3. Metric Myopia: Focusing only on cycle time reduction at the expense of quality or compliance.\n4. Change Fatigue: Rolling out too many process updates too quickly, leading to stakeholder resistance.\n5. Documentation Drift: Letting maps and guides become outdated by neglecting regular reviews."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "AI assistance guidelines are high-level; lacking specific prompts, data inputs, or decision thresholds for analysis and documentation tasks.",
      "example_rewrite": "AI Deployment Details:\n- Analysis Assistant: \"Prompt: Analyze process_map_v1.csv and highlight top 3 bottlenecks by average wait time >10 days.\"  
- Documentation Generator: \"Prompt: Using the approved future_state_diagram.pptx, produce step-by-step SOP in Confluence format with section headers and examples.\"  
- Metric Tracker: \"Task: Every Monday at 9 AM, query the process_performance_db for cycle_time, error_rate; if cycle_time > SLA, alert Process Manager via Slack.\""
    }
  ],
  "top_improvement": "Add a dedicated anti-patterns section with 3–5 specific cautions to guide the Process Manager away from common missteps."
}