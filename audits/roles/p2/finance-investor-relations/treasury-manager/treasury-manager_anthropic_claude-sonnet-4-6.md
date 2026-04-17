```json
{
  "role": "treasury-manager",
  "department": "finance-investor-relations",
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
      "finding": "All 6 principles are single-sentence slogans with no operational meaning. 'Cash Is Oxygen' and 'Safety First' are finance clichés that could appear in any treasury textbook. None of the principles encode a decision rule specific to Story Portal's early-stage context — for example, how to balance runway preservation against payment timing, or when to accept lower yield for same-day liquidity. 'Relationships Matter' with the explanation 'Good banking relationships help' is circular and provides zero guidance to an AI agent.",
      "example_rewrite": "| **Runway Is the Metric That Matters** | At Story Portal's current stage, every cash decision is evaluated first against its effect on runway. A 0.5% yield improvement that reduces same-day liquidity by $50K is rejected. Runway extension beats optimization. | | **Never Forecast From a Single Line** | Cash forecasts always include a base case, a 30% revenue-miss scenario, and a payroll-stress scenario. If all three scenarios show >6 months runway, proceed. If any scenario drops below 3 months, escalate to CFO immediately. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs describe categories of information, not actual artifacts. 'Receives: CFO → Policy and approvals' and 'Delivers: Controller → Transaction data' give an AI agent nothing actionable. No artifact names, no formats, no cadence, no file references, no field-level specificity. 'Cash availability' delivered to All Teams is meaninglessly vague. The handoff table also fails to specify triggering conditions — does the cash report go to the CFO daily, weekly, or on exception only?",
      "example_rewrite": "| Delivers To | Artifact | Format | Cadence | Trigger | | CFO | Daily Cash Position Report | Structured table: opening balance, inflows, outflows, closing balance, 30-day runway figure | Daily by 9:00 AM | Every business day; immediate escalation if closing balance drops below $[X] threshold | | Financial Controller | Daily Transaction Summary | CSV export from banking platform listing all debits/credits by account, reference number, counterparty | Daily by 5:00 PM | Every business day | | FP&A Analyst | 13-Week Cash Flow Actuals | Rolling actuals vs. forecast variance table, week-by-week | Weekly, Monday AM | Weekly forecast refresh cycle |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file at all. The template standard explicitly requires 3-5 role-specific anti-patterns. The DO/DON'T boundary list is present but that is a scope boundary list, not an anti-pattern section. Anti-patterns should describe failure modes specific to how a Treasury Manager AI agent would go wrong — e.g., over-optimizing yield at the cost of liquidity, treating forecast inputs as gospel without sanity-checking against bank statements, or initiating a transfer based on an emailed request without verifying through a secondary channel.",
      "example_rewrite": "## Anti-Patterns | Anti-Pattern | What It Looks Like | Why It Fails | | **Yield-Chasing at the Cost of Liquidity** | Moving operating funds into a higher-yield account with a 30-day notice period to improve interest income by 0.3% | At Story Portal's stage, same-day access to operating funds is non-negotiable. A 0.3% yield gain does not compensate for inability to cover payroll on short notice. Always prioritize liquidity tier before yield. | | **Trusting a Single Data Source for Cash Position** | Reporting cash position using only the treasury system balance without cross-referencing the live bank portal | Treasury systems have settlement lags. A $200K outbound wire may show as pending in the system but already debited at the bank. Always confirm position against live bank feed before reporting. | | **Processing Transfer Requests Without Dual Verification** | Executing a wire transfer based on a Slack message or email from a known executive | Fraud vectors frequently impersonate executives for payment redirection. Every transfer above $5K requires verification through a second channel (phone call to known number or in-person confirmation). Never rely on a single digital message regardless of sender identity. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol loop exists and the Hybrid classification is explained, but an AI agent loading this role would still not know what to actually do on Day 1. The Context Requirements section contains unfilled placeholders ('[Context item 1]', '[Context item 2]') and the Required Skills table is completely empty. The Browser Capabilities list names capabilities but not which banking platforms to access, what URLs or systems to use, or what the actual monitoring triggers are. The STOP points in workflows lack acceptance criteria — 'Position understood' is not a verifiable condition.",
      "example_rewrite": "### Required Context | Context Item | Why Required | Where to Find It | | Story Portal bank account credentials and portal URLs | Required before any cash monitoring can begin | Provided by CFO during onboarding; stored in [password manager/vault reference] | | Current CFO-approved minimum cash threshold (the 'floor') | Determines when to escalate vs. routine operations | CFO policy document v[X], Section 2 | | 13-week cash flow forecast (most recent) | Baseline for daily variance tracking | Shared by FP&A Analyst every Monday; file location: [drive path] | | Approved counterparty list for wire transfers | Required to validate any outbound transfer request | Maintained by Financial Controller; request current version before first transfer |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is the strongest section of the file and shows genuine contextual awareness — early stage, simple banking setup, runway focus, low complexity. The four-account structure (Operating, Payroll, Savings, Cards) is specific and useful. However, the section stops short of being actionable: runway visibility is listed as 'Critical' but no runway target, floor, or alert threshold is specified. 'Burn tracking' is listed as High priority but there is no burn rate figure, no tracking cadence, and no escalation trigger defined. The appendix describes the situation but does not translate it into operating parameters.",
      "example_rewrite": "### Cash Management Needs | Need | Priority | Operating Parameter | Escalation Trigger | | Runway visibility | Critical | Maintain and report rolling 13-week runway figure, updated every Monday | Escalate to CFO immediately if projected runway falls below 6 months on any scenario | | Burn tracking | High | Calculate and report weekly net burn (total outflows minus inflows) against prior-week actuals | Escalate if weekly burn exceeds budget by more than 15% for two consecutive weeks | | Payment execution | Standard | All vendor payments funded within 24 hours of AP approval | Flag if operating account balance would fall below $[floor amount] post-transfer |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 Treasury Manager-specific failure modes. This is a complete section omission — not a quality issue but a missing section — and it is the single highest-risk gap because without it an AI agent has no guardrails against the most dangerous treasury errors (fraud vector exploitation, liquidity sacrifice for yield, single-source position reporting). Draft the section using the example rewrite provided in the anti_pattern_quality finding above before addressing any other dimension."
}
```