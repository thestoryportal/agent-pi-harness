```json
{
  "role": "okr-planning-coordinator",
  "department": "strategy-business-dev",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic OKR platitudes that could appear in any business textbook. 'Goals Drive Behavior' and 'What's measured gets done' is a Drucker quote with no specificity to Story Portal's stage, team size, or planning context. None of the principles address the tension unique to this role: coordinating goal-setting for an early-stage startup where strategy is still forming, teams are small, and the OKR coordinator has no direct authority. There is zero mention of how to handle OKRs during a pre-launch phase like Love Burn, or how to balance aspiration with startup resource constraints.",
      "example_rewrite": "Replace 'Simplicity Scales' with: **Startup OKRs Are Hypotheses** — At Story Portal's stage, quarterly OKRs are assumptions about what success looks like, not commitments carved in stone. Design every goal with a built-in review trigger: if market signals or product pivots invalidate the hypothesis within 6 weeks, the OKR should be revised, not defended. Coordinator resists the pressure to preserve OKRs for the sake of process consistency."
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Every handoff is described with a generic artifact label that conveys no operational meaning. 'Receives: Strategic priorities from CSO' does not specify whether this is a written strategy memo, a slide deck, a verbal briefing, or a ranked priority list — and therefore an AI agent cannot know what format to expect or how to process it. 'Delivers: Alignment reports to All Leaders' is equally vague: no frequency, no format, no specific content structure. The Business Planner is listed as a collaborator but does not appear in either handoff table at all, creating a referenced relationship with no defined artifact exchange.",
      "example_rewrite": "| Receives From | Artifact | Format | Frequency |\n|---|---|---|---|\n| CSO | Signed-off Company OKRs for the quarter | Written memo with ranked Objectives (max 5) and 2–4 KRs each | Once per quarter, Week 1 |\n| Department Heads | Draft Department OKRs | Completed OKR template (Google Doc, standard template v1) | Week 2 of planning cycle |\n| All Teams | Weekly confidence scores (1–10) per KR | Form submission via tracking tool | Every Monday by 10am |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "This role file contains NO anti-patterns section whatsoever. The template standard explicitly requires 3–5 role-specific anti-patterns, and this section is entirely absent. The DO/DON'T boundary list in the Boundaries section is a boundary enforcement list, not an anti-pattern list. Anti-patterns describe failure modes — behaviors the role might drift into that look reasonable but cause harm — which is categorically different from boundary statements like 'Don't set strategic priorities.' This is a critical omission, not a quality issue.",
      "example_rewrite": "## Anti-Patterns\n\n| Anti-Pattern | What It Looks Like | Why It Fails |\n|---|---|---|\n| **OKR Theater** | Facilitating goal-setting sessions that produce perfectly formatted OKRs nobody tracks after Week 2 | Process compliance substitutes for actual accountability; coordinator measures session completion, not behavioral change |\n| **Cascading Without Connecting** | Publishing department OKRs that technically align to company OKRs on paper but have no shared dependencies mapped | False alignment; teams optimize locally while company objective stalls |\n| **Consensus Paralysis** | Extending planning cycles to achieve full stakeholder agreement on every KR | Planning becomes the work; quarter starts 3 weeks late with stale goals |\n| **Coordinator as Goal Setter** | Suggesting specific KR targets when teams are uncertain, then tracking against those numbers | Crosses into Managers' and Heads' domain; teams feel no ownership of goals the coordinator effectively wrote |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol loop exists and is structurally correct, but it provides no operational starting point for an AI agent. The Context Requirements section — which should specify what inputs an AI needs before beginning any task — contains literal placeholder text '[Context item 1]' and '[Context item 2]' that was never filled in. The Required Skills table is also empty with a placeholder instruction. An AI loading this role cannot determine: what documents to request before starting a planning session, what questions to ask the human operator first, what tool or dashboard format to use for tracking, or how to distinguish between its tasks (tracking, reporting, drafting) versus human tasks (facilitating, coaching, conflict resolution).",
      "example_rewrite": "### Required Context (Before Starting Any Task)\n- [ ] Current quarter company OKRs (signed off by CSO)\n- [ ] Department OKR drafts from all Heads (or confirmation that planning cycle is in Week 1 — pre-draft)\n- [ ] Previous quarter final scores and retrospective notes\n- [ ] Tracking tool access confirmation (specify: Notion / Linear / Sheets)\n- [ ] List of active departments and their designated OKR leads\n\n### AI Operating Rules\n- AI NEVER drafts OKR content without receiving strategic input artifact from CSO first\n- AI flags any KR that lacks a numeric or binary measurable target before publishing\n- AI escalates to human operator if two department OKRs claim ownership of the same KR metric"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix names Story Portal-specific terms (Love Burn, MVP) which is a positive signal, but the content remains surface-level and non-actionable. The OKR Examples table lists objective titles with no key results, no owners, no success criteria, and no time horizons — making them useless as actual planning inputs. The Planning Priorities table ranks four items but provides no rationale for the ranking, no current status, and no decision on how priority conflicts between items 1 and 2 should be resolved. A coordinator loading this role cannot begin a planning session using this appendix as a reference.",
      "example_rewrite": "### Active Company OKRs — Q1 2025 (Example Structure)\n| Objective | Key Result | Owner | Target Date | Current Status |\n|---|---|---|---|---|\n| Launch Love Burn successfully | 500 registered users at launch event | CSO | March 15 2025 | Not started |\n| Launch Love Burn successfully | NPS ≥ 45 from post-event survey | Head of Product | March 22 2025 | Not started |\n| Complete MVP feature set | All P0 features QA-passed | Head of Engineering | Feb 28 2025 | In progress — 60% |\n\n### Planning Conflict Rule\nIf MVP completion (Priority 2) threatens Love Burn timeline (Priority 1), coordinator escalates to CSO within 24 hours with a written options memo — not a meeting request."
    }
  ],
  "top_improvement": "Add the missing Anti-Patterns section immediately — this is not a quality gap but a complete section omission that violates the template standard. A role with no anti-patterns gives an AI agent no failure mode awareness, meaning it will drift into OKR Theater (facilitating process with no accountability follow-through) or Goal Setting Creep (crossing into CSO and Department Head domains) without any guardrails. Draft 4 role-specific anti-patterns before addressing any other dimension."
}
```