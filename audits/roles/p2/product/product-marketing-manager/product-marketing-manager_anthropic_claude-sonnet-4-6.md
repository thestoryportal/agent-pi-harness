```json
{
  "role": "product-marketing-manager",
  "department": "product",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 5,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "All 6 principles are present and PMM-specific. 'Benefits Over Features' and 'Customer Voice First' are grounded in real PMM discipline. However, 'Messaging Must Resonate' and 'Launch Is Just the Beginning' border on generic marketing wisdom rather than differentiating PMM philosophy. None of the principles address the tension that defines PMM work: serving two masters (product and market) simultaneously.",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff tables name roles but artifacts are dangerously vague. 'Product features, roadmap' is not an artifact — it is a category. 'Win/loss feedback' has no format specified. 'Competitor analysis' could mean anything from a Slack message to a 40-page report. The receiving party cannot act on these descriptions. Additionally, 'Delivers To: Marketing' references a department, not a role, which violates the charter principle of naming actual roles.",
      "example_rewrite": "Receives From — Product Manager: 'Product Brief v[X] (Notion doc) containing feature specs, target persona, and release date, delivered at GTM kickoff meeting'. Delivers To — Content Marketing Manager: 'Messaging Architecture doc (Notion) containing approved value propositions, three-tier messaging hierarchy, and segment variants, delivered before content calendar planning session'."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Six anti-patterns are present and most are genuinely PMM-specific. 'Copy competitor positioning' and 'Create without sales input' reflect real PMM failure modes. However, 'Launch without metrics' and 'Create once and forget' are universal project management anti-patterns that would appear identically in a content or growth role. The table format with Why/Instead columns is well-structured.",
      "example_rewrite": null
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol loop is present and structurally correct, and the Human/AI split in Deployment Notes is clear. However, the AI agent lacks a cold-start instruction: there is no statement of what to do on first invocation when no task has been specified. The skill files are all marked as 'planned development' with no fallback behavior described — an AI agent loading this role would not know how to proceed without those files. The phrase 'AI drafts messaging' gives no format, length, or output standard.",
      "example_rewrite": "On first invocation with no task specified, ask: (1) Which workflow are we executing — Product Launch, Competitive Response, or Sales Enablement? (2) What product or feature is in scope? (3) What is the target segment? Do not begin drafting until all three are answered. If skill files are unavailable, apply embedded positioning framework: Problem → Unique Mechanism → Proof → Call to Action."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix correctly identifies the festival context and captures the tagline and differentiation. However, 'Sales Enablement: N/A (no sales team)' and 'Competitive: N/A (unique concept)' are missed opportunities — festival staff ARE the sales team for this context and competing for attendee attention IS a competitive dynamic. The PMM Priorities table lists five items but provides no success criteria, owner confirmation, or deadline for any of them, making it a list rather than an actionable plan.",
      "example_rewrite": "Priority 1 — Festival Positioning: Deliver one-page concept brief (PDF + printed) to festival operations lead by [date]. Success = 100% of staff can answer 'What is Story Portal?' in one sentence. Priority 2 — Staff Briefing Materials: Deliver 5-minute verbal script + FAQ card to volunteer coordinator by [date]. Success = zero confused staff interactions in post-event debrief. Reframe Sales Enablement as 'Attendee Conversion' — staff at booth need talk tracks, not silence."
    }
  ],
  "top_improvement": "Handoff specificity: Replace all artifact descriptions with named documents in specified formats delivered at defined trigger points, and replace the vague 'Marketing' recipient with the actual role name 'Content Marketing Manager' or 'Growth Marketing Manager' — vague handoffs are the most likely failure point when this role operates in a multi-agent workflow where the receiving agent needs to know exactly what file to expect and when."
}
```