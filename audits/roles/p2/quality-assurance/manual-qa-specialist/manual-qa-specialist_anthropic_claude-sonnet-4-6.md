```json
{
  "role": "manual-qa-specialist",
  "department": "quality-assurance",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 5,
    "anti_pattern_quality": 6,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Three of the six principles are repackaged generic QA truisms that appear in any testing handbook. 'Think Like a User' and 'Document Everything' are boilerplate found in every QA job description. 'Curiosity Finds Bugs' is a motivational poster, not an operational principle. None of the principles reference the specific product context (WebGL, steampunk UI, audio recording, Three.js) that defines what this role actually tests at Story Portal.",
      "example_rewrite": "Replace 'Curiosity Finds Bugs' with: '**WebGL Needs Human Eyes** — Automated tests cannot perceive that a brass gear texture looks washed out on Safari or that a Three.js segment highlight flickers on low-end Android. Visual and perceptual quality in 3D environments requires a human evaluator who can distinguish \"technically rendered\" from \"actually correct.\"' Replace 'Think Like a User' with: '**First-Time User Amnesia** — Test every session as if you have never seen Story Portal before. A returning developer cannot see the wheel is confusing; a simulated first-time visitor can. Always include a cold-visit scenario in every exploration charter.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Multiple handoff entries are vague role-level descriptions rather than artifact-level specifications. 'QA Lead → Test assignments, priorities' does not specify what form that assignment takes (a Linear ticket? a sprint board filter? a shared test charter doc?). 'Delivers To: QA Research Lead → Testing observations' is the worst offender — no artifact name, no format, no trigger condition. Additionally, 'QA Research Lead' does not appear in the Works With table, suggesting it may be a hallucinated or unverified role. 'Developers → Bug reports' omits that the artifact is a Linear issue with a specific label, severity tag, and linked screen recording.",
      "example_rewrite": "Replace 'Delivers To: QA Research Lead → Testing observations' with either a verified role name from the charter or remove it entirely. Replace 'Delivers To: Test Automation Engineer → Test cases for automation' with: 'Delivers To: **Test Automation Engineer** → A Linear ticket tagged [automation-candidate] containing: written test steps, the confirmed reproduction rate, browser/device scope, and a screen recording. Triggered after any exploratory session where the same bug path was reproduced 3+ times.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 6,
      "finding": "Four of the six anti-patterns ('Vague bug reports', 'Forget screenshots', 'Skip edge cases', 'Only happy paths') are universal QA hygiene rules that belong in a junior tester onboarding doc, not a role-specific anti-pattern table. They carry no Story Portal or AI-agent context. None of the anti-patterns address failure modes unique to an AI agent performing manual QA — for example, an AI systematically generating plausible-sounding but unverified reproduction steps, or over-reporting visual issues based on pixel comparison without understanding design intent.",
      "example_rewrite": "Replace 'Test like a robot / Miss exploratory bugs / Think like a user' with: '**Fabricating Confidence in Reproduction Steps** — An AI agent may write reproduction steps that sound precise but were inferred rather than observed. NEVER list a step you did not explicitly execute. If a bug appeared once and cannot be reproduced, label it [intermittent - unconfirmed] and include the session timestamp. A confident-sounding unreproducible bug report wastes developer time and erodes trust in QA output.' Add: '**Flagging Design as a Bug** — The steampunk brass aesthetic uses intentional desaturation, grain, and imperfect geometry. Do not file visual bugs against intentional art direction. Before filing any visual issue, cross-reference the UX Designer spec or ask QA Lead to confirm it deviates from approved design.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol and Autonomous Operating Protocol are present and functional, which clears the baseline bar. However, the autonomous loop lacks a concrete decision boundary for when the AI should STOP versus continue without human input. The guardrail 'Never modify production data' is correct but states the obvious — there is no guardrail specific to the ambiguity this role will actually face, such as: what to do when a visual finding is subjective, when a bug cannot be reproduced after three attempts, or when test environment instability makes results unreliable. An agent loading this role would not know how to handle those cases.",
      "example_rewrite": "Add to Guardrails section: 'IF a bug cannot be reproduced after 3 independent attempts → Tag [intermittent] and STOP → escalate to QA Lead with session log before proceeding. IF visual finding is subjective (e.g., animation feels slow, color looks off) → Do NOT file as bug → log as [design-observation] and STOP → request UX Designer confirmation. IF test environment returns errors on more than 30% of test runs → HALT session → escalate to QA Operations Manager with error log before continuing.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The Story Portal appendix is the strongest section of this role file. It names specific UI elements (steampunk wheel, brass effects, Three.js), defines a concrete browser/device matrix with priority levels, and lists six prioritized testing areas with meaningful focus descriptions. Minor gap: the Key User Scenarios table lists steps at a very high level ('Tap/click wheel → Watch animation → See result') without specifying the expected outcome that defines pass/fail. This means an AI agent executing 'Spin Wheel' has no definition of what a successful wheel spin looks like, making pass/fail judgment impossible without human input on every run.",
      "example_rewrite": "Expand the Spin Wheel scenario row: '**Spin Wheel** | 1. Tap/click wheel on desktop Chrome | 2. Wheel rotates with visible momentum for 2–4 seconds | 3. Rotation decelerates with easing (not abrupt stop) | 4. One segment lands highlighted with brass glow effect | 5. Highlighted segment title is legible at 1x zoom | **Pass criteria:** Smooth deceleration visible, single segment highlighted, no frame drop observable, result text readable. **Fail triggers:** Abrupt stop, multiple segments highlighted, text clipped, animation freeze.'"
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. The delivery to 'QA Research Lead' references a role not confirmed in the Works With table (possible hallucinated role), and every other handoff row omits the artifact format, the trigger condition, and the tracking mechanism. An AI agent executing this role cannot complete a handoff without knowing what file or ticket to create, where to put it, and when the handoff is considered done. Fix all Delivers To rows to specify: recipient role (charter-verified), artifact type, artifact format, trigger condition, and delivery location."
}
```