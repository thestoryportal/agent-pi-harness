# Enrichment Proposals — platform-engineering — 2026-04-17

## CI/CD Engineer
**File:** `~/.claude/roles/platform-engineering/cicd-engineer.md`
**JD sources used:** *Only WEAK match (DevOps Engineer.md) available; skimmed for deltas — no distinct content absent from existing appendix*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 1

Skip — WEAK matches only, content too generic. The role already cites GitHub Actions patterns, preview deployments, lint/type-check/bundle-size gates, dependency/secret/SAST scanning, build-time targets (<10 min), and artifact parity. The DevOps Engineer JD repeats this material without sharper artifacts.

---

## Database Administrator
**File:** `~/.claude/roles/platform-engineering/database-administrator.md`
**JD sources used:** Database Administrator.md
**JD tiers:** STRONG: 1, GOOD: 0, WEAK: 0

### Required Context
**Add:**
- `- [ ] High-availability / replication topology (if any)` — *source: Database Administrator.md, reason: JD names clustering, replication, failover as explicit responsibilities; role Quality Bar targets uptime but context omits HA topology*
- `- [ ] Compliance obligations on stored data (GDPR, HIPAA, SOX)` — *source: Database Administrator.md, reason: JD explicitly names compliance scope; role currently omits this constraint from context*

**Edit:** *No edit — existing six items are tight access/artifact phrases.*

**No change** on remainder.

### Key Priorities
**Add:**
- `Configure encryption at rest and in transit on every environment holding production data` — *source: Database Administrator.md, reason: JD explicitly calls out encryption as core; role currently cites backups and index tuning but not encryption posture*

**Edit:** *No edit — existing five bullets are imperative with concrete artifacts (slow-query monitoring, connection-pool sizing, DBA review).*

**No change** on remainder. Note: adds one bullet bringing total to 6, within the 4-6 style-guide range.

### Quality Bar
**Add:** *None — 5 rows with falsifiable criteria (p50 <100ms, p95 <500ms, RTO/RPO drills).*

**Edit:** *No edit.*

**No change** — table is well-anchored.

---

## Developer Experience Engineer
**File:** `~/.claude/roles/platform-engineering/developer-experience-engineer.md`
**JD sources used:** *Only WEAK matches (Technical Writer.md, DevOps Engineer.md) — both domain-adjacent*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

Skip — WEAK matches only, content too generic. Role already cites setup scripts, contributing guides, editor settings, new-dev interviews, and time-to-first-commit targets. Technical Writer JD is docs-only; DevOps Engineer JD is infra-focused — neither maps cleanly to DX tooling.

---

## DevOps Research Lead
**File:** `~/.claude/roles/platform-engineering/devops-research-lead.md`
**JD sources used:** *Only WEAK matches (enterprise-architect.md, DevOps Engineer.md)*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

Skip — WEAK matches only, content too generic. The role's existing appendix already cites evaluation workflow, POC + criteria framework, Adopt/Trial/Hold/Reject output, and research archive — sharper than either WEAK JD.

---

## Head of Platform Engineering
**File:** `~/.claude/roles/platform-engineering/head-of-platform-engineering.md`
**JD sources used:** *Only WEAK matches (director-of-engineering.md, it-director.md)*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

Skip — WEAK matches only, content too generic. Existing content covers Platform roadmap, ownership clarity, internal-customer feedback loop, Platform OKRs, and org-wide quality standards with falsifiable Quality Bar gates. Generic director JDs would not sharpen it.

---

## Infrastructure Engineer
**File:** `~/.claude/roles/platform-engineering/infrastructure-engineer.md`
**JD sources used:** *Only WEAK matches (Cloud Architect.md, DevOps Engineer.md, Google Cloud Engineer.md) — skimmed; role already concrete*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 3

Skip — WEAK matches only, content too generic. Role already cites IaC, staging + production parity, secrets with scoped access + rotation, preview deployments, and standard security headers (HSTS, CSP, X-Frame-Options). The WEAK JDs do not provide sharper cloud-neutral artifacts.

---

## Release Manager
**File:** `~/.claude/roles/platform-engineering/release-manager.md`
**JD sources used:** *Only WEAK matches (Program Manager.md, DevOps Engineer.md)*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

Skip — WEAK matches only, content too generic. Role already names semantic versioning, Keep-a-Changelog style, block/warn gate policy, rollback rehearsal, and cross-team coordination ownership. Program Manager JD is project-mgmt generic; DevOps JD is infra-focused.

---

## Repository Manager
**File:** `~/.claude/roles/platform-engineering/repository-manager.md`
**JD sources used:** *Only WEAK match (DevOps Engineer.md)*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 1

Skip — WEAK matches only, content too generic. Role already cites Conventional Commits, CODEOWNERS, PR/issue templates, branch protection (required checks, linear-history rules), and pre-commit secret scanning. DevOps JD does not cover repo-hygiene artifacts specifically.

---

## Security Operations Engineer
**File:** `~/.claude/roles/platform-engineering/security-operations-engineer.md`
**JD sources used:** operations-engineer.md, security-engineer.md
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**Add:**
- `- [ ] WAF configuration and rule access` — *source: security-engineer.md, reason: JD explicitly names WAF configuration as core security ops work; missing from current context list*
- `- [ ] Network segmentation diagram (if multi-environment)` — *source: security-engineer.md, reason: JD names network segregation; `(if multi-environment)` follows style-guide conditional suffix*

**Edit:** *No edit — existing six items cover secrets, CI/CD configs, scanners, security logs, policies, and release schedule.*

**No change** on remainder.

### Key Priorities
**Add:** *None — five bullets cover secrets centralization, PR gating, pre-commit hooks, rotation runbooks, and incident-response partnership.*

**Edit:** *No edit — bullets pair imperative with concrete output.*

**No change** — within 4-6 range.

### Quality Bar
**Add:** *None — 5 rows with falsifiable criteria (zero secrets in repo/logs, high/critical CVE block, scan coverage every PR, tested compromise playbook, alert fatigue tracked).*

**Edit:** *No edit.*

**No change** — table is well-anchored.

---

## Site Reliability Engineer
**File:** `~/.claude/roles/platform-engineering/site-reliability-engineer.md`
**JD sources used:** site-reliability-engineer.md
**JD tiers:** STRONG: 1, GOOD: 0, WEAK: 0

### Required Context
**Add:** *None — existing seven items already cover architecture, environments, monitoring, incident history, on-call, stakeholders, and SLOs. JD (Workable template) is thinner than the current list.*

**Edit:** *No edit.*

**No change** — role is one of the four style-guide sample files.

### Key Priorities
**Add:** *None — five bullets are the style-guide reference (error tracking/RUM, SLI/SLO dashboard, alert thresholds, runbooks, on-call rotation).*

**Edit:** *No edit.*

**No change** — sample file; enrichment would regress it.

### Quality Bar
**Add:** *None — 5 rows are the style-guide reference for the observable-anchor pattern.*

**Edit:** *No edit.*

**No change** — sample file.

---
