```json
{
  "role": "contract-manager",
  "department": "legal-compliance",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are generic contract platitudes that could apply to any contract manager at any company. 'Enable Deals', 'Clarity Prevents Disputes', and 'Template First' are textbook phrases with no operational specificity. There is no reference to Story Portal's actual business context (festival production timelines, content rights for user-generated stories, partnership structures). The 'Meaning' column adds nothing — 'Contracts support relationships' under 'Enable Deals' is a circular restatement, not a behavioral guide.",
      "example_rewrite": "| **Festival-First Urgency** | Festival vendor agreements have hard event dates — a 3-day negotiation delay can collapse production. Turnaround on vendor SOWs is 48 hours max, not standard 5-day cycles. | **Content Rights by Default** | Every Story Portal partner agreement defaults to non-exclusive, revocable content licensing. Never draft exclusive rights without General Counsel sign-off. | **Redline Threshold Discipline** | Accept counterparty redlines on liability caps only if they stay within pre-approved 2x contract value bands. Anything outside triggers a STOP to General Counsel, not a counter-proposal."
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but describe artifacts in vague categorical terms. 'Contract requests' from Business Teams, 'Executed contracts' to Business Teams, and 'Obligation summaries' to Finance are format-free and trigger-free. There is no specification of what format the artifact takes (e.g., PDF in DocuSign CLM, Ironclad record ID, spreadsheet), what state it must be in to transfer, or which specific roles within 'Business Teams' are valid senders. 'Legal Research Analyst' appears in Works With but is absent from both handoff tables despite being the most obvious research dependency.",
      "example_rewrite": "| Receives From | Role | Artifact | Format | Condition | **Sales Director** | Signed Contract Request Form (Ironclad intake form, Deal ID attached) | Ironclad workflow trigger | Deal value confirmed by Finance Director | **Legal Research Analyst** | Jurisdiction Risk Memo (PDF, max 2 pages) | Email attachment | Required before drafting non-standard governing law clauses | **Delivers To** | **Vendor Manager** | Executed Vendor MSA + SOW (DocuSign completed envelope, Ironclad record updated) | DocuSign envelope link | All signature blocks complete, stored in CLM under vendor record |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "This role file contains zero anti-patterns. The section does not exist. The ESCALATE block in Boundaries provides four escalation triggers but these are not framed as failure modes or behavioral warnings — they are routing rules. There is no 'DON'T DO THIS' behavioral guidance specific to a Contract Manager in an AI-assisted Hybrid deployment, such as AI over-accepting counterparty redlines, generating contracts without a confirmed Deal ID, or drafting non-template agreements without escalation. This is the most critical structural omission in the file.",
      "example_rewrite": "### Anti-Patterns — What This Role Must Never Do | Anti-Pattern | Why It Fails | Correct Behavior | **Drafting from Scratch Without Checking Template Library** | Creates inconsistent terms, duplicates legal review effort, and introduces unapproved clauses. | Always check /templates in Ironclad first. If no template exists, flag to General Counsel before drafting. | **Accepting Any Liability Cap Redline in Agent Mode** | AI cannot assess organizational risk tolerance without current Finance and Legal context. | STOP at every liability cap change. Deliver redline summary to General Counsel; do not counter-propose. | **Treating 'Business Terms Decided' as a Given** | Sales Directors sometimes send requests with aspirational terms not approved by Finance. | Verify Deal ID and Finance Director confirmation before any drafting begins. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and correctly identifies the Human/AI split in the Hybrid section, but an AI agent loading this role would face three blocking ambiguities: (1) Context Requirements section has unfilled placeholders '[Context item 1]' and '[Context item 2]' — these are literally empty, making the role unloadable in a compliant framework. (2) Required Skills table has only a placeholder format note with no actual skills listed. (3) The AI/Human split in the Hybrid section uses categorical language ('AI drafts', 'Human negotiates') but provides no decision rule for edge cases — e.g., what triggers the AI to stop drafting and escalate mid-task when it encounters a non-standard indemnification clause from a counterparty.",
      "example_rewrite": "### Required Context | Context Item | Source | When to Load | **Active Contract Queue** | Ironclad CLM dashboard export | Load at session start for any drafting or renewal task | **Approved Template Library** | /legal/templates/ in document store | Load before any drafting activity | **Counterparty Risk Tier** | Vendor Manager's Vendor Risk Register (current quarter) | Load before any vendor contract negotiation | ### Edge Case Rule: If AI encounters indemnification language outside pre-approved bands (>2x contract value or uncapped), STOP immediately, generate a Redline Issue Summary (template: redline-issue-summary.md), and deliver to General Counsel before proceeding."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix identifies four contract types that are plausible for the platform, but every entry is description-only with no operational detail. 'Festival Vendor' contracts get no information about typical vendor categories (AV, security, food, talent), deal sizes, or turnaround SLAs tied to festival production schedules. 'Content Rights / User Licensing' is listed as a contract type but Story Portal's core product involves user-generated stories — this should be the most detailed section explaining the licensing model (non-exclusive, royalty-free, revocable) and the risk of overreach. There are no template names, no Ironclad workflow names, and no escalation thresholds specific to Story Portal's scale.",
      "example_rewrite": "| Contract Type | Story Portal Context | Template | Ironclad Workflow | Turnaround SLA | Escalation Threshold | **Festival Vendor — Production** | Covers AV, staging, security, and catering vendors for Story Portal live events. Hard event date = hard deadline. | vendor-production-sow-v2.docx | Vendor-Production-Fast-Track | 48 hours from approved Deal ID | Any indemnification ask or IP claim → General Counsel same day | **User Content License** | Governs Story Portal's right to display, distribute, and archive user-submitted stories. Default: non-exclusive, revocable, royalty-free, worldwide. | user-content-license-v3.docx | User-License-Standard | Embedded in Terms of Service; no per-user negotiation | Any request to modify user license terms from a partner → General Counsel approval required |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section — this is the only structural section missing entirely, it creates behavioral ambiguity for both human practitioners and AI agents operating in Hybrid mode, and it cannot be inferred from any other section in the file. Draft 3-5 role-specific failure modes with Story Portal context (e.g., AI accepting liability redlines without STOP, drafting without a confirmed Deal ID, treating Sales-proposed business terms as Finance-approved)."
}
```