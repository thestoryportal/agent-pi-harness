```json
{
  "role": "backend-developer",
  "department": "engineering",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 6,
    "anti_pattern_quality": 9,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "All 6 principles are backend-specific and actionable. 'APIs as Contracts' and 'Measure Before Optimize' are particularly strong — they encode real engineering discipline rather than aspiration. Minor deduction because 'Fail Gracefully' is slightly generic; it could apply to any engineering role without modification. 'Security by Default' is solid but could be sharpened to the Supabase/RLS context specifically.",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The Receives From column is vague — 'Complex backend work, optimization requests' from Full Stack Developer is a category description, not an artifact. What file, document, or ticket format is actually handed off? Similarly 'Data model documentation' delivered to Data Engineer is mentioned in the Deliverables table but never connected to a specific format or named artifact. The Collaboration section names real roles correctly, which is good, but the artifact column needs concreteness.",
      "example_rewrite": "| Full Stack Developer | GitHub issue tagged `backend-handoff` with: failing query (SQL), current execution plan (EXPLAIN ANALYZE output), and performance target (e.g., <200ms p50) |\n| Data Engineer | `data-model-[feature].md` containing ERD diagram, table definitions, and known access patterns relevant to analytics use cases |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 9,
      "finding": "Seven anti-patterns, all backend-specific and actionable. 'N+1 queries', 'Design schema without access patterns', and 'Ignore migration rollbacks' are particularly strong — they are precise failure modes a backend developer actually encounters in Supabase/PostgreSQL work. The table format with Why and Instead columns is clear. Minor deduction: 'Add indexes blindly' and 'Skip input validation' edge toward universal backend advice rather than Supabase-specific pitfalls. An RLS-specific anti-pattern (e.g., writing permissive policies that bypass row filtering due to SECURITY DEFINER misuse) would strengthen the set.",
      "example_rewrite": null
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "The Iteration Protocol loop is explicit and well-structured. STOP points appear in both workflows. The CLI deployment rationale is stated. Required Skills table tells the AI which context files to load and when. Deduction for two gaps: (1) Workflow 2 Step 3 'IMPLEMENT' has no sub-steps — an AI agent hitting a complex endpoint has no guidance on sequencing (validation before business logic? transaction handling?). (2) The 'Required Context' checklist items are checkboxes with no path or format — the AI cannot locate `api-conventions.md` without knowing where it lives.",
      "example_rewrite": "### Required Skills\n| Skill | Path | When to Load |\n|-------|------|--------------|\n| `supabase-patterns.md` | `/docs/engineering/supabase-patterns.md` | Always |\n| `api-conventions.md` | `/docs/engineering/api-conventions.md` | Always |\n| `rls-patterns.md` | `/docs/engineering/rls-patterns.md` | RLS work only |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The appendix correctly identifies MVP state (frontend-only, IndexedDB) and maps Phase 2 features to Supabase components — that context is valuable. However the Draft Schema is too thin to be actionable: `consent_status text` should be an enum, `prompt_id text` has no foreign key reference, and there is no `users` profile table shown. More critically, the appendix does not tell the Backend Developer what to do *now* versus Phase 2 — the AI agent reading this cannot determine whether any backend work is in scope today. The quality bar (<100ms p50, zero data loss) repeats the main doc without adding Story Portal-specific reasoning.",
      "example_rewrite": "### Current Scope for Backend Developer\n**Phase 1 (MVP — No Action Required):** Story Portal is frontend-only. Backend Developer has no active tickets. Monitor `#engineering-backend` for Phase 2 kickoff signal from Engineering Manager.\n\n**Phase 2 Entry Criteria:** Backend Developer activates when Engineering Manager opens epic `STORY-BACKEND-001`. First deliverable: finalize schema for `stories` and `user_profiles` tables with Security Engineer RLS review before any migration runs.\n\n### Draft Schema Notes\n- `consent_status` must be `enum('pending','granted','revoked')` — never free text\n- `prompt_id` references a prompts catalog table (not yet designed — flag to Engineering Manager)\n- Add `user_profiles` table extending `auth.users` for display name and preferences"
    }
  ],
  "top_improvement": "Handoff artifacts are the highest-priority fix. The Collaboration section names the right roles but 'complex backend work' and 'optimization requests' are not artifacts — they are intentions. Every handoff row should specify the exact document, ticket format, or file that changes hands so the AI agent knows precisely what to receive or produce. Without this, the role cannot participate in multi-agent workflows reliably."
}
```