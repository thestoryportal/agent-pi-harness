```json
{
  "role": "product-operations-manager",
  "department": "product",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 4,
    "anti_pattern_quality": 5,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic operational platitudes applicable to any ops role in any industry. 'Enable, Don't Block', 'Process Serves People', and 'Continuous Improvement' could be copy-pasted into a DevOps Manager, HR Ops, or Finance Ops role without changing a word. None of the principles reflect the specific tension of a Product Ops Manager sitting between PM strategy and engineering execution, or the challenge of maintaining operational discipline in a fast-moving product org at MVP stage.",
      "example_rewrite": "Replace generic principles with role-specific ones. Example — instead of 'Process Serves People: Processes exist to help, not create bureaucracy', use: 'Shield PMs from Operational Drag: Every hour a PM spends in Jira housekeeping, permission requests, or status formatting is an hour stolen from discovery. My job is to absorb that overhead so PMs never touch it.' Or instead of 'Continuous Improvement', use: 'Ops Debt Compounds Silently: An undocumented process is a process that will break the moment its creator leaves. I treat documentation gaps with the same urgency PMs treat critical bugs.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs are critically vague on both sides. 'Receives: Operational priorities from CPO' and 'Delivers: Tools, processes, documentation to Product Team' describe categories, not artifacts. There is no specification of format, trigger, or named artifact. The collaboration table says 'Process support, tool support' for Product Managers, which is a job description, not a handoff. The IT Manager appears in the handoff table as a sender but does not appear in the Works With table, suggesting a possible charter-inconsistency. No handoff specifies the file, document, or structured output being exchanged.",
      "example_rewrite": "Replace vague handoff rows with artifact-specific entries. Example — instead of 'Receives From: Chief Product Officer | Artifact: Operational priorities', rewrite as: 'Receives From: Chief Product Officer | Artifact: Quarterly Ops Priority Brief (written doc or Slack brief) naming top 3 operational focuses, budget constraints, and any new tool approvals — received at start of each quarter and before major milestones.' Instead of 'Delivers To: Product Team | Artifact: Tools, processes, documentation', rewrite as: 'Delivers To: Product Managers | Artifact: Sprint Readiness Checklist — a per-sprint GitHub Issues board audit confirming labels applied, milestones assigned, and blockers tagged, delivered every Monday before standup.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 5,
      "finding": "Six anti-patterns are listed but most are generic enough to appear in any operations role ('Add process without value', 'Let documentation go stale', 'Over-complicate'). None of the anti-patterns reflect Product Ops-specific failure modes such as: becoming a shadow PM by making prioritization calls during backlog grooming, tool-proliferating by adopting vendor demos without PM buy-in, or creating process theater — running ceremonies that produce no decisions. The 'Operate in isolation' anti-pattern is particularly generic and applies to every role in any organization.",
      "example_rewrite": "Replace generic entries with Product Ops-specific failure modes. Example — instead of 'Operate in isolation | Miss needs | Stay close to team', use: 'Becoming a Shadow PM | Anti-Pattern: When a PM is unavailable, filling the vacuum by making scope or priority calls during backlog grooming or stakeholder syncs. | Why it fails: Erodes PM authority and creates conflicting signals to engineering. | Instead: Escalate to PM async with a clear decision request; block the ceremony if no PM proxy is available.' Add: 'Tool Proliferation Theater | Anti-Pattern: Piloting three roadmap tools simultaneously because different PMs have preferences. | Why it fails: Fragments data, creates reconciliation work, and signals operational immaturity to stakeholders. | Instead: Force convergence to one tool per function; document the decision and close evaluations formally.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Hybrid classification is correctly applied and the iteration protocol is present with a clear STOP/WAIT/HALT loop. The AI vs Human split is reasonably articulated. The role scores above threshold, but loses points because the skill files listed in Context Requirements are marked as 'planned development' and do not exist, meaning an AI agent loading this role has no actual skills to pull. Additionally, the iteration protocol does not specify what format the AI should use when presenting a proposal at STOP point 2 — leaving the AI to invent its own output format.",
      "example_rewrite": "Add a proposal format to the iteration protocol STOP point. Instead of '2. STOP → Present proposal', specify: '2. STOP → Present proposal as: [Problem Statement 1 sentence] | [Proposed Change with affected tool or process named] | [Estimated effort: Low/Med/High] | [Rollback plan if it fails] | [Approval needed from: role name]. Do not proceed until explicit approval received.' Also flag the missing skill files more urgently — note that until skill files exist, the AI should rely on role definition context only and should not attempt to simulate the missing skill file content."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is better than most — it names the actual tool stack, acknowledges the MVP state honestly, and lists 5 concrete priorities. However, the priorities are still vague ('Establish basic issue tracking workflow' without defining what that workflow is), the Communication tool is listed as TBD with no owner or timeline, and the 'festival preparation' context appears without any explanation of what festival this refers to, what it means operationally, or what the ops risks are. An AI agent reading this appendix cannot infer what 'festival prep review' entails or why it requires weekly cadence.",
      "example_rewrite": "Add one sentence of operational context per priority and define the festival. Example — Priority 4 'Coordinate festival preparation' should read: 'Coordinate festival preparation — Story Portal's first public demo event [name/date if known]. Ops responsibilities include: ensuring GitHub Issues board is cleared of critical bugs before event date, preparing a read-only demo environment checklist, and establishing a war-room communication channel for day-of issues. Weekly review checkpoint: every [day] until event.' Also resolve the TBD communication tool: 'Communication: Slack [pending workspace creation] — blocked on IT provisioning, owner: CPO, target: [date].'"
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. Every handoff currently names a role and a category ('Operational priorities', 'Tool and process needs') but zero handoffs specify a named artifact, format, trigger condition, or delivery cadence. In a Hybrid role where AI drafts documentation and the human manages relationships, ambiguous handoffs mean the AI will either over-produce (generating unrequested reports) or under-produce (waiting for instructions that never arrive in a recognized form). Rewrite every handoff row to answer: what is the exact artifact, what format is it in, what triggers the exchange, and who confirms receipt."
}
```