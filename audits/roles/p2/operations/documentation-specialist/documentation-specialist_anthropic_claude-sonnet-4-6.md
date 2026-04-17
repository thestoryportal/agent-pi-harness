```json
{
  "role": "documentation-specialist",
  "department": "operations",
  "scores": {
    "philosophy_depth": 2,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 2,
      "finding": "All six principles are one-line platitudes that could apply to any documentation role at any company in any industry. 'Accuracy Required: Correct information' and 'Currency Matters: Keep it updated' are definitions of words, not principles. None of the six principles reference Story Portal, festival operations, AI-assisted authorship, or the specific tension this role faces (AI drafts vs. human validates). The philosophy column describes what documentation is, not how this role thinks about its work.",
      "example_rewrite": "| **Festival-First Sequencing** | Festival playbooks are the highest-stakes docs we own — one missing step in a load-in procedure costs real money on event day. Prioritize operational accuracy over completeness speed. | | **AI Drafts, Humans Certify** | AI generates structure and first drafts; no document is published without a named human subject-matter expert signing off on accuracy. The AI is a drafting engine, not an authority. | | **Findability Over Completeness** | A perfect doc no one can find is useless. Every piece of content gets tagged, categorized, and search-tested before publishing — if you can't surface it in two clicks, it doesn't exist. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "The handoff tables list artifact names like 'Documentation requests' and 'Process content' that are too vague to act on. 'Knowledge Base Manager (Support)' is referenced as a collaborator but does not appear to exist in a standard operations charter — this may be a hallucinated role. There is no specification of artifact format (e.g., Confluence page, PDF, Notion template), no version or approval state required, and no trigger condition for when a handoff occurs. 'Delivers To: All Departments → Documentation' is the least specific handoff possible.",
      "example_rewrite": "| Receives From | Artifact | Format | Trigger | | Process Manager | Approved process map + step narrative | Notion page draft or Lucidchart export | When process is finalized and signed off by COO | | Subject Matter Experts | Reviewed draft with tracked-change comments | Google Doc with comment thread resolved | Within 48h of draft delivery, before publish step | | Delivers To | Artifact | Format | Trigger | | COO | Monthly documentation health report | PDF dashboard: pages created, pages outdated, top-searched terms | First Monday of each month |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "This role file has no dedicated Anti-Patterns section at all — it is entirely absent. The DO/DON'T boundary list exists but describes ownership boundaries, not behavioral failure modes. There is no list of how this specific AI-Primary documentation role goes wrong in practice: e.g., publishing AI-drafted content without expert review, creating duplicate pages instead of updating existing ones, or over-indexing on new content creation while legacy docs decay. The template standard explicitly requires 3-5 role-specific anti-patterns and this section is missing entirely.",
      "example_rewrite": "## Anti-Patterns to Avoid | Anti-Pattern | Why It Fails | Correct Behavior | | **Publish Before Expert Sign-Off** | AI-generated content sounds authoritative but may contain plausible inaccuracies; publishing without human validation erodes trust in the entire knowledge base | STOP at Review step; no page goes live without a named SME approval recorded in the doc header | | **Creating New Pages Instead of Updating** | Duplicate content fragments search results and confuses users; over time the KB becomes a graveyard of near-identical pages | Always search for existing coverage first; update and version-bump before creating a new page | | **Documentation Debt Accumulation** | Prioritizing new requests over maintenance means 40% of the KB becomes stale within 6 months | Maintenance cycle is non-negotiable — block 20% of weekly capacity for audits regardless of request queue |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and includes a STOP point, which is correct. However, an AI agent loading this role still faces critical ambiguity: there is no definition of what 'draft documentation' means in practice (what template to use, what sections are required, what tone/voice standard applies). The Agent Capabilities table lists generic capabilities like 'Text generation' without mapping them to specific workflows. The role does not specify what the AI should do when subject-matter expertise is unavailable, how to handle conflicting information from multiple sources, or what constitutes a complete-enough draft to trigger the human review STOP. The workflows lack decision branches.",
      "example_rewrite": "Add to Iteration Protocol: 'DRAFT step: Use the [Process Documentation Template v2] stored in Notion > Templates > Ops. Required sections: Purpose, Scope, Step-by-Step (numbered), Exceptions, Owner, Last Reviewed. If information gaps exist after one async request to the SME, flag the gap inline with [NEEDS VERIFICATION: {specific question}] and proceed to STOP — do not fabricate. Minimum viable draft for STOP trigger: all required sections present, gap flags explicit, estimated reading time under 5 minutes.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix identifies four correct documentation categories for a festival/event platform context (Festival Playbooks, Platform Guides, Onboarding, Operational Procedures) but provides no actionable specificity. There are no example document titles, no link to where these live, no indication of which festival phases generate documentation demand, and no description of what makes Story Portal documentation unique versus generic ops docs. The priorities table ranks festival docs first but does not explain why or what the seasonal documentation cycle looks like. A new team member reading this would not know what to actually open or create on day one.",
      "example_rewrite": "| Documentation | Story Portal-Specific Detail | Season Trigger | | Festival Load-In Playbook | Step-by-step for venue setup, credential distribution, vendor check-in; must include contingency steps for common failure modes (weather, no-show vendor) | 8 weeks before each festival | | Story Portal Platform Guide | How staff submit stories, moderate content, and publish to festival displays; screenshots required for each UI state | Update after every platform release | | Artist & Talent Onboarding Pack | What artists need to know about Story Portal submission, approval timeline, and on-site display locations | 6 weeks before festival |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific failure modes. This is the highest-priority fix because the section is completely absent — not just weak, but missing — and for an AI-Primary agent that autonomously drafts and publishes content, the absence of explicit behavioral guardrails (e.g., never publish without SME sign-off, never create duplicate pages) creates direct operational risk. A generic role file without anti-patterns produces generic agent behavior; a documentation agent without publish guardrails will eventually surface inaccurate AI-generated content to the whole organization."
}
```