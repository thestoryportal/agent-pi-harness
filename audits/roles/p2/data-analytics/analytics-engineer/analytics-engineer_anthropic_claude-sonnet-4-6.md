```json
{
  "role": "analytics-engineer",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 5,
    "anti_pattern_quality": 3,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All six principles are generic data engineering platitudes that could appear in any analytics role on the internet. 'Data as Product' and 'Testing Is Required' carry no specificity to this role, project, or organization. There is no principle governing how this engineer balances transformation performance against model readability, how they handle breaking changes in shared marts, or how they navigate the tension between analyst self-service and model sprawl — all real, role-specific tensions for an Analytics Engineer.",
      "example_rewrite": "| **Marts Are Contracts** | Once a mart table is consumed downstream by a BI Developer or Data Analyst, its schema is a contract. Breaking changes require a deprecation notice, a migration plan, and sign-off from Head of Data & Analytics before merging. Silent schema changes are the fastest way to destroy trust in the data layer. | | **Test Coverage Is Non-Negotiable Before Merge** | No dbt model enters production without at minimum: not_null and unique tests on primary keys, referential integrity tests on foreign keys, and at least one business-logic assertion validated against a known-good sample. A model with no tests is not a model — it is a guess. | | **Staging Is Sacred** | Staging models rename and lightly cast only. No business logic, no joins, no filtering lives in the staging layer. This boundary exists so that raw source changes are isolated and the intermediate/mart layers remain readable and trustworthy. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoffs name roles but artifacts are dangerously vague. 'Raw data, infrastructure' from Data Engineer tells an AI agent nothing about what it is actually receiving — no table names, no schema conventions, no format. 'Analytics-ready data' delivered to BI Developer is equally abstract. There is also no specification of what form the artifact takes (dbt model name, schema location, YAML doc file, Slack notification, PR link) or what state it must be in to be considered a valid handoff.",
      "example_rewrite": "| Receives From | Artifact | Form | Ready-State Condition | | Data Engineer | New source table available in raw schema | Slack message in #data-eng-releases + source YAML entry in dbt sources.yml | Table exists in Snowflake raw schema, row count > 0, load timestamp populated, Data Engineer has confirmed grain and update frequency in message | | Delivers To | Artifact | Form | Ready-State Condition | | BI Developer | Finalized mart model | dbt model deployed to prod schema (e.g. analytics.fct_story_completions), YAML docs with column descriptions, sample SELECT query in model README | All dbt tests passing in CI, model documented in dbt docs site, schema and grain confirmed in #analytics-releases Slack thread |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 3,
      "finding": "The role has no dedicated Anti-Patterns section at all. The DON'T list under Boundaries covers jurisdictional boundaries (don't build dashboards, don't build infrastructure) but contains zero behavioral anti-patterns specific to Analytics Engineering work. There is no warning against the most common and costly mistakes this role makes in practice: logic duplication across marts, over-denormalization into one massive wide table, bypassing the staging layer for convenience, hardcoding date filters in models, or defining the same metric differently in two different marts.",
      "example_rewrite": "### Anti-Patterns — Do Not Do These \n | Anti-Pattern | Why It Fails | Correct Approach | \n | **Defining the same metric twice in different marts** | fct_stories.completion_rate and fct_sessions.story_completion_rate calculated differently causes stakeholder arguments about which number is correct and erodes trust in the entire data layer | Define all metrics once in the metrics layer / semantic layer. Marts reference the metric definition; they do not recalculate it. | \n | **Putting business logic in staging models** | Staging models are consumed by multiple intermediate models. One business-logic change in staging cascades and breaks downstream models in unexpected ways | Staging renames and casts only. All joins, filters, and business logic live in intermediate or mart models. | \n | **Building a mart without tests** | Untested marts will silently produce wrong numbers. The BI Developer and Data Analyst will not discover the error — a business stakeholder will, in a meeting. | PR cannot be approved unless dbt test suite includes not_null + unique on PK and at least one accepted_values or expression_is_true business assertion. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol and CLI capabilities give a reasonable skeleton, but the Context Requirements section is left with literal placeholder text ('[Context item 1]', '[Context item 2]') and the Required Skills table is empty. An AI agent loading this role cannot determine what context files to load before starting work, what dbt project structure to expect, what Snowflake database and schema conventions to follow, or what CI/CD system is in use. The agent would have to ask clarifying questions before doing anything, which defeats the purpose of a deployment-ready role file.",
      "example_rewrite": "### Required Context \n - [ ] dbt project README (project name, profile, target schemas for dev/prod) \n - [ ] Snowflake schema map (raw, staging, intermediate, marts schema names and access credentials reference) \n - [ ] Source freshness SLA document (which sources update hourly vs daily vs event-driven) \n - [ ] Story Portal data dictionary (canonical definitions for story, session, prompt, completion event) \n - [ ] CI/CD pipeline config (which branch triggers dbt run in CI, which deploys to prod) \n \n ### Required Skills \n | Skill | When to Load | \n | dbt-modeling-patterns.md | Load at start of every model development workflow | \n | sql-optimization-snowflake.md | Load when model run time exceeds 60 seconds in dev | \n | data-vault-patterns.md | Load only when working on enterprise source-of-record models |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies four correct domain areas and four reasonable metrics, but it provides no actionable specifics. There are no source table names, no event names from the tracking spec, no grain definitions (is fct_story_completions one row per user per story, or one row per completion event?), no refresh cadence, and no indication of which models are blocked on upstream dependencies from the Data Engineer or Tracking Specialist. A new Analytics Engineer — human or AI — cannot build anything from this appendix without a separate discovery conversation.",
      "example_rewrite": "### Story Portal Data Models — Build Specification \n | Model | Grain | Source Tables | Blocking Dependency | \n | stg_app__story_events | One row per event per user per story | raw.app_events WHERE event_type IN ('story_start','story_complete','story_abandon') | Tracking Specialist must finalize event schema v2 (ticket #TS-44) | \n | fct_story_completions | One row per user per story per session | stg_app__story_events, dim_users, dim_stories | stg models must pass freshness check | \n | fct_prompt_effectiveness | One row per prompt per day | stg_app__story_events JOIN dim_prompts | dim_prompts requires Prompt taxonomy from Product Analyst | \n \n ### Key Metric Definitions (Canonical) \n | Metric | SQL Definition | Owner | \n | story_completion_rate | COUNT(CASE WHEN event_type='story_complete' THEN 1 END) / NULLIF(COUNT(CASE WHEN event_type='story_start' THEN 1 END),0) | Analytics Engineer — defined once in metrics layer |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4-5 Analytics Engineering-specific failure modes (metric definition duplication, business logic in staging, untested mart deployment, silent schema breaking changes). The current file has zero anti-patterns, which means an AI agent operating in this role has no guard rails against the most expensive and trust-destroying mistakes this role can make. This is the highest-risk gap in the document."
}
```