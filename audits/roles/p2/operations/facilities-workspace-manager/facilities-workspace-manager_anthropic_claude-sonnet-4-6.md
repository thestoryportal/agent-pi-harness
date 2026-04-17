```json
{
  "role": "facilities-workspace-manager",
  "department": "operations",
  "scores": {
    "philosophy_depth": 2,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 4,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 2,
      "finding": "All six principles are generic platitudes that could apply to any facilities role at any company anywhere. 'Safety First' and 'Comfort Matters' are industry clichés. None reference Story Portal's specific context: festival infrastructure cycles, a distributed/remote-first team, or community event cadence. There is zero role-specific philosophy — these could be copied from a WeWork brochure.",
      "example_rewrite": "Replace generic principles with role-specific ones: | **Festival-First Readiness** | Facilities planning runs on the festival calendar — every workspace decision accounts for the surge periods when the team triples in intensity and on-site infrastructure must be pre-staged 30 days out. | **Remote-Parity Standard** | A distributed team member must never experience fewer environmental affordances than an in-office peer — home office stipends, async-friendly room booking, and virtual collaboration tooling are treated as facilities responsibilities, not IT perks. | **Vendor Relationship as Operational Insurance** | Single-vendor dependencies for critical systems (HVAC, AV, cleaning) are treated as risk events — every critical service has a qualified backup vendor on contract before a primary failure occurs. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoff tables name artifacts in the vaguest possible terms: 'Space requests', 'Workspace services', 'Facility reports'. No artifact has a format, template name, or defined field set. 'Vendor Manager' is listed as a collaboration partner but does not appear to be a named role in a standard operations charter — this may be a hallucinated role. Receives/Delivers tables do not specify trigger conditions, frequency, or what 'done' looks like for a handoff.",
      "example_rewrite": "| Delivers To | Artifact | Format | Trigger | \n|-------------|----------|--------|---------| \n| COO | Monthly Facility Health Report | Standardized PDF dashboard — sections: space utilization %, open maintenance tickets, safety incidents, vendor SLA compliance, budget vs. actuals | First Monday of each month | \n| HR | New Hire Workspace Readiness Checklist | Completed checklist confirming desk assigned, access badge issued, equipment provisioned, emergency exits briefed | 48 hours before employee start date | \n| Event Marketing Manager | Event Space Setup Brief | Room layout diagram, AV configuration, catering logistics, capacity compliance sign-off | 5 business days before each community event |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There are no anti-patterns section in this role file at all — the template standard requires 3-5 role-specific anti-patterns and none were written. The DO/DON'T boundary list exists but reads as generic scope boundaries, not behavioral failure modes. There is no section titled Anti-Patterns and no examples of how this specific role typically fails in practice.",
      "example_rewrite": "Add an Anti-Patterns section: **Anti-Pattern 1 — Festival Tunnel Vision:** Treating festival season as the only planning horizon and deferring routine maintenance, vendor contract renewals, and remote-work infrastructure upgrades until 'after the festival' — resulting in cascading failures when the next cycle begins. **Anti-Pattern 2 — Reactive-Only Maintenance:** Waiting for team complaints to surface space problems instead of running proactive utilization audits monthly; the first signal of a broken environment should never be a Slack message from a frustrated employee. **Anti-Pattern 3 — Scope Creep into IT:** Purchasing, configuring, or troubleshooting network hardware, software licenses, or device management because 'it's in the office' — this erodes the IT Manager boundary and creates accountability gaps when systems fail. **Anti-Pattern 4 — Unilateral Space Decisions:** Redesigning or repurposing shared spaces without a documented needs assessment and COO sign-off, even for changes that seem minor — workspace changes affect every department's workflows."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Iteration Protocol exists and follows the correct LOOP structure, which is good. However, the Required Context section contains literal placeholder text '[Context item 1]' and '[Context item 2]' — this is an unfilled template that would leave an AI agent with no idea what context files to load. Required Skills table is also empty with only a format hint. The AI/human division of labor is stated but vague: 'AI assists with scheduling' and 'AI generates reports' without specifying what scheduling system, what report template, or what triggers an AI action versus a human action.",
      "example_rewrite": "Replace placeholder Required Context with: | Context | File | When Required | \n|---------|------|---------------| \n| Festival calendar and key dates | festival-calendar-2025.md | Always loaded — all facilities planning references this | \n| Office floor plan and room inventory | office-space-inventory.md | Load when handling space requests or utilization reports | \n| Active vendor contracts and SLA terms | vendor-contracts-summary.md | Load when managing vendors or escalating service failures | \n| Remote work equipment policy | remote-work-policy.md | Load when processing equipment requests or home office support | \nAnd rewrite AI trigger: 'TRIGGER FOR AI ACTION: When a space request is submitted, AI pulls current room availability from space management platform, cross-references festival calendar for conflicts, and drafts a Space Assignment Confirmation for human review before sending.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix acknowledges the right context categories (festival, remote, community events) but provides no actionable specifics. 'Festival infrastructure support' is Priority 1 but there is no detail about what that means — what infrastructure, what timeline, what vendors, what the failure mode is. The appendix reads as a generic categorization exercise rather than genuine project context. No specific festival names, event cadences, team size, or geographic context is referenced.",
      "example_rewrite": "Rewrite Facility Priorities with specificity: | Priority | Focus | Concrete Action | Success Metric | \n|----------|-------|-----------------|----------------| \n| 1 | Festival infrastructure support | 30-day pre-festival checklist: confirm on-site power, AV, seating, and vendor access credentials are staged; conduct walkthrough with Event Marketing Manager | Zero day-of infrastructure failures during festival weekend | \n| 2 | Team workspace optimization | Run quarterly utilization audit using room booking data; identify underused spaces and repurpose within 60 days | Office space utilization rate above 70% on peak days | \n| 3 | Remote work enablement | Process all remote equipment requests within 3 business days; conduct semi-annual home office stipend review with HR | Remote team satisfaction score above 8/10 on quarterly pulse | \n| 4 | Community event spaces | Maintain a pre-configured event layout for the main gathering space that can be deployed in under 2 hours for pop-up community events | Event setup completed within 2-hour target 95% of the time |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 4 role-specific behavioral failure modes — this section is entirely missing and is a required template component. Without it, neither a human reviewer nor an AI agent has guidance on how this role characteristically fails, making quality control impossible. The current DO/DON'T boundary list does not substitute for anti-patterns, which must describe failure behaviors, not just scope lines."
}
```