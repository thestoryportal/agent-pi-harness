```json
{
  "role": "brand-strategist",
  "department": "marketing",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 3,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 4,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "Six principles are present and titled well, but the meaning column is shallow sloganeering. 'Every interaction delivers on promise' explains nothing about HOW a Brand Strategist operationalizes that belief. 'Consistency Builds Trust' is a generic marketing maxim found in any intro textbook. None of the principles encode a decision rule specific to a Brand Strategist's actual trade-offs — e.g., when to evolve vs. protect, how to prioritize audience resonance against stakeholder pressure, or how to handle brand extension requests.",
      "example_rewrite": "Replace 'Consistency Builds Trust — Same voice, every time' with: 'Consistency Is Non-Negotiable — When a team member requests a one-off tone exception for a campaign, the answer is a framework adjustment or the answer is no. Exceptions are data points that the guidelines need updating, not licenses to deviate. A brand that bends for convenience erodes faster than one that never launches.' Replace 'Emotion Over Logic — Connection before explanation' with: 'Lead With Feeling, Prove With Fact — The opening line of any message earns the right to the proof point. If a stakeholder wants to open with a feature list, reorder it. Emotional resonance is the door; logic is the room inside.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Every handoff entry is vague to the point of being non-functional. 'CMO → Strategy direction' is not an artifact — it is a description of a conversation. 'Content Team → Messaging framework' does not specify which document, what format, what version, or what the recipient is expected to do with it. 'Marketing Research Lead' and 'User Research Lead' appear as sources but neither role is confirmed to exist in the charter (the template checklist explicitly warns against hallucinated roles). The Design Team receives 'Brand direction' with no artifact name. An AI agent cannot execute a handoff that says 'receives strategy direction.'",
      "example_rewrite": "Replace the Receives/Delivers tables with: 'Receives From CMO: Approved Marketing Strategy Document (quarterly PDF/Notion page) containing target segments, growth priorities, and approved budget envelope — this is the strategic brief that gates positioning work. Receives From Marketing Research Lead: Audience Insight Report (slide deck, minimum 20 interviews) including verbatim quotes, pain point taxonomy, and competitive perception map. Delivers To Content Marketing Manager: Messaging Framework v[X] (Notion doc) containing brand pillars, message hierarchy per audience segment, approved proof points, and banned language list. Delivers To Marketing Designer: Brand Direction Brief (single-page PDF) specifying tone adjectives with visual analogies, do/don't usage examples, and signed-off positioning statement.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no Anti-Patterns section in this role file at all. The DON'T list in the Boundaries section is a domain boundary list ('don't create visual designs') — that is ownership delineation, not anti-pattern documentation. Anti-patterns should describe failure modes that a Brand Strategist specifically and repeatedly falls into: e.g., over-indexing on internal stakeholder preferences over audience research, writing positioning statements that are aspirational but untestable, or treating brand guidelines as finished documents rather than living frameworks. None of this is present. The template quality checklist explicitly requires 3-5 role-specific anti-patterns.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: '**Anti-Pattern 1 — Positioning by Committee:** Allowing brand positioning to be edited into meaninglessness by incorporating every stakeholder's preferred language. Sign: the positioning statement contains no competitive claim and could describe any company in the category. Fix: revert to research-backed differentiation and present it as a recommendation, not a draft for group editing. **Anti-Pattern 2 — Guidelines as Decoration:** Publishing a brand guidelines document and considering the job done. Sign: teams are not using the guidelines and are unaware they exist six months after launch. Fix: embed governance checkpoints into existing content and design review workflows. **Anti-Pattern 3 — Messaging Without Proof Points:** Writing emotionally resonant messages that have no supporting evidence. Sign: sales team cannot answer 'why should I believe that?' Fix: every brand claim must be paired with one verifiable proof point before it enters the framework.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Context Requirements section — the single most critical section for AI deployment — contains unfilled placeholders: '[Context item 1]' and '[Context item 2]'. The Required Skills table has no entries, only a format note. This means an AI agent loading this role has no idea what files, documents, or knowledge to load before beginning work. The Iteration Protocol exists and is correctly structured, which prevents a lower score. However, the Browser Capabilities list ('Research and analysis, Document creation') is generic and does not tell the AI what tools to actually use, what outputs to produce first, or how to distinguish between a positioning task and a guidelines task at load time.",
      "example_rewrite": "Replace the Context Requirements section with: 'Required Context: [ ] story-portal-brand-brief.md — current approved positioning and mission statement. [ ] competitor-landscape.md — names, positioning, and voice descriptors of top 5 competitors. [ ] audience-segments.md — primary and secondary audience personas with jobs-to-be-done. [ ] approved-messaging-framework.md — current version if one exists (load as baseline, not as constraint). Required Skills: | brand-positioning-frameworks.md | Load for any positioning or differentiation task | | messaging-architecture.md | Load when building or auditing message hierarchy | | brand-voice-calibration.md | Load when reviewing or producing any written output |'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix exists and makes a genuine attempt at project specificity — 'Make empathy contagious' and 'Warm, authentic, wonder' are real brand signals, not placeholders. However, the Brand Priorities table lists four items with no actionability: Priority 1 is 'Core positioning development' with no current status, no definition of done, and no indication of what already exists vs. what needs to be built. The Voice Guidelines table gives adjectives but no behavioral examples in the Story Portal context — 'Warm: Inviting, friendly' is as generic as the philosophy principles. There is no mention of how the brand should behave specifically at festival touchpoints, in the app, or in storyteller communications, which are the core Story Portal use cases.",
      "example_rewrite": "Replace the Voice Guidelines table with: '| Attribute | Story Portal Behavior | Anti-Example | | Warm | Open submissions with second-person invitation: \"Your story belongs here.\" Use first name in all storyteller communications. | \"Submit your content via the portal below.\" | | Authentic | Never use superlatives about the festival itself (\"best,\" \"most powerful\"). Let storyteller quotes carry the proof. | \"The most transformative storytelling experience.\" | | Wonder | Describe the festival experience with sensory specificity — sounds, light, the feeling of a crowd leaning in. | \"A great community event with diverse programming.\" | | Connected | Always reference the audience as a community with shared history, not as attendees or users. | \"Users of the Story Portal platform.\" |' Add to Brand Priorities: 'Priority 1 — Core Positioning: STATUS: Not yet drafted. Milestone: CMO-approved positioning statement by [date]. Inputs needed: audience research report + competitive landscape.'"
    }
  ],
  "top_improvement": "Fill the Context Requirements section with actual file names and add a dedicated Anti-Patterns section — these two omissions mean an AI agent cannot safely load or execute this role. A role file with placeholder context and no failure-mode guidance will either stall immediately (waiting for inputs that were never specified) or produce plausible-sounding brand strategy that violates the most common Brand Strategist failure modes without any self-correction mechanism."
}
```