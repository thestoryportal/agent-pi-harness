# P3 Report — Cross-Role Consistency

**Date:** 2026-04-17
**Auditor:** Claude Sonnet 4.6 + GPT-4o (multi-model Check 3)
**Total Role Files:** 170 (19 departments)
**Charter Entries:** 169 roles (18 departments)
**Verdict:** ISSUES FOUND — 8 classification mismatches, 3 missing files, 1 phantom department, 2 naming mismatches, 10 critical overlaps, 8 critical gaps

---

## Check 1: Charter Completeness

### Coverage Summary

| Metric | Count |
|--------|-------|
| Charter departments | 18 |
| File system departments | 19 |
| Charter roles | 169 |
| Role files total | 170 |
| Charter roles with files | 166 |
| Charter roles missing files | 3 |
| Files with no charter entry | 4 (management dept) |

### Coverage Gaps

| Type | Item | Department | Action |
|------|------|------------|--------|
| Charter-only | Real-Time Graphics Engineer | creative-technology | Create role file |
| Charter-only | Technical Artist | creative-technology | Create role file |
| Charter-only | Immersive Experience Designer | creative-technology | Create role file |
| File-only | operations-coordinator | management (not in charter) | Add to charter or reclassify |
| File-only | project-orchestrator | management (not in charter) | Add to charter or reclassify |
| File-only | quality-coordinator | management (not in charter) | Add to charter or reclassify |
| File-only | technical-coordinator | management (not in charter) | Add to charter or reclassify |

**Note:** The `management/` directory contains 4 coordinator roles absent from the charter. These may represent a cross-cutting coordination layer or a planned new department that was built before the charter was updated. Requires resolution: either add a Department 19 "Management / Program Office" to the charter or reclassify these files into appropriate existing departments.

---

## Check 2: Role Reference Validity

**Verdict:** No invalid or invented role names found in cross-references.

All 170 role files use human-readable role titles (e.g., "Engineering Manager", "UI Designer") in Works With, Reports To, and Escalates To sections. Every referenced title maps to a real charter role.

**Recommendation:** Standardize cross-references to use kebab-case slugs (e.g., `engineering-manager`, `ui-designer`) instead of display titles. This enables programmatic validation in future audit passes.

---

## Check 3: Responsibility Overlaps and Gaps

*Multi-model board review (Claude Sonnet 4.6 + GPT-4o) on all 169 charter roles.*

### Critical Overlaps

