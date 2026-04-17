```json
{
  "role": "qa-operations-manager",
  "department": "quality-assurance",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 5,
    "anti_pattern_quality": 5,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Four of the six principles are generic enough to apply to any operations manager role ('Enable, Don't Block', 'Process Serves People', 'Measure to Improve', 'Automate the Boring'). Only 'Reliable Environments' and 'Right Tools, Right Time' carry role-specific weight. The table format shows the structure is correct but the content is insufficiently differentiated from a DevOps Manager, IT Ops Manager, or any enablement role.",
      "example_rewrite": "Replace 'Process Serves People' with: **'Environment Parity Protects Releases** — A QA environment that doesn't mirror production isn't a test environment, it's a false confidence machine. Config drift between QA and prod is treated as a P1 issue.' Replace 'Automate the Boring' with: **'Data Freshness Is a Testing Prerequisite** — Stale test data produces stale results. Test data refresh cycles are scheduled, documented, and owned — never ad hoc or assumed."
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff tables list roles and broad artifact categories but fail the specificity test on both sides. 'Receives From: Head of QA → Priorities, budget approval' and 'Delivers To: QA Team → Environments, tools, processes' name no actual documents, no formats, and no triggering conditions. The Workflow sections name STOP points but don't specify what artifact is produced at the stop or who signs off. 'DevOps Research Lead' in the Works With table is suspicious — this role does not appear to be a standard QA org role and may be a hallucinated reference.",
      "example_rewrite": "Replace vague handoff rows with: 'Receives From: QA Lead → [Environment Request Form] containing: environment type, required config, test data needs, and target-ready date. Delivered via Jira ticket tagged ENV-REQUEST.' and 'Delivers To: Release Manager → [Environment Status Report] in standard markdown template confirming environment name, URL, last refresh date, known issues, and go/no-go recommendation. Delivered 24 hours before release window.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 5,
      "finding": "Six anti-patterns are listed but several are generic operational cautions that would appear in any IT or ops role ('Skip documentation → Knowledge silos', 'Ignore metrics → Can't improve'). None of the anti-patterns are specific to QA operations failure modes. Missing are the most characteristic QA Ops failure patterns: environment state drift between sprints, granting prod-data access in QA environments for convenience, and letting CI pipeline flakiness get normalized as 'known flaky tests' rather than treated as infrastructure debt.",
      "example_rewrite": "Replace 'Skip documentation' and 'Ignore metrics' with: **'Normalize Flaky Environments** — When testers start saying 'oh, that environment just does that sometimes,' it means ops has accepted instability as permanent. Every recurring environment issue gets a runbook and a root-cause ticket within 48 hours, not a workaround.' and **'Use Production Data in QA for Convenience** — Shortcuts that copy live customer data into QA environments to avoid test data setup create compliance exposure. Test data sets are synthetic, documented, and refreshed on schedule.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol loop is present and well-structured. The AI/Human split is clearly articulated in the Hybrid section. The role would load with reasonable operational clarity. Minor gaps: the skill files are explicitly flagged as not yet existing ('planned development'), which means an AI agent loading this role has no actual skill content to reference. The Context Requirements checklist is useful but gives no guidance on what to do if context is missing — should the AI ask, halt, or proceed with assumptions?",
      "example_rewrite": "Add a 'Missing Context Protocol' block: 'If Required Context items are not provided at deployment, DO NOT proceed with environment or tool recommendations. Instead, output: [CONTEXT REQUEST] listing each missing item with a one-sentence explanation of why it is required before operations work can begin. Example: Missing item: Environment architecture — Required to avoid recommending configurations that conflict with existing infrastructure.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix is one of the stronger sections — it correctly identifies the current-state gap (Vercel previews only, no test management tool, informal processes) and maps priorities in ranked order. The recommended tools table is grounded and realistic for an MVP budget. Score is held from higher because the 'Audio recordings, prompts' test data note is the only Story Portal-specific content detail, and the environment approach ('Leverage preview URLs for QA') has no concrete next step — no example of how preview URLs get assigned to test cycles or tracked in GitHub Issues.",
      "example_rewrite": "Expand the Environments row: 'Vercel preview deployments — Each PR auto-generates a preview URL. QA Operations will establish a GitHub Issues label scheme (env:preview-{PR#}) so testers tag bugs to the exact environment build they tested. QA Ops maintains a pinned GitHub Issue as the Environment Registry listing active preview URLs, their associated PR, last deploy timestamp, and assigned tester.'"
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. Every handoff currently names a role and a vague category ('priorities', 'environments', 'metrics reports') but specifies no artifact format, no trigger condition, and no acceptance criteria. An AI agent or human picking up this role cannot determine what 'done' looks like for any handoff. Rewrite all handoff table rows to follow the pattern: [Role] → [Named Artifact] → [Format/Location] → [Trigger Condition]. This single change would also force resolution of the suspected hallucinated 'DevOps Research Lead' reference, which has no corresponding handoff row and should be verified against the Organizational Charter before the next version release."
}
```