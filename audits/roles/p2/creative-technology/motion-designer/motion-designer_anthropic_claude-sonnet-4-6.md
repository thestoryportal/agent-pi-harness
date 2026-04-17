```json
{
  "role": "motion-designer",
  "department": "creative-technology",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 6,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "All 6 principles are role-specific and actionable. 'Timing Is Feeling' and 'Test in Context' are genuinely craft-specific rather than generic. Minor deduction because 'Iterate Quickly' could appear in any creative role without modification — it lacks motion-specific grounding (e.g., no mention of why motion iteration differs from static design iteration, such as the need to feel timing in real-time rather than inspect a frame).",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The handoff tables name roles and artifacts, which is good. However, the 'Receives From' column is vague in critical places. 'Motion Design Lead: Direction, pattern guidance, feedback' is not an artifact — it's a category of conversation. There is no named document, file, or deliverable format specified for what the Motion Design Lead actually passes. Similarly, 'UX Designer: Interaction flows, user context' does not specify format (e.g., Figma flow file, Notion spec, verbal briefing). An AI agent cannot know what to look for or request.",
      "example_rewrite": "| Motion Design Lead | `motion-system-v{n}.md` (token reference), Figma component file with motion annotations, verbal/written assignment brief specifying which UI component or flow to animate |\n| UI Designer | Figma file link with finalized static designs, component states labeled (default, hover, active, disabled), any design notes flagging motion-sensitive moments |\n| UX Designer | Interaction flow document (Figma or Notion) identifying trigger events, user goals per screen, and any usability constraints that affect animation timing |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Most anti-patterns are role-specific. 'Arbitrary timing values' and 'Skip reduced-motion' are genuinely motion-designer problems, not copy-paste from a generic creative role. The table format with Why and Instead columns is well-structured. Minor deduction: 'Polish before validation' is common to all creative roles and its motion-specific articulation is missing — it does not explain why motion polish is particularly wasteful (e.g., a polished prototype in After Effects may be impossible to replicate in CSS, making the polish irrelevant). One entry ('Ignore context') is borderline generic without a motion-specific example.",
      "example_rewrite": "| Over-polish prototype before validation | Motion polished in After Effects may be technically unachievable in CSS/JS at 60fps — effort is wasted and creates false expectations with stakeholders | Build lowest-fidelity prototype that communicates timing feel (even a simple CSS transition in DevTools), validate the feel first, then refine the artifact |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 9,
      "finding": "This is the strongest dimension. The Hybrid classification is correctly applied and explained. The STOP checkpoint in Workflow 1 Step 5 is explicit. Workflows have named triggers, sequential steps, and clear escalation paths. The AI agent knows what it executes versus what humans approve. The Motion Specification Format section with a fully worked example (Button Press Feedback) gives an AI agent an immediate output template. Minor deduction: the 'Required Skills' section references `steampunk-design-system.md` and `animation-standards.md` but these are framed as skills to 'load' — the instruction on how or when to load them mid-workflow is absent, which could cause an AI agent to proceed without necessary context.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix is project-specific and actionable — the motion token table, the six named animations with status, and the steampunk motion feel guidelines are genuine project context rather than filler. The steampunk descriptors ('Mechanical weight,' 'No digital snappiness') give an AI agent tonal direction that affects design decisions. Deduction: all six animations in the Key Animations table have status 'Define' with identical one-line notes. This provides no differentiation about priority, which component to tackle first, or which are blocking other roles. An AI agent starting work has no way to sequence tasks from this table.",
      "example_rewrite": "| Animation | Priority | Blocking | Notes |\n|-----------|----------|---------|-------|\n| Button feedback | P0 — immediate | Frontend Developer (all interactive elements blocked) | Apply to all primary/secondary buttons; use `fast` token (100ms); scale 0.97 on press |\n| Recording states | P0 — immediate | UX Designer sign-off pending | Start/active/stop states for the core recording feature; active state needs pulse or breathing loop using `slow` token |\n| Menu open/close | P1 | None | Hamburger menu; consider slight overshoot on open per steampunk feel guidelines |\n| Loading states | P1 | None | Async operations; avoid spinner clichés — explore gear/mechanical metaphor consistent with steampunk theme |\n| Panel transitions | P2 | None | Content panels; use `moderate` token (350-500ms) |\n| Toast/notification | P2 | None | Entry/exit only; ease-out settle on arrival |"
    }
  ],
  "top_improvement": "Handoff specificity: replace the vague 'Receives From' artifact descriptions with named file formats and document titles. An AI agent receiving 'direction, pattern guidance, feedback' from Motion Design Lead cannot know what to request, what to wait for, or when it has sufficient context to begin work. Specifying the actual artifact (e.g., 'motion-system-v{n}.md with token definitions' or 'Figma file with labeled component states') gives the agent a concrete deliverable to locate or request before starting Workflow 1."
}
```