```json
{
  "role": "implementation-specialist",
  "department": "client-services",
  "scores": {
    "philosophy_depth": 2,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 3,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 2,
      "finding": "All six principles are generic platitudes that could apply to any technical role in any industry. 'Technical Excellence = Quality configuration' and 'Minimal Friction = Smooth onboarding' are tautologies, not guiding philosophy. None of the principles provide behavioral guidance specific to the tensions an Implementation Specialist actually faces — e.g., speed-vs-quality tradeoffs at go-live, client pressure to skip validation, or scope creep during configuration.",
      "example_rewrite": "| **Validate Before You Migrate** | Never execute a data migration without a signed-off mapping document and a dry-run report. Client urgency does not override data integrity — a corrupted migration costs 10x more to fix than a delayed one. | | **Config Is a Contract** | Every platform setting changed is documented before the change is made, not after. If it isn't written down, it didn't happen — and the CSM inheriting this client will need that record. | | **Go-Live Is Not Done Until the Client Says It's Done** | The Specialist does not close a launch until the primary client contact has confirmed success in writing. Internal confidence is not a substitute for client sign-off. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoff tables name roles correctly but the artifacts are vague one-liners. 'Configured platform' is a system state, not a deliverable artifact. 'Setup documentation' and 'Technical status' are generic labels with no format, template reference, or acceptance criteria. The receiving role (CSM) cannot act on 'Configured platform' — they need a specific handoff document. Additionally, the 'Receives From: Sales' row references a role not confirmed to exist in the charter, which is a hallucination risk.",
      "example_rewrite": "| Delivers To | Artifact | Format | Acceptance Criteria | | Client Success Manager | Implementation Handoff Package | Standardized handoff doc (implementation-handoff-v1.md) including: configured feature list, known limitations, training completion status, open items log | CSM countersigns within 48hrs of go-live | | Support | Setup Documentation | Config record per template (config-record-template.md) stored in shared drive | All integration endpoints, credentials location, and migration source documented | | Technical Account Manager | Technical Status Report | Structured status using (tech-status-template.md): blockers, resolved issues, outstanding risks | Delivered at go-live and at 30-day mark |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "This role file contains no Anti-Patterns section at all. The DO/DON'T boundary table is present but that is not the same as an anti-patterns section — it lists domain boundaries, not failure modes. There are zero role-specific anti-patterns documented, which is a critical omission per the template standard. An Implementation Specialist has well-known failure modes: skipping UAT to hit a deadline, migrating dirty data without client sign-off, configuring beyond agreed scope to please the client, and closing a launch without a formal handoff.",
      "example_rewrite": "## Anti-Patterns | Anti-Pattern | Why It Happens | Why It's Dangerous | Correct Behavior | |---|---|---|---| | **Go-Live Without Validation Sign-Off** | Client pressure, deadline proximity | Undiscovered data errors surface post-launch and become Support and CSM problems | STOP at Workflow 1 Step 3 — testing complete gate requires written client UAT sign-off before proceeding | | **Scope Creep Configuration** | Desire to help client, vague requirements | Undocumented config creates support black holes; CSM inherits unknown state | Any configuration request beyond the agreed implementation scope goes to Project Manager as a change request, not into the build | | **Verbal-Only Training** | Time pressure, client preference for informal sessions | No knowledge transfer record; client re-asks questions; CSM has no baseline | Every training session produces a written summary delivered to client and CSM within 24 hours |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 3,
      "finding": "The Context Requirements section is entirely unfilled — '[Context item 1]' and '[Context item 2]' are literal placeholders, and the Skills table has no entries. This means an AI agent loading this role has no idea what context files to load before starting work. The Iteration Protocol exists but is a generic loop with no role-specific trigger conditions. The AI/human split in the Hybrid section is described but never operationalized — there is no decision rule for when AI should stop and hand to human (e.g., 'if data anomaly rate exceeds X%, halt migration and escalate'). An AI agent loading this role cannot determine what to do on first task receipt.",
      "example_rewrite": "### Required Context | Context File | When Required | | client-requirements-brief.md | Load before any configuration task begins | | implementation-plan.md | Load before Workflow 1 Step 1 | | data-mapping-spec.md | Load before any migration task | | platform-config-template.md | Load before Build phase | | integration-spec.md | Load before Integration Setup responsibility | ### AI Decision Boundaries IF data anomaly rate > 5% during migration → STOP, generate anomaly report, escalate to human Specialist. IF configuration requirement is not in approved implementation plan → STOP, flag to Project Manager, do not configure. IF client requests training on undocumented features → STOP, log gap, route to Technical Account Manager."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix names relevant implementation types (festival deployment, partner onboarding, community launch) but provides no actionable specifics. 'Festival platform setup' as Priority 1 is a label, not a guide. There is no mention of Story Portal-specific configuration objects, data schemas, known integration partners, or what 'community data' actually consists of. An Implementation Specialist reading this section gains no additional knowledge about how Story Portal implementations differ from a generic SaaS implementation. The section reads as a placeholder with Story Portal nouns substituted in.",
      "example_rewrite": "### Story Portal Implementation Specifics | Implementation Type | Key Config Objects | Known Integration Partners | Data Migration Source | | Festival Deployment | Event taxonomy, stage schedule, artist profiles, ticketing tier config | Eventbrite, Dice, Festicket | Client-provided CSV via festival-data-template.xlsx | | Partner Onboarding | Partner profile, content permissions, revenue share rules, co-branding settings | Partner SSO (SAML 2.0), partner CRM | Partner sends contacts via partner-import-template.csv | | Community Launch | Community structure (groups, roles, permissions), moderation rules, welcome flows | None standard — confirm per client | Legacy forum exports (Discourse, Vanilla) or manual import | ### Festival Go-Live Checklist (Story Portal-specific) - [ ] Ticket scanner integration tested with at least 50 test scans - [ ] Artist profile images within 2MB limit (platform constraint) - [ ] Schedule published in draft mode and reviewed by client before public toggle"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 4-5 role-specific failure modes (skip validation, scope creep configuration, verbal-only training, premature launch closure) — this section is entirely missing and represents the highest safety risk for AI deployment, as an AI agent with no anti-patterns will optimize for task completion over correct process gates."
}
```