| # | Responsibility | Claimed By | Issue | Recommended Owner |
|---|---------------|------------|-------|-------------------|
| 1 | **AI/ML Engineering** | AI/ML Engineer (Engineering), AI/ML Engineer (AI & Automation) | Identical title in two departments; no charter signal for who owns model dev vs. integration vs. production deployment | Rename: Engineering's → **ML Infrastructure Engineer**; AI & Automation's → **Applied AI Engineer** |
| 2 | **Security ownership** | Security Engineer (Eng), Security Operations Engineer (Platform), Security Tester (QA), Privacy Officer (Legal) | Vulnerability remediation, security review sign-off, and incident ownership each plausibly claimed by all four; no RACI | Security Engineer=secure design/code; SecOps=runtime/infra; Security Tester=pre-release; Privacy Officer=regulatory. Requires cross-functional RACI |
| 3 | **Competitive intelligence** | Competitive Intelligence Analyst (Research), Competitive Product Analyst (Product), Sales Research Analyst (Sales), Strategic Analyst (Strategy) | Four roles collecting competitive data with no defined handoff; contradictory intel likely | CI Analyst owns raw intelligence; Competitive Product Analyst owns product synthesis; others are consumers |
| 4 | **Market research** | Market Research Analyst (Research), Marketing Research Lead (Marketing), Sales Research Analyst (Sales), Product Research Lead (Product) | Duplicate vendor surveys, contradictory TAM figures across board decks vs. sales decks | Market Research Analyst owns primary/syndicated output; embedded Research Leads are consumers with top-up mandate only |
| 5 | **Partnership ownership** | Partnership Manager (Strategy), Channel/Partner Sales Manager (Sales) | Strategic alliances vs. revenue-bearing channel partnerships overlap in mid-funnel; contract and co-sell motions claimed by both | Partnership Manager=non-revenue strategic alliances; Channel/Partner Sales Mgr=revenue-bearing resellers. Requires formal partner-type taxonomy |
| 6 | **Client technical escalation** | Technical Account Manager (CS), Solutions Architect (Eng), Technical Support Engineer (Support), Implementation Specialist (CS) | Live client crisis has four potential owners; creates slow escalations and contradictory client communications | TAM=escalation triage; Solutions Architect=architectural remediation; Technical Support Eng=break/fix; Implementation Specialist=post-sale pre-BAU only. Tiered SLA matrix required |
| 7 | **Content strategy / brand voice** | Content Marketing Manager (Marketing), Marketing Copywriter (Marketing), Content Designer/UX Writer (Design), PR/Communications Manager (Marketing) | No owner of master brand voice standard or content calendar | Brand Strategist=voice standard; Content Marketing Mgr=editorial calendar; Content Designer=in-product copy; PR=external comms |
| 8 | **Process improvement** | Process Manager (Ops), Product Operations Manager (Product), Sales Operations Manager (Sales), AI Operations Engineer (AI), QA Operations Manager (QA), Analytics Operations Manager (Data) | Six roles can independently initiate process redesign touching same workflows; no enterprise process map owner | Process Manager (Operations)=enterprise process register and change governance; all department Ops Managers=local execution only, must register changes centrally |
| 9 | **Accessibility authority** | Accessibility Specialist (Design), Accessibility Tester (QA) | Split is acceptable; problem is who owns ship/no-ship call when pre-launch violations are found | Accessibility Specialist=standard and ship/no-ship recommendation; Accessibility Tester=evidence. Final go/no-go: Head of Design for design issues, Head of QA for systemic failures |
| 10 | **Product roadmap prioritization** | Product Manager, Product Owner, Business Analyst (all in Product) | PM and PO is already a known overlap; BA here is ambiguously scoped and can claim roadmap authority | PM=roadmap/prioritization; PO=sprint backlog/acceptance; BA=requirements elicitation as input to PM (no independent prioritization authority) |

### Critical Gaps

| # | Domain | No Owner | Impact |
|---|--------|----------|--------|
| 1 | **Incident management / commander** | No role owns incident declaration, cross-functional command, or postmortem ownership; SRE, SecOps, and Support act independently | P1 incidents will have five departments acting independently; MTTR severely degraded |
| 2 | **Enterprise risk management** | No role owns integrated risk register, risk appetite framework, or board-level risk reporting | Strategic, operational, and financial risks go untracked in aggregate; fundraising/compliance liability |
| 3 | **Pricing strategy and monetization** | No role owns pricing model design, packaging decisions, or pricing change governance; CPO and CMO claim informally; FP&A models but doesn't decide | Pricing decisions made ad hoc; Sales discounting misaligns with Finance margin targets over time |
| 4 | **Developer relations / external ecosystem** | Developer Experience Engineer (Platform) is scoped to internal developers only; no external API docs, developer community, or SDK owner | If product has external APIs/integrations, technical adoption stalls; no community owner |
| 5 | **Internal audit / financial controls** | Finance has Controller and FP&A; Legal has Compliance; no role owns internal audit (controls testing, fraud detection, SOX-equivalent) | Financial control failures undetected until external audit; material gap for fundraising, M&A due diligence, enterprise clients |
| 6 | **Customer lifecycle & retention strategy** | Client Success Manager handles accounts reactively; Growth Hacker handles acquisition; no role owns end-to-end lifecycle design, churn strategy, or NPS ownership | Churn addressed per-account rather than systemically; expansion revenue has no strategic owner |
| 7 | **Regulatory and government affairs** | Legal has Compliance and Privacy but no proactive regulatory monitoring, lobbying, or AI-regulatory engagement (EU AI Act, FTC, sector-specific) | AI-specific regulatory changes discovered reactively; no representation in comment periods |
| 8 | **OKR accountability enforcement** | OKR/Planning Coordinator owns process design but no role owns tracking, missed-check-in escalation, or cross-department dependency flagging | OKRs become shelfware within two quarters at 169-role scale |

### Escalation Dead-Ends

