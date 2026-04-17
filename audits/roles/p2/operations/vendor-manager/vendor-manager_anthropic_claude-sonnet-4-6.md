```json
{
  "role": "vendor-manager",
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
      "finding": "All 6 principles are generic platitudes that could apply to any procurement role at any company. 'Partnership Over Transaction' and 'Value Over Cost' are vendor management clichés with no Story Portal context. None reference the festival production environment, the specific tension between creative vendor relationships and cost discipline, or the operational reality of managing vendors across live events. The 'Meaning' column is one-sentence filler ('Build lasting relationships') that adds zero actionable guidance.",
      "example_rewrite": "Replace generic principles with role-specific ones. Example: **Festival-First Vendor Selection** — When evaluating vendors, production reliability at live events outweighs unit cost. A vendor who fails at a festival cannot be replaced mid-show; a vendor who costs 15% more but has proven festival execution gets the contract. | **Creative Vendor Autonomy with Output Accountability** — Creative vendors (audio, design, production) are given latitude on process but are held to defined deliverable specs and milestone dates. Do not micromanage creative method; do enforce delivery standards. | **Single-Vendor Risk Ceiling** — No single vendor category should have more than one sole-source provider without COO sign-off. Redundancy planning is mandatory for festival-critical services."
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs name roles but artifacts are vague labels, not actual documents. 'Vendor requirements' from All Departments could mean an email or a 40-page spec — the AI has no idea. 'Contract requests' to Legal is undefined — is this a completed intake form, a redline, a summary brief? 'Vendor reports' to COO has no format, cadence, or trigger specified. 'All Departments' is not a role. The Receives/Delivers tables also omit critical handoffs: no handoff to/from IT Manager for technology vendor specs, and no handoff from Finance specifying the format of budget constraints.",
      "example_rewrite": "Tighten every handoff to name artifact, format, and trigger. Example row: | **Receives From: Requesting Department** | Artifact: **Vendor Requirements Brief** (completed intake form: business need, budget ceiling, timeline, minimum SLA requirements, preferred evaluation criteria) — triggered when department identifies external vendor need | | **Delivers To: Legal** | Artifact: **Contract Request Package** (selected vendor name, agreed commercial terms summary, scope of work draft, risk flags, requested execution date) — triggered after vendor selection approval from COO | | **Delivers To: COO** | Artifact: **Monthly Vendor Health Report** (PDF, 1-page per strategic vendor: SLA performance RAG status, spend vs. budget, open issues, renewal dates within 90 days) — delivered first Monday of each month |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There are no anti-patterns section in this role file at all. The template standard explicitly requires 3-5 role-specific anti-patterns, and this section is completely absent. The DON'T list in Boundaries is a boundary list (do not draft contracts, do not specify technology), not anti-patterns. Anti-patterns describe failure modes the AI might drift into — common wrong behaviors like over-negotiating on price at the expense of relationship, or managing vendors reactively only when issues arise. None of this exists.",
      "example_rewrite": "Add a dedicated Anti-Patterns section. Example: **Anti-Pattern 1: Cost Tunnel Vision** — Negotiating price reductions on every renewal regardless of vendor performance. If a festival production vendor delivered flawlessly, opening with aggressive price cuts signals distrust and damages the relationship. Reserve hard negotiation for underperformers or market-misaligned contracts. | **Anti-Pattern 2: Reactive Vendor Management** — Only engaging vendors when something breaks. Quarterly business reviews exist to surface issues before they become incidents. If the last vendor communication was a complaint, the relationship is already degraded. | **Anti-Pattern 3: Scope Creep Acceptance** — Allowing vendors to deliver outside contracted scope without a formal change order, then discovering budget overruns at invoice. Every scope change, even informal, triggers a written change order before work begins. | **Anti-Pattern 4: Consolidation for Its Own Sake** — Merging vendor categories to reduce headcount without evaluating whether a single vendor can actually serve both needs. Forced consolidation that creates a single point of failure in a festival-critical category is worse than managing two vendors."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Iteration Protocol loop exists, which is a positive signal for Hybrid classification. However, the AI cannot immediately know what to do because: (1) Context Requirements section contains literal placeholder text '[Context item 1]' and '[Context item 2]' — this was never completed; (2) Required Skills table has placeholder format instruction but no actual skills listed; (3) The boundary between human-led and AI-assisted tasks is stated at a category level ('AI assists with analysis') but never broken down by workflow step — which specific steps in Workflow 1 does the AI execute vs. the human? (4) No STOP points are labeled as human-approval gates vs. AI self-checkpoints, so the agent cannot distinguish when to pause for a human vs. when to proceed.",
      "example_rewrite": "Complete the Context Requirements section and annotate workflows with H/AI ownership. Example context: **Required Context: [ ] vendor-roster.md — current active vendors, contract end dates, SLA status | [ ] spend-report-current.md — YTD spend by vendor category | [ ] festival-calendar.md — upcoming events requiring vendor coordination | [ ] approved-vendor-tiers.md — strategic vs. preferred vs. approved vendor classifications**. Workflow annotation example: '3. EVALUATE — AI: score proposals against criteria matrix, compile comparison table | Human: conduct reference calls, attend demos | STOP → Human approves shortlist before proceeding to SELECT.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 3,
      "finding": "The Story Portal appendix exists but is generic to any entertainment company. 'Festival production: Event execution' is a tautology. No actual vendor names or categories specific to Story Portal's business are mentioned. The priorities list (festival vendor management, technology vendor optimization, cost efficiency, vendor consolidation) could apply to any operations role. There is no mention of the specific vendor lifecycle pressures unique to Story Portal — seasonal festival spikes, the relationship between creative production vendors and the platform's content output, or which vendor categories are currently at risk or up for renewal.",
      "example_rewrite": "Replace generic categories with Story Portal-specific operational context. Example: **Key Vendor Categories for Story Portal** | **Festival Production** — Stage, lighting, sound, and logistics vendors for annual Story Portal festival events; these are sole-source relationships that require 6-month advance booking; failure point is Q3 festival season | **Streaming Infrastructure** — CDN and cloud hosting vendors tied to platform SLAs; uptime SLA minimum 99.9%; contract renewal in Q2 2025 | **Audio Recording Services** — Studio and mobile recording vendors supporting artist content library; evaluate consolidation from 3 vendors to 2 by Q3 | **Vendor Risk Flag** — [Vendor Category X] is currently month-to-month; contract stabilization is Priority 1 for Q1 2025 | This gives the AI agent an actual operational picture rather than a placeholder taxonomy."
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section — it is entirely missing and is the single biggest gap. A Vendor Manager AI agent with no anti-patterns has no guardrails against the most common failure modes (cost tunnel vision, reactive management, accepting scope creep). This is a safety and quality gap, not just a completeness gap. Draft 4 role-specific anti-patterns tied to festival operations and vendor relationship management before this role is deployed."
}
```