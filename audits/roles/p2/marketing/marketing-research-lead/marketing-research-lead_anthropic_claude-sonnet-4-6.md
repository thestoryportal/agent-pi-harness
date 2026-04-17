```json
{
  "role": "marketing-research-lead",
  "department": "marketing",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 3,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic marketing platitudes that could apply to any research role in any industry. 'Data Reveals Truth', 'Competitive Awareness', and 'Continuous Learning' are textbook filler. None reflect Story Portal's specific context (festival community, storytelling behavior, experience apps). There is no principle about the tension between quantitative signals and qualitative community sentiment, nor about research latency in a seasonal/event-driven product cycle.",
      "example_rewrite": "Replace generic principles with role-specific ones: | **Festival Cycles Drive Research Windows** | Story Portal's audience engagement spikes around events — research must be timed to capture peak community behavior, not averaged across dead periods. | **Community Signal > Sample Size** | In a niche festival community, 50 engaged participant interviews outweigh a 5,000-response survey of disengaged users. Prioritize depth over breadth. | **Competitive Moat is Experiential, Not Feature-Based** | Competitors are not just other apps — they are passive consumption habits (streaming, scrolling). Research must frame differentiation in terms of participation identity, not product specs. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs are critically vague. 'Receives: CMO → Research priorities' and 'Delivers: CMO → Research findings' describe a conversation, not a handoff. No artifact names, no formats, no file types, no trigger conditions. 'Campaign Managers' is listed as a delivery target but does not appear in the collaboration table or the Organizational Charter as a confirmed role. 'Marketing Analyst' appears in the Works With table but not in the handoffs table, creating a gap. Zero handoffs specify what happens at STOP points in the workflows.",
      "example_rewrite": "Replace vague rows with: | Delivers To | Artifact | Format | Trigger | | CMO | Audience Research Brief | 1-page PDF summary + supporting data appendix | Before quarterly campaign planning cycle | | Content Strategist | Channel Effectiveness Report | Ranked channel scorecard (CSV + narrative summary) | After each campaign cycle closes | | Marketing Analyst | Raw Segmentation Dataset | Cleaned CSV with segment labels and behavioral flags | Upon completion of audience research workflow Step 3 |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no dedicated Anti-Patterns section anywhere in this role file — this is a missing required section per the Template Standard. The DO/DON'T boundary list in the Boundaries section is the closest analog, but those are ownership rules, not behavioral failure modes. There are zero anti-patterns described. The template checklist explicitly requires role-specific anti-patterns, and this role file entirely omits them.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: | Anti-Pattern | Why It Fails | Correct Behavior | | **Reporting data without a recommendation** | Delivering a 20-page campaign analysis that ends with 'performance varied by channel' forces the CMO to do the synthesis work the Research Lead exists to do. | Every report must end with a ranked action list: 'Top 3 changes to make before next campaign launch.' | | **Treating all competitors as feature competitors** | Benchmarking Story Portal against other apps misses that the real competition is user inertia and passive media habits. | Include 'behavioral alternatives' (e.g., passive scrolling, live event attendance) in every competitive analysis. | | **Averaging across the full year to assess festival audience** | Festival community engagement is event-clustered. Annual averages suppress the signal. | Always segment time-series data by event proximity: pre-event, during-event, post-event windows. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and is structurally correct, but it lacks concrete STOP point definitions that would allow an AI agent to self-determine when to halt. 'STOP → Present for review' has no criteria for what triggers the stop — is it time-based, confidence-based, or task-completion-based? The Agent Capabilities table lists 'survey execution' without specifying what tools or APIs are authorized. Workflows have no explicit decision branches for ambiguous or conflicting data. An AI agent loading this role would know the general loop but would have no guardrails for edge cases.",
      "example_rewrite": "Expand the Iteration Protocol STOP criteria: 'STOP conditions that require human review before proceeding: (1) Confidence in data source is below threshold — e.g., sample size under 50 for a segment claim, or source is unverifiable. (2) Findings contradict a prior approved research report by more than 20% on a key metric. (3) Competitive intelligence reveals a strategic threat (new entrant, major feature launch) that has CMO-level implications. (4) Research task requires primary data collection from real users (survey deployment requires CMO approval before send). In all STOP cases, produce a structured Findings Memo — headline finding, confidence level, recommended next step — before halting.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix acknowledges the product exists but stays at surface level. 'Festival community' and 'storytelling behavior' are mentioned but never operationalized. There are no specific research methodologies tied to Story Portal's unique context (e.g., how to measure story participation rates, what behavioral signals indicate a healthy festival community, which competitive tools apply to experience apps). The 'Key Research Areas' table asks questions but provides no guidance on how to answer them. 'Experience apps' as a competitive category is named but not defined — an AI agent cannot action this.",
      "example_rewrite": "Replace the generic questions table with specific research protocols: | Research Area | Specific Metric | Method | Source | Frequency | | Festival audience motivation | % of users who cite 'community belonging' vs 'content consumption' as primary value | In-app post-festival survey (5 questions max) | Story Portal user database | Post each festival cycle | | Story sharing drivers | Share-to-view ratio by story type (text, audio, visual) | Funnel analysis in Mixpanel, segmented by story format | Mixpanel event data | Weekly during active festival periods | | Competitive differentiation | Feature gap map vs top 3 experience apps (Participate, YOUmedia, Storyworth) | Manual audit + user review mining (App Store, G2) | Public app store reviews + CI platform | Monthly |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section. This is a required section per the Template Standard and is completely absent — not just weak, but missing. Without role-specific anti-patterns, the AI agent has no failure-mode awareness, meaning it will confidently produce the exact wrong outputs (data dumps without recommendations, feature-only competitive analysis, annual averages that mask festival seasonality) with no internal check. This single gap undermines the entire research quality guarantee of the role."
}
```