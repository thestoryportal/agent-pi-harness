```json
{
  "role": "seo-sem-specialist",
  "department": "marketing",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are generic SEO industry clichés that could appear verbatim in any SEO textbook, blog post, or job description. 'Content Is King' and 'Data-Driven Decisions' are marketing platitudes with zero specificity to this role, this organization, or the Story Portal context. None of the principles address how SEO operates inside an AI-Primary constraint, how to balance organic compound growth against a limited SEM budget, or how to handle the unique search vocabulary of empathy-driven storytelling communities.",
      "example_rewrite": "Replace generic principles with role-specific ones. Example: | **Semantic Intent Over Keyword Density** | Story Portal audiences search emotionally ('how to share my story at Burning Man') not transactionally — optimize for question-intent and narrative-intent clusters, not volume-first head terms. | | **Organic Compounding Before Paid Acceleration** | SEM budget is limited at early stage; every paid dollar must be justified by a gap organic cannot close within 90 days. Never recommend SEM where organic has a credible path. | | **Technical SEO as Engineering Prerequisite** | A recommendation unimplemented is not an optimization. Every technical SEO output must include an Engineering-ready spec, not just an observation, so Frontend Developer can act without a follow-up meeting. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoff tables name roles but describe artifacts in vague, category-level language ('Priorities and budget', 'Content for optimization', 'Keyword guidance'). No handoff specifies the format, trigger condition, or acceptance criteria of the artifact. 'Technical requirements' delivered to Engineering could mean a Slack message or a 50-page spec — the role is silent on this. The Delivers To table also omits the Performance Marketing Manager entirely, despite that role being listed as a collaboration partner, creating a workflow gap.",
      "example_rewrite": "| Delivers To | Artifact | Format | Trigger |\n|-------------|----------|--------|---------|\n| Content Marketing Manager | Keyword Brief | Structured doc: target keyword, search volume, intent classification, suggested H1, internal linking anchor | Before each content piece enters drafting |\n| Frontend Developer | Technical SEO Spec | Prioritized issue list with: URL affected, current state, required state, estimated traffic impact, implementation effort (S/M/L) | Monthly audit cycle or post-crawl alert |\n| CMO | Monthly Search Performance Report | Dashboard export + written summary: ranking deltas, organic sessions, SEM spend vs. conversion, top 3 recommended actions | First Monday of each month |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "The role contains no dedicated Anti-Patterns section at all — this is a template standard violation. The DO/DON'T boundary list exists but it describes role scope boundaries (don't create content, don't build websites), not failure modes specific to how an SEO/SEM Specialist actually goes wrong. It does not warn against over-indexing on vanity ranking metrics, bidding on brand terms that cannibalize organic, producing keyword briefs that ignore narrative intent, or the common AI failure of optimizing for crawlability at the expense of human readability.",
      "example_rewrite": "## Anti-Patterns\n\n| Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **Vanity Ranking Optimization** | Chasing position #1 for high-volume terms with no conversion history wastes crawl budget and misrepresents SEO health to leadership | Report rankings only alongside CTR, sessions, and goal completions — position is a leading indicator, not an outcome |\n| **Keyword Brief Without Intent Classification** | Handing Content a keyword list without specifying informational / navigational / transactional intent produces content that ranks but doesn't convert | Every keyword brief must include intent type and the user question the content must answer |\n| **SEM Spend Before Organic Baseline** | Launching paid campaigns on keywords where organic data is insufficient (<90 days) wastes budget on under-validated terms | Require minimum 90-day organic impression data before recommending SEM investment on any keyword cluster |\n| **Technical SEO as Observation, Not Spec** | Reporting 'site has slow Core Web Vitals' without a reproducible fix hands Engineering an incomplete ticket | Every technical finding must include current measured value, target value, and one specific remediation action |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and names the AI/Human split, which is the minimum required. However, an AI agent loading this role cannot determine: what tools to actually invoke (SEO Platforms and Keyword Tools are unnamed), what constitutes a STOP point within the SEO Optimization or SEM Campaign workflows (neither workflow contains a STOP checkpoint despite the template standard requiring them), what thresholds trigger escalation versus autonomous action, or what the agent should do when a ranking drops suddenly versus gradually. The workflows are four-step summaries with no branching logic.",
      "example_rewrite": "Add explicit STOP checkpoints and thresholds inside workflows. Example for Workflow 1: \n'3. IMPLEMENT\n   - Execute on-page changes within CMS (autonomous)\n   - Submit technical SEO spec to Frontend Developer (autonomous)\n   ⛔ STOP — HUMAN APPROVAL REQUIRED: Any change to site URL structure, canonical tags, or robots.txt must be reviewed by CMO + Frontend Developer before implementation. Present: proposed change, affected URLs, estimated ranking impact, rollback plan.\n   - Monitor post-change rankings for 14 days (autonomous)\n   → OUTPUT: Change log with pre/post ranking delta'\n\nAlso name specific tools: replace 'SEO Platforms' with 'Ahrefs / SEMrush' and 'Keyword Tools' with 'Google Keyword Planner, Ahrefs Keywords Explorer'."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix acknowledges the project exists and lists some thematic keyword categories, which is better than a blank section. However, the keyword list is surface-level ('Personal stories, storytelling, Festival experiences, Burning Man') with no search volume context, no intent classification, no competitor gap analysis direction, and no acknowledgment of the unique challenge that Story Portal's core audience may not be actively searching — they discover through community, not search. The SEM guidance ('Limited — early stage') provides no decision criteria for when SEM becomes appropriate or what budget threshold unlocks it.",
      "example_rewrite": "Expand with actionable search strategy specifics. Example:\n\n| Keyword Cluster | Intent Type | Estimated Monthly Volume | Priority | Notes |\n|---|---|---|---|---|\n| 'how to share my story publicly' | Informational | Low-medium | High | Aligns with onboarding funnel; target with long-form guide |\n| 'Burning Man story archive' | Navigational | Low | Medium | Brand-adjacent; optimize festival landing pages |\n| 'audio storytelling platform' | Commercial Investigation | Medium | High | Competitive cluster; requires backlink strategy |\n\nAlso add: '**SEM Activation Trigger:** Recommend SEM budget request to CMO when organic impressions on a commercial-intent cluster exceed 500/month with CTR below 2% — indicating demand exists but content is not converting. Minimum viable SEM test budget: $500/month for 60-day proof of concept.'"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4 role-specific failure modes. This role has zero anti-patterns documented, which is both a template standard violation and an operational risk — an AI agent running autonomously with no documented failure modes has no guardrails against the most common SEO mistakes (vanity metrics, premature SEM spend, incomplete technical specs). This single addition would most immediately reduce the risk of the agent producing plausible-but-harmful search recommendations."
}
```