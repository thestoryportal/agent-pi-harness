# Role-JD Enrichment Match List - 2026-04-17

Durable artifact for the role-enrichment pipeline. Pairs each role template at `~/.claude/roles/<dept>/<file>.md` with the most relevant job descriptions in `/Users/robertrhu/Projects/global-agent-assets/Job Descriptions/`. Downstream enrichment agents should consume this file without re-doing the enumeration.

**Matching rules (applied programmatically, then curated):**

- Names normalized: lowercase, parenthetical acronyms dropped, non-alphanumerics split into tokens, common synonyms expanded (`ml` > `machine learning`, `cto` > `chief technology officer`, etc.), `developer` and `engineer` canonicalized as equivalent.
- Level tokens (`junior`/`senior`/`staff`/`principal`/`lead`/`intern`) are stripped from the core fingerprint so seniority variants collapse.
- Generic role-shape tokens (`manager`/`specialist`/`analyst`/`officer`/`administrator`/`coordinator`/`lead`/`director`/`representative`/`associate`/`assistant`/`architect`/`chief`/`head`/`vice`/`president`) do not count as meaningful overlap on their own.
- **STRONG** = core fingerprints identical after the normalizations above.
- **GOOD** = one non-generic token differs, OR one side adds specialization to a shared stem (`ai engineer` subset of `ai ml engineer`).
- **WEAK** = curated domain-adjacent pair outside the token matcher's reach (e.g., CI/CD Engineer > DevOps Engineer, Accessibility Specialist > UX Designer). Useful for enrichment but confirm before copying content.
- When the same JD exists in multiple source folders, the `role-descriptions/` version is preferred over `role-descriptions-2/` and `role-descriptions-3/`. Dupes with identical normalized core are collapsed to one row per tier.
- **No fan-out cap.** All matches are included per tier. Roles that match many specialization variants (e.g., `product-manager.md` maps to AI / B2B / Platform / Growth variants) keep every pair so downstream agents can pick.

## Summary

- Role files scanned: **170**
- Roles with at least one match: **170**
- Roles with zero matches: **0**
- Total match pairs: **369**
  - STRONG: 57
  - GOOD: 177
  - WEAK: 135
- Roles with multiple matches: **118**

## Match Table

Paths are relative: role paths are under `~/.claude/roles/`; JD paths are under `/Users/robertrhu/Projects/global-agent-assets/Job Descriptions/`.

