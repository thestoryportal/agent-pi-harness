```json
{
  "role": "sales-director",
  "department": "sales",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 3
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic sales management platitudes that could appear in any sales leadership textbook. 'Execution Over Strategy' and 'Lead by Example' contain zero specificity to this role, this company, or this industry. There is no mention of Story Portal's specific sales context (festival partnerships, community sponsors), no principle about relationship longevity over transactional closes, and no principle reflecting the cultural or event-driven nature of the business. The Meaning column entries ('Results from doing', 'Develop the team') are single-phrase summaries that add no behavioral guidance.",
      "example_rewrite": "Replace generic principles with role-specific ones. Example: | **Partnership Over Transaction** | Story Portal deals are multi-year festival relationships — a closed deal that damages the partnership costs more than a lost deal. Never sacrifice trust for quota. | **Pipeline Honesty Beats Forecast Comfort** | An inflated pipeline misleads the CRO and destroys forecast credibility. Flag at-risk deals in the weekly forecast even when it hurts the number. | **Coaching Is the Multiplier, Not the Meeting** | A 30-minute deal coaching session that reframes a rep's strategy is worth more than joining the call yourself. Build rep capability, don't just close their deals for them. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoff artifacts are named at the category level, not the document level. 'Strategy and targets' from the CRO, 'Qualified opportunities' from SDRs, and 'Performance reports' to the CRO are all vague enough to be meaningless operationally. There is no specification of format (CRM record, spreadsheet, PDF brief), no field-level detail, and no indication of what 'qualified' means in the SDR handoff. The Client Services handoff for 'Closed deals' lacks any transition artifact name (e.g., customer handoff brief, signed contract package, onboarding intake form).",
      "example_rewrite": "Example rewrite for SDR handoff: | Receives From | Artifact | | SDRs | Qualified Opportunity Record — SFDC opportunity with: company name, primary contact + title, pain statement, budget indicator (confirmed/unconfirmed), next meeting booked, SDR notes field completed. Minimum 3x pipeline coverage maintained. | Example rewrite for Client Services: | Delivers To | Artifact | | Client Services | Closed Deal Handoff Package — includes signed agreement, deal summary (1-page), key stakeholder contacts, committed deliverables list, and 'promises made' notes from negotiation. Delivered within 48 hours of contract execution. |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "The role file has no dedicated Anti-Patterns section at all — it is entirely missing as a standalone section. The DON'T list in Boundaries partially substitutes but only addresses domain boundary violations (don't set strategy, don't design compensation), not behavioral failure modes. There are no patterns describing how this specific role commonly fails: carrying deals instead of coaching reps, over-forecasting to please the CRO, ignoring pipeline coverage in favor of chasing the current quarter's close, or bypassing Sales Ops process in urgent deals. These are the real failure modes for a Sales Director and none are captured.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: **Anti-Pattern 1 — Hero Closer:** Jumping into rep deals to close them personally rather than coaching the rep through it. Feels productive, creates rep dependency, doesn't scale. INSTEAD: Coach the rep on the next move, observe the call, debrief after. **Anti-Pattern 2 — Forecast Optimism:** Keeping deals in the forecast past their close date to avoid a difficult CRO conversation. Destroys forecast credibility within two quarters. INSTEAD: Flag slipping deals in the weekly review with a revised close date and a reason. **Anti-Pattern 3 — Pipeline Neglect in Q4:** Focusing entirely on closing current-quarter deals while letting top-of-funnel dry up. Results in Q1 pipeline crisis. INSTEAD: Protect at least 20% of weekly coaching time for early-stage pipeline review regardless of quarter."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Deployment Notes section correctly identifies Human-Primary classification and lists what AI assists with (reporting, administration, analytics), but provides no actionable instruction for how an AI agent should actually behave when loaded into this role. The Context Requirements section is left with literal placeholder text '[Context item 1]' and '[Context item 2]' — these were never filled in, which is a template completion failure. The Required Skills table is also blank with only a format note. An AI loading this role cannot determine what context files to load, what data sources to pull, or what its first action should be in any given trigger scenario.",
      "example_rewrite": "Replace placeholder Context Requirements with specifics: **Required Context:** - [ ] Current quarter quota by rep (from CRO or SFDC dashboard) - [ ] This week's pipeline report (pull from SFDC: opportunities closing this quarter, stage, amount, last activity date) - [ ] Rep 1:1 schedule and last session notes - [ ] Current forecast submitted to CRO. **Required Skills:** | Skill | When to Load | | sfdc-reporting.md | Any pipeline review or forecast workflow | | coaching-framework.md | Any 1:1 or deal review session | | escalation-thresholds.md | Any deal exceeding $50K or requiring non-standard terms |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 3,
      "finding": "The Story Portal appendix names four sales motions (Partnership, Sponsorship, Inbound, Relationship) and four priorities, but provides no operational detail that differentiates Story Portal from any other company with sales. There is no description of what a festival partnership deal cycle looks like, what the typical deal size or timeline is, who the buyer persona is (festival organizer? brand sponsor?), what the competitive dynamic is, or how the Sales Director should prioritize these four motions against each other. The team priorities table lists 'Festival partnership closure' as #1 but gives no context for what stage current deals are at or what 'closure' requires.",
      "example_rewrite": "Example rewrite for Partnership Sales row: | **Partnership Sales** | Primary motion. Target: regional festival organizers (500-5000 attendees). Deal size $15K-$80K annually. Cycle: 60-90 days. Key buyer: Festival Director or Sponsorship Lead. Win criteria: platform demo + reference call from existing festival partner + proposal within 2 weeks of demo. Director joins calls at proposal stage and final negotiation. Current priority: 3 deals in final stage, target close by Jan 31. |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific behavioral failure modes. The current file has no anti-patterns at all — this is the most critical missing element because it is the primary mechanism for preventing the most common and costly Sales Director failures (hero closing, forecast inflation, pipeline neglect). Without it, the role provides no behavioral guardrails beyond domain boundary rules, leaving both human users and any AI-assist functions without guidance on recognizable failure states."
}
```