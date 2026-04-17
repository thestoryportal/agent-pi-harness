```json
{
  "role": "service-designer",
  "department": "design",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 5,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "All 6 principles are present but several read as field jargon rather than role-specific convictions. 'Service = System' and 'Touchpoint Orchestration' describe what service design IS, not how THIS designer should think or trade off decisions. None of the principles address the specific context of Story Portal — a festival installation with physical/digital blending — which is where the philosophy should be grounded. There is no principle about ephemeral or event-bound service design, no principle about designing for strangers in public spaces, and no principle that would differentiate this designer's approach from a generic enterprise service designer.",
      "example_rewrite": "Replace 'Service = System' (too abstract) with: | **Design for the Stranger** | Every touchpoint must work for someone who has never heard of Story Portal, has 90 seconds, and is standing in a loud festival environment — design for that person first, not the informed user. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff artifacts are named at the category level ('Journey context', 'Service blueprints', 'System requirements') but not at the artifact level. 'Journey context' delivered to the UX Designer could mean a Miro board, a PDF, a Figma frame, or a verbal briefing — an AI agent has no way to know what to produce. Similarly, 'Customer insights' received from Design Research Lead is undefined in format. The template checklist explicitly flags 'Vague handoffs — Specify what artifact is passed, not just works with' and this role fails that standard. Roles like 'Engineering Manager' also need charter verification as they may not exist under that exact title.",
      "example_rewrite": "| Delivers To | Artifact | Format | Trigger |\n|-------------|----------|--------|---------|\n| UX Designer | Journey Map — Recording Flow | Miro board, exported as PDF + shared link, annotated with 5 critical moments and emotional state per stage | Before screen design begins for any new flow |\n| Operations Manager | Service Blueprint v1 | FigJam file with all 4 swimlanes complete, failure points highlighted in red, PDF export attached | After blueprint STOP point 3 (Analysis complete) |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "The 5 anti-patterns are role-appropriate and avoid pure generic advice. 'Ignore backstage' and 'Screen-level focus' are genuinely specific to service designers crossing into UX territory. However, none of the anti-patterns are specific to the Story Portal context. There is no anti-pattern about over-engineering a service blueprint for a 4-minute festival interaction, or about designing for repeat users when most Story Portal participants are one-time visitors. The anti-patterns would apply equally to a hospital or a bank, which misses the template's intent of role-specific patterns.",
      "example_rewrite": "| Blueprint for Repeat Users | Story Portal participants are mostly one-time festival visitors — designing onboarding flows for retention or return journeys wastes design resources and creates false service requirements | Design for the first-and-only interaction; treat return visits as a bonus, not the baseline scenario |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol is present and correctly structured for a Hybrid role, which satisfies the checklist requirement. However, the Context Requirements section is left as unfilled placeholders ('[Context item 1]', '[Context item 2]') and the Required Skills table is empty with only a placeholder comment. An AI agent loading this role cannot determine what context files to load before starting work. The AI/Human split in Deployment Notes is clear in principle but does not specify decision thresholds — at what point does AI-generated journey analysis get handed to the human facilitator, and in what format?",
      "example_rewrite": "### Required Context\n- [ ] story-portal-brief.md — physical installation specs, festival schedule, expected foot traffic\n- [ ] existing-customer-feedback.md — any prior festival or beta feedback\n- [ ] operations-constraints.md — power, network, staffing limitations at venue\n\n### Required Skills\n| Skill | When to Load |\n|-------|-------------|\n| service-blueprinting.md | Any blueprint workflow trigger |\n| journey-mapping.md | Any journey mapping workflow trigger |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The Story Portal appendix is the strongest section in this role file. The three-layer service ecosystem (Frontstage/Backstage/Support), the five journey stages with physical touchpoints, and the four-swimlane blueprint are all accurate and actionable for a festival installation context. The Key Service Moments table correctly identifies the spin, recording, playback, and sharing as the critical design moments. Minor gap: the Support swimlane lists 'Kiosk, power, network, staff' but does not indicate what failure modes or recovery paths exist when these fail — which is a real service design concern for a live festival environment with no IT helpdesk on-site.",
      "example_rewrite": "Add to Key Service Moments: | Network failure during recording | HIGH — silent failure destroys trust; must design visible fallback state and staff recovery protocol | Frontstage must show clear error state; backstage must queue for retry; staff script needed |"
    }
  ],
  "top_improvement": "Fill the Context Requirements section with actual Story Portal context files and rewrite all handoff artifacts to specify exact format, file type, and trigger condition — these two gaps together mean an AI agent cannot start work or finish a deliverable without guessing, which defeats the purpose of a Hybrid deployment role."
}
```