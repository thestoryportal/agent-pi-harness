```json
{
  "role": "organizational-designer",
  "department": "human-resources",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 4,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are one-liner slogans with no operational meaning. 'Structure Enables Strategy' and 'Clarity Reduces Friction' could appear in any management textbook from 1987. None explain HOW this designer applies the principle in a hybrid AI workforce context — which is the entire point of the role. 'Human + AI Integration' simply restates the classification emoji.",
      "example_rewrite": "| **Span of Control Scales Differently for Hybrid Teams** | An AI agent does not fatigue at 8 direct reports. When designing teams that include AI roles, apply a 1 AI agent = 0.3 human equivalent for span calculations, and document the reasoning in the org chart annotation so future designers don't revert to legacy ratios. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Every artifact in both Receives and Delivers tables is a vague noun phrase: 'Design direction', 'Structure requirements', 'Role placement'. None specify format, trigger condition, or what the receiving role does with it. The handoff to Role Engineer says 'Role placement' — placement of what? A list? A chart? A spreadsheet with department, reporting line, and classification? This cannot be acted on.",
      "example_rewrite": "| Delivers To | Artifact | Format | Trigger |\n|-------------|----------|--------|---------|\n| Role Engineer | Role Placement Map | Spreadsheet: role name, department, reports-to, classification (Human/AI/Hybrid), FTE or agent count | After each Structure Design workflow Step 3 STOP is signed off by CHRO |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section at all. The template standard explicitly requires 3-5 role-specific anti-patterns. The DO/DON'T boundary section partially substitutes but only lists ownership violations, not failure modes. An AI agent running this role has no guard rails against common org design mistakes like over-matrixing, shadow hierarchies, or designing structure before strategy is locked.",
      "example_rewrite": "## Anti-Patterns\n| Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **Designing Before Strategy Is Locked** | Structure built on draft strategy requires full redesign when strategy shifts, wasting stakeholder trust | STOP at Workflow 1 Step 1 until CHRO confirms strategy is finalized, not 'directionally set' |\n| **AI Roles Mapped to Human Spans** | Treating 1 AI agent as 1 headcount inflates team size on paper and triggers unnecessary headcount approvals | Use hybrid-adjusted span ratios; annotate AI roles with [AI] tag in all org charts |\n| **Org Chart as Final Artifact** | A chart without interface protocols leaves team connections undefined, creating coordination gaps | Every department boundary on an org chart must link to a corresponding Interface Map before design is marked Done |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Iteration Protocol loop is present but hollow — it says 'Work on design activities' and 'Report on design status' without telling an AI agent what output format to produce, what threshold triggers a STOP, or what 'guidance on priorities' looks like. The Context Requirements section contains unfilled placeholders '[Context item 1]' and '[Context item 2]', and the Required Skills table is entirely blank. An AI agent loading this role cannot determine what context files to load before starting.",
      "example_rewrite": "### Required Context\n- [ ] current-org-chart.md — existing reporting structure baseline\n- [ ] workforce-strategy-brief.md — CHRO-approved strategy doc this design must serve\n- [ ] role-registry.md — master list of all approved roles for placement validation\n\n### Required Skills\n| Skill | When to Load |\n|-------|-------------|\n| org-chart-notation.md | Before any visualization task |\n| hybrid-span-calculator.md | Before any team sizing task |\n| change-communication-template.md | Before Workflow 1 Step 4 |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix names four areas (Festival Operations, Platform Teams, Community, Creative) but provides no actual structural decisions, constraints, or design artifacts specific to Story Portal. 'Festival surge → Temporary structure' is a label, not guidance. An AI agent reading this cannot produce a Story Portal org chart — it has no team names, no known roles, no surge staffing ratios, and no known reporting lines.",
      "example_rewrite": "### Story Portal Design Constraints\n| Area | Known Constraint | Design Implication |\n|------|-----------------|--------------------|\n| Festival Surge | 3 annual events require 40-60% headcount spike over 6-week windows | Design Festival Operations as a standing skeleton team (4 roles) with a pre-approved surge template that activates event-specific contractor and AI agent slots without new CHRO approval |\n| Platform Engineering | Two squads: Content Delivery and Community Platform | Each squad reports to Platform Engineering Lead; shared QA role uses dotted-line to both Squad Leads; document in Interface Map INF-PE-001 |\n| Community Engagement | Spans both organic community and festival attendee engagement | Avoid splitting into two separate departments; design as unified team with sub-tracks to prevent duplicate tooling and conflicting voice |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 3-5 role-specific failure modes. This role has zero anti-patterns documented, which means an AI agent operating in Hybrid mode has no guard rails. The most dangerous missing pattern is 'Designing Before Strategy Is Locked' — in a hybrid workforce context where org changes cascade into AI agent configurations, a premature design wastes significant downstream Role Engineer and Department Head effort. This single addition would also force the author to write with the specificity that would expose and fix the vagueness problems in every other section."
}
```