```json
{
  "role": "data-analyst",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are generic platitudes applicable to any analyst at any company. 'Questions Drive Analysis' and 'Clarity in Communication' are so obvious they provide no behavioral guidance. None of the principles address Story Portal-specific tradeoffs, such as how to handle thin data from a small user base, when to trust engagement metrics vs. qualitative signals, or how to avoid over-indexing on completion rates as the sole success metric.",
      "example_rewrite": "Replace generic principles with role-specific ones, e.g.: | **Completion Rate Is a Lagging Signal** | Don't optimize for completion alone — analyze the *quality* of engagement within a session (replays, shares, prompt revisits) to distinguish passive listening from active connection. | **Small-N Discipline** | Story Portal is an early-stage product; flag analyses where cohort sizes fall below 30 users and never present percentage changes without absolute counts alongside them. | **Prompt Is a Confound** | Every behavioral pattern must be tested against prompt variation — a drop-off spike may reflect a bad prompt, not a bad feature. Always segment by prompt before drawing conclusions."
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but the artifacts are vague labels, not actual deliverables. 'Analysis requests' from Stakeholders, 'Data models' from Analytics Engineer, and 'Dashboard specs' to BI Developer are placeholders. There is no specification of format, schema, or what constitutes a complete artifact. The template standard explicitly requires specifying 'what artifact is passed, not just works with' — this file fails that standard. Additionally, 'Data Quality Engineer' appears in the Escalate and Handoffs sections but must be verified against the Organizational Charter before inclusion.",
      "example_rewrite": "Receives From Analytics Engineer: a dbt model documentation export (schema.yml + model README) confirming which tables are production-ready and their grain, refresh cadence, and known limitations. Delivers To BI Developer: a Dashboard Spec document containing (1) the specific question the dashboard must answer, (2) the confirmed SQL query or dbt model name serving as the data source, (3) a sketch of required dimensions/filters, and (4) the stakeholder who approved the analysis this dashboard operationalizes."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "The role has NO dedicated anti-patterns section at all. The DON'T list under Boundaries is purely jurisdictional ('don't build data models') and contains zero behavioral anti-patterns — the kind that describe how this specific analyst role fails in practice. There is no warning about over-interpreting small samples, confusing correlation with causation in engagement data, presenting findings without confidence intervals, or burying the insight in methodology detail. This is the most critical structural gap in the file.",
      "example_rewrite": "Add an Anti-Patterns section: | **The Methodology Essay** | Leading the report with how the analysis was done rather than what was found. Stakeholders need the insight in sentence one. Put methodology in an appendix. | **Percentage Without Denominator** | Reporting '40% increase in story completion' without stating the base (e.g., 5 → 7 users). Always pair percentages with absolute counts, especially in early-stage cohorts. | **Correlation Presented as Cause** | Writing 'users who hear Festival prompts complete more stories' implies the prompt causes completion — it may reflect self-selection. Flag causal claims explicitly and recommend an A/B test before acting. | **Answering the Asked Question Only** | Delivering exactly what was requested without noting adjacent anomalies discovered during analysis. If the data shows something the stakeholder didn't ask about but should know, include it as a 'What Else We Found' section."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol exists and is structurally sound. The Agent Capabilities list is present. However, the STOP point in the Iteration Protocol ('STOP → Present for review') lacks specificity about what triggers a stop vs. what the AI can proceed through autonomously. There is no guidance on how to handle ambiguous requests, data access failures, or situations where the data contradicts the stakeholder's stated assumption. An AI agent loading this role knows the loop structure but not the decision logic inside each step.",
      "example_rewrite": "Expand the Iteration Protocol with explicit decision gates: 'STOP → Present for review' should read: 'STOP — Do not proceed to delivery if: (a) sample size in any key segment is below 30, (b) findings contradict a stated business assumption (flag the contradiction explicitly and pause), (c) data freshness of the source table exceeds 48 hours for a time-sensitive request, or (d) the analysis would require joining more than 3 tables not documented in the Analytics Engineer's model catalog. In all four cases, surface the blocker with a specific question before continuing.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is a genuine attempt at project specificity and names relevant domains (festival, prompts, completion). However, the Key Questions section maps questions to single-method answers in a way that oversimplifies — 'Which prompts drive completion? → Cohort comparison' ignores that prompt assignment may not be random, making cohort comparison misleading without controls. The Data Sources table lists sources without schema details, table names, or refresh cadences, making it decorative rather than operational. An AI agent cannot actually use 'App events / User interactions' to write a SQL query.",
      "example_rewrite": "Replace the generic Data Sources table with actionable references: | Source | Table Name | Grain | Refresh | Key Fields | | App events | fct_story_sessions | One row per session | Hourly | user_id, prompt_id, session_start_ts, completion_flag, replay_count | | Prompt data | dim_prompts | One row per prompt | Manual/release | prompt_id, prompt_text, prompt_type (festival/standard), release_date | | Audio metadata | dim_stories | One row per story | On publish | story_id, duration_seconds, narrator_id, theme_tags |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4-5 behavioral failure modes specific to this role and domain. The file currently has zero anti-patterns — only jurisdictional boundary rules. Without anti-patterns, an AI agent has no guardrails against the most common ways data analysis goes wrong in practice (small-n overconfidence, correlation-as-causation, methodology-first reporting). This is both the largest structural gap and the highest-leverage fix because it directly constrains AI behavior during autonomous analysis loops."
}
```