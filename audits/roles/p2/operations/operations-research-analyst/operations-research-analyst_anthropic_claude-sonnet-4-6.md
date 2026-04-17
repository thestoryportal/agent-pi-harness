```json
{
  "role": "operations-research-analyst",
  "department": "operations",
  "scores": {
    "philosophy_depth": 2,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 2,
      "finding": "All six principles are generic platitudes that could apply to any analyst role in any industry. 'Data Reveals Truth' and 'Efficiency Focus' carry zero role-specific meaning. None of the principles address the tension unique to this role — being an AI agent that produces intelligence for human decision-makers without overstepping into strategy. There is no principle about data provenance integrity, about the limits of benchmark applicability, or about communicating uncertainty in analysis.",
      "example_rewrite": "Replace generic entries with role-specific principles. Example: 'Benchmark Skepticism — Industry benchmarks describe averages, not targets. Always surface the source methodology, sample size, and recency before presenting a comparison as actionable. A benchmark from a 500-person SaaS company does not translate directly to Story Portal festival operations.' And: 'Uncertainty is Data — When confidence in a finding is low due to incomplete data, say so explicitly in the report. A hedged insight is more valuable than a false certainty that sends the Process Manager in the wrong direction.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs list artifact categories ('Operational data', 'Strategic insights', 'Process analysis') rather than named documents with defined states. The Receives From section is especially weak — 'Operations Team' and 'All Departments' are not specific roles, and 'Process data' has no format or trigger condition. The Delivers To section does not specify the format of the artifact, the cadence, or the condition that triggers delivery. Roles referenced (Vendor Manager, IT Manager, Head of Data & Analytics) cannot be verified against a charter that was not provided, creating hallucination risk.",
      "example_rewrite": "Replace vague rows with artifact-level detail. Example: '| Delivers To | Artifact | Trigger | Format | | Process Manager | Bottleneck Analysis Report | After Workflow 2 Step 4 completes | PDF + raw data CSV, shared in ops-reports channel | | COO | Weekly Operations Intelligence Brief | Every Monday 08:00 | 1-page executive summary + supporting data appendix |'. For Receives From: '| IT Manager | System Performance Export | Weekly automated pull from ops dashboard | CSV with uptime, error rates, transaction volumes |'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file. The DO/DON'T boundary list exists but it covers role jurisdiction, not behavioral failure modes. Anti-patterns should describe ways this specific AI agent could produce harmful or misleading outputs — such as presenting correlation as causation in efficiency analysis, over-indexing on available data while ignoring missing data gaps, or generating recommendations that exceed the research mandate and drift into strategy. None of these failure modes are addressed anywhere in the document.",
      "example_rewrite": "Add a dedicated Anti-Patterns section. Example: '| Anti-Pattern | Description | Correct Behavior | | Correlation Causation Drift | Reporting that Process A causes inefficiency because it correlates with delay metrics, without ruling out confounds | State the correlation finding and explicitly note what additional data would be needed to establish causation before recommending process changes | | Recency Bias in Benchmarks | Using the most recently found benchmark without checking if it reflects comparable operational scale or business model | Always document benchmark source, date, sample, and comparability assessment in every benchmark table | | Scope Creep into Strategy | Framing a recommendation as a decision rather than an option — e.g., writing We should switch vendors rather than The data supports evaluating alternative vendors | All recommendations must use enabling language and route strategic conclusions to the COO via escalation |'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and is a positive signal, but the STOP point is underspecified — it does not define what constitutes a reviewable output, who the human reviewer is by role name, what the approval signal looks like, or what timeout behavior applies if no response is received. The Agent Capabilities table lists capabilities but does not map them to specific tools or APIs the agent should invoke. The workflows have no STOP checkpoints embedded within them — a multi-step analysis workflow runs entirely autonomously with human review only at the very end, which is insufficient for an AI-Primary agent handling strategic operational intelligence.",
      "example_rewrite": "Embed STOP points inside workflows and sharpen the iteration protocol. Example in Workflow 1: '3. INTERPRET — Extract insights, develop recommendations, prioritize findings → OUTPUT: Draft Insights Document — STOP: Present draft insights to COO or delegated Operations Lead for strategic alignment check before proceeding. Do not generate final report until human confirms findings are directionally correct. If no response within 24 hours, hold and send reminder. Do not self-approve.' And in Iteration Protocol: 'STOP → Send insight summary to COO via [defined channel]. Wait for explicit approve, revise, or discard signal. Default behavior on timeout: re-send once at 24h, escalate to Process Manager at 48h.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix names four focus areas and five metrics, which is a start, but nothing in it is actionable or specific to the Story Portal product context. 'Festival readiness' and 'Platform uptime' are labels, not definitions. There is no explanation of what festival operations means in this context, what the festival cycle looks like, what operational data sources exist in the Story Portal environment, or how the research priorities connect to current business challenges. A newly loaded AI agent reading this appendix would have no additional capability compared to reading nothing.",
      "example_rewrite": "Replace label-only tables with context that activates the agent. Example: '### Festival Operations Context — Story Portal runs N festival cycles per year. Each festival has a 90-day preparation window. The Analyst monitors a pre-defined set of readiness milestones tracked in [system name]. Key efficiency question: are festival preparation tasks completing on schedule relative to the prior cycle baseline? Benchmark source: internal historical data from previous festivals stored in [location]. Alert threshold: any milestone category falling more than 7 days behind prior-cycle pace triggers an immediate efficiency flag to the Process Manager.' Also specify: what does platform uptime mean here — is it the streaming platform, the ticketing integration, the partner API layer? Each has a different owner and different acceptable threshold."
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section. This role has zero anti-patterns defined anywhere in the document, which is the highest-risk gap. An AI-Primary agent performing operational intelligence analysis without explicit failure mode guardrails will inevitably drift into correlation-causation errors, scope creep into strategy, and false-confidence reporting. This is not a formatting issue — it is a safety gap. The anti-patterns section should be written before this role is deployed in any live environment."
}
```