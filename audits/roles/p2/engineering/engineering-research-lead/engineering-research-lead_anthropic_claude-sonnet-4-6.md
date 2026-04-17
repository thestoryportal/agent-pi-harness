```json
{
  "role": "engineering-research-lead",
  "department": "engineering",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 6,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "All 6 principles are present and most are role-specific. 'Prove, Don't Assume' and 'Fail Fast, Learn Faster' are genuinely tailored to a research role. However, 'Document the Journey' and 'Pragmatic Exploration' border on generic — nearly any engineering role could claim these. The table format is clean but the 'Meaning' column for 'Breadth Before Depth' ('Survey the landscape before drilling into specifics') simply restates the principle rather than explaining the research-specific reasoning behind it.",
      "example_rewrite": "| **Breadth Before Depth** | Run a 2-hour survey pass across all viable candidates before time-boxing any single POC — prevents falling in love with the first option that works and missing a clearly superior alternative |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The 'Delivers To' table names real roles but the artifacts are dangerously vague. 'POC code (for reference)' doesn't specify where it lives, what format it takes, or what accompanies it. 'Evaluation reports' is a category, not an artifact. The 'Receives From' table is even weaker — 'Strategic technology questions' is a conversation, not an artifact. Additionally, 'DevOps Research Lead' and 'Product Research Lead' are listed as collaborators in the Works With table but do not appear as handoff partners, creating a gap. 'Performance Engineer' receives no handoff entry despite being listed as a collaborator for benchmarking work.",
      "example_rewrite": "| Delivers To | Artifact |\n|-------------|----------|\n| Solutions Architect | Technology Evaluation Report (Markdown, /research/evaluations/YYYY-MM-topic.md) + Comparison Matrix (scored criteria table) |\n| Development Team | POC Summary Document + archived POC code path in /research/pocs/ — explicitly NOT merged to main |\n| Performance Engineer | Benchmark Results Sheet (raw data + methodology + device targets) |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Five anti-patterns are present and the table format with Why/Instead columns is strong. 'POC becomes product' and 'Endless exploration' are genuinely specific to a research role. However, 'Research in isolation' and 'Opinion without evidence' could appear in any analyst or data role without modification. The checklist template warns against copy-paste boundaries — these two feel borrowed. Also missing: a research-specific anti-pattern around recency bias (choosing newer technology because it's newer, not because it's better), which is a real failure mode for this exact role.",
      "example_rewrite": "| **Recency Bias** | Recommending the newest framework because it's exciting, not because it's proven fit-for-purpose | Weight community maturity, production case studies, and team ramp-up cost equally against novelty in every evaluation scorecard |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "This is the role's strongest dimension. The Iteration Protocol loop is explicit, STOP points appear at correct decision gates in every workflow, and the CLI vs Browser split is unambiguous. The Hybrid classification rationale is well-articulated with five specific reasons rather than a generic statement. Minor gap: the Iteration Protocol loop says 'Execute research task' but doesn't tell the AI agent how to determine which workflow to enter (Evaluation vs POC vs Spike) when a new request arrives. An AI agent receiving an ambiguous request has no triage logic to follow.",
      "example_rewrite": "TRIAGE on intake:\n  IF request is 'which technology should we use for X' → Workflow 1 (Technology Evaluation)\n  IF request is 'can approach Y actually work in our stack' → Workflow 2 (POC)\n  IF request is 'answer this specific technical question by Friday' → Workflow 3 (Spike)\n  IF ambiguous → STOP and ask requestor: 'Are you comparing options, validating an approach, or answering a specific question?'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The appendix is genuinely project-specific — React 19, Vite 7, Three.js, IndexedDB, festival environment constraints, and the 60fps mobile target all demonstrate real context. The Phase 2 backend research priorities are actionable. However, the 'Research Lead has evaluated/may evaluate' bullet list is written in an ambiguous past/future tense that gives an AI agent no signal about current status. It reads like placeholder text. Additionally, 'Findings documented in project knowledge base' is cited as a quality bar but the knowledge base location is never specified, making it unactionable.",
      "example_rewrite": "### Research Status\n| Topic | Status | Output Location |\n|-------|--------|-----------------|\n| Supabase feasibility | 🔲 Not started — Priority 1 | /research/evaluations/supabase-phase2.md |\n| Three.js mobile rendering | 🔲 Not started — Priority 2 | /research/evaluations/threejs-mobile-perf.md |\n| IndexedDB sync strategy | 🔲 Not started — Priority 2 | /research/evaluations/offline-sync-strategy.md |\n\n**Knowledge base location:** /docs/research/ in project repo. Every completed evaluation must add an entry to /docs/research/INDEX.md."
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. Currently, artifacts like 'Evaluation reports' and 'Strategic technology questions' are categories and conversations, not deliverables. Every handoff row should specify: (1) the exact document name or file path convention, (2) the format (Markdown, scored matrix, working code path), and (3) whether it is accompanied by a verbal presentation or async-only. Without this, an AI agent completing a research task has no definition of 'done' that maps to what the receiving role actually needs."
}
```