```json
{
  "role": "performance-tester",
  "department": "quality-assurance",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 5,
    "anti_pattern_quality": 8,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "All 6 principles are present and role-specific — 'Find the Breaking Point' and 'Baseline Everything' are genuinely performance-testing-specific rather than generic QA platitudes. 'Performance Is a Feature' borders on an industry cliché but is grounded in context. The table format is functional but principles lack a second column that explains *how* this agent applies the principle operationally, not just what it means philosophically. No improvement rewrite required at this score, but adding an 'Applied As' column would push this to a 9.",
      "example_rewrite": null
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "The Receives From table lists role names but the artifacts column is vague — 'Features ready for performance testing' and 'Release candidate for testing' are descriptions of states, not named artifacts. The Delivers To table is marginally better but 'Performance test reports' and 'Performance status' are still artifact categories, not named deliverables. No role in the charter is confirmed to exist (e.g., 'Performance Engineer' appears in Works With but is not in the escalation paths or confirmed as a charter role). Critical omission: no artifact format is specified, so the receiving role has no way to know what file type, structure, or tool output to expect.",
      "example_rewrite": "Receives From | QA Lead | 'Feature Performance Test Request' ticket (Jira, includes: target URL/endpoint, SLA requirements, target concurrency, and signed-off test environment URL). Delivers To | QA Lead | k6 HTML report + Markdown summary (load-test-report-[feature]-[date].md) containing P50/P95/P99 response times, error rate, throughput chart, and pass/fail against SLA thresholds."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 8,
      "finding": "Six anti-patterns are present and all are genuinely specific to performance testing. 'Test with unrealistic data → False confidence' and 'Ignore memory over time → Memory leaks in production' are exactly the kind of role-specific failure modes the template standard calls for. Minor deduction: 'Optimize without measuring' is slightly generic (applies to any engineering discipline) and the 'Instead' column for it ('Measure before and after') could be more prescriptive — it should specify *what* to measure and with which tool. No rewrite required at this score.",
      "example_rewrite": null
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "The Autonomous Operating Protocol loop and Iteration Protocol are both present and well-structured. The guardrails are concrete and enforceable ('Never test production without explicit approval'). The role would load cleanly and an agent would understand its operating cycle. Two gaps prevent a higher score: (1) the Required Skills section notes that all skill files are 'planned development' and do not yet exist — an agent loading this role has no actual skill files to load, leaving a critical context gap for its first deployment; (2) the STOP points in workflows reference 'QA Lead' but the role's Reports To says 'Head of QA (or QA Lead for daily work)' — the ambiguity about which human to surface results to could cause the agent to pause and ask rather than act.",
      "example_rewrite": "Until skill files are created, inject inline fallback context: 'If load-testing.md is unavailable, apply k6 defaults: ramp 0→target VUs over 2 minutes, hold for 5 minutes, ramp down 2 minutes. Capture P50/P95/P99/error rate. Compare to stored baseline in baselines/ directory. If no baseline exists, flag and create one from this run.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 9,
      "finding": "This is the strongest section in the file. The Story Portal appendix is highly specific: 60fps animation targets, WebGL render time budget of <16ms (correctly derived from the 60fps frame budget), memory growth cap of <10MB/hour, and a concrete performance budget table. The six testing priorities are ranked and clearly motivated by the product context (festival load simulation, PWA caching, audio recording). Minor gap: the 'Festival Concurrent Load' challenge specifies '100+ concurrent users' in the appendix but the standard metrics table earlier in the file lists generic throughput targets — these two sections are not linked. The agent should know to use the festival-specific concurrency number (100+) as the load test target for Story Portal, not the generic default.",
      "example_rewrite": null
    }
  ],
  "top_improvement": "Handoff specificity: replace vague artifact descriptions ('Features ready for performance testing', 'Performance test reports') with named file formats, tool outputs, and required fields for each handoff — e.g., specify that the deliverable to QA Lead is a k6 HTML report plus a Markdown summary with a defined filename convention and required sections (P50/P95/P99, error rate, pass/fail against SLA). Without this, the receiving role cannot validate completeness and the agent cannot confirm a handoff is done."
}
```