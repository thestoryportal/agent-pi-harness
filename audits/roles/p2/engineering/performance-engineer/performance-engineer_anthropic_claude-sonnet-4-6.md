```json
{
  "role": "performance-engineer",
  "department": "engineering",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 7,
    "anti_pattern_quality": 8,
    "ai_deployment_clarity": 9,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "All 6 principles are role-specific and meaningful. 'Alert, Don't Drown' and 'Data Over Intuition' are particularly strong — they encode real professional judgment. Minor deduction because 'Measure Everything' and 'Catch It Early' are widely used in performance engineering culture and appear in countless blog posts. They aren't wrong, but they're closer to industry clichés than proprietary principles. 'User Experience Is the Metric' is strong in intent but lacks the sharp specificity that would make it operationally distinct — it doesn't tell the agent *which* user experience metric to prioritize when they conflict (e.g., LCP vs. CLS vs. audio latency for Story Portal).",
      "example_rewrite": "Replace 'Catch It Early' with: '**Shift Left, Not Shift Blame** — A regression caught in a PR comment costs one engineer one hour; the same regression caught in production costs a war room. Every CI/CD gate is cheaper than every postmortem.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 7,
      "finding": "The delivers-to table is the strongest section — naming specific artifact types (optimization recommendations with evidence, capacity recommendations, automated performance gates) is exactly right. The receives-from table is weaker: 'Engineering Manager → Performance requirements, priorities' is vague. What format? A Jira ticket? A written spec? A Slack message? Similarly, 'QA → Performance bugs, test scenarios' doesn't specify what artifact QA actually produces. The handoff flow diagram between Performance Engineer and Performance Tester (QA) is excellent structural documentation but doesn't name the specific artifact passed at the pre-release handoff — 'baseline metrics and known issues' should be a named document.",
      "example_rewrite": "In the Receives From table: | Engineering Manager | Signed-off Performance Budget Document (Google Doc or Confluence page) defining target metrics per user journey, approval threshold for budget changes, and escalation contacts | and at the pre-release handoff: 'Performance Engineer → delivers: Performance Baseline Report (PDF/markdown) containing: p50/p95/p99 for all monitored endpoints, current Core Web Vitals scores, known regressions with JIRA ticket links, and signed baseline hash for QA comparison.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 8,
      "finding": "All 6 anti-patterns are genuinely role-specific — 'Suppress alerts' and 'Profile production carelessly' are strong because they encode real failure modes unique to autonomous performance agents. 'Recommend without data' directly enforces the 'Data Over Intuition' philosophy principle, showing internal consistency. Minor deduction: 'Alert on every metric' is well-framed but the remediation ('Smart thresholds, actionable alerts') is vague — it doesn't tell the agent *how* to decide what's actionable. A second gap: there's no anti-pattern covering the autonomous agent's specific risk of updating baselines incorrectly after a known-bad build, which is a real failure mode for this exact role.",
      "example_rewrite": "Add: | Accept a regression as the new baseline | Silently absorbs performance degradation into the baseline, making future regressions invisible | Baselines may only be updated after a human-approved build; flag any auto-baseline candidate with a PENDING_APPROVAL tag and hold for Engineering Manager sign-off before writing to baseline store |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 9,
      "finding": "This is the strongest dimension. The autonomy table with three columns (Activity / Autonomy / Human Involvement) is immediately actionable. The two autonomous workflow pseudocode blocks give an agent a clear decision tree. The Agent vs. CLI split by activity type is precise. The guardrails table is enforceable, not aspirational. The only gap: the CONTINUOUS MONITORING workflow references 'alert appropriate owner' without mapping which alert type routes to which owner — an agent would need to make a judgment call on routing. The escalation table in Boundaries covers this partially but isn't cross-referenced from the workflow.",
      "example_rewrite": "In the CONTINUOUS MONITORING workflow, step 3: 'IF threshold violated: → Log issue → Generate diagnosis → Alert appropriate owner [See: Boundaries > ESCALATE for routing table — Critical performance degradation → Engineering Manager; Infrastructure capacity → Platform/DevOps; Code-level fix required → Relevant Engineer + EM]'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The Story Portal appendix is genuinely project-specific — naming wheel_spin_fps, recording_start_latency, and electricity_effect_fps as custom metrics shows real product knowledge. The priority ranking (Wheel Frame Rate → App Load Time → Recording Responsiveness → Electricity Effect) gives the agent clear triage logic. The k6 scripts are runnable, not placeholder. Two gaps: (1) The metrics table shows 'TBD' for all Current values, which is expected for MVP but means the agent has no baseline to detect regressions against — there should be a protocol for what the agent does before baselines exist. (2) The recommended monitoring setup uses a real production URL (thestoryportal.org) in the load test patterns but the metrics table says 'Current: TBD' — minor inconsistency suggesting the appendix was partially templated.",
      "example_rewrite": "Add a 'Pre-Baseline Protocol' subsection: 'Before baselines exist, Performance Engineer operates in Observation Mode: run Lighthouse and key journey benchmarks on every build, record all results, and after 5 consecutive builds with no code changes to a component, compute p50 of those runs as the provisional baseline. Flag as PROVISIONAL in all reports until Engineering Manager approves. Do not block CI/CD builds on PROVISIONAL baselines — warn only.'"
    }
  ],
  "top_improvement": "Add a Pre-Baseline Protocol to the Story Portal appendix. The role is deployed at MVP with all current metrics marked TBD, meaning the autonomous regression detection workflows — the core value of an AI-Primary performance agent — cannot function until baselines exist. Without a defined bootstrap protocol, the agent either blocks incorrectly (no baseline = every build fails) or silently skips regression checks (no baseline = no gates). A 5-build observation window with provisional baseline logic and warn-only CI/CD enforcement unblocks the agent immediately at project start and gives Engineering Manager a clear approval trigger to activate full enforcement."
}
```