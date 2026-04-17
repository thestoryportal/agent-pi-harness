# Enrichment Proposals — creative-technology — 2026-04-17

**Structural note for downstream consumer:** In these department templates, `### Required Context` lives inside the `## Context Requirements` block (not inside `## Appendix: Project Context` as the style guide states). `### Key Priorities` and `### Quality Bar` live inside `## Appendix: Project Context` as expected. All proposed edits target the section at its actual location in each role file. The same structure holds for the style guide's own reference sample `engineering/backend-developer.md` (verified 2026-04-17, lines 519 and 607), so this is a style-guide documentation gap, not a template mismatch.

---

## 3D Artist / Generalist
**File:** `~/.claude/roles/creative-technology/3d-artist-generalist.md`
**JD sources used:** 3D Artist.md
**JD tiers:** STRONG: 0, GOOD: 1, WEAK: 0

### Required Context
**Add:**
- `- [ ] Substance Painter or equivalent PBR texturing tool access` — *source: 3D Artist.md (Substance Painter/Designer for PBR workflows), reason: names the specific PBR toolchain; current list covers Blender and GLTF but not PBR texturing*
- `- [ ] UV mapping and LOD requirements for the target engine` — *source: 3D Artist.md (UV mapping best practices, LOD setup), reason: adds the two upstream technical constraints current list omits*

**Edit:**
- (no edits — existing five items are already concrete)

### Key Priorities
**Add:**
- `Produce LOD variants per asset matched to the renderer's distance bands` — *source: 3D Artist.md (game art pipelines, LOD setup), reason: adds missing real-time-delivery practice; current bullets cover export pipeline and optimization but not LOD tiering*

**Edit:**
- OLD: `Optimize aggressively — every kilobyte matters on the web` → NEW: `Optimize aggressively with basis/KTX2 textures, meshopt compression, and LOD tiers so every kilobyte and draw call is accounted for` — *reason: 3D Artist.md (real-time rendering constraints) — names the three specific optimization techniques that make "optimize aggressively" falsifiable*

### Quality Bar
**Add:**
- `| **Topology** | Quads-first for deformable meshes; triangle count within budget |` — *source: 3D Artist.md (topology requirements for deformation and optimization), reason: adds a falsifiable gate for mesh quality current rows don't cover*

---

## Animation Specialist
**File:** `~/.claude/roles/creative-technology/animation-specialist.md`
**JD sources used:** animator.md
**JD tiers:** STRONG: 0, GOOD: 1, WEAK: 0

Skip — GOOD match (`animator.md`) is a short traditional-animation JD (storyboards, 2D/3D, frame-audio sync) that describes a different craft than this role's web-implementation focus (Framer/GSAP/Motion, 60fps profiling, reduced-motion, Chrome DevTools). The role file's existing Required Context, Key Priorities, and Quality Bar are already highly specific with concrete tooling and falsifiable gates. No enrichment warranted.

---

## Creative Tech Research Lead
**File:** `~/.claude/roles/creative-technology/creative-tech-research-lead.md`
**JD sources used:** Creative Director.md, UX Researcher.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (skimmed)

Skip — WEAK matches only, insufficient signal. `Creative Director.md` is a leadership/brand-strategy JD and `UX Researcher.md` is a product-research JD; neither produces the creative-technical radar/R&D signal this role owns. The role file's existing sections (technology radar with Adopt/Trial/Assess/Hold, synthesis cadence, decision-grade recommendations) are already specific and appropriate.

---

## Creative Technologist
**File:** `~/.claude/roles/creative-technology/creative-technologist.md`
**JD sources used:** Creative Director.md, Digital Designer.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (skimmed)

Skip — WEAK matches only, insufficient signal. Both JDs describe adjacent creative-leadership and digital-design work, not the R&D/prototyping/design-engineering-bridge craft this role performs. Existing Required Context, Key Priorities, and Quality Bar (time-boxed experiments with testable hypotheses, findings documented regardless of outcome, production-readiness criteria, transferability) are already specific.

---

## Head of Creative Technology
**File:** `~/.claude/roles/creative-technology/head-of-creative-technology.md`
**JD sources used:** Chief Creative Officer.md, Creative Director.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (skimmed)

### Required Context
**Add:**
- (no new items — existing eight items are exceptionally thorough)

### Key Priorities
**Add:**
- `Own the creative-tech tooling budget (engines, renderers, plugins, device fleet) and renew based on usage data` — *source: Creative Director.md (creative department budgets and vendor relationships), reason: adds budget-authority bullet missing from current list — a head-of role needs to own the tooling-spend lever*

**Edit:**
- (no edits — existing five bullets are already strong)

### Quality Bar
**Add:**
- `| **Device Fleet Coverage** | Representative target hardware (low, mid, high-tier) available for every ship gate |` — *source: role content itself plus Chief Creative Officer.md (creative technology adoption), reason: the existing "Performance" row references "representative target hardware" but no row guarantees the fleet actually exists; this closes the loop*

---

## Motion Design Lead
**File:** `~/.claude/roles/creative-technology/motion-design-lead.md`
**JD sources used:** Creative Director.md, Motion Graphics Designer.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (skimmed)

### Required Context
**Add:**
- `- [ ] Motion-token schema (duration scale, easing curves, choreography rules) in the design system` — *source: Motion Graphics Designer.md (motion design systems and templates that maintain brand consistency), reason: current "Existing design system" bullet is too generic; this names the motion-specific sub-schema*

