```json
{
  "role": "fpa-analyst",
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
      "finding": "All 6 principles are one-line platitudes with no FP&A-specific guidance. 'Forecasts Guide Decisions' means nothing actionable. 'Continuous Improvement' is a generic business cliché that could appear in any role file. None explain HOW this analyst should behave differently than a human FP&A analyst or what trade-offs to make under pressure.",
      "example_rewrite": "| **Timeliness Over Precision** | When a department head needs forecast guidance before month-end close, deliver a clearly-labeled directional estimate with stated confidence range (±15%) rather than waiting 3 days for perfect actuals. Label all pre-close outputs as PRELIMINARY. | | **Variances Tell Stories** | A 12% favorable labor variance in Engineering during a sprint cycle is not a win — it signals under-hiring or deferred headcount. Always pair variance magnitude with a causal hypothesis and a forward implication before presenting to CFO. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs name roles but describe artifacts in vague category terms: 'Planning guidance', 'Actual financials', 'Forecasts and analysis'. There is no file format, no named template, no defined cadence, and no specification of what state the artifact must be in when passed. 'Financial Modeler' appears as a collaborator but does not exist as a verified charter role — potential hallucination. The receives/delivers tables are symmetric mirrors of each other with no added specificity.",
      "example_rewrite": "| Receives From | Artifact | Format | Cadence | Acceptance Criteria | | Financial Controller | Actuals export from ERP (P&L + Balance Sheet) | Excel .xlsx, trial balance format | By business day 3 of each month | All accounts mapped to FP&A chart of accounts; no unreconciled suspense items | | CFO | Annual planning guidance memo | PDF, signed | October 1 annually | Includes revenue growth target, headcount ceiling, and capex envelope |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "The role file contains NO anti-patterns section whatsoever. The template standard explicitly requires 3-5 role-specific anti-patterns. The Boundaries section lists what not to own (approve budgets, set strategy) but these are ownership boundaries, not behavioral failure modes. There is zero guidance on how this AI agent fails in ways specific to FP&A work.",
      "example_rewrite": "### Anti-Patterns — FP&A Analyst | Anti-Pattern | What It Looks Like | Why It Fails | | **False Precision Forecasting** | Presenting revenue forecast as '$4,847,392' when driver confidence is ±20% | Implies certainty that doesn't exist; erodes trust when actuals diverge; CFO makes decisions on false precision | | **Variance Without Cause** | Reporting 'Marketing overspent by $42K' without investigating whether it was timing, scope change, or run-rate issue | Useless to decision-makers; forces CFO to do analyst work | | **Assumption Burial** | Building a 3-year model where headcount growth assumption is hardcoded in cell D47 with no documentation | Model becomes a black box; next cycle rebuilds from scratch | | **Sandbagging Detector Failure** | Accepting department budget inputs at face value without benchmarking against historical actuals or industry comps | Budget becomes a wish list; variances are structurally guaranteed |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and is the strongest section, but it is a generic 8-step loop applicable to any analyst role. STOP points do not specify what human must review (CFO? Department Head?), what approval looks like, or what happens on rejection beyond 'iterate'. The Agent Capabilities table lists capabilities but not how to invoke them or what triggers autonomous action vs. requiring human input. An AI agent loading this role cannot determine: what to do on day 1, what data access it has, or when to escalate vs. proceed.",
      "example_rewrite": "### Iteration Protocol — Monthly Forecast Cycle LOOP: 1. TRIGGER: Controller delivers actuals file by BD3 → validate against prior month close (check: total assets balance, revenue recognition complete) 2. AUTO-PROCEED: Update rolling forecast model with actuals; recalculate burn rate and runway 3. STOP → HUMAN CHECKPOINT (CFO): Present variance summary >5% on any major line item. Required input: 'Approve forecast assumptions' or 'Revise [specific assumption]'. SLA: 24 hours. 4. IF approved → Generate department budget tracking reports and distribute 5. IF revision requested → Update flagged assumption, re-run model, return to STOP 6. AUTO-DELIVER: Forecast pack to CFO and Department Heads by BD6"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix identifies the right domains (runway, burn rate, festival schedule, unit economics) and is more specific than a blank template. However, it lacks actual numbers, thresholds, or decision rules that would make it actionable. 'Runway forecasting' as Priority 1 is stated but no runway threshold is defined (e.g., 'flag if projected runway falls below 12 months'). Festival schedule is mentioned as a revenue timing driver but no festival cadence or revenue model structure is provided.",
      "example_rewrite": "### Story Portal FP&A Thresholds | Metric | Green | Yellow — Flag to CFO | Red — Immediate Escalation | | Runway | >18 months at current burn | 12-18 months | <12 months | | Monthly Burn Rate Change | <5% MoM | 5-15% MoM unexplained | >15% MoM or budget deviation >$50K | | Unit Economics (Cost per Story Published) | <$X target TBD | 10-20% above target | >20% above target | ### Festival Revenue Model Structure Revenue recognized in two tranches: (1) sponsorship commitments 90 days pre-festival, (2) ticket/attendance revenue 30 days pre-festival. Forecast must carry scenario where festival delays 60 days and model cash gap impact on runway."
    }
  ],
  "top_improvement": "Add a role-specific anti-patterns section immediately — this is a complete omission, not a quality issue. The template standard requires 3-5 behavioral failure modes unique to this role. An FP&A AI agent with no anti-patterns will present false precision, accept sandbagged budgets, and report variances without causes — all high-stakes failures in a financial planning context. Draft 4 anti-patterns (False Precision Forecasting, Variance Without Cause, Assumption Burial, Sandbagging Detector Failure) before any other revision."
}
```