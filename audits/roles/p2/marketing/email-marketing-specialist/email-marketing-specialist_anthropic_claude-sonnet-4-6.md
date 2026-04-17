```json
{
  "role": "email-marketing-specialist",
  "department": "marketing",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic email marketing slogans that could appear in any beginner's blog post. 'Inbox Is Sacred' and 'Value Every Send' are motivational posters, not operational principles. None reference Story Portal's specific context (storytelling platform, festival lifecycle, community-driven users). There is zero behavioral guidance — a principle should tell the AI how to make a tradeoff, not just name a value.",
      "example_rewrite": "| **Festival-Aware Cadence** | Suppress non-festival emails within 72 hours of a Festival send to prevent fatigue — Story Portal users are community members first, subscribers second. During Festival windows, shift from acquisition tone to celebration tone. | | **Story Prompt Timing Over Frequency** | An inactivity prompt sent at the wrong moment damages more than silence. Check last story submission date and platform login before triggering re-engagement. One well-timed prompt outperforms three generic nudges. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Receives artifacts are named vaguely ('Content for emails', 'Email templates') with no format, no file type, no naming convention, and no SLA. Delivers artifacts are even vaguer — 'Email capabilities' delivered to 'All Teams' is meaningless. The role references 'Content Manager' in handoffs but the Collaboration section lists 'Content Marketing Manager' — inconsistent naming creates lookup failures for AI agents traversing the charter. No handoff specifies what triggers the transfer.",
      "example_rewrite": "| Receives From | Artifact | Format | Trigger | \n|---|---|---|---| \n| Content Marketing Manager | Approved copy brief per campaign | Google Doc, template v2, reviewed + signed off | Campaign brief approved by CMO | \n| Marketing Designer | Final HTML email template | .html file + mobile preview screenshots | Design sign-off complete | \n| CMO | Quarterly campaign priority stack-rank | Priority matrix doc | Sprint planning kickoff | \n\n| Delivers To | Artifact | Format | Trigger | \n|---|---|---|---| \n| CMO | Monthly email performance report | Dashboard PDF + 3-bullet exec summary | Last business day of month | \n| Marketing Analyst | Raw campaign send data | CSV export from ESP, UTM-tagged | 48 hours post-send |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file at all — it is entirely absent. The template standard explicitly requires 3-5 role-specific anti-patterns. The DO/DON'T boundary section exists but lists boundary violations (e.g., 'Don't design templates') not behavioral failure modes. A boundary violation tells the AI what is out of scope; an anti-pattern warns against plausible mistakes the AI might make while staying in scope.",
      "example_rewrite": "## Anti-Patterns\n\n| Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **Blasting the full list for every campaign** | Destroys deliverability reputation and spikes unsubscribes from irrelevant segments | Always define the minimum viable segment before scheduling any send |\n| **Launching automation without a full-flow test send** | Broken merge tags or mis-fired triggers erode trust and cannot be recalled | Complete end-to-end test with seed addresses covering all branch conditions before activation |\n| **Optimizing open rate in isolation** | High opens + low clicks + high unsubscribes indicates misleading subject lines, which degrades long-term list health | Report open rate, click-to-open rate, and unsubscribe rate as a triad — never one metric alone |\n| **Sending Festival emails on a generic template** | Story Portal users have a narrative relationship with the platform; a generic promo email breaks immersion and signals the brand doesn't know them | Festival emails must use community-voice tone guidelines from Brand Strategist and reference the specific Festival name/theme |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists, which is a positive signal, but it is dangerously underspecified for an AI-Primary Agent deployment. STOP points are listed once ('Report for review') but there is no definition of what triggers a mandatory STOP versus autonomous continuation. Workflow steps lack decision branches — what does the AI do if open rate is below benchmark? If a deliverability alert fires? The Agent Capabilities table lists capabilities but not constraints or confidence thresholds. An AI agent loading this role knows what it can do but not when to stop doing it.",
      "example_rewrite": "### Mandatory STOP Points\n\n| Trigger | STOP Action | Resume Condition |\n|---|---|---|\n| Campaign audience > 10,000 recipients | Halt send, escalate to CMO with segment definition and suppression list | Written CMO approval in task thread |\n| Deliverability score drops below 85 | Pause all sends, alert CMO + Engineering with ESP health report | Engineering confirms root cause resolved |\n| Unsubscribe rate on single send > 0.5% | Halt related automation, flag to CMO with copy and segment details | CMO reviews copy and segment; provides go/no-go |\n| Any email referencing legal terms, refunds, or account termination | Do not send — escalate to Legal with draft | Legal written clearance |\n\nAutonomous continuation is permitted only when: task is a repeat send type previously approved, audience < 5,000, and no compliance flags triggered."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is the strongest section in the file — it names real email types (Welcome, Festival prep, Post-festival) and real triggers (sign up, inactivity, event approaching). It scores above 7 threshold but misses specificity that would make it actionable: no content tone guidance per sequence, no benchmark metrics specific to Story Portal's audience, no mention of the storytelling or festival identity that makes this platform distinct from a generic SaaS product. The 'Story prompts' sequence trigger ('Inactivity') needs a definition — inactivity for how long?",
      "example_rewrite": "| Sequence | Trigger | Inactivity Definition | Tone Guidance | Success Metric |\n|---|---|---|---|---|\n| Story Prompts Re-engagement | No story submission in 14 days AND no platform login in 7 days | 14-day submission gap | Curious, warm — reference their last story theme if available | Click-to-story-start rate > 8% |\n| Festival Prep Series | 21 days before registered Festival date | N/A | Anticipation-building, community-forward — name the specific Festival | Email-to-RSVP confirmation rate |\n| Post-Festival Reflection | 48 hours after Festival end | N/A | Celebratory, reflective — reference community participation numbers | Story submission rate within 7 days post-email |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific behavioral failure modes. This file has zero anti-patterns, which is the most critical gap for an AI-Primary Agent — without explicit failure mode warnings, the AI has no guardrails against plausible but harmful behaviors (mass blasting, single-metric optimization, untested automation launches) that stay within the role's stated scope while silently degrading email channel health."
}
```