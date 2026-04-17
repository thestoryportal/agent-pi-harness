```json
{
  "role": "uat-coordinator",
  "department": "quality-assurance",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 6,
    "anti_pattern_quality": 6,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All six principles are generic UAT platitudes that could appear in any project management textbook. 'User Voice Matters', 'Feedback Is Gold', and 'Timely Communication' carry no role-specific meaning and give the AI no behavioral differentiation. A UAT Coordinator in a festival tech context has specific tensions — non-technical users, time-boxed live events, consent sensitivity — none of which surface in the philosophy table. 'Facilitation Over Execution' comes closest to being role-specific but is still abstract.",
      "example_rewrite": "Replace generic principles with operationally specific ones. Example rewrites: 'Non-Technical Testers Need Structure — festival organizers and event staff are not QA professionals; every UAT session must begin with a 5-minute orientation covering what to look for, not how software works.' | 'Consent UAT Is Legal UAT — the consent flow is not a UX preference; it carries legal exposure, so any consent-related feedback is automatically escalated to Legal before synthesis, not after.' | 'Festival Deadlines Are Hard Walls — unlike enterprise UAT where timelines slip, a festival date cannot move; UAT planning must build in 48-hour contingency before go-live, and any blocker raised after that window triggers immediate Release Manager escalation.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Handoffs name actual roles and artifact categories, which is above baseline. However, several entries are still vague containers. 'Acceptance criteria, feature specs' from Product Manager and 'UAT issues for triage' to QA Lead do not specify format, location, or completeness threshold. The AI does not know whether 'acceptance criteria' means a Jira ticket, a Google Doc, a structured AC table, or a verbal confirmation. 'Technically tested features' from QA Lead has no definition of done attached, so the AI cannot determine whether a feature is actually ready to enter UAT. 'Client Success Manager → client tester access' has no artifact at all.",
      "example_rewrite": "Receives From — Product Manager: 'Acceptance Criteria Document (AC-DOC): structured table with columns [Scenario, Given/When/Then, Pass Condition, Owner], stored in Notion under the feature ticket, marked status=APPROVED before UAT planning begins.' | Delivers To — QA Lead: 'UAT Issue Log: export from issue tracker tagged [UAT-CYCLE-ID], each issue containing [scenario ID, tester name, steps to reproduce, severity, screenshot/recording link], delivered within 24 hours of session close.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 6,
      "finding": "The six anti-patterns are reasonable but mostly generic project management warnings that apply to any coordinator role ('rush for deadline', 'delay communication', 'let issues go unlogged'). Only 'accept unclear criteria' and 'skip stakeholder prep' have meaningful UAT specificity. Missing are anti-patterns unique to this role's context: proxy testing (a developer or PM filling in for a real user), sign-off by silence (treating non-response as approval), and the specific Story Portal risk of testing in a controlled environment but not simulating festival noise/connectivity conditions.",
      "example_rewrite": "Add: | 'Accept Proxy Testers — Don't | A developer running through UAT scenarios to unblock a deadline is not UAT; it is a second technical review. Business sign-off requires the actual business stakeholder or a named representative approved by Product Manager in advance.' | 'Treat Silence as Sign-Off — Don't | If a stakeholder does not respond to a sign-off request within the defined window, that is not approval — it is an escalation trigger to Release Manager and Head of QA.' | 'Test in Ideal Conditions Only — Don't | Story Portal deploys at live festivals; UAT sessions must include at least one run on mobile with degraded connectivity (throttled to 3G) to surface offline/PWA edge cases before go-live.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol, Hybrid split, and workflow STOP points give an AI agent sufficient structure to operate without going rogue. The role clearly delineates AI-owned tasks (drafting plans, compiling feedback, generating reports) from human-owned tasks (facilitation, negotiation, sign-off). Minor gap: the AI has no instruction for what to do when it receives ambiguous or contradictory acceptance criteria before UAT planning begins — a common real-world scenario — and the skill files are all marked as not yet existing, which leaves the AI without concrete methodology references at runtime.",
      "example_rewrite": "Add a conflict-handling instruction under the Iteration Protocol: 'IF acceptance criteria received from Product Manager contain ambiguous pass/fail conditions (e.g., subjective language like \"feels intuitive\" or \"loads quickly\" without a measurable threshold), STOP — do not proceed to UAT planning. Draft a Criteria Clarification Request listing each ambiguous item with a proposed measurable alternative and route to Product Manager for resolution before continuing.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The Story Portal appendix is the strongest section in the file. It identifies specific UAT scenarios, maps stakeholder groups with availability constraints, and prioritizes test areas in a way that reflects real project knowledge (consent flow, offline mode, festival conditions). Minor gaps: stakeholder availability for 'Target users' is listed as 'TBD' with no owner or plan to resolve, which leaves a planning hole. The UAT priorities table does not indicate which items are blockers for go-live versus nice-to-have, which the AI needs to correctly triage sign-off urgency.",
      "example_rewrite": "Resolve the TBD: 'Target Users — Availability: Client Success Manager owns recruitment of 3-5 representative users by [DATE-2 weeks before festival]; if not confirmed by that date, UAT Coordinator escalates to Head of QA and flags as go-live risk in weekly status report.' | Add a 'Go-Live Blocker' column to the UAT Priorities table: Priority 1 (Core Flow), 2 (Festival Readiness), and 4 (Consent Flow) = BLOCKER; Priority 3 (Content) and 5 (Mobile Experience) = HIGH but not blocking, can ship with known issues documented.'"
    }
  ],
  "top_improvement": "Rewrite the Philosophy section with UAT-Coordinator-specific principles that encode behavioral rules for this exact role in this exact context. The current six principles give the AI no decision-making guidance that differs from a generic project manager. At minimum, three of the six principles should reference Story Portal-specific realities (festival hard deadlines, non-technical testers, legal exposure on consent) so the AI has opinionated defaults when it encounters ambiguous situations — which is precisely when philosophy principles are actually used."
}
```