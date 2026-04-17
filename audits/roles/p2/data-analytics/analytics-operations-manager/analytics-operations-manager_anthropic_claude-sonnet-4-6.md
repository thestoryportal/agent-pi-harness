```json
{
  "role": "analytics-operations-manager",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 2,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 4,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 2,
      "finding": "All 6 principles are one-line platitudes with zero operational specificity. 'Ops Enables Analytics' = 'Good ops = good analytics' is circular and meaningless. 'Continuous Improvement' is a generic Lean/Agile slogan copy-pasted from a management textbook. None of the principles describe HOW this role operationalizes them in the context of analytics tooling, access governance, or Story Portal's specific privacy constraints. A philosophy principle should be a decision-making guide — none of these are.",
      "example_rewrite": "Replace generic principles with decision rules specific to this role. Example: | **Access Follows Least Privilege** | Every access grant starts at the minimum required scope — analysts get read-only by default; write access requires documented justification from Head of Data & Analytics; no standing admin access for any role. | | **Governance Is Upstream, Not Overhead** | Privacy and consent requirements (e.g., audio metadata rules, festival anonymization) are embedded into access provisioning templates BEFORE requests arrive — not reviewed after the fact. | | **Tool Debt Is Invisible Until It Isn't** | License sprawl, stale permissions, and undocumented configs compound silently; a monthly ops audit is non-negotiable, not optional. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs name vague artifact categories ('Priorities', 'Access requests', 'Updates, issues', 'Tool access', 'Operations reports') and use placeholder roles like 'All Analytics Team' and 'All Data Consumers' that do not correspond to named roles in any charter. There is no specification of artifact format, trigger condition, or delivery mechanism. 'Receives: Vendors → Updates, issues' tells an AI agent nothing actionable. The template standard explicitly requires actual role names and actual artifacts — this file violates both.",
      "example_rewrite": "| Receives From | Artifact | Format | Trigger | | Analytics Engineer | dbt Cloud project access request | Slack #data-access form + Jira ticket | New hire or project kickoff | | Head of Data & Analytics | Quarterly tool governance priorities | Written brief in Notion | First week of each quarter | | Delivers To | Artifact | Format | Trigger | | Analytics Engineer | Provisioned dbt Cloud role + confirmation | Email + access audit log entry | Within 24h of approved request | | Head of Data & Analytics | Monthly Operations Report (tool health, license usage, open access requests, compliance flags) | Notion doc, shared async | Last Friday of each month |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "This role file contains NO anti-patterns section whatsoever. The template standard requires 3-5 role-specific anti-patterns. The Boundaries section lists DO/DON'T items but these are ownership boundaries, not behavioral anti-patterns. Anti-patterns should describe failure modes this specific role is prone to — e.g., over-provisioning access to reduce friction, treating governance as a one-time setup rather than ongoing enforcement, or becoming a bottleneck by manually handling every access request instead of building self-service. None of this exists in the file.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: | Anti-Pattern | Why It Happens | Why It's Dangerous | Correct Behavior | | **Access Generosity** | Granting broader permissions than requested to avoid repeat requests | Creates audit failures, violates least-privilege, exposes PII and audio metadata | Grant minimum scope; require re-request with justification for elevation | | **Governance Theater** | Publishing policies in Notion but never enforcing or auditing them | False compliance posture; discovered during incident or external audit | Schedule quarterly access audits; flag and remediate violations within 5 business days | | **Ops as Bottleneck** | Handling every tool question and access request manually | Analyst productivity blocked; ops manager becomes single point of failure | Build self-service runbooks and automate routine provisioning where possible | | **Tool Config Drift** | Making undocumented config changes to resolve urgent issues | Impossible to audit, reproduce, or roll back | All config changes logged in ops changelog before execution |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Context Requirements section is completely unfilled — '[Context item 1]' and '[Context item 2]' are literal placeholders, and the Required Skills table has no entries. An AI agent loading this role has no idea what context files to load, what platforms to authenticate against, or what the current operational state is. The Iteration Protocol exists (positive) but the STOP points in workflows are labeled as human checkpoints yet the file never specifies WHICH human approves what — 'STOP → Request validated' by whom? The Hybrid classification says humans handle 'sensitive access' but never defines what 'sensitive' means in this context.",
      "example_rewrite": "Fill Context Requirements with specifics: Required Context: [ ] Current tool inventory (platforms, versions, license counts) [ ] Active access policy document (link to Notion governance page) [ ] Open access request queue (Jira board link) [ ] Last audit report date and findings [ ] Vendor contract renewal dates. Required Skills: | analytics-access-management.md | When provisioning any user access | | data-governance-frameworks.md | When defining or updating policies | | rbac-patterns.md | When configuring role-based access in warehouse or BI tools |. For STOP points, specify: 'STOP → Head of Data & Analytics approves any access grants to raw audio metadata tables or PII fields.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies the right domains (audio metadata, consent, PII, festival data) but remains at a surface level. The tool stack lists options with '(if needed)' qualifiers — an ops manager role should reflect actual deployed tools, not a menu. The Governance Focus table lists requirements ('Metadata only', 'Strict controls') without specifying what those controls ARE or how this role enforces them operationally. There is no reference to Story Portal-specific workflows like onboarding a new musician to the platform, handling a consent withdrawal, or managing access for festival partner integrations.",
      "example_rewrite": "Replace generic rows with Story Portal-specific operational procedures: | Scenario | Ops Action | | New musician onboarded to Story Portal | Provision Amplitude read-only access to their own story metrics; NO access to other artists' data; log in access audit | | Consent withdrawal received | Within 24h: revoke data subject's event data from Amplitude exports; flag to Head of Data & Analytics; document in consent log | | Festival partner requests analytics access | Escalate to Head of Data & Analytics before any provisioning; apply anonymization filter to all festival data exports; time-limit access to event window + 30 days | | Audio file ingested | Confirm pipeline writes metadata only (duration, format, timestamp) to warehouse; verify no raw audio path stored in analytics layer |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section — this is the most critical gap because it is entirely absent (not just weak), and anti-patterns are the primary mechanism by which an AI agent avoids role-specific failure modes. Without them, the AI has no guard rails against over-provisioning access, rubber-stamping governance, or becoming an operational bottleneck — all high-probability failure modes for an ops role operating in a privacy-sensitive context like Story Portal."
}
```