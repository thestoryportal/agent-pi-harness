```json
{
  "role": "chief-marketing-officer",
  "department": "marketing",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 3,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic marketing platitudes that could appear in any CMO job description on LinkedIn. 'Brand Is Promise', 'Story Over Features', 'Test and Learn' — none of these are grounded in Story Portal's specific context (empathy-driven festival community, Burning Man culture, steampunk aesthetic). They offer no decision-making guidance unique to this role.",
      "example_rewrite": "Replace generic principles with context-specific ones. Example: 'Burner Culture First — Marketing to festival communities requires earned trust, not broadcast advertising; our campaigns speak peer-to-peer, not brand-to-consumer. We never run paid acquisition tactics that feel transactional in spaces where gifting culture is the norm.' Or: 'Empathy Is the Product — Love Burn exists to make empathy contagious; every campaign metric must include a qualitative story of human connection alongside CAC and conversion data.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs are critically vague. 'Receives: Strategic priorities from CEO' and 'Delivers: Qualified leads to Sales' are not artifacts — they are categories. No document names, no formats, no field specifications, no SLA. 'Research' is listed as a handoff source but does not appear to be a defined role in context. The handoff table cannot be used to verify completeness of a work product.",
      "example_rewrite": "Receives From CEO: 'Quarterly Strategic Priorities Memo (Google Doc, 1-pager, includes top 3 company goals, approved budget envelope, and any brand constraints for the quarter — delivered at start of each planning cycle).' Delivers To CRO: 'Marketing Qualified Lead (MQL) Report — CSV export from CRM tagged with lead source, campaign ID, acquisition date, and lead score ≥40 — delivered weekly every Monday by 9am.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There are NO anti-patterns section in this role file. The template standard explicitly requires 3-5 role-specific anti-patterns, but this section is entirely absent. The DO/DON'T boundary list exists but describes jurisdictional boundaries (don't build product, don't close sales), not behavioral failure modes specific to how a CMO might actually go wrong in execution.",
      "example_rewrite": "Add a dedicated Anti-Patterns section with entries such as: 'Vanity Metric Obsession — Reporting follower counts and impressions to leadership without tying to acquisition or retention. INSTEAD: Every metric presented to CEO must have a downstream business outcome attached.' Or: 'Campaign Before Community — Launching paid acquisition campaigns into the festival space before organic community trust is established. Burning Man-adjacent audiences reject inauthentic outreach; community credibility must precede demand generation.' Or: 'Brand Consistency Theater — Enforcing visual guidelines while allowing inconsistent tone across channels, creating a polished but hollow brand experience.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 3,
      "finding": "The Context Requirements section contains unfilled placeholder text ('[Context item 1]', '[Context item 2]', '[Use placeholder format: skill-name.md]') — these are template artifacts that were never completed. An AI agent loading this role has no idea what context files to load, what skills to activate, or what constraints apply to AI-assisted work. The Hybrid deployment section states AI 'assists with analysis' and 'generates content drafts' but provides no specificity about which tasks, what format, or what approval gates apply before AI output is used.",
      "example_rewrite": "Replace placeholders with: 'Required Context: [ ] brand-guidelines-v1.md — Load before any content creation task. [ ] love-burn-event-brief.md — Load before any campaign planning. [ ] audience-personas.md — Load before any messaging work.' For AI task boundaries add: 'AI may draft social copy and blog posts but MUST STOP and present to CMO before any copy referencing the Love Burn event dates, ticket pricing, or partner names is finalized. AI must never autonomously publish to any channel.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies the right domains (Love Burn, empathy, festival community, steampunk aesthetic) but stays at the level of labels rather than actionable direction. 'Priority 1: Love Burn launch marketing' tells an AI or human operator nothing about what to actually do, what channels are approved, what the launch timeline is, what success looks like, or what constraints exist. The channel table lists 'Community' and 'Events' without naming the actual communities or events.",
      "example_rewrite": "Replace high-level priority rows with specific operational context: 'Love Burn Launch Marketing — Target audience is Burning Man regional event participants in Florida; primary acquisition channel is direct outreach within existing regional Burn communities (ePlaya, Facebook groups for Florida regional burns) NOT paid social; launch campaign must go live 90 days before event date; success metric is 500 ticket registrations in first 30 days at CAC under $12.' For channels, name them: 'Community: ePlaya forums, Florida Burners Facebook Group (22k members); Content: Story Portal narrative blog targeting 3 posts/week; Events: Presence at Sno-Core and other Florida regionals as preview activations.'"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section (currently entirely missing) with 3-5 Story Portal-specific failure modes — this is the single largest structural gap and the most likely source of role confusion, since without it there is no guidance on how this CMO should NOT behave when marketing to a Burning Man-adjacent festival community where standard growth marketing tactics will actively damage brand trust."
}
```