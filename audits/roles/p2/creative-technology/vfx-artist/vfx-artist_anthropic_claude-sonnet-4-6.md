```json
{
  "role": "vfx-artist",
  "department": "creative-technology",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 6,
    "anti_pattern_quality": 8,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "All 6 principles are present and most are VFX-specific. 'Reference Is Everything' and 'Feel Before Fidelity' are genuinely craft-specific. However, 'Iterate Relentlessly' and 'Partner with Engineering' are near-generic — they could appear in any creative or product role without modification. The table format also strips nuance; no principle explains *when* it overrides another (e.g., does 'Constraints Breed Creativity' ever yield to 'Feel Before Fidelity'?).",
      "example_rewrite": "Replace 'Iterate Relentlessly' with: **'Frame-Level Precision** — Feedback without a timestamp is noise. Every design note cites a specific frame, reference clip, or parameter. If you cannot point to the exact moment something fails, the note is not ready to send.' This is VFX-specific, actionable, and non-obvious."
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The handoff table names real artifacts (effect specification, mood board, timing requirements) and real roles, which is good. Two gaps lower the score: (1) The 'Receives From' row lists 'Product/Design' as an origin role, but no such role exists by that name in the visible charter — it should map to a specific charter role. (2) The handoff to Motion Designer ('Effect timing requirements') is underspecified — there is no named document format, file type, or schema, making it ambiguous whether this is a Notion doc, a Figma annotation, or a timing curve export.",
      "example_rewrite": "Change the Motion Designer handoff row to: | Motion Designer | `effect-timing-brief.md` — includes effect duration (ms), easing curve name (e.g., ease-out-cubic), trigger event, and loop behavior. Delivered in Notion before animation pass begins. |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 8,
      "finding": "Six anti-patterns are present and most are role-specific. 'Dictate implementation' and 'Skip references' are distinctly VFX Artist problems that would not appear in, say, a Motion Designer or UI Designer role. 'Vague feedback' has a strong example contrast (✓/✗ format in Workflow 2) that reinforces it. Minor deduction: 'Approve good enough' is slightly generic — nearly every creative role could list this. It would score higher if tied to a VFX-specific failure mode, such as approving an effect that looks correct in isolation but loses impact at real UI scale or frame rate.",
      "example_rewrite": "Replace 'Approve good enough' with: **'Review at Wrong Fidelity** — Approving an effect from a screen recording or compressed export masks banding, timing drift, and glow clipping. Always review on target hardware at native resolution before signing off. A Loom at 720p is not an approval artifact.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "This is the strongest dimension. The role clearly separates AI-executed actions from human approval gates, the STOP points in Workflow 1 are explicit, the feedback example with ✓/✗ contrast gives the agent a behavioral model, and the Browser deployment rationale is well-reasoned. One gap: the Context Requirements section lists skill files to load (steampunk-design-system.md, animation-standards.md) but does not specify *what question or decision* each file answers. An agent loading this cold would not know when to consult each file mid-workflow.",
      "example_rewrite": "Update the Required Skills table: | `steampunk-design-system.md` | Load before any color or aesthetic decision on Story Portal effects — contains the approved palette, material language, and 'forbidden' aesthetic directions. | | `animation-standards.md` | Load before writing timing specs or reviewing implementations — defines acceptable easing curves, minimum frame durations, and the AAA quality benchmark the studio uses. |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The appendix is genuinely specific: a named effect (Electricity Portal), a defined aesthetic ('Tesla coil meets ancient portal'), hex values for a four-stop color palette, and a reference to the SSIM-based iteration pipeline. This is meaningfully above generic. Two gaps prevent a higher score: (1) 'Current State' says implementation is 'in progress' but does not say what iteration number, what is blocking, or what the next human decision point is — an agent loading this mid-project has no orientation. (2) Film references (Doctor Strange, Tesla imagery) are named but not linked or annotated, so the agent cannot distinguish which quality from each reference is target-relevant.",
      "example_rewrite": "Expand Current State to: 'Current State: Iteration 4 of electricity shader. Core bolt structure approved. Blocking issue: glow bloom is clipping on dark backgrounds — WebGL Engineer needs direction on falloff radius. Next human gate: stakeholder review of Iteration 5 before mobile performance pass. Reference annotation: Doctor Strange portal — capture the *rotational energy and layering*, not the blue palette. Tesla imagery — capture *irregular branching and taper*, not the static discharge shape.'"
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix: the 'Receives From: Product/Design' entry references a role name that does not appear in the charter, and the Motion Designer handoff lacks a named document format. In a live multi-agent system, these two gaps are the most likely to cause a broken handoff chain — the agent will not know who to wait on or what file to produce. Resolve by mapping every handoff to a charter-verified role name and a named, typed artifact (filename pattern + format + delivery location)."
}
```