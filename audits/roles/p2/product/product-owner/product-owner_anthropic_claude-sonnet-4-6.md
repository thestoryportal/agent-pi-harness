```json
{
  "role": "product-owner",
  "department": "product",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 5,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "All 6 principles are present and role-specific. 'Backlog Is Always Ready' and 'Sprint Commitment Is Sacred' are concrete and PO-specific. 'Value Over Volume' and 'Small Slices, Fast Feedback' are directionally good but slightly generic — they could appear in any agile role. The table format clearly distinguishes principle from meaning, which is solid. No rewrites needed, but sharpening two principles would push this to a 9.",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoffs name roles but artifacts are vague and directional rather than concrete. 'Requirements, priorities' from Product Manager is not an artifact — it's a category. 'Designs, specs' from UX Designer is similarly loose. No file formats, no named documents, no state indicators (e.g., 'approved' vs 'draft'). The Delivers To table is equally vague: 'Prioritized, refined stories' doesn't specify where they live or what state they're in when handed off.",
      "example_rewrite": "| Receives From | Artifact |\n|---------------|----------|\n| Product Manager | Approved PRD (Notion, marked 'Ready for PO') |\n| UX Designer | Figma file with accepted designs (status: 'Dev Ready') |\n| Stakeholders | Feature request ticket (GitHub Issue, label: 'needs-grooming') |\n| Engineering | Story PR link with demo video, marked 'Ready for Acceptance' |\n\n| Delivers To | Artifact |\n|-------------|----------|\n| Development Team | GitHub Issues with AC in Given-When-Then format, label: 'sprint-ready' |\n| Product Manager | Sprint progress comment in Notion roadmap doc |\n| QA | Acceptance criteria checklist embedded in each GitHub Issue |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Six anti-patterns are present and most are PO-specific. 'Accept incomplete work' and 'Change scope mid-sprint' are genuinely role-specific failure modes. 'Prioritize by whoever is loudest' is sharp and real. However, 'Write vague stories' is a mild observation that applies to any writer role, and 'Micro-manage implementation' is a generic agile principle that appears in Scrum Master and Engineering Manager roles too. The table format (Don't / Why / Instead) is well-structured.",
      "example_rewrite": null
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol is present and correctly structured for a Hybrid role. The AI/Human split is clearly articulated: AI drafts stories and criteria, Human makes acceptance decisions and attends ceremonies. The three ALWAYS directives at the end are actionable. Minor gap: the protocol doesn't specify what format AI should use when presenting draft stories for human review, or what constitutes 'approved' vs 'needs adjustment' in step 3. An AI agent would know its lane but might loop ambiguously on the review step.",
      "example_rewrite": "LOOP:\n  1. Draft backlog item as GitHub Issue using template: Title (As a [user]...), AC in Given-When-Then, label 'draft'\n  2. STOP → Present draft to human with: story text, 3 clarifying questions if requirements are ambiguous\n  3. WAIT for human feedback\n  4. IF human edits or comments → Revise and return to step 2\n  5. IF human says 'approved' or adds label 'sprint-ready' → Item is finalized, no further AI action\n  6. IF human says 'stop' or 'pause' → HALT immediately, confirm halt with human\n  7. REPEAT for next backlog item"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The appendix names real Story Portal features (wheel spin, audio recording, PWA, festival deadline) which is meaningful context. The acceptance criteria examples are specific and testable. However, the Current State table reveals almost nothing actionable — 'Sprint Cadence: Flexible' and 'User Stories: Informal' are observations, not operational context. The Sprint Focus table references sprints without dates, velocity, or capacity. The PO has no way to know how many stories fit in a sprint, what the festival deadline actually is, or which stakeholders exist. This limits operational usefulness.",
      "example_rewrite": "### Current State (Story Portal MVP)\n\n| Area | Current State |\n|------|---------------|\n| **Backlog** | GitHub Issues — primary tracking tool, labels: feature/bug/tech-debt |\n| **Sprint Cadence** | 2-week sprints; current sprint ends Jan 10, 2025 |\n| **Team Capacity** | ~3 dev days per sprint (solo developer, part-time) |\n| **Hard Deadline** | Festival demo: March 15, 2025 — 10 sprints remaining |\n| **Stakeholders** | Festival organizer (external), 2 internal reviewers |\n| **Definition of Done** | Works offline on iOS Safari, no console errors, accepted by PO |\n\n### Sprint Focus\n\n| Sprint | Dates | Focus | Exit Criteria |\n|--------|-------|-------|---------------|\n| Current | Dec 25 – Jan 10 | Core wheel + recording | Wheel spins, prompt displays, audio saves locally |\n| Next | Jan 11 – Jan 24 | PWA + offline | Installable, works with no connection |\n| Following | Jan 25 – Feb 7 | Polish + festival prep | Stakeholder demo-ready build |"
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority improvement. Vague artifacts like 'Requirements, priorities' and 'Designs, specs' mean an AI agent cannot reliably identify when a handoff has occurred or what to do with it. Rewrite all handoff artifacts to specify: the actual document or tool (GitHub Issue, Notion PRD, Figma link), the state or label that signals readiness (e.g., 'Dev Ready', 'sprint-ready'), and the direction of flow. This single change unlocks reliable AI-assisted workflow execution across every ceremony and sprint cycle."
}
```