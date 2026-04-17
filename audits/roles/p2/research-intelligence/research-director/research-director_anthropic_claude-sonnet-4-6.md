```json
{
  "role": "research-director",
  "department": "research-intelligence",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 4,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic platitudes that could apply to any research function at any company. 'Rigor Is Non-Negotiable' and 'Continuous Learning' are filler statements with no specificity to Story Portal, festival storytelling, or the unique tension this role must navigate between fast-moving experiential tech research and strategic advisement. None of the principles explain HOW this director operates differently from a generic researcher.",
      "example_rewrite": "| **Prototype Research Over Perfect Research** | Story Portal operates in pre-product space — research must inform rapid prototyping cycles, not wait for longitudinal studies. A directionally correct insight in 48 hours beats a rigorous report in 6 weeks. |\n| **Ethnographic Instinct** | Festival storytellers don't self-report accurately. Research must observe behavior in situ — at events, in the moment — not rely on surveys or focus groups conducted in sterile conditions. |\n| **Skepticism Toward Competitive Benchmarks** | No direct competitor to Story Portal exists. Analogous experience research (escape rooms, interactive theatre, ambient installations) must be translated, not copied. Avoid false equivalence."
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs are dangerously vague. 'Receives: Strategic priorities from CEO' and 'Delivers: Strategic insights to Executive Team' describe categories of communication, not actual artifacts. There is no specification of format (deck, memo, database entry), cadence (weekly, per-project), or the triggering condition that initiates the handoff. 'Research findings' appears three times with zero differentiation. Referenced roles like 'All Research Leads' are not verified against the Organizational Charter and may be hallucinated.",
      "example_rewrite": "| Delivers To | Artifact | Format | Trigger |\n|-------------|----------|--------|---------|\n| Chief Strategy Officer | Quarterly Research Priorities Memo | 1-page PDF, ranked by strategic impact score | First Monday of each quarter |\n| Chief Product Officer | User Research Brief | Structured template: question, method, n=, key findings, 3 implications | Upon completion of each user study |\n| Executive Team | Monthly Intelligence Digest | Slide deck max 10 slides: market signals, competitive moves, user behavior shifts | Last Friday of each month |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There are NO anti-patterns section in this role file. The DO/DON'T list under Boundaries is a boundary definition, not an anti-pattern section. Anti-patterns should describe failure modes specific to how a Research Director in this context goes wrong — e.g., over-indexing on academic rigor at the expense of speed, or producing insights that get shelved. The template standard explicitly requires 3-5 role-specific anti-patterns and this role has zero.",
      "example_rewrite": "### Anti-Patterns\n| Anti-Pattern | Why It Fails | Correct Behavior |\n|--------------|--------------|------------------|\n| **The Academic Trap** | Pursuing methodological perfection while the product team makes decisions without you. Research arrives after the decision is made. | Time-box all research programs. If a decision is needed in 5 days, deliver directional findings in 4. |\n| **Insight Without Activation** | Producing beautifully synthesized reports that sit in a shared drive. No one reads them, nothing changes. | Every research deliverable requires a named owner, a decision it informs, and a 30-day check-in on whether action was taken. |\n| **Surveying Festival-Goers Who Aren't Festival-Goers** | Recruiting research participants through online panels who don't attend festivals produces invalid data for Story Portal. | All primary user research must recruit from verified festival attendees or be conducted on-site at events. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Deployment Notes section contradicts itself structurally. The role is classified Human-Primary but includes an Iteration Protocol (which the template standard says is required for Hybrid/AI-Primary). The AI assistance items ('AI generates reports, AI tracks research') are listed without any instruction on what tool, what prompt structure, or what output format the AI should use. A real AI agent loading this role would have no idea what 'AI assists with analysis' means operationally. The Required Context section is left with literal placeholder text '[Context item 1]' and '[Context item 2]' — this is an unfilled template published in production.",
      "example_rewrite": "### AI Assistance Scope\n| Task | AI Role | Human Gate |\n|------|---------|------------|\n| Competitive landscape scanning | AI searches and summarizes public sources into structured brief using competitive-scan.md template | Human validates before distribution |\n| Research report drafting | AI drafts findings section from human-provided data outputs | Human rewrites implications and recommendations |\n| Tagging and filing research artifacts | AI categorizes and indexes completed research into knowledge base | Human approves taxonomy changes |\n\n### Required Context\n- [ ] story-portal-brief.md (product overview and target user definition)\n- [ ] current-research-roadmap.md (active and queued research programs)\n- [ ] research-quality-standards.md (methodology approval criteria)"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix names the right research territories (festival storytellers, interactive installation market, audio/visual tech) but stops at naming them. The Strategic Research Questions are good instincts but have no methodology specified beyond a label ('user research', 'engagement analysis'). There is no mention of research constraints specific to Story Portal — e.g., the difficulty of doing research in live festival environments, the small and hard-to-reach target user population, or the pre-product stage meaning there is no usage data to analyze. The appendix reads like a brainstorm, not a research plan.",
      "example_rewrite": "### Story Portal Research Constraints\n| Constraint | Implication for Research Director |\n|------------|-----------------------------------|\n| Pre-product stage | No behavioral data exists. All user research is attitudinal or observational. Avoid surveys that assume product familiarity. |\n| Festival access required | Primary research windows limited to event calendars. Director must secure research access to 2+ festivals per year minimum. |\n| Small target population | 'Festival storytellers' is a niche segment. Quantitative sample sizes will be small (n<50). Research must be qualitative-first. |\n| Fast iteration cycles | Product team prototypes every 6 weeks. Research turnaround must match. No program longer than 3 weeks without interim findings delivery. |"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section — this is the most critical gap because the role has zero anti-patterns, which means there is no guard rail against the most predictable failure modes (research that arrives too late, insights that never activate, recruiting wrong participants). This is not a polish issue; it is a missing safety mechanism. Draft 3-5 anti-patterns specific to the tension between research rigor and Story Portal's fast-moving, festival-constrained, pre-product context before this role is deployed."
}
```