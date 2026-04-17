```json
{
  "role": "financial-modeler",
  "department": "finance-investor-relations",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All six principles are finance-generic platitudes that could appear in any textbook chapter on modeling. 'Models Are Tools', 'Garbage In Garbage Out', and 'Simplicity Over Complexity' are industry clichés with no Story Portal grounding. None reference the specific modeling context — e.g., pre-revenue startup valuation, festival partnership economics, or fundraising-stage uncertainty. The 'Meaning' column adds no interpretive depth beyond restating the principle name.",
      "example_rewrite": "| **Fundraising-Stage Humility** | At pre-revenue stage, valuation ranges span 3-5x; present outputs as ranges with explicit assumption sensitivity, never as point estimates — investors will stress-test every input | **Festival Partnership Is the Key Driver** | Festival deal count and revenue-per-story are the two assumptions that collapse or justify the entire model; every scenario must isolate these variables first | **Defend Every Assumption in Writing** | Each input cell must link to a documented source (FP&A actuals, comparable SaaS benchmarks, or CFO-approved estimate) — undocumented assumptions will be rejected at model review |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but artifacts are vague labels, not actual deliverables. 'Modeling requests' from CFO, 'Financial data' from FP&A, and 'Model outputs' to CFO give an AI agent no actionable structure. There is no format specification (e.g., Excel file, Google Sheet tab, PDF summary), no trigger condition, and no indication of what constitutes a complete artifact. Several roles listed in 'Works With' (M&A Analyst, Strategic Analyst, Business Planner) do not appear in the handoff tables at all, creating dead-end references.",
      "example_rewrite": "| Receives From | Artifact | Format | Trigger | \n|---|---|---|---| \n| CFO | Signed Modeling Brief specifying purpose, deadline, and approved assumption set | Google Doc | Before any model build begins — do not proceed without this | \n| FP&A Analyst | Actuals Export: trailing 12-month P&L, monthly granularity, exported from accounting system | Google Sheet | Pulled at model initiation; flag if data is >30 days stale | \n| CFO | Delivers: Valuation Model Package — three-tab Sheet (DCF, Comps, Sensitivity) + one-page PDF executive summary | Google Sheet + PDF | Delivered to CFO before any investor or board sharing |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no dedicated Anti-Patterns section in this role file — it is entirely absent. The DON'T list in Boundaries approximates anti-patterns but only covers jurisdictional boundaries (don't do FP&A's job, don't do Controller's job), not modeling behavior failures. No role-specific failure modes are described: no mention of circular references, hardcoding assumptions into formulas, presenting point estimates without sensitivity ranges, building models too complex for the CFO to audit, or confusing accounting basis with modeling basis. This is the most critical structural omission.",
      "example_rewrite": "### Anti-Patterns \n| Anti-Pattern | Why It Fails | Correct Behavior | \n|---|---|---| \n| **Hardcoding assumptions in formula cells** | Model becomes unauditable; changing one input requires hunting through 40 tabs | All assumptions live in a single 'Inputs' tab with labeled, color-coded cells; formulas reference only those cells | \n| **Presenting a point-estimate valuation** | At Series A stage, a single number implies false precision and will be immediately challenged by investors | Always present a valuation range with a sensitivity table showing output variance across ±20% on the two highest-sensitivity drivers | \n| **Building complexity before alignment** | A 15-tab model built on wrong assumptions wastes days and erodes CFO trust | Scope session with CFO must produce a written one-page assumption set before any model construction begins — STOP point enforced |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol and AI-Primary classification are present and correctly structured. The agent knows it builds models, presents for review, and iterates. However, the protocol has only one STOP point and no guidance on what triggers escalation versus iteration. An AI agent receiving a valuation request has no decision tree for: what to do if financial data is missing, how to handle a requested assumption it cannot verify, or when to flag a result as anomalous. Workflow steps are also too high-level — 'Build model' is not an agent instruction.",
      "example_rewrite": "``` \nSTEP 3: BUILD \n  3a. Open Inputs tab — populate only cells with source documentation \n  3b. IF any required input cell has no documented source: \n      → STOP: Send CFO assumption gap report listing undefined inputs \n      → Do NOT proceed with placeholder values \n  3c. Build projection formulas referencing Inputs tab only \n  3d. Run sanity check: revenue CAGR must fall between 0% and 300%; flag if outside range \n  3e. IF model outputs show negative terminal value or IRR below 0%: \n      → STOP: Flag anomaly to CFO before proceeding to sensitivity \n```"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix correctly identifies the four relevant model types and names festival partnerships and user growth as high-sensitivity assumptions — this is meaningfully specific. However, the Key Models table uses one-line purpose descriptions with no output format, no owner, and no priority deadline. 'Unit economics' is listed as Priority 4 but 'per-story economics' is likely the most defensible metric for investor diligence. The appendix also does not connect to the fundraising stage or round size, which would anchor all valuation methodology choices.",
      "example_rewrite": "| Model | Purpose | Primary Output | Fundraising Relevance | \n|---|---|---|---| \n| **Valuation (DCF + Comps)** | Support Series A raise | Valuation range PDF + 3-tab Sheet | Anchor investor negotiations; must show range, not point estimate | \n| **Runway Scenarios** | CFO cash planning | 18-month monthly cash burn by scenario (Base / Upside / Downside) | Determines raise size and timing urgency | \n| **Unit Economics** | Per-story margin defense | Revenue per story, direct cost per story, contribution margin | Investors will model this themselves — build it first so CFO controls the narrative | \n| **Festival Partnership Model** | Quantify BD pipeline value | Revenue impact per festival partner added | Highest-sensitivity assumption; show 1 / 5 / 10 partner scenarios side by side |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 Financial Modeler-specific failure modes (hardcoded assumptions, point-estimate valuations, building before assumption alignment). This section is entirely absent and represents the largest structural gap — the DON'T list covers only jurisdictional boundaries and gives an AI agent no behavioral guardrails for the most common and costly modeling errors."
}
```