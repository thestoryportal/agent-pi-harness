```json
{
  "role": "investor-relations-manager",
  "department": "finance-investor-relations",
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
      "finding": "All six principles are generic platitudes that could apply to any communications role, a customer success manager, or a PR function. 'Transparency Builds Trust' and 'Consistency Is Key' carry zero IR-specific meaning. There is no principle addressing the tension between full disclosure and material non-public information (MNPI), the discipline of managing investor expectations vs. reality, or the craft of delivering bad news without triggering panic. The meanings column (e.g., 'Honest communication wins') adds no operational guidance.",
      "example_rewrite": "| **Bad News First** | When performance misses, lead with the miss and the recovery plan before highlights — investors who discover problems you downplayed become ex-investors. Negative surprises destroy IR credibility faster than the underlying miss. | | **Expectation Discipline** | Never let investor mental models run ahead of company reality. Correct inflated expectations proactively in writing, not reactively in a board meeting. | | **MNPI Firewall** | Treat every investor conversation as potentially discoverable. Nothing material is shared selectively — if one investor hears it, all investors hear it simultaneously or no one does. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but describe artifacts at the category level only ('Messaging guidance,' 'Financial results,' 'Metrics and forecasts'). No artifact format, file type, naming convention, or expected completeness state is specified. 'Messaging guidance' from the CFO could mean a one-line Slack message or a structured brief — the AI cannot distinguish. Outbound deliverables to 'Investors' and 'Board' are not scoped to named document types. The roles 'Legal' and 'Marketing' appear in the Works With table but are absent from handoffs entirely despite being listed as boundary owners.",
      "example_rewrite": "| Receives From | Artifact | Format | Completeness Gate | | CFO | Quarterly messaging brief | Written doc, CFO-signed-off Google Doc | Must include: approved narrative on misses, forward guidance bounds, topics explicitly off-limits | | Controller | Monthly actuals package | Excel or Google Sheet, locked for editing | Must include: P&L, cash position, runway calculation, prior-period comparison | | FP&A Analyst | KPI dashboard | Looker/Sheets export, PDF snapshot | Must include: 13-week cash, MoM growth, burn multiple, labeled as DRAFT or FINAL |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There are zero anti-patterns in this role file. The section does not exist. The DO/DON'T boundary list is a scope-of-authority list, not a behavioral anti-pattern list. Anti-patterns for an IR Manager would include: over-promising metrics to maintain investor enthusiasm, sending updates without CFO approval because the cadence deadline is pressing, selectively sharing positive news with lead investors before others, burying bad news in the middle of a long update, or allowing investor questions in a board meeting to be answered ad-hoc without prepared responses. None of these appear anywhere in the document.",
      "example_rewrite": "### Anti-Patterns to Avoid | Anti-Pattern | Why It Fails | Correct Behavior | | **Enthusiasm Inflation** | Framing mediocre metrics as strong to keep sentiment positive — investors calibrate future expectations on your language; inflation now means credibility loss later | State actuals plainly, then provide context and plan | | **Approval Bypass** | Sending an investor update on deadline without CFO sign-off because 'it's mostly the same as last month' — one unapproved sentence about forward guidance creates legal and relational liability | Hard stop at CFO approval gate; delay send if needed | | **Selective Positivity** | Leading with wins and footnoting misses — sophisticated investors read the footnotes first; burying bad news signals weak management | Lead with variance to plan, then narrative |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The iteration protocol exists and is structurally sound, but the Context Requirements section is left entirely as unfilled placeholders ('[Context item 1]', '[Context item 2]', '[Use placeholder format: skill-name.md]'). An AI agent loading this role has no idea what context files to load, what investor data to reference, or what the current fundraising stage or investor list looks like. The workflows have STOP points but do not specify what the AI produces vs. what the human produces within each step. 'Draft investor update' — does the AI draft a full narrative or populate a template? The classification correctly separates AI vs. human duties in Deployment Notes but that guidance is not echoed inside the workflow steps themselves.",
      "example_rewrite": "### Required Context | Context Item | File | Why Required | | Current investor list | investor-database.csv | AI must address updates to correct investor names and tiers | | Approved messaging brief | cfo-messaging-brief-[quarter].md | AI drafts must stay within approved narrative bounds | | Prior investor update | investor-update-[prior-month].md | Consistency check; AI flags any metric that changed >20% without explanation | | Board deck template | board-deck-template.pptx | AI populates slides 3–7; human writes slide 1 (narrative) and slide 8 (ask) |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix acknowledges the pre-seed/seed stage but offers no Story Portal-specific operational guidance. The key metrics table lists 'Runway,' 'Progress,' 'Engagement,' and 'Team' with one-word relevance labels — these are the same four metrics every pre-seed IR role would list and provide no Story Portal product context. There is no mention of what Story Portal's current runway is, who the named angels or early VCs are, what MVP milestones are being tracked, or what the current fundraising narrative is. The communication cadence table is a generic startup cadence. The appendix reads as a placeholder with stage labels inserted rather than a genuine project-specific configuration.",
      "example_rewrite": "### Story Portal IR Configuration | Item | Detail | | Current stage | Pre-seed, building toward Seed raise in Q3 2025 | | Named investors | [Angel 1], [Angel 2], [Lead VC contact] — maintain individual relationship logs | | Board composition | CEO, CFO, 1 independent; quarterly cadence, materials due 5 days prior | | MVP milestone being reported | AI role deployment count, active enterprise pilots, Story Portal session volume | | Fundraising narrative | 'Enterprise AI workforce operating system — the only platform with role-level governance' | | Current runway | [X] months as of [date] — flag in every update, never omit | | Sensitive topics this cycle | [e.g., delayed pilot conversion, team change] — coordinate framing with CFO before any mention |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4–5 IR-specific behavioral failure modes (e.g., approval bypass, enthusiasm inflation, selective disclosure). This role file currently has zero anti-patterns, which is the single largest gap — it means an AI agent has no guardrails against the exact mistakes that destroy investor relationships and create legal liability."
}
```