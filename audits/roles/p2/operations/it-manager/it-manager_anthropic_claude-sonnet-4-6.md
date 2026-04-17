```json
{
  "role": "it-manager",
  "department": "operations",
  "scores": {
    "philosophy_depth": 2,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 4,
    "story_portal_relevance": 3
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 2,
      "finding": "All six principles are generic IT platitudes that could apply to any IT role at any company. 'Reliability First: Systems must work' and 'Security Always: Protect the organization' are textbook filler — they carry zero actionable meaning. None of the principles reflect Story Portal's specific context (festival operations, distributed team, on-site event tech). The template standard explicitly flags 'Quality first means nothing' as a common mistake, and every single principle here commits that exact error.",
      "example_rewrite": "| **Festival-Day Zero Tolerance** | Festival day IT failures are unrecoverable — all critical systems (ticketing, comms, on-site coordination) must be validated and failover-tested 72 hours before gates open, not the morning of. | | **Access Ends at Offboarding** | Contractor and seasonal staff accounts are disabled the same day HR submits the offboarding request — no grace periods, no exceptions, because festival season brings high staff turnover and credential sprawl. | | **Shadow IT Is a Security Incident** | When a department adopts an unapproved SaaS tool, treat it as a security event requiring review, not a bureaucratic violation — because data lives in that tool now. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs name categories of artifacts ('IT requests', 'IT services', 'Security data') rather than actual named documents or deliverables. 'All Departments → IT requests' tells an AI agent nothing about format, urgency tier, or intake channel. 'Security → Security requirements' is circular — the Security Engineer role presumably has a named deliverable (e.g., 'Quarterly Security Requirements Brief'). 'Vendor Manager' appears in the Works With table but does not appear as a handoff partner despite being the most natural artifact exchange point for IT procurement.",
      "example_rewrite": "| Receives From | Artifact | Format | |\n|---|---|---|---|\n| HR | Onboarding/Offboarding Request | Standardized HR ticket via HRIS with role, start date, required access tier | |\n| Security Engineer | Quarterly Security Requirements Brief (PDF) | Specifies controls IT must implement next quarter | |\n| All Departments | IT Support Ticket | Submitted via helpdesk portal; triaged by severity (P1–P4) within 2 hours | |\n\n| Delivers To | Artifact | |\n|---|---|---|\n| COO | Monthly IT Health Report (dashboard + narrative PDF) | |\n| Security Engineer | Weekly Access Audit Log (CSV export from Identity Management) | |\n| All Departments | Resolved ticket with documented fix and knowledge base entry |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "The role file contains no dedicated Anti-Patterns section whatsoever. The DO/DON'T boundary table exists but lists boundary violations (e.g., 'Don't manage product infrastructure') rather than behavioral anti-patterns — patterns of how this role degrades in practice. The template standard requires 3–5 role-specific anti-patterns. A role this operational-heavy has well-known failure modes (e.g., treating every request as equal urgency, building undocumented workarounds, conflating IT policy with security strategy) that are entirely absent.",
      "example_rewrite": "### Anti-Patterns to Avoid\n\n| Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **The Heroic Workaround** | Resolving incidents with undocumented one-off fixes feels fast but creates invisible technical debt that breaks during festivals when no one remembers what was done. | Every incident resolution requires a knowledge base entry before the ticket closes. |\n| **Treating All Tickets as Equal** | Responding to 'my printer is slow' with the same urgency as 'payroll system is down' burns goodwill and misses actual crises. | Enforce P1–P4 SLA tiers strictly; P1 (system-wide outage) interrupts all other work. |\n| **Security Theater Over Security Practice** | Installing security tools and checking a compliance box without verifying they are configured, monitored, and alerting correctly. | Every deployed security control must have a documented alert owner and monthly validation test. |\n| **IT as Gatekeeper** | Blocking department tool requests for weeks in the name of review, forcing teams to adopt shadow IT instead. | Tool review SLA is 5 business days; default answer is conditional approval with guardrails, not denial. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Iteration Protocol exists (satisfying the Hybrid requirement) but is a generic loop with no role-specific triggers, thresholds, or decision criteria. The Required Context section contains literal placeholder text ('[Context item 1]', '[Context item 2]') and the Required Skills table is empty — these are unfilled template fields shipped in a v1.0 document. An AI agent loading this role cannot determine what context files to load, what constitutes a P1 escalation threshold, or when to stop autonomous action versus wait for human approval. The STOP points in workflows are present but the conditions for stopping are not defined (e.g., 'STOP → Monitoring active' is not a decision point, it is a status label).",
      "example_rewrite": "### Required Context\n- [ ] org-charter.md (to verify role boundaries before escalating)\n- [ ] it-incident-severity-matrix.md (P1–P4 definitions and SLA targets)\n- [ ] festival-it-runbook.md (on-site tech stack and failover procedures)\n- [ ] approved-vendor-list.md (for tool procurement decisions)\n- [ ] onboarding-offboarding-checklist.md (access provisioning steps)\n\n### Iteration Protocol\n```\nLOOP:\n  1. Pull open IT tickets; sort by severity tier\n  2. Work P1 incidents to resolution — NO autonomous action on security incidents; STOP → page human IT Manager immediately\n  3. For P2–P4: resolve and document fix in knowledge base\n  4. STOP → Weekly: generate IT Health Report draft and WAIT for human review before sending to COO\n  5. IF human approves report → send\n  6. IF new security alert detected → HALT all other tasks, ESCALATE to Security Engineer + COO\n  7. REPEAT\n```"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 3,
      "finding": "The Story Portal appendix names four areas (Team Systems, Festival IT, Security, Remote Work) and four priorities, but neither table contains any actionable content. 'Festival IT: On-site technology' and 'Priority 1: Festival IT readiness' are headings, not guidance. There is no mention of what on-site systems exist, what the festival tech stack looks like, what remote work tools the distributed team uses, or what 'readiness' means in measurable terms. An AI agent reading this appendix learns nothing about Story Portal that it could not infer from the role title alone.",
      "example_rewrite": "### Story Portal IT Context\n\n| Area | Specific Focus | Key Systems | Success Metric |\n|---|---|---|---|\n| **Festival Day Operations** | On-site ticketing, artist credential scanning, production comms | Ticketing terminals, walkie-talkie coordination platform, on-site Wi-Fi mesh | Zero ticketing system downtime during gates-open hours |\n| **Distributed Team Productivity** | Story Portal runs a remote-first team across multiple time zones | G Suite (primary), Slack, Notion, Zoom; all managed via IT | <4 hour helpdesk response SLA for all remote staff |\n| **Seasonal Staff Surge** | Festival season brings 50–200 temporary contractors needing scoped access | Identity management group: 'Festival-Seasonal' with auto-expiry 7 days post-event | 100% of seasonal accounts deprovisioned within 48 hours of event end |\n| **On-Site Network** | Festival venues have no reliable ISP; IT must provide portable network infrastructure | LTE bonding routers, backup hotspots, offline-capable ticketing fallback | Network available 99.5% of festival operating hours |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4 role-specific behavioral failure modes. This is the most critical gap because the role file currently has zero anti-patterns — not a weak section but a missing section — and anti-patterns are the primary mechanism by which an AI agent self-corrects during autonomous operation. Without them, the AI has no guardrails against the most common IT Manager failure modes (heroic workarounds, undifferentiated ticket urgency, security theater) that are especially dangerous in a festival operations context where failures are public and time-bounded."
}
```