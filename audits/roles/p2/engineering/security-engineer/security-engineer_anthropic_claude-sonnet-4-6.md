```json
{
  "role": "security-engineer",
  "department": "engineering",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 8,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "Four of the six principles hold up well — 'Defense in Depth', 'Least Privilege', 'Enable, Don't Block', and 'Transparency Builds Trust' are role-specific and meaningful. However, 'Security by Design' is a well-worn industry slogan that nearly every security framework recites verbatim, and 'Trust but Verify' is a geopolitical cliché that is especially odd for a security role — a Security Engineer's entire job is to NOT simply trust. Neither principle explains what it means *for this role on this project*. The checklist requires 6+ principles that are not generic; two of these six are borderline.",
      "example_rewrite": "Replace 'Security by Design' with: 'Threat Model First — Before writing a spec, identify the top three attack vectors. No authentication design leaves the drawing board without a documented threat model.' Replace 'Trust but Verify' with: 'Zero Trust at the Boundary — Every request to a protected resource is treated as potentially adversarial. Auth checks are not optional, not skippable for internal callers, and not delegated to the client.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 8,
      "finding": "The handoff tables and the Backend Developer coordination diagram are strong — artifacts are named (auth/RLS design specifications, incident reports, compliance documentation) and receiving roles are actual charter roles. The one gap is the inbound 'Receives From Product' row: it lists 'Feature requirements (assess security implications)' but does not name the artifact format or the Product role's exact title as it would appear in the charter. If the charter calls that role 'Product Manager' rather than 'Product', this is a hallucinated role reference. Additionally, the handoff to QA says only 'Security testing coordination' with no artifact named.",
      "example_rewrite": "Change the QA row from 'Security testing coordination' to: 'Delivers to QA Engineer: Signed security test plan (security-test-plan.md) listing test cases, OWASP coverage matrix, and pass/fail criteria for each mandatory review trigger.' Change the inbound Product row to match the exact charter role name and specify: 'Receives from Product Manager: Feature brief (feature-brief.md) — Security Engineer produces a threat assessment memo within 48 hours of receipt.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "The anti-patterns table has eight entries, which is good volume, and several are genuinely role-specific: 'Use service key in frontend' is Supabase-specific and precise, 'Implement custom crypto' is a classic security engineer failure mode, and 'Block without explanation' reflects the Enable-Don't-Block philosophy. However, 'Security through obscurity' is a textbook entry that appears in every OWASP training slide deck — it names no Story Portal context and gives no actionable alternative beyond 'use proper controls'. Similarly, 'Trust client input / Validate on server' is so generic it would belong in a Backend Developer role file unchanged.",
      "example_rewrite": "Replace 'Security through obscurity' with: 'Hiding the share-link ID instead of enforcing RLS — Generating long random share-link tokens feels secure but does not replace a storage policy. Always pair obscure identifiers with an explicit RLS policy that checks token validity and expiry.' Replace 'Trust client input' with: 'Letting the Frontend Developer own consent record writes — Consent records are PII and audit-critical. All writes must go through a server-side function that validates the payload schema, stamps the timestamp server-side, and logs to the audit trail. Never accept a client-submitted timestamp for a consent record.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 9,
      "finding": "This is the strongest dimension. The Iteration Protocol is explicit, the CLI vs Browser deployment table tells the agent exactly which environment to use per task type, STOP points appear in every workflow, severity levels are defined for incident response, and the 'Security Review Triggers' table gives the agent a deterministic checklist for deciding when to engage. The Deployment Notes section clearly delineates what the AI executes versus what requires human approval. Minor gap: the iteration protocol says 'STOP → Present specification or findings' but does not specify the artifact format to present (e.g., inline markdown, a named file, a checklist). An agent could reasonably be unsure whether to produce a prose document or a structured checklist.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 9,
      "finding": "Excellent. The appendix correctly identifies that MVP is frontend-only and defers heavy security work to Phase 2, which prevents the agent from over-engineering a local-storage app. The RLS classification table with per-table sensitivity levels and policy ownership is immediately actionable. The planned architecture diagram is project-specific. The six Phase 2 priorities are ordered by urgency. The only minor gap: 'Consent Records (PII)' is flagged as High sensitivity requiring Security Engineer design, but there is no stub specification or even a field list for what a consent record contains — the agent has no starting point if asked to begin that design today.",
      "example_rewrite": null
    }
  ],
  "top_improvement": "Replace the two generic philosophy principles ('Security by Design' and 'Trust but Verify') with Story Portal-specific, operationally precise principles that describe actual behaviors the agent should exhibit — particularly around threat modeling before spec writing and zero-trust enforcement at Supabase RLS boundaries. This is the highest-priority fix because philosophy principles cascade into every decision the agent makes; generic principles produce generic outputs."
}
```