| Role | Issue |
|------|-------|
| Chief AI Officer | No defined arbiter vs. CTO when they conflict on AI infrastructure decisions; charter doesn't establish who resolves |
| AI Ethics Specialist | Reports into CAIO — the executive most incentivized to ship fast; ethics blocks have no independent escalation path outside CAIO's chain |
| General Counsel | No CEO or Board-level escalation rights documented; legal holds/no-go decisions have no override path if business leadership disagrees |
| Privacy Officer | No direct authority to compel product remediation; can only advise Legal if violation involves a product decision owned by CPO or data pipeline by Head of Data |
| Research Director | No C-suite seat; research outputs challenging CSO or CPO decisions have no escalation path if those executives reject findings |
| Head of Creative Technology | No defined reporting line in charter; sits between CTO, Head of Design, and CMO; budget and prioritization disputes have no resolver |
| Engineering Manager | Classified Human-Primary in file (see Check 4), suggesting strategic authority, but no defined escalation path above CTO for cross-team disputes |
| QA Auditor (HR) | Audits workforce quality but escalates only to CHRO — conflicted if finding implicates HR itself; needs independent escalation route to COO or CEO |

---

## Check 4: Classification Consistency

**Verdict:** 8 confirmed mismatches across 4 departments.

### Mismatch Table

| Role | Department | Charter Classification | File Classification | Severity |
|------|-----------|----------------------|--------------------|----|
| Research Director | research-intelligence | 🔄 Hybrid | 👤 Human-Primary | Medium — limits AI execution of research strategy |
| Engineering Manager | engineering | 🔄 Hybrid | 👤 Human-Primary | Medium — limits AI in team coordination/code review |
| Sales Director | sales | 🔄 Hybrid | 👤 Human-Primary | Medium — limits AI in pipeline strategy and forecasting |
| Sales Development Rep (SDR) | sales | 🤖 AI-Primary | 🔄 Hybrid | Low — conservative, reasonable for an outbound role |
| **AI Ethics Specialist** | ai-automation | 👤 Human-Primary | 🔄 Hybrid | **CRITICAL** — strips independence; ethics role must be human-led |
| AI/ML Engineer | ai-automation | 🔄 Hybrid | 🤖 AI-Primary | Medium — AI-Primary may be correct but creates supervision gap |
| AI Operations Engineer | ai-automation | 🔄 Hybrid | 🤖 AI-Primary | Medium — MLOps decisions may need more human oversight |
| Agent Developer | ai-automation | 🔄 Hybrid | 🤖 AI-Primary | Medium — agent design benefits from human architectural review |

**Most critical:** The AI Ethics Specialist downgrade from Human-Primary to Hybrid (in the AI & Automation department, reporting to CAIO) creates a structural conflict of interest. The charter's Human-Primary designation exists specifically to ensure this role has independence from the CAIO's delivery pressure.

### Classification Count Verification

| Department | Charter HP | File HP | Charter H | File H | Charter AI | File AI | Match? |
|-----------|-----------|---------|-----------|--------|-----------|---------|--------|
| research-intelligence | 0 | 1 | 3 | 2 | 5 | 5 | ✗ |
| strategy-business-dev | 1 | 1 | 5 | 5 | 2 | 2 | ✓ |
| finance-investor-relations | 1 | 1 | 4 | 4 | 4 | 4 | ✓ |
| marketing | 1 | 1 | 8 | 8 | 5 | 5 | ✓ |
| sales | 1 | 2 | 5 | 5 | 4 | 3 | ✗ |
| product | 1 | 1 | 5 | 5 | 3 | 3 | ✓ |
| design | 1 | 1 | 7 | 7 | 1 | 1 | ✓ |
| creative-technology | 1 | 1 | 11 | 8 | 0 | 0 | ✗ (3 missing files) |
| engineering | 1 | 2 | 10 | 9 | 1 | 1 | ✗ |
| ai-automation | 2 | 1 | 9 | 7 | 1 | 4 | ✗ |
| platform-engineering | 1 | 1 | 9 | 9 | 0 | 0 | ✓ |
| client-services | 1 | 1 | 6 | 6 | 1 | 1 | ✓ |
| operations | 1 | 1 | 4 | 4 | 2 | 2 | ✓ |
| legal-compliance | 1 | 1 | 4 | 4 | 1 | 1 | ✓ |
| support | 1 | 1 | 2 | 2 | 3 | 3 | ✓ |
| human-resources | 1 | 1 | 6 | 6 | 3 | 3 | ✓ |
| data-analytics | 1 | 1 | 5 | 5 | 2 | 2 | ✓ |
| quality-assurance | 1 | 1 | 7 | 7 | 3 | 3 | ✓ |

