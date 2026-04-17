```json
{
  "role": "growth-hacker",
  "department": "marketing",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All six principles are generic growth hacking clichés recycled from any startup blog post circa 2015. 'Velocity Wins', 'Fail Fast', 'Data Decides' — these could appear in a Dropbox, Uber, or Duolingo growth playbook without changing a word. None are specific to Story Portal's context (oral storytelling community, festival mechanics, empathy-driven sharing). 'Full Funnel' and 'Creative Hacking' are single-word labels with two-word definitions that add no behavioral guidance.",
      "example_rewrite": "Replace generic principles with Story Portal-specific behavioral rules. Example: | **Story as the Hook** | Every growth experiment must be anchored to a real story moment — the share button appears after emotional peak, not at session end | and | **Empathy Drives K-Factor** | Viral loops at Story Portal succeed when they lead with the listener's curiosity ('Hear what happened to Maya'), not the teller's vanity — design mechanics accordingly |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but not actual artifacts. 'Growth priorities' from CMO, 'Performance data' from Marketing Analyst, and 'Winning tactics to scale' to Performance Marketing are all vague process descriptions, not named documents or data objects. There is no indication of format (dashboard link, Notion doc, CSV export, Slack message), no SLA, and no indication of what 'winning' threshold triggers the handoff to Performance Marketing. The collaboration table says Growth Hacker 'works with Engineering' but there is no corresponding handoff row for Engineering despite technical implementation being listed as a dependency.",
      "example_rewrite": "Handoff row example — | **Delivers To** | **Artifact** | **Trigger** | | Performance Marketing Manager | Experiment Results Card (Notion template): hypothesis, variant, sample size, lift %, confidence interval, recommended scaling budget | Experiment reaches p<0.05 with >15% lift on activation metric | and | Marketing Analyst | Growth Experiment Brief (Google Sheet): test name, funnel stage, target segment, success KPI, baseline | Before experiment launches, minimum 48hrs prior |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "The role file contains NO dedicated anti-patterns section at all. The DON'T list in Boundaries is purely jurisdictional ('don't set strategy', 'don't scale paid channels') — these are ownership boundaries, not behavioral failure modes. Anti-patterns should describe how this specific role fails in practice: e.g., running experiments without statistical validity, optimizing the wrong funnel stage, confusing correlation with causation in viral coefficient calculations, or launching growth tactics that erode Story Portal's emotional brand trust. None of these appear anywhere in the document.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: | **Anti-Pattern** | **What It Looks Like** | **Why It Fails** | | Shipping Speed Theater | Running 10 experiments per week with <100 users each | Sample sizes too small to reach significance; creates false learnings and wastes engineering cycles | | Vanity Metric Loops | Optimizing story shares without tracking whether shared stories get completed by recipients | K-factor looks healthy while actual new user activation stays flat | | Empathy Erosion | A/B testing aggressive re-engagement copy ('You haven't shared in 7 days!') without brand review | Short-term reactivation lift damages Story Portal's trust-based community tone permanently |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol is present and has basic loop logic, which is good. However, the Context Requirements section is literally unfilled — '[Context item 1]' and '[Context item 2]' are placeholder text left in the published document, and the Required Skills table has no entries. An AI agent loading this role cannot determine what context files to load (analytics dashboard? product roadmap? current experiment backlog?), what the current north star metric is for Story Portal, or what constitutes a 'winner' threshold that triggers scaling. The human/AI division of labor in the Hybrid section is stated but not operationalized — it says 'AI assists with data analysis' but never specifies what analysis format to return, to whom, or in what tool.",
      "example_rewrite": "Replace placeholder Context Requirements: | **Required Context** | **When to Load** | | story-portal-growth-metrics.md | Every session — contains current north star metric, baseline conversion rates by funnel stage, and active experiment registry | | story-portal-brand-guidelines.md | Before designing any experiment touching user-facing copy or sharing mechanics | | current-experiment-backlog.csv | Before proposing new experiments — prevents duplicate hypothesis testing | Also add to Iteration Protocol: Step 2 should read: 'STOP → Report results in Experiment Results Card format (hypothesis / variant / n / lift % / confidence / recommendation) and post to #growth-experiments Slack channel. Tag CMO if confidence >90% or lift >20%.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is the strongest section — it correctly identifies the platform's unique growth levers (story sharing virality, listener-to-teller conversion, festival community mechanics) and names Story Portal-specific viral mechanics like 'empathy chains' and 'festival teams'. However, it remains at the label level without actionable specifics. 'Story invites' as a mechanic is listed but there is no description of what the invite loop actually looks like, what the current baseline K-factor is, which funnel stage has the worst drop-off, or what experiments are already proven vs. hypothesized. The priorities table ranks 4 items without explaining why Story Sharing Virality is #1 or what success looks like for each.",
      "example_rewrite": "Expand the viral mechanics table with measurable baselines and current state: | **Mechanic** | **Current State** | **Target** | **Key Experiment to Run** | | Story invites ('Hear my story') | Baseline K-factor unknown — measurement not yet implemented | K-factor > 1.0 within 90 days | Add share prompt immediately after teller completes recording; test 3 copy variants targeting listener curiosity vs. social proof vs. urgency | | Listener-to-Teller conversion | Est. 8% of listeners have ever recorded a story | 15% within 6 months | Test 'Your turn' prompt triggered 48hrs after listener completes their 3rd story |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 Story Portal-specific behavioral failure modes. This is the most critical gap because the role currently has zero guardrails against the most common growth hacking failures in emotionally-driven community products — specifically the risk of optimizing engagement metrics in ways that erode the trust and empathy that make Story Portal's community function. Generic jurisdictional DON'Ts ('don't set strategy') do not protect against an AI agent running statistically invalid experiments, optimizing vanity shares, or deploying aggressive re-engagement tactics that damage the brand. This single addition would also force specificity improvements across philosophy and Story Portal sections."
}
```