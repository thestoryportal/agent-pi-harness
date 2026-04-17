```json
{
  "role": "product-research-lead",
  "department": "product",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 6,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "All 6 principles are genuinely role-specific and avoid generic quality platitudes. 'Users Know What They Do, Not What They Need' and 'Triangulate Everything' are sharp and behaviorally meaningful. Minor deduction because 'Share Widely' and 'Continuous Discovery' drift slightly toward common UX wisdom rather than a distinctive philosophical stance — they describe practice more than belief.",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Several handoff entries name roles correctly but describe artifact categories that are too vague to be operationally useful. 'Insights, recommendations' delivered to Product Manager and 'Research questions, priorities' received from Product Manager could describe any research role anywhere. Missing: what format are these artifacts in, at what workflow stage, and what specifically triggers the handoff. The Research Director handoff ('Methodology guidance') is especially thin — it reads like a general relationship description rather than a discrete artifact exchange.",
      "example_rewrite": "| Product Manager | Delivers: 'Discovery Insight Report' (structured PDF with problem statements, opportunity areas, and top 3 prioritized recommendations) — triggered after Workflow 1 Step 3 STOP point | Receives: 'Research Brief' (one-page doc with research questions, target user segments, and sprint timeline) — provided at Workflow 1 Step 1 STOP point |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "The six anti-patterns are well-targeted for a research role and avoid generic entries like 'communicate clearly.' 'Ask leading questions,' 'only do usability testing,' and 'hide negative findings' are all specific failure modes a researcher would actually encounter. Minor deduction: 'Research in isolation' and 'Research once and stop' are somewhat universal research-team concerns rather than patterns unique to an embedded Product Research Lead specifically — they don't speak to the PM-boundary tension or the festival-context challenges that make this role distinctive.",
      "example_rewrite": null
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "The Hybrid classification is well-explained with a concrete human/AI split: AI plans and drafts, human facilitates and interprets. The Iteration Protocol loop is explicit and includes a HALT condition. Browser deployment rationale is clear. The role definition gives an AI agent enough context to begin planning a research sprint immediately. Minor deduction: skill files are flagged as 'planned development' with no fallback instruction — an AI agent loading this role today has no skill files to actually load, and the template doesn't tell it what to do in that absence.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 9,
      "finding": "This is the strongest appendix section in the file. The current-state gap table is honest and specific ('Usability Testing: Not yet,' 'User Personas: Festival attendee assumed'), the five research priorities are ranked and scoped, and the festival-context challenges table directly addresses real constraints like 'Hard to simulate' with a concrete approach. The key research questions map cleanly to methods. Only minor gap: consent understanding as a research priority is listed but the research challenge column for that row is missing — it appears only in the Story Portal-Specific Considerations table, leaving the research questions table without a paired challenge/approach entry for consent.",
      "example_rewrite": null
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. Currently, artifacts like 'insights, recommendations' and 'methodology guidance' are category labels, not actionable handoff definitions. Every handoff entry should specify: (1) the named artifact and its format, (2) the workflow step that triggers it, and (3) what the receiving role is expected to do with it. Without this, an AI agent knows who to talk to but not what to produce or when — defeating the operational purpose of the handoff table."
}
```