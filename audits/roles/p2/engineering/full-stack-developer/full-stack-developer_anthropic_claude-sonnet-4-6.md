```json
{
  "role": "full-stack-developer",
  "department": "engineering",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 6,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "Six principles are present and most are role-specific. 'Breadth Over Depth' and 'Know Your Limits' are genuinely distinctive to a generalist role and avoid generic platitudes. 'Ship Complete Work' and 'Consistency Across Layers' are stronger than typical boilerplate. Minor deduction: 'Pragmatic Choices' borders on generic — 'simplest solution that meets requirements' is advice that could appear in any engineering role without modification.",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The Handoff Matrix names specific roles correctly, and the quantified thresholds (>3 joins, >100ms, >300 lines) are excellent. However, the 'Handoffs' table at the bottom of Collaboration is vague in both directions. 'Receives From: Product/UX → Feature requirements, user stories' does not name an actual charter role — 'Product/UX' is ambiguous. More critically, 'Delivers To: Frontend Developer → Complex UI work that needs depth' does not specify what artifact is handed off. What file, document, or output changes hands?",
      "example_rewrite": "| Delivers To | Artifact |\n|-------------|----------|\n| QA Engineer | PR link + completed feature checklist (Definition of Done filled) |\n| Frontend Developer | Handoff note in PR: component file path, what complexity was hit (e.g. 'exceeded 300 lines, needs animation logic'), and reproduction steps |\n| Backend Developer | PR comment with: query file path, profiling output (if available), and specific threshold hit (e.g. '>3 joins in stories_query.ts') |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Seven anti-patterns are listed, which exceeds the 3-5 guideline range but most are role-relevant. 'Go deep in specialist domains' and 'Assume you know security' are genuinely specific to a full-stack generalist's failure modes. 'Copy-paste across layers' is a nice role-specific addition. However, 'Skip layers in testing' and 'Over-engineer / Under-test' are generic enough to appear in any developer role without modification and dilute the specificity of the stronger entries.",
      "example_rewrite": "| Don't | Why | Instead |\n|-------|-----|--------|\n| Implement the full feature in one layer (e.g. all logic in UI) | Full-stack means owning the stack, not collapsing it | Distribute logic correctly: validation at API, persistence at DB, display at UI |\n| Start coding before checking handoff triggers | Auth/schema work discovered mid-feature causes expensive rework | Run the handoff checklist at step 2 of every feature workflow before writing any code |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 9,
      "finding": "This is the strongest dimension. The Iteration Protocol loop is explicit, imperative, and unambiguous. The skill loading strategy with named files (e.g. 'steampunk-design-system.md', 'supabase-patterns.md') gives an AI agent concrete loading instructions. Quantified thresholds remove judgment calls. STOP points appear in every workflow. The 'Example: Feature Task Skill Loading' block is exactly the kind of concrete worked example that prevents AI agents from guessing. Minor deduction: Workflow 3 (API Integration) references 'Creative Technology' in step 3 but this role name does not appear in the Collaboration section — a potential hallucinated role reference.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The appendix correctly names the actual stack (React 19, TypeScript 5.9, Vite 7, Supabase) and references the steampunk design system indirectly via skill files. However, the project structure shown is generic ('components/', 'views/', 'hooks/') and the 'legacy/' prefix is unexplained — an AI agent reading this has no context for what 'legacy' means or whether new code should go inside or outside it. The Phase 2 backend section is forward-looking but provides no actionable guidance for the current phase. The quality bar entry '60fps performance maintained' is specific but isolated — no guidance on how the Full Stack Developer should detect or respond to a performance regression.",
      "example_rewrite": "### Project Structure Notes for Full Stack Developer\n\n- All current source lives under `src/legacy/` — this is the active codebase, not deprecated code. The 'legacy' prefix reflects a planned refactor that has not begun.\n- New feature components go in `src/legacy/components/[feature-name]/`\n- New views go in `src/legacy/views/`\n- Do NOT create a parallel `src/` structure outside `legacy/` without Backend Developer + Engineering Manager approval.\n- 60fps performance bar: if Vitest or manual testing reveals a render taking >16ms, flag it in your PR description with the component name before submitting for review."
    }
  ],
  "top_improvement": "Handoff artifacts are under-specified in the Collaboration section. The Handoff Matrix correctly identifies when to hand off and to whom, but the Handoffs table does not name what physical artifact changes hands (no file path, no document type, no PR convention). An AI agent hitting a handoff trigger knows to stop, but does not know what to produce before stopping. Rewrite every 'Delivers To' row to name a concrete artifact (e.g. 'PR comment with profiling output', 'handoff note with component file path and threshold hit') so the agent can complete its side of the handoff cleanly."
}
```