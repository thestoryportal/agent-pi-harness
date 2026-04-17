```json
{
  "role": "head-of-platform-engineering",
  "department": "platform-engineering",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 6,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "All 6 principles are present and role-specific rather than generic. 'Platform as Product' and 'Own the Boring Stuff' are distinctively platform-engineering-flavored. However, 'Automate Everything' and 'Incidents Are Learning Opportunities' border on industry clichés that appear in nearly every SRE/DevOps role without differentiation. They pass the bar but don't excel.",
      "example_rewrite": "Replace 'Automate Everything' with: 'Automate at the Seam — Automation is prioritized at integration points between teams (deployment handoffs, environment provisioning, secret rotation) where manual steps create the most friction and failure risk, not for its own sake.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Handoff tables list role names correctly but artifact descriptions are too vague to be actionable. 'Technology strategy, organizational priorities' from CTO and 'Deployment requirements, pain points' from Engineering Manager describe categories of information, not actual deliverable artifacts. A CI/CD Engineer or SRE receiving 'Platform capabilities, documentation' from this role has no idea what format, cadence, or specific document to expect.",
      "example_rewrite": "Delivers To Engineering teams: 'Quarterly Platform Capabilities Changelog (Markdown doc listing new services, deprecated endpoints, and breaking changes), plus updated deployment runbooks in /docs/platform/runbooks/' — and Receives From Engineering Manager: 'Deployment Friction Report (monthly Confluence page listing blocked deployments, failed pipelines, and team-reported pain points from the previous sprint cycle).'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Six anti-patterns are present and most are contextually appropriate for a platform leader. 'Micromanage team members' and 'Neglect career development' are generic people-management warnings that would appear in any Head-of-X role file. The platform-specific ones ('Over-engineer for scale,' 'Ignore developer feedback,' 'Skip postmortems') are strong. The generic two dilute the set.",
      "example_rewrite": "Replace 'Neglect career development' with: 'Treat platform work as invisible — Failing to publicize reliability wins, deployment improvements, or cost savings makes the platform team appear as a cost center rather than a value driver, eroding budget and headcount support. Instead: publish monthly platform health newsletters and celebrate incident-free deployment milestones.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "The Deployment Notes section is one of the stronger elements in the file. The Hybrid mode table mapping Activity to Browser/CLI with rationale is genuinely useful. The Iteration Protocol loop is explicit. The critical callout box clearly distinguishes AI advisory capacity from human decision authority. Minor gap: the skill files are flagged as 'planned development' with no fallback instruction, leaving an AI agent uncertain what to do when those files don't exist yet.",
      "example_rewrite": "Add to Skills section: 'If a skill file is not yet available, proceed using the role's Core Responsibilities and Quality Standards sections as the governing framework. Flag the missing skill file in your session output so HR can prioritize creation.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix correctly identifies the MVP infrastructure gap (no deployment, no CI/CD, no monitoring) and maps it to a prioritized initiative list. The quality bar table pulling from APP_SPECIFICATION is a strong, concrete touch. However, the 'Key Decisions Pending' table lists stakeholders by title only (CTO, Engineering) without linking to how this role drives those decisions to closure — there's no workflow trigger or timeline, making it a status list rather than an action plan.",
      "example_rewrite": "Add a 'Decision Owner & Next Action' column to Key Decisions Pending, e.g.: Deployment Target | Vercel vs. Netlify vs. Cloudflare | CTO, Engineering | Head of Platform delivers Technology Evaluation Report (see Workflow 2) to CTO by end of Sprint 1; decision gates CI/CD pipeline work starting Sprint 2."
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix: the current artifact descriptions ('technology strategy,' 'deployment requirements,' 'platform capabilities') are category labels, not deliverables. Every handoff entry should name a specific document type, format, and cadence so that receiving roles — and any AI agent playing those roles — know exactly what to expect and when. This is the gap most likely to cause coordination failures in actual deployment."
}
```