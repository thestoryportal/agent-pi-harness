```json
{
  "role": "ui-designer",
  "department": "design",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 7,
    "anti_pattern_quality": 5,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Four of the six principles are genuinely UI-specific ('System, Then Style', 'Hierarchy Guides', 'Motion With Purpose', 'Accessibility Is Visual'). However, 'Details Matter' and 'Consistency Is Trust' are near-universal design platitudes that could belong to any designer, illustrator, or even a copywriter. They lack the UI-specific framing that would distinguish this role from, say, a Brand Designer or Print Designer.",
      "example_rewrite": "Replace 'Details Matter: Pixel-perfect execution distinguishes quality' with 'States Are Not Optional: Every interactive element must have default, hover, focus, active, disabled, and error states designed before handoff — partial states cause implementation debt.' Replace 'Consistency Is Trust: Visual consistency builds user confidence' with 'Token First, Override Never: Visual decisions must trace to a design token; one-off hex values and arbitrary spacing create system drift that compounds across every future component.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 7,
      "finding": "Handoff table names actual roles and artifact types, which is solid. The weakness is that delivered artifacts to Frontend Developer are listed as 'Visual specs, assets' — these are categories, not artifacts. An AI agent or human successor cannot tell whether this means a Figma file link, a Zeplin export, a PDF redline, or a Storybook reference. Incoming artifacts from UX Designer are listed only as 'Wireframes' with no format or fidelity expectation specified.",
      "example_rewrite": null
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 5,
      "finding": "All five anti-patterns ('Ignore design system', 'Skip accessibility check', 'Design one state only', 'Skip responsive', 'Poor handoff specs') are generic UI design best-practices found in any onboarding deck. None reference Story Portal's steampunk aesthetic, the specific roles named in this file, or failure modes unique to a Hybrid AI-assisted workflow. There is no anti-pattern addressing the AI-specific risk of over-generating visual variations without human approval, or the risk of applying steampunk textures in ways that fail WCAG contrast requirements.",
      "example_rewrite": "Replace 'Poor handoff specs → Implementation errors → Document thoroughly' with 'Steampunk Texture Over Contrast: Applying aged-paper or leather-texture backgrounds without re-checking WCAG AA contrast ratios on every text layer — the aesthetic creates a systematic risk of contrast failures that only appear in implementation. Always re-run contrast checks after any texture layer is added.' Add: 'AI Variation Overload: Accepting the first AI-generated visual variation without evaluating against the steampunk-design-system.md tokens. AI outputs plausible-looking colors that are not brass/copper palette tokens — always reconcile hex values against the token file before refinement.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Context Requirements section — the single most critical section for AI deployment — is left as unfilled placeholders: '[Context item 1]', '[Context item 2]', and the Required Skills table has no entries. An AI agent loading this role has no idea what files to read before starting, what skills to activate, or what the steampunk-design-system.md file contains. The Iteration Protocol exists and is correctly structured, but it is meaningless without the context loading instructions that precede it. This is the most serious defect in the file.",
      "example_rewrite": "Replace the empty Context Requirements section with: 'Required Context: [ ] steampunk-design-system.md — load before any design task to validate token usage [ ] brand-guidelines.md — load before applying any color or typography [ ] Current wireframes from UX Designer (Figma link or PDF) — must be present before Workflow 1 begins [ ] Accessibility checklist — load before any STOP → Design approved checkpoint. Required Skills: | visual-design-execution.md | Every design task | | wcag-contrast-checking.md | Before every STOP → Design approved | | figma-component-spec.md | Before every STOP → Handoff complete |'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix names the aesthetic, palette, and key elements with reasonable specificity — brass, copper, leather, aged paper, mechanical details are all actionable. The reference to steampunk-design-system.md is correct. The weakness is that the Key Visual Elements table describes only static elements (wheel, buttons, backgrounds, text) and gives no guidance on interactive states, which is the UI Designer's primary concern. There is also no guidance on how the steampunk aesthetic interacts with dark/light mode, mobile breakpoints, or loading/empty states — all of which a UI Designer must resolve.",
      "example_rewrite": "Add to Key Visual Elements table: '| Interactive States | Hover: brass sheen shift; Focus: copper glow ring (not default browser outline); Disabled: desaturated to aged-iron tone; Error: red-patina, not pure #FF0000 — reference error-state token in steampunk-design-system.md | | Mobile Adaptation | Mechanical textures reduce to flat brass tones below 768px — texture PNGs are performance-prohibitive on mobile; use CSS token approximations defined in steampunk-design-system.md §Mobile |'"
    }
  ],
  "top_improvement": "Fill the Context Requirements section immediately — the '[Context item 1]' placeholders mean an AI agent cannot load this role and function at all. At minimum, list steampunk-design-system.md, brand-guidelines.md, and the current wireframe artifact as required context, and populate the Required Skills table with at least wcag-contrast-checking.md and figma-component-spec.md with the workflow checkpoint at which each must be loaded. Without this, every other quality improvement in this file is blocked."
}
```