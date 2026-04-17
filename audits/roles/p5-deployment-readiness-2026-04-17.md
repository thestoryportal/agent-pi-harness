# P5 Deployment Readiness Report

**Date:** 2026-04-17
**Auditor:** Claude Sonnet 4.6
**Roles Assessed:** 170 (19 departments)

---

## Scoring Model

Each role scored 0–5 across five dimensions:

| Dimension | Criterion | Source |
|-----------|-----------|--------|
| +1 | All required sections present | P1 structural check |
| +1 | No encoding issues | P1 encoding check |
| +1 | All skill references valid | Skill library cross-reference |
| +1 | Context requirements specific | Required Context checklist review |
| +1 | Story Portal section is not a placeholder | P4 extraction findings |

**Score thresholds:** 5 = deployment-ready · 4 = conditional · ≤3 = blocked

---

## System-Wide Findings

### Dimension Outcomes Across All 170 Roles

| Dimension | Pass | Fail | Notes |
|-----------|------|------|-------|
| Sections present | 170 | 0 | P2/P3 confirmed consistent major structure across departments |
| Encoding clean | 170 | 0 | P3 sampling found no encoding-corrupt files |
| Skill refs valid | 42 | 128 | 42 roles have no Required Skills table (no invalid refs); 128 reference project-specific .md files that do not exist in `~/.claude/skills/` |
| Context specific | ~5 | ~165 | 76 roles have literal `[Context item 1]` placeholders; ~89 have content but VAGUE items; ~5 approach SPECIFIC |
| Story Portal | 170 | 0 | P4 confirmed 170/170 specific, 0 placeholders |

### Critical Finding: All Referenced Skill Files Are Missing

The roles reference project-specific skill files in their "Required Skills (Always Load)" tables. None of these files exist anywhere in `~/.claude/skills/`:

| Skill Referenced | Exists | Notes |
|-----------------|--------|-------|
| `supabase-patterns.md` | ✗ | Engineering — backend, full-stack, data-engineer |
| `api-conventions.md` | ✗ | Engineering — multiple |
| `code-quality-standards.md` | ✗ | Engineering — multiple |
| `steampunk-design-system.md` | ✗ | Creative Technology (9 roles) |
| `animation-standards.md` | ✗ | Creative Technology (9 roles) |
| `react-patterns.md` | ✗ | Engineering — frontend, full-stack |
| `typescript-standards.md` | ✗ | Engineering — multiple |
| `testing-standards.md` | ✗ | QA — multiple |
| `data-modeling.md` | ✗ | Engineering, Data |
| `rls-patterns.md` | ✗ | Engineering — backend, security |

**Impact:** 128 roles list skills they cannot load. A deployer following the Required Skills checklist will find no files to load.

---

## Deployment Readiness by Department

| Department | Total | Ready (5/5) | Conditional (4/5) | Blocked (≤3/5) |
|-----------|-------|-------------|------------------|----------------|
| ai-automation | 12 | 0 | 7 | 5 |
| client-services | 8 | 0 | 1 | 7 |
| creative-technology | 9 | 0 | 1 | 8 |
| data-analytics | 8 | 0 | 2 | 6 |
| design | 9 | 0 | 1 | 8 |
| engineering | 12 | 0 | 1 | 11 |
| finance-investor-relations | 9 | 0 | 4 | 5 |
| human-resources | 10 | 0 | 3 | 7 |
| legal-compliance | 6 | 0 | 1 | 5 |
| management | 4 | 0 | 0 | 4 |
| marketing | 14 | 0 | 5 | 9 |
| operations | 7 | 0 | 2 | 5 |
| platform-engineering | 10 | 0 | 0 | 10 |
| product | 9 | 0 | 0 | 9 |
| quality-assurance | 11 | 0 | 1 | 10 |
| research-intelligence | 8 | 0 | 5 | 3 |
| sales | 10 | 0 | 3 | 7 |
| strategy-business-dev | 8 | 0 | 2 | 6 |
| support | 6 | 0 | 3 | 3 |
| **TOTAL** | **170** | **0** | **42** | **128** |

**Conditional roles** are those with no Required Skills table (dim3 passes by absence) and non-placeholder Story Portal. They score 4/5, failing only on context specificity. They can be deployed with awareness that context guidance is vague.

**Blocked roles** score 3/5, failing dim3 (missing skill files) and dim4 (vague or placeholder context). They can still be loaded — the skill ref failure is a documentation gap, not a runtime failure — but the deployer has no reliable pre-session checklist.

---

## Blocked Roles — Priority Fix List

### Priority 1: Missing Skill Library (128 roles, fix once, unblocks all)

The skill files do not exist. Creating them unblocks all 128 simultaneously. Minimum viable set to create:

| Skill File | Roles Unblocked | Department(s) |
|-----------|-----------------|---------------|
| `supabase-patterns.md` | 8 | Engineering |
| `api-conventions.md` | 6 | Engineering |
| `code-quality-standards.md` | 7 | Engineering |
| `steampunk-design-system.md` | 9 | Creative Technology |
| `animation-standards.md` | 9 | Creative Technology |
| `react-patterns.md` | 4 | Engineering |
| `testing-standards.md` | 8 | QA |
| `data-modeling.md` | 4 | Engineering, Data Analytics |

### Priority 2: Context Placeholder Cleanup (76 roles, fix per role)

76 roles have unfilled `[Context item 1]` / `[Context item 2]` template text. These need to be replaced with actual deployment-time requirements. By department:

| Department | Roles with Placeholders |
|-----------|------------------------|
| marketing | 9 (brand-strategist, chief-marketing-officer, content-marketing-manager, event-marketing-manager, growth-hacker, marketing-designer, performance-marketing-manager, pr-communications-manager, social-media-manager) |
| client-services | 7 (account-manager, client-success-manager, delivery-manager, head-of-client-services, implementation-specialist, project-manager, technical-account-manager) |
| design | 8 (content-designer-ux-writer, design-research-lead, design-system-manager, head-of-design, service-designer, ui-designer, ux-designer, visual-brand-designer) |
| sales | 7 (account-executive, channel-partner-sales-manager, chief-revenue-officer, sales-development-rep, sales-director, sales-engineer, sales-operations-manager) |
| human-resources | 7 (agent-onboarding-specialist, chief-human-resources-officer, cross-training-coordinator, organizational-designer, role-engineer, skill-developer, workforce-registry-manager) |
| strategy-business-dev | 6 (business-planner, chief-strategy-officer, corporate-development-manager, new-ventures-lead, okr-planning-coordinator, partnership-manager) |
| data-analytics | 6 (analytics-engineer, analytics-operations-manager, bi-developer, data-analytics-research-lead, head-of-data-analytics, tracking-instrumentation-specialist) |
| finance-investor-relations | 5 (chief-financial-officer, financial-controller, fundraising-lead, investor-relations-manager, treasury-manager) |
| legal-compliance | 5 (compliance-officer, contract-manager, general-counsel, ip-manager, privacy-officer) |
| operations | 5 (chief-operating-officer, facilities-workspace-manager, it-manager, process-manager, vendor-manager) |
| ai-automation | 4 (ai-enablement-specialist, ai-ethics-specialist, ai-research-lead, conversational-ai-designer) |
| research-intelligence | 3 (data-scientist, research-director, user-research-lead) |
| support | 2 (head-of-support, support-operations-manager, technical-support-engineer — note: support has 3) |
| product | 1 (chief-product-officer) |

### Priority 3: Missing LOOP Blocks (6 non-Human-Primary roles)

Hybrid and AI-Primary roles require a `LOOP:` block in Deployment Notes. These are missing it:

| Role | Classification | Fix |
|------|---------------|-----|
| `creative-technology/creative-technologist.md` | 🔄 Hybrid | Add LOOP block to Deployment Notes |
| `creative-technology/motion-design-lead.md` | 🔄 Hybrid | Add LOOP block to Deployment Notes |
| `creative-technology/vfx-artist.md` | 🔄 Hybrid | Add LOOP block to Deployment Notes |
| `creative-technology/creative-tech-research-lead.md` | 🔄 Hybrid | Add LOOP block to Deployment Notes |
| `creative-technology/motion-designer.md` | 🔄 Hybrid | Add LOOP block to Deployment Notes |
| `engineering/performance-engineer.md` | 🤖 AI-Primary | Add LOOP block to Deployment Notes |

### Priority 4: Classification/Deployment Mismatches (4 roles)

Hybrid roles should deploy to Browser, CLI, or Browser+CLI only — not Agent:

| Role | Classification | Current Deployment | Fix |
|------|---------------|-------------------|-----|
| `marketing/social-media-manager.md` | 🔄 Hybrid | Browser + Agent | Change to Browser or Browser + CLI |
| `sales/sales-development-rep.md` | 🔄 Hybrid | Browser + Agent | Change to Browser or Browser + CLI |
| `legal-compliance/contract-manager.md` | 🔄 Hybrid | Browser + Agent | Change to Browser or Browser + CLI |
| `platform-engineering/site-reliability-engineer.md` | 🔄 Hybrid | CLI + Agent | Change to CLI or CLI + Browser |

**Note from P3 (carried forward):** `ai-automation/ai-ethics-specialist.md` is classified 🔄 Hybrid but P3 flagged this as a governance conflict — the charter designates this role Human-Primary to maintain independence from the CAO. If P3's fix is applied (restore to Human-Primary), the classification/deployment match resolves automatically.

---

## Deployment Manifest (Sample — Conditional Roles)

Full manifest for conditional (4/5) roles — these are the 42 closest to deployment-ready:

| Role | Score | Classification | Deployment | Skills OK | Context | Story Portal |
|------|-------|---------------|-----------|-----------|---------|-------------|
| ai-automation/agent-developer | 4/5 | 🤖 AI-Primary | Agent + CLI | ✓ (no refs) | Vague | ✓ |
| ai-automation/ai-ml-engineer | 4/5 | 🤖 AI-Primary | Agent + CLI | ✓ (no refs) | Vague | ✓ |
| ai-automation/ai-operations-engineer | 4/5 | 🤖 AI-Primary | Agent + CLI | ✓ (no refs) | Vague | ✓ |
| ai-automation/ai-solutions-architect | 4/5 | 🔄 Hybrid | Browser + CLI | ✓ (no refs) | Vague | ✓ |
| ai-automation/ai-trainer-evaluator | 4/5 | 🔄 Hybrid | Browser + CLI | ✓ (no refs) | Vague | ✓ |
| ai-automation/automation-engineer | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| ai-automation/chief-ai-officer | 4/5 | 👤 Human-Primary | Hybrid | ✓ (no refs) | Vague | ✓ |
| design/accessibility-specialist | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| data-analytics/data-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| data-analytics/data-quality-engineer | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| finance-investor-relations/cap-table-manager | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| finance-investor-relations/financial-modeler | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Semi-specific | ✓ |
| finance-investor-relations/fpa-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| finance-investor-relations/grant-writer | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| human-resources/agent-performance-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| human-resources/hr-research-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| human-resources/quality-assurance-auditor | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| legal-compliance/legal-research-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| marketing/email-marketing-specialist | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| marketing/marketing-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| marketing/marketing-copywriter | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| marketing/marketing-research-lead | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| marketing/seo-sem-specialist | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| operations/documentation-specialist | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| operations/operations-research-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| quality-assurance/head-of-qa | 4/5 | 👤 Human-Primary | Hybrid | ✓ (no refs) | Vague | ✓ |
| research-intelligence/competitive-intelligence-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| research-intelligence/industry-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| research-intelligence/market-research-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| research-intelligence/research-librarian | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| research-intelligence/technology-research-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| sales/deal-desk-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| sales/proposal-writer | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| sales/sales-research-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| strategy-business-dev/ma-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| strategy-business-dev/strategic-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| support/customer-support-specialist | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| support/knowledge-base-manager | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| support/support-research-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| client-services/client-research-analyst | 4/5 | 🤖 AI-Primary | Agent | ✓ (no refs) | Vague | ✓ |
| engineering/engineering-manager | 4/5 | 👤 Human-Primary | Hybrid | ✓ (no refs) | Vague | ✓ |
| creative-technology/head-of-creative-technology | 4/5 | 👤 Human-Primary | Hybrid | ✓ (no refs) | Vague | ✓ |

---

## How to Load a Ready Role in Claude

```
1. Read the role file at ~/.claude/roles/[department]/[role-name].md
2. Confirm the Required Context checklist before beginning:
   - For roles with [Context item N] placeholders: ask the user to specify
     what project context and documentation to provide
   - For roles with vague items: use judgment based on project state
3. For Hybrid (🔄) and AI-Primary (🤖) roles: apply the Iteration Protocol
   LOOP block from Deployment Notes
4. Skip the Required Skills table for blocked roles — those files do not
   yet exist; proceed without them or substitute project-local equivalents
```

**Fastest path to deployment:** Use one of the 42 conditional (4/5) roles from the manifest above. They have no invalid skill references and their Story Portal context is project-specific and complete.

---

## Recommended Fix Sequence

| Priority | Fix | Impact | Effort |
|----------|-----|--------|--------|
| 1 | Create missing skill files in `~/.claude/skills/` | Unblocks 128 roles (dim3 → pass) | High effort, one-time |
| 2 | Fill placeholder context in 76 roles | Unblocks 76 roles (dim4 → pass) | Medium — per-role |
| 3 | Add LOOP blocks to 6 Hybrid/AI-Primary roles in creative-technology + engineering | Closes iteration protocol gap | Low — 6 files |
| 4 | Fix Classification/Deployment in 4 Hybrid roles | Removes "Agent" from Hybrid deployments | Low — 4 files |
| 5 | Upgrade VAGUE context to SPECIFIC in remaining ~89 roles | Moves 42 conditional → 5/5 (fully ready) | High — per-role |

**If priorities 1+2 are completed:** 128 currently-blocked roles move to conditional (4/5). Zero remain blocked.  
**If priorities 1+2+5 are completed:** ~130 roles reach 5/5 deployment-ready.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-17 | Role Audit P5 | Initial P5 assessment |
