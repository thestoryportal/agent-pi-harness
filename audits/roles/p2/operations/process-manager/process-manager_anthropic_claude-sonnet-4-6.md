```json
{
  "role": "process-manager",
  "department": "operations",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are generic management platitudes that could appear in any operations textbook. 'Simplicity Wins', 'Measure To Improve', and 'Continuous Improvement' carry zero role-specific meaning — they say nothing about how a Process Manager at Story Portal specifically thinks. The meaning column compounds the problem by restating the principle in two words ('Good process multiplies', 'Always getting better') instead of explaining operational stance.",
      "example_rewrite": "| **Festival-First Triage** | When two processes compete for design bandwidth, the one blocking a live festival deployment takes priority — community and partner processes queue behind it | \n| **Document Before You Optimize** | Never redesign a process that lacks a current-state map; optimization without baseline is guesswork and destroys audit trails | \n| **Adoption Rate Is the Real Metric** | A theoretically perfect process with 40% adoption is worse than a mediocre process at 95% — design for the humans who will actually follow it, not the ideal actor |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoff artifacts are named at the level of categories, not actual deliverables. 'Process requests', 'Process priorities', and 'Optimized processes' tell an AI agent nothing about what file, format, or structured output changes hands. The delivers-to row for Documentation Specialist says 'Process content' — this could mean a rough notes email or a fully structured BPMN diagram. Role names in the Works With table are listed but the interface column ('Strategy and priorities', 'Technology enablement') describes topics, not interaction mechanics.",
      "example_rewrite": "| Delivers To | Artifact | Format |\n|-------------|----------|--------|\n| Documentation Specialist | Validated process narrative with step-by-step flow, owner per step, and exception paths | Confluence draft page using Process Doc Template v2 |\n| COO | Monthly Process Health Report: adoption rates, cycle time deltas, open audit findings, and top 3 improvement recommendations | PDF + Notion dashboard link |\n| All Departments | Future-state BPMN diagram + Implementation Runbook (roles, dates, training requirements) | Lucidchart export + Asana project |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file. The template standard explicitly requires 3-5 role-specific anti-patterns, and this section is entirely absent. The DON'T list in Boundaries is not a substitute — it lists domain boundaries ('Don't own department processes'), not behavioral failure modes. This is the most critical structural gap in the document.",
      "example_rewrite": "## Anti-Patterns\n\n| Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **Mapping for mapping's sake** | Producing 40-step BPMN diagrams nobody reads; process documentation becomes the goal instead of process execution | Map only to the level of detail required for consistent handoffs — if a step has one owner and no decision gate, one line is enough |\n| **Redesigning without data** | Launching a future-state redesign based on stakeholder complaints alone, without cycle time or error rate baselines | Gather at least 30 days of performance data before proposing structural changes |\n| **Change without champions** | Rolling out a new festival deployment process by sending a Confluence link; adoption fails because no department head co-owns it | Identify and brief a department-side champion before any implementation kickoff |\n| **Optimizing an orphaned process** | Improving a partner onboarding sub-process without confirming the parent workflow hasn't already been flagged for replacement by the COO | Always check the Process Roadmap in Notion before scoping an optimization request |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and is structurally correct, but the Required Context section contains literal placeholder text ('[Context item 1]', '[Context item 2]') and the Required Skills table is empty with only a format note. An AI agent loading this role cannot determine what context files to load, what skills to activate, or what constitutes a valid trigger for each workflow. The STOP points in workflows do not specify what output the human is reviewing or what approval criteria must be met before proceeding.",
      "example_rewrite": "### Required Context\n- [ ] org-charter.md — confirms reporting line to COO and referenced role names\n- [ ] process-library.md — current state maps for all active Story Portal processes\n- [ ] festival-calendar.md — upcoming deployment dates that affect process change freeze windows\n- [ ] partner-onboarding-sop.md — baseline for onboarding optimization requests\n\n### STOP Point Criteria (Workflow 1, Step 2)\nSTOP → Design ready\nHuman must confirm: (1) stakeholder sign-off documented in Notion, (2) implementation effort estimated in story points, (3) no active festival deployment within 14 days of proposed go-live. AI does not proceed to IMPLEMENT until all three are marked complete."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix names four relevant areas (Festival Operations, Community Management, Partner Onboarding, Content Workflow) but provides no actionable specifics. Process priorities are ranked 1-4 without any rationale, owner, or current-state assessment. 'Festival deployment — Event execution' repeats the label as the description. There are no links to existing process assets, no cycle time targets, no known pain points, and no indication of which processes exist versus which need to be built.",
      "example_rewrite": "### Key Processes — Story Portal\n\n| Process | Current State | Known Pain Point | Priority Metric |\n|---------|--------------|-----------------|----------------|\n| Festival Deployment | Informal checklist in Slack; no single owner per stage | Venue coordination steps missed 2 of last 3 festivals | Zero missed handoffs per event |\n| Partner Onboarding | Partially documented in Confluence; 3 conflicting versions | Average onboarding takes 18 days; target is 10 | Time-to-first-story < 10 days |\n| Story Submission Workflow | Defined in Notion but not enforced; editors bypass intake form | ~30% of submissions skip editorial triage | Intake compliance > 90% |\n| Community Moderation | Undocumented; handled ad hoc by community leads | No escalation path; COO pulled into routine flags | Escalation rate to COO < 5% of flags |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific failure modes. This is the single highest-priority fix because the section is entirely missing — not weak, absent — and anti-patterns are the primary mechanism that prevents an AI agent from drifting into adjacent roles (rewriting documentation, making strategic redesign calls, or implementing technology changes). Without them, every boundary stated in the DON'T list will be violated under ambiguous task conditions."
}
```