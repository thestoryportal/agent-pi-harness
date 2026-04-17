```json
{
  "role": "account-executive",
  "department": "sales",
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
      "finding": "All six principles are generic sales platitudes that could appear in any B2B sales handbook from 2005. 'Customer Value First: Solve their problems' and 'Pipeline Is Life: Build continuously' contain zero specificity about Story Portal's mission-driven context, festival partnership model, or community-oriented sales approach. There is no acknowledgment that this AE sells an emotionally resonant product requiring a fundamentally different pitch than enterprise SaaS. The principles could be lifted verbatim into a role for a generic CRM vendor.",
      "example_rewrite": "| **Mission Before Margin** | Story Portal sells community impact — lead with empathy outcomes, not feature lists. A sponsor who feels the mission closes faster and stays longer. | | **Festival Cycles Are Real Deadlines** | Partner decisions happen months before events. Pipeline timing must map to festival calendars, not arbitrary quarter-end pressure. | | **Champion the Storyteller** | Every deal pitch must connect the buyer to the end user — a refugee sharing a story, a survivor finding community. Buyers who feel that connection become evangelists. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but the artifacts are dangerously vague. 'Qualified opportunities' from SDR could mean anything — a Salesforce record, a Slack message, a spreadsheet row. 'Closed deals' delivered to Client Success gives CS no indication of what format, what fields, or what commitments were made during the sale. 'Revenue booking' delivered to Finance is not an artifact at all — it is an outcome. Two handoff receivers ('Delivery' and 'Finance') are not confirmed roles in any visible charter, raising hallucinated-role risk.",
      "example_rewrite": "| Receives From | Artifact | Format | Required Fields | | SDR | Qualified Opportunity Brief | Salesforce Opportunity record at Stage 2 | BANT score, primary contact, pain summary, next step agreed | | Delivers To | Artifact | Format | Required Fields | | Client Success Manager | Closed-Won Handoff Package | CS Handoff Template in Notion | Signed contract date, committed outcomes, key stakeholders, renewal date, any side commitments made verbally |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "This role file contains no Anti-Patterns section whatsoever. The template standard explicitly requires 3-5 role-specific anti-patterns. The DON'T list in Boundaries partially compensates but lists boundary violations (e.g., 'don't do outbound qualification') rather than behavioral failure modes an AI agent would exhibit. There is no guidance on what a bad AE session looks like — over-discounting, skipping discovery, pitching features instead of outcomes, or misrepresenting Story Portal's capabilities to close faster.",
      "example_rewrite": "## Anti-Patterns\n| Anti-Pattern | Why It Fails | Correction |\n|---|---|---|\n| **Feature Pitching** | Listing Story Portal features before understanding the partner's community goals loses mission-aligned buyers immediately | Run at least 20 minutes of discovery before any product demonstration |\n| **Premature Discounting** | Offering price reductions before the prospect expresses budget concern trains buyers to wait for concessions and erodes deal margins | Present full value case; escalate to Sales Director before any discount discussion |\n| **Skipping Stakeholder Mapping** | Closing with one contact at a festival organization risks a veto from the Executive Director or Board | Identify and document all four stakeholder roles before moving to Propose stage |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol loop is present but barely functional. It says 'work on sales activities' with no specificity about which activities an AI agent can independently execute versus which require human hands. The Context Requirements section is completely unfilled — '[Context item 1]' and '[Context item 2]' are literal placeholders that were never completed. Required Skills table is also blank. An AI loading this role cannot determine what documents to load, what CRM fields to populate, which deal stage requires a STOP, or how to structure a festival partnership pitch without human intervention on every step.",
      "example_rewrite": "### Required Context\n- [ ] story-portal-product-overview.md — load before any demo or proposal task\n- [ ] festival-partner-pricing-tiers.md — load before any negotiation task\n- [ ] active-pipeline-report.csv — load at session start for pipeline review tasks\n- [ ] competitor-positioning-guide.md — load when competitive objection is raised\n\n### Iteration Protocol\nLOOP:\n  1. AI drafts discovery question sequence based on account research\n  2. STOP → Human AE reviews before live call\n  3. AI updates Salesforce fields post-call from human's debrief notes\n  4. STOP → Human confirms stage advancement is accurate\n  5. AI drafts proposal using Proposal Writer template\n  6. STOP → Human AE and Proposal Writer approve before sending"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix identifies the right deal categories (festival partnerships, community sponsors, technology partners, grant opportunities) but provides no actionable intelligence for any of them. Value messaging entries like 'Empathy connection: Mission resonance' are circular — they restate the category without explaining what to say or why it works. There are no example talk tracks, no specific objection responses for mission-driven buyers, no guidance on grant versus sponsorship versus partnership deal structures, and no reference to Story Portal's actual differentiators versus competitor platforms.",
      "example_rewrite": "| Deal Type | Primary Buyer Motivation | Opening Hook | Most Common Objection | Objection Response |\n|---|---|---|---|---|\n| **Festival Partnerships** | Amplify their community storytelling beyond the event footprint | 'What happens to the stories your attendees share after the festival ends? Story Portal makes them permanent and searchable.' | 'We don't have budget for new platforms' | 'Our festival tier is structured as a revenue-share on sponsor activations — no upfront cost until we generate value for you.' |\n| **Grant Opportunities** | Demonstrate measurable community impact to funders | 'Story Portal generates the engagement metrics your grant reports require automatically — documented story submissions, community reach, demographic data.' | 'Our grant doesn't cover technology vendors' | 'We qualify as a program delivery partner in most NEA and community foundation frameworks — we can provide language for your grant amendment.' |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 3-5 role-specific behavioral failure modes. This section is entirely missing — not weak, not vague, absent. For an AI-assisted Hybrid role in a mission-driven sales context, the absence of anti-patterns means an AI agent has no guardrails against the highest-risk AE behaviors: premature discounting, feature-led pitching, and skipping stakeholder discovery. This single addition would also force the author to confront how generic the philosophy and Story Portal sections are, likely triggering rewrites of both."
}
```