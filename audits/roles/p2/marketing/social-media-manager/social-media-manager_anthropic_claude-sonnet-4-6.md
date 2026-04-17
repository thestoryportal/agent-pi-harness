```json
{
  "role": "social-media-manager",
  "department": "marketing",
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
      "finding": "All 6 principles are generic social media platitudes that could appear in any introductory social media course. 'Authenticity Wins', 'Community Over Audience', and 'Conversation, Not Broadcast' are industry clichés with no operational specificity. None of the principles reference Story Portal's actual mission (empathy, user stories, festival context), the AI-human hybrid dynamic of this specific role, or measurable behaviors that distinguish this SMM from any other. The 'Platform Native' and 'Value Every Post' principles are especially hollow — they name a concept without defining what it means operationally for this role.",
      "example_rewrite": "Replace generic principles with role-specific operational guidance. Example: Replace 'Authenticity Wins — Be genuine, not corporate' with 'Story-First Voice — Every post must connect to a real human story on the platform; promotional content that doesn't tie back to a user story or community moment is rejected before publishing. Example: A TikTok about platform growth gets reframed as the story of a user who found community here.' Replace 'Platform Native — Adapt to each platform' with 'Festival Vernacular — Content language, format, and tone are adapted not just to platform norms but to Story Portal's festival community culture; Instagram captions reference shared experiences, not product features.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name some roles but fail the artifact specificity requirement on both sides. 'Content to share' from Content Manager is not a real artifact — what format, what file, what brief? 'Issue escalations' to Support is a category, not an artifact. The 'Social insights' delivered to Content Team has no defined format or trigger. Critically, the role references 'PR/Communications Manager' and 'Brand Strategist' in the Works With table but neither appears in any handoff row — so the collaboration interface is declared but never operationalized. 'Support Team' is referenced without a role name consistent with charter conventions.",
      "example_rewrite": "Replace vague handoff rows with artifact-specific entries. Example: Change 'Content Manager | Content to share' to 'Content Marketing Manager | Approved Content Brief (content-brief-v[n].pdf) with platform adaptation notes and publish window; delivered via shared content calendar every Monday by 9am.' Change 'Support | Issue escalations' to 'Support Team | Social Escalation Report (escalation-form.md) listing: platform, username, issue type, screenshot URL, urgency tier (1-3), and recommended response; sent within 15 minutes of detection.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file. This is a complete omission of a required section per the Template Standard quality checklist. The DO/DON'T boundary list in the Boundaries section is a partial substitute but does not function as anti-patterns — it lists domain ownership rules, not failure modes or behavioral traps specific to this role. Anti-patterns should describe how this specific AI-human hybrid SMM role fails in practice: e.g., the AI drafting crisis responses without human review, over-scheduling content that crowds out real-time community moments, or homogenizing voice across platforms by applying Instagram tone to LinkedIn posts.",
      "example_rewrite": "Add a dedicated Anti-Patterns section with role-specific failure modes. Example: '**Anti-Pattern 1: AI-Drafted Crisis Response** — AI detects negative spike and drafts a response without flagging for human review. CORRECT: Any sentiment spike above threshold triggers STOP and human review before any response is published. **Anti-Pattern 2: Calendar Rigidity Over Community Moments** — Scheduled content is published during an active community crisis or sensitive news moment because the queue was not paused. CORRECT: Agent checks news and community sentiment before each publish action and holds if context has changed. **Anti-Pattern 3: Platform Voice Flattening** — The same caption is adapted only by character count across platforms, losing TikTok's informal energy and LinkedIn's professional register.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists but is dangerously vague for an AI agent. 'IF routine → Continue autonomously' gives the agent no definition of what constitutes routine versus sensitive — a newly onboarded AI agent cannot make that distinction reliably. The STOP points in workflows are present but function as completions, not decision gates with defined criteria. The Context Requirements section contains literal placeholder text ('[Context item 1]', '[Context item 2]') and the Required Skills table is empty — this means an agent loading this role has no skill files to load and no context documents to ingest. Browser vs. Agent capability split is described but the agent has no decision tree for choosing which mode to invoke.",
      "example_rewrite": "Replace the placeholder Context Requirements and vague Iteration Protocol with operational specifics. Example Context Requirements: '- [ ] brand-voice-guide.md (required before any content creation) - [ ] platform-strategy-doc.md (required before scheduling) - [ ] crisis-escalation-thresholds.md (required before community monitoring)'. Example Iteration Protocol clarification: 'ROUTINE (AI proceeds autonomously): Scheduling pre-approved posts, monitoring keyword dashboards, logging engagement metrics. STOP REQUIRED (human reviews before proceeding): Any response to a negative comment, any content not in the approved calendar, any sentiment spike >20% in 2 hours, any mention of competitor, legal, or safety topics.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix identifies the correct platforms and gestures at relevant themes (stories, festival community, empathy mission) but provides no actionable specificity. 'Stories — User stories shared' tells an AI agent nothing about what a user story post looks like, what the approval process is, or how it differs from standard content. 'Festival community building' as Priority 1 is unexplained — there is no definition of what the festival is, what community building looks like in this context, or what success metrics apply. The appendix reads as a placeholder adaptation rather than genuine project context. No mention of Story Portal-specific community norms, moderation policies, or platform handles.",
      "example_rewrite": "Replace generic theme rows with actionable Story Portal context. Example: Change 'Stories | User stories shared' to 'User Story Spotlight — Weekly Instagram carousel (3-5 slides) featuring an anonymized user story submitted via Story Portal; copy must include the user's own words (with permission tag), a community response prompt in caption, and link to full story in bio. Drafted by AI using story-spotlight-template.md, reviewed by CMO before publishing.' Add a row: 'Moderation Policy — Story Portal community has zero-tolerance for dismissing user vulnerability; any comment minimizing a shared story is hidden within 5 minutes and escalated per crisis-escalation-thresholds.md.'"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section — this is a full section omission that leaves the AI agent with no failure mode awareness. For a Hybrid role managing live community interactions and potential brand crises, the absence of documented anti-patterns (especially around AI-drafted crisis responses and autonomous publishing decisions) is the highest risk gap in the entire file. A single misfire on a sensitive community post can cause brand damage that no amount of good philosophy or clean handoffs can repair."
}
```