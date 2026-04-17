```json
{
  "role": "proposal-writer",
  "department": "sales",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 8,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "The six principles are solid but read as generic writing best practices rather than proposal-writer–specific philosophies.",
      "example_rewrite": "Add a principle like **ROI Alignment**: \"Every proposal must quantify expected ROI for the client, linking features directly to financial impact.\""
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "No anti-patterns are defined. The template is missing role-specific warnings about common proposal mistakes.",
      "example_rewrite": "Anti-Pattern: **Feature Dump** — Listing every product feature without tying it to client needs. Instead, focus on top three features mapped to key buyer drivers."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix lists proposal types but doesn’t tie them to concrete writing guidelines or success metrics.",
      "example_rewrite": "For **Festival Partnerships**: \"Include a 2-column table mapping festival goals (e.g., attendance growth) to platform capabilities (e.g., ticket-sale analytics), with KPI targets in each cell.\""
    }
  ],
  "top_improvement": "Introduce and document 3–5 role-specific anti-patterns so proposal writers avoid the most common, damaging mistakes."
}
```