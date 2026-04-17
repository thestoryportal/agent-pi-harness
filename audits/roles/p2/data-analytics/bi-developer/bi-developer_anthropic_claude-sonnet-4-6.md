```json
{
  "role": "bi-developer",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic BI platitudes that could appear in any dashboard role at any company. 'Clarity Over Complexity' and 'User-Centered Design' are textbook filler. None reference Story Portal's steampunk aesthetic, festival context, privacy-first constraints, or the specific tension between real-time festival ops data and aggregate privacy requirements. There is no principle that would distinguish this role from a BI Developer at a bank or a hospital.",
      "example_rewrite": "Replace generic principles with role-specific ones: | **Festival-First Rendering** | Festival dashboards serve live operations — latency over 3 seconds during events is a product failure, not a performance issue | | **Privacy Through Aggregation** | Story Portal never exposes individual user journeys; every visualization defaults to cohort-level (n≥10) unless explicitly approved by Data Governance | | **Steampunk as Signal** | Visual design choices (warm ambers, sepia tones, vintage typography) are not decoration — they reinforce brand immersion and must be preserved across all dashboard updates |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but not actual artifacts with formats, schemas, or naming conventions. 'Receives data models from Analytics Engineer' is not actionable — an AI agent cannot act on it. What models? In what format? What naming convention? The outbound side is worse: 'Delivers Dashboards to All Teams' specifies no dashboard URLs, no Looker explore names, no Tableau workbook naming standard, no sign-off artifact. The UX Designer handoff lists 'design guidance' which is completely undefined.",
      "example_rewrite": "| Receives From | Artifact | Format | Trigger | \n|---|---|---|---| \n| Analytics Engineer | Certified data model | LookML view file (certified_ prefix) committed to main branch in looker-models repo | Model tagged 'bi-ready' in dbt docs | \n| UX Designer | Dashboard wireframe | Figma file shared via #bi-design Slack channel with frame named '[dashboard-name]-v[n]-approved' | Designer posts 'APPROVED FOR BUILD' comment in Figma |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "The role file contains NO anti-patterns section at all. The template standard explicitly requires 3-5 role-specific anti-patterns. The DO/DON'T boundaries section exists but lists domain ownership rules, not anti-patterns — it describes what the role should not own, not the bad behaviors a BI Developer specifically falls into (e.g., building dashboards on uncertified models, using misleading chart types for engagement funnels, duplicating logic that belongs in LookML, over-indexing on aesthetics at the expense of query performance, or exposing individual-level story data in aggregate views).",
      "example_rewrite": "Add a dedicated Anti-Patterns section: | Anti-Pattern | Why It Happens | Why It's Harmful | Correct Behavior | \n|---|---|---|---| \n| **Building on raw tables** | Stakeholder pressure to ship fast | Bypasses Analytics Engineer's certified models; breaks when schema changes | Only connect to views with the certified_ prefix in the looker-models repo | \n| **Funnel charts with non-sequential steps** | Copy-paste from prior dashboard | Misrepresents story completion rates to Leadership; inflates conversion optics | Audit every funnel against the canonical Story Journey map before publishing | \n| **Duplicating LookML metrics in DAX/calculated fields** | Power BI familiarity | Creates metric divergence — two dashboards show different 'completion rate' values | Any new metric must be defined in LookML first; BI layer only references, never redefines |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists (credit for that) and CLI deployment is named, but an AI agent loading this role still cannot answer: What BI tool is primary for Story Portal? What SQL dialect does the warehouse use? What does 'connect data sources' mean operationally — what credentials, what warehouse, what schema? The Context Requirements section is literally placeholder text ('[Context item 1]', '[Context item 2]') and the Required Skills table is empty with a format note left in. This means the role is incomplete and an AI agent would have no context to load before starting work.",
      "example_rewrite": "Replace placeholder Context Requirements with: **Required Context** \n- [ ] looker-models repo access (read/write to feature branches) \n- [ ] Snowflake credentials for ANALYTICS_PROD schema \n- [ ] Story Portal brand guide (steampunk_palette.json) \n- [ ] Certified metrics glossary (confluence: /Data/Metrics-Glossary) \n- [ ] Current festival event schedule (ops-calendar.md) \n\n**Required Skills** \n| Skill | When to Load | \n|---|---| \n| lookml-syntax.md | Any Looker dashboard build | \n| snowflake-sql-dialect.md | Any SQL query against warehouse | \n| story-portal-metrics.md | Any engagement or content dashboard |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix is the strongest section in this file. It names four specific dashboards with audiences and purposes, maps metrics to chart types, and calls out steampunk aesthetic and festival real-time context explicitly. Score is capped at 7 because priorities are listed without acceptance criteria or delivery sequencing — 'Priority 1: Story engagement dashboard' does not tell an AI agent what done looks like for that dashboard, what data sources feed it, or what the launch dependency is (e.g., does it require the Analytics Engineer to certify the engagement model first?).",
      "example_rewrite": "Extend the Dashboard Priorities table: | Priority | Dashboard | Launch Dependency | Definition of Done | \n|---|---|---|---| \n| 1 | Story Engagement Overview | certified_story_events LookML view merged to main | Funnel from prompt-start → story-complete live in Looker; Leadership sign-off in #data-leadership Slack | \n| 2 | Festival Operations View | Ops team confirms real-time event feed; latency SLA <2s validated | Dashboard auto-refreshes every 60s; Festival Director approves layout in UAT |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 BI Developer-specific failure modes (e.g., building on uncertified raw tables, duplicating LookML metrics in the viz layer, exposing individual-level story data). This section is entirely missing — not just weak — which means there is zero guardrail content preventing the most common and damaging BI mistakes in a privacy-sensitive, real-time festival context."
}
```