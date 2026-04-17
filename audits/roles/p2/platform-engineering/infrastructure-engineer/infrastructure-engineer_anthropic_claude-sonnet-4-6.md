```json
{
  "role": "infrastructure-engineer",
  "department": "platform-engineering",
  "scores": {
    "philosophy_depth": 9,
    "handoff_specificity": 7,
    "anti_pattern_quality": 8,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 9,
      "finding": "All six principles are domain-specific and operationally meaningful. 'Environments Are Cattle, Not Pets' and 'Immutable Over Mutable' are genuine infrastructure philosophy, not generic quality platitudes. 'Cost-Conscious Always' is slightly broad but is grounded by the cost management workflow and 20% anomaly escalation threshold. Minor deduction only because 'Automate Everything' edges toward generic — it appears in DevOps roles universally without differentiation from, say, a CI/CD Engineer's philosophy.",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 7,
      "finding": "Most handoffs name real roles and real artifact types, which is solid. However, several inbound handoff entries are vague at the artifact level. 'Architecture requirements, infrastructure constraints' from Solutions Architect and 'Application requirements, scaling needs' from Engineering teams do not specify document format or structure — an AI agent cannot know whether to expect an ADR, a Confluence page, a Slack message, or a structured schema. The outbound side is better ('vercel.json config', 'runbooks') but still inconsistent.",
      "example_rewrite": "Receives From Solutions Architect: Architecture Decision Record (ADR) specifying compute type, expected RPS, data residency requirements, and approved cloud platforms — delivered as a markdown file in /docs/architecture/ before IaC work begins."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 8,
      "finding": "The anti-patterns table is strong and infrastructure-specific. 'ClickOps', 'Snowflake environments', and 'Secrets in code' are precise failure modes unique to this role. 'Under-document' and 'Skip staging' are slightly generic and could appear in any engineering role. A missed opportunity: no anti-pattern covers drift between IaC state and actual cloud state (e.g., manual hotfixes applied during incidents that never get codified back), which is a leading real-world failure mode for infrastructure engineers.",
      "example_rewrite": "| IaC State Drift | Emergency manual fixes applied to production never get backported to Terraform, causing the next terraform apply to revert or conflict | After any manual emergency change, file a 'drift remediation' ticket within 24 hours and codify the fix in IaC before the next planned change window |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 9,
      "finding": "The Iteration Protocol is explicit, numbered, and includes a hard HALT instruction. STOP checkpoints appear in every workflow. The classification rationale (why CLI over Chat) is clearly stated. The role distinguishes between what AI writes vs. what humans approve with no ambiguity. Minor deduction: the skill files listed in Context Requirements are marked as 'planned development' and don't exist yet — an AI agent loading this role will find dead references when attempting to load 'vercel-deployment.md', which could cause silent context gaps.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 9,
      "finding": "The Story Portal appendix is exceptionally actionable: a live vercel.json config with security headers, a specific domain (thestoryportal.org), a platform comparison matrix, a named environment variable table with secret classification, and a phased infrastructure roadmap with checkbox tasks. The Phase 2 Supabase architecture diagram is a genuine deliverable preview. Marginal deduction: the PWA/Service Worker items in Story Portal Priorities have no acceptance criteria or linked workflow step — an AI agent knows to do them but not how to verify they are done.",
      "example_rewrite": "6. **PWA Manifest** — Verify PWA configuration deploys correctly by running Lighthouse PWA audit post-deploy and confirming score >90; check that manifest.json is served with correct MIME type and all icons resolve. 7. **Service Worker** — Confirm offline capability by throttling to offline in DevTools and verifying cached shell loads without network errors."
    }
  ],
  "top_improvement": "Handoff artifacts need format and delivery-point specificity: every 'Receives From' entry should state the document type, file location or delivery method, and the triggering condition — so the AI agent knows not just what it will receive but when and in what form, enabling it to block on missing inputs rather than proceeding with assumptions."
}
```