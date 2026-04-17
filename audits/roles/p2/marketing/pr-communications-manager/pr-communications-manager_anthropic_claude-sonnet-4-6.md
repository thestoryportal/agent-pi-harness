```json
{
  "role": "pr-communications-manager",
  "department": "marketing",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 5,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All six principles are generic PR platitudes that could appear in any communications textbook. 'Story First,' 'Transparency Builds Trust,' and 'Consistency Matters' carry no Story Portal specificity and give an AI agent zero behavioral guidance. None of the principles reference the empathy-driven mission, festival context, or community storytelling that define this project. There is no principle governing how to handle the tension between aggressive narrative control and the authentic vulnerability that Story Portal's brand demands.",
      "example_rewrite": "Replace generic principles with role-specific ones. Example: Instead of 'Story First — Lead with compelling narratives,' write: 'Earned Vulnerability Over Polished Spin — Story Portal's credibility rests on authentic human stories, not corporate messaging. Every press angle must feel discovered, not manufactured. If a press release reads like a brand brochure, rewrite it as a human moment.' Instead of 'Preparation Prevents Crisis,' write: 'Festival Timing Is Irreversible — Love Burn is a fixed, public event. A PR misstep two days before launch cannot be walked back with a correction. Pre-approve all outbound materials at least 72 hours before distribution windows.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoffs name roles but artifacts are vague to the point of being non-actionable. 'Brand messaging' from Brand Strategist could mean anything from a one-pager to a 40-slide deck. 'Product news' lists no source role — 'Product' is not a defined charter role name. Outbound handoffs are equally weak: 'Coordinated messaging' delivered to Social Media does not specify format, channel, or timing. There is no artifact handoff for the Crisis Communications workflow, which is the highest-stakes process in the role.",
      "example_rewrite": "Tighten every handoff row to specify artifact format and triggering condition. Example: Change 'Brand Strategist | Brand messaging' to 'Brand Strategist | Approved Brand Voice & Messaging Framework (brand-voice.md) — loaded before drafting any press release or spokesperson brief.' Change 'Social Media | Coordinated messaging' to 'Social Media Manager | Press Release Amplification Brief — a one-page document specifying: embargo lift time, approved quote pulls, hashtags, and which platform leads. Delivered no later than 24 hours before distribution.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "The role has no dedicated Anti-Patterns section at all — this is a missing required section per the template standard. The Boundaries section contains DO/DON'T lists, but these are jurisdictional rules, not behavioral failure modes. There is no warning against common PR mistakes specific to this role, such as over-pitching journalists, issuing reactive statements without CMO sign-off, conflating marketing content with earned media, or breaking embargo timing. The absence of this section means an AI agent has no guardrails against the most common failure patterns in PR work.",
      "example_rewrite": "Add a dedicated Anti-Patterns section with role-specific failure modes. Example: 'ANTI-PATTERN: Pitching Before the Story Is Ready — Do not contact journalists until the press kit, approved quotes, and spokesperson are confirmed. A premature pitch that falls apart damages the relationship permanently. ANTI-PATTERN: Drafting Crisis Statements Alone — Never finalize a crisis statement without CMO + Legal review, even if the situation feels minor. What looks like a small issue often has legal exposure the PR Manager cannot see. ANTI-PATTERN: Treating Press Releases as Marketing Copy — A press release written in brand voice rather than news voice will be ignored. If a journalist could not reprint the first paragraph as a news lede, rewrite it.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol and Hybrid split are clearly defined, and STOP points exist in both workflows. However, the Context Requirements section is entirely unfilled — placeholder text '[Context item 1]' and '[Use placeholder format: skill-name.md]' were never completed. An AI agent loading this role has no idea what context files to load before beginning work. Additionally, the AI has no guidance on tone calibration — it knows it can draft materials but has no instruction on what 'good' looks like for Story Portal's specific voice versus a generic corporate PR voice.",
      "example_rewrite": "Complete the Context Requirements section with actual files and triggers. Example: 'Required Context: [x] brand-voice.md — load before any drafting task. [x] story-portal-mission.md — load before any media pitch. [x] crisis-protocol.md — load immediately upon any crisis trigger. Required Skills: | Press Release Writing | Load when: Announcement workflow triggered | press-release-style.md | | Crisis Drafting | Load when: Crisis Response workflow triggered | crisis-comms-guide.md |' Also add a Voice Calibration note: 'Story Portal press materials use first-person plural we, avoid corporate jargon, and always anchor the lede in a human moment before introducing the platform.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix identifies the right thematic areas — festival coverage, human interest, community impact — and the key messages are directionally correct. However, the section lacks operational specificity: no media targets are listed, no embargo dates or festival timeline anchors are referenced, no guidance on which story angles to lead versus hold in reserve, and no instruction on how to handle the intersection of a tech platform with an intentional community event (Love Burn), which creates unique media framing challenges. The PR Priorities table lists four items but provides no criteria for what 'done' looks like for each.",
      "example_rewrite": "Add media targeting and timeline context. Example: 'Festival Coverage Target Media: Tech-culture outlets (WIRED, Fast Company) for platform angle; event/festival press (BurnLife, Everfest) for community angle; local Miami outlets for Love Burn geographic hook. Do not pitch national news without CMO approval — the festival audience is intentional and mass coverage may conflict with community values. Festival PR Timeline: 8 weeks out — seed human interest stories with long-lead outlets. 3 weeks out — distribute press kit and embargo announcement. 1 week out — follow-up pitches and interview scheduling. Day of — real-time coverage coordination with Social Media Manager using Amplification Brief.'"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4-5 role-specific behavioral failure modes. This section is entirely missing, which means an AI agent has no guardrails against the most consequential PR mistakes — premature pitching, solo crisis drafting, and marketing-voice contamination of earned media. Of all gaps in this file, the absence of anti-patterns creates the highest risk of an AI agent producing work that damages real media relationships or triggers a reputational incident without a human checkpoint."
}
```