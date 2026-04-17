```json
{
  "role": "ai-research-lead",
  "department": "ai-automation",
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
      "finding": "All 6 principles are generic research platitudes that could apply to any researcher in any field. 'Applied Over Academic,' 'Evidence-Based,' and 'Share Knowledge' carry zero signal about what makes an AI Research Lead's philosophy distinct. They describe the job category, not the role's actual decision-making identity. There is no principle about how to handle the tension between chasing frontier models and organizational readiness, no principle about responsible experimentation with unproven AI, and no principle about when to kill a research thread.",
      "example_rewrite": "Replace generic entries with role-specific principles: | **Fail Fast on Fundamentals** | If a POC cannot beat the baseline within 2 experiments, kill it and document why — sunk cost is the enemy of good research | | **Capability Gap Over Hype Cycle** | Evaluate a technology against our specific audio/content/prompt gaps, not its benchmark scores or press coverage | | **Research Debt Is Real** | Every validated approach not handed off with a working artifact creates an orphaned finding — incomplete transfers are failed research | | **Festival-First Constraints** | Every experiment must include an offline/edge variant; a solution that requires cloud-only is a conditional solution, not a validated one |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but artifacts are one-word labels with no format, no trigger condition, and no acceptance criteria. 'Research insights' delivered to CAO could mean a Slack message or a 50-page paper. 'Validated approaches' to AI/ML Engineer does not specify whether that means a working Jupyter notebook, a benchmark report, a Docker container, or a written spec. Incoming artifacts are equally vague — 'Research priorities' from CAO and 'Technical constraints' from Engineering provide no structure for the AI agent to know what to expect or how to consume them. 'Product Research Lead' and 'Engineering Research Lead' are referenced in Works With but do not appear in the handoff table at all.",
      "example_rewrite": "| Delivers To | Artifact | Format | Trigger |\n|-------------|----------|--------|---------|\n| Chief AI Officer | Opportunity Brief | 1-page structured memo: background, experiment summary, confidence level (High/Med/Low), recommended next step, resource ask | After STOP → Validation complete in Workflow 1 |\n| AI/ML Engineer | Validated Approach Package | GitHub repo containing: working POC notebook, benchmark results CSV, known limitations doc, suggested production architecture notes | When confidence level is High and CAO approves productionization |\n| Product Manager | Opportunity Assessment | Prioritized shortlist (max 3 options) with effort estimate, risk rating, and Story Portal use case mapping | After STOP → Evaluation complete in Workflow 2 |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There are zero anti-patterns in this role file. The Boundaries section lists DO/DON'T items that are jurisdictional scope rules, not behavioral failure modes. An anti-pattern section should describe the specific wrong behaviors this AI agent might drift into — over-indexing on benchmark scores that don't reflect Story Portal's actual data distribution, building POCs that are too polished to kill, or continuing to explore a research thread past the STOP point without human approval. None of this is present. This is the most critical gap in the document.",
      "example_rewrite": "Add an Anti-Patterns section: | Anti-Pattern | Description | Correct Behavior |\n|---|---|---|\n| **Benchmark Capture** | Selecting a model because it wins on published leaderboards rather than on Story Portal's actual audio/content data | Always run evaluation on internal sample data before recommending; leaderboard scores are a filter, not a decision |\n| **POC Scope Creep** | Continuing to refine a proof of concept beyond the validation question, adding features that belong to production engineering | Stop when the research question is answered; hand off a working-but-rough artifact, not a finished product |\n| **Finding Hoarding** | Completing research but delaying knowledge sharing until a 'perfect' report is ready, leaving teams blocked | Share interim findings after each STOP point; the research wiki entry is written during the research, not after |\n| **Frontier Chasing** | Pivoting research focus to the newest model release before validating the previous candidate | Complete the validation cycle on the current candidate before opening a new research thread |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Context Requirements section — the most critical section for AI deployment — contains unfilled placeholder text: '[Context item 1]' and '[Context item 2]'. Required Skills uses a placeholder instruction instead of actual skill files. An AI agent loading this role has no idea what context to request before starting work. The Iteration Protocol exists and is functional, but the STOP points in Workflow 1 and 2 do not specify who the human checkpoint owner is or what approval looks like. The agent cannot distinguish between 'STOP → get a thumbs up in Slack' and 'STOP → present to CAO and wait for written go-ahead'.",
      "example_rewrite": "Replace placeholder Context Requirements: | Required Context | Source | When to Request |\n|---|---|---|\n| Current research priorities memo | Chief AI Officer | At session start, before any Workflow 1 trigger |\n| Story Portal audio sample dataset (min 50 clips) | Data Engineering | Before any audio AI evaluation begins |\n| Existing technology radar document | Research Wiki | Before any technology scouting work |\n| Production architecture constraints | AI Solutions Architect | Before Workflow 1 SCOPE step |\n\nAlso update STOP points: 'STOP → Scope approved' should read 'STOP → Present scope document to Chief AI Officer via async memo; do not proceed to EXPLORE until written approval received.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is the strongest section in the document and shows genuine project awareness — festival context, offline capability, noise tolerance, and latency are all real constraints that map to actual research implications. However, the Active Research Topics table lists statuses ('Evaluating,' 'Planned') without any owner, timeline, or success criterion, making it an inventory list rather than an actionable research agenda. The Research Questions in the focus table are directional but not experimentally framed — 'transcription quality' is not a research question, it is a topic area.",
      "example_rewrite": "Sharpen Research Focus table with testable questions and exit criteria: | Area | Research Question | Success Criterion | Current Status |\n|---|---|---|---|\n| **Audio AI** | Does Whisper large-v3 outperform AssemblyAI on Story Portal field recordings with >40dB background noise at under 2x realtime on edge hardware? | >85% WER on internal test set, <2x realtime on target device | Evaluating — benchmark dataset ready |\n| **Content Safety** | Can a lightweight local classifier match cloud moderation API accuracy within 5% on Story Portal content categories while running offline? | <5% accuracy gap vs. API baseline, <500ms latency | Exploring — defining test categories |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4-5 role-specific failure modes. This role file has zero anti-patterns, which means an AI agent has no guardrails against the most common research drift behaviors — benchmark capture, POC scope creep, and finding hoarding. Anti-patterns are the primary mechanism for keeping a Hybrid AI agent on the rails between STOP points, and their complete absence is the single highest-risk gap in this document."
}
```