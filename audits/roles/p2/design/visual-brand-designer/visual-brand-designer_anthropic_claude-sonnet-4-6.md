```json
{
  "role": "visual-brand-designer",
  "department": "design",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic brand platitudes that could appear in any design textbook. 'Brand Is Promise', 'Consistency Builds Recognition', and 'Quality Reflects Values' provide zero behavioral guidance specific to this role in this project. They do not tell an agent HOW to make decisions when trade-offs arise — e.g., when distinctiveness conflicts with consistency, or when a marketing deadline pressures quality. None reference steampunk aesthetics, the Story Portal project context, or the hybrid AI-human creative dynamic.",
      "example_rewrite": "Replace generic entries with decision-guiding principles. Example: 'Steampunk Warmth Over Trend' → When modern design trends conflict with the brass/copper/leather aesthetic vocabulary, the established Story Portal visual language wins — no clean sans-serif minimalism, no flat design shortcuts. Or: 'Variation Before Finalization' → Always produce 3 distinct directional concepts before refining; presenting a single option to stakeholders is a scope failure, not a time-saver."
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but fail on artifacts. 'Receives: Brand strategy from Brand Strategist' and 'Delivers: Brand assets to UI Designer' describe categories, not actual documents. There is no mention of file format, naming convention, resolution spec, or delivery location. The 'Marketing Team' entry in Delivers is not a specific role — it is a department, which violates the template standard against vague handoffs. 'Campaign briefs' and 'Social needs' as incoming artifacts are too vague to act on.",
      "example_rewrite": "Receives From Brand Strategist: 'Brand Strategy Brief v[X].pdf — includes approved color palette hex codes, typography stack, tone descriptors, and usage prohibitions. Stored in /brand/strategy/.' Delivers To UI Designer: 'Brand Asset Package — Figma library file (.fig) plus exported SVG/PNG set at 1x/2x/3x, named per convention [asset-name]-[variant]-[size].svg, shared via Figma link with Edit access confirmed before handoff is considered complete.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "This role has NO dedicated anti-patterns section. The DON'T list in Boundaries lists role-boundary violations (don't do UI, don't write copy) but these are ownership rules, not anti-patterns. Anti-patterns should describe failure modes specific to how this role goes wrong — e.g., over-polishing a first concept before direction is validated, or creating assets that look great in isolation but fail at small sizes. The template checklist explicitly requires role-specific anti-patterns and none are present.",
      "example_rewrite": "Add an Anti-Patterns section with entries like: (1) 'Single-Concept Trap' — Presenting one fully rendered concept instead of 3 directional sketches; this forces stakeholders to approve or reject rather than guide, creating revision loops. (2) 'Style Over System' — Designing a beautiful one-off asset that cannot be templated or reproduced by the team; every asset must have a reusable logic. (3) 'Context Collapse' — Approving an asset at full size without testing at 32px favicon, social thumbnail, and print bleed simultaneously."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Context Requirements section contains unfilled placeholders: '[Context item 1]', '[Context item 2]', and the Required Skills table has '[Use placeholder format: skill-name.md]' — these are template scaffolding left in the final file, which is a critical deployment failure. An AI agent loading this role cannot determine what context files to load before starting work. The Iteration Protocol exists and is correct, but without knowing which context files prime the agent with brand guidelines and asset library state, the protocol has nothing to iterate on.",
      "example_rewrite": "Replace placeholders with actuals. Required Context: [ ] brand-guidelines-v2.md — full Story Portal visual standards including color hex codes, type scale, logo clearspace rules. [ ] asset-library-index.md — current inventory of completed/in-progress assets with status. Required Skills: | illustration-systems.md | Load when creating new illustration series to maintain style consistency | | print-spec-reference.md | Load when producing any physical festival materials |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is the strongest section — it names the steampunk theme, lists specific asset statuses, and maps touchpoints. However, the Brand Assets Needed table lists items as 'Needed' with no owner, no deadline context, no format spec, and no priority order. 'Festival signage' could mean a 2-inch table card or a 10-foot banner. The appendix is directionally correct but stops short of being actionable enough for an agent to begin work without further clarification.",
      "example_rewrite": "Expand the Brand Assets Needed table: | Festival Signage | Needed | HIGH — required before festival date | Outdoor vinyl banner 10ft x 4ft + A-frame 24x36in + directional arrows 8x8in | Brass/copper colorway, readable at 20ft | Delivers to: Print Vendor via PDF/X-1a |. Also add a 'Visual Decision Log' entry noting any approved deviations from brand guidelines already made in completed assets, so the agent inherits institutional memory."
    }
  ],
  "top_improvement": "Fill the unfilled Context Requirements placeholders immediately — an AI agent cannot deploy this role without knowing which context files to load, making every other quality improvement irrelevant until the role is actually loadable. Simultaneously add a dedicated Anti-Patterns section, as this is the most complete structural omission: the role currently has no failure-mode guidance whatsoever."
}
```