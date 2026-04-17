```json
{
  "role": "ai-ml-engineer",
  "department": "engineering",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 6,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "All 6 principles are role-specific and actionable. 'Latency Is UX', 'Bias Is a Bug', and 'Graceful Degradation' are genuinely specific to AI/ML work and not generic engineering platitudes. Minor deduction: 'Ship and Iterate' is the one principle that bleeds into generic startup culture — it could appear in any engineering role. 'Explain When Needed' is also slightly underspecified; explain to whom and under what trigger conditions is left vague.",
      "example_rewrite": "Replace 'Ship and Iterate' with: **'Production Is the Lab'** — Real user interactions reveal failure modes no test suite catches. Instrument every AI feature for output quality signals from day one; treat production telemetry as primary feedback, not an afterthought."
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The handoff tables name real roles but the artifacts are too vague to be actionable. 'Feature requirements, user stories' from Product Manager and 'AI API endpoints, response formats' to Frontend Developer could describe any engineering role. Missing: what format are endpoints delivered in (OpenAPI spec? Postman collection?), what does 'response formats' mean concretely (JSON schema? TypeScript interface?), and the QA handoff lists 'Test cases, expected behaviors' with no indication of format or tooling. The diagram showing Prompt Engineer coordination is a strength but the arrow labels are informal.",
      "example_rewrite": "| Delivers To | Artifact | Format |\n|-------------|----------|--------|\n| Frontend Developer | AI API endpoint contract | TypeScript interface file + OpenAPI 3.0 spec, including streaming event schema and error envelope |\n| Backend Developer | AI service integration spec | ADR (Architecture Decision Record) documenting model choice, retry policy, and data flow |\n| QA | AI quality test suite | Vitest test file with golden-set inputs/outputs + bias test cases per protected attribute |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Six anti-patterns are present and most are genuinely AI/ML-specific. 'Hardcode prompts' and 'Trust AI blindly' are strong and specific to this role. However, 'Skip quality testing' is generic engineering advice that applies to any feature — the AI-specific version would call out the particular failure mode (prompt regression after iteration, not just bugs). 'Ignore costs' also appears in backend and platform roles and needs an AI-specific angle to be differentiated.",
      "example_rewrite": "Replace 'Skip quality testing — Bad outputs damage trust' with: **'Test only happy paths — Prompts that work on your five test cases will hallucinate on the sixth user input. Build a golden-set eval with adversarial inputs, topic drift, and multilingual edge cases before merging any prompt change. A passing unit test means nothing if the LLM was never tested on inputs it will actually receive in production.'**"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 9,
      "finding": "This is the strongest dimension. The Iteration Protocol is explicit with numbered steps and a HALT condition. STOP points appear at every meaningful decision gate in all three workflows. The Hybrid classification is correctly applied and the rationale for CLI deployment (file system access, debugging, profiling) is stated. The agent knows what it executes autonomously versus what requires human approval. The four code patterns give an AI agent immediate implementation reference. Minor deduction: the Iteration Protocol does not specify a maximum loop count or time-box, which could lead to unbounded iteration on a stuck problem.",
      "example_rewrite": "Add to Iteration Protocol: 'MAX ITERATIONS: If the same quality or performance issue persists after 3 full loops without measurable improvement, STOP and escalate to Engineering Manager with a written summary of attempted approaches and blockers. Do not continue iterating past this point without human re-scoping.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Phase 2+ activation caveat is honest and well-placed — this role is correctly scoped as inactive for MVP. The feature opportunity table and technical integration points are specific (Whisper API, Edge Functions, embeddings). The quality bar items are concrete. Deduction: the offline-first constraint is listed but not operationalized — there is no guidance on what the AI agent should actually do differently when designing for offline (e.g., which features are blocked vs. queued vs. skipped). The 'Wheel Topic Generation' feature listed as High priority has no acceptance criteria, making it hard to know when it is done.",
      "example_rewrite": "Expand the Constraints section: **Offline Strategy by Feature** | Feature | Offline Behavior | Implementation |\n|---------|-----------------|----------------|\n| Wheel Topic Generation | Serve cached topic set (last 50 generated) | Pre-fetch and store in localStorage on connect |\n| Story Transcription | Queue recording locally; transcribe on reconnect | IndexedDB queue + background sync API |\n| Content Moderation | Block submission until online; show clear offline status | Disable submit button with 'Moderation requires connection' message |"
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. The current artifacts table reads like a category list rather than a contract — 'response formats' and 'test cases' tell a receiving agent nothing about what file to open, what schema to follow, or what done looks like. Adding format column with concrete file types (TypeScript interface, OpenAPI spec, ADR, Vitest golden-set) would make every downstream role's entry point unambiguous and eliminate the most likely source of integration confusion between this agent and Frontend Developer or QA."
}
```