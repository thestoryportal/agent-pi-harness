```json
{
  "role": "product-analyst",
  "department": "product",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 5,
    "anti_pattern_quality": 6,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "All 6 principles are present but read as generic data-team platitudes applicable to any analyst role — Data Engineer, Business Analyst, Data Scientist. 'Measure What Matters' and 'Actionable Insights' appear in virtually every analytics job description ever written. None of the principles reflect what is specific to a Product Analyst: the tension between short-term experiment pressure and long-term metric integrity, the risk of teaching a PM to misread a p-value, or the discipline of not shipping a dashboard until the tracking plan is validated. The 'Meaning' column also just restates the principle in different words rather than explaining a behavioral commitment.",
      "example_rewrite": "Replace 'Measure What Matters' with: | **Instrument Before You Launch** | A feature without tracking is a feature that never happened. Tracking requirements are defined and validated in the Tracking Specialist handoff *before* a feature ships — not after the PM asks why numbers look flat. | And replace 'Continuous Measurement' with: | **Protect the Denominator** | Completion Rate means nothing if Recording Started is undercounted. Every metric report begins by auditing the denominator for data quality issues before drawing any conclusions about the numerator. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "The handoff tables name roles but describe artifacts at a level of abstraction that provides no operational guidance. 'Analysis requests' (received from PM), 'Analysis, insights' (delivered to PM), and 'Data infrastructure' (received from Data Engineer) are category labels, not artifacts. An AI agent loading this role cannot determine what file format, what schema, what template, or what trigger initiates a handoff. The 'Delivers To: UX Designer → Usability data' row is particularly vague — usability data could mean a raw export, a segmentation report, or a dashboard link. There is also no indication of how handoffs are initiated (Slack message, task ticket, shared doc).",
      "example_rewrite": "| Delivers To | Artifact | Format | Trigger | \n|---|---|---|---| \n| Product Manager | Feature Analysis Report | Markdown doc + summary slide, filed in /product/analysis/ | A/B test concludes or feature question raised in sprint planning | \n| UX Designer | Usability Metrics Report | Dashboard link + annotated funnel screenshot highlighting drop-off steps above 20% | Design review requested or post-launch review scheduled | \n| Tracking Specialist | Tracking Requirements Doc | Structured event spec listing event name, properties, and acceptance criteria per the tracking-plan template | New feature enters development sprint |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 6,
      "finding": "The anti-patterns are better than average — 'Cherry-pick data' and 'Declare significance without testing' are analytically specific. However, three of the six ('Report without context', 'Delay insights', 'Over-complicate') are universal communication anti-patterns that apply equally to a copywriter or a finance analyst. None of the anti-patterns address Product Analyst-specific failure modes: calling an experiment early because a PM is impatient, treating correlation as causation in funnel drop-off analysis, defining a metric post-hoc to make a feature look successful, or building a dashboard on unvalidated tracking events. The table has 6 entries which exceeds the 3-5 checklist standard — trimming the generic ones and replacing with role-specific ones would sharpen it.",
      "example_rewrite": "Add: | **Call the experiment early** | PM pressure produces false positives | Enforce pre-registered sample size and duration; document the agreed stopping rule in the experiment design before launch, not after. | \n\nAdd: | **Analyze on unvalidated events** | Garbage in, garbage out — but it looks authoritative | Before any funnel analysis, run event volume QA against the tracking plan. If wheel_spin count and recording_start count diverge by >5% unexpectedly, pause and escalate to Tracking Specialist before presenting findings. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Autonomous Operating Protocol and Iteration Protocol give a functional operational loop, and the AI-Primary classification is correctly applied with a clear human/AI responsibility split. The role scores above 7 primarily due to these sections. Minor gaps: the CONTINUOUS OPERATION loop does not specify cadence (is 'monitor' every 5 minutes or once daily?), 'Queue ad-hoc requests' has no defined queue mechanism, and the GUARDRAILS do not specify what threshold triggers an anomaly alert — leaving the AI to make an unconstrained judgment call about what counts as 'significant'. These are solvable with one additional context field in deployment.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The Story Portal appendix is the strongest section of the document. It names real events (wheel_spin, recording_complete), defines real metrics with formulas (Completion Rate = Completed / Started), and maps a genuine MVP-state starting point. The festival dashboard section maps directly to the product's use case. Minor gap: the 'Analyst Priorities' list includes 'Implement basic tracking' as Priority 2, but the role's own boundaries state 'Implement tracking code — Tracking Specialist's domain.' This creates a contradiction an AI agent would have to resolve. Clarifying that Priority 2 means 'Define and hand off tracking requirements to Tracking Specialist' would eliminate the ambiguity.",
      "example_rewrite": "In Analyst Priorities table, change: | 2 | Implement basic tracking | to: | 2 | Define tracking requirements and hand off Tracking Spec to Tracking Specialist for implementation — covering all six core events listed in the Tracking Events table |"
    }
  ],
  "top_improvement": "Handoff specificity: The role cannot function as an autonomous agent without knowing what artifact to produce, in what format, filed where, and triggered by what event. Upgrading the handoff tables to include Format, Trigger, and Location columns — especially for the PM analysis request loop and the Tracking Specialist spec handoff — is the single change that most directly enables the AI-Primary deployment model to operate without constant human clarification."
}
```