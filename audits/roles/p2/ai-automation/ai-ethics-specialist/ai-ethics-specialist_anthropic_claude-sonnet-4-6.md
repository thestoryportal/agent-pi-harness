```json
{
  "role": "ai-ethics-specialist",
  "department": "ai-automation",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic AI ethics slogans lifted from any textbook or framework. 'Ethics by Design', 'Transparency Matters', 'Safety Is Non-Negotiable' — these could appear in any org's boilerplate. None are specific to Story Portal's context (audio storytelling, festival settings, oral narratives, emotionally vulnerable participants). The meaning column adds nothing — 'Build ethics in, don't bolt on' explains the label but doesn't define how this role applies the principle operationally in this org.",
      "example_rewrite": "Replace generic labels with Story Portal-specific principles: | **Narrative Consent Is Ongoing** | Consent for story recording, AI processing, and public use are three separate gates — each requires explicit opt-in, and any can be revoked independently at any time. | **Festival Context Changes Risk Calculus** | Public outdoor settings, emotional storytelling, and children present elevate privacy and safety thresholds above standard enterprise deployments. | **Moderation Bias Harms Marginalized Voices First** | Content moderation on oral narratives disproportionately flags non-dominant dialects, accents, and cultural idiom — bias testing must use demographic-stratified audio samples, not only text proxies. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Every artifact in both the Receives and Delivers tables is a vague category noun: 'Systems for review', 'Agents for safety review', 'Ethics reports', 'Bias findings'. There is no specification of file format, template name, required fields, or what 'ready for ethics review' means as a trigger condition. The collaboration table says 'Bias mitigation' and 'Safety review' as interface descriptions — these describe topic areas, not what is exchanged or when.",
      "example_rewrite": "| Receives From | Artifact | Format | Trigger Condition | | AI/ML Engineer | Model Card v1.0 (completed template) | .md file in /ethics-review/queue/ | Engineer marks PR 'ethics-review-required' | | Agent Developer | Agent Safety Checklist (self-assessment) + system prompt draft | .md + .txt | Before agent promotion to staging | | Delivers To | Artifact | Format | SLA | | Chief AI Officer | Ethics Review Report (severity-rated: Green/Amber/Red) | .md with executive summary ≤1 page | 5 business days from intake | | AI/ML Engineer | Bias Findings Report with fairness metric deltas by demographic group | .md with attached CSV | Concurrent with CAO delivery |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no dedicated Anti-Patterns section anywhere in this role file. The DO/DON'T list in Boundaries is not an anti-pattern section — it describes jurisdiction, not failure modes. Anti-patterns should describe how this specific role fails in practice: e.g., rubber-stamping reviews under deadline pressure, over-indexing on quantitative fairness metrics while ignoring qualitative stakeholder harm, or conflating legal compliance with ethical sufficiency. None of these failure modes are documented.",
      "example_rewrite": "### Anti-Patterns — AI Ethics Specialist | Anti-Pattern | Why It's Dangerous | Correction | | **Ethics Washing** | Completing review checklist items without substantive investigation because engineering timeline is tight — producing Green reports for systems with unexamined risks | Ethics review timelines are fixed minimums, not negotiables. Escalate timeline conflicts to CAO rather than compress review depth. | | **Metrics Tunnel Vision** | Declaring a model 'fair' because demographic parity scores meet threshold, while ignoring qualitative harm signals from community feedback or edge-case testing | Fairness metrics are necessary but not sufficient. Every quantitative pass requires a qualitative 'so what' check against actual user impact in Story Portal's festival context. | | **Compliance Conflation** | Closing an ethics concern because Legal has signed off — treating legal permissibility as ethical sufficiency | Legal clears the floor, not the ceiling. Document legal status separately from ethics recommendation; they can diverge. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Context Requirements section — one of the most critical for AI deployment — contains literal placeholder text: '[Context item 1]', '[Context item 2]', and '[Use placeholder format: skill-name.md]'. An AI agent loading this role has no idea what context files to load or what skills to activate. The Iteration Protocol exists and is structurally sound, but STOP points in the workflows lack specificity about what output must exist before proceeding. 'STOP → Scope confirmed' by whom, in what form, is unanswered.",
      "example_rewrite": "### Required Context | File | Purpose | Load When | | story-portal-overview.md | Platform architecture, user types, data flows | Every session | | ethics-review-template.md | Standardized report format with severity rubric | Ethics Review workflow | | bias-testing-corpus.md | Demographic groups, audio sample sources, fairness metric thresholds | Bias Analysis workflow | | festival-context.md | Physical setting constraints, vulnerable population protocols | Any Story Portal assessment | ### Required Skills | Skill | When to Load | | algorithmic-fairness-metrics.md | Bias Analysis workflow Step 2 | | stakeholder-harm-mapping.md | Ethics Review workflow Step 1 |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is the strongest section of this file and shows genuine project awareness — audio consent, festival context, vulnerable users, and oral narrative specifics are all present. However, the Ethics Checklist is still binary (check/no-check) with no thresholds, owners, or escalation criteria. The Festival Context table lists implications but no actions. 'Emotional content → Sensitivity, support' is not actionable for an AI agent or a human reviewer.",
      "example_rewrite": "Replace the Festival Context table with: | Factor | Specific Risk | Required Control | Owner | Escalation Trigger | | Emotional/traumatic content | Story triggers distress in narrator post-recording | Distress protocol document linked in booth; AI flags keyword patterns for human review within 2 hours | AI Ethics + Privacy Officer | Any report of narrator distress post-session → CAO + CEO same day | | Children present | Incidental capture of minors in background audio | Age-verification gate before recording; automated minor-voice detection model bias-tested quarterly | AI Ethics + Legal | Detection model false-negative rate >2% → halt deployment pending re-audit |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific failure modes. This role has zero anti-patterns documented, which is the most critical gap — an AI Ethics Specialist without documented failure modes is the highest-risk omission in the file, because ethics review failure (rubber-stamping, metrics tunnel vision, compliance conflation) is precisely what this role exists to prevent, and the role file provides no guard against it happening from within."
}
```