| Department | Role File | JD Path | Tier | Notes |
|------------|-----------|---------|------|-------|
| ai-automation | `ai-automation/agent-developer.md` | `role-descriptions/AI & Emerging Roles/Generative AI Developer.md` | WEAK | domain-adjacent; review before enrichment |
| ai-automation | `ai-automation/agent-developer.md` | `role-descriptions/Technology/AI Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| ai-automation | `ai-automation/agent-developer.md` | `role-descriptions/Technology/Software Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| ai-automation | `ai-automation/ai-enablement-specialist.md` | `role-descriptions/AI & Emerging Roles/AI Implementation Specialist.md` | WEAK | domain-adjacent; review before enrichment |
| ai-automation | `ai-automation/ai-enablement-specialist.md` | `role-descriptions/AI & Emerging Roles/AI Trainer.md` | WEAK | domain-adjacent; review before enrichment |
| ai-automation | `ai-automation/ai-ethics-specialist.md` | `role-descriptions-2/engineering/ai-ethics-researcher.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/ai-ethics-specialist.md` | `role-descriptions/AI & Emerging Roles/AI Ethics Officer.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/ai-ml-engineer.md` | `role-descriptions/Technology/AI Engineer.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/ai-ml-engineer.md` | `role-descriptions/Technology/Machine Learning Engineer.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/ai-operations-engineer.md` | `role-descriptions-2/engineering/operations-engineer.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/ai-operations-engineer.md` | `role-descriptions-2/information-technology/ai-operations-manager.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/ai-operations-engineer.md` | `role-descriptions/Technology/AI Engineer.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/ai-research-lead.md` | `role-descriptions-2/engineering/ai-research-scientist.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/ai-solutions-architect.md` | `role-descriptions-2/engineering/solutions-architect.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/ai-solutions-architect.md` | `role-descriptions-2/information-technology/ai-architect.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/ai-trainer-evaluator.md` | `role-descriptions/AI & Emerging Roles/AI Trainer.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/automation-engineer.md` | `role-descriptions/Technology/QA Automation Engineer.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/chief-ai-officer.md` | `role-descriptions/Executive/Chief AI Officer (CAIO).md` | STRONG | direct title match |
| ai-automation | `ai-automation/conversational-ai-designer.md` | `role-descriptions/AI & Emerging Roles/Conversational AI Designer.md` | STRONG | direct title match |
| ai-automation | `ai-automation/conversational-ai-designer.md` | `role-descriptions-2/design/junior-designer.md` | GOOD | specialization or synonym |
| ai-automation | `ai-automation/prompt-engineer.md` | `role-descriptions-2/information-technology/prompt-engineer.md` | STRONG | direct title match |
| client-services | `client-services/account-manager.md` | `role-descriptions/Sales/Account Manager.md` | STRONG | direct title match |
| client-services | `client-services/account-manager.md` | `role-descriptions-2/customer-service/technical-account-manager.md` | GOOD | specialization or synonym |
| client-services | `client-services/account-manager.md` | `role-descriptions-2/marketing/digital-account-manager.md` | GOOD | specialization or synonym |
| client-services | `client-services/account-manager.md` | `role-descriptions/Sales/Key Account Manager.md` | GOOD | specialization or synonym |
| client-services | `client-services/account-manager.md` | `role-descriptions/Sales/National Account Manager.md` | GOOD | specialization or synonym |
| client-services | `client-services/client-research-analyst.md` | `role-descriptions-2/marketing/market-research-analyst.md` | WEAK | domain-adjacent; review before enrichment |
| client-services | `client-services/client-research-analyst.md` | `role-descriptions/Customer Service/Customer Experience Analyst.md` | WEAK | domain-adjacent; review before enrichment |
| client-services | `client-services/client-success-manager.md` | `role-descriptions/Sales/Account Manager.md` | WEAK | domain-adjacent; review before enrichment |
| client-services | `client-services/client-success-manager.md` | `role-descriptions/Sales/Customer Success Manager.md` | WEAK | domain-adjacent; review before enrichment |
| client-services | `client-services/delivery-manager.md` | `role-descriptions/Operations/Program Manager.md` | WEAK | domain-adjacent; review before enrichment |
| client-services | `client-services/delivery-manager.md` | `role-descriptions/Operations/Project Manager.md` | WEAK | domain-adjacent; review before enrichment |
| client-services | `client-services/head-of-client-services.md` | `role-descriptions/Customer Service/Director of Customer Service.md` | WEAK | domain-adjacent; review before enrichment |
| client-services | `client-services/head-of-client-services.md` | `role-descriptions/Customer Service/VP of Customer Service.md` | WEAK | domain-adjacent; review before enrichment |
| client-services | `client-services/implementation-specialist.md` | `role-descriptions/AI & Emerging Roles/AI Implementation Specialist.md` | GOOD | specialization or synonym |
| client-services | `client-services/project-manager.md` | `role-descriptions/Operations/Project Manager.md` | STRONG | direct title match |
| client-services | `client-services/project-manager.md` | `role-descriptions-2/administrative/assistant-project-manager.md` | GOOD | specialization or synonym |
| client-services | `client-services/project-manager.md` | `role-descriptions-2/marketing/digital-project-manager.md` | GOOD | specialization or synonym |
| client-services | `client-services/project-manager.md` | `role-descriptions-3/executive-management/architectural-project-manager.md` | GOOD | specialization or synonym |
| client-services | `client-services/project-manager.md` | `role-descriptions/Creative/Creative Project Manager.md` | GOOD | specialization or synonym |
| client-services | `client-services/project-manager.md` | `role-descriptions/Operations/Construction Project Manager.md` | GOOD | specialization or synonym |
| client-services | `client-services/project-manager.md` | `role-descriptions/Operations/IT Project Manager.md` | GOOD | specialization or synonym |
| client-services | `client-services/project-manager.md` | `role-descriptions/Operations/Technical Project Manager.md` | GOOD | specialization or synonym |
| client-services | `client-services/technical-account-manager.md` | `role-descriptions-2/customer-service/technical-account-manager.md` | STRONG | direct title match |
| client-services | `client-services/technical-account-manager.md` | `role-descriptions/Sales/Account Manager.md` | GOOD | specialization or synonym |
| creative-technology | `creative-technology/3d-artist-generalist.md` | `role-descriptions/Creative/3D Artist.md` | GOOD | specialization or synonym |
| creative-technology | `creative-technology/animation-specialist.md` | `role-descriptions-2/media/animator.md` | GOOD | specialization or synonym |
| creative-technology | `creative-technology/creative-tech-research-lead.md` | `role-descriptions/Creative/Creative Director.md` | WEAK | domain-adjacent; review before enrichment |
| creative-technology | `creative-technology/creative-tech-research-lead.md` | `role-descriptions/Product/UX Researcher.md` | WEAK | domain-adjacent; review before enrichment |
| creative-technology | `creative-technology/creative-technologist.md` | `role-descriptions/Creative/Creative Director.md` | WEAK | domain-adjacent; review before enrichment |
| creative-technology | `creative-technology/creative-technologist.md` | `role-descriptions/Creative/Digital Designer.md` | WEAK | domain-adjacent; review before enrichment |
| creative-technology | `creative-technology/head-of-creative-technology.md` | `role-descriptions/Creative/Chief Creative Officer.md` | WEAK | domain-adjacent; review before enrichment |
| creative-technology | `creative-technology/head-of-creative-technology.md` | `role-descriptions/Creative/Creative Director.md` | WEAK | domain-adjacent; review before enrichment |
| creative-technology | `creative-technology/motion-design-lead.md` | `role-descriptions/Creative/Creative Director.md` | WEAK | domain-adjacent; review before enrichment |
| creative-technology | `creative-technology/motion-design-lead.md` | `role-descriptions/Creative/Motion Graphics Designer.md` | WEAK | domain-adjacent; review before enrichment |
| creative-technology | `creative-technology/motion-designer.md` | `role-descriptions-2/design/junior-designer.md` | GOOD | specialization or synonym |
| creative-technology | `creative-technology/motion-designer.md` | `role-descriptions/Creative/Motion Graphics Designer.md` | GOOD | specialization or synonym |
| creative-technology | `creative-technology/vfx-artist.md` | `role-descriptions/Creative/3D Artist.md` | WEAK | domain-adjacent; review before enrichment |
| creative-technology | `creative-technology/vfx-artist.md` | `role-descriptions/Creative/Motion Graphics Designer.md` | WEAK | domain-adjacent; review before enrichment |
| creative-technology | `creative-technology/webgl-engineer.md` | `role-descriptions-3/information-technology/web-developer.md` | GOOD | specialization or synonym |
| data-analytics | `data-analytics/analytics-engineer.md` | `role-descriptions-2/information-technology/bi-consultant.md` | WEAK | domain-adjacent; review before enrichment |
| data-analytics | `data-analytics/analytics-engineer.md` | `role-descriptions/Technology/Data Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| data-analytics | `data-analytics/analytics-operations-manager.md` | `role-descriptions-2/information-technology/analytics-manager.md` | GOOD | specialization or synonym |
| data-analytics | `data-analytics/analytics-operations-manager.md` | `role-descriptions/Operations/Operations Manager.md` | GOOD | specialization or synonym |
| data-analytics | `data-analytics/bi-developer.md` | `role-descriptions-2/information-technology/bi-(business-intelligence)-developer.md` | STRONG | direct title match |
| data-analytics | `data-analytics/bi-developer.md` | `role-descriptions-2/administrative/business-intelligence-analyst.md` | GOOD | specialization or synonym |
| data-analytics | `data-analytics/bi-developer.md` | `role-descriptions-2/information-technology/bi-consultant.md` | GOOD | specialization or synonym |
| data-analytics | `data-analytics/data-analyst.md` | `role-descriptions/Operations/Data Analyst.md` | STRONG | direct title match |
| data-analytics | `data-analytics/data-analyst.md` | `role-descriptions-2/information-technology/healthcare-data-analyst.md` | GOOD | specialization or synonym |
| data-analytics | `data-analytics/data-analyst.md` | `role-descriptions/Marketing/Marketing Data Analyst.md` | GOOD | specialization or synonym |
| data-analytics | `data-analytics/data-analytics-research-lead.md` | `role-descriptions-2/information-technology/lead-data-scientist.md` | WEAK | domain-adjacent; review before enrichment |
| data-analytics | `data-analytics/data-analytics-research-lead.md` | `role-descriptions/Technology/Data Scientist.md` | WEAK | domain-adjacent; review before enrichment |
| data-analytics | `data-analytics/data-quality-engineer.md` | `role-descriptions-3/engineering/quality-engineer.md` | GOOD | specialization or synonym |
| data-analytics | `data-analytics/data-quality-engineer.md` | `role-descriptions/Technology/Data Engineer.md` | GOOD | specialization or synonym |
| data-analytics | `data-analytics/head-of-data-analytics.md` | `role-descriptions-2/information-technology/analytics-manager.md` | WEAK | domain-adjacent; review before enrichment |
| data-analytics | `data-analytics/head-of-data-analytics.md` | `role-descriptions-2/information-technology/lead-data-engineer.md` | WEAK | domain-adjacent; review before enrichment |
| data-analytics | `data-analytics/tracking-instrumentation-specialist.md` | `role-descriptions-2/information-technology/analytics-manager.md` | WEAK | domain-adjacent; review before enrichment |
| data-analytics | `data-analytics/tracking-instrumentation-specialist.md` | `role-descriptions/Technology/Data Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| design | `design/accessibility-specialist.md` | `role-descriptions-2/design/ux-designer.md` | WEAK | domain-adjacent; review before enrichment |
| design | `design/accessibility-specialist.md` | `role-descriptions/Creative/Web Designer.md` | WEAK | domain-adjacent; review before enrichment |
| design | `design/content-designer-ux-writer.md` | `role-descriptions-2/design/ux-designer.md` | GOOD | specialization or synonym |
| design | `design/design-research-lead.md` | `role-descriptions/Product/Senior UI Designer.md` | WEAK | domain-adjacent; review before enrichment |
| design | `design/design-research-lead.md` | `role-descriptions/Product/UX Researcher.md` | WEAK | domain-adjacent; review before enrichment |
| design | `design/design-system-manager.md` | `role-descriptions-2/design/design-operations-manager.md` | WEAK | domain-adjacent; review before enrichment |
| design | `design/design-system-manager.md` | `role-descriptions/Product/Senior UI Designer.md` | WEAK | domain-adjacent; review before enrichment |
| design | `design/head-of-design.md` | `role-descriptions-2/design/design-operations-manager.md` | WEAK | domain-adjacent; review before enrichment |
| design | `design/head-of-design.md` | `role-descriptions/Creative/Creative Director.md` | WEAK | domain-adjacent; review before enrichment |
| design | `design/service-designer.md` | `role-descriptions-2/design/junior-designer.md` | GOOD | specialization or synonym |
| design | `design/ui-designer.md` | `role-descriptions/Product/Senior UI Designer.md` | STRONG | direct title match |
| design | `design/ui-designer.md` | `role-descriptions-2/design/junior-designer.md` | GOOD | specialization or synonym |
| design | `design/ui-designer.md` | `role-descriptions-2/design/ui-ux-designer.md` | GOOD | specialization or synonym |
| design | `design/ui-designer.md` | `role-descriptions-2/design/ux-designer.md` | GOOD | specialization or synonym |
| design | `design/ux-designer.md` | `role-descriptions-2/design/ux-designer.md` | STRONG | direct title match |
| design | `design/ux-designer.md` | `role-descriptions-2/design/junior-designer.md` | GOOD | specialization or synonym |
| design | `design/ux-designer.md` | `role-descriptions-2/design/ui-ux-designer.md` | GOOD | specialization or synonym |
| design | `design/ux-designer.md` | `role-descriptions/Product/Senior UI Designer.md` | GOOD | specialization or synonym |
| design | `design/ux-designer.md` | `role-descriptions/Product/UX Researcher.md` | GOOD | specialization or synonym |
| design | `design/visual-brand-designer.md` | `role-descriptions-2/design/brand-designer-and-illustrator.md` | GOOD | specialization or synonym |
| design | `design/visual-brand-designer.md` | `role-descriptions-2/design/junior-designer.md` | GOOD | specialization or synonym |
| design | `design/visual-brand-designer.md` | `role-descriptions-2/design/visual-designer.md` | GOOD | specialization or synonym |
| design | `design/visual-brand-designer.md` | `role-descriptions/Marketing/Brand Designer.md` | GOOD | specialization or synonym |
| engineering | `engineering/ai-ml-engineer.md` | `role-descriptions/Technology/AI Engineer.md` | GOOD | specialization or synonym |
| engineering | `engineering/ai-ml-engineer.md` | `role-descriptions/Technology/Machine Learning Engineer.md` | GOOD | specialization or synonym |
| engineering | `engineering/backend-developer.md` | `role-descriptions/Technology/Backend Developer.md` | STRONG | direct title match |
| engineering | `engineering/backend-developer.md` | `role-descriptions-2/information-technology/backend-javascript-developer.md` | GOOD | specialization or synonym |
| engineering | `engineering/backend-developer.md` | `role-descriptions/Technology/C# Backend Developer.md` | GOOD | specialization or synonym |
| engineering | `engineering/backend-developer.md` | `role-descriptions/Technology/Python Backend Developer.md` | GOOD | specialization or synonym |
| engineering | `engineering/chief-technology-officer.md` | `role-descriptions/Executive/Chief Technology Officer (CTO).md` | STRONG | direct title match |
| engineering | `engineering/data-engineer.md` | `role-descriptions/Technology/Data Engineer.md` | STRONG | direct title match |
| engineering | `engineering/data-engineer.md` | `role-descriptions-3/information-technology/big-data-engineer.md` | GOOD | specialization or synonym |
| engineering | `engineering/engineering-manager.md` | `role-descriptions-2/engineering/engineering-manager.md` | STRONG | direct title match |
| engineering | `engineering/engineering-manager.md` | `role-descriptions/AI & Emerging Roles/Prompt Engineering Manager.md` | GOOD | specialization or synonym |
| engineering | `engineering/engineering-research-lead.md` | `role-descriptions-2/engineering/enterprise-architect.md` | WEAK | domain-adjacent; review before enrichment |
| engineering | `engineering/engineering-research-lead.md` | `role-descriptions-2/information-technology/director-of-engineering.md` | WEAK | domain-adjacent; review before enrichment |
| engineering | `engineering/frontend-developer.md` | `role-descriptions/Technology/Frontend Developer.md` | STRONG | direct title match |
| engineering | `engineering/full-stack-developer.md` | `role-descriptions/Technology/Full Stack Developer.md` | STRONG | direct title match |
| engineering | `engineering/mobile-developer.md` | `role-descriptions/Technology/Mobile Developer.md` | STRONG | direct title match |
| engineering | `engineering/performance-engineer.md` | `role-descriptions-2/engineering/site-reliability-engineer.md` | WEAK | domain-adjacent; review before enrichment |
| engineering | `engineering/security-engineer.md` | `role-descriptions-2/information-technology/security-engineer.md` | STRONG | direct title match |
| engineering | `engineering/security-engineer.md` | `role-descriptions-3/information-technology/application-security-engineer.md` | GOOD | specialization or synonym |
| engineering | `engineering/solutions-architect.md` | `role-descriptions-2/engineering/solutions-architect.md` | STRONG | direct title match |
| finance-investor-relations | `finance-investor-relations/cap-table-manager.md` | `role-descriptions/Finance/Controller.md` | WEAK | domain-adjacent; review before enrichment |
| finance-investor-relations | `finance-investor-relations/cap-table-manager.md` | `role-descriptions/Finance/Financial Analyst.md` | WEAK | domain-adjacent; review before enrichment |
| finance-investor-relations | `finance-investor-relations/chief-financial-officer.md` | `role-descriptions/Executive/Chief Financial Officer (CFO).md` | STRONG | direct title match |
| finance-investor-relations | `finance-investor-relations/chief-financial-officer.md` | `role-descriptions-2/finance/nonprofit-cfo.md` | GOOD | specialization or synonym |
| finance-investor-relations | `finance-investor-relations/financial-controller.md` | `role-descriptions-2/finance/financial-controller.md` | STRONG | direct title match |
| finance-investor-relations | `finance-investor-relations/financial-controller.md` | `role-descriptions/Finance/Controller.md` | GOOD | specialization or synonym |
| finance-investor-relations | `finance-investor-relations/financial-modeler.md` | `role-descriptions/Finance/Financial Analyst.md` | WEAK | domain-adjacent; review before enrichment |
| finance-investor-relations | `finance-investor-relations/financial-modeler.md` | `role-descriptions/Finance/Senior Financial Analyst.md` | WEAK | domain-adjacent; review before enrichment |
| finance-investor-relations | `finance-investor-relations/fpa-analyst.md` | `role-descriptions/Finance/Financial Analyst.md` | GOOD | specialization or synonym |
| finance-investor-relations | `finance-investor-relations/fpa-analyst.md` | `role-descriptions/Finance/Financial Planning Analyst.md` | GOOD | specialization or synonym |
| finance-investor-relations | `finance-investor-relations/fundraising-lead.md` | `role-descriptions-2/administrative/fundraiser.md` | STRONG | direct title match |
| finance-investor-relations | `finance-investor-relations/grant-writer.md` | `role-descriptions-2/marketing/grant-writer.md` | STRONG | direct title match |
| finance-investor-relations | `finance-investor-relations/grant-writer.md` | `role-descriptions-2/media/writer.md` | GOOD | specialization or synonym |
| finance-investor-relations | `finance-investor-relations/investor-relations-manager.md` | `role-descriptions-2/marketing/communications-director.md` | WEAK | domain-adjacent; review before enrichment |
| finance-investor-relations | `finance-investor-relations/investor-relations-manager.md` | `role-descriptions/Finance/Financial Analyst.md` | WEAK | domain-adjacent; review before enrichment |
| finance-investor-relations | `finance-investor-relations/treasury-manager.md` | `role-descriptions-2/finance/financial-manager.md` | WEAK | domain-adjacent; review before enrichment |
| finance-investor-relations | `finance-investor-relations/treasury-manager.md` | `role-descriptions-2/finance/treasurer.md` | WEAK | domain-adjacent; review before enrichment |
| human-resources | `human-resources/agent-onboarding-specialist.md` | `role-descriptions-2/human-resources/onboarding-specialist.md` | GOOD | specialization or synonym |
| human-resources | `human-resources/agent-performance-analyst.md` | `role-descriptions-2/administrative/business-performance-analyst.md` | WEAK | domain-adjacent; review before enrichment |
| human-resources | `human-resources/agent-performance-analyst.md` | `role-descriptions-2/information-technology/ai-auditor.md` | WEAK | domain-adjacent; review before enrichment |
| human-resources | `human-resources/chief-human-resources-officer.md` | `role-descriptions-2/human-resources/chief-human-resources-officer-(chro).md` | STRONG | direct title match |
| human-resources | `human-resources/chief-human-resources-officer.md` | `role-descriptions-2/human-resources/hr-and-admin-officer.md` | GOOD | specialization or synonym |
| human-resources | `human-resources/chief-human-resources-officer.md` | `role-descriptions-2/human-resources/hr-officer.md` | GOOD | specialization or synonym |
| human-resources | `human-resources/cross-training-coordinator.md` | `role-descriptions-2/corporate-training/training-coordinator.md` | GOOD | specialization or synonym |
| human-resources | `human-resources/hr-research-analyst.md` | `role-descriptions-2/human-resources/hr-analyst.md` | GOOD | specialization or synonym |
| human-resources | `human-resources/organizational-designer.md` | `role-descriptions-2/design/junior-designer.md` | GOOD | specialization or synonym |
| human-resources | `human-resources/quality-assurance-auditor.md` | `role-descriptions-2/information-technology/qa-tester.md` | GOOD | specialization or synonym |
| human-resources | `human-resources/quality-assurance-auditor.md` | `role-descriptions-2/production/manager-of-quality-assurance.md` | GOOD | specialization or synonym |
| human-resources | `human-resources/quality-assurance-auditor.md` | `role-descriptions-2/production/quality-assurance-specialist.md` | GOOD | specialization or synonym |
| human-resources | `human-resources/quality-assurance-auditor.md` | `role-descriptions-3/finance-accounting/auditor.md` | GOOD | specialization or synonym |
| human-resources | `human-resources/quality-assurance-auditor.md` | `role-descriptions/Technology/QA Engineer.md` | GOOD | specialization or synonym |
| human-resources | `human-resources/role-engineer.md` | `role-descriptions-2/information-technology/junior-developer.md` | STRONG | direct title match |
| human-resources | `human-resources/skill-developer.md` | `role-descriptions-2/corporate-training/curriculum-designer.md` | WEAK | domain-adjacent; review before enrichment |
| human-resources | `human-resources/skill-developer.md` | `role-descriptions-2/human-resources/learning-and-development-specialist.md` | WEAK | domain-adjacent; review before enrichment |
| human-resources | `human-resources/skill-developer.md` | `role-descriptions-3/education-training/instructional-designer.md` | WEAK | domain-adjacent; review before enrichment |
| human-resources | `human-resources/workforce-registry-manager.md` | `role-descriptions-2/human-resources/workforce-manager.md` | GOOD | specialization or synonym |
| legal-compliance | `legal-compliance/compliance-officer.md` | `role-descriptions-2/administrative/contract-administrator.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/compliance-officer.md` | `role-descriptions-3/legal-compliance/legal-assistant.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/compliance-officer.md` | `role-descriptions-3/legal-compliance/paralegal.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/contract-manager.md` | `role-descriptions-2/administrative/contract-administrator.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/general-counsel.md` | `role-descriptions-2/administrative/contract-administrator.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/general-counsel.md` | `role-descriptions-3/legal-compliance/legal-assistant.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/general-counsel.md` | `role-descriptions-3/legal-compliance/paralegal.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/ip-manager.md` | `role-descriptions-2/administrative/contract-administrator.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/ip-manager.md` | `role-descriptions-3/legal-compliance/paralegal.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/legal-research-analyst.md` | `role-descriptions-3/legal-compliance/legal-assistant.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/legal-research-analyst.md` | `role-descriptions-3/legal-compliance/paralegal.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/privacy-officer.md` | `role-descriptions-2/administrative/contract-administrator.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/privacy-officer.md` | `role-descriptions-3/legal-compliance/legal-assistant.md` | WEAK | domain-adjacent; review before enrichment |
| legal-compliance | `legal-compliance/privacy-officer.md` | `role-descriptions-3/legal-compliance/paralegal.md` | WEAK | domain-adjacent; review before enrichment |
| management | `management/operations-coordinator.md` | `role-descriptions/Operations/Operations Coordinator.md` | STRONG | direct title match |
| management | `management/project-orchestrator.md` | `role-descriptions/Operations/Program Manager.md` | WEAK | domain-adjacent; review before enrichment |
| management | `management/project-orchestrator.md` | `role-descriptions/Operations/Project Manager.md` | WEAK | domain-adjacent; review before enrichment |
| management | `management/quality-coordinator.md` | `role-descriptions-2/information-technology/qa-tester.md` | WEAK | domain-adjacent; review before enrichment |
| management | `management/quality-coordinator.md` | `role-descriptions/AI & Emerging Roles/AI Quality Assurance Specialist.md` | WEAK | domain-adjacent; review before enrichment |
| management | `management/technical-coordinator.md` | `role-descriptions/Operations/Project Coordinator.md` | WEAK | domain-adjacent; review before enrichment |
| management | `management/technical-coordinator.md` | `role-descriptions/Operations/Technical Program Manager.md` | WEAK | domain-adjacent; review before enrichment |
| marketing | `marketing/brand-strategist.md` | `role-descriptions-2/marketing/brand-strategist.md` | STRONG | direct title match |
| marketing | `marketing/chief-marketing-officer.md` | `role-descriptions/Executive/Chief Marketing Officer (CMO).md` | STRONG | direct title match |
| marketing | `marketing/chief-marketing-officer.md` | `role-descriptions-2/marketing/marketing-intern.md` | GOOD | specialization or synonym |
| marketing | `marketing/chief-marketing-officer.md` | `role-descriptions-2/marketing/marketing-officer.md` | GOOD | specialization or synonym |
| marketing | `marketing/content-marketing-manager.md` | `role-descriptions/Marketing/Content Marketing Manager.md` | STRONG | direct title match |
| marketing | `marketing/content-marketing-manager.md` | `role-descriptions-2/marketing/content-manager.md` | GOOD | specialization or synonym |
| marketing | `marketing/content-marketing-manager.md` | `role-descriptions-2/marketing/content-marketing-intern.md` | GOOD | specialization or synonym |
| marketing | `marketing/content-marketing-manager.md` | `role-descriptions-2/marketing/director-of-content-marketing.md` | GOOD | specialization or synonym |
| marketing | `marketing/content-marketing-manager.md` | `role-descriptions-2/marketing/marketing-intern.md` | GOOD | specialization or synonym |
| marketing | `marketing/content-marketing-manager.md` | `role-descriptions/Marketing/Marketing Manager.md` | GOOD | specialization or synonym |
| marketing | `marketing/email-marketing-specialist.md` | `role-descriptions/Marketing/Email Marketing Specialist.md` | STRONG | direct title match |
| marketing | `marketing/email-marketing-specialist.md` | `role-descriptions-2/marketing/marketing-intern.md` | GOOD | specialization or synonym |
| marketing | `marketing/email-marketing-specialist.md` | `role-descriptions-2/marketing/marketing-specialist.md` | GOOD | specialization or synonym |
| marketing | `marketing/email-marketing-specialist.md` | `role-descriptions/Marketing/Email Marketing Manager.md` | GOOD | specialization or synonym |
| marketing | `marketing/event-marketing-manager.md` | `role-descriptions-2/marketing/marketing-intern.md` | GOOD | specialization or synonym |
| marketing | `marketing/event-marketing-manager.md` | `role-descriptions/Marketing/Event Marketing Specialist.md` | GOOD | specialization or synonym |
| marketing | `marketing/event-marketing-manager.md` | `role-descriptions/Marketing/Marketing Manager.md` | GOOD | specialization or synonym |
| marketing | `marketing/growth-hacker.md` | `role-descriptions/Marketing/Demand Generation Manager.md` | WEAK | domain-adjacent; review before enrichment |
| marketing | `marketing/growth-hacker.md` | `role-descriptions/Marketing/Growth Marketing Manager.md` | WEAK | domain-adjacent; review before enrichment |
| marketing | `marketing/marketing-analyst.md` | `role-descriptions/Marketing/Marketing Analyst.md` | STRONG | direct title match |
| marketing | `marketing/marketing-analyst.md` | `role-descriptions-2/marketing/marketing-intern.md` | GOOD | specialization or synonym |
| marketing | `marketing/marketing-analyst.md` | `role-descriptions/Marketing/Marketing Data Analyst.md` | GOOD | specialization or synonym |
| marketing | `marketing/marketing-copywriter.md` | `role-descriptions-2/marketing/marketing-copywriter.md` | STRONG | direct title match |
| marketing | `marketing/marketing-copywriter.md` | `role-descriptions-2/marketing/marketing-intern.md` | GOOD | specialization or synonym |
| marketing | `marketing/marketing-copywriter.md` | `role-descriptions/Creative/Copywriter.md` | GOOD | specialization or synonym |
| marketing | `marketing/marketing-designer.md` | `role-descriptions-2/design/junior-designer.md` | GOOD | specialization or synonym |
| marketing | `marketing/marketing-designer.md` | `role-descriptions-2/marketing/marketing-intern.md` | GOOD | specialization or synonym |
| marketing | `marketing/marketing-research-lead.md` | `role-descriptions-2/marketing/marketing-intern.md` | GOOD | specialization or synonym |
| marketing | `marketing/performance-marketing-manager.md` | `role-descriptions-2/marketing/marketing-intern.md` | GOOD | specialization or synonym |
| marketing | `marketing/performance-marketing-manager.md` | `role-descriptions/Marketing/Marketing Manager.md` | GOOD | specialization or synonym |
| marketing | `marketing/pr-communications-manager.md` | `role-descriptions-2/public-relations/public-relations-intern.md` | GOOD | specialization or synonym |
| marketing | `marketing/pr-communications-manager.md` | `role-descriptions-2/public-relations/public-relations-manager.md` | GOOD | specialization or synonym |
| marketing | `marketing/seo-sem-specialist.md` | `role-descriptions-2/marketing/junior-sem-seo-specialist.md` | STRONG | direct title match |
| marketing | `marketing/seo-sem-specialist.md` | `role-descriptions-2/marketing/search-engine-marketing-(sem)-specialist.md` | GOOD | specialization or synonym |
| marketing | `marketing/seo-sem-specialist.md` | `role-descriptions/Marketing/SEO Specialist.md` | GOOD | specialization or synonym |
| marketing | `marketing/social-media-manager.md` | `role-descriptions/Marketing/Social Media Manager.md` | STRONG | direct title match |
| marketing | `marketing/social-media-manager.md` | `role-descriptions-2/marketing/social-media-analyst.md` | GOOD | specialization or synonym |
| marketing | `marketing/social-media-manager.md` | `role-descriptions-2/marketing/social-media-coordinator.md` | GOOD | specialization or synonym |
| marketing | `marketing/social-media-manager.md` | `role-descriptions-2/marketing/social-media-copywriter.md` | GOOD | specialization or synonym |
| marketing | `marketing/social-media-manager.md` | `role-descriptions-2/marketing/social-media-strategist.md` | GOOD | specialization or synonym |
| marketing | `marketing/social-media-manager.md` | `role-descriptions/Marketing/Social Media Specialist.md` | GOOD | specialization or synonym |
| operations | `operations/chief-operating-officer.md` | `role-descriptions/Executive/Chief Operating Officer (COO).md` | STRONG | direct title match |
| operations | `operations/documentation-specialist.md` | `role-descriptions-2/administrative/documentation-specialist.md` | STRONG | direct title match |
| operations | `operations/facilities-workspace-manager.md` | `role-descriptions-3/operations-logistics/facilities-manager.md` | GOOD | specialization or synonym |
| operations | `operations/it-manager.md` | `role-descriptions-2/information-technology/it-manager.md` | STRONG | direct title match |
| operations | `operations/it-manager.md` | `role-descriptions-2/information-technology/it-operations-manager.md` | GOOD | specialization or synonym |
| operations | `operations/it-manager.md` | `role-descriptions/Operations/IT Project Manager.md` | GOOD | specialization or synonym |
| operations | `operations/operations-research-analyst.md` | `role-descriptions/Operations/Operations Analyst.md` | GOOD | specialization or synonym |
| operations | `operations/process-manager.md` | `role-descriptions-2/engineering/process-engineer.md` | WEAK | domain-adjacent; review before enrichment |
| operations | `operations/process-manager.md` | `role-descriptions/Operations/Operations Manager.md` | WEAK | domain-adjacent; review before enrichment |
| operations | `operations/vendor-manager.md` | `role-descriptions-2/administrative/procurement-specialist.md` | WEAK | domain-adjacent; review before enrichment |
| operations | `operations/vendor-manager.md` | `role-descriptions-3/operations-logistics/procurement-manager.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/cicd-engineer.md` | `role-descriptions/Technology/DevOps Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/database-administrator.md` | `role-descriptions/Technology/Database Administrator.md` | STRONG | direct title match |
| platform-engineering | `platform-engineering/developer-experience-engineer.md` | `role-descriptions/Creative/Technical Writer.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/developer-experience-engineer.md` | `role-descriptions/Technology/DevOps Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/devops-research-lead.md` | `role-descriptions-2/engineering/enterprise-architect.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/devops-research-lead.md` | `role-descriptions/Technology/DevOps Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/head-of-platform-engineering.md` | `role-descriptions-2/information-technology/director-of-engineering.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/head-of-platform-engineering.md` | `role-descriptions-2/information-technology/it-director.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/infrastructure-engineer.md` | `role-descriptions/Technology/Cloud Architect.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/infrastructure-engineer.md` | `role-descriptions/Technology/DevOps Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/infrastructure-engineer.md` | `role-descriptions/Technology/Google Cloud Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/release-manager.md` | `role-descriptions/Operations/Program Manager.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/release-manager.md` | `role-descriptions/Technology/DevOps Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/repository-manager.md` | `role-descriptions/Technology/DevOps Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| platform-engineering | `platform-engineering/security-operations-engineer.md` | `role-descriptions-2/engineering/operations-engineer.md` | GOOD | specialization or synonym |
| platform-engineering | `platform-engineering/security-operations-engineer.md` | `role-descriptions-2/information-technology/security-engineer.md` | GOOD | specialization or synonym |
| platform-engineering | `platform-engineering/site-reliability-engineer.md` | `role-descriptions-2/engineering/site-reliability-engineer.md` | STRONG | direct title match |
| product | `product/business-analyst.md` | `role-descriptions/Operations/Business Analyst.md` | STRONG | direct title match |
| product | `product/business-analyst.md` | `role-descriptions-2/administrative/business-intelligence-analyst.md` | GOOD | specialization or synonym |
| product | `product/business-analyst.md` | `role-descriptions-2/administrative/business-performance-analyst.md` | GOOD | specialization or synonym |
| product | `product/business-analyst.md` | `role-descriptions-2/information-technology/lead-business-systems-analyst.md` | GOOD | specialization or synonym |
| product | `product/business-analyst.md` | `role-descriptions/AI & Emerging Roles/AI Business Analyst.md` | GOOD | specialization or synonym |
| product | `product/chief-product-officer.md` | `role-descriptions/Executive/Chief Product Officer (CPO).md` | STRONG | direct title match |
| product | `product/competitive-product-analyst.md` | `role-descriptions/Product/Product Analyst.md` | GOOD | specialization or synonym |
| product | `product/product-analyst.md` | `role-descriptions/Product/Product Analyst.md` | STRONG | direct title match |
| product | `product/product-manager.md` | `role-descriptions/Product/Product Manager.md` | STRONG | direct title match |
| product | `product/product-manager.md` | `role-descriptions-2/marketing/product-partner-manager.md` | GOOD | specialization or synonym |
| product | `product/product-manager.md` | `role-descriptions/Marketing/Product Marketing Manager.md` | GOOD | specialization or synonym |
| product | `product/product-manager.md` | `role-descriptions/Product/AI Product Manager.md` | GOOD | specialization or synonym |
| product | `product/product-manager.md` | `role-descriptions/Product/Associate Product Manager.md` | GOOD | specialization or synonym |
| product | `product/product-manager.md` | `role-descriptions/Product/B2B Product Manager.md` | GOOD | specialization or synonym |
| product | `product/product-manager.md` | `role-descriptions/Product/B2C Product Manager.md` | GOOD | specialization or synonym |
| product | `product/product-manager.md` | `role-descriptions/Product/Group Product Manager.md` | GOOD | specialization or synonym |
| product | `product/product-manager.md` | `role-descriptions/Product/Growth Product Manager.md` | GOOD | specialization or synonym |
| product | `product/product-manager.md` | `role-descriptions/Product/Mobile Product Manager.md` | GOOD | specialization or synonym |
| product | `product/product-manager.md` | `role-descriptions/Product/Platform Product Manager.md` | GOOD | specialization or synonym |
| product | `product/product-manager.md` | `role-descriptions/Product/Technical Product Manager.md` | GOOD | specialization or synonym |
| product | `product/product-marketing-manager.md` | `role-descriptions/Marketing/Product Marketing Manager.md` | STRONG | direct title match |
| product | `product/product-marketing-manager.md` | `role-descriptions-2/marketing/lead-product-marketing-writer.md` | GOOD | specialization or synonym |
| product | `product/product-marketing-manager.md` | `role-descriptions-2/marketing/marketing-intern.md` | GOOD | specialization or synonym |
| product | `product/product-marketing-manager.md` | `role-descriptions-2/marketing/product-marketing-associate.md` | GOOD | specialization or synonym |
| product | `product/product-marketing-manager.md` | `role-descriptions-2/marketing/product-marketing-director.md` | GOOD | specialization or synonym |
| product | `product/product-marketing-manager.md` | `role-descriptions/Marketing/Marketing Manager.md` | GOOD | specialization or synonym |
| product | `product/product-marketing-manager.md` | `role-descriptions/Product/Product Manager.md` | GOOD | specialization or synonym |
| product | `product/product-operations-manager.md` | `role-descriptions/Operations/Operations Manager.md` | GOOD | specialization or synonym |
| product | `product/product-operations-manager.md` | `role-descriptions/Product/Product Manager.md` | GOOD | specialization or synonym |
| product | `product/product-owner.md` | `role-descriptions/Product/Product Owner.md` | STRONG | direct title match |
| product | `product/product-research-lead.md` | `role-descriptions/Product/Senior Product Manager.md` | WEAK | domain-adjacent; review before enrichment |
| product | `product/product-research-lead.md` | `role-descriptions/Product/UX Researcher.md` | WEAK | domain-adjacent; review before enrichment |
| quality-assurance | `quality-assurance/accessibility-tester.md` | `role-descriptions-2/information-technology/qa-tester.md` | WEAK | domain-adjacent; review before enrichment |
| quality-assurance | `quality-assurance/accessibility-tester.md` | `role-descriptions/Technology/QA Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| quality-assurance | `quality-assurance/head-of-qa.md` | `role-descriptions-2/information-technology/qa-tester.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/head-of-qa.md` | `role-descriptions-2/production/manager-of-quality-assurance.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/head-of-qa.md` | `role-descriptions-2/production/quality-assurance-specialist.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/head-of-qa.md` | `role-descriptions/Technology/QA Engineer.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/manual-qa-specialist.md` | `role-descriptions-2/production/quality-assurance-specialist.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/manual-qa-specialist.md` | `role-descriptions/AI & Emerging Roles/AI Quality Assurance Specialist.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/mobile-qa-specialist.md` | `role-descriptions-2/production/quality-assurance-specialist.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/mobile-qa-specialist.md` | `role-descriptions/AI & Emerging Roles/AI Quality Assurance Specialist.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/performance-tester.md` | `role-descriptions-2/information-technology/qa-tester.md` | WEAK | domain-adjacent; review before enrichment |
| quality-assurance | `quality-assurance/performance-tester.md` | `role-descriptions/Technology/QA Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| quality-assurance | `quality-assurance/qa-automation-engineer.md` | `role-descriptions/Technology/QA Automation Engineer.md` | STRONG | direct title match |
| quality-assurance | `quality-assurance/qa-automation-engineer.md` | `role-descriptions-3/engineering/quality-engineer.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-automation-engineer.md` | `role-descriptions/Technology/QA Engineer.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-lead.md` | `role-descriptions-2/information-technology/qa-tester.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-lead.md` | `role-descriptions-2/production/manager-of-quality-assurance.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-lead.md` | `role-descriptions-2/production/quality-assurance-specialist.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-lead.md` | `role-descriptions/AI & Emerging Roles/AI Quality Assurance Specialist.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-lead.md` | `role-descriptions/Technology/QA Automation Engineer.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-lead.md` | `role-descriptions/Technology/QA Engineer.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-operations-manager.md` | `role-descriptions-2/production/manager-of-quality-assurance.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-operations-manager.md` | `role-descriptions-2/production/quality-manager.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-operations-manager.md` | `role-descriptions/Operations/Operations Manager.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-research-lead.md` | `role-descriptions-2/information-technology/qa-tester.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-research-lead.md` | `role-descriptions-2/production/manager-of-quality-assurance.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-research-lead.md` | `role-descriptions-2/production/quality-assurance-specialist.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/qa-research-lead.md` | `role-descriptions/Technology/QA Engineer.md` | GOOD | specialization or synonym |
| quality-assurance | `quality-assurance/security-tester.md` | `role-descriptions-2/information-technology/qa-tester.md` | WEAK | domain-adjacent; review before enrichment |
| quality-assurance | `quality-assurance/security-tester.md` | `role-descriptions-3/information-technology/penetration-tester.md` | WEAK | domain-adjacent; review before enrichment |
| quality-assurance | `quality-assurance/security-tester.md` | `role-descriptions-3/information-technology/security-analyst.md` | WEAK | domain-adjacent; review before enrichment |
| quality-assurance | `quality-assurance/uat-coordinator.md` | `role-descriptions-2/information-technology/qa-tester.md` | WEAK | domain-adjacent; review before enrichment |
| quality-assurance | `quality-assurance/uat-coordinator.md` | `role-descriptions/Technology/QA Engineer.md` | WEAK | domain-adjacent; review before enrichment |
| research-intelligence | `research-intelligence/competitive-intelligence-analyst.md` | `role-descriptions-2/marketing/market-research-analyst.md` | WEAK | domain-adjacent; review before enrichment |
| research-intelligence | `research-intelligence/data-scientist.md` | `role-descriptions/Technology/Data Scientist.md` | STRONG | direct title match |
| research-intelligence | `research-intelligence/industry-analyst.md` | `role-descriptions-2/marketing/market-research-analyst.md` | WEAK | domain-adjacent; review before enrichment |
| research-intelligence | `research-intelligence/market-research-analyst.md` | `role-descriptions-2/marketing/market-research-analyst.md` | STRONG | direct title match |
| research-intelligence | `research-intelligence/research-director.md` | `role-descriptions-2/marketing/lead-researcher.md` | WEAK | domain-adjacent; review before enrichment |
| research-intelligence | `research-intelligence/research-director.md` | `role-descriptions/Product/UX Researcher.md` | WEAK | domain-adjacent; review before enrichment |
| research-intelligence | `research-intelligence/research-librarian.md` | `role-descriptions-2/marketing/lead-researcher.md` | WEAK | domain-adjacent; review before enrichment |
| research-intelligence | `research-intelligence/technology-research-analyst.md` | `role-descriptions-2/marketing/lead-researcher.md` | WEAK | domain-adjacent; review before enrichment |
| research-intelligence | `research-intelligence/technology-research-analyst.md` | `role-descriptions-2/marketing/market-research-analyst.md` | WEAK | domain-adjacent; review before enrichment |
| research-intelligence | `research-intelligence/user-research-lead.md` | `role-descriptions/Product/UX Researcher.md` | WEAK | domain-adjacent; review before enrichment |
| sales | `sales/account-executive.md` | `role-descriptions/Sales/Account Executive.md` | STRONG | direct title match |
| sales | `sales/account-executive.md` | `role-descriptions-2/marketing/advertising-account-executive.md` | GOOD | specialization or synonym |
| sales | `sales/account-executive.md` | `role-descriptions/Sales/Enterprise Account Executive.md` | GOOD | specialization or synonym |
| sales | `sales/account-executive.md` | `role-descriptions/Sales/Strategic Account Executive.md` | GOOD | specialization or synonym |
| sales | `sales/channel-partner-sales-manager.md` | `role-descriptions-2/marketing/channel-partner-manager.md` | GOOD | specialization or synonym |
| sales | `sales/channel-partner-sales-manager.md` | `role-descriptions/Sales/Sales Manager.md` | GOOD | specialization or synonym |
| sales | `sales/chief-revenue-officer.md` | `role-descriptions-2/finance/chief-revenue-officer.md` | STRONG | direct title match |
| sales | `sales/deal-desk-analyst.md` | `role-descriptions/Sales/Revenue Operations Analyst.md` | WEAK | domain-adjacent; review before enrichment |
| sales | `sales/deal-desk-analyst.md` | `role-descriptions/Sales/Sales Operations Analyst.md` | WEAK | domain-adjacent; review before enrichment |
| sales | `sales/proposal-writer.md` | `role-descriptions-2/media/writer.md` | GOOD | specialization or synonym |
| sales | `sales/sales-development-rep.md` | `role-descriptions/Sales/Sales Development Representative (SDR).md` | STRONG | direct title match |
| sales | `sales/sales-development-rep.md` | `role-descriptions/Sales/Sales Representative.md` | GOOD | specialization or synonym |
| sales | `sales/sales-director.md` | `role-descriptions/Sales/Sales Director.md` | STRONG | direct title match |
| sales | `sales/sales-director.md` | `role-descriptions-2/marketing/inside-sales-director.md` | GOOD | specialization or synonym |
| sales | `sales/sales-engineer.md` | `role-descriptions/Sales/Sales Engineer.md` | STRONG | direct title match |
| sales | `sales/sales-engineer.md` | `role-descriptions/Sales/Pre-Sales Engineer.md` | GOOD | specialization or synonym |
| sales | `sales/sales-operations-manager.md` | `role-descriptions/Sales/Sales Operations Manager.md` | STRONG | direct title match |
| sales | `sales/sales-operations-manager.md` | `role-descriptions-2/customer-service/sales-operations.md` | GOOD | specialization or synonym |
| sales | `sales/sales-operations-manager.md` | `role-descriptions/Operations/Operations Manager.md` | GOOD | specialization or synonym |
| sales | `sales/sales-operations-manager.md` | `role-descriptions/Sales/Sales Manager.md` | GOOD | specialization or synonym |
| sales | `sales/sales-operations-manager.md` | `role-descriptions/Sales/Sales Operations Analyst.md` | GOOD | specialization or synonym |
| sales | `sales/sales-research-analyst.md` | `role-descriptions-2/marketing/market-research-analyst.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/business-planner.md` | `role-descriptions-2/administrative/strategic-planner.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/business-planner.md` | `role-descriptions/Operations/Business Analyst.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/chief-strategy-officer.md` | `role-descriptions-2/administrative/business-consultant.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/chief-strategy-officer.md` | `role-descriptions/Executive/Chief Executive Officer (CEO).md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/corporate-development-manager.md` | `role-descriptions-2/administrative/strategic-planner.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/corporate-development-manager.md` | `role-descriptions/Sales/Business Development Manager.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/ma-analyst.md` | `role-descriptions-2/finance/private-equity-associate.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/ma-analyst.md` | `role-descriptions/Finance/Investment Analyst.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/new-ventures-lead.md` | `role-descriptions-2/administrative/strategic-planner.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/new-ventures-lead.md` | `role-descriptions/Sales/Business Development Manager.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/okr-planning-coordinator.md` | `role-descriptions-2/administrative/strategic-planner.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/okr-planning-coordinator.md` | `role-descriptions/Operations/Program Manager.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/partnership-manager.md` | `role-descriptions-2/marketing/partnership-manager.md` | STRONG | direct title match |
| strategy-business-dev | `strategy-business-dev/strategic-analyst.md` | `role-descriptions-2/administrative/strategic-planner.md` | WEAK | domain-adjacent; review before enrichment |
| strategy-business-dev | `strategy-business-dev/strategic-analyst.md` | `role-descriptions/Operations/Business Analyst.md` | WEAK | domain-adjacent; review before enrichment |
| support | `support/customer-support-specialist.md` | `role-descriptions-2/customer-service/customer-support-specialist.md` | STRONG | direct title match |
| support | `support/customer-support-specialist.md` | `role-descriptions-2/customer-service/support-specialist.md` | GOOD | specialization or synonym |
| support | `support/head-of-support.md` | `role-descriptions/Customer Service/Director of Customer Service.md` | WEAK | domain-adjacent; review before enrichment |
| support | `support/head-of-support.md` | `role-descriptions/Customer Service/VP of Customer Service.md` | WEAK | domain-adjacent; review before enrichment |
| support | `support/knowledge-base-manager.md` | `role-descriptions-2/administrative/documentation-specialist.md` | WEAK | domain-adjacent; review before enrichment |
| support | `support/knowledge-base-manager.md` | `role-descriptions/Creative/Technical Writer.md` | WEAK | domain-adjacent; review before enrichment |
| support | `support/support-operations-manager.md` | `role-descriptions/Operations/Operations Manager.md` | GOOD | specialization or synonym |
| support | `support/support-research-analyst.md` | `role-descriptions/Customer Service/Customer Experience Analyst.md` | WEAK | domain-adjacent; review before enrichment |
| support | `support/technical-support-engineer.md` | `role-descriptions-2/customer-service/technical-support-engineer.md` | STRONG | direct title match |
| support | `support/technical-support-engineer.md` | `role-descriptions/Customer Service/Technical Support Specialist.md` | GOOD | specialization or synonym |

## Unmatched Roles

_None. All 170 role files have at least one match._

## Multi-Match Roles

Roles below map to more than one JD. When enriching, prefer the STRONG row first, then merge distinctive specifics from the GOOD rows. WEAK rows are curated domain-adjacent hints, not content sources; lift only if the concrete artifact/tool clearly applies.

- `ai-automation/agent-developer.md` > [`role-descriptions/AI & Emerging Roles/Generative AI Developer.md` (WEAK), `role-descriptions/Technology/AI Engineer.md` (WEAK), `role-descriptions/Technology/Software Engineer.md` (WEAK)]
- `ai-automation/ai-enablement-specialist.md` > [`role-descriptions/AI & Emerging Roles/AI Implementation Specialist.md` (WEAK), `role-descriptions/AI & Emerging Roles/AI Trainer.md` (WEAK)]
- `ai-automation/ai-ethics-specialist.md` > [`role-descriptions-2/engineering/ai-ethics-researcher.md` (GOOD), `role-descriptions/AI & Emerging Roles/AI Ethics Officer.md` (GOOD)]
- `ai-automation/ai-ml-engineer.md` > [`role-descriptions/Technology/AI Engineer.md` (GOOD), `role-descriptions/Technology/Machine Learning Engineer.md` (GOOD)]
- `ai-automation/ai-operations-engineer.md` > [`role-descriptions-2/engineering/operations-engineer.md` (GOOD), `role-descriptions-2/information-technology/ai-operations-manager.md` (GOOD), `role-descriptions/Technology/AI Engineer.md` (GOOD)]
- `ai-automation/ai-solutions-architect.md` > [`role-descriptions-2/engineering/solutions-architect.md` (GOOD), `role-descriptions-2/information-technology/ai-architect.md` (GOOD)]
- `ai-automation/conversational-ai-designer.md` > [`role-descriptions/AI & Emerging Roles/Conversational AI Designer.md` (STRONG), `role-descriptions-2/design/junior-designer.md` (GOOD)]
- `client-services/account-manager.md` > [`role-descriptions/Sales/Account Manager.md` (STRONG), `role-descriptions-2/customer-service/technical-account-manager.md` (GOOD), `role-descriptions-2/marketing/digital-account-manager.md` (GOOD), `role-descriptions/Sales/Key Account Manager.md` (GOOD), `role-descriptions/Sales/National Account Manager.md` (GOOD)]
- `client-services/client-research-analyst.md` > [`role-descriptions-2/marketing/market-research-analyst.md` (WEAK), `role-descriptions/Customer Service/Customer Experience Analyst.md` (WEAK)]
- `client-services/client-success-manager.md` > [`role-descriptions/Sales/Account Manager.md` (WEAK), `role-descriptions/Sales/Customer Success Manager.md` (WEAK)]
- `client-services/delivery-manager.md` > [`role-descriptions/Operations/Program Manager.md` (WEAK), `role-descriptions/Operations/Project Manager.md` (WEAK)]
- `client-services/head-of-client-services.md` > [`role-descriptions/Customer Service/Director of Customer Service.md` (WEAK), `role-descriptions/Customer Service/VP of Customer Service.md` (WEAK)]
- `client-services/project-manager.md` > [`role-descriptions/Operations/Project Manager.md` (STRONG), `role-descriptions-2/administrative/assistant-project-manager.md` (GOOD), `role-descriptions-2/marketing/digital-project-manager.md` (GOOD), `role-descriptions-3/executive-management/architectural-project-manager.md` (GOOD), `role-descriptions/Creative/Creative Project Manager.md` (GOOD), `role-descriptions/Operations/Construction Project Manager.md` (GOOD), `role-descriptions/Operations/IT Project Manager.md` (GOOD), `role-descriptions/Operations/Technical Project Manager.md` (GOOD)]
- `client-services/technical-account-manager.md` > [`role-descriptions-2/customer-service/technical-account-manager.md` (STRONG), `role-descriptions/Sales/Account Manager.md` (GOOD)]
- `creative-technology/creative-tech-research-lead.md` > [`role-descriptions/Creative/Creative Director.md` (WEAK), `role-descriptions/Product/UX Researcher.md` (WEAK)]
- `creative-technology/creative-technologist.md` > [`role-descriptions/Creative/Creative Director.md` (WEAK), `role-descriptions/Creative/Digital Designer.md` (WEAK)]
- `creative-technology/head-of-creative-technology.md` > [`role-descriptions/Creative/Chief Creative Officer.md` (WEAK), `role-descriptions/Creative/Creative Director.md` (WEAK)]
- `creative-technology/motion-design-lead.md` > [`role-descriptions/Creative/Creative Director.md` (WEAK), `role-descriptions/Creative/Motion Graphics Designer.md` (WEAK)]
- `creative-technology/motion-designer.md` > [`role-descriptions-2/design/junior-designer.md` (GOOD), `role-descriptions/Creative/Motion Graphics Designer.md` (GOOD)]
- `creative-technology/vfx-artist.md` > [`role-descriptions/Creative/3D Artist.md` (WEAK), `role-descriptions/Creative/Motion Graphics Designer.md` (WEAK)]
- `data-analytics/analytics-engineer.md` > [`role-descriptions-2/information-technology/bi-consultant.md` (WEAK), `role-descriptions/Technology/Data Engineer.md` (WEAK)]
- `data-analytics/analytics-operations-manager.md` > [`role-descriptions-2/information-technology/analytics-manager.md` (GOOD), `role-descriptions/Operations/Operations Manager.md` (GOOD)]
- `data-analytics/bi-developer.md` > [`role-descriptions-2/information-technology/bi-(business-intelligence)-developer.md` (STRONG), `role-descriptions-2/administrative/business-intelligence-analyst.md` (GOOD), `role-descriptions-2/information-technology/bi-consultant.md` (GOOD)]
- `data-analytics/data-analyst.md` > [`role-descriptions/Operations/Data Analyst.md` (STRONG), `role-descriptions-2/information-technology/healthcare-data-analyst.md` (GOOD), `role-descriptions/Marketing/Marketing Data Analyst.md` (GOOD)]
- `data-analytics/data-analytics-research-lead.md` > [`role-descriptions-2/information-technology/lead-data-scientist.md` (WEAK), `role-descriptions/Technology/Data Scientist.md` (WEAK)]
- `data-analytics/data-quality-engineer.md` > [`role-descriptions-3/engineering/quality-engineer.md` (GOOD), `role-descriptions/Technology/Data Engineer.md` (GOOD)]
- `data-analytics/head-of-data-analytics.md` > [`role-descriptions-2/information-technology/analytics-manager.md` (WEAK), `role-descriptions-2/information-technology/lead-data-engineer.md` (WEAK)]
- `data-analytics/tracking-instrumentation-specialist.md` > [`role-descriptions-2/information-technology/analytics-manager.md` (WEAK), `role-descriptions/Technology/Data Engineer.md` (WEAK)]
- `design/accessibility-specialist.md` > [`role-descriptions-2/design/ux-designer.md` (WEAK), `role-descriptions/Creative/Web Designer.md` (WEAK)]
- `design/design-research-lead.md` > [`role-descriptions/Product/Senior UI Designer.md` (WEAK), `role-descriptions/Product/UX Researcher.md` (WEAK)]
- `design/design-system-manager.md` > [`role-descriptions-2/design/design-operations-manager.md` (WEAK), `role-descriptions/Product/Senior UI Designer.md` (WEAK)]
- `design/head-of-design.md` > [`role-descriptions-2/design/design-operations-manager.md` (WEAK), `role-descriptions/Creative/Creative Director.md` (WEAK)]
- `design/ui-designer.md` > [`role-descriptions/Product/Senior UI Designer.md` (STRONG), `role-descriptions-2/design/junior-designer.md` (GOOD), `role-descriptions-2/design/ui-ux-designer.md` (GOOD), `role-descriptions-2/design/ux-designer.md` (GOOD)]
- `design/ux-designer.md` > [`role-descriptions-2/design/ux-designer.md` (STRONG), `role-descriptions-2/design/junior-designer.md` (GOOD), `role-descriptions-2/design/ui-ux-designer.md` (GOOD), `role-descriptions/Product/Senior UI Designer.md` (GOOD), `role-descriptions/Product/UX Researcher.md` (GOOD)]
- `design/visual-brand-designer.md` > [`role-descriptions-2/design/brand-designer-and-illustrator.md` (GOOD), `role-descriptions-2/design/junior-designer.md` (GOOD), `role-descriptions-2/design/visual-designer.md` (GOOD), `role-descriptions/Marketing/Brand Designer.md` (GOOD)]
- `engineering/ai-ml-engineer.md` > [`role-descriptions/Technology/AI Engineer.md` (GOOD), `role-descriptions/Technology/Machine Learning Engineer.md` (GOOD)]
- `engineering/backend-developer.md` > [`role-descriptions/Technology/Backend Developer.md` (STRONG), `role-descriptions-2/information-technology/backend-javascript-developer.md` (GOOD), `role-descriptions/Technology/C# Backend Developer.md` (GOOD), `role-descriptions/Technology/Python Backend Developer.md` (GOOD)]
- `engineering/data-engineer.md` > [`role-descriptions/Technology/Data Engineer.md` (STRONG), `role-descriptions-3/information-technology/big-data-engineer.md` (GOOD)]
- `engineering/engineering-manager.md` > [`role-descriptions-2/engineering/engineering-manager.md` (STRONG), `role-descriptions/AI & Emerging Roles/Prompt Engineering Manager.md` (GOOD)]
- `engineering/engineering-research-lead.md` > [`role-descriptions-2/engineering/enterprise-architect.md` (WEAK), `role-descriptions-2/information-technology/director-of-engineering.md` (WEAK)]
- `engineering/security-engineer.md` > [`role-descriptions-2/information-technology/security-engineer.md` (STRONG), `role-descriptions-3/information-technology/application-security-engineer.md` (GOOD)]
- `finance-investor-relations/cap-table-manager.md` > [`role-descriptions/Finance/Controller.md` (WEAK), `role-descriptions/Finance/Financial Analyst.md` (WEAK)]
- `finance-investor-relations/chief-financial-officer.md` > [`role-descriptions/Executive/Chief Financial Officer (CFO).md` (STRONG), `role-descriptions-2/finance/nonprofit-cfo.md` (GOOD)]
- `finance-investor-relations/financial-controller.md` > [`role-descriptions-2/finance/financial-controller.md` (STRONG), `role-descriptions/Finance/Controller.md` (GOOD)]
- `finance-investor-relations/financial-modeler.md` > [`role-descriptions/Finance/Financial Analyst.md` (WEAK), `role-descriptions/Finance/Senior Financial Analyst.md` (WEAK)]
- `finance-investor-relations/fpa-analyst.md` > [`role-descriptions/Finance/Financial Analyst.md` (GOOD), `role-descriptions/Finance/Financial Planning Analyst.md` (GOOD)]
- `finance-investor-relations/grant-writer.md` > [`role-descriptions-2/marketing/grant-writer.md` (STRONG), `role-descriptions-2/media/writer.md` (GOOD)]
- `finance-investor-relations/investor-relations-manager.md` > [`role-descriptions-2/marketing/communications-director.md` (WEAK), `role-descriptions/Finance/Financial Analyst.md` (WEAK)]
- `finance-investor-relations/treasury-manager.md` > [`role-descriptions-2/finance/financial-manager.md` (WEAK), `role-descriptions-2/finance/treasurer.md` (WEAK)]
- `human-resources/agent-performance-analyst.md` > [`role-descriptions-2/administrative/business-performance-analyst.md` (WEAK), `role-descriptions-2/information-technology/ai-auditor.md` (WEAK)]
- `human-resources/chief-human-resources-officer.md` > [`role-descriptions-2/human-resources/chief-human-resources-officer-(chro).md` (STRONG), `role-descriptions-2/human-resources/hr-and-admin-officer.md` (GOOD), `role-descriptions-2/human-resources/hr-officer.md` (GOOD)]
- `human-resources/quality-assurance-auditor.md` > [`role-descriptions-2/information-technology/qa-tester.md` (GOOD), `role-descriptions-2/production/manager-of-quality-assurance.md` (GOOD), `role-descriptions-2/production/quality-assurance-specialist.md` (GOOD), `role-descriptions-3/finance-accounting/auditor.md` (GOOD), `role-descriptions/Technology/QA Engineer.md` (GOOD)]
- `human-resources/skill-developer.md` > [`role-descriptions-2/corporate-training/curriculum-designer.md` (WEAK), `role-descriptions-2/human-resources/learning-and-development-specialist.md` (WEAK), `role-descriptions-3/education-training/instructional-designer.md` (WEAK)]
- `legal-compliance/compliance-officer.md` > [`role-descriptions-2/administrative/contract-administrator.md` (WEAK), `role-descriptions-3/legal-compliance/legal-assistant.md` (WEAK), `role-descriptions-3/legal-compliance/paralegal.md` (WEAK)]
- `legal-compliance/general-counsel.md` > [`role-descriptions-2/administrative/contract-administrator.md` (WEAK), `role-descriptions-3/legal-compliance/legal-assistant.md` (WEAK), `role-descriptions-3/legal-compliance/paralegal.md` (WEAK)]
- `legal-compliance/ip-manager.md` > [`role-descriptions-2/administrative/contract-administrator.md` (WEAK), `role-descriptions-3/legal-compliance/paralegal.md` (WEAK)]
- `legal-compliance/legal-research-analyst.md` > [`role-descriptions-3/legal-compliance/legal-assistant.md` (WEAK), `role-descriptions-3/legal-compliance/paralegal.md` (WEAK)]
- `legal-compliance/privacy-officer.md` > [`role-descriptions-2/administrative/contract-administrator.md` (WEAK), `role-descriptions-3/legal-compliance/legal-assistant.md` (WEAK), `role-descriptions-3/legal-compliance/paralegal.md` (WEAK)]
- `management/project-orchestrator.md` > [`role-descriptions/Operations/Program Manager.md` (WEAK), `role-descriptions/Operations/Project Manager.md` (WEAK)]
- `management/quality-coordinator.md` > [`role-descriptions-2/information-technology/qa-tester.md` (WEAK), `role-descriptions/AI & Emerging Roles/AI Quality Assurance Specialist.md` (WEAK)]
- `management/technical-coordinator.md` > [`role-descriptions/Operations/Project Coordinator.md` (WEAK), `role-descriptions/Operations/Technical Program Manager.md` (WEAK)]
- `marketing/chief-marketing-officer.md` > [`role-descriptions/Executive/Chief Marketing Officer (CMO).md` (STRONG), `role-descriptions-2/marketing/marketing-intern.md` (GOOD), `role-descriptions-2/marketing/marketing-officer.md` (GOOD)]
- `marketing/content-marketing-manager.md` > [`role-descriptions/Marketing/Content Marketing Manager.md` (STRONG), `role-descriptions-2/marketing/content-manager.md` (GOOD), `role-descriptions-2/marketing/content-marketing-intern.md` (GOOD), `role-descriptions-2/marketing/director-of-content-marketing.md` (GOOD), `role-descriptions-2/marketing/marketing-intern.md` (GOOD), `role-descriptions/Marketing/Marketing Manager.md` (GOOD)]
- `marketing/email-marketing-specialist.md` > [`role-descriptions/Marketing/Email Marketing Specialist.md` (STRONG), `role-descriptions-2/marketing/marketing-intern.md` (GOOD), `role-descriptions-2/marketing/marketing-specialist.md` (GOOD), `role-descriptions/Marketing/Email Marketing Manager.md` (GOOD)]
- `marketing/event-marketing-manager.md` > [`role-descriptions-2/marketing/marketing-intern.md` (GOOD), `role-descriptions/Marketing/Event Marketing Specialist.md` (GOOD), `role-descriptions/Marketing/Marketing Manager.md` (GOOD)]
- `marketing/growth-hacker.md` > [`role-descriptions/Marketing/Demand Generation Manager.md` (WEAK), `role-descriptions/Marketing/Growth Marketing Manager.md` (WEAK)]
- `marketing/marketing-analyst.md` > [`role-descriptions/Marketing/Marketing Analyst.md` (STRONG), `role-descriptions-2/marketing/marketing-intern.md` (GOOD), `role-descriptions/Marketing/Marketing Data Analyst.md` (GOOD)]
- `marketing/marketing-copywriter.md` > [`role-descriptions-2/marketing/marketing-copywriter.md` (STRONG), `role-descriptions-2/marketing/marketing-intern.md` (GOOD), `role-descriptions/Creative/Copywriter.md` (GOOD)]
- `marketing/marketing-designer.md` > [`role-descriptions-2/design/junior-designer.md` (GOOD), `role-descriptions-2/marketing/marketing-intern.md` (GOOD)]
- `marketing/performance-marketing-manager.md` > [`role-descriptions-2/marketing/marketing-intern.md` (GOOD), `role-descriptions/Marketing/Marketing Manager.md` (GOOD)]
- `marketing/pr-communications-manager.md` > [`role-descriptions-2/public-relations/public-relations-intern.md` (GOOD), `role-descriptions-2/public-relations/public-relations-manager.md` (GOOD)]
- `marketing/seo-sem-specialist.md` > [`role-descriptions-2/marketing/junior-sem-seo-specialist.md` (STRONG), `role-descriptions-2/marketing/search-engine-marketing-(sem)-specialist.md` (GOOD), `role-descriptions/Marketing/SEO Specialist.md` (GOOD)]
- `marketing/social-media-manager.md` > [`role-descriptions/Marketing/Social Media Manager.md` (STRONG), `role-descriptions-2/marketing/social-media-analyst.md` (GOOD), `role-descriptions-2/marketing/social-media-coordinator.md` (GOOD), `role-descriptions-2/marketing/social-media-copywriter.md` (GOOD), `role-descriptions-2/marketing/social-media-strategist.md` (GOOD), `role-descriptions/Marketing/Social Media Specialist.md` (GOOD)]
- `operations/it-manager.md` > [`role-descriptions-2/information-technology/it-manager.md` (STRONG), `role-descriptions-2/information-technology/it-operations-manager.md` (GOOD), `role-descriptions/Operations/IT Project Manager.md` (GOOD)]
- `operations/process-manager.md` > [`role-descriptions-2/engineering/process-engineer.md` (WEAK), `role-descriptions/Operations/Operations Manager.md` (WEAK)]
- `operations/vendor-manager.md` > [`role-descriptions-2/administrative/procurement-specialist.md` (WEAK), `role-descriptions-3/operations-logistics/procurement-manager.md` (WEAK)]
- `platform-engineering/developer-experience-engineer.md` > [`role-descriptions/Creative/Technical Writer.md` (WEAK), `role-descriptions/Technology/DevOps Engineer.md` (WEAK)]
- `platform-engineering/devops-research-lead.md` > [`role-descriptions-2/engineering/enterprise-architect.md` (WEAK), `role-descriptions/Technology/DevOps Engineer.md` (WEAK)]
- `platform-engineering/head-of-platform-engineering.md` > [`role-descriptions-2/information-technology/director-of-engineering.md` (WEAK), `role-descriptions-2/information-technology/it-director.md` (WEAK)]
- `platform-engineering/infrastructure-engineer.md` > [`role-descriptions/Technology/Cloud Architect.md` (WEAK), `role-descriptions/Technology/DevOps Engineer.md` (WEAK), `role-descriptions/Technology/Google Cloud Engineer.md` (WEAK)]
- `platform-engineering/release-manager.md` > [`role-descriptions/Operations/Program Manager.md` (WEAK), `role-descriptions/Technology/DevOps Engineer.md` (WEAK)]
- `platform-engineering/security-operations-engineer.md` > [`role-descriptions-2/engineering/operations-engineer.md` (GOOD), `role-descriptions-2/information-technology/security-engineer.md` (GOOD)]
- `product/business-analyst.md` > [`role-descriptions/Operations/Business Analyst.md` (STRONG), `role-descriptions-2/administrative/business-intelligence-analyst.md` (GOOD), `role-descriptions-2/administrative/business-performance-analyst.md` (GOOD), `role-descriptions-2/information-technology/lead-business-systems-analyst.md` (GOOD), `role-descriptions/AI & Emerging Roles/AI Business Analyst.md` (GOOD)]
- `product/product-manager.md` > [`role-descriptions/Product/Product Manager.md` (STRONG), `role-descriptions-2/marketing/product-partner-manager.md` (GOOD), `role-descriptions/Marketing/Product Marketing Manager.md` (GOOD), `role-descriptions/Product/AI Product Manager.md` (GOOD), `role-descriptions/Product/Associate Product Manager.md` (GOOD), `role-descriptions/Product/B2B Product Manager.md` (GOOD), `role-descriptions/Product/B2C Product Manager.md` (GOOD), `role-descriptions/Product/Group Product Manager.md` (GOOD), `role-descriptions/Product/Growth Product Manager.md` (GOOD), `role-descriptions/Product/Mobile Product Manager.md` (GOOD), `role-descriptions/Product/Platform Product Manager.md` (GOOD), `role-descriptions/Product/Technical Product Manager.md` (GOOD)]
- `product/product-marketing-manager.md` > [`role-descriptions/Marketing/Product Marketing Manager.md` (STRONG), `role-descriptions-2/marketing/lead-product-marketing-writer.md` (GOOD), `role-descriptions-2/marketing/marketing-intern.md` (GOOD), `role-descriptions-2/marketing/product-marketing-associate.md` (GOOD), `role-descriptions-2/marketing/product-marketing-director.md` (GOOD), `role-descriptions/Marketing/Marketing Manager.md` (GOOD), `role-descriptions/Product/Product Manager.md` (GOOD)]
- `product/product-operations-manager.md` > [`role-descriptions/Operations/Operations Manager.md` (GOOD), `role-descriptions/Product/Product Manager.md` (GOOD)]
- `product/product-research-lead.md` > [`role-descriptions/Product/Senior Product Manager.md` (WEAK), `role-descriptions/Product/UX Researcher.md` (WEAK)]
- `quality-assurance/accessibility-tester.md` > [`role-descriptions-2/information-technology/qa-tester.md` (WEAK), `role-descriptions/Technology/QA Engineer.md` (WEAK)]
- `quality-assurance/head-of-qa.md` > [`role-descriptions-2/information-technology/qa-tester.md` (GOOD), `role-descriptions-2/production/manager-of-quality-assurance.md` (GOOD), `role-descriptions-2/production/quality-assurance-specialist.md` (GOOD), `role-descriptions/Technology/QA Engineer.md` (GOOD)]
- `quality-assurance/manual-qa-specialist.md` > [`role-descriptions-2/production/quality-assurance-specialist.md` (GOOD), `role-descriptions/AI & Emerging Roles/AI Quality Assurance Specialist.md` (GOOD)]
- `quality-assurance/mobile-qa-specialist.md` > [`role-descriptions-2/production/quality-assurance-specialist.md` (GOOD), `role-descriptions/AI & Emerging Roles/AI Quality Assurance Specialist.md` (GOOD)]
- `quality-assurance/performance-tester.md` > [`role-descriptions-2/information-technology/qa-tester.md` (WEAK), `role-descriptions/Technology/QA Engineer.md` (WEAK)]
- `quality-assurance/qa-automation-engineer.md` > [`role-descriptions/Technology/QA Automation Engineer.md` (STRONG), `role-descriptions-3/engineering/quality-engineer.md` (GOOD), `role-descriptions/Technology/QA Engineer.md` (GOOD)]
- `quality-assurance/qa-lead.md` > [`role-descriptions-2/information-technology/qa-tester.md` (GOOD), `role-descriptions-2/production/manager-of-quality-assurance.md` (GOOD), `role-descriptions-2/production/quality-assurance-specialist.md` (GOOD), `role-descriptions/AI & Emerging Roles/AI Quality Assurance Specialist.md` (GOOD), `role-descriptions/Technology/QA Automation Engineer.md` (GOOD), `role-descriptions/Technology/QA Engineer.md` (GOOD)]
- `quality-assurance/qa-operations-manager.md` > [`role-descriptions-2/production/manager-of-quality-assurance.md` (GOOD), `role-descriptions-2/production/quality-manager.md` (GOOD), `role-descriptions/Operations/Operations Manager.md` (GOOD)]
- `quality-assurance/qa-research-lead.md` > [`role-descriptions-2/information-technology/qa-tester.md` (GOOD), `role-descriptions-2/production/manager-of-quality-assurance.md` (GOOD), `role-descriptions-2/production/quality-assurance-specialist.md` (GOOD), `role-descriptions/Technology/QA Engineer.md` (GOOD)]
- `quality-assurance/security-tester.md` > [`role-descriptions-2/information-technology/qa-tester.md` (WEAK), `role-descriptions-3/information-technology/penetration-tester.md` (WEAK), `role-descriptions-3/information-technology/security-analyst.md` (WEAK)]
- `quality-assurance/uat-coordinator.md` > [`role-descriptions-2/information-technology/qa-tester.md` (WEAK), `role-descriptions/Technology/QA Engineer.md` (WEAK)]
- `research-intelligence/research-director.md` > [`role-descriptions-2/marketing/lead-researcher.md` (WEAK), `role-descriptions/Product/UX Researcher.md` (WEAK)]
- `research-intelligence/technology-research-analyst.md` > [`role-descriptions-2/marketing/lead-researcher.md` (WEAK), `role-descriptions-2/marketing/market-research-analyst.md` (WEAK)]
- `sales/account-executive.md` > [`role-descriptions/Sales/Account Executive.md` (STRONG), `role-descriptions-2/marketing/advertising-account-executive.md` (GOOD), `role-descriptions/Sales/Enterprise Account Executive.md` (GOOD), `role-descriptions/Sales/Strategic Account Executive.md` (GOOD)]
- `sales/channel-partner-sales-manager.md` > [`role-descriptions-2/marketing/channel-partner-manager.md` (GOOD), `role-descriptions/Sales/Sales Manager.md` (GOOD)]
- `sales/deal-desk-analyst.md` > [`role-descriptions/Sales/Revenue Operations Analyst.md` (WEAK), `role-descriptions/Sales/Sales Operations Analyst.md` (WEAK)]
- `sales/sales-development-rep.md` > [`role-descriptions/Sales/Sales Development Representative (SDR).md` (STRONG), `role-descriptions/Sales/Sales Representative.md` (GOOD)]
- `sales/sales-director.md` > [`role-descriptions/Sales/Sales Director.md` (STRONG), `role-descriptions-2/marketing/inside-sales-director.md` (GOOD)]
- `sales/sales-engineer.md` > [`role-descriptions/Sales/Sales Engineer.md` (STRONG), `role-descriptions/Sales/Pre-Sales Engineer.md` (GOOD)]
- `sales/sales-operations-manager.md` > [`role-descriptions/Sales/Sales Operations Manager.md` (STRONG), `role-descriptions-2/customer-service/sales-operations.md` (GOOD), `role-descriptions/Operations/Operations Manager.md` (GOOD), `role-descriptions/Sales/Sales Manager.md` (GOOD), `role-descriptions/Sales/Sales Operations Analyst.md` (GOOD)]
- `strategy-business-dev/business-planner.md` > [`role-descriptions-2/administrative/strategic-planner.md` (WEAK), `role-descriptions/Operations/Business Analyst.md` (WEAK)]
- `strategy-business-dev/chief-strategy-officer.md` > [`role-descriptions-2/administrative/business-consultant.md` (WEAK), `role-descriptions/Executive/Chief Executive Officer (CEO).md` (WEAK)]
- `strategy-business-dev/corporate-development-manager.md` > [`role-descriptions-2/administrative/strategic-planner.md` (WEAK), `role-descriptions/Sales/Business Development Manager.md` (WEAK)]
- `strategy-business-dev/ma-analyst.md` > [`role-descriptions-2/finance/private-equity-associate.md` (WEAK), `role-descriptions/Finance/Investment Analyst.md` (WEAK)]
- `strategy-business-dev/new-ventures-lead.md` > [`role-descriptions-2/administrative/strategic-planner.md` (WEAK), `role-descriptions/Sales/Business Development Manager.md` (WEAK)]
- `strategy-business-dev/okr-planning-coordinator.md` > [`role-descriptions-2/administrative/strategic-planner.md` (WEAK), `role-descriptions/Operations/Program Manager.md` (WEAK)]
- `strategy-business-dev/strategic-analyst.md` > [`role-descriptions-2/administrative/strategic-planner.md` (WEAK), `role-descriptions/Operations/Business Analyst.md` (WEAK)]
- `support/customer-support-specialist.md` > [`role-descriptions-2/customer-service/customer-support-specialist.md` (STRONG), `role-descriptions-2/customer-service/support-specialist.md` (GOOD)]
- `support/head-of-support.md` > [`role-descriptions/Customer Service/Director of Customer Service.md` (WEAK), `role-descriptions/Customer Service/VP of Customer Service.md` (WEAK)]
- `support/knowledge-base-manager.md` > [`role-descriptions-2/administrative/documentation-specialist.md` (WEAK), `role-descriptions/Creative/Technical Writer.md` (WEAK)]
- `support/technical-support-engineer.md` > [`role-descriptions-2/customer-service/technical-support-engineer.md` (STRONG), `role-descriptions/Customer Service/Technical Support Specialist.md` (GOOD)]

## Document Control

- **Generated:** 2026-04-17
- **Generator:** `/tmp/claude/match_roles.py` (token normalization + curated WEAK supplement) > `/tmp/claude/generate_artifact.py` (markdown render)
- **Consumers:** downstream role-enrichment agents; JD content is consumed as suggestion, never as authoritative rewrite
