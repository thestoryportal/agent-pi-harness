```json
{
  "role": "3d-artist-generalist",
  "department": "creative-technology",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 7,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Four of the six principles read as broadly applicable to any technical creative role. 'Serve the Experience', 'Craft at Every Scale', and 'Collaborate Early' could appear in a UI Designer or VFX Artist role unchanged. 'Flexible Pipeline' is vague — every role should be flexible. Only 'Optimize for Medium' and 'Performance Is Part of Quality' are genuinely 3D-web-specific.",
      "example_rewrite": "Replace 'Flexible Pipeline' with: **Bake Early, Bake Often** — Real-time 3D on the web cannot afford dynamic computation that film pipelines take for granted. Default to baked lighting, baked AO, and pre-computed LODs rather than assuming the GPU will compensate. And replace 'Craft at Every Scale' with: **Topology Serves Animation and Engine, Not the Eye** — Clean edge loops and proper pole placement are non-negotiable even when the final mesh will be Draco-compressed, because downstream rigging and morph targets depend on intentional geometry decisions made at modeling time."
    },
    {
      "dimension": "handoff_specificity",
      "score": 7,
      "finding": "Outbound handoffs are good — GLTF/GLB to WebGL Engineer and rigged models to Animation Specialist are concrete. However, inbound handoffs are weak. 'Design' is listed as a source role but does not map to a named role in the collaboration section (UI Designer? Visual/Brand Designer?). 'Head of Creative Tech' delivering 'asset requirements, constraints' is a vague artifact — no format is specified.",
      "example_rewrite": "Replace the inbound 'Design' row with two explicit rows: | **Visual/Brand Designer** | Concept art PDF or Figma link with annotated style notes, color palette, and reference mood board | and | **Head of Creative Technology** | Asset Brief document specifying: asset name, poly budget (tris), texture budget (KB), target LOD count, delivery deadline, and integration owner |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Most anti-patterns are legitimately 3D-specific (over-texturing, skipping LODs, ignoring web constraints). However, 'Work in isolation' and the implied 'Skip testing' are generic enough to appear in any role file. The table also has six rows, which dilutes focus. The 'Why' column entries are minimal — 'Performance suffers' and 'Memory bloat' don't teach the agent why these are traps for this specific stack.",
      "example_rewrite": "Replace 'Work in isolation → Integration issues' with: | **Export without validating in Three.js r3f viewer** | A model that renders correctly in Blender's EEVEE can have broken normals, missing UV channel 1 for lightmaps, or unsupported KHR extensions when loaded via Three.js GLTFLoader — these failures are invisible until the WebGL Engineer loads the file | Validate every export in a local Three.js sandbox before marking the asset complete |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "The Iteration Protocol is present and correct, the CLI deployment rationale is explained, the Definition of Done checklist is concrete, and performance targets give the agent hard numbers. The main gap is that the Context Requirements section lists skills to load ('steampunk-design-system.md', 'animation-standards.md') but the agent has no instruction for what to do if those files are absent — halt and request them, or proceed with defaults?",
      "example_rewrite": "Add a 'Missing Context Fallback' block under Context Requirements: **If required skill files are absent at deploy time:** STOP before beginning modeling work. Output: 'Required context file [filename] not found. This file is needed to ensure asset style matches project standards. Please provide or confirm proceeding without it. If proceeding without steampunk-design-system.md, I will default to brass/copper PBR values: metallic 0.9, roughness 0.3-0.5, albedo #B5651D range — confirm these defaults before I begin.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The appendix correctly identifies that Story Portal uses CSS 3D today and lists four future opportunities, but everything is marked 'Future' with no prioritization criteria, no trigger conditions, and no actionable next step. The steampunk aesthetic section cites four game references without connecting them to specific material or geometry decisions. An AI agent reading this section learns nothing it could act on today, and the transition criteria from CSS 3D to true 3D are completely absent.",
      "example_rewrite": "Replace the Potential 3D Opportunities table with an Upgrade Trigger section: **When to escalate from CSS 3D to true 3D:** Engage this role for asset production when any of these conditions are met: (1) Wheel requires per-face depth variation >8px that CSS perspective cannot achieve without z-fighting, (2) Steampunk gear decorations need specular highlights that respond to a shared scene light source, (3) Performance profiling shows CSS 3D paint cost exceeds 4ms/frame on target device. First recommended asset: a single brass gear decoration (<2,000 tris, 512x512 ORM texture, GLB <80KB) as a pilot to validate the GLTF pipeline before committing to full wheel replacement."
    }
  ],
  "top_improvement": "The Story Portal appendix is the highest-priority fix. A role that is 'Hybrid' classification on an active project should have an appendix that gives the AI agent something to do or decide today — not a list of future maybes. Adding concrete upgrade trigger conditions and a pilot asset specification (single gear decoration with hard budget numbers) would immediately transform this from a placeholder into actionable guidance, and would also validate the entire 3D pipeline end-to-end before any major CSS-to-3D migration is attempted."
}
```