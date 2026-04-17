```json
{
  "role": "head-of-data-analytics",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 4,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic data platitudes that could appear in any analytics textbook. 'Data Is Strategy', 'Quality Is Foundation', 'Insight to Action' have no Story Portal specificity — they do not reference oral storytelling data, asynchronous audio events, prompt-driven engagement patterns, or the unique challenge of measuring emotional/narrative value. 'Privacy by Design' lists no concrete meaning (GDPR? COPPA? audio recordings of personal stories?). Zero principles are operationally actionable.",
      "example_rewrite": "Replace generic principles with role-specific ones. Example: **Prompt-Driven Engagement** — Story Portal's content is prompt-initiated; analytics must track prompt-to-recording conversion rates, not just raw engagement, because a high-traffic prompt with low recording rates signals a product failure, not a success. **Audio-First Measurement** — Traditional text engagement metrics (scroll depth, time-on-page) are meaningless here; completion rate of audio recordings and re-listen rates are the primary signals of story value. **Privacy as Consent Architecture** — User stories contain personal family narratives; data retention, sharing permissions, and deletion requests require explicit consent-layer tracking, not just compliance checkboxes."
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Every handoff artifact is a vague noun phrase: 'Strategic priorities', 'Analytics needs', 'Data infrastructure', 'Analytics insights', 'Analytics support', 'Data requirements'. No artifact specifies format, cadence, owner role by charter name, or what triggers the handoff. The 'Works With' table lists roles but defines the interface only as two-word labels ('Technical alignment', 'Product analytics') with no named deliverable crossing the boundary. The template standard explicitly requires 'what artifact is passed, not just works with' — this file fails that check entirely.",
      "example_rewrite": "Receives From Engineering: **Data Infrastructure Specification** — a versioned schema document (schema-registry.md) listing all tracked event types, audio metadata fields, and pipeline SLAs, delivered at the start of each sprint and on any schema change. Delivers To Chief Product Officer: **Weekly Engagement Dashboard** — a Looker report covering 7-day story recording volume, prompt conversion funnel, completion rate by prompt category, and one flagged anomaly with recommended action, delivered every Monday by 9am."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There are NO anti-patterns section in this role file. The template standard checklist explicitly requires anti-patterns that are role-specific. The Boundaries section lists DO/DON'T items, but these are ownership boundaries, not behavioral anti-patterns — they describe jurisdiction, not failure modes. There is no list of 3-5 named anti-patterns with descriptions of how this specific role typically fails. This is a complete omission of a required section.",
      "example_rewrite": "Add a dedicated Anti-Patterns section. Example: **Vanity Metric Reporting** — Reporting total stories recorded without segmenting by prompt type, user cohort, or completion status creates false confidence; always pair volume metrics with quality and retention signals. **Infrastructure Over Insight** — Spending team capacity on data pipeline perfection while stakeholders lack basic dashboards; governance must serve insight delivery, not precede it. **Analysis Paralysis on Governance** — Blocking analytics requests pending a perfect data quality score; establish a 'fit for purpose' standard per use case rather than a universal quality gate. **Insight Without Activation** — Producing a weekly dashboard that no team references in decisions; every recurring analytics output must have a named stakeholder who acts on it or it gets deprecated."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Deployment Notes section correctly identifies this as Human-Primary but the Hybrid Iteration Protocol is a 6-step generic loop with no specificity about what an AI agent actually does in this role versus what the human does. The 'Required Context' section contains literal placeholder text '[Context item 1]' and '[Context item 2]' — this is an unfilled template, not a deployable role. The Required Skills table has '[Use placeholder format: skill-name.md]' as its only content. An AI agent loading this role cannot determine what context files to load, what its specific AI-assist tasks are, or what outputs it is expected to generate independently versus hand off.",
      "example_rewrite": "Required Context section should read: **Required Context: [ ] story-portal-overview.md — product mission and user persona, [ ] data-infrastructure.md — current event schema and pipeline architecture, [ ] analytics-roadmap.md — current quarter priorities. Required Skills: analytics-sql.md (load when writing data validation queries), dashboard-design.md (load when building stakeholder reports), privacy-compliance.md (load when reviewing data collection changes). AI-Assist Tasks: generate weekly engagement summary from dashboard data, draft governance policy documents for human review, flag anomalies in daily error rate monitoring."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix names the right domains (engagement, content, experience, technical) and lists plausible metrics (completion rate, prompt popularity, latency). However, it lacks actionability: no thresholds are defined (what is a good completion rate?), no data sources are named (where do these events come from?), no analytics questions are articulated (what decisions should these metrics drive?), and the infrastructure table is too abstract to act on. The priorities list is ranked but unexplained — why is engagement priority 1 over technical monitoring for an audio platform where latency directly causes recording abandonment?",
      "example_rewrite": "Key Metrics should include decision context. Example: **Prompt Conversion Rate** (recordings started / prompt views) — baseline target >15%; if below 10% for a prompt, flag to Chief Product Officer for prompt revision or retirement. **Recording Completion Rate** (recordings submitted / recordings started) — target >70%; drops below 60% trigger a technical latency investigation with Engineering before assuming content issues. **Re-listen Rate** — currently unmeasured; establish tracking in Q1 as primary signal of story emotional value, since a story replayed by family members indicates archival success, which is Story Portal's core mission."
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section — this is a fully missing required section, not just a weak one. No other fix delivers more immediate quality improvement. Draft 4-5 named failure modes specific to a data leader at an audio storytelling product (vanity metrics, infrastructure over insight, governance blocking delivery, producing dashboards nobody uses). This single addition moves the role from structurally incomplete to structurally compliant and directly addresses the template standard checklist failure."
}
```