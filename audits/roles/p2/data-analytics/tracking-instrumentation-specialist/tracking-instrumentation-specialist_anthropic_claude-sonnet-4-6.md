```json
{
  "role": "tracking-instrumentation-specialist",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 5,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are single-sentence labels that could apply to any data or engineering role. 'Track What Matters' and 'Validation Always' are generic imperatives with no operational specificity. There is no principle addressing the tension between comprehensive instrumentation and performance overhead, no principle about backward compatibility when evolving schemas, and no principle about the political reality of tracking being a dependency on other teams' release cycles.",
      "example_rewrite": "Replace 'Track What Matters' with: **Instrument Decisions, Not Vanity** — Every event must map to a decision someone will make: if no one can name the question this event answers, it does not ship. Schema reviews begin by asking 'what changes if this number is 10% higher?' before writing a single property definition."
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff tables name roles but artifacts are vague nouns rather than named deliverables. 'Feature requirements' from Product Manager does not specify whether this is a PRD, a Jira ticket, a tracking request form, or a verbal conversation. 'Event data' delivered to Data Engineer is meaningless — it could be a Segment schema JSON, a live stream, or a spreadsheet. No artifact format, no file naming convention, no destination system is specified. The Analytics Engineer appears in Works With but is absent from the Handoffs table entirely.",
      "example_rewrite": "Change the Delivers To row for Data Engineer from 'Event data' to: **Artifact:** Segment schema JSON + validated event stream in dev environment | **Format:** `tracking-spec-[feature]-v[n].json` committed to `/tracking/schemas/` | **Condition:** Only after Workflow 1 Step 3 STOP point passes QA checklist"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section anywhere in this role file. The template standard explicitly requires 3-5 role-specific anti-patterns, and this section is completely absent. The DO/DON'T boundary list exists but is a boundary list, not an anti-pattern list — it describes scope, not failure modes. This is the most critical structural omission in the document.",
      "example_rewrite": "Add a dedicated Anti-Patterns section with entries such as: **Anti-Pattern: Schema Drift** — Implementing tracking directly in code without first committing a schema definition to `/tracking/schemas/`. Symptom: two features fire `button_clicked` with different property sets. Fix: schema PR must merge before implementation PR opens. | **Anti-Pattern: Spy Tracking** — Adding events to measure user behavior beyond the stated analytics requirement because 'we might want it later.' Every event requires a named requester and a linked decision. | **Anti-Pattern: Silent Failures** — Deploying tracking without alerting on event volume drop. Every production event must have a Segment monitoring rule with a 20% deviation threshold."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Context Requirements section contains unfilled placeholders ('[Context item 1]', '[Context item 2]') and an empty Skills table with only a format hint. An AI agent loading this role cannot determine what context files to load, what skill documents to attach, or what the actual starting state should be. The Iteration Protocol is present and correctly structured, but the required context gap means the agent has no way to self-configure before beginning work.",
      "example_rewrite": "Replace the empty Context Requirements section with: **Required Context:** [ ] `story-portal-tracking-spec.md` — current event schema inventory [ ] `segment-workspace-config.md` — destination IDs and write keys for dev/prod [ ] `privacy-consent-matrix.md` — which user states permit which event categories | **Required Skills:** `gtm-container-management.md` → load when configuring web tags | `segment-protocols.md` → load when designing or modifying schemas | `ios-swift-analytics.md` → load when working on mobile instrumentation"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix is the strongest section in the file — it names actual events, actual properties, and actual privacy constraints specific to the product. It earns a 7. It loses points because the key events table omits consent-related events despite listing consent as a tracked domain, the `story_abandoned` reason property has no enumerated values defined (leaving ambiguity for the AI implementer), and there is no mapping between tracking priorities and which workflows they trigger.",
      "example_rewrite": "Expand `story_abandoned` entry to: **Properties:** `reason` (enum: `navigation_away` | `session_timeout` | `explicit_cancel` | `audio_error`), `progress_pct` (integer 0–100), `prompt_id` (string), `session_id` (string) | **Note:** `reason: audio_error` must co-fire with `audio_error_occurred` event for cross-referencing in Amplitude"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 3-5 tracking-specific failure modes (schema drift, spy tracking, silent failures, property type inconsistency, consent bypass). This section is entirely absent and is the single largest gap between this file and the template standard — without it, there is no guardrail against the most common and costly instrumentation mistakes an AI agent or junior implementer will make."
}
```