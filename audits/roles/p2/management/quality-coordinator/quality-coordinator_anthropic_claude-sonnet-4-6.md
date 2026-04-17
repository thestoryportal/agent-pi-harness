```json
{
  "role": "quality-coordinator",
  "department": "management",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 5,
    "anti_pattern_quality": 4,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "All six principles are industry-standard QA platitudes that could appear verbatim in any testing textbook. 'Quality is Everyone's Job', 'Shift Left', and 'Automate the Repeatable' are so generic they provide zero behavioral differentiation for an AI agent playing this specific role in a Story Portal context. None of the principles reference the actual product domain (animations, offline-first, recording flows) or the AI-native org structure this role operates within.",
      "example_rewrite": "Replace 'Shift Left' with: **Defect Cost Curves Are Exponential** — A broken recording flow caught in Sprint QA costs one engineer-hour to fix. The same defect caught post-release costs sprint capacity, a hotfix deployment, and user trust. Triage every defect against its release proximity, not just its severity. A P2 found in week 1 of a sprint is more urgent than a P1 found the day before release if the P1 has a known workaround."
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Three critical failures: (1) The 'Receives From' table lists 'Product' and 'Engineering' — neither is a named role in the Works With table or presumably the Organizational Charter. The charter roles listed are 'Technical Coordinator', 'QA Specialists', 'Product Manager', 'Release Manager'. 'Product' and 'Engineering' are departments, not roles. (2) Artifacts are vague — 'Requirements, acceptance criteria' does not specify format, location, or completeness criteria. (3) The QA Specialists handoff only goes one direction — QA Specialists send test results in, but the role never specifies what it sends back to QA Specialists (assignments, test plans, environment configs).",
      "example_rewrite": "| Receives From | Artifact | Format | Completeness Gate |\n|---|---|---|---|\n| **Product Manager** | Acceptance criteria per user story | Gherkin scenarios in Jira ticket | All stories must have ≥1 passing scenario before sprint QA begins |\n| **Technical Coordinator** | Test build manifest | Tagged Docker image + changelog | Must include migration scripts and seed data for test environments |\n| **QA Specialists** | Test execution report | Playwright HTML report + Vitest coverage JSON | Required within 2 hours of test suite completion |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 4,
      "finding": "All four anti-patterns are generic QA management advice found in any Agile certification course. None reference Story Portal, the AI-native org structure, or the specific failure modes of a Hybrid AI role. 'Blame engineers for defects' is a culture tip, not a QA coordination anti-pattern. Missing entirely: anti-patterns specific to AI-agent coordination (e.g., accepting an AI-generated test plan without verifying coverage claims), or patterns specific to this product (e.g., approving release readiness without physically verifying 60fps on target hardware, not just CI metrics).",
      "example_rewrite": "| Don't | Why | Instead |\n|---|---|---|\n| Accept AI-generated coverage reports as ground truth | Vitest coverage numbers reflect code exercised, not behavior validated — an agent can claim 85% coverage while the recording flow has zero meaningful assertions | Cross-reference coverage percentage with a critical-path trace: manually verify that wheel-spin, record-start, and playback-complete are each represented by a named test with a behavioral assertion, not just a line hit |\n| Approve release readiness from CI metrics alone | 60fps on a MacBook Pro CI runner does not equal 60fps on a mid-range Android device | Release gate requires Playwright performance trace results from at least one physical low-spec device in the test matrix, documented in the readiness report |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol and Classification section are well-structured and give an AI agent a clear operational loop. STOP points exist in all three workflows. The skill-loading table is actionable. Score is held to 7 because the trigger conditions for workflows are underspecified — 'Sprint planning begins' does not tell an AI agent what event or artifact signals this (a Jira board state change? a message from Project Orchestrator? a calendar event?), creating ambiguity at the moment of autonomous activation.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The appendix names the right tools (Vitest, Playwright) and the right critical paths (wheel spin, recording, playback) but stays at a list level rather than providing actionable quality intelligence. The '60fps maintained on target devices' quality bar is mentioned but 'target devices' is never defined. WCAG 2.1 AA compliance is listed but no specific components or interaction patterns are called out as high-risk for accessibility. An AI agent loading this context cannot derive a more specific test strategy than it could from generic QA knowledge.",
      "example_rewrite": "### High-Risk Areas Requiring Explicit Test Coverage\n| Feature | Risk | Required Test Type | Acceptance Signal |\n|---|---|---|---|\n| Wheel spin animation | Frame drops on low-end Android degrade UX below acceptable threshold | Playwright performance trace + requestAnimationFrame timing assertions | P95 frame time ≤16.7ms across 10 spin cycles on Pixel 4a profile |\n| Recording start/stop | Race condition between audio capture init and UI state update causes silent recordings | Integration test with mock MediaRecorder + state machine assertions | Zero cases where recording indicator shows active but MediaRecorder.state !== 'recording' |\n| Offline playback | Service worker cache miss on first load after update causes blank story | Playwright offline mode test with cache invalidation sequence | Playback completes without network requests after SW registration |"
    }
  ],
  "top_improvement": "Fix handoff specificity: replace department-level references ('Product', 'Engineering') with the actual named charter roles ('Product Manager', 'Technical Coordinator'), and add format and completeness-gate columns to every handoff row. Without this, an AI agent cannot determine who to request artifacts from, what a complete artifact looks like, or when it is authorized to proceed — making every workflow's first step ambiguous."
}
```