```json
{
  "role": "marketing-designer",
  "department": "marketing",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are generic platitudes that could apply to any designer anywhere. 'Brand Consistency: Every asset reinforces brand' and 'Clarity Wins: Clear design communicates' are circular non-definitions. None of the principles are anchored to Story Portal's specific context, the marketing-vs-brand-system tension this role navigates, or the performance-conversion tradeoffs unique to a marketing designer operating under a separate Head of Design authority.",
      "example_rewrite": "Replace with role-specific principles, e.g.: | **Copy Serves Design, Design Serves Copy** | Never start a layout without final or near-final copy from the Copywriter — retrofitting copy into a finished design degrades both. | **Borrow the Brand System, Never Break It** | Marketing assets adapt the design system defined by Head of Design; when a campaign idea requires a system exception, escalate before executing. | **Conversion Is the Creative Brief** | Every aesthetic decision — color, hierarchy, whitespace — is evaluated against its impact on click-through or sign-up, not visual taste alone. | **Steampunk Warmth Over Generic Polish** | Story Portal visuals evoke worn leather, warm gaslight, and handwritten invitations — reject sleek/corporate aesthetics even when they feel 'cleaner'."
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Multiple handoff problems compound each other. First, 'Brand Strategist' appears in the Receives From table but does not appear in the Works With table or the Organizational Charter reference — this is a likely hallucinated role. Second, artifacts are named generically: 'Copy' (what format? Google Doc? content brief with character limits per platform?), 'Briefs' (what template?), 'Ad creatives' (what file format, resolution, naming convention?). Third, 'All Marketing' as a delivery target is not a role. No handoff specifies the state of the artifact at handoff — approved vs. draft.",
      "example_rewrite": "| Receives From | Artifact | Format/State |\n|---|---|---|\n| Marketing Copywriter | Platform copy deck | Google Doc, copy approved by CMO, includes character limits per platform |\n| Performance Marketing Manager | Campaign creative brief | Completed brief template: objective, audience, CTA, dimensions required, deadline |\n\n| Delivers To | Artifact | Format/State |\n|---|---|---|\n| Performance Marketing Manager | Ad creative set | Figma link + exported PNGs/MP4s, named [Campaign]-[Platform]-[Size]-[Version], all required dimensions present |\n| Social Media Manager | Social graphic pack | Exported files at platform spec, Figma source file linked, brand-reviewed |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "The role has no dedicated Anti-Patterns section at all — the DON'T list in Boundaries is not equivalent. The DON'T items listed ('Don't define brand system', 'Don't write copy') describe jurisdiction boundaries, not failure modes. There are zero behavioral anti-patterns that would help an AI agent recognize when it is going wrong mid-task. A marketing designer has rich, specific failure modes: designing before copy is final, creating one-off assets that can't be templatized, prioritizing aesthetic over conversion, letting brand drift accumulate across a campaign, or delivering files in wrong formats/resolutions.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: | Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **Designing to lorem ipsum** | Layout collapses or requires rework when real copy arrives at different lengths | Request final or length-approved copy from Copywriter before beginning layout |\n| **One-off asset creation** | Each asset built from scratch creates inconsistency and slows future campaigns | Build every asset as a Figma component; if a template doesn't exist, create one first |\n| **Aesthetic over conversion** | Beautiful ads that don't drive sign-ups waste budget | Validate every design decision against the conversion objective in the brief |\n| **Silent brand drift** | Small campaign-by-campaign deviations accumulate into off-brand identity | Flag any brand system deviation to Head of Design before shipping, not after |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol is present and functional, which is the most important element for a Hybrid role. The Human/AI division of labor is stated. However, the Context Requirements section is literally unfilled placeholder text ('[Context item 1]', '[Context item 2]') and the Required Skills table is empty. An AI agent loading this role has no idea what context files to request before starting work — brand guidelines filename, campaign brief template, platform spec sheet. This is a critical gap for autonomous deployment.",
      "example_rewrite": "### Required Context\n- [ ] Brand guidelines document (provided by Head of Design)\n- [ ] Active campaign brief with objectives, audience, and CTA\n- [ ] Platform specification sheet (ad dimensions per channel)\n- [ ] Approved copy deck from Marketing Copywriter\n- [ ] Asset library access (existing approved graphics)\n\n### Required Skills\n| Skill | When to Load |\n|---|---|\n| figma-export-specs.md | When preparing final delivery to Performance Marketing or Social |\n| email-client-compatibility.md | When designing email templates |\n| story-portal-brand-guide.md | At start of every task |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix names the product and gestures at its aesthetic ('Steampunk warmth', 'Festival, community') but stops well short of actionable. There are no actual design constraints: no hex codes, no font names, no example imagery descriptions, no ad copy tone guidance, no information about what Story Portal's acquisition funnel looks like or what the festival event materials need to contain. A designer reading this appendix cannot make a single concrete design decision from it. The priority ranking (Acquisition ads first) is useful but unexplained.",
      "example_rewrite": "### Story Portal Visual Identity (Design Constraints)\n| Element | Specification |\n|---|---|\n| Primary palette | Amber (#C8860A), Deep Teal (#1A4A4A), Parchment (#F5ECD7) — never pure white backgrounds |\n| Typography | Headlines: Playfair Display (serif, worn-book feel); Body: Inter (readability); avoid sans-serif-only layouts |\n| Imagery style | Candlelit gatherings, handwritten props, aged maps, diverse storytellers — avoid stock-photo-corporate |\n| Forbidden aesthetics | Neon, flat-minimal, tech-startup blue, photorealistic AI faces |\n\n### Acquisition Ad Priority (Why #1)\nStory Portal is in growth phase — CMO goal is festival sign-up conversion. Acquisition ads run on Meta and Instagram. Primary CTA is always 'Join the Story' linking to festival landing page. All ad sets need 3 size variants: 1080x1080, 1080x1920, 1200x628."
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4-5 role-specific behavioral failure modes. This role currently has zero anti-patterns, which means an AI agent has no self-correction mechanism mid-task. The absence of anti-patterns (score: 2) is the single largest gap — it affects every workflow execution, not just setup or context loading. Specific patterns like 'designing before copy is final' or 'one-off asset creation' would immediately improve output quality on every task."
}
```