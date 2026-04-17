{
  "role": "customer-support-specialist",
  "department": "support",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 6,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "Principles are high-level platitudes rather than actionable guidelines tailored to AI-driven support workflows.",
      "example_rewrite": "Replace 'Empathy First' with 'Use sentiment analysis to detect user frustration and adjust responses: apologize within the first message and offer escalation options if no resolution in 2 minutes.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Handoffs list roles and broad artifact names, but lack detailed artifact descriptions like ticket fields or logs.",
      "example_rewrite": "Change 'Technical Support Engineer → Complex issues' to 'Deliver fully documented tickets with error logs, user session transcripts, and reproduction steps to Technical Support Engineer for deep-dive resolution.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "Missing anti-pattern section entirely; no role-specific anti-patterns to prevent common mistakes.",
      "example_rewrite": "Add 'Anti-Patterns: 1. Over-Escalation: Escalating every unknown issue without first consulting the knowledge base. 2. Delayed Acknowledgment: Waiting over 5 minutes to greet chat users. 3. Template Overuse: Sending generic macros without personalization.'"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific anti-patterns to guide AI and human agents on what to avoid."
}