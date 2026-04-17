```json
{
  "role": "cap-table-manager",
  "department": "finance-investor-relations",
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
      "finding": "All six principles are generic platitudes that could apply to any record-keeping role in any industry. 'Accuracy Is Critical — Cap table errors cause real problems' is circular and says nothing about what makes cap table accuracy uniquely consequential. 'Compliance Always — Legal requirements first' is indistinguishable from a compliance role at a bank. None of the principles reflect the specific tension this role navigates: maintaining a single source of truth across conflicting stakeholder interests (founders protecting dilution, investors verifying pro-rata rights, employees tracking vesting) under securities law constraints.",
      "example_rewrite": "Replace generic principles with role-specific ones, e.g.: | **One Source of Truth** | When Carta, a term sheet, and a board consent disagree, this role resolves the conflict — never accepts three different 'authoritative' sources simultaneously | | **Dilution Is Irreversible** | Unlike financial models, issuing equity cannot be undone — every grant recorded must be approved before entry, not corrected after | | **Silence Is Not Approval** | A grant request from HR without a signed board consent is not a recordable event, regardless of urgency or seniority of requestor | | **409A Integrity Gates Grants** | No option grants are recorded without a current 409A valuation — an expired FMV creates IRS exposure that legal cannot fix retroactively |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "The handoff tables name roles but describe artifacts at the category level, not the actual document level. 'Transaction approvals' from CFO, 'Equity documents' from Legal, and 'Cap table reports' to CFO are placeholders, not specifications. A receiving agent cannot know whether 'transaction approvals' means a signed board consent, a DocuSign-completed stock purchase agreement, or an email confirmation. Critically, the collaboration section references 'Financial Controller' — this role must be verified against the Organizational Charter as it may be a hallucinated role.",
      "example_rewrite": "| Receives From | Artifact | Format | Required Fields |\n|---|---|---|---|\n| CFO | Board Consent (equity issuance) | Signed PDF via DocuSign | Authorized shares, price per share, recipient name, date authorized |\n| Legal | Stock Purchase Agreement or Option Grant Notice | Countersigned PDF | Exercise price, share class, vesting schedule, cliff date |\n| HR | Option Grant Request | Internal grant request form | Employee ID, grant size, grant date, vesting template reference |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file at all — it is completely absent. The template standard requires 3-5 role-specific anti-patterns. The DO/DON'T boundary list in the Boundaries section is not a substitute: items like 'Set equity strategy (Leadership's domain)' describe scope boundaries, not failure modes an AI agent would actually encounter. The absence of anti-patterns is the single most dangerous gap in this file for an AI-Primary agent operating on sensitive equity records.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: | Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **Recording grants on verbal approval** | Equity issued without board consent is legally defective and may require rescission | Only record grants accompanied by a signed board consent or unanimous written consent — no exceptions for urgency |\n| **Updating cap table during active negotiation** | Recording a term sheet as a closed transaction misrepresents ownership to other parties | Cap table is updated only upon closing documents signed by all parties, not at term sheet or LOI stage |\n| **Presenting a single dilution scenario** | Decision-makers anchoring to one model miss downside cases | Always present minimum 3 scenarios: base case, full dilution (all options exercised), and liquidation preference waterfall |\n| **Treating option pool refresh as non-dilutive** | Pool increases dilute existing holders even before grants are made | Model pool expansion as immediate dilution to all pre-expansion holders in all financing scenario outputs |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and correctly places a STOP point before finalization, which is appropriate for an AI-Primary role handling irreversible equity records. However, the protocol is dangerously underspecified for the risk level of this domain. There is no STOP point before the initial recording step — an AI agent could enter an unverified transaction into the cap table before human review. The workflow steps (RECEIVE → RECORD → VERIFY → REPORT) show verification happening after recording, which is backwards for equity. Additionally, the 'Agent Capabilities' section lists 'Data entry: Cap table updates' without specifying which fields the AI may populate autonomously versus which require human entry.",
      "example_rewrite": "Revise the Iteration Protocol to front-load the STOP: LOOP:\n  1. Receive transaction task with supporting documents\n  2. Parse and validate: confirm board consent present, shares authorized match request, price matches current 409A\n  3. STOP → Present validation checklist to CFO for pre-entry approval\n  4. IF approved → Record transaction in cap table\n  5. IF documents incomplete → Return to requestor with specific missing items list (do not record)\n  6. Post-entry: generate verification report showing pre/post ownership percentages\n  7. STOP → CFO signs off on verification report before report distribution\n  8. Distribute to authorized stakeholders only\n  9. Archive all source documents linked to transaction record"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix acknowledges the project context (early-stage, simple cap table) but provides no actionable specifics. '10-15% typical' for option pool is a generic startup statistic, not Story Portal's actual pool size. 'Financing rounds — Per round' for modeling frequency is a tautology. The appendix does not name Story Portal's actual current equity holders, the specific round the company is at, which cap table tool has been selected (or if spreadsheet-only), or what the next near-term equity event is (e.g., upcoming seed round, pending advisor grants). It reads as a template stub that was never filled in with project data.",
      "example_rewrite": "Replace generic rows with project-specific entries: | Domain | Story Portal Current State |\n|---|---|\n| **Cap Table Tool** | Google Sheets (migrate to Carta upon Seed close — tracked in Finance backlog) |\n| **Current Holders** | 2 co-founders (common), 1 angel (SAFE, $150K, MFN), option pool authorized not yet granted |\n| **Option Pool Size** | 10% post-incorporation, expansion to 15% modeled for Seed round |\n| **Next Equity Event** | Seed round close — dilution model required before investor pitch deck is finalized |\n| **Immediate Priority** | Build pre-money / post-money dilution model for $1.5M Seed at $8M cap before CFO investor meetings |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 4-5 cap-table-specific failure modes before deploying this role. This is an AI-Primary agent with write access to irreversible legal records — operating without documented anti-patterns means the agent has no guardrails against recording unverified transactions, updating the cap table during open negotiations, or presenting incomplete dilution analyses to decision-makers. This is the highest-risk gap in the file."
}
```