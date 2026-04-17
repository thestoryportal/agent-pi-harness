```json
{
  "role": "ai-trainer-evaluator",
  "department": "ai-automation",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 5,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic evaluation platitudes that could apply to any QA role in any industry. 'What gets measured gets improved' is a management cliché. 'Failure Is Data' and 'Continuous Improvement' appear in every quality framework ever written. None of the principles reflect the specific tension of a human evaluating AI outputs — the rater bias problem, the moving-target nature of AI quality as models update, or the ethical weight of deciding what 'good' AI behavior looks like.",
      "example_rewrite": "Replace generic principles with role-specific ones: | **Rater Bias Is the Enemy** | Your judgment is the gold standard — which means your blind spots become the system's blind spots. Calibrate constantly against other evaluators. | | **Evaluate the Edge, Not the Average** | Any AI looks good on easy cases. Your value is finding the 5% of inputs where the system fails in ways that matter — safety violations, hallucinations, tone failures. | | **A Score Without a Cause Is Noise** | A quality score of 3/5 tells an engineer nothing. Every rating below threshold requires a failure category, a root cause hypothesis, and a reproduction case. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoffs name roles correctly but the artifacts are dangerously vague. 'Models to evaluate' does not tell an AI agent what format to expect, what system to pull from, or what constitutes a complete handoff package. 'Training feedback' delivered to AI/ML Engineer could mean a Slack message or a structured JSON file — the ambiguity will cause dropped handoffs. The 'Works With' table uses descriptions like 'Quality feedback' which describes a topic, not an artifact.",
      "example_rewrite": "Replace vague artifact names with specific ones: | Receives From | Artifact | Format | | AI/ML Engineer | Model evaluation request: version tag, test set ID, evaluation criteria doc | Notion ticket + CSV test set | | Prompt Engineer | Prompt variants for A/B quality scoring: prompt text, intended use case, sample outputs (n≥20) | Google Sheet with standardized columns | | Delivers To | Artifact | Format | | AI/ML Engineer | Structured failure report: failure category taxonomy, reproduction inputs, severity scores, recommended retraining priority | JSON + PDF summary | | Prompt Engineer | Per-prompt quality scorecard: rubric scores on 5 dimensions, annotated failure examples, recommended revision targets | Annotated Google Sheet |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "This role has NO anti-patterns section at all. The template standard explicitly requires 3-5 role-specific anti-patterns. The Boundaries section has DO/DON'T lists but these describe scope boundaries, not behavioral failure modes. There is no section warning against the specific ways an AI Trainer/Evaluator goes wrong — rating drift over time, confirmation bias toward the model they helped design, over-indexing on fluency at the expense of factual accuracy, or creating evaluation datasets that only reflect easy cases.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: **Anti-Patterns to Avoid** | Anti-Pattern | Why It Fails | Correct Behavior | | **Fluency Bias** | Rating grammatically smooth outputs as high quality even when factually wrong or subtly unsafe | Score accuracy and safety independently from fluency; a polished hallucination is a high-severity failure | | **Dataset Convenience Sampling** | Building evaluation sets from whatever examples are easy to find, not from the distribution that matters | Evaluation datasets must include adversarial cases, edge inputs, and low-frequency but high-impact scenarios | | **Rater Drift** | Calibration loosens over time — what scored 3 in week 1 scores 4 in week 6 | Re-anchor to gold-standard examples weekly; flag any week where personal score distribution shifts >10% | | **Feedback Without Reproduction** | Reporting 'the model sometimes hallucinates dates' without a reproducible input sequence | Every failure finding must include the exact input, the bad output, and the expected output |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol exists (good — required for Hybrid) but is generic. The workflows lack STOP points that are explicitly labeled as human checkpoints — the template standard flags 'Missing STOP points' as a common mistake. Workflow 1 has no moment where a human must approve before proceeding. The Context Requirements table lists inputs but doesn't tell the AI agent where to look or what to do if an input is missing. An agent loading this role would know the shape of the work but would stall on the first ambiguous trigger.",
      "example_rewrite": "Add explicit STOP points to Workflow 1: '2. EVALUATE — Apply criteria, rate outputs, document issues, note patterns → OUTPUT: Ratings and notes ⛔ STOP: Present first 10 ratings to human evaluator for calibration check before continuing. Do not proceed if inter-rater agreement < 0.8. WAIT for human sign-off. 3. ANALYZE — Aggregate scores, identify trends, categorize issues → OUTPUT: Draft analysis ⛔ STOP: Present draft pattern findings to AI Research Lead before finalizing. Any finding that implies systemic model failure requires human confirmation before report generation.' Also add: 'IF input artifact is missing or ambiguous → HALT workflow and request clarification from triggering role. Do not substitute assumptions for missing ground truth data.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix is the strongest section in this file. It correctly identifies four specific evaluation targets (transcription, content safety, prompts, conversation), provides concrete metrics (word error rate, precision/recall, false positive rate), and even accounts for festival-specific conditions like noise and accents. The Festival Considerations table is genuinely role-specific. Minor gap: the Evaluation Datasets table lists dataset types but not where they live, who owns them, or how to request access — an agent would still need to ask a human where to find 'audio samples'.",
      "example_rewrite": "Strengthen the Evaluation Datasets table with ownership and access: | Dataset | Purpose | Owner | Access | | Audio samples | Transcription testing — min 500 clips, festival noise conditions | AI Operations Engineer | S3 bucket: story-portal/eval/audio — CLI access required | | Safety edge cases | Moderation validation — includes known bypass attempts and borderline content | AI Ethics Specialist | Restricted: request via Notion ticket to Ethics Specialist; 24hr SLA | | Prompt variations | Quality assessment across themes/genres | Prompt Engineer | Shared Google Drive: Story Portal > Eval > Prompts |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section. This is the only dimension that scores below 3, and it is a complete omission — not a quality issue but a missing section. The role currently has no behavioral failure modes documented, meaning an AI agent running this role has no guardrails against the most common and damaging ways this job goes wrong (fluency bias, dataset convenience sampling, rater drift, feedback without reproduction). This single addition would raise the role's safety and usefulness profile more than any other change."
}
```