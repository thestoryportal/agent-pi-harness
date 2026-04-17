```json
{
  "role": "grant-writer",
  "department": "finance-investor-relations",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 5,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All six principles are one-line labels with two-to-four-word explanations that could apply to any grant writer anywhere. 'Story Over Stats' and 'Persistence Pays' are industry clichés. None of the principles are calibrated to Story Portal's specific context — an AI-native storytelling platform seeking non-dilutive arts/tech/community funding. There is no principle about AI-assisted writing transparency with funders, no principle about the tension between automated research and relationship-driven grant ecosystems, and no principle about protecting Story Portal's mission narrative from being diluted to fit every funder's language.",
      "example_rewrite": "| **AI-Transparent Authorship** | Disclose AI involvement per funder guidelines — some foundations explicitly prohibit AI-drafted proposals; always verify policy before submission. | | **Mission Integrity Over Fit-Stretching** | Never reframe Story Portal as a pure tech company for an NSF grant or a pure arts org for NEA if it distorts the actual mission — funders who discover misalignment rescind awards and blacklist. | | **Relationship Asymmetry** | AI can research, draft, and track; only humans can steward funder relationships — identify which funders require personal contact and route immediately to CFO or CEO rather than templating outreach. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff tables name roles but describe artifacts in vague functional terms: 'Funding priorities,' 'Financial information,' 'Program data,' 'Grant pipeline.' There is no specification of document format, required fields, or acceptance criteria. The CFO hand-in 'Funding priorities' could be a Slack message or a formal priorities matrix — the agent cannot distinguish. 'Award details' delivered to Program Leads has no template reference. The handoff to Funders ('Applications and reports') is technically an external party, which bypasses internal review checkpoints entirely as written.",
      "example_rewrite": "| Receives From | Artifact | Format | Required Fields | \n|---|---|---|---| \n| CFO | Funding Priorities Brief | Google Doc, shared drive /Finance/Grants/Priorities/ | Target domains, min/max grant size, geographic restrictions, fiscal year deadline windows, blacklisted funders | \n| Program Leads | Program Fact Sheet | Standardized template v1.2 | Outcomes to date, participant counts, budget actuals, narrative quotes, photos/assets approved for external use | \n| Controller | Grant Budget Template | Excel — Chart of Accounts aligned | Personnel costs by FTE %, indirect rate applied, matching funds documented |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no Anti-Patterns section in this role file at all. The Boundaries section contains a DO/DON'T list, but these are jurisdictional rules, not anti-patterns. Anti-patterns describe failure modes the AI agent is specifically prone to — behaviors that look correct but produce bad outcomes. This is a critical omission for an AI-Primary role writing legal and financial documents on behalf of an organization. The template standard explicitly flags this as a common mistake: 'copy-paste boundaries — each role has unique DO/DON'T items.' The DON'T list here (don't set priorities, don't approve budgets) is entirely about human role boundaries, not AI failure modes in grant writing.",
      "example_rewrite": "### Anti-Patterns \n| Anti-Pattern | Why It Fails | Correct Behavior | \n|---|---|---| \n| **Hallucinating Funder Requirements** | AI confidently states a grant requires a 501(c)(3) or has a $50K cap — if wrong, application is disqualified | Always cite the primary source URL for every requirement stated; flag any requirement not found in official documentation | \n| **Recycling Boilerplate Narratives** | Reusing Story Portal's standard mission paragraph across multiple applications creates detectable duplication and signals low effort to program officers | Each application narrative must reference the specific funder's stated priorities using their own language from their guidelines | \n| **Submitting Without STOP** | AI completes a full application and moves to submit step without human review because the iteration protocol wasn't triggered explicitly | Never advance past WRITE step without explicit human approval — treat every application as requiring a STOP regardless of funder size | \n| **Over-Claiming AI Capabilities** | Describing Story Portal's AI features in technically inaccurate ways to impress tech-forward funders | All technical claims about Story Portal's AI must be validated by the CTO before inclusion in any application |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The iteration protocol exists and is structurally sound. Agent capabilities are listed. However, the workflows lack explicit STOP points marked as human checkpoints — the template standard flags this as a common mistake. Workflow 1 (Grant Application) has no STOP between WRITE and REFINE, and no STOP before SUBMIT. An agent reading this workflow could interpret 'Submit on time' as autonomous action. Additionally, there is no guidance on what the agent should do when it hits a funder requirement it cannot verify — the escalation table covers strategic decisions but not research dead-ends or ambiguous requirements.",
      "example_rewrite": "3. WRITE \n   - Draft narrative \n   - Complete all required sections \n   - Compile full package \n   → OUTPUT: Draft application \n   ⛔ STOP — HUMAN REVIEW REQUIRED \n   Present draft to CFO with: (1) fit score against funder priorities, (2) flagged claims requiring verification, (3) any requirements that could not be confirmed from primary sources \n   → IF approved: proceed to REFINE \n   → IF rejected: return to PREPARE with documented feedback \n\n4. REFINE ... \n   ⛔ STOP — FINAL APPROVAL REQUIRED \n   CFO + relevant Program Lead sign off before any submission action is taken"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies four broad grant domains and lists real funder examples (NEA, NSF, community foundations), which is better than generic. However, it does not address the core complexity of Story Portal's positioning: an AI-native platform, which creates funder friction. NEA and many arts foundations have active policies against AI-generated content — this tension is not acknowledged. The grant fit assessment lists 'AI + storytelling' as an innovation factor but provides no guidance on how to frame this for conservative arts funders versus tech-forward funders. Funder examples are illustrative only with no actionable qualification criteria, and there is no competitive landscape awareness or known disqualifying factors.",
      "example_rewrite": "### Funder Positioning Matrix \n| Funder Type | Story Portal Frame | AI Disclosure Strategy | Known Risk | \n|---|---|---|---| \n| NEA / State Arts Councils | Community storytelling platform; AI as accessibility tool | Proactively address AI use policy; emphasize human storyteller outcomes | Many arts funders have AI-content restrictions — verify per cycle before applying | \n| NSF / Tech Foundations | Innovation in human-AI collaborative narrative | Lead with research methodology and measurable innovation | Requires documented R&D component; cannot be purely platform/product | \n| Community Foundations (local) | Festival community builder, local economic impact | Minimal AI emphasis; center community participation metrics | Geographic restrictions; Story Portal must demonstrate local presence or impact | \n| Social Impact Funders | Empathy infrastructure; measurable behavior change | AI as delivery mechanism for human connection outcomes | Must show outcome measurement framework, not just outputs |"
    }
  ],
  "top_improvement": "Add a role-specific Anti-Patterns section immediately. This is an AI-Primary agent writing legal and financial documents representing the organization to external funders — the absence of documented failure modes is the highest-risk gap in the file. Hallucinating grant requirements, recycling boilerplate across applications, and auto-submitting without human review are all plausible AI failure modes with severe real-world consequences including disqualification, blacklisting, and reputational damage. This section should be added before the role is deployed."
}
```