```json
{
  "role": "automation-engineer",
  "department": "ai-automation",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 5,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "The 6 principles exist and are better than pure platitudes, but several remain surface-level for an automation engineer specifically. 'Eliminate Toil' and 'Integrate Everything' are directionally correct but lack measurable thresholds or decision rules. 'Incremental Value' has no guidance on what 'small' means or when to stop iterating. None of the principles address the tension unique to automation work: when NOT to automate (e.g., low-frequency processes, high-variability inputs).",
      "example_rewrite": "Replace 'Incremental Value — Small automations compound' with: 'Automate at the Threshold — A process qualifies for automation only when it recurs 10+ times/week OR consumes 2+ hours/week of human time. Below that threshold, document the manual process instead. Premature automation creates maintenance burden without ROI.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff tables list role names and generic artifact labels but fail the specificity test. 'Receives: Process requirements from Operations Manager' does not specify the document format, required fields, or acceptance criteria. 'Delivers: Automation triggers to Agent Developer' does not name what format those triggers take (webhook URL? event schema? config file?). 'Delivers: Working automations to Operations' is vague enough to be meaningless. No handoff specifies the condition that triggers the handoff or what a recipient does with the artifact.",
      "example_rewrite": "Delivers To Agent Developer: A completed Trigger Manifest (JSON schema defining event name, payload structure, authentication method, and retry policy) so the Agent Developer can wire the trigger into agent logic without a synchronous meeting. Handoff condition: automation is deployed to staging and has passed 48-hour smoke test."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "This is the most critical gap: the role file contains NO anti-patterns section at all. The template standard explicitly requires 3-5 role-specific anti-patterns. The DO/DON'T boundary list covers domain ownership but is not the same thing as anti-patterns, which should describe failure modes specific to how an Automation Engineer goes wrong in practice. Generic automation pitfalls like 'hardcoding credentials,' 'no idempotency,' 'automating a broken process,' and 'no circuit breaker on external APIs' are entirely absent.",
      "example_rewrite": "Add an Anti-Patterns section with entries such as: (1) Automating a Broken Process — Never automate a workflow that Operations hasn't signed off as correct; automation amplifies broken logic at machine speed. STOP and escalate to Operations Manager if the manual process has no documented happy path. (2) Silent Failure — An automation that catches all exceptions and logs nothing is worse than no automation; every catch block must emit a named alert to the monitoring dashboard. (3) Credentials in Code — API keys hardcoded in automation scripts will eventually leak; all secrets must be injected via the secrets manager at runtime, never committed."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol is present and the Agent Capabilities table gives a reasonable action vocabulary. The classification and deployment mode are unambiguous. The role loses points because the STOP points in workflows are inconsistently placed: Workflow 1 has one STOP in the Iteration Protocol but none embedded in the workflow steps themselves, while Workflow 2 has no STOP at all. An AI agent executing Workflow 2 would deploy to production without a documented human checkpoint, which violates the AI-Primary classification requirement that humans approve designs and validate outputs.",
      "example_rewrite": "In Workflow 2, add between steps 3 and 4: 'STOP → Present tested integration spec, connectivity test results, and data validation report to Operations Manager and Backend Developer. Do not proceed to Deploy until written approval received. If no response within 24 hours, escalate to Chief AI Officer.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix names four real automation opportunities and four festival-specific automations, which is project-relevant. However, the tables are inventory lists, not actionable specifications. 'Audio Processing — Automatic transcription queue' tells an AI agent what exists but not the trigger condition, the upstream system, the expected SLA, or the failure behavior. The Festival Automations table (sync queue, health check, backup, alert) duplicates concepts from the main Automation Opportunities table without clarifying whether these are the same automations or separate ones. Priority 1 (audio processing pipeline) is never linked to a specific workflow or existing system name.",
      "example_rewrite": "Replace the Audio Processing row with: 'Audio Processing Pipeline — TRIGGER: New .wav or .mp3 file lands in /festival/audio/raw S3 bucket. ACTION: Enqueue transcription job to AssemblyAI API (credentials in secrets manager as ASSEMBLYAI_KEY). SLA: Transcription complete within 15 minutes of upload. FAILURE: If API returns 5xx, retry 3x with exponential backoff; after 3rd failure, post alert to #automation-alerts Slack channel and halt. OUTPUT: Transcript JSON written to /festival/audio/transcripts with matching filename.'"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 4-5 automation-specific failure modes (automating broken processes, silent failures, missing idempotency, hardcoded credentials, no circuit breakers). This section is entirely absent, which is both a template compliance failure and a practical safety gap — an AI-Primary agent operating without documented anti-patterns has no guardrails against the most common ways automation engineers cause production incidents."
}
```