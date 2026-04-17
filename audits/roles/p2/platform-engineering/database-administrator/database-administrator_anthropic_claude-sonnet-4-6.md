```json
{
  "role": "database-administrator",
  "department": "platform-engineering",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 7,
    "anti_pattern_quality": 8,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "All 6 principles are meaningfully DBA-specific. 'Measure Before Tuning' and 'Security at the Data Layer' are precise and behavioral. Minor weakness: 'Data Is Sacred' risks being a platitude — it states a value but doesn't encode a decision rule. A DBA seeing a 3-hour ETL job that blocks writes needs more than 'data is sacred' to know what to do. The principle would be stronger if it implied a concrete trade-off stance (e.g., prioritizing recoverability over write throughput).",
      "example_rewrite": "**Recoverability Over Convenience** — Every operation must be reversible or recoverable. If a maintenance task cannot be rolled back and has no tested restore path, it does not run. RTO/RPO targets are non-negotiable constraints, not aspirational goals."
    },
    {
      "dimension": "handoff_specificity",
      "score": 7,
      "finding": "Handoff tables name real roles and real artifact types, which is solid. However, several entries remain vague at the artifact level. 'Schema migrations, slow query reports, optimization requests' (from Backend Developer) and 'Performance alerts, database health issues' (from SRE) describe artifact categories, not specific deliverable formats. An AI agent doesn't know if a 'slow query report' is a Slack message, a pg_stat_statements export, or a Jira ticket. The Delivers To side is similarly category-level. No handoffs specify file format, system of record, or trigger condition.",
      "example_rewrite": "| Backend Developer | `slow_query_report.md` containing query text, EXPLAIN ANALYZE output, and observed p95 latency — filed as a Jira ticket tagged `dba-review` when query exceeds 500ms threshold in staging or production logs |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 8,
      "finding": "Seven anti-patterns are listed and all are DBA-specific — none are generic 'don't write bad code' filler. Standouts: 'Vacuum during peak hours' and 'Add indexes without analysis' are precisely scoped to database operations. One weakness: 'Store database credentials in code' is a generic security anti-pattern that applies equally to any backend role. It belongs in a shared security standard, not as a DBA-specific item. The slot could be used for something uniquely DBA: e.g., running REINDEX without CONCURRENTLY on a live table, or disabling autovacuum to 'speed things up.'",
      "example_rewrite": "| Run REINDEX without CONCURRENTLY on production | Blocks all reads and writes on the table for the duration | Always use `REINDEX INDEX CONCURRENTLY`; schedule non-concurrent reindex only in confirmed maintenance windows with affected teams notified |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 9,
      "finding": "This is the role's strongest dimension. The Iteration Protocol is explicit, the STOP points in all five workflows are clearly placed, and the CLI deployment rationale is well-reasoned. Required vs. task-specific skill files are separated correctly. The 'NEVER / ALWAYS / ALWAYS' block at the end of the Iteration Protocol gives an AI agent unambiguous behavioral guardrails. Minor gap: the role does not specify what the AI should do when it encounters a production incident mid-workflow (e.g., active data corruption or replication lag spike) — the escalation table covers roles but not the interrupt behavior."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The appendix correctly identifies that this role has zero current-phase relevance (MVP is frontend-only) and maps forward to Phase 2 Supabase responsibilities. The planned schema SQL stub is a good anchor. However, the 'Key Coordination Points' table in the Story Portal section duplicates the main Collaboration section without adding project-specific detail. More critically, the quality bar metrics (100ms p50, monthly backup verification) are not tied to any Story Portal-specific usage pattern — for an early-stage app with likely <1,000 users at Phase 2 launch, these thresholds need context or they're meaningless targets an AI agent can't act on.",
      "example_rewrite": "**Phase 2 Launch Thresholds (Story Portal-specific):** At projected launch load (<500 concurrent users, ~10K stories), acceptable p50 is <50ms on `stories` table reads with RLS active. If p50 exceeds 80ms during internal beta, trigger index review against `stories(user_id, updated_at)`. Backup verification cadence: monthly restore drill to isolated Supabase project; pass criteria is full schema + data integrity within 15-minute RTO."
    }
  ],
  "top_improvement": "Handoff specificity: replace artifact category labels with concrete deliverable definitions including format, system of record, and trigger condition. An AI agent receiving 'slow query reports' from SRE cannot act without knowing whether to look in Supabase logs, a Jira board, or a Slack channel — and cannot produce a 'migration approval' without knowing if that means a comment in a PR, a signed-off Jira ticket, or a markdown file committed to the repo. Resolving this unlocks the full value of the otherwise strong workflow and collaboration sections."
}
```