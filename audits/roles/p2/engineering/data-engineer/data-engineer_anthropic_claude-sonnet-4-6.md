```json
{
  "role": "data-engineer",
  "department": "engineering",
  "scores": {
    "philosophy_depth": 9,
    "handoff_specificity": 7,
    "anti_pattern_quality": 6,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 9,
      "finding": "All six principles are genuinely role-specific and operationally meaningful. 'Idempotency Always' and 'Schema Is Contract' are precise engineering commitments, not values-poster language. 'Reliability Over Speed' even includes a testable corollary ('late data is better than wrong data'). Minor deduction: 'Cost Awareness' is the weakest — it states an obvious consequence of scale rather than a decision rule. It would be stronger if it named a behavior.",
      "example_rewrite": "Cost Awareness — Every pipeline design decision includes a cost estimate. If a streaming approach costs 10x a micro-batch alternative with equivalent latency, choose micro-batch and document the tradeoff."
    },
    {
      "dimension": "handoff_specificity",
      "score": 7,
      "finding": "The handoff tables name real roles and real artifact types, which is solid. The coordination diagrams add useful flow context. However, the 'Delivers To' rows are still partially vague: 'Cleaned, validated data in warehouse' does not specify the form — is it a dbt model, a materialized view, a raw schema? The AI agent receiving this handoff cannot infer the exact artifact to produce or accept.",
      "example_rewrite": "Delivers To Analytics Engineer: dbt-modeled staging tables in the `stg_` schema of Snowflake, validated via dbt tests, with a freshness SLA documented in `schema.yml`. Handoff is complete when the Analytics Engineer confirms downstream models compile without errors."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 6,
      "finding": "The six anti-patterns are directionally correct but read as generic data engineering advice applicable to any engineer at any company. 'Hardcode credentials' and 'Skip documentation' would appear identically in a Backend Developer or Platform Engineer role. None of the anti-patterns reference Story Portal-specific risks or the Data Engineer's specific boundary violations (e.g., drifting into analytics modeling, or building product DB schemas). The checklist format also lacks severity signal.",
      "example_rewrite": "Don't model business logic in pipeline transformations — Why: Embedding revenue calculation or user segmentation rules in ETL code means Analytics Engineer cannot govern the definitions, creating two sources of truth. Instead: Deliver raw or lightly cleaned data to the warehouse; Analytics Engineer owns business logic in dbt models. Escalate ambiguous cases to Head of Data."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "The iteration protocol is present and includes a hard HALT instruction. The three workflows each have explicit STOP checkpoints with labeled trigger conditions. The deployment rationale for CLI is clear and justified. Minor gaps: the skill files listed in Context Requirements are flagged as 'planned development,' meaning an agent loading this role today gets skill pointers that resolve to nothing. The agent also has no fallback instruction for when a referenced skill file is absent.",
      "example_rewrite": "Required Skills — If skill file is not available in context, state explicitly: 'Skill file `dbt-patterns.md` not loaded. Proceeding with general dbt best practices; flag for human review before production deployment.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The Phase 2 activation note is honest and project-accurate — the role correctly self-describes as dormant during MVP rather than fabricating current scope. The Phase 2 data domain table and technical integration points are specific to Story Portal's actual architecture (Supabase, GA4, Whisper). Minor gap: the 'Data Quality Priorities' list names consent data integrity as GDPR-critical but provides no actionable guidance on what that means for pipeline design (retention periods, anonymization requirements, audit log schema).",
      "example_rewrite": "Consent Data Integrity — Consent records must include immutable audit trail: user_id, consent_type (GDPR_marketing, GDPR_analytics), granted_at timestamp, ip_hash, consent_version. Pipeline must never UPDATE or DELETE consent rows; append-only. Backfill prohibited without Security Engineer sign-off."
    }
  ],
  "top_improvement": "Rewrite the anti-patterns section to be role-boundary-specific: at least two anti-patterns should describe the Data Engineer's most likely boundary violations (drifting into analytics modeling, building product DB schemas, or deploying infrastructure directly), with explicit escalation paths. Generic anti-patterns like 'hardcode credentials' belong in a shared engineering standards doc, not in a role-differentiating template."
}
```