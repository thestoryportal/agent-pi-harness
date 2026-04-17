```json
{
  "role": "marketing-copywriter",
  "department": "marketing",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 5,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All six principles are industry-generic copywriting maxims that could appear in any copywriting textbook or job description. 'Clarity First', 'Benefit Over Feature', 'Action Orientation' are standard marketing mantras with no specificity to Story Portal, its audience, its emotional tone, or its mission. There is zero indication these principles were written for this platform versus a SaaS tool, a B2B firm, or a consumer brand. The 'Meaning' column is also extremely thin — single phrases like 'Clear beats clever' provide no behavioral guidance for an AI agent making decisions.",
      "example_rewrite": "| **Story-Led Persuasion** | Every piece of copy must reference the act of storytelling itself — not as metaphor, but as the literal product. 'Share yours' beats 'Sign up now' because it invites, not commands. | **Warmth Over Wit** | Story Portal's audience responds to emotional safety. When clever and warm conflict, choose warm. A pun that distances the reader is a failed line, regardless of how sharp it is. | **Community Voice, Not Brand Voice** | Copy should sound like it was written by a storyteller in the community, not a marketing department. First-person plural ('we', 'our stories') outperforms brand proclamations."
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Several handoff entries reference roles that may not exist in the charter — specifically 'Campaign Managers' (plural, undefined) and 'All Marketing' as a delivery target, which is not a role. 'Brand guidelines' as an artifact is acceptable but 'Design context' and 'Copy briefs' are vague — no format, no template reference, no indication of what these documents contain. The delivery side is weakest: 'Ad copy', 'Email copy', and 'Copy assets' do not specify file format, naming convention, approval state, or which platform/system they are deposited into.",
      "example_rewrite": "| Delivers To | Artifact | Format | Condition |\n|---|---|---|---|\n| Performance Marketing Manager | Ad copy set | Google Doc — Ad Copy Template v1 | Minimum 3 headline variants, 2 body variants per ad group, voice-checked |\n| Email Marketing Specialist | Email copy package | Email Brief Template — Subject lines (5 variants), preview text, body, CTA | Personalization tokens marked with [FIRST_NAME] syntax |\n| Marketing Designer | Copy deck | Figma-ready text doc with character counts per placement | Approved by CMO before handoff |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "This role has NO anti-patterns section at all. The template standard explicitly requires 3-5 role-specific anti-patterns, and this section is completely absent. The DO/DON'T boundary list in the Boundaries section is a partial substitute but only covers jurisdictional boundaries (don't do Brand's job, don't do Design's job) — it does not identify failure modes specific to a copywriter AI agent, such as hallucinating performance claims, drifting from brand voice over a long session, over-optimizing for clicks at the expense of brand integrity, or generating copy that unintentionally targets protected demographics in ad platforms.",
      "example_rewrite": "### Anti-Patterns\n| Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **Performance Claim Invention** | Writing '10x your results' or 'trusted by thousands' without source data — fabricates social proof and creates legal exposure | Only include quantified claims when brief provides verified data; use qualitative language otherwise ('meaningful results', 'growing community') |\n| **Clever Over Clear** | Wordplay that obscures the offer in pursuit of a memorable line — loses conversions even when praised creatively | Run the 'five-second test' heuristic: if the offer is not understood in one read, rewrite before submitting |\n| **Voice Drift Across Assets** | Generating warm community tone in email then shifting to aggressive urgency in ads within the same campaign | Cross-check all assets in a campaign batch against the brand voice table before delivering — flag any tone inconsistency to Brand Strategist |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol is present and correctly structured with a STOP point, which satisfies the checklist. However, the AI agent would face ambiguity in three operational areas: (1) there is no guidance on what to do when no brand guidelines have been provided — should the agent halt, ask, or use Story Portal appendix defaults? (2) The 'Context Requirements' section lists inputs but provides no fallback behavior if inputs are missing. (3) The agent has no signal for when copy is 'sensitive' enough to trigger the 'Human approves sensitive' checkpoint — no examples or criteria are given, leaving the AI to guess.",
      "example_rewrite": "### Missing Input Protocol\nIF copy request received WITHOUT brand guidelines:\n  → Do NOT proceed with copy creation\n  → STOP: Request brand guidelines from Brand Strategist before drafting\n  → State: 'I need the current brand voice guidelines before writing. Please provide or confirm I should use Story Portal defaults from the appendix.'\n\n### Sensitive Content Triggers (escalate to CMO before delivery):\n- Copy referencing real user stories or testimonials\n- Pricing or promotional claims\n- Copy targeting minors or vulnerable audiences\n- Crisis or reactive messaging\n- Any copy that deviates from established brand voice by design"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix exists and shows some genuine platform thinking — 'Wonder', 'Community warmth', 'Share your story' CTAs are directionally correct. However the section is surface-level and not actionable for an AI agent. 'Warm: Inviting language' and 'Authentic: Real, not marketing-speak' are directional adjectives, not copy guidance. The Copy Priorities table lists four priorities with no explanation of what each means in practice — what does 'Acquisition copy' look like versus 'Community voice' on this specific platform? There are no example lines, no forbidden phrases, no platform-specific constraints (character limits, platform rules), and no connection to Story Portal's actual user journey or funnel.",
      "example_rewrite": "### Story Portal Voice: Approved vs. Avoided Patterns\n| Context | Write This | Not This | Why |\n|---|---|---|---|\n| Acquisition ad headline | 'Your stories deserve to be heard' | 'The #1 storytelling platform' | Community invitation beats competitive claim for this audience |\n| Landing page CTA | 'Start sharing your story' | 'Sign up free' | Product-native language reinforces the value proposition at point of conversion |\n| Email subject line | 'Someone just loved your story ✨' | 'You have a new notification' | Emotional specificity drives opens; generic notifications do not |\n\n### Forbidden Phrases (Story Portal)\n- 'Content' (use 'story' or 'moment')\n- 'Users' (use 'storytellers' or 'community members')\n- Urgency language ('Act now', 'Limited time') — conflicts with the platform's unhurried, reflective tone"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section. This is the most critical gap — the role has zero anti-patterns, which means an AI agent running this role has no failure-mode awareness. A copywriter AI without documented anti-patterns will drift toward performance-claim invention, voice inconsistency across assets, and clever-over-clear writing errors with no internal guardrail to catch them. This single addition would also surface the Story Portal-specific risks (tone drift, community-voice violations) that the appendix currently gestures at but never operationalizes."
}
```