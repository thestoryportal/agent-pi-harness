```json
{
  "role": "prompt-engineer",
  "department": "ai-automation",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 5,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 3
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "Six principles present and mostly role-specific. 'Every Token Counts' and 'Test, Don't Guess' are genuinely prompt-engineering-specific. 'Clarity Over Cleverness' and 'Structure Enables Understanding' border on generic software wisdom but are grounded in the prompt context. 'Constraint Breeds Creativity' is the strongest differentiator — it reflects a real counterintuitive truth in prompt engineering. No rewrite needed; minor deduction for two principles that would fit any technical writing role."
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoffs name artifact types but not specific artifact instances or file conventions. 'Any role' as a sender is a hallucinated catch-all — the charter would list specific roles. 'HR' receiving 'Prompt patterns for skill library' doesn't specify the file format, naming convention, or destination path. 'AI/ML Engineer' receiving 'Efficiency metrics' doesn't specify what document or schema those metrics follow. The Works With table references 'Project Orchestrator' which may not exist in all charters.",
      "example_rewrite": "| Delivers To | Artifact | Format |\n|-------------|----------|---------|\n| Requesting Role | Optimized prompt as `[role]-prompt-v[n].md` with before/after token diff | Markdown |\n| HR Department | Prompt pattern entry following `pattern-library-entry.md` schema, filed to `/skills/prompt-patterns/` | Markdown |\n| AI/ML Engineer | Token audit report as `token-audit-[YYYY-MM-DD].csv` with columns: prompt_name, before_tokens, after_tokens, savings_pct | CSV |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Six anti-patterns are present and most are role-specific. 'Please kindly...' and 'Try to...' are genuinely prompt-engineering-specific with concrete token cost framing. 'Repeat instructions 3x' is solid. However, 'Skip testing' and 'Assume model knows intent' are generic enough to appear in any QA or technical writing role. The table is also missing one critical prompt-engineering anti-pattern: prompt injection risk when accepting prompts from untrusted sources."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "An AI agent could load this role and execute immediately. The three workflows have clear triggers, numbered steps, and explicit STOP checkpoints. The Iteration Protocol loop is unambiguous. The Optimization Techniques section with before/after token tables gives the agent concrete transformation rules to apply. Deduction for the Required Skills section referencing `claude-api.md` and `story-portal-stack.md` as skill files to load — if those files don't exist in the project, the agent has no fallback instruction and may hallucinate their contents."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 3,
      "finding": "There is no Story Portal section in this role file. The template standard requires a dedicated Story Portal section that is project-relevant and actionable. The Appendix covers token counting and Claude model limits, which is useful context but is not a Story Portal section. The file has no guidance on how this role interacts with Story Portal specifically — e.g., where optimized prompts are stored in the portal, how pattern library entries are surfaced to other agents, or how this role is invoked through the portal's orchestration layer.",
      "example_rewrite": "## Story Portal\n\n### How This Role Is Invoked\nThe Prompt Engineer is invoked by the Project Orchestrator via a `prompt-optimization-request` task card. The card must include: original prompt text, requester role, token budget, and desired output description.\n\n### Where Artifacts Live in the Portal\n| Artifact | Portal Location |\n|----------|-----------------|\n| Optimized prompts | `/roles/[department]/prompts/` |\n| Pattern library entries | `/skills/prompt-patterns/` |\n| Token audit reports | `/reports/token-audits/` |\n\n### Portal Trigger Events\n- `prompt.optimization.requested` → Workflow 1\n- `prompt.creation.requested` → Workflow 2\n- `token.audit.scheduled` → Workflow 3\n\n### Surfacing Patterns to Other Agents\nWhen a new pattern is added to the library, the Prompt Engineer emits a `pattern.library.updated` event so downstream roles can reload their skill context."
    }
  ],
  "top_improvement": "Add a dedicated Story Portal section. The role scores a 3 here because the section is entirely absent — not weak, but missing. Without it, the role cannot be properly orchestrated within the Story Portal framework: other agents don't know how to invoke it, artifacts have no canonical storage location, and the pattern library has no mechanism for surfacing updates to the broader AI workforce. This is a structural gap that affects every deployment of this role."
}
```