**Edit:**
- (no edits — other four items already appropriate)

### Key Priorities
**Add:**
- `Partner with UI Designer on motion-in-handoff so specs arrive with timing and easing, not just "animate it"` — *source: Motion Graphics Designer.md (developer handoff), reason: names the cross-role artifact; current bullets cover language/tokens/rationale but not the cross-role handoff discipline*

**Edit:**
- (no edits — existing 5 bullets are already specific and imperative)

### Quality Bar
**Add:**
- `| **Reduced Motion** | Every shipped animation has a tested reduced-motion alternative that preserves meaning |` — *source: Motion Graphics Designer.md (accessibility standards for motion content), reason: adds a11y-motion gate missing from current rows; the sibling Animation Specialist role has this but the Lead role should own the standard*

---

## Motion Designer
**File:** `~/.claude/roles/creative-technology/motion-designer.md`
**JD sources used:** Motion Graphics Designer.md, junior-designer.md
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**Add:**
- `- [ ] After Effects or Rive file access for spec-level motion authoring` — *source: Motion Graphics Designer.md (After Effects mastery), reason: names the specific authoring tool; current list covers tokens/system/designs but not the authoring file-type access*
- `- [ ] Lottie or Rive export pipeline to the implementing codebase` — *source: Motion Graphics Designer.md (Lottie, Rive, or similar web animation tools), reason: adds the export-to-code bridge that turns spec work into shippable asset*

**Edit:**
- (no edits — existing five items already specific)

### Key Priorities
**Add:**
- `Deliver Lottie/Rive exports when the target is web, not just storyboards and specs` — *source: Motion Graphics Designer.md (web animation tools), reason: adds the concrete shippable-artifact bullet; current bullets cover specs but not the runtime-asset handoff*

**Edit:**
- OLD: `Specify animations per component with clear entry, active, exit states` → NEW: `Specify animations per component with entry, active, exit, loading, and error states` — *reason: Motion Graphics Designer.md (micro-interactions and UI motion principles) — completes state coverage parallel to the UI Designer Quality Bar*

### Quality Bar
**Add:**
- `| **Runtime Fidelity** | Exported asset matches the spec within documented tolerance on target devices |` — *source: Motion Graphics Designer.md (developer handoff, video compression and delivery specifications), reason: adds a falsifiable gate for the spec-to-runtime drift problem motion designers own*

---

## VFX Artist
**File:** `~/.claude/roles/creative-technology/vfx-artist.md`
**JD sources used:** 3D Artist.md, Motion Graphics Designer.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (skimmed)

### Required Context
**Add:**
- `- [ ] Reference capture and AI-generation tooling (Sora, Luma, Runway) licensed and available` — *source: existing role-file mention + Motion Graphics Designer.md (emerging 3D technologies), reason: the Current State already references AI-generated references as a norm — promoting this to Required Context makes the access prerequisite explicit*

**Edit:**
- (no edits — existing five items already appropriate)

### Key Priorities
**Add:**
- `Establish per-effect graceful-degradation tiers (hero / standard / minimum) before implementation begins` — *source: existing Quality Bar "Scalability" row turned into an upstream priority — rigor from 3D Artist.md LOD practice, reason: turns the "graceful degradation" gate into a concrete setup activity the role owns day one*

**Edit:**
- (no edits — existing five bullets already imperative and specific)

### Quality Bar
**Add:**
- `| **Reference Traceability** | Every shipped effect cites its reference board and approved moodframe |` — *source: 3D Artist.md (work from concept art, reference photography to achieve director's vision), reason: adds a falsifiable provenance gate; current rows cover fidelity and performance but not reference-lineage*

---

## WebGL Engineer
**File:** `~/.claude/roles/creative-technology/webgl-engineer.md`
**JD sources used:** web-developer.md
**JD tiers:** STRONG: 0, GOOD: 1, WEAK: 0

### Required Context
**Add:**
- `- [ ] Cross-browser/device test matrix with GPU tier mapping` — *source: web-developer.md (cross-browser compatibility and testing), reason: adds the GPU-tier testing dimension specific to WebGL work; current "Existing codebase patterns" doesn't cover the runtime target matrix*

**Edit:**
- OLD: `- [ ] Existing codebase patterns (how effects are structured)` → NEW: `- [ ] Existing shader-module conventions, uniform/attribute naming, and effect-composition patterns` — *reason: web-developer.md (documentation and organizational habits) — makes the "codebase patterns" item falsifiable by naming the three WebGL-specific conventions*

### Key Priorities
**Add:**
- `Wire a WebGL-capability detection path so unsupported GPUs fall back deterministically rather than rendering broken` — *source: web-developer.md (cross-browser compatibility, debugging), reason: adds the capability-gate practice; current "Fallbacks" quality-bar row gestures at this but no priority names the setup work*

**Edit:**
- OLD: `Partner with VFX Artist so creative intent survives implementation` → NEW: `Partner with VFX Artist via SSIM-diff review loops so creative intent survives implementation` — *reason: the role file's existing Current State references SSIM iteration — making the partnership bullet name the specific tool turns collaboration into a concrete review ritual*

### Quality Bar
**Add:**
- `| **Shader Documentation** | Every uniform, attribute, and function has a comment explaining intent |` — *source: web-developer.md (clear documentation and organizational habits), reason: sharper than current "Shader Hygiene" row which bundles review/comments/reusability — this isolates the documentation standard as its own falsifiable gate*

---
