```json
{
  "role": "content-designer-ux-writer",
  "department": "design",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 6,
    "anti_pattern_quality": 6,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "All six principles are generic UX writing maxims that could appear in any content design textbook. 'Clarity Over Cleverness,' 'Less Is More,' and 'Voice Is Consistent' are industry clichés with no binding to Story Portal, festival contexts, or this team's actual constraints. None reference the emotional stakes of storytelling, the transient festival audience, or the interplay between AI-generated variations and human voice judgment that defines this specific Hybrid role.",
      "example_rewrite": "Replace 'Less Is More' with: **One Shot, One Sentence** — Festival users read in motion, under noise, with 3 seconds of attention. Every UI element gets one sentence maximum; if you need two, the design has a clarity problem, not a copy problem. Replace 'Voice Is Consistent' with: **Whimsy With a Guardrail** — Story Portal earns warmth and playfulness only inside a safety boundary: consent copy is always plain, unambiguous, and legally reviewable regardless of surrounding tone."
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Handoffs name roles correctly but artifacts remain vague. 'Wireframes, flows' from UX Designer and 'Voice guidelines' from Visual/Brand Designer give an AI agent no actionable information about file format, naming convention, or what 'ready' looks like. The delivery side is equally thin — 'Final strings' to Frontend Developer does not specify whether strings are delivered as a JSON file, a Figma annotation layer, a spreadsheet, or a pull request comment.",
      "example_rewrite": "| Receives From | Artifact | Format | Ready Signal |\n|---|---|---|---|\n| UX Designer | Annotated wireframes with copy slot markers | Figma file, shared link | Frame named 'Copy-Ready v[n]' |\n| Product Manager | Feature brief with user story and error state list | Notion doc | Tagged 'Content: Needs Copy' |\n| Visual/Brand Designer | Voice & Tone guide with banned word list | PDF + Figma library | Version number confirmed in #design-system Slack |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 6,
      "finding": "The five anti-patterns ('Jargon,' 'Blame language,' 'Vague errors,' 'Inconsistent voice,' 'Walls of text') are universally applicable to any writer in any product and require no knowledge of Story Portal to produce. None address failure modes specific to this role's Hybrid classification — for example, an AI generating copy variations that are technically consistent but emotionally flat, or defaulting to corporate-sounding error messages that violate the whimsical voice. The festival deployment context is entirely absent.",
      "example_rewrite": "| Don't | Why | Instead |\n|---|---|---|\n| AI-generated 'safe' synonyms that strip warmth | AI variations default to neutral; neutral kills Story Portal's voice | Human must reintroduce personality in every AI draft pass before approval |\n| Applying festival tone to consent screens | Whimsy on a data consent prompt reads as dismissive and erodes trust | Consent copy follows plain-language legal standard; tone switch is intentional and documented |\n| Spin prompt copy that implies failure is possible | 'Try spinning again' creates anxiety at an emotional moment | Frame every retry as continuation: 'The wheel has another story for you' |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Context Requirements section is unfilled — '[Context item 1]' and '[Context item 2]' are literal placeholders, and the Required Skills table has no entries. An AI agent loading this role has no idea what context files to pull, what skill modules to activate, or how to initialize for a Story Portal session versus a generic copy task. The Iteration Protocol loop is present but has no state for 'AI proposes, human selects' which is the core Hybrid interaction pattern. There is also no guidance on what the AI should NOT generate without human sign-off.",
      "example_rewrite": "### Required Context\n- [ ] story-portal-voice-guide.md — defines whimsy guardrails and banned words\n- [ ] festival-audience-profile.md — age range, literacy baseline, ambient noise constraints\n- [ ] error-state-catalog.md — master list of all technical error codes and current message status\n\n### Required Skills\n| Skill | When to Load |\n|---|---|\n| microcopy-variation-generator.md | When drafting UI copy alternatives for human selection |\n| plain-language-checker.md | Before any consent or error copy is marked final |\n\n### Iteration Protocol — Hybrid Clarification\nAI MUST STOP before: finalizing any consent copy, changing voice guidelines, approving copy that contains legal claims. AI MAY proceed without stop: generating three variation drafts for human selection, checking existing copy against style guide, flagging inconsistencies."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The Story Portal appendix is the strongest section in the file. It names the actual product features (Wheel, Prompts, Recording, Consent), provides concrete sample copy with the correct voice, and addresses the festival context meaningfully. Minor gap: the Festival Context table identifies challenges (quick scanning, noise) but does not specify character limits or any measurable constraint. 'Ultra-short' is not actionable for an AI agent generating copy.",
      "example_rewrite": "| Consideration | Constraint | Rule |\n|---|---|---|\n| Quick scanning | 3-second read window | Spin invitation ≤ 8 words; all primary CTAs ≤ 4 words |\n| Diverse audience | Reading level target | Flesch-Kincaid Grade 6 maximum for all non-consent copy |\n| Emotional moment | High personal vulnerability | No exclamation marks on recording screens; warmth through word choice not punctuation |\n| Noise/distraction | Cannot rely on body text | Every screen must communicate its primary action via button label alone, no supporting paragraph required |"
    }
  ],
  "top_improvement": "Fill the Context Requirements section immediately — the two placeholder items '[Context item 1]' and '[Context item 2]' mean an AI agent loading this role has zero initialization instructions. A Hybrid role with no required context files cannot self-configure, making the entire deployment section non-functional. Define at minimum: the Story Portal voice guide, the error-state catalog, and the festival audience profile as required context, then add explicit STOP gates for consent copy and voice-guideline changes."
}
```