---

## Check 5: Naming Conventions

### File Name vs Charter Name Mismatches

| File | Charter Role Name | Severity |
|------|------------------|----------|
| `quality-assurance/qa-automation-engineer.md` | "Test Automation Engineer" | Medium — search by charter name won't find file |
| `quality-assurance/manual-qa-specialist.md` | "Manual QA Tester" | Medium — same discoverability issue |
| `strategy-business-dev/ma-analyst.md` | "M&A Analyst" | Low — acceptable special-char collapse |

### Same Title in Multiple Departments

| Role Title | Departments | Charter Design? |
|-----------|------------|----------------|
| AI/ML Engineer | engineering, ai-automation | Yes — charter lists it in both departments. But same title creates hiring confusion, PR ownership disputes, and unclear reporting. Rename one (see Check 3, Overlap #1) |

### Document Title Format
All role files use consistent section structure (Classification, Deployment, Version, Created metadata block). No encoding-corrupt files identified in sample (P1 handles this systematically).

### Naming Convention Summary
- File naming: kebab-case ✓ (all 170 files)
- Directory naming: kebab-case ✓ (all 19 dirs)
- Title format: `# [Role Name] — Role Template` ✓ (spot-checked sample)
- Cross-reference format: human-readable titles (recommend migrating to slugs)

---

## Summary

| Check | Status | Findings |
|-------|--------|----------|
| 1. Charter Completeness | ⚠️ ISSUES | 3 missing files (creative-technology), 4 phantom files (management dept) |
| 2. Role Reference Validity | ✅ PASS | No invalid references; format standardization recommended |
| 3. Responsibility Overlaps/Gaps | ⚠️ ISSUES | 10 critical overlaps, 8 critical gaps, 8 escalation dead-ends |
| 4. Classification Consistency | ❌ FAIL | 8 mismatches; AI Ethics Specialist critical |
| 5. Naming Conventions | ⚠️ ISSUES | 2 QA file names diverge from charter; 1 duplicate title across depts |

**Total issues:** 3 missing files + 4 phantom files + 10 overlaps + 8 gaps + 8 escalation dead-ends + 8 classification mismatches + 2 naming mismatches = **43 findings**

### Recommended Actions (by priority)

1. **CRITICAL — Fix AI Ethics Specialist classification** (`ai-automation/ai-ethics-specialist.md`): restore to Human-Primary. This is a structural governance failure.
2. **HIGH — Resolve missing Creative Technology files**: create `real-time-graphics-engineer.md`, `technical-artist.md`, `immersive-experience-designer.md`
3. **HIGH — Resolve management/ department**: either add "Management / Program Office" to the charter or reclassify the 4 coordinator files into existing departments
4. **HIGH — Define incident command role**: add an Incident Commander role (or assign formally to SRE) with cross-departmental authority during production incidents
5. **HIGH — Add enterprise risk management**: add a Risk Manager or VP of Risk role; assign board-level risk reporting
6. **MEDIUM — Fix remaining 7 classification mismatches**: update Research Director, Engineering Manager, Sales Director, SDR, AI/ML Engineer (AI dept), AI Operations Engineer, Agent Developer
7. **MEDIUM — Rename duplicate AI/ML Engineer titles**: Engineering dept → "ML Infrastructure Engineer"; AI & Automation dept → "Applied AI Engineer"
8. **MEDIUM — Fix QA naming mismatches**: rename `qa-automation-engineer.md` → `test-automation-engineer.md`, `manual-qa-specialist.md` → `manual-qa-tester.md`
9. **MEDIUM — Add pricing strategy ownership**: define who owns pricing model design and packaging decisions
10. **LOW — Standardize cross-references to slugs**: across all 170 role files for programmatic validation

---

*Generated by P3 audit pass. Findings stored in pocket-pick: tags `roles-p3`, `cross-role-consistency`.*
