```json
{
  "role": "compliance-officer",
  "department": "legal-compliance",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are generic compliance platitudes that could appear in any compliance textbook. 'Compliance Enables Trust' and 'Continuous Improvement' carry no operational meaning specific to Story Portal or this AI-assisted hybrid role. None of the principles address the tension between AI-assisted monitoring and human judgment, the specific regulatory landscape (GDPR/CCPA for audio consent), or the unique risks of a storytelling platform collecting user-generated audio content.",
      "example_rewrite": "| **Consent Is Non-Negotiable** | Audio story collection triggers recording consent laws in 12+ US states and GDPR Article 6 — every collection touchpoint must have documented lawful basis before launch, not after. | | **Regulatory Ambiguity Gets Escalated, Not Assumed** | When a regulation could be interpreted two ways, flag it to General Counsel with a written options memo — never silently adopt the convenient interpretation. | | **Festival Context Changes Everything** | Physical event compliance (venue permits, public recording, minor consent) differs from platform compliance — maintain separate control sets for each environment. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but describe artifacts only at the category level — 'Regulatory research,' 'Compliance reports,' 'Audit documentation' are folder names, not deliverable specifications. The template standard requires specifying what artifact is passed, not just a label. There is also no handoff to or from the Privacy Officer despite being listed as a key collaborator, and no handoff specifying format, trigger condition, or acceptance criteria.",
      "example_rewrite": "| Delivers To | Artifact | Format | Trigger | \n|---|---|---|---| \n| General Counsel | Compliance Status Report | Written memo: open findings, severity ratings (Critical/High/Medium/Low), remediation owners, target dates | Monthly + immediately on Critical finding | \n| Privacy Officer | Data Processing Activity Log delta | Spreadsheet listing new or changed data flows identified during audit, with regulation mapped to each | After each audit cycle closes | \n| All Departments | Compliance Requirement Notice | One-page memo: regulation name, what must change, deadline, point of contact | Within 5 business days of regulatory change assessment completion |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file at all — it is entirely absent. The DO/DON'T boundary list exists but describes jurisdictional boundaries (don't do the CFO's job), not behavioral failure modes specific to a Hybrid AI compliance role. The template standard requires 3-5 role-specific anti-patterns. A compliance officer AI agent has distinctive failure modes — false confidence on regulatory interpretation, over-relying on pattern matching for novel regulations, hallucinating regulatory citations — none of which are captured.",
      "example_rewrite": "## Anti-Patterns\n\n| Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **Citing regulations without verification** | AI may confabulate specific clause numbers or misstate effective dates for GDPR/CCPA rules — a wrong citation in a compliance memo creates legal exposure | Always flag regulatory citations with [VERIFY] tag; human must confirm primary source before memo is finalized |\n| **Treating audit findings as closed when remediation is claimed** | Accepting a team's self-report that a gap is fixed without evidence review is how audit cycles produce false comfort | Mark findings Closed only after reviewing documented evidence artifact, not after receiving a verbal or email confirmation |\n| **Applying platform compliance rules to festival events** | GDPR consent flows designed for web UX do not map to in-person audio recording at a public festival — conflating them produces gaps in both contexts | Maintain and apply separate control checklists: one for digital platform, one for physical event operations |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol and Hybrid division of labor exist but are vague enough to be unactionable. The protocol says 'Work on compliance activities' with no specificity about what triggers action, what the AI produces before stopping, or what format the status report takes. The Context Requirements section contains literal placeholder text '[Context item 1]' and '[Context item 2]' and the Required Skills table is empty — meaning an AI agent loading this role has no idea what context files to load or what skills to activate. This is a deployment-blocking defect.",
      "example_rewrite": "### Required Context\n- [ ] story-portal-charter.md (org structure, active roles)\n- [ ] regulatory-register.md (active regulations tracked: GDPR, CCPA, COPPA, state recording consent laws)\n- [ ] current-audit-plan.md (scope, schedule, open findings)\n- [ ] compliance-policy-library.md (approved policies in force)\n\n### Required Skills\n| Skill | When to Load |\n|---|---|\n| gdpr-ccpa-analysis.md | When assessing privacy regulation impact on new features or data flows |\n| audit-testing-methodology.md | When executing or planning a compliance audit cycle |\n| regulatory-change-assessment.md | When a new regulation or amendment is identified for impact review |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies the right compliance domains (privacy, audio consent, festival regulations, content moderation) but provides no actionable specificity. Priority 1 says 'Privacy compliance (GDPR/CCPA)' but does not explain what Story Portal actually does that triggers these regulations, what the current compliance status is, or what the AI should actually monitor or check. 'Festival regulatory compliance' appears with zero detail about what that means operationally — which jurisdictions, what permit types, what the audit trigger is.",
      "example_rewrite": "### Story Portal Compliance Areas\n\n| Area | Regulation | Story Portal Trigger | AI Monitoring Task |\n|---|---|---|---|\n| Audio consent — digital | GDPR Art. 6, CCPA, state wiretapping laws | Any feature collecting voice/audio from users | Flag new feature specs that include audio input for consent review before build |\n| Audio consent — physical | State two-party consent laws (CA, FL, IL, etc.) | Festival events where stories are recorded in person | Check event location against two-party consent state list; flag for human legal sign-off |\n| Minor data collection | COPPA (US), GDPR Art. 8 (EU) | Platform allows user accounts; festivals may include minors | Audit age-verification controls quarterly; escalate any under-13 data flow to Privacy Officer immediately |\n| Content licensing | Platform terms, creator IP rights | User-submitted stories published or monetized | Review content submission flow for rights grant language at each product update |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section immediately — this is the only dimension with a score of 1 because the section does not exist at all. A Hybrid AI compliance role operating without documented anti-patterns will produce false confidence on regulatory citations, accept unverified remediation claims, and conflate platform and festival compliance contexts. Draft 3-5 patterns specific to AI-assisted compliance work (hallucinated citations, premature finding closure, context conflation) before this role is deployed in any audit or regulatory response workflow."
}
```