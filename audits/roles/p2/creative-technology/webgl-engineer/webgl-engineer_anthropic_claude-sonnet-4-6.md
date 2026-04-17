```json
{
  "role": "webgl-engineer",
  "department": "creative-technology",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 6,
    "anti_pattern_quality": 9,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "Five of six principles are genuinely WebGL-specific: the 60fps hard floor, GPU architecture understanding, visual iteration as test suite, and measure-before-optimize are all role-authentic. 'Collaborate with Designers' is the weakest entry — it reads as a generic cross-functional platitude that would appear unchanged in a Frontend Developer or Motion Designer role. It does no work distinguishing a WebGL Engineer's specific design partnership (translating visual specs into shader math) from generic collaboration.",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The receives-from side names artifacts but they remain vague: 'visual design, references, mood boards' could mean a Figma file, a Sora MP4, a PNG frame grab, or a Notion page. The delivers-to side is worse — 'Integrated effect components' and 'Effect for testing' do not name file types, component names, or acceptance criteria. Two roles listed in Works With ('Performance Engineer' and 'QA') do not appear to exist in a standard Creative Technology charter and may be hallucinated roles, which violates the template standard. Frontend Developer handoff also lacks integration contract detail.",
      "example_rewrite": "Receives From VFX Artist: `electricity-portal-v2-reference.mp4` (Sora output) + `effect-spec.md` (palette hex values, intensity envelope, target SSIM floor). Delivers To Frontend Developer: `<ElectricityPortal />` React component at `src/effects/electricity-portal/index.tsx` with exported `ElectricityPortalProps` TypeScript interface and README covering uniform names and accepted value ranges."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 9,
      "finding": "Six anti-patterns, all WebGL-specific. 'Magic numbers in shaders' is an excellent catch that only applies to shader authorship. 'Skip visual verification / metrics can lie' directly addresses a real GPU profiling failure mode where frame time looks fine but visual corruption exists. 'Continue after stop' enforces the iteration protocol at the anti-pattern level, creating redundant safety. The only marginal entry is 'Make multiple changes at once' — true and role-relevant, but it also appears nearly verbatim in the iteration protocol, making it slightly redundant rather than additive.",
      "example_rewrite": null
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 9,
      "finding": "The iteration protocol is explicit, numbered, and includes a hard HALT instruction. Workflow 3 includes a mandatory every-7-iterations checkpoint with a STOP gate. The 'Visual Feedback = Ground Truth' section with priority, action, scope, and trust fields gives an AI agent a clear tiebreaker hierarchy when metrics and human feedback conflict. The Required Skills table with exact filenames to load is strong. Minor gap: the role does not specify what the AI should output when it hits an ESCALATE condition — it lists escalation triggers but not the format or recipient of the escalation artifact.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The appendix names actual files, actual techniques (simplex noise, ACES tone mapping, cream→amber palette), and a two-phase iteration strategy. The 'AAA video game quality' quality bar is memorable and directional. The file tree is the strongest element — an AI agent can immediately locate entry points. Two gaps: (1) The 'wheel-mechanics.md' skill in Required Skills has no corresponding explanation in the appendix — a wheel effect is mentioned but not described, leaving an AI agent without context for when to load it. (2) The Phase 1 / Phase 2 description is present but does not state completion criteria for Phase 1 before Phase 2 begins, which could cause an agent to start envelope work prematurely.",
      "example_rewrite": null
    }
  ],
  "top_improvement": "Fix handoff specificity: replace vague artifact names with exact file paths, formats, and interface contracts, and audit the Works With table to remove or confirm 'Performance Engineer' and 'QA' against the Organizational Charter — hallucinated collaborator roles will cause an AI agent to attempt handoffs to non-existent recipients and stall workflows."
}
```