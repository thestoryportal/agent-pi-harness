```json
{
  "role": "ai-operations-engineer",
  "department": "ai-automation",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are one-liners that read as generic SRE/DevOps slogans. 'Observe Everything — Can't fix what you can't see' and 'Continuous Improvement — Learn from every incident' appear verbatim in hundreds of generic ops playbooks. None are anchored to AI-specific concerns: model drift, inference latency variance, token cost curves, GPU saturation, or the difference between a code bug and a data distribution shift. The principle column and meaning column are nearly tautological — the meaning adds no new information over the principle name.",
      "example_rewrite": "Replace generic slogans with AI-ops-specific principles. Example: | **Drift Is Not a Bug** | Model degradation looks like normal traffic until it doesn't. Set statistical drift thresholds on embedding distributions and output confidence scores — not just error rates — because a model can fail silently for days while HTTP 200s pile up. | and | **GPU Waste Is a Strategy Tax** | Every idle A100 hour is budget stolen from model iteration. Autoscale inference pods on queue depth, not CPU, and schedule batch jobs against spot capacity windows. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but artifacts are dangerously vague. 'Production-ready models' from AI/ML Engineer, 'Infrastructure' from Platform Engineering, and 'Performance feedback' to AI/ML Engineer tell an AI agent nothing actionable. What file format is the model artifact? What does 'infrastructure' mean — a Terraform module, a Kubernetes namespace, a kubeconfig? What schema does performance feedback follow? The collaboration table lists 'Site Reliability Engineer' and 'Security Operations' as worked-with roles but neither appears in the Organizational Charter reference, creating hallucinated role dependencies. 'Agent Developer' is listed but has no defined artifact exchange.",
      "example_rewrite": "Receives From AI/ML Engineer: signed model artifact in ONNX or safetensors format, model card (accuracy/latency benchmarks, input schema, hardware requirements), and a passed staging evaluation report. Delivers To AI/ML Engineer: weekly drift report (JSON — feature distribution deltas, prediction confidence histograms, error rate by input segment) generated from the production monitoring pipeline."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file. The template standard explicitly requires 3-5 role-specific anti-patterns. The DO/DON'T/ESCALATE block in Boundaries partially substitutes but lists boundary violations (develop models, manage base infra), not operational failure modes. No anti-patterns means an AI agent has no guardrails against common AI ops mistakes: deploying without a rollback plan, monitoring only HTTP errors while ignoring model-level metrics, or scaling GPU nodes reactively instead of proactively. This is the single most critical structural omission.",
      "example_rewrite": "Add an Anti-Patterns section: | **Treating Model Errors Like App Errors** | HTTP 200 with a hallucinated response is not success. Always monitor output-layer metrics (confidence scores, output token length distribution, downstream task accuracy) alongside infrastructure metrics. | **Blue-Green Without Shadow Traffic** | Never promote a new model version based solely on offline benchmark scores. Run shadow traffic for minimum 1 hour capturing real production inputs before shifting any live percentage. | **Alert on Symptoms, Not Signals** | Paging on CPU >80% for an LLM pod is noise. Alert on p95 inference latency breach, token throughput drop >20%, or cost-per-request exceeding SLA threshold. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol loop is present and correct for AI-Primary classification, and the Agent Capabilities table is useful. However, STOP points in the two main workflows are implicit rather than explicit — Workflow 1 (Model Deployment) has no STOP label at any step, so an AI agent could plausibly auto-promote from staging to production without a human gate. Workflow 2 (Incident Response) has no STOP point before the RESOLVE step, meaning an AI agent could autonomously implement production fixes. The 'Human reviews deployments / Human handles complex incidents' note in Deployment Notes is not connected to specific workflow steps. The Context Requirements section lists 'Budget' from 'Finance' with no indication of how the agent accesses or uses this information operationally.",
      "example_rewrite": "In Workflow 1 Step 2→3 add: → STOP: Present staging validation report to human operator. Do not proceed to Step 3 without explicit approval. Required: sign-off from AI/ML Engineer on model metrics AND Platform Engineering on resource allocation. In Workflow 2 Step 2→3 add: → STOP (if Severity 1 or 2): Pause before implementing fix. Present diagnosis and proposed resolution to on-call human. Auto-resolve only permitted for Severity 3 incidents matching known runbook patterns."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix is the strongest section — it names actual systems (Transcription, Moderation, Prompts, Analytics), provides concrete SLA targets with real numbers, and addresses the genuinely unusual festival operating context (offline periods, burst traffic, limited connectivity). The Festival Operations table is specific and actionable. Minor gaps: 'Prompts' as a system name is ambiguous (is this the prompt generation service or the LLM serving layer?). The SLA for audio transcription (<10s for 60s audio) is specific but there is no mention of what happens operationally when SLA is breached — no escalation path or degraded-mode behavior is defined for the Story Portal context specifically.",
      "example_rewrite": "Add SLA breach response column: | Audio transcription | <10s for 60s audio | On breach: switch to smaller Whisper variant (base vs large-v3), alert AI/ML Engineer via PagerDuty, log degraded-mode flag to analytics pipeline, auto-revert when p95 returns below 8s for 5 consecutive minutes. |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 AI-ops-specific failure modes (e.g., treating HTTP 200 as model success, skipping shadow traffic before promotion, alerting on infrastructure metrics instead of model-output metrics). This section is entirely missing and is the most critical structural gap — without it, an AI agent operating this role has no guardrails against the class of silent failures unique to production AI systems."
}
```