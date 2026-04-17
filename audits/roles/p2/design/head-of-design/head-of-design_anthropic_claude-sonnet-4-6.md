```json
{
  "role": "head-of-design",
  "department": "design",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 3,
    "anti_pattern_quality": 3,
    "ai_deployment_clarity": 2,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic design leadership platitudes that could appear in any design role at any company. 'User-Centered Everything', 'Excellence Is Non-Negotiable', and 'Craft Matters' carry no operational meaning specific to Story Portal or this role's actual context. There is no principle that reflects the steampunk aesthetic constraint, the small-team reality, the festival deadline pressure, or the tension between design vision and startup velocity.",
      "example_rewrite": "Replace generic principles with role-specific ones. Example: 'Steampunk Warmth Over Polish' — Story Portal's design language favors warmth and wonder over clean minimalism; when in doubt, choose the detail that delights over the layout that scales. Or: 'Vision at Speed' — with a small team and festival deadlines, design direction must be decisive; a good decision today beats a perfect decision after the sprint ends."
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs name roles but the artifacts are vague to the point of being useless. 'Receives: Company strategy from CEO' and 'Delivers: Vision, direction, standards to Design Team' do not specify what physical or digital artifact changes hands, in what format, at what cadence, or what triggers the handoff. An AI agent or a new hire cannot act on these. No artifacts like 'Design Principles v1.2 Figma doc', 'Quarterly Design OKRs deck', or 'Design Review Feedback document' are named.",
      "example_rewrite": "Receives From CPO: 'Product Roadmap (Notion doc, updated each sprint planning) — triggers Design Strategy Workflow'. Delivers To Design Team: 'Design Principles Document (Figma cover + Notion reference, reviewed quarterly) and Sprint Design Brief (Notion, issued each Monday before sprint kickoff)'. Delivers To Executive Team: 'Design Health Report (Slides, monthly, covers system adoption %, user satisfaction delta, and open accessibility blockers)'."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 3,
      "finding": "The DON'T list contains 5 items but they are boundary statements, not anti-patterns. Anti-patterns should describe failure modes this specific role actually falls into — behaviors that feel correct but cause harm. 'Dictate product strategy' is a boundary violation, not an anti-pattern. There are no anti-patterns specific to a Head of Design at a small steampunk story platform, such as over-investing in system documentation at the expense of shipping experiences, or letting aesthetic perfectionism block festival-critical features.",
      "example_rewrite": "Anti-Pattern: 'System Before Story' — spending sprint cycles refining the steampunk design token library while Wheel and Recording UI remain unpolished. The system exists to serve the experience, not precede it. If a component decision is blocking a feature that ships before the festival, ship the feature with a local solution and backlog the system update. Anti-Pattern: 'Review Bottleneck' — inserting Head of Design approval into every design decision. With a small team, this creates a single-point-of-failure. Establish design principles strong enough that designers can self-approve routine work."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 2,
      "finding": "The Context Requirements section — the most critical section for AI deployment — contains literal placeholder text: '[Context item 1]' and '[Context item 2]', and the Required Skills table is entirely empty with only a format hint. This means an AI agent loading this role has no idea what context files to load, what skills to activate, or what its first action should be. The Hybrid deployment notes say AI 'assists with research' and 'helps draft communications' but give zero specificity about which tasks, which formats, or which triggers activate AI assistance.",
      "example_rewrite": "Required Context: [ ] story-portal-design-system.md — load before any design review task. [ ] story-portal-brand-guidelines.md — load before any vision or communications task. [ ] current-sprint-roadmap.md — load before any strategy or prioritization task. Required Skills: design-critique.md → load when conducting design reviews. executive-communication.md → load when preparing leadership updates. Required AI Actions: When asked to draft design feedback, output structured Situation / Observation / Recommendation format. When asked to assess design quality, reference the steampunk design principles doc before responding."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix names the right aesthetic (steampunk-inspired warmth) and lists 5 priorities, which is a good start. However, the priorities are not actionable — 'Wheel experience polish' gives no definition of done, no success metric, no current state, and no indication of what 'polish' means in steampunk terms. The table entries read like backlog items copied without context. There is no mention of the festival deadline, team size constraints, or which priorities are blocked versus active.",
      "example_rewrite": "Design Priorities (Story Portal) — Priority 1: Wheel Experience Polish. Current state: Spin animation exists but lacks tactile feedback cues and the result reveal feels abrupt. Definition of done: Haptic-analog motion curve applied, result card uses aged-parchment reveal transition, tested with 3 users before festival. Owner: Lead Product Designer. Status: In progress, targeting sprint 4. Blocked by: None. Priority 2: Recording UI Clarity. Current state: Users misidentify the record button as decorative due to steampunk styling. Definition of done: Iconography passes 5-second usability test with new users while retaining aesthetic."
    }
  ],
  "top_improvement": "Complete the Context Requirements section immediately — it contains literal placeholder text which makes this role non-deployable for an AI agent. Define the 3-5 specific context files that must be loaded (design system doc, brand guidelines, sprint roadmap), specify which skills activate for which task types, and replace the vague AI assistance notes with concrete trigger-action pairs. Until this section is real, the Hybrid deployment classification is misleading because the AI half of the hybrid cannot function."
}
```