{
  "role": "user-research-lead",
  "department": "research-intelligence",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 8,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "No anti-patterns section is present; without 3–5 role-specific anti-patterns, the role lacks guardrails against common mistakes.",
      "example_rewrite": "- Anti-Pattern: 'Opinion over Evidence' — Jumping to conclusions without systematic data analysis.\n- Anti-Pattern: 'Tool Overuse' — Letting AI transcription or analytics replace direct engagement.\n- Anti-Pattern: 'One-Off Research' — Treating each study in isolation instead of synthesizing learnings.\n- Anti-Pattern: 'Gut-Check Approval' — Skipping peer review of methodologies before fieldwork."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The AI’s role is described at a high level but lacks precise tasks, tool names, input/output formats, and success criteria for each step.",
      "example_rewrite": "AI Assistants:\n- Transcription Agent: Use Otter.ai API to transcribe interviews within 30 minutes of sessions.\n- Thematic Analysis Bot: Run NLP topic modeling (via spaCy) on transcripts to generate initial codebook.\n- Report Drafter: Populate slide deck template with key quotes, themes, and visual journey maps in Confluence."
    }
  ],
  "top_improvement": "Add a dedicated anti-patterns section with 3–5 role-specific anti-patterns to provide clear guardrails and prevent common research pitfalls."
}