```json
{
  "role": "design-research-lead",
  "department": "design",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 5,
    "anti_pattern_quality": 3,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All six principles are generic UX research platitudes that could appear in any research textbook. 'Test, Don't Assume' and 'Research Is Continuous' offer no behavioral specificity — they don't describe how this role applies them in a design-validation context versus product discovery. 'Inclusion Matters' is a single sentence with zero operational meaning. None of the principles address the unique tension this role holds: being embedded in a Design department while maintaining research objectivity, or the specific challenge of separating design-validation research from product-needs research.",
      "example_rewrite": "Replace 'Inclusion Matters — Research should include diverse users' with: 'Diversity Is a Design Constraint — Recruit participants across age, device literacy, and accessibility need on every study. A design that tests well with one demographic and fails another is not a passing design. Document demographic coverage in every test plan and flag gaps before sessions begin.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff artifacts are named but not defined. 'Designs for testing' could be a Figma link, a printed PDF, a live prototype, or a wireframe — the AI agent receiving this has no way to know what format to expect or how to process it. Similarly, 'Usability findings' delivered to UX Designer has no format specified (report, Slack summary, Jira tickets?). The 'User context' artifact from Product Research Lead is entirely undefined. No handoffs specify the state or readiness criteria of the artifact.",
      "example_rewrite": "Change the UX Designer handoff row to: | UX Designer | Figma prototype link (mid-fidelity or higher) with task scenarios document (.md or .docx) specifying the 3–5 flows to be tested, acceptance criteria, and known design risks flagged by the designer |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 3,
      "finding": "There is no dedicated Anti-Patterns section in this role file at all — the DON'T list in Boundaries is the only analog, and it contains only four items that are boundary statements, not anti-patterns. Anti-patterns should describe failure modes this specific role falls into: over-recruiting for statistical significance in qualitative studies, leading participants during moderated sessions, presenting raw quotes without synthesis, conflating preference with usability, or timing research after design decisions are already locked. None of these appear. The four DON'T items ('Make design decisions,' 'Conduct market research') are obvious boundary violations, not behavioral failure modes.",
      "example_rewrite": "Add a dedicated Anti-Patterns section. Example entry: 'Insight Burial — Writing a 40-slide report where the three critical usability blockers appear on slides 28–31. Anti-pattern: Burying severity-1 findings in appendices. Correct behavior: Lead every deliverable with the top 3 actionable findings, severity-rated, with a single recommended design change per finding.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Context Requirements section contains unfilled placeholders ('[Context item 1]', '[Context item 2]') and the Required Skills table is entirely empty with only a placeholder format note. This means an AI agent loading this role has no idea what context files to load before beginning work. The Iteration Protocol exists but is generic. The Hybrid classification note describes the human/AI split at a high level but does not specify which workflow steps the AI executes autonomously versus which require human handoff — for example, in Workflow 1 Step 3 (ANALYZE), it's unclear whether the AI drafts the full severity-rated issue report or only categorizes raw notes.",
      "example_rewrite": "Replace the empty Context Requirements section with: Required Context: [ ] story-portal-product-brief.md — to understand feature scope before writing test scenarios [ ] design-system.md — to identify component names when logging usability issues [ ] participant-recruitment-criteria.md — current user segments and screening criteria. Required Skills: | usability-facilitation-guide.md | When conducting or reviewing moderated sessions | | severity-rating-rubric.md | When classifying issues in Step 3 of Workflow 1 |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix correctly identifies four relevant research areas (Wheel, Recording, Consent, Mobile) and maps them to methods. However, the research questions are surface-level and the methods lack specificity. 'Is wheel spin intuitive?' does not define what 'intuitive' means as a measurable outcome — completion rate, error rate, time-on-task? 'Do prompts inspire?' is not a usability question and 'Concept testing' is not a sufficient method description. The appendix would benefit from success metrics per question and participant profile guidance specific to Story Portal users.",
      "example_rewrite": "Rewrite the Wheel row as: | Wheel | Is the spin-to-record gesture discoverable without instruction? | Unmoderated task test — ask participant to 'start a story' with no further guidance. Success = participant initiates spin within 60 seconds without help. Failure threshold = >40% of participants tap static UI elements instead. |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4–5 role-specific behavioral failure modes. The current file has no anti-patterns — only boundary statements. This is the highest-priority gap because anti-patterns are the primary mechanism preventing an AI agent from drifting into common research failure modes (insight burial, leading questions, over-quantifying qualitative data, post-hoc research theater). Without them, the role has no self-correcting behavior constraints."
}
```