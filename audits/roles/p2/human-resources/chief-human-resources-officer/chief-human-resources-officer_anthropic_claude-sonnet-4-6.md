```json
{
  "role": "chief-human-resources-officer",
  "department": "human-resources",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 3,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All six principles are generic HR platitudes that could appear in any HR handbook. 'Continuous Optimization' and 'Quality Through Design' carry no specific meaning in an AI-native workforce context. None of the principles address the unique tension of managing AI agents as workforce members, handling role versioning, or balancing human oversight against AI autonomy — the actual hard problems this CHRO faces.",
      "example_rewrite": "Replace generic principles with role-specific ones. Example: 'Role Debt Is Workforce Debt — Vague or outdated role templates degrade every agent that loads them; the CHRO treats template maintenance as a first-class operational obligation, not a backlog item.' Or: 'Classification Integrity Over Convenience — Mislabeling a role Human-Primary vs AI-Primary to avoid design work creates downstream failures; the CHRO enforces correct classification even when stakeholders push for shortcuts.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs name broad categories, not actual artifacts or specific named roles from the charter. 'Strategic direction' from CEO and 'Role requirements' from Department Heads are non-artifacts — they describe conversations, not deliverables. The 'Delivers To: All Departments' pattern is explicitly called out in the template standard as a vague anti-pattern. No artifact format, file type, or structured output is named anywhere.",
      "example_rewrite": "Specify artifact name, format, and receiving role. Example: 'Delivers To: Project Manager | Artifact: Agent Deployment Package (project-context.md + role-config.yaml listing selected CLAUDE.md templates, context injections, and activation sequence) | Trigger: Project kickoff approval from CEO.' And: 'Receives From: Chief AI Officer | Artifact: Agent Capability Report (quarterly .md doc listing new model capabilities, deprecated skills, and recommended role updates).'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There are no anti-patterns section in this role file at all — the section is entirely absent. The DO/DON'T boundary list exists but functions as scope definition, not behavioral anti-patterns. The template standard explicitly requires 3-5 role-specific anti-patterns. The closest thing present ('Don't set business strategy') is a boundary rule, not a failure mode pattern unique to how a CHRO operating in an AI-native workforce actually goes wrong.",
      "example_rewrite": "Add a dedicated Anti-Patterns section. Example: 'Anti-Pattern: Role Template Proliferation Without Registry Hygiene — Creating new role templates for every edge case without deprecating outdated versions causes agents to load stale context. CHRO must enforce a one-in-one-reviewed policy: no new template merges without a registry audit. Anti-Pattern: Deploying Agents Without Context Injection — Activating a role template without attaching project-specific context produces generic output; CHRO must verify context packages are attached before marking deployment active.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Context Requirements section is entirely unfilled — placeholder text '[Context item 1]' and '[skill-name.md]' was never completed. This is a critical failure: an AI agent loading this role cannot determine what skills to load or what context is required to begin work. The workflows have STOP points, which is positive, but without populated context requirements, the role is operationally incomplete. The Human-Primary classification also means AI assistance is undefined beyond four vague bullet points.",
      "example_rewrite": "Populate Context Requirements with specifics. Example: 'Required Context: [ ] organizational-charter.md — needed to validate role references and classification | [ ] workforce-registry.md — current agent catalog for gap analysis | [ ] active-project-list.md — for deployment workflow trigger awareness. Required Skills: | org-design-frameworks.md | When: Organizational Design workflow step 1 | | role-template-standards.md | When: Any role engineering activity | | ai-workforce-metrics.md | When: Effectiveness review in Workflow 1 step 4'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix lists four generic workforce areas (Festival Operations, Platform Development, Community, Creative) without naming a single actual role that needs to be staffed, a specific deployment gap, or a concrete seasonal staffing trigger. 'Festival surge' as a consideration with 'Seasonal staffing' as the application provides no actionable guidance. No existing Story Portal roles are named, no workforce gaps are identified, and no specific artifacts relevant to Story Portal operations are mentioned.",
      "example_rewrite": "Replace generic tables with specific Story Portal workforce intelligence. Example: 'Festival Surge Protocol: Sixty days before each festival event, CHRO initiates Role Deployment Workflow for the following roles: Festival Operations Manager, Community Engagement Specialist, Audio Story Producer. Context package must include festival-brief.md and venue-logistics.md. Peak staffing window is T-14 days to T+3 days. Current gap as of v1.0: no Festival Operations Manager role template exists — creation is Priority 1 backlog item assigned to CHRO.'"
    }
  ],
  "top_improvement": "Complete the Anti-Patterns section and populate Context Requirements — the anti-patterns section is entirely missing (a template standard requirement), and the placeholder context fields mean no AI agent can operationally load this role. These two gaps make the role file functionally incomplete regardless of the quality of other sections."
}
```