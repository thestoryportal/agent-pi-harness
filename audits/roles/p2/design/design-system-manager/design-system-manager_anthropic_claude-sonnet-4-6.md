```json
{
  "role": "design-system-manager",
  "department": "design",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 5,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "The 6 principles are directionally relevant to a design system role, but most collapse into tautologies. 'Single Source of Truth' and 'Consistency Through System' say nearly the same thing. 'Documentation Is Product' and 'Adoption Is Success' are widely repeated design system mantras, not differentiated beliefs. Only 'Design + Dev Parity' and 'Evolve, Don't Ossify' gesture at real operational tension. None articulate HOW the role resolves conflict — e.g., when adoption pressure clashes with system integrity.",
      "example_rewrite": "Replace 'Single Source of Truth — One system, everywhere' with: 'Divergence Is Technical Debt — Every one-off component created outside the system is a future migration cost. The Design System Manager tracks divergence as debt, not exceptions, and schedules reconciliation sprints rather than accepting drift silently.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff tables name roles but describe artifacts at the wrong level of abstraction. 'New component designs' and 'Component specs' are categories, not artifacts. No file formats, naming conventions, or delivery states are specified. 'All Designers' is not a role — it is an audience. 'Engineering' is not a role. The Accessibility Specialist appears in Works With but is absent from all handoff rows, which is a significant omission for a component-producing role. Receives-From also references 'Visual/Brand Designer' but that role name does not match the Boundaries table which says 'Visual/Brand Designer' — minor inconsistency that signals copy-paste drift.",
      "example_rewrite": "Replace 'Frontend Developer | Component specs' with: 'Frontend Developer | Figma component spec sheet (component-name.fig) including: all variant/state frames labeled with prop names, redline annotations, token references by name (e.g. color/interactive/primary), and WCAG notes. Delivered via Figma share link in the component's GitHub issue before dev branch is opened.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no Anti-Patterns section in this role file. The template standard explicitly requires 3-5 role-specific anti-patterns. The DON'T list in Boundaries is a boundary statement, not an anti-pattern list. Anti-patterns describe failure modes the role itself might fall into — behaviors that look like good work but produce bad outcomes. None are present. This is the most significant structural gap in the file.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: '**Componentizing Too Early** — Abstracting a pattern into a system component before it has appeared in 3+ distinct product contexts creates premature API contracts that calcify bad assumptions. Symptom: components with a single known consumer. Fix: document as a local pattern first, promote to system only after second confirmed use case. **Token Proliferation** — Adding new tokens for each designer request rather than mapping to existing scale. Symptom: 47 shades of gray with names like color-gray-button-hover-disabled. Fix: require token requests to show why existing scale cannot satisfy the need. **Spec Without Conversation** — Delivering component specs to Frontend Developer without a sync call. Symptom: implementation reviews flag 8+ discrepancies per component. Fix: schedule a 20-min kickoff per new component before Figma handoff.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Deployment Notes section states AI generates documentation and checks consistency, but provides no operational instructions for how an AI agent should behave in practice. The Iteration Protocol loop is present (satisfying the Hybrid checklist item) but is completely generic — identical to what would appear in any Hybrid role. The Context Requirements section is left as unfilled placeholders ('[Context item 1]', '[Context item 2]') and the Skills table has no entries. An AI agent loading this role cannot determine what context files to load, what its first action should be, or what 'checking consistency' means operationally.",
      "example_rewrite": "Replace the placeholder Context Requirements with: 'Required Context: [ ] steampunk-design-system.md — load before any token or component task [ ] component-inventory.md — load before assessing new component requests [ ] design-dev-parity-log.md — load before any sync review. Required Skills: | token-naming-conventions.md | Load when creating or auditing tokens | | wcag-aa-checklist.md | Load when documenting or reviewing any component | | storybook-story-format.md | Load when writing component documentation for Storybook |'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix names the steampunk design system and references a real context file (steampunk-design-system.md), which is meaningful. The prioritized list of 5 focus areas is actionable. However, the token/component status table uses vague states ('Established', 'Core complete', 'In progress') with no definition of what those states mean operationally. 'Storybook: Planned' with no owner or timeline provides no guidance. The appendix does not connect Story Portal priorities back to the workflows defined earlier in the file — there is no indication that Workflow 1 (New Component) should be run against the 'Component inventory' priority, for example.",
      "example_rewrite": "Extend Priority 2 entry: '2 | Component inventory — Run Workflow 1 (New Component) for each component in the steampunk-design-system.md that lacks a Figma frame in the library. Target: 10 core components audited and specced before Storybook setup begins. Blocking dependency for Priority 4.'"
    }
  ],
  "top_improvement": "Add a role-specific Anti-Patterns section with 3-5 named failure modes unique to design system work (e.g., premature componentization, token proliferation, spec-without-conversation). This section is entirely absent and is the largest structural gap relative to the template standard — it cannot be partially credited from any existing content in the file."
}
```