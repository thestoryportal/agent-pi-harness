```json
{
  "role": "ai-ml-engineer",
  "department": "ai-automation",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 5,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic ML engineering platitudes that could appear in any textbook. 'Reproducibility — Results must be reproducible' and 'Monitoring Is Essential — Track model performance continuously' are industry clichés with no Story Portal specificity. No principle addresses edge inference for festival deployment, on-device privacy constraints, or the tradeoff between model accuracy and festival-environment latency — all of which are documented in the appendix but absent from philosophy.",
      "example_rewrite": "Replace generic principles with role-specific ones: | **Edge-First Optimization** | Story Portal deploys at festivals with constrained hardware — every model decision must account for edge inference viability before cloud fallback is considered | | **Privacy-by-Architecture** | On-device inference is preferred over cloud for audio data; model design choices must justify any data leaving the device | | **Latency Is a Feature** | A transcription model at 94% WER delivered in 4s beats a 97% WER model at 8s in a live festival context — latency targets are product requirements, not engineering preferences |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff artifacts are vague nouns rather than concrete deliverables. 'Validated approaches' from AI Research Lead, 'Data pipelines' from Data Engineer, and 'ML capabilities' to Agent Developer give an agent no actionable information about format, schema, or acceptance criteria. There is also no specification of what artifact triggers each handoff or what 'ML APIs' means concretely for the Backend Developer.",
      "example_rewrite": "| Receives From | Artifact | Format | Acceptance Gate | | AI Research Lead | Validated approach report including baseline model card, benchmark results on Story Portal eval set, and recommended architecture | Markdown report + experiment tracking URL (MLflow/W&B) | Baseline WER < 10% on internal audio test set before engineering begins | | Data Engineer | Labeled audio dataset manifest with S3 paths, sample counts, label schema, and data quality report | JSON manifest + DVC pointer | Zero null labels, >1000 samples per class, quality report signed off | | Delivers To: Backend Developer | REST API spec for /transcribe endpoint including request schema, response schema, latency SLA, and model version header | OpenAPI 3.0 YAML + Postman collection | Latency p95 < 5s validated in staging |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "This role file contains NO anti-patterns section whatsoever. The template standard explicitly requires 3-5 role-specific anti-patterns. The DO/DON'T boundary section covers jurisdictional overreach but zero ML-specific failure modes — no mention of training-serving skew, overfitting to offline metrics, deploying without monitoring baselines, gold-labeling on production data, or ignoring festival edge constraints during model selection.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: | Anti-Pattern | Why It Fails Here | Correct Approach | | **Optimizing for offline metrics only** | A model with 96% WER on benchmark audio that runs at 9s latency fails the festival use case entirely | Always benchmark latency on target edge hardware before reporting accuracy results | | **Training-serving skew** | Festival audio (crowd noise, outdoor acoustics) differs from clean training data — models that look good in dev degrade silently in production | Include festival-condition augmentation in training data; validate on field recordings | | **Deploying without a monitoring baseline** | Shipping a content safety classifier without logging false-positive rate means model drift is invisible until a content incident occurs | Capture and store prediction confidence distributions on day-1 deployment as the baseline for drift alerts | | **Cloud-first model selection** | Choosing a model that requires server-side inference when festival connectivity is unreliable creates a single point of failure | Evaluate on-device feasibility first; cloud inference is a fallback, not a default |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The iteration protocol is present and functional. The agent capabilities table is clear. The role loses points because STOP checkpoints in the workflows are implicit rather than explicit — Workflow 1 has no marked human review gates within the DEVELOP and OPTIMIZE stages, only an implied review before DEPLOY. An agent could run through architecture design, training, and optimization autonomously without surfacing results until production deployment. For an AI-Primary role with model risk, mid-workflow STOP points are essential.",
      "example_rewrite": "In Workflow 1, add explicit STOP markers: '2. DEVELOP — Build model, train and evaluate, iterate on approach → OUTPUT: Candidate model with eval report → ⛔ STOP: Present candidate model card and evaluation metrics to AI Research Lead for architecture review before optimization begins. Do not proceed until approved. 3. OPTIMIZE — Profile performance, optimize for production → OUTPUT: Optimized model benchmarks → ⛔ STOP: Present latency/accuracy tradeoff report to Engineering Manager. Confirm edge deployment viability before containerization.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix is genuinely specific — naming Whisper, providing concrete latency and accuracy targets, and identifying festival edge constraints is meaningfully better than most role files. It loses points because the accuracy metric for transcription is incorrectly specified as '>95% WER' when WER (Word Error Rate) is a metric where lower is better, not higher. A target of '>95% WER' would mean 95%+ of words are wrong — this is a critical error that would cause an agent to optimize in the wrong direction. Additionally, the model priorities table has no owner or review date.",
      "example_rewrite": "Correct the metric and add ownership: | Model | Latency Target | Accuracy Target | Metric Definition | Owner | | Transcription (Whisper) | p95 < 5s for 60s audio on target edge device | WER < 5% on Story Portal eval set | Word Error Rate — lower is better; WER = (S+D+I)/N | AI/ML Engineer | | Content safety | p95 < 500ms | Precision > 99% at 95% recall on labeled moderation set | High precision prevents over-blocking; recall floor prevents unsafe content passing | AI/ML Engineer |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 4+ role-specific failure modes. This section is entirely absent, and for an AI-Primary role that autonomously trains and deploys models to production, the absence of documented failure modes (training-serving skew, offline-metric overfitting, missing monitoring baselines) creates direct production risk. An agent with no anti-pattern guardrails has no basis to self-correct before a bad model reaches a festival deployment."
}
```