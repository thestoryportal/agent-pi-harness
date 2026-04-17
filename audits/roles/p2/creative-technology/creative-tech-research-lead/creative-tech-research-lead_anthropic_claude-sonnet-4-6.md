```json
{
  "role": "creative-tech-research-lead",
  "department": "creative-technology",
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
      "finding": "All 6 principles are present but read as generic research platitudes applicable to any analyst role. 'Research Enables Better Decisions' and 'Actionable Over Academic' could appear verbatim in a market research, UX research, or data analytics role. None of the principles are grounded in the specific tension this role navigates: being an embedded outsider (R&I methodology vs. Creative Tech speed), or the craft-specific challenge of researching ephemeral, visually-driven work where sources are often demos and conference talks rather than papers. There is no principle addressing how to evaluate creative quality as research evidence.",
      "example_rewrite": "Replace 'Stay Connected — The industry moves fast; stay current' with: 'Demo Over Documentation — In creative technology, a Shadertoy demo or GDC talk reveals more than a whitepaper. Prioritize primary artifacts (live experiences, source repos, recorded presentations) over secondary commentary about them.' Replace 'Breadth and Depth — Know the landscape, go deep where it matters' with: 'Embedded Perspective — You carry R&I rigor into a team that ships visual work. Translate academic precision into language the Creative Technologist can act on in a sprint, not a quarter.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "The handoff tables name roles but not artifacts with sufficient specificity. 'Delivers To: Creative Technology team → Trend reports, best practices, teardowns' does not specify format, frequency, or triggering condition. The Receives From table is weaker still: 'Research priorities, questions' from Head of Creative Tech is not an artifact — it is a conversation. No handoff specifies what a completed artifact looks like (e.g., page count, template, naming convention) or which workflow produces it. The Workflow 3 step 'Share with Creative Technologist for feasibility check' names a role but not what artifact is passed or returned.",
      "example_rewrite": "Change the Delivers To row for Creative Technologist from 'Technology evaluation, R&D support' to: 'Delivers: Best Practice Guide (Markdown doc, max 2 pages, sections: Consensus Practice / Variations / Tradeoffs / Recommended Starting Point) — triggered by Workflow 3, validated by Creative Technologist before archiving. Delivers: Competitive Teardown Document (structured template: Subject / Techniques Identified / Implementation Hypothesis / Applicable Learnings / Avoid) — triggered by Workflow 2.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 6,
      "finding": "The anti-pattern table has 6 entries and two are role-specific enough to be useful ('Hoard findings' and 'Over-research'). However, 'Research without purpose,' 'Present raw data,' and 'Single source' are universal research anti-patterns that would appear unchanged in a Product Research Lead or User Research Lead role. None of the anti-patterns address the unique failure modes of this specific embedded position: e.g., conducting research that serves R&I methodology goals rather than Creative Tech sprint needs, or mistaking aesthetic trend-chasing for strategic intelligence. The 'Ignore context' entry is too vague to be actionable.",
      "example_rewrite": "Replace 'Present raw data — Hard to use → Synthesize and recommend' with: 'Researching for R&I, Not Creative Tech — Producing thorough, methodologically sound reports on a 3-week timeline when the Creative Technologist needs a 1-page technique comparison by Thursday. Your embedded role means R&I standards must flex to Creative Tech cadence, not the reverse.' Add: 'Trend Tourism — Reporting on every notable Awwwards site or SIGGRAPH paper without filtering for Story Portal relevance. A steampunk particle system from a game engine is signal; a CSS scroll animation award is noise for this project.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Deployment Notes section correctly identifies that the AI executes research while the human guides priorities, and the Browser/Claude.ai Project rationale is sound. The Required Context checklist and Required Skills skill-loading table are well-structured. The role scores above threshold here, but one gap prevents a higher score: there is no instruction for how the AI should handle the absence of required context at session start. If 'Current technology stack' is not loaded, should the AI ask before proceeding, make assumptions explicit, or halt? The iteration protocol expected for Hybrid classification is also absent — the template standard requires it.",
      "example_rewrite": "Add a Session Start Protocol block: 'At the start of each session, confirm: (1) Is a specific research question or workflow trigger present? If not, default to Workflow 1 scan mode. (2) Is the current technology stack loaded? If not, state assumed stack [Three.js, React Spring, GSAP] and ask for correction before proceeding. (3) State which workflow you are executing and the expected deliverable before beginning.' Add Iteration Protocol: 'For recurring deliverables (Trend Report, Radar Update), human reviews draft → provides corrections → AI produces revised version → human approves for distribution. Maximum 2 revision cycles before escalating scope ambiguity to Head of Creative Tech.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The Story Portal appendix is the strongest section in the document. The four research priorities are specific questions rather than topic areas, the competitive landscape distinguishes between immersive web studios and game/film references with clear rationale, and the Technology Radar with ring placements gives an AI agent an immediate starting orientation. Minor gap: the 'Competitive/Inspirational Landscape' mixes direct competitors (Active Theory, Resn) with stylistic references (Arcane, Hades) without flagging the distinction — an AI agent should know to teardown Active Theory differently than it deconstructs Arcane's visual language.",
      "example_rewrite": "Split the Competitive/Inspirational Landscape table into two: 'Direct Competitive (analyze implementation and technique — use Workflow 2 Teardown): Active Theory, Resn, North Kingdom' and 'Aesthetic Reference (analyze visual grammar and mood, not technology stack — use Workflow 3 Best Practice): Arcane VFX style, Hades UI motion, Bioshock Infinite environmental storytelling.' This prevents the AI from attempting a technical deconstruction of an animated film."
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. The role's entire value proposition is synthesizing research into artifacts that unblock the Creative Technology team, but the handoff table currently lists artifact categories rather than artifacts. Without a defined output format for the Competitive Teardown, Best Practice Guide, and Trend Report, an AI agent will produce inconsistently structured deliverables that accumulate in a knowledge base no one uses. Define a named template with sections and a maximum length for each of the three primary deliverables, and specify which workflow produces each one."
}
```