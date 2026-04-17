```json
{
  "role": "ux-designer",
  "department": "design",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 6,
    "anti_pattern_quality": 5,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "All 6 principles present, but most are UX industry clichés that could appear in any design textbook. 'Simplicity Over Cleverness,' 'Test Early Test Often,' and 'Iteration Is Progress' are generic mantras with no specificity to this role's context (Story Portal, festival environment, AI-assisted hybrid workflow). None of the principles address the unique constraints of this product — ephemeral recording, first-time festival users, consent under cognitive load, or the tension between AI suggestion and human UX judgment in a Hybrid role.",
      "example_rewrite": "Replace 'Simplicity Over Cleverness' with: | **One-Shot Clarity** | Festival users encounter Story Portal once, in a noisy environment, with no time to learn — every screen must be self-evident on first glance, with zero reliance on discoverability or learnability. | And replace 'Iteration Is Progress' with: | **AI Suggests, Human Decides** | When AI proposes flow alternatives or pattern options, treat them as raw material — always validate against real user context before adopting, never ship an AI-generated interaction without a human prototype test. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Handoff tables name roles correctly and list artifact types, which is above baseline. However, artifacts are category labels, not actual named deliverables. 'Wireframes, flows' tells the UI Designer nothing about format, fidelity, or what file to open. 'Interaction specs' delivered to Frontend Developer does not specify whether this is a Figma annotation, a written spec doc, or a Zeplin export. 'Expected behavior' to QA is dangerously vague — a QA engineer cannot test against 'expected behavior' as an artifact name.",
      "example_rewrite": "Change the Delivers To table to: | UI Designer | Figma file (link in project board): annotated lo-fi wireframes at 375px and 1440px breakpoints, with component inventory and spacing notes on each frame | and | QA | Interaction spec sheet (Notion doc): enumerated list of user actions, system responses, edge cases, and error states per screen, linked to prototype |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 5,
      "finding": "Five anti-patterns are present but all five are universal UX platitudes ('skip research,' 'design in isolation,' 'skip prototyping') that would appear identically in a UX Designer role for a banking app, an enterprise SaaS product, or a medical device. None address failure modes specific to this role: AI-generated patterns being adopted without validation, over-engineering the wheel interaction for delight at the cost of first-time clarity, designing consent flows that satisfy legal requirements but fail plain-language comprehension, or handoff gaps between UX wireframes and UI visual execution in this team's Figma workflow.",
      "example_rewrite": "Replace 'Design in isolation' with: | Accept AI pattern suggestions without prototype testing | AI alternatives are generated from pattern libraries, not from festival-context user behavior — an AI-suggested 'swipe to record' interaction may be elegant in theory but fail when a user's hands are full at an outdoor event. Always test AI-proposed interactions with a clickable prototype before including in wireframes. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol is present and correctly structured for a Hybrid role, with explicit STOP points and a HALT condition. The AI/Human division of labor in the Deployment Notes is clear. Score does not fall below 7, but a notable gap exists: the Context Requirements section contains literal placeholder text ('[Context item 1]', '[Context item 2]') and the Required Skills table is entirely empty. An AI agent loading this role would have no instruction on what context files to load before starting work, which undermines the otherwise solid deployment structure.",
      "example_rewrite": "Replace the placeholder Context Requirements block with: | Required Context | | - [ ] story-portal-product-brief.md (feature scope and constraints) | - [ ] design-system-components.md (existing component library) | - [ ] user-research-festival-findings.md (Design Research Lead synthesis) | - [ ] accessibility-standards.md (WCAG AA requirements for recording flows) | Required Skills | | | Skill | When to Load | | | wheel-interaction-patterns.md | Before designing spin/wheel screens | | | mobile-recording-ux.md | Before designing recording interface | |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is better than most — it names actual screens (Wheel, Recording, Consent, Playback) and acknowledges the festival context. However, the UX Challenges table lists approaches that are generic design responses ('Clear visual cues,' 'Progress indication,' 'Plain language') rather than specific UX decisions. The Wireframe Priorities table is the strongest section but stops at naming screens without specifying what the wireframe must answer. A designer loading this role still cannot determine what the first wireframe frame should contain or what question it is designed to test.",
      "example_rewrite": "Expand Wireframe Priorities to: | Priority | Screen | Key UX Question to Answer | | 1 | Wheel landing | Does a first-time user understand they should tap/spin without any instruction text? | | 2 | Recording interface | Can a user confidently know they are being recorded, how long remains, and how to stop — with one glance, while holding a drink? | | 3 | Consent flow | Does a user understand what they are consenting to in under 8 seconds without reading body copy? | | 4 | Playback/confirmation | Does a user feel their story was captured successfully and know what happens next? |"
    }
  ],
  "top_improvement": "Replace all five anti-patterns with role-and-product-specific failure modes: the current list ('skip research,' 'design in isolation,' etc.) is indistinguishable from a generic UX job description and provides zero behavioral guardrails for this role's actual risks — specifically, the AI-suggestion-to-shipped-interaction pipeline in a Hybrid role, and the unique failure modes of designing for a festival context where users are distracted, time-pressured, and encountering the product exactly once."
}
```