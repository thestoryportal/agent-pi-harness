# Enrichment Proposals — marketing — 2026-04-17

## Brand Strategist
**File:** `~/.claude/roles/marketing/brand-strategist.md`
**JD sources used:** brand-strategist.md
**JD tiers:** STRONG: 1, GOOD: 0, WEAK: 0

### Required Context
**No change** — existing five items already cover strategic direction, competitive landscape, audience insights, prior brand assets, and founder narrative. JD adds no sharper signal.

### Key Priorities
**Add:**
- `Conduct competitive teardown (positioning, pricing, creative, tone) before finalizing differentiation` — *source: brand-strategist.md, reason: JD explicitly calls out competitive research as a distinct input to positioning; current bullets assume it but don't name it*

**Edit:**
- OLD: `Define voice attributes and usage examples` → NEW: `Define voice attributes with approved terminology, slogans, and do/don't examples` — *reason: JD specifies voice guidelines cover "terminology and slogans"; sharper artifact list*

### Quality Bar
**No change** — existing 5-row table is measurable and role-specific. No numeric thresholds in JD to lift.

---

## Chief Marketing Officer
**File:** `~/.claude/roles/marketing/chief-marketing-officer.md`
**JD sources used:** Chief Marketing Officer (CMO).md, marketing-officer.md
**JD tiers:** STRONG: 1, GOOD: 2, WEAK: 0

### Required Context
**Add:**
- `- [ ] Marketing technology stack inventory and attribution model in use` — *source: Chief Marketing Officer (CMO).md, reason: JD's Growth/Digital templates consistently require visibility into martech stack and attribution before any CMO decisions*

### Key Priorities
**Add:**
- `Stand up a marketing attribution model (multi-touch or MMM) so budget decisions are defensible` — *source: Chief Marketing Officer (CMO).md, reason: JD lists "marketing attribution and analytics" as a core responsibility across all CMO templates; current priorities address spend review but not attribution*

**Edit:**
- OLD: `Hire or contract the highest-leverage role first` → NEW: `Hire or contract the highest-leverage role first (typically demand gen or content for early-stage)` — *reason: JD's Growth vs. Brand templates make the first-hire choice explicit; a pointer is more actionable*

### Quality Bar
**Add:**
- `| **LTV/CAC** | Ratio tracked quarterly; payback period within target band |` — *source: Chief Marketing Officer (CMO).md, reason: JD consistently cites CAC payback and LTV/CAC as CMO success metrics; adds numeric gate*

---

## Content Marketing Manager
**File:** `~/.claude/roles/marketing/content-marketing-manager.md`
**JD sources used:** Content Marketing Manager.md, content-manager.md, director-of-content-marketing.md
**JD tiers:** STRONG: 1, GOOD: 5, WEAK: 0

### Required Context
**No change** — existing five items cover priorities, brand, personas, editorial calendar, and SEO targets. JD adds no missing input.

### Key Priorities
**Add:**
- `Map content to buyer-journey stages (awareness, consideration, decision) with dedicated formats per stage` — *source: Content Marketing Manager.md, reason: JD explicitly names "content for all stages of the buyer's journey" across templates; current bullets are pillar-centric, not stage-centric*

### Quality Bar
**No change** — the five existing gates (Usefulness, Originality, SEO Hygiene, Brand Fit, Performance) are measurable and role-specific. No additional numeric thresholds warranted.

---

## Email Marketing Specialist
**File:** `~/.claude/roles/marketing/email-marketing-specialist.md`
**JD sources used:** Email Marketing Specialist.md, Email Marketing Manager.md, marketing-specialist.md
**JD tiers:** STRONG: 1, GOOD: 3, WEAK: 0

### Required Context
**No change** — existing seven items already name SPF/DKIM/DMARC, ESP, CAN-SPAM/GDPR/CASL, and baseline rates. Already above the 4-7 sweet spot; no further adds warranted.

### Key Priorities
**No change** — existing five bullets (authentication, welcome flow, segmentation, test plan, cadence) cover first-release work completely. JD content largely duplicates.

### Quality Bar
**No change** — existing five rows are specific and measurable (deliverability, authentication, opt-in hygiene, engagement, compliance).

---

## Event Marketing Manager
**File:** `~/.claude/roles/marketing/event-marketing-manager.md`
**JD sources used:** Event Marketing Specialist.md, Marketing Manager.md
**JD tiers:** STRONG: 0, GOOD: 3, WEAK: 0

### Required Context
**No change** — existing items cover budget, brand, event calendar, ROI baseline, and ICP. Complete.

### Key Priorities
**No change** — existing five bullets (scored calendar, booth package, capture pipeline, nurture, ROI targets) cover first-release cleanly.

### Quality Bar
**No change** — existing five rows already specify numeric windows (two weeks out, 48-hour nurture, 30-day ROI review).

---

## Growth Hacker
**File:** `~/.claude/roles/marketing/growth-hacker.md`
**JD sources used:** Demand Generation Manager.md, Growth Marketing Manager.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (skipped)

Skip — WEAK matches only, insufficient signal. Existing content already names funnel stages, north-star, cohort/retention, and experiment cadence with specifics that a WEAK JD cannot sharpen.

---

## Marketing Analyst
**File:** `~/.claude/roles/marketing/marketing-analyst.md`
**JD sources used:** Marketing Analyst.md, Marketing Data Analyst.md
**JD tiers:** STRONG: 1, GOOD: 2, WEAK: 0

### Required Context
**Add:**
- `- [ ] SQL access to the data warehouse or marketing DB for custom analysis` — *source: Marketing Analyst.md, reason: JD lists SQL + warehouse (Snowflake, BigQuery) as core requirements across all three context templates; current context lists platform data but not direct warehouse access*

### Key Priorities
**Add:**
- `Build a cohort view of CAC, LTV, and retention by acquisition channel before any media-mix recommendations` — *source: Marketing Analyst.md, reason: JD's in-house and startup templates both name cohort analysis and customer-lifecycle analytics as core deliverables; current bullets focus on tracking/dashboards but omit cohorting*

### Quality Bar
**No change** — existing gates (Data Quality, Definition Clarity, Actionability, Reproducibility, Honesty) are strong and role-specific.

---

## Marketing Copywriter
**File:** `~/.claude/roles/marketing/marketing-copywriter.md`
**JD sources used:** marketing-copywriter.md, Copywriter.md
**JD tiers:** STRONG: 1, GOOD: 2, WEAK: 0

### Required Context
**No change** — existing seven items already cover brief, voice, deliverables, research, prior A/B results, competitor samples, and legal constraints. Above sweet-spot length; further adds would pad.

### Key Priorities
**No change** — existing five priorities (voice codification, value-prop bank, brief template, copy library, weekly testing) are complete and concrete.

### Quality Bar
**No change** — existing five gates are falsifiable and cite specific anchors (five-second comprehension, documented tone guide, supported claims).

---

## Marketing Designer
**File:** `~/.claude/roles/marketing/marketing-designer.md`
**JD sources used:** junior-designer.md, marketing-intern.md
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**No change** — existing five items cover guidelines, brief, copy, platform specs, and asset inventory. JDs are generic designer roles and add no marketing-specific delta.

### Key Priorities
**No change** — existing five priorities (asset library, master templates, intake format, approval chain, versioning) are concrete.

### Quality Bar
**No change** — existing gates already cite WCAG AA contrast; JDs provide no numeric thresholds to add.

---

## Marketing Research Lead
**File:** `~/.claude/roles/marketing/marketing-research-lead.md`
**JD sources used:** marketing-intern.md
**JD tiers:** STRONG: 0, GOOD: 1, WEAK: 0

### Required Context
**No change** — existing six items cover brief, performance data, prior research, CI data, market sizing, and survey infrastructure. JD (intern) adds no relevant signal.

### Key Priorities
**No change** — existing five priorities (personas, teardown, TAM/SAM/SOM, VOC synthesis, repository) are first-release appropriate and concrete.

### Quality Bar
**No change** — existing gates (Evidence, Sampling, Actionability, Reproducibility, Freshness) are strong.

---

## Performance Marketing Manager
**File:** `~/.claude/roles/marketing/performance-marketing-manager.md`
**JD sources used:** Marketing Manager.md, marketing-intern.md
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**No change** — existing five items (budget, ICP, creative, copy, attribution setup) are complete.

### Key Priorities
**No change** — existing five bullets (tracking before spend, CAC/LTV bands, 2-3 channel test, creative pipeline, kill/scale rules) are concrete.

### Quality Bar
**No change** — existing gates are falsifiable and name specific mechanics (reconciled conversion data, defensible attribution, UTM conventions).

---

## PR / Communications Manager
**File:** `~/.claude/roles/marketing/pr-communications-manager.md`
**JD sources used:** public-relations-manager.md, public-relations-intern.md
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**No change** — existing five items (calendar, messaging, product news, press list, crisis playbook) are complete.

### Key Priorities
**No change** — existing priorities (press list, narrative, crisis playbook, launch moments, coverage tracker) are role-appropriate.

### Quality Bar
**No change** — existing gates are specific (verifiable facts, tailored outreach, SLA responses, pre-drafted holding statements).

---

## SEO/SEM Specialist
**File:** `~/.claude/roles/marketing/seo-sem-specialist.md`
**JD sources used:** junior-sem-seo-specialist.md, search-engine-marketing-(sem)-specialist.md, SEO Specialist.md
**JD tiers:** STRONG: 1, GOOD: 2, WEAK: 0

### Required Context
**No change** — existing seven items already name SEMrush/Ahrefs, Search Console, Google Ads structure, Screaming Frog crawl, and competitor list. Already at sweet-spot ceiling.

### Key Priorities
**No change** — existing five priorities (technical audit, keyword universe, content alignment, tracking, SEM structure) are concrete.

### Quality Bar
**No change** — existing gates cite Core Web Vitals, schema validation, wasted-spend threshold — all role-specific.

---

## Social Media Manager
**File:** `~/.claude/roles/marketing/social-media-manager.md`
**JD sources used:** Social Media Manager.md, social-media-strategist.md, social-media-analyst.md, social-media-coordinator.md, social-media-copywriter.md, Social Media Specialist.md
**JD tiers:** STRONG: 1, GOOD: 5, WEAK: 0

### Required Context
**No change** — existing five items (content plan, guidelines, assets, platforms + SLAs, baselines) are complete and specific.

### Key Priorities
**No change** — existing priorities (handles, calendar, pillars + voice, community SLAs, weekly analytics) cover founding work cleanly.

### Quality Bar
**No change** — existing gates are role-specific and falsifiable (voice match, SLA reply times, pillar + objective tagging, safety check).

---
