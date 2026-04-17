```json
{
  "role": "knowledge-base-manager",
  "department": "support",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are one-line platitudes with no operational meaning specific to a KB Manager. 'Self-Service First' and 'Clear Is Kind' could appear in any content role at any company. None of the principles address KB-specific tensions: e.g., when to retire stale articles vs. keep them, how to balance depth vs. scannability, or when search optimization conflicts with plain language. 'Data-Driven' has no specificity — driven by what data, toward what threshold?",
      "example_rewrite": "| **Retire Over Hoard** | An outdated article is worse than no article. Content older than 90 days without a review flag gets archived, not updated, until a ticket spike justifies the rebuild cost. | | **Search Intent Over Topic Titles** | Articles are titled and tagged by the question a user types ('why won't my recording save') not the feature name ('Audio Persistence Module'). | | **Ticket Volume Is a Lagging Signal** | A spike in tickets about a topic means KB failed 3 weeks ago. Proactively audit KB coverage when Product ships any feature touching recording, sharing, or privacy — before tickets arrive. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs are vague in both directions. 'Content requests' from Support Team is not a role (the charter has Customer Support Specialist and Technical Support Engineer as distinct roles). 'Gap analysis' from Support Research Analyst lacks the artifact format — is it a spreadsheet, a tagged ticket export, a Slack message? 'Feature updates' from Product has no named role. Outbound handoffs are worse: 'Self-service content to Users' is not a handoff, it is a publish action. No artifact format is specified anywhere.",
      "example_rewrite": "| Receives From | Role | Artifact | Format | | Customer Support Specialist | Weekly Top-10 Unanswered Tickets | Zendesk saved view shared as CSV, tagged 'kb-gap' | | Support Research Analyst | Monthly Gap Analysis Report | Google Doc with ranked content gaps, search-zero-result queries, and deflection rate by topic | | Product Manager | Feature Release Brief | Confluence page linked in #product-releases Slack channel, minimum 5 days before launch | | Delivers To | Role | Artifact | Format | | Technical Support Engineer | Draft Technical Article | Google Doc in 'KB Review' folder, tagged 'needs-tse-review', accuracy sign-off required before publish |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no Anti-Patterns section in this role file at all — it is entirely absent. The template standard explicitly requires 3-5 role-specific anti-patterns. The DO/DON'T boundary list exists but lists boundary violations (don't do Product's job), not behavioral failure modes the AI agent itself might exhibit during KB work. A KB Manager AI has specific failure modes: over-documenting edge cases, writing for the product team instead of end users, creating duplicate articles instead of updating existing ones, or publishing without a TSE accuracy check on technical content.",
      "example_rewrite": "## Anti-Patterns (Never Do This) | Anti-Pattern | Why It Fails | Correct Behavior | | **Publishing Without TSE Sign-Off on Technical Content** | AI-generated technical steps may be plausible but wrong. A single bad troubleshooting guide erodes trust in the entire KB. | Any article involving hardware, audio encoding, file formats, or error codes requires Technical Support Engineer approval before publish. | | **Creating New Articles Instead of Updating Existing Ones** | Duplicate content splits search traffic and confuses users. KB sprawl is harder to maintain than a disciplined single-source structure. | Always search for an existing article on the topic first. If one exists, update it and log the revision. Create new only when no existing article covers the use case. | | **Writing for Feature Names, Not User Goals** | Users search 'how do I send my story to grandma' not 'Story Sharing Module v2.' Expert-framed titles make content unfindable. | Every article title must pass the 'would a first-time user type this into the search bar?' test before publish. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol exists and includes a STOP point, which is correct. However, the protocol only covers Article Creation. Content Optimization workflow has no STOP points at all — an AI agent could autonomously publish rewrites based on analytics with no human checkpoint. The agent capabilities table lists what the AI can do but not the decision thresholds that trigger autonomous action vs. escalation. For example: at what point does a content gap trigger a new article vs. an update vs. an escalation to Product? The Classification section correctly states 'Human approves publication' but Workflow 1 Step 4 (PUBLISH) has no corresponding STOP marker.",
      "example_rewrite": "In Workflow 1 Step 3: 'STOP → Present draft to Head of Support or designated reviewer. Do not proceed to Step 4 without written approval in the KB review channel.' In Workflow 2 Step 3: 'STOP → Present improvement plan (list of articles to update, proposed changes, estimated impact) before making any edits to live content. Bulk updates of 3+ articles require Head of Support sign-off.' Add decision rule: 'If gap analysis reveals a topic with zero KB coverage AND 10+ tickets in 30 days → escalate to Head of Support with gap brief before creating new content. Do not self-initiate new article creation above this threshold.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies the right topic domains (Recording, Sharing, Festival, Privacy) but provides no actionable specificity. 'Audio capture guides' and 'step-by-step with visuals' could describe any audio app KB. There is no mention of Story Portal's unique context: oral history preservation, elderly or non-technical users, festival submission workflows, family sharing permissions, or the emotional sensitivity of the content (these are people's life stories). The content priority list ranks Recording #1 but gives no rationale tied to actual Story Portal user behavior or known pain points.",
      "example_rewrite": "| Topic | Content Approach | Priority Signal | | **First Recording for Non-Technical Users** | Step-by-step with annotated screenshots sized for mobile; assume user has never used a voice memo app; avoid all technical terms | Highest — onboarding drop-off data shows 40% of new users never complete first recording | | **Festival Submission Deadline Workflow** | Time-sensitive quick-reference card format; include submission checklist; publish 2 weeks before each festival cycle | Seasonal spike — support tickets increase 300% in the week before festival deadlines | | **Privacy and Family Sharing Permissions** | Lead with reassurance ('Your stories are private by default'); explain in plain language who can see what before explaining how to change it; acknowledge emotional sensitivity of content | High trust surface — privacy confusion is the top reason users cite for not sharing stories |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 KB Manager-specific failure modes (duplicate article creation, publishing technical content without TSE review, expert-framed titles). This section is entirely missing, which means the AI agent has no guardrails against its most common and highest-risk failure modes — particularly publishing inaccurate technical content autonomously."
}
```