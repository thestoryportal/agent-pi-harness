```json
{
  "role": "privacy-officer",
  "department": "legal-compliance",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are textbook GDPR definitions lifted directly from regulatory language ('Privacy By Design', 'Data Minimization', etc.). They describe the law, not how THIS officer operates. 'Trust Is Earned' is a motivational poster slogan. None of the principles say anything about Story Portal's specific context — audio consent, festival participants, or child protection. A HIPAA officer and this role would share identical principles.",
      "example_rewrite": "Replace generic principles with operationally specific ones: | **Consent Before Recording** | No Story Portal audio capture begins without explicit, timestamped opt-in — not implied by platform use | | **Jurisdiction-First Assessment** | Before any feature ships, map which GDPR/CCPA/COPPA regime governs each data element | | **Silence Is Not Consent** | Pre-ticked boxes, bundled permissions, and 'by using this app' clauses are automatically rejected | | **Children Get Extra Gates** | Any feature accessible to under-13s triggers automatic COPPA review before development begins, not after |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs fail on both artifact specificity and role verification. 'Receives From: Legal Research Analyst' — this role does not appear in the charter context provided, making it a potentially hallucinated role. 'Receives From: Product Teams' is not a role name. 'Delivers To: All Departments' with artifact 'Privacy guidance' is maximally vague. No handoff specifies file format, template name, or system of record. 'Privacy reports' to General Counsel — what report? Weekly dashboard? Breach memo? DPIA sign-off form?",
      "example_rewrite": "| Receives From | Artifact | Format | Trigger | | Head of Product | Feature specification doc | Confluence page | Pre-sprint privacy review requested | | Head of Data Engineering | Data flow diagram | Miro/Lucidchart export | New pipeline or third-party integration | | Users (via DSR portal) | Subject rights request form | OneTrust ticket | User submits deletion/access request | | Delivers To | Artifact | Format | SLA | | General Counsel | DPIA sign-off memo | PDF, countersigned | Within 5 business days of assessment | | IT Manager | Privacy requirements spec | Jira ticket with acceptance criteria | Before sprint planning |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file. The template standard explicitly requires 3-5 role-specific anti-patterns. The 'DON'T' list in Boundaries partially substitutes but lists domain boundaries ('don't build product features'), not behavioral failure modes. It scores 1 rather than 0 only because the DON'T list exists at all. A Privacy Officer-specific anti-pattern would be something like 'Treating GDPR compliance as a checkbox rather than re-evaluating when processing purpose changes' — nothing like that appears anywhere.",
      "example_rewrite": "Add an Anti-Patterns section: **Anti-Patterns (Privacy Officer)** | Anti-Pattern | Why It Fails | Correct Behavior | | **Consent Bundling** | Combining recording consent with ToS acceptance invalidates GDPR consent for audio | Issue separate, granular consent for each processing purpose | | **Breach Minimization** | Classifying an incident as 'low risk' to avoid 72-hour GDPR notification creates regulatory and reputational liability | Default to notifying General Counsel within 24 hours; let Counsel decide on regulator notification | | **Policy-As-Shelfware** | Publishing a privacy policy without an enforcement mechanism or staff training | Every policy ships with a training module and a compliance check date | | **Scope Creep Silence** | Approving a PIA for 'analytics' and not re-reviewing when the analytics vendor adds ML profiling | Any change to processing purpose or vendor sub-processor triggers a new assessment |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists but is a copy-paste generic loop with no privacy-specific triggers. The Human/AI split in Deployment Notes is the strongest part — it clearly states AI processes routine DSRs and monitors compliance. However, 'Context Requirements' section contains literal placeholder text '[Context item 1]' and '[Context item 2]' which are unfilled template artifacts. Required Skills table is completely empty. An AI agent loading this role has no idea which context files to load, what a 'routine DSR' threshold is versus an escalation, or what tool to open first.",
      "example_rewrite": "Fix Context Requirements: **Required Context** - [ ] privacy-regulations.md — GDPR Article summaries, CCPA/CPRA text, COPPA thresholds - [ ] story-portal-data-map.md — Current inventory of all personal data collected by platform - [ ] dsr-decision-tree.md — Logic for routing deletion vs. access vs. portability requests - [ ] breach-response-playbook.md — Escalation thresholds and notification templates **Required Skills** | Skill | When to Load | | gdpr-assessment.md | Any EU user data processing review | | dsr-processing.md | OneTrust ticket assigned to Privacy Officer queue | | pia-template.md | Head of Product submits pre-launch privacy review request |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is the strongest section in the file — it correctly identifies audio recording consent, COPPA, multi-jurisdiction, and data minimization as platform-specific concerns. It scores below 7 because it stops at identification without becoming actionable. 'Priority 1: Recording consent framework' doesn't tell the AI or human what to actually do, what artifact to produce, or what done looks like. 'Analytics: Anonymous/aggregated data' is a standard and not a Story Portal-specific requirement or implementation detail.",
      "example_rewrite": "Upgrade Priority table to include deliverable and owner: | Priority | Focus | Deliverable | Definition of Done | | 1 | Recording consent framework | Consent flow wireframe + legal copy for audio opt-in modal | General Counsel signs off; Head of Product confirms implementation in app | | 2 | COPPA compliance gate | Age-verification decision tree; under-13 data handling procedure | Legal review complete; IT Manager confirms enforcement in registration flow | | 3 | Festival participant privacy | Event-specific privacy notice (short-form, plain language) | Approved by General Counsel; available at all festival touchpoints before launch |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section — this is the only dimension that scores below 3 and represents a total section omission, not just weak content. A Privacy Officer role with no anti-patterns gives an AI agent no guardrails against the most common and costly privacy failures (consent bundling, breach minimization, scope creep silence), making every other section in the file operationally riskier."
}
```