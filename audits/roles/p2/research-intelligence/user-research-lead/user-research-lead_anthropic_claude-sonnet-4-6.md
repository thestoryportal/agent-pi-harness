```json
{
  "role": "user-research-lead",
  "department": "research-intelligence",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic research platitudes that could appear in any UX textbook. 'Users First: User needs drive decisions' and 'Empathy as Skill: Understanding is practiced' are meaningless without specificity. None of the principles address the unique context of Story Portal (a live festival, emotionally vulnerable storytellers, one-shot recording moments) or the strategic-level seniority of this role (synthesizing across studies, setting org-wide methodology standards). The principle column restates the header; the meaning column restates the principle.",
      "example_rewrite": "Replace with role-specific principles such as: | **One-Shot Context Sensitivity** | Festival storytelling is ephemeral — research methods must account for high-emotion, low-repeatability conditions where participants cannot be recalled; | **Synthesis Over Collection** | At this seniority, value is created by connecting patterns across 10 studies, not conducting the 11th; | **Methodology as Org Memory** | Standards you set today govern how every researcher on this team collects data for years — rigor compounds; | **Advocacy Requires Evidence** | User voice in a product meeting without a cited study is opinion; your job is to make user needs irrefutable; | **Longitudinal Beats Snapshot** | Single-session interviews miss how storytelling confidence evolves across a festival weekend — design for time; | **Participant Safety First** | Story sharing can surface trauma; ethical protocols are not optional overhead, they are the research foundation."
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but not specific artifacts with enough detail to be operationally useful. 'Delivers To: Design Team → User understanding' and 'Delivers To: All Teams → Personas, journeys' are vague. The receiving roles 'Design Team' and 'All Teams' are not role names — they are group nouns that may not correspond to named roles in the Organizational Charter. 'Receives From: Product Manager → Research questions' does not specify format (brief? ticket? meeting notes?) or trigger condition. No handoff specifies file format, repository location, or completion state.",
      "example_rewrite": "| Delivers To | Artifact | Format | Trigger |\n|---|---|---|---|\n| Design Research Lead | Foundational User Personas v[n] — validated archetypes with behavioral dimensions, not demographics | Figma-linked PDF + Notion card | Before any design validation study begins |\n| Product Manager | Research Briefing — top 3 user needs with supporting evidence citations from study IDs | 1-page memo | At each sprint planning cycle |\n| Research Director | Quarterly Synthesis Report — cross-study patterns, methodology gaps, and recommended priority shifts | Slide deck + raw data link | End of each research quarter |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There are NO anti-patterns section in this role file. The template standard explicitly requires 3-5 role-specific anti-patterns, but this section is entirely absent. The DO/DON'T boundary table is present but serves a different function — it defines domain ownership, not failure modes. Without anti-patterns, an AI agent has no behavioral guardrails against the specific ways this role commonly fails (e.g., over-recruiting for a single study instead of synthesizing existing data, treating personas as permanent truth rather than living models, conducting research after product decisions are already made).",
      "example_rewrite": "Add a dedicated Anti-Patterns section: **Anti-Pattern 1 — Research Theater:** Conducting new studies to appear active when existing repository data already answers the question. INSTEAD: Run a 30-minute synthesis check against the knowledge repository before scoping any new study. **Anti-Pattern 2 — Persona Calcification:** Treating personas created 12 months ago as current truth without versioning or validation. INSTEAD: Every persona carries a 'Valid Until' date; flag for revalidation after 2 major product changes or 6 months. **Anti-Pattern 3 — Insight Hoarding:** Completing research synthesis without a scheduled share-out, leaving reports in a repository no one reads. INSTEAD: Every study closes with a 20-minute findings read-out booked before fieldwork ends. **Anti-Pattern 4 — Post-Decision Research:** Accepting research requests framed as 'validate our decision' rather than 'inform our decision.' INSTEAD: Escalate to Research Director when a research brief arrives after a product decision is already socialized."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol loop is present and correctly structured for a Hybrid role, which is good. However, the Context Requirements section is entirely unfilled — '[Context item 1]' and '[Context item 2]' are literal placeholders, and the Required Skills table is empty with only a format note. An AI agent loading this role cannot determine what context files to load before starting work. The Tools section lists 'Survey Platforms,' 'Analysis Tools,' and 'Repository Tools' — these are categories, not tools. An agent cannot open 'Repository Tools.' The Hybrid deployment note explains the human/AI split correctly but does not specify which AI tasks are autonomous vs. require human review before proceeding.",
      "example_rewrite": "Replace the Context Requirements section: **Required Context:** [ ] story-portal-project-brief.md — festival dates, audience demographics, operational constraints; [ ] existing-research-repository-index.md — catalog of all prior studies with status and key findings; [ ] research-ethics-guidelines.md — participant consent protocols for Story Portal; [ ] organizational-charter.md — confirmed role names for handoff validation. **Required Skills (load when):** | affinity-mapping.md | When conducting synthesis across 5+ studies | | survey-statistics.md | When designing quantitative instruments with n>50 |. **Tool specificity fix:** Replace 'Repository Tools: Expert' with 'Dovetail (or Notion Research DB): Expert — tag insights by theme, user type, and study ID for cross-study query.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is the strongest section in the file — it correctly identifies the four user types, maps research questions to methods, and sets prioritized research focus areas. This is meaningfully specific to the project. However, it scores below 7 for two reasons: (1) the User Models table lists model types without connecting them to the specific user types identified (e.g., which persona maps to 'first-time storyteller at a festival vs. returning oral historian'), and (2) Research Priority 1 'First-time storyteller experience' is not linked to a named workflow, method, or responsible handoff — it reads as a list without operational consequence. The festival-specific emotional context (vulnerability of sharing personal stories in a public space) is noted implicitly in the diary studies method but never made explicit as a research design constraint.",
      "example_rewrite": "Extend the Research Priorities table to include method and output: | Priority | Focus | Primary Method | Output | Handoff To |\n|---|---|---|---|---|\n| 1 | First-time storyteller experience | Contextual inquiry at booth entry point | Barrier map + comfort spectrum | Design Research Lead before prompt UI design |\n| 2 | Recording comfort and confidence | Diary study across full festival weekend | Longitudinal confidence model | Product Manager for onboarding feature scoping |\nAlso add a Constraints row: **Ethical Constraint:** Story Portal participants may share emotionally significant memories in semi-public festival settings. All study designs must include opt-out checkpoints and debrief protocols reviewed by Research Director before fielding."
    }
  ],
  "top_improvement": "Add the missing Anti-Patterns section immediately — this is a complete omission of a required template section, not a quality issue with existing content. A User Research Lead AI agent without anti-patterns has no guardrails against the most common and costly failure modes of this role (post-decision research, persona calcification, insight hoarding), meaning it will confidently execute bad research practice with no self-correction trigger. This single fix also has the highest ratio of effort-to-risk-reduction of any improvement available in this file."
}
```