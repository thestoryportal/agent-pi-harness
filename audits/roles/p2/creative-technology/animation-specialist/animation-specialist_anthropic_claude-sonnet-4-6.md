```json
{
  "role": "animation-specialist",
  "department": "creative-technology",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 6,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "All 6 principles are role-specific and technically grounded. 'Master the Frame' and 'Performance Is Visible' are genuinely unique to this role. Minor deduction: 'Iterate with Measurement' edges toward generic — it could apply to any engineering role without the animation-specific framing. The table format also buries what makes each principle distinctive.",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The receives/delivers tables name roles correctly, but artifacts are dangerously vague. 'Timing specifications, feel direction' from Motion Design Lead could mean anything — a Notion doc, a verbal brief, a Figma prototype, a JSON config. 'Animation utilities' delivered to Frontend Developer doesn't specify format, file location, or what constitutes a complete handoff. An AI agent receiving this role cannot determine when a handoff is complete.",
      "example_rewrite": "| Motion Design Lead | Receives: `motion-spec.md` — a structured document containing: named animation (e.g., 'wheel-snap'), target duration (ms), easing curve descriptor (e.g., 'spring: tension 180, friction 26'), and reference video or SSIM baseline | | Frontend Developer | Delivers: merged PR containing animation hook (e.g., `useWheelPhysics.ts`), exported constants file (`WHEEL_PHYSICS.ts`), and updated `animation-standards.md` with usage example |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Five of the six anti-patterns are genuinely animation-specific ('animate layout properties', 'heavy JS per frame', 'ignore interruption'). However, 'Magic numbers' and 'Over-engineer' are universal software engineering anti-patterns with no animation-specific framing. They read as filler. The table is also missing the most dangerous animation anti-pattern for this specific role: animating wheel physics parameters without SSIM measurement.",
      "example_rewrite": "| Tune physics by feel alone | Subjective parameter drift across iterations destroys consistency — friction: 0.984 vs 0.985 is invisible to the eye but measurable | Run SSIM comparison against approved baseline after every physics parameter change; document delta in PR |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 9,
      "finding": "Exceptionally clear. The Iteration Protocol is present and mandatory, STOP points appear in every workflow, CLI deployment rationale is explicit, the Required Skills table maps skill files to load conditions, and the Development Environment checklist is concrete. An AI agent could load this role and begin work with minimal ambiguity. Minor deduction: the Required Context checklist has no owner specified for each item — the AI doesn't know who to request missing context from.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The Wheel Physics appendix is specific, actionable, and includes actual file paths and parameter values. The quality bar ('AAA video game quality', 60fps) is concrete. Deduction: the SSIM-based iteration pipeline is referenced in Required Skills (`visual-iteration-pipeline.md`) but never connected to the wheel workflow — an AI agent working on wheel animations won't know to invoke SSIM comparison as part of its quality gate, only that the file exists.",
      "example_rewrite": "Add to Wheel Physics section: '**Quality Gate:** After each physics parameter change, run SSIM comparison per `visual-iteration-pipeline.md`. Target SSIM ≥ 0.95 against approved wheel baseline (`/baselines/wheel-spin-approved.png`). Include SSIM score in every review comment to Motion Design Lead.'"
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. Vague artifacts ('timing specifications', 'animation utilities') mean an AI agent cannot determine when a handoff is complete or what to produce. Define each handoff as a named file or structured document with required fields — this prevents the agent from either over-delivering (rewriting things not asked for) or under-delivering (handing off verbally instead of in code)."
}
```