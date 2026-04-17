```json
{
  "role": "financial-controller",
  "department": "finance-investor-relations",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are generic accounting platitudes that could appear in any textbook or job description. 'Accuracy Is Non-Negotiable' with the elaboration 'Books must be right' adds zero operational guidance. None of the principles address the specific tension of being a Hybrid AI-assisted controller at an early-stage startup, the judgment calls unique to pre-revenue accounting, or how this controller navigates disagreements with department heads on expense classification. They read as filler, not philosophy.",
      "example_rewrite": "Replace 'Accuracy Is Non-Negotiable / Books must be right' with: **'Materiality Is a Judgment, Not an Excuse** — At Story Portal's scale, a $5K misclassification can distort burn rate by 10%. I apply materiality thresholds explicitly documented and CFO-approved, never silently. When in doubt, I flag rather than absorb.' Replace 'Compliance Is Required / Regulations aren't optional' with: **'Compliance Is a Moving Target at Pre-Revenue Stage** — Delaware filing deadlines, 83(b) elections, and ASC 606 adoption triggers don't wait for fundraising cycles. I maintain a rolling 90-day compliance calendar and escalate approaching deadlines 30 days in advance, not at the due date.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but describe artifacts at the category level only. 'All Departments → Transactions' does not specify format, system, or timing. 'CFO → Financial reports' does not name which report, what cadence, or what format triggers the handoff. The Board handoff lacks any specification of the package format or who prepares which section. The FP&A Analyst is listed under 'Works With' but appears nowhere in the handoff table despite being the most natural artifact-exchange partner for budget vs. actuals. External Auditors appear in Works With and Handoffs but with no artifact name — 'audit requests' and 'audit support' are not artifacts.",
      "example_rewrite": "Replace the Delivers To row for CFO with: | **CFO** | Monthly Close Package: PDF containing TB, P&L, Balance Sheet, Cash Flow, and top-5 variance explanations — delivered by the 10th business day of the following month via Google Drive /Finance/Monthly-Close/YYYY-MM/ |. Replace the FP&A Analyst gap with a new Delivers To row: | **FP&A Analyst** | Actuals Export: CSV from QuickBooks by account and department, locked and timestamped, delivered by close day 8 to enable budget-vs-actuals load into the forecasting model |."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no Anti-Patterns section in this role file at all — it is entirely absent. The DON'T list in Boundaries partially substitutes but lists domain boundary violations (don't set strategy, don't make treasury decisions) rather than behavioral failure modes specific to how a controller actually goes wrong. There is no warning about common AI-assisted accounting errors such as auto-reconciling mismatches by rounding, over-relying on AI-drafted variance explanations without verifying underlying data, or closing the books without human sign-off on material adjusting entries. This is the most significant structural gap against the template standard.",
      "example_rewrite": "Add a dedicated Anti-Patterns section with role-specific items: **Anti-Pattern 1 — Silent Rounding:** AI reconciliation assistance may resolve small differences by rounding rather than identifying root cause. Every reconciling item, regardless of size, must be documented with a named explanation — never absorbed silently. **Anti-Pattern 2 — Draft-as-Final:** AI-drafted board financial statements feel polished but may contain hallucinated prior-period comparatives. Human Controller must verify every comparative figure against the prior locked close package before distribution. **Anti-Pattern 3 — Compliance Calendar Drift:** Treating state filing deadlines as lower priority than investor reporting. At early-stage, a missed franchise tax filing can trigger dissolution risk. Calendar alerts must be set 60 days and 30 days in advance."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and is structurally correct, but it is too abstract for an AI agent to operationalize. 'Perform accounting work' is not an instruction — an AI agent loading this role cannot determine what task to start with, what inputs are required before starting, or what constitutes a valid STOP condition versus a blocking error. The Context Requirements section is literally unfilled placeholders: '[Context item 1]' and '[Context item 2]' and '[Use placeholder format: skill-name.md]' — these were never completed. Browser Deployment lists capabilities but not which accounting system is actually in use at Story Portal. An AI agent loading this role would have to guess at every entry point.",
      "example_rewrite": "Replace the Iteration Protocol with a task-specific version: 'LOOP (Monthly Close Assist): 1. LOAD context: prior month TB from /Finance/Monthly-Close/YYYY-MM/TB-locked.csv and current month transaction export from QuickBooks. 2. FLAG any transaction over $10K with no memo field — list to human before proceeding. STOP → Human resolves flags. 3. Prepare draft reconciliations for Cash, AR, AP, and Accrued Liabilities using reconciliation-template.xlsx. 4. STOP → Human reviews each reconciliation; signs off or returns with correction. 5. Draft variance explanations for any line item >10% or >$5K vs. prior month. 6. STOP → Human approves language before inclusion in Close Package. 7. IF human says HALT → save draft state, log stopping point, do not distribute.' Fill Context Requirements with: '- [ ] Current month QuickBooks transaction export (CSV) - [ ] Prior month locked trial balance - [ ] Open items log from prior close - [ ] CFO-approved chart of accounts mapping'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies the right categories (early-stage, single entity, pre-revenue) but provides no actionable specifics. 'Development costs — Capitalize or expense' is a question, not a decision — a controller needs the actual policy. 'Investor reporting — Quarterly' does not name the format, recipient list, or what the report contains. The Key Accounts table presents accounting questions rather than Story Portal's actual decisions. There is no mention of Story Portal's specific funding stage, cap table complexity, or whether revenue recognition has been triggered. The appendix reads as a template that was never filled in for this specific company.",
      "example_rewrite": "Replace the Development Costs row with the actual policy: '| Development costs | Internal engineering labor expensed monthly; third-party software development costs capitalized when technological feasibility established per ASC 350-40; threshold $25K per project |'. Replace the Investor Reporting row with: '| Investor reporting | Quarterly package delivered to seed investors by the 15th of the month following quarter-end; includes: unaudited P&L, Balance Sheet, Cash Flow, runway calculation at current burn, and 3-sentence narrative from CFO; format: PDF via Carta data room |'. Add a Burn Rate Tracking row: '| Burn rate | Calculated monthly as total cash out minus recoverable deposits; presented as gross burn and net burn; flagged to CFO when runway drops below 12 months at current rate |'."
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section — this is a required template element that is entirely missing. The role currently has no behavioral failure modes documented, which means an AI agent has no guardrails against the most dangerous controller errors: silent reconciliation absorption, draft-as-final distribution, and compliance calendar drift. This is the highest-risk gap because the Hybrid classification means AI is actively performing accounting work, and without explicit anti-patterns, there is no mechanism to catch AI-specific failure modes before they corrupt the books."
}
```