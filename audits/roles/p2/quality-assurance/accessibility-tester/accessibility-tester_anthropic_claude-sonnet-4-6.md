```json
{
  "role": "accessibility-tester",
  "department": "quality-assurance",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 6,
    "anti_pattern_quality": 8,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "All 6 principles are role-specific and actionable. 'Design for the Margins' and 'Test With Real Tools' are genuinely distinctive. Minor deduction: 'Accessibility Is Not Optional' edges toward motivational-poster territory — it states a value without describing how this role operationalizes that value differently from a general QA mindset.",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The handoff tables name roles correctly and those roles appear to exist in a QA-centric charter context. However, the artifacts are vague on both sides. 'Features ready for accessibility testing' is a state, not an artifact. 'Accessibility audit reports' is a document type but lacks format or location. There is no mention of what tool or system issues are logged in (e.g., Jira, Linear), and no artifact format (e.g., WCAG Audit Report v1.0 in Confluence) is specified. The Manual QA Specialist handoff is especially weak — 'accessibility issues observed' could mean a Slack message or a sticky note.",
      "example_rewrite": "Receives From: QA Lead → Artifact: 'Feature test ticket in Linear tagged [a11y-review], linking to Figma spec and staging URL.' Delivers To: Frontend Developer → Artifact: 'Accessibility Issue Report (Markdown) logged in Linear under [a11y] label, each issue containing: WCAG criterion, severity, steps to reproduce, exact screen reader output observed, and recommended ARIA fix with code snippet.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 8,
      "finding": "The six anti-patterns are specific, well-justified, and directly tied to accessibility testing failure modes. 'Only run automated scans' with the '50%+ of issues' quantifier is especially strong. Minor deduction: 'Document without remediation' is slightly generic — any tester role could have this. A stronger version would name the specific accessibility context where this failure is most costly.",
      "example_rewrite": null
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "The Autonomous Operating Protocol loop is clear, the guardrails are enforceable, and the Iteration Protocol includes an explicit HALT condition. The AI-Primary classification is justified with concrete examples. Deduction: the agent is told to 'test with VoiceOver and NVDA' autonomously, but an AI agent cannot actually operate screen readers — this creates a false capability claim. The role should clarify whether screen reader testing means scripted simulation, delegating to a human tester, or invoking a specific tool integration. Without this, an agent loading this role will either hallucinate screen reader results or stall.",
      "example_rewrite": "Under Autonomous Operating Protocol, add: 'NOTE: Screen reader testing (VoiceOver, NVDA) requires human operator or dedicated test environment. AI agent performs: automated axe/WAVE/Lighthouse scans, ARIA DOM inspection via browser DevTools, keyboard navigation simulation, and contrast ratio calculation. Screen reader validation steps are flagged as STOP points requiring human tester confirmation before audit report is finalized.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 9,
      "finding": "This is the strongest section in the file. The steampunk palette contrast concern, WebGL keyboard alternative requirement, prefers-reduced-motion for animations, and the specific WCAG success criteria mapped to Story Portal features are all concrete and actionable. The 'not audited' baseline table gives an agent an immediate starting checklist. Minor deduction: the WebGL/3D wheel entry says 'test keyboard controls' but does not specify what the acceptable keyboard alternative actually is — an agent needs a success condition, not just a test instruction.",
      "example_rewrite": null
    }
  ],
  "top_improvement": "Resolve the screen reader autonomy contradiction: the role classifies as AI-Primary Agent and instructs autonomous screen reader testing, but AI agents cannot operate VoiceOver or NVDA. This creates a critical execution gap — an agent will either fabricate results or deadlock. Add explicit STOP points in Workflows 1 and 2 that delegate screen reader steps to a human tester, and redefine the AI's scope to: automated tool scanning, DOM/ARIA inspection, contrast calculation, and keyboard simulation only. This single fix prevents the most likely failure mode in production deployment."
}
```