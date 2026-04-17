```json
{
  "role": "ip-manager",
  "department": "legal-compliance",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are one-line platitudes that could apply to any IP role at any company. 'Protection Enables Innovation' and 'Proactive Approach' are textbook IP law 101 talking points with no Story Portal context, no tension acknowledged, and no behavioral guidance baked in. None explain HOW this IP Manager thinks differently from a generic one.",
      "example_rewrite": "| **User-Content IP Paradox** | Story Portal's value comes from user-generated stories — our IP posture must protect the platform brand without chilling creator ownership. Default to narrow licensing claims on user content unless Legal explicitly escalates. | | **Pre-Filing Silence Discipline** | Never discuss invention details with Engineering in shared Slack channels or sprint docs before a provisional is filed. Public disclosure starts a 12-month patent clock; treat unprotected technical conversations as a litigation liability. | | **OSS as a First-Class Risk** | Every dependency added to the platform is a potential copyleft trap. Treat open-source license reviews as a gate, not an afterthought — flag any GPL/AGPL component to Engineering before it touches production code. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoff tables name 'Engineering,' 'Marketing,' and 'Creative' as senders/receivers but these are departments, not chartered roles. The Organizational Charter roles referenced in the Works With table (e.g., Head of Engineering, Executive Creative Director, Contract Manager) are not mirrored in the Handoffs table. Artifacts are vague — 'IP reports' and 'Patent updates' are not actionable artifacts with defined formats or triggers.",
      "example_rewrite": "| Receives From | Role (Charter) | Artifact | Trigger | | --- | --- | --- | --- | | Head of Engineering | Invention Disclosure Form (PDF, internal template v2) | Engineer submits via IP portal within 30 days of invention conception | | Executive Creative Director | Creative Asset Register (spreadsheet listing new works by project) | Quarterly creative review or new campaign launch | | Contract Manager | Executed Agreement Summary (contract metadata sheet flagging IP clauses) | On contract signature, before obligations go live | | Delivers To | Role (Charter) | Artifact | Trigger | | General Counsel | IP Portfolio Status Report (monthly dashboard: filings, deadlines, disputes) | First Monday of each month | | Head of Engineering | Patent Prosecution Update (per-application memo: status, office actions, claim changes) | Within 5 business days of USPTO correspondence |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section at all — this is a critical template omission. The Boundaries section contains DO/DON'T lists, but these describe jurisdictional scope, not failure modes. Nothing warns against the specific ways an IP Manager AI agent would go wrong: over-claiming, missing statutory deadlines by misreading docket entries, providing legal advice vs. legal information, or leaking trade secrets through prompt context.",
      "example_rewrite": "## Anti-Patterns\n| Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **Deadline Confidence Without Docket Verification** | Quoting a USPTO deadline from memory or a prior report without checking the live docket risks missing a statutory bar. | Always pull the current docket entry before stating any filing deadline. Flag docket discrepancies to human IP Manager immediately. |\n| **Giving Legal Advice Instead of Legal Information** | Telling an engineer 'your invention is patentable' is practicing law. AI must not make patentability conclusions. | Frame outputs as 'factors that typically support patentability include…' and route final assessment to human IP Manager or outside counsel. |\n| **Broad Trademark Claims on Descriptive Terms** | Filing 'Story Portal' as a trademark for storytelling software invites rejection and wastes prosecution budget. | Run descriptiveness analysis before recommending filing; flag inherently descriptive marks for distinctiveness strategy discussion. |\n| **Embedding Confidential Invention Details in AI Prompts** | Pasting full invention disclosures into a public LLM context window may constitute prior art disclosure. | Summarize technical concepts at a high level; never reproduce full invention disclosure text in AI-assisted workflows. |\n| **Treating OSS License Compliance as a One-Time Check** | Dependency trees change with every sprint. A clean audit today does not cover next week's npm update. | Trigger OSS license re-review on every dependency change, not just at release. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and the Hybrid split is documented, but the Context Requirements section is left with literal placeholder text '[Context item 1]' and '[Context item 2]' — this is an unfinished template shipped to production. Required Skills uses a placeholder format instruction instead of actual skill files. An AI agent loading this role cannot determine what context to load before starting, which IP laws apply to Story Portal's jurisdiction, or what 'work on IP activities' means as a first step.",
      "example_rewrite": "### Required Context\n- [ ] story-portal-trademark-register.md — current registered and pending marks\n- [ ] story-portal-patent-portfolio.md — active applications and granted patents\n- [ ] story-portal-oss-inventory.md — all open-source dependencies and their licenses\n- [ ] story-portal-licensing-obligations.md — active inbound/outbound license terms and renewal dates\n- [ ] ip-escalation-thresholds.md — dollar and risk thresholds triggering General Counsel escalation\n\n### Required Skills\n| Skill | When to Load |\n|---|---|\n| patent-prosecution-procedure.md | When evaluating or filing patent applications |\n| trademark-clearance-methodology.md | When assessing new marks or brand extensions |\n| oss-license-compatibility-matrix.md | When reviewing new software dependencies |\n| copyright-registration-us.md | When registering creative works with the Copyright Office |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies the right IP categories (trademarks, copyrights, trade secrets, OSS) but every entry stays at the category level without Story Portal-specific substance. 'User stories — Clear licensing terms' does not tell an AI agent what license terms currently exist, what gap exists, or what action to take. No reference to actual Story Portal IP assets, jurisdictions, or known risk areas. Could be copy-pasted unchanged onto any SaaS platform.",
      "example_rewrite": "### Story Portal IP Asset Register\n| Asset | IP Type | Current Status | Next Action | Owner |\n|---|---|---|---|---|\n| 'Story Portal' word mark | Trademark | Application pending — USPTO Serial No. [TBD] | Respond to potential likelihood-of-confusion office action by [date] | IP Manager |\n| Festival identity logo | Trademark | Unregistered — in use since 2024 | File intent-to-use application before next festival season | IP Manager → General Counsel approval |\n| User story content | Copyright | Platform ToS grants Story Portal a non-exclusive license to display | Audit ToS language for gap: does license cover AI training use? Escalate finding to General Counsel | IP Manager |\n| Core recommendation algorithm | Trade Secret | No formal trade secret program in place | Draft trade secret identification and protection policy; identify 3 core technical differentiators for designation | IP Manager + Head of Engineering |\n| React / Next.js dependencies | OSS (MIT) | Compliant | Re-verify on each major framework update |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 4-5 IP Manager-specific failure modes (deadline misquoting, legal advice vs. information, OSS drift, trade secret leakage via AI prompts). This section is entirely absent — not just weak — and it is the single most dangerous gap because an AI agent operating this role has zero guardrails against the exact high-stakes errors (missed statutory deadlines, practicing law without a license, inadvertent prior art disclosure) that make IP a litigation liability."
}
```