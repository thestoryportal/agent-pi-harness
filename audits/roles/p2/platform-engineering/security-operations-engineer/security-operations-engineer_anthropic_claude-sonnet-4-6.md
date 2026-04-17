```json
{
  "role": "security-operations-engineer",
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
      "finding": "All 6 principles are role-specific and avoid generic quality platitudes. 'Secrets Are Sacred' and 'Enable, Don't Block' are particularly strong — they capture the operational tension SecOps faces daily. Minor deduction: 'Zero Trust Operations' is a well-known industry term that reads slightly borrowed rather than interpreted for this specific role's operational context. It would score higher if it explained what zero trust means *in practice* for this SecOps agent (e.g., every service-to-service call, every pipeline credential, every API key is treated as potentially compromised until verified).",
      "example_rewrite": "**Zero Trust Operations** | Every credential, service call, and pipeline artifact is treated as potentially compromised — verification is the default, not the exception. No implicit trust based on network location or prior success."
    },
    {
      "dimension": "handoff_specificity",
      "score": 7,
      "finding": "Most handoffs name real roles and real artifact types. The Receives/Delivers tables are solid. However, several entries are still somewhat vague on the artifact side. 'Security policies, requirements, incident investigation findings' (from Security Engineer) is three different things bundled together with no format specified. Similarly, 'Incident alerts, vulnerability reports, operational issues' to Security Engineer doesn't distinguish a Slack alert from a formal incident report. The handoff diagram also omits CI/CD Engineer and Infrastructure Engineer who appear in the tables, creating an incomplete picture.",
      "example_rewrite": "| Security Engineer | Receives: `security-policy-v{n}.md` (policy documents), CVSS-scored vulnerability escalation tickets (Jira/GitHub Issues), post-incident RCA reports | Delivers: Real-time incident alerts (PagerDuty/Slack #security-incidents), weekly `vulnerability-status-report.md`, ad-hoc operational blockers as GitHub Issues tagged `secops-escalation` |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 8,
      "finding": "Seven anti-patterns are listed, all role-specific and grounded in real SecOps failure modes. 'Alert on everything → Alert fatigue' and 'Fix vulns in other teams' code → Wrong ownership' are excellent because they capture the exact boundary violations SecOps agents are likely to commit. Minor deduction: 'Store secrets in code' is so universal it borders on generic — every developer role could have this. A stronger entry would target a SecOps-specific failure like rotating secrets in production without coordinating dependent service restarts, or closing a vulnerability ticket after patching without re-scanning to verify.",
      "example_rewrite": "| Mark vuln remediated without re-scanning | False closure; vulnerability may persist through transitive dependency | Re-run scan tool against same artifact after fix is deployed; only close ticket when scan returns clean |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 9,
      "finding": "This is the strongest dimension. The Iteration Protocol is explicit, the STOP points are clearly labeled in every workflow, the NEVER/ALWAYS rules at the bottom of Deployment Notes are unambiguous, and the Hybrid classification is well-explained with a concrete split of what AI executes vs. what humans approve. The CLI rationale is also provided, which helps an agent understand its execution environment. Minor deduction: the Context Requirements section lists skill files (secrets-management.md, vulnerability-scanning.md) that may not exist yet — an agent loading this role would not know whether to halt or proceed if those files are missing.",
      "example_rewrite": "Add a fallback note: 'If skill file is not found in project knowledge base, proceed using role expertise and flag the missing skill file to Head of Platform before executing sensitive operations.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix correctly acknowledges MVP minimalism and provides a Phase 2 activation map. The Supabase credential rotation schedule is genuinely specific and actionable. However, the CI/CD example is a code snippet stub that doesn't reflect Story Portal's actual pipeline structure — it reads as a generic example rather than a configured artifact. The 'Key Coordination Points' table mostly duplicates the main Collaboration section without adding project-specific context. Missing: any mention of what triggers SecOps to become active (e.g., the specific Phase 2 milestone or PR that activates backend responsibilities).",
      "example_rewrite": "**SecOps Activation Trigger:** SecOps responsibilities activate when the Phase 2 backend PR introducing `SUPABASE_SERVICE_ROLE_KEY` usage is merged. At that point: (1) configure GitHub repository secrets per the secrets inventory template, (2) enable Dependabot for npm ecosystem targeting Next.js and Supabase client packages, (3) add `npm audit --audit-level=high` as a required CI check blocking merge to `main`."
    }
  ],
  "top_improvement": "Handoff specificity: Replace bundled artifact descriptions with format-specific entries (document name, channel, ticket tag) so that when SecOps delivers to or receives from Security Engineer, both agents know exactly what object is being transferred and where it lives — eliminating the ambiguity between a Slack ping, a formal report, and a tracked ticket."
}
```