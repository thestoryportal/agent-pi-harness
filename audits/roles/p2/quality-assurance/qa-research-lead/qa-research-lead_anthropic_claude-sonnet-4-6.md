```json
{
  "role": "qa-research-lead",
  "department": "quality-assurance",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 6,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "All 6 principles are present and named well, but two lean generic. 'Share Knowledge Freely' and 'Question Assumptions' could apply to any research role in any domain. The four strongest principles (Evidence Over Opinion, Understand Before Recommending, Context Matters, Total Cost of Adoption) are genuinely QA-research-specific. The role earns a 7 because it clears the bar, but the weaker two dilute the set.",
      "example_rewrite": "Replace 'Share Knowledge Freely' with 'Research Decays Without Adoption — A tool evaluation report that sits unread has zero value. Every research output must include a knowledge transfer plan: who needs to know, in what format, and by when.' Replace 'Question Assumptions' with 'The QA Team Is Your Customer — Research priorities come from their pain points, not from interesting technology. If the team cannot use a finding within two quarters, deprioritize it.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The Receives From and Delivers To tables name roles correctly, but the artifact column is too vague on both sides. 'Research priorities, problem areas' from Head of QA tells an AI agent nothing about format or triggering condition. 'Research reports, recommendations' to Head of QA is equally opaque — is this a Notion doc, a slide deck, a structured markdown file? An AI agent cannot initiate or close a handoff without knowing the artifact format and the signal that triggers the handoff.",
      "example_rewrite": "Delivers To Head of QA: 'Tool Evaluation Report (structured markdown: executive summary, scored comparison matrix, POC findings, go/no-go recommendation) — delivered at Workflow Step 5 STOP point, minimum 48 hours before adoption decision meeting.' Receives From Head of QA: 'Research Brief (written Notion page: problem statement, current pain point evidence, deadline, budget ceiling) — triggers Workflow 1 Step 1 or Workflow 2 Step 1.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Six anti-patterns are listed, which exceeds the minimum. Five are genuinely role-specific ('Recommend without testing', 'Ignore adoption costs', 'Chase shiny objects', 'Research in isolation', 'Hoard knowledge'). 'Skip documentation' is too generic — it applies to every role in the framework. The set would be stronger with a QA-research-specific replacement targeting a failure mode unique to this role, such as over-investing in POC completeness at the expense of timely recommendations.",
      "example_rewrite": "Replace 'Skip documentation — Knowledge lost — Document everything' with 'Over-engineer the POC — A 500-line prototype is not more convincing than a 50-line one, and it takes three times as long. POCs exist to validate the hypothesis, not to production-harden the approach. Timebox every POC to 2 days maximum. If you cannot demonstrate the key finding in 2 days, the hypothesis needs to be narrower.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "The Iteration Protocol is present and explicit. The Hybrid classification is correctly applied and explained. STOP points appear at logical decision gates in all three workflows. The role loses points in two places: (1) the Context Requirements section lists skill files and explicitly notes they are 'planned development' — an AI agent loading this role has no fallback if those files do not exist; (2) the Browser deployment rationale is solid but does not specify what to do when a workflow step requires live tool access that browser mode may not support (e.g., installing and running k6).",
      "example_rewrite": "Add to Context Requirements: 'If skill files are unavailable, fall back to: (1) R&I research methodology standards embedded in this document's Quality Standards section, (2) tool documentation from official vendor sources, (3) explicit request to Head of QA for constraints before proceeding.' Add to Browser Deployment: 'When a workflow step requires tool installation or CLI execution (e.g., running k6, axe-core), flag the step as HUMAN-EXECUTED, document the exact commands needed, and resume synthesis after the human provides output.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 9,
      "finding": "This is the strongest section in the document. The research priorities table is ranked, the current state column gives an AI agent real starting context, and the Story Portal-specific research areas (WebGL, animation timing, MediaRecorder, steampunk UI) are granular enough to be immediately actionable. The initial recommendations table with rationale is excellent. One minor gap: the E2E priority is listed as 'Not started' but the recommendations table already commits to Playwright — the research feels pre-concluded, which undercuts the role's 'Evidence Over Opinion' philosophy.",
      "example_rewrite": "Change Priority 1 row to: 'Status: Evaluation criteria defined, POC required. Hypothesis: Playwright preferred based on cross-browser support and Vitest ecosystem alignment — requires validation against Story Portal WebGL rendering constraints before recommendation is final.' This preserves the directional signal while keeping the research process honest."
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority improvement. Every other dimension in this role is functional, but vague handoff artifacts ('research priorities', 'research reports') mean an AI agent cannot initiate or close a workflow step without human clarification on format and trigger conditions. Define each artifact with: (1) document format, (2) required sections, (3) the workflow step at which it is produced or consumed, and (4) the signal that triggers the handoff. This change alone would make the role operationally self-sufficient."
}
```