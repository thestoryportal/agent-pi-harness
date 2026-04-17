```json
{
  "role": "head-of-creative-technology",
  "department": "creative-technology",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 6,
    "anti_pattern_quality": 6,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "Six principles are present and most are genuinely role-specific. 'AAA Quality Bar', 'Technical Excellence', and 'Show, Don't Tell' are meaningfully differentiated from generic leadership platitudes. 'Design ↔ Engineering Unity' is especially strong for this hybrid role. Minor deduction: 'Craft Matters' and 'Innovation Through Constraints' are slightly abstract and could appear in any creative leadership role without the specific context of WebGL/motion/3D work.",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Handoffs name roles correctly, but the artifacts are too generic on both sides. 'Visual direction, brand guidelines' received from Head of Design could mean a Figma file, a PDF deck, or a verbal briefing — the ambiguity will cause miscommunication at handoff time. Deliverables like 'Effect components, integration specs' to Frontend Developer are similarly vague. No artifact format, naming convention, or file type is specified anywhere.",
      "example_rewrite": "Delivers To: Frontend Developer | Artifact: 'Packaged effect component (e.g., ElectricityPortal.tsx) with co-located README covering props API, performance budget (target <2ms GPU frame time), and a Loom walkthrough video. Checked into /src/components/effects/ branch before handoff is considered complete.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 6,
      "finding": "The anti-patterns table has six entries which meets the minimum, but four of them ('Accept good enough', 'Make decisions in isolation', 'Hoard context', 'Ignore performance') are generic enough to appear verbatim in a Head of Engineering or Head of Design role file. Only 'Over-engineer' and 'Under-invest in R&D' feel specific to a creative technology leader. Missing are role-specific traps like chasing visual trends at the expense of product coherence, or letting WebGL experiments block production timelines.",
      "example_rewrite": "Anti-Pattern: 'Ship visually impressive work that tanks product metrics' | Why: A 200ms first-paint delay from a hero animation is invisible in isolation but catastrophic at scale | Instead: Every effect must pass a 'beauty-to-budget' gate — document the GPU/CPU cost before it enters any user-facing build."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The AI Assistance Model section clearly enumerates what AI does and does not do autonomously, which is the most critical safety information. The Skills to Load table with specific trigger conditions is excellent. Score held at 7 rather than higher because there is no iteration protocol — the template standard explicitly requires one for Hybrid deployment, and this role is classified Hybrid. An AI agent picking up a review task has no documented feedback loop or revision cycle to follow.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The appendix names four concrete priorities, references specific components (Wheel, Electricity Portal), and anchors quality language to real-world references (Sora/Luma, physical installations). The 'Analog soul, digital reach' philosophy tie-in is strong. Score capped at 7 because 'Current State' is a static snapshot with no owner or update cadence — it will become stale and misleading. There are also no STOP points or decision gates specific to Story Portal (e.g., who approves the electricity effect before it ships to production).",
      "example_rewrite": "Add a Story Portal Gate section: 'STOP — Electricity Portal Effect: Before any WebGL shader moves from sandbox to staging, Head of Creative Technology must co-review with WebGL Engineer using the visual-iteration-pipeline.md checklist. Approval recorded in /decisions/electricity-portal-approvals.md. Current reviewer: [name]. Last reviewed: [date].'"
    }
  ],
  "top_improvement": "Add a Hybrid Iteration Protocol section. The role is classified Hybrid deployment but contains no documented revision loop for AI-assisted work. At minimum, define: (1) how many AI-generated drafts are reviewed before a human STOP point is triggered, (2) what artifact format is expected at each checkpoint, and (3) who has final approval authority per work type (e.g., AI can draft quality feedback, but Head of Creative Technology must sign off before it is delivered to a direct report). Without this, an AI agent operating in this role has no guardrails on how far to iterate autonomously."
}
```