```json
{
  "role": "agent-performance-analyst",
  "department": "human-resources",
  "scores": {
    "philosophy_depth": 2,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 4,
    "story_portal_relevance": 3
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 2,
      "finding": "All 6 principles are generic management platitudes that could apply to any analyst role in any industry. 'Measure To Improve' and 'Continuous Optimization' carry no specificity to AI agent performance analysis. None of the principles address what makes this role unique: the challenge of measuring non-human workers, the difference between output quality and prompt compliance, or the ethical complexity of optimizing AI behavior. The explanations ('Data drives optimization', 'Always getting better') are one-liners that add zero operational guidance.",
      "example_rewrite": "Replace generic principles with role-specific ones. Example: **Behavior Is a Proxy, Not the Goal** — Agent output metrics (task completion rate, response time) reveal symptoms, not causes. Always trace metric anomalies back to role design, skill gaps, or prompt drift before recommending changes. | **Dead Metrics Mislead** — A metric no longer connected to a real outcome (e.g., 'handoff count' when the workflow changed) actively harms optimization. Audit metric relevance every cycle, not just metric values. | **Cross-Agent Patterns Outrank Individual Outliers** — A single underperforming agent is a deployment issue. The same underperformance across five agents with the same skill is a systemic design failure. Prioritize systemic signals."
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs name roles but describe artifacts in the vaguest possible terms: 'Deployment data', 'Quality metrics', 'Role insights', 'Skill insights'. These tell an AI agent nothing about what file format to expect, what fields matter, what constitutes a complete artifact, or what the receiving role will do with it. 'Performance feedback' sourced from 'All Departments' is not a handoff — it is a wishful input with no defined structure or trigger. The outbound handoffs to Role Engineer and Skill Developer lack any specification of what form 'insights' take or what action should follow receipt.",
      "example_rewrite": "**Receives From — Quality Assurance Auditor:** Artifact: Weekly QA Audit Report (Markdown, structured by agent name > task type > pass/fail > failure category). Analyst uses failure category distribution to identify whether errors cluster around a specific skill, role boundary violation, or prompt behavior. | **Delivers To — Role Engineer:** Artifact: Role Optimization Brief (Markdown) containing: (1) agent name, (2) performance metric triggering review, (3) 90-day trend line, (4) analyst hypothesis on root cause (role design vs. skill gap vs. data input), (5) recommended role change in plain language. Role Engineer uses this brief as the intake document for a role revision cycle."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "The role contains NO anti-patterns section whatsoever. The DO/DON'T boundary list is present but functions only as a domain ownership map ('don't design roles'), not as behavioral anti-patterns. There is no list of failure modes specific to performance analysis of AI agents — such as confusing correlation with causation in agent metrics, over-indexing on easily measurable outputs while ignoring hard-to-measure quality signals, or recommending role redesigns based on insufficient data samples. This is the most critical structural gap in the document.",
      "example_rewrite": "Add a dedicated Anti-Patterns section. Example: **ANTI-PATTERN 1 — Metric Tunnel Vision:** Optimizing only for the metrics that are easy to collect (task completion count, response time) while ignoring harder signals (output quality drift, escalation rate increase). Fix: Every analysis cycle must include at least one qualitative signal sourced from QA Audit Reports. | **ANTI-PATTERN 2 — Single-Cycle Conclusions:** Declaring an agent underperforming based on one reporting cycle. AI agent performance fluctuates with input quality and context. Fix: Require minimum 3-cycle trend before escalating a performance concern to CHRO. | **ANTI-PATTERN 3 — Recommending Fixes Outside Your Domain:** Analyst identifies a skill gap and begins drafting skill content instead of routing a Skill Optimization Brief to Skill Developer. Fix: All recommendations must terminate at a named role handoff, never at a solution the Analyst implements directly."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "An AI agent loading this role would know its general purpose but would be unable to execute any specific task without additional context. The workflows use placeholder language ('Run analysis', 'Gather data', 'Develop insights') that provide no operational instruction. The Iteration Protocol is present and correctly structured with a STOP point, which is a positive. However, there is no specification of what data schema to expect, what a 'performance metric' is defined as in the Story Portal context, what threshold triggers escalation vs. a recommendation, or what the actual output format of a report looks like. The Tools section lists 'Analytics Platforms' and 'Statistical Tools' without naming any actual tools, making it inoperable.",
      "example_rewrite": "Replace vague workflow steps with executable instructions. Example — ANALYZE step: 'For each agent in the current cycle dataset: (1) Calculate 30-day rolling average for each metric in the Agent Scorecard schema [task_completion_rate, quality_pass_rate, escalation_rate, avg_cycle_time]. (2) Compare to department benchmark baseline stored in Workforce Registry. (3) Flag any agent where two or more metrics fall more than 1.5 standard deviations below baseline for three consecutive cycles. (4) Tag flagged agents with failure hypothesis: ROLE_BOUNDARY, SKILL_GAP, INPUT_QUALITY, or INSUFFICIENT_DATA. Do not escalate INSUFFICIENT_DATA flags.' Also add: escalation threshold — escalate to CHRO only when 3+ agents in the same department show correlated decline within a single 30-day window."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 3,
      "finding": "The Story Portal appendix names four agent categories (Platform, Creative, Festival, Support) and four generic metric types (task completion, quality output, efficiency, collaboration), but provides no Story Portal-specific content. There is no reference to what 'Festival Agents' actually do, what makes 'Creative Agent' effectiveness different to measure from 'Support Agent' effectiveness, or what the actual performance priorities of the Story Portal project are. The priority list (Core effectiveness > Quality > Efficiency > Collaboration) is identical to what any analyst role would produce for any project. The appendix reads as a placeholder filled with plausible-sounding but project-agnostic content.",
      "example_rewrite": "Add Story Portal-specific metric definitions per agent category. Example: **Creative Agents** — Primary effectiveness signal is Festival Director approval rate on generated content briefs (target: >85% first-pass approval). Secondary signal is revision cycle count per deliverable (target: <2 cycles). Warning threshold: if revision cycles exceed 3 on more than 20% of briefs in a single festival cycle, trigger a Role Optimization Brief to Role Engineer. **Festival Agents** — Effectiveness is measured against festival milestone adherence: did agent-generated timelines match actual delivery dates within ±2 days? Track drift per festival phase (pre-production, production, post). Escalate to CHRO if milestone drift exceeds 5 days on two consecutive festivals for the same agent."
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific failure modes. This is the most critical gap because the role has zero protection against the most common analyst failure modes (metric tunnel vision, single-cycle conclusions, scope creep into solution implementation). Without anti-patterns, an AI agent operating this role has no guardrails on its reasoning process, only guardrails on its domain ownership — and domain ownership rules do not prevent bad analysis, they only prevent role boundary violations."
}
```