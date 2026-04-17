```json
{
  "role": "role-engineer",
  "department": "human-resources",
  "scores": {
    "philosophy_depth": 2,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 3,
    "story_portal_relevance": 2
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 2,
      "finding": "All 6 principles are generic placeholders that could apply to any engineering role. 'Templates Are Training' and 'Boundaries Enable Focus' are vague slogans with no operational meaning. None reference the specific tension of this role: translating ambiguous organizational intent into precise agent behavior constraints. No principle addresses the core challenge of writing instructions for non-human executors.",
      "example_rewrite": "Replace generic slogans with role-specific operating principles: | **Precision Over Completeness** | A role template with 8 razor-sharp boundaries outperforms one with 20 vague responsibilities. When in doubt, constrain more. | **The Blank Context Problem** | Every template must assume the agent has zero institutional memory. If a behavior isn't written, it won't happen. | **Boundaries Are Bilateral** | Every DO requires a corresponding DON'T. A role that defines what it owns without defining what it refuses creates overlap debt. | **Anti-Patterns Are First-Class Citizens** | The failure modes of a role are as important as its success criteria. Document how this role breaks before it ships. | **Test Against Adversarial Prompts** | A role template is only as good as its worst-case input. Validate every role by trying to make it behave badly. | **Charter Fidelity Over Local Optimization** | A clever template that references a non-existent role poisons the entire workforce graph. Charter accuracy is non-negotiable. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Artifact names are present but remain abstract. 'Role requirements' and 'Role templates' are category labels, not actual artifact names. The handoff to Workforce Registry Manager references a role that may not exist in the charter — this is a hallucination risk flagged in the template standard. No handoff specifies file format, naming convention, required fields, or acceptance criteria. A receiving agent cannot act on 'templates for review' without knowing what a complete, review-ready template looks like.",
      "example_rewrite": "| Delivers To | Artifact | Format | Acceptance Criteria | | Agent Onboarding Specialist | Completed role template file | Markdown (.md), named [role-slug]-role.md, all 11 sections present, version table populated | Zero placeholder text remaining; Classification emoji matches charter; all referenced roles verified against Organizational Charter | | Quality Assurance Auditor | Role template + QA checklist | role template file + completed template-standard-checklist.md | Checklist self-assessment complete; known deviations documented in Document Control notes |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file. This is a critical omission per the template standard checklist. The DON'T list in Boundaries is a simple role-exclusion list ('don't do Designer's job'), not anti-patterns — which should describe specific failure behaviors this role is prone to. A Role Engineer has highly specific failure modes: hallucinating role references, writing philosophy that sounds good but gives no behavioral guidance, creating workflows without STOP points, and over-templating to the point where every role looks identical.",
      "example_rewrite": "Add a dedicated Anti-Patterns section: | Anti-Pattern | Description | Correction | | **Charter Hallucination** | Referencing roles in Collaboration or Handoffs that don't exist in the Organizational Charter | Before finalizing any template, cross-check every role name against the charter. If the role doesn't exist, either remove the reference or escalate to Organizational Designer to create it. | | **Philosophy Laundering** | Writing principles that sound meaningful ('Quality First', 'Context Is Key') but provide zero behavioral constraint to an agent | Each principle must complete the sentence: 'When facing [specific situation], I will [specific action] rather than [tempting alternative].' | | **Symmetric Role Cloning** | Copy-pasting DO/DON'T and Boundaries sections across roles with minimal changes, making every role indistinguishable | Every role must have at least 3 DON'T items that could not appear in any other role file. | | **STOP Point Omission** | Writing workflows as continuous sequences with no human checkpoints, enabling runaway autonomous execution | Every workflow stage must have an explicit STOP with a named human approver and the specific decision being made. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 3,
      "finding": "The Context Requirements section contains literal placeholder text '[Context item 1]' and '[Context item 2]' — this is an unfinished template shipped as a finished role. Required Skills table has no entries. An AI agent loading this role cannot determine what context files to load, what skills to activate, or what a first task looks like. The Iteration Protocol exists but is abstract. There is no example of what a completed template output looks like, no quality gate criteria an AI can self-check against, and no definition of what 'requirements gathered' means operationally.",
      "example_rewrite": "Context Requirements section should read: | Required Context | | --- | | organizational-charter.md — Must be loaded before any template work begins. Used to validate all role references. | | template-standard-checklist.md — The 11-section quality checklist used to validate every output. | | existing-role-library/ — Directory of current role files. Used to check for boundary conflicts and ensure new roles don't duplicate existing ones. | Required Skills: | Skill File | When to Load | | role-writing-guide.md | Load at session start for any template creation task | | yaml-config-patterns.md | Load when writing deployment configurations | | story-portal-context.md | Load when creating roles for Story Portal projects |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 2,
      "finding": "The Story Portal appendix lists four role categories (Platform, Creative, Festival, Community) and three domain elements (audio recording, festival ops, community) with no actionable specifics. There is no information about what makes a Story Portal role template different from a generic role template, what unique constraints apply (e.g., audio workflow integration, festival scheduling dependencies), which roles have already been created vs. are pending, or what the priority order means in practice. This appendix could be copy-pasted into any project with a word-find-replace.",
      "example_rewrite": "Replace the generic table with actionable Story Portal specifics: **Story Portal Template Constraints:** All Story Portal role templates must include an Audio Context block specifying how the role interacts with recorded story assets (read-only, contributes metadata, triggers recording workflow, or no interaction). Festival roles must include a Season Dependency field indicating which festival calendar phases activate or suspend the role. **Current Template Gaps (as of v1.0):** Festival Stage Manager role — not yet created, blocking audio recording workflow. Community Story Curator — draft exists, pending Quality Assurance Auditor review. **Story Portal-Specific Anti-Pattern:** Do not create roles that assume synchronous human availability during festival live events — all Story Portal roles operating during festival windows must have async fallback workflows defined."
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 4-5 Role Engineer-specific failure modes. This role is responsible for the quality of every other role in the system — its own failure modes (charter hallucination, philosophy laundering, symmetric role cloning, missing STOP points) are high-leverage defects that cascade across the entire workforce. Without this section, the role file violates its own template standard and ships without the most operationally critical content."
}
```