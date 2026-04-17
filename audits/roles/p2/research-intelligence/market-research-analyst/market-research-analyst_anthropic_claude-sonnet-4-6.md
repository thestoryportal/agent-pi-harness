```json
{
  "role": "market-research-analyst",
  "department": "research-intelligence",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic research platitudes that could apply to any analyst role in any industry. 'Data-Driven: Analysis grounded in evidence' and 'Actionable Insights: Research must inform decisions' are meaningless without role-specific context. There is no principle about how a Market Research Analyst specifically handles contradictory data sources, navigates the macro-vs-micro boundary with User Research, or manages the uncertainty inherent in market sizing estimates. None of the principles reflect the Story Portal context (e.g., sizing nascent/emerging markets like festival installations where no reliable TAM data exists).",
      "example_rewrite": "Replace generic principles with role-specific ones. Example — 'Estimate With Rigor, Not False Precision: Market sizing for emerging categories like interactive installations lacks authoritative data. We build bottom-up and top-down models simultaneously, document our assumptions explicitly, and report confidence ranges rather than point estimates. A TAM of $2B–$4B with named assumptions is more useful than a false-precise $2.7B.' Another: 'Macro Stops At The Segment Door: This role tracks market-level dynamics — size, growth, segments. When findings implicate specific user behaviors or individual customer motivations, we flag and hand off to User Research Lead rather than overreaching into qualitative territory.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but artifacts are vague labels, not actual deliverable specifications. 'Research Director → Research priorities' does not describe what format priorities arrive in (a brief, a Notion page, a ranked list). 'Delivers to Product Manager → Market intelligence' is not a named artifact — it could be anything. Critically, the handoff to Competitive Intelligence Analyst is listed only in the 'Works With' table as 'Market context' with no direction, no artifact, and no trigger. The template standard explicitly requires specifying what artifact is passed.",
      "example_rewrite": "Restructure handoff tables with artifact specificity. Example — Receives From: 'Research Director delivers a Research Brief (1–2 page scoped document listing target markets, strategic questions, timeline, and priority tier) via project management system before each research cycle.' Delivers To: 'Competitive Intelligence Analyst receives a Market Landscape Summary (structured report: market size, top 3 growth trends, segment map, and flagged whitespace) as the trigger input for competitive deep-dives. Delivered as a shared document link with a Slack notification tagging the Analyst directly.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no dedicated Anti-Patterns section in this role file at all — it is entirely absent. The DON'T list in Boundaries covers domain overreach but does not constitute anti-patterns in the template sense, which should describe failure modes specific to how this role goes wrong in practice. Generic boundary violations ('don't set strategy') are not the same as behavioral anti-patterns like over-citing a single industry report, confusing correlation with causation in trend analysis, or producing a TAM number without methodology documentation. The template standard explicitly requires 3–5 role-specific anti-patterns.",
      "example_rewrite": "Add a dedicated Anti-Patterns section. Example entries: '1. Single-Source TAM Syndrome — Citing one Gartner or IBISWorld report as the market size without triangulation. Every sizing must include at least two independent methodologies (e.g., top-down from industry reports + bottom-up from unit economics). 2. Trend Labeling Without Drivers — Reporting that a trend exists without explaining the causal mechanism (e.g., reporting festival experience growth without identifying whether it is driven by millennial spending patterns, post-pandemic behavioral shifts, or brand activation budgets). 3. Precision Theater — Reporting $847M TAM when the confidence interval spans $400M–$1.2B. Anti-pattern: false precision obscures uncertainty and misleads strategy decisions.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol exists and follows the correct LOOP structure with a STOP point, which meets the minimum bar for an AI-Primary Agent role. However, the workflows contain no STOP checkpoints — both Workflow 1 and Workflow 2 run from trigger to output with zero human review gates embedded in the steps. For an AI Agent conducting autonomous market research, the absence of mid-workflow STOP points is a meaningful gap: an AI could complete a full analysis cycle on incorrect scope before a human reviews it. Additionally, 'Tools' section lists generic categories ('Data Analysis', 'Visualization') rather than actual tool names, making it impossible for an agent to know which systems to invoke.",
      "example_rewrite": "Embed STOP points in workflows. Example in Workflow 1: 'Step 1 SCOPE → OUTPUT: Analysis plan. STOP — Present scope and methodology to Research Director for approval before data gathering begins. Do not proceed to Step 2 without explicit confirmation. Rationale: Scope errors discovered after analysis waste significant compute and human review time.' Also update Tools table: replace 'Data Analysis | Expert | Quantitative analysis' with 'Python/Pandas | Expert | Quantitative data processing and TAM modeling' and 'Statista/IBISWorld | Expert | Industry report retrieval and market sizing source data.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix names four relevant markets and four research questions, which demonstrates minimal project awareness. However, it is not actionable — the 'Research Approach' column simply restates methodology names ('TAM/SAM/SOM', 'Trend analysis') without any Story Portal-specific guidance. There are no known data sources identified for these niche markets, no baseline size estimates or ranges to orient the analyst, no flagged data gaps specific to festival/interactive installation research, and no connection between the market priorities and which roles will consume the output. A researcher loading this role gets no head start on where to actually find data for interactive installation markets.",
      "example_rewrite": "Replace generic methodology labels with project-specific research guidance. Example: 'Market: Festival Installations | Size Estimate: $1.2B–$2.8B globally (low confidence — sparse authoritative data) | Best Sources: IFEA (International Festivals & Events Association) annual reports, Eventbrite industry data, PwC Entertainment & Media Outlook, press releases from Moment Factory and teamLab for revenue benchmarks | Key Data Gap: No standardized SIC/NAICS code covers interactive installations — sizing requires proxy construction from adjacent categories (experiential marketing + museum interactives + live events technology) | Primary Consumer: Chief Strategy Officer uses this for market entry decisions; output format is a 2-page brief with a single recommended SAM figure and documented assumption set.'"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3–5 role-specific failure modes. This role has zero anti-patterns documented, which is the most critical gap: the template standard explicitly requires them, they are the primary mechanism for preventing AI agent drift in an AI-Primary deployment, and the current DON'T list only covers domain boundaries — not the behavioral failure modes (single-source sizing, false precision, trend labeling without drivers) that actually degrade the quality of market research output. Without anti-patterns, an AI agent has no guardrails against its most likely mistakes."
}
```