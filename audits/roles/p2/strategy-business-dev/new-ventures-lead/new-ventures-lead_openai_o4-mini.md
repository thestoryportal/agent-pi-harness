{
  "role": "new-ventures-lead",
  "department": "strategy-business-dev",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 8,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "The six listed principles are generic lean-startup platitudes and lack customization for this organization’s industry or venture stages.",
      "example_rewrite": "| Principle | Meaning |\n|-----------|---------|\n| Rapid Micro-Experiments | Run 3 targeted pilot tests in 10 days to validate each feature hypothesis |\n| Strategic Pivot Points | Define 5 data-driven criteria that trigger a pivot decision |\n| Priority Segment Focus | Concentrate on top 2 user personas for initial product tests |\n| Resource-Light MVPs | Cap prototypes to under $5K spend per sprint |\n| Evidence-Driven Metrics | Track 3 key leading indicators (engagement, conversion, retention) |\n| Charter Alignment Gates | Conduct quarterly reviews with CSO to ensure ventures map to corporate growth goals |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 8,
      "finding": "Handoffs clearly name actual roles (CSO, User Research, Engineering) and specify artifacts ('Venture priorities', 'Customer insights', 'MVP requirements')."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "The role file omits an anti-patterns section entirely, leaving no guidance on common pitfalls.",
      "example_rewrite": "### Anti-Patterns\n- Skipping customer discovery: launching features without interviews, leading to low adoption.\n- Overbuilding MVP: spending >4 weeks on prototypes before testing core hypotheses.\n- Single-bet syndrome: allocating all resources to one idea without a portfolio of experiments.\n- Ignoring strategic fit: pursuing ventures misaligned with the corporate roadmap."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "AI responsibilities ('assist with research and analysis') are too high-level; lacks tool names, data sources, or specific prompts.",
      "example_rewrite": "- AI Task: In Browser mode, query Gartner and Forrester APIs for trend reports on millennial festival spending.\n- AI Task: Generate a 2-page market summary with top 5 pain points, citing source links.\n- AI Task: Draft weekly experiment plans with test hypotheses and interview scripts in Markdown format."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The Story Portal appendix is tailored to current ventures and includes clear priorities and success metrics for festivals, corporate, education, and therapy domains."
    }
  ],
  "top_improvement": "Add a dedicated anti-patterns section with 3–5 pitfalls unique to the New Ventures Lead to guide what to avoid in each workflow."
}