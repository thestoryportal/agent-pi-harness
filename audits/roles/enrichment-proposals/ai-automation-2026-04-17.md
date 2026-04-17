# Enrichment Proposals — ai-automation — 2026-04-17

## Agent Developer
**File:** `~/.claude/roles/ai-automation/agent-developer.md`
**JD sources used:** Generative AI Developer.md, AI Engineer.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 3 (2 read, Software Engineer.md skipped as generic)

### Required Context
**Add:**
- `- [ ] Vector database access` — *source: Generative AI Developer.md, reason: JD names Pinecone/Weaviate/Qdrant as core GenAI RAG infra; current context lacks retrieval-layer credentials*

**No edit** (existing 7 items are already concrete and tightly scoped to agent work)

### Key Priorities
**Add:**
- `Implement guardrails and output filters (PII redaction, prompt-injection defense) before external tool execution` — *source: Generative AI Developer.md, reason: JD lists "guardrails and safety measures" as key responsibility; current priorities cover bounds/checkpoints but not input/output filters*

**Edit:**
- OLD: `Build core tool library with tested error handling` → NEW: `Build core tool library with typed schemas, tested error handling, and per-tool timeout/retry policy` — *reason: JD stresses production-ready patterns; adds the concrete tool-surface discipline*

### Quality Bar
**Add:**
- `| **Cost per task** | Inference cost tracked per run; flagged when above budget threshold |` — *source: Generative AI Developer.md, reason: JD names "cost optimization" through caching/batching; current gates cover safety/reliability but not cost discipline; net add — reviewer to retire one existing row (candidate: Documentation, which overlaps with Required Context artifacts) if 5-row ceiling holds*

**No edit** (existing 5 gates are already falsifiable)

---

## AI Enablement Specialist
**File:** `~/.claude/roles/ai-automation/ai-enablement-specialist.md`
**JD sources used:** AI Implementation Specialist.md, AI Trainer.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

### Required Context
**Add:**
- `- [ ] Change-management playbook` — *source: AI Implementation Specialist.md, reason: JD names change management + pilot-to-rollout framework as core skill; current context lists tool inventory but not rollout methodology*

**Edit:**
- OLD: `- [ ] Existing AI use cases and success stories` → NEW: `- [ ] Existing AI use cases with measured ROI and adoption metrics` — *reason: JD stresses ROI/adoption measurement; sharpens vague "success stories"*

### Key Priorities
**Add:**
- `Establish pilot-to-rollout playbook with success criteria, ROI capture, and sunset gate per use case` — *source: AI Implementation Specialist.md, reason: JD emphasises pilot programs and measurable business impact; current priorities cover curriculum and library but not the deployment lifecycle*

**No edit** (existing 5 priorities cover inventory, curriculum, library, use cases, safety)

### Quality Bar
**Add:**
- `| **Activation rate** | 70%+ of trained users active in tool within 30 days |` — *source: AI Implementation Specialist.md, reason: JD names adoption monitoring as success criterion; adds a falsifiable numeric threshold; net add — paired with Edit below that repurposes "Adoption" row, so row count stays at 5*

**Edit:**
- OLD: `| Adoption | Tools in active use within 30 days of rollout |` → NEW: `| Adoption | >60% of target users active monthly; churn reason captured for drop-offs |` — *reason: JD stresses adoption tracking and reason-capture; replaces single-point "in active use" with ongoing threshold + diagnostic*

---

## AI Ethics Specialist
**File:** `~/.claude/roles/ai-automation/ai-ethics-specialist.md`
**JD sources used:** AI Ethics Officer.md, ai-ethics-researcher.md
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**Add:**
- `- [ ] Fairness-testing toolkit access` — *source: AI Ethics Officer.md, reason: JD names Fairlearn/AI Fairness 360/What-If Tool; current context lists "Fairness metrics" but not the tooling*
- `- [ ] Regulatory mapping per regime` — *source: AI Ethics Officer.md, reason: JD lists EU AI Act, NIST AI RMF, ISO/IEC 42001 as required knowledge; current context says "regulatory requirements" generically*

**No edit** (existing 5 items adequately bracket ethics inputs)

### Key Priorities
**Add:**
- `Publish model cards and transparency documentation for every user-facing AI feature before GA` — *source: AI Ethics Officer.md, reason: JD names model cards explicitly; current priorities stop at consent patterns*

**Edit:**
- OLD: `Establish bias and fairness evaluation for user-facing models` → NEW: `Establish bias and fairness evaluation with Fairlearn or AI Fairness 360 across demographic slices on every user-facing model` — *reason: JD names the tooling and slice-level requirement; tightens generic "fairness evaluation"*

### Quality Bar
**Add:**
- `| **Incident response** | Ethics incident triaged and remediated within 72 hours of report |` — *source: AI Ethics Officer.md, reason: JD Template 1 lists "incident response for AI-related ethical concerns"; current gates omit response SLA; net add — reviewer to retire one existing row (candidate: Safety, partly subsumed by this response-SLA row) if 5-row ceiling holds*

**No edit** (existing 5 gates are already concrete)

---

## AI/ML Engineer
**File:** `~/.claude/roles/ai-automation/ai-ml-engineer.md`
**JD sources used:** AI Engineer.md, Machine Learning Engineer.md
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**No change** — existing 7 items already cite labeled datasets, feature store, MLflow/W&B, experiment-tracking, privacy constraints, drift hooks. JD offered no sharper additions beyond what is already listed; existing Required Context is more complete than the JD itself.

### Key Priorities
**Add:**
- `Put model retraining automation in place with data-drift triggers and human-review gate` — *source: Machine Learning Engineer.md, reason: JD lists "automated retraining and validation" as key responsibility; current priorities cover monitoring but not the retraining loop*

**Edit:**
- OLD: `Stand up training, evaluation, and experiment-tracking infrastructure` → NEW: `Stand up training, evaluation, and experiment-tracking infrastructure on MLflow or Weights & Biases with versioned datasets` — *reason: JD names these tools and stresses versioning; names the tools + dataset discipline already referenced in Required Context*

### Quality Bar
**Add:**
- `| **Model card** | Intended use, limitations, and training data documented before production |` — *source: Machine Learning Engineer.md + AI Engineer.md, reason: Documentation row exists but is generic; model card is the industry-standard artifact; net add — paired with the Swap below that repurposes the "Documentation" row, so row count stays at 5*

**Swap (not a sharpening):**
- OLD: `| Documentation | Model card with intended use and limitations |` → NEW: `| Documentation | Runbook, rollback procedure, and on-call owner documented at deploy time |` — *reason: existing text is already specific (not vague), so this is a topic swap rather than a sharpening; the new Model-card row above absorbs the original content, freeing the Documentation row to cover operational deploy artifacts that are currently absent. Reviewer should accept the swap or keep the existing row and drop the Model-card add instead.*

---

## AI Operations Engineer
**File:** `~/.claude/roles/ai-automation/ai-operations-engineer.md`
**JD sources used:** AI Engineer.md, ai-operations-manager.md, operations-engineer.md
**JD tiers:** STRONG: 0, GOOD: 3, WEAK: 0

### Required Context
**Add:**
- `- [ ] GPU cluster and autoscaler config` — *source: AI Engineer.md, reason: JD names GPU/inference infra; current context lists observability stack but not the compute layer beyond a mention*

**No edit** (existing 7 items already cite model artifacts, SLAs, infra inventory, budget, observability stack, runbooks, compliance)

### Key Priorities
**Add:**
- `Publish on-call rotation with escalation tree and postmortem template for model incidents` — *source: ai-operations-manager.md + AI Engineer.md, reason: JD names operational management and incident handling; current priorities mention runbooks/escalation but not the on-call rotation*

**Edit:**
- OLD: `Put cost controls and budget alerts in place` → NEW: `Put token-usage caps, per-model budget alerts, and anomaly detection on inference spend` — *reason: JD lists token-usage caps and anomaly alerts explicitly (in existing Required Context); names the three concrete controls*

### Quality Bar
**Add:**
- `| **MTTR** | Median time to restore service <30 min for critical model endpoints |` — *source: ai-operations-manager.md, reason: JD emphasises operational efficiency; adds numeric recovery SLA absent from current gates; net add — reviewer to retire one existing row (candidate: Recovery, which is less falsifiable than this MTTR row) if 5-row ceiling holds*

**No edit** (existing 5 gates are already falsifiable)

---

## AI Research Lead
**File:** `~/.claude/roles/ai-automation/ai-research-lead.md`
**JD sources used:** ai-research-scientist.md
**JD tiers:** STRONG: 0, GOOD: 1, WEAK: 0

### Required Context
**Add:**
- `- [ ] Quarterly compute budget and GPU-hour allocation` — *source: ai-research-scientist.md, reason: JD expects large-scale experimentation; current context lists technical constraints but not the compute-budget envelope*

**No edit** (existing 5 items adequately bracket research inputs)

### Key Priorities
**Add:**
- `Publish quarterly research summary with production-relevant findings and adoption recommendations for engineering` — *source: ai-research-scientist.md, reason: JD lists publication and knowledge transfer; current priorities cover handoff criteria but not the cadence artifact*

**No edit** (existing 5 priorities cover mapping, infra, literature, handoff, early-warning)

### Quality Bar
**Add:**
- `| **Transfer cadence** | At least one research finding piloted in production per quarter |` — *source: ai-research-scientist.md, reason: JD stresses practical application of research; adds a measurable transfer rate absent from current gates; net add — reviewer to retire one existing row (candidate: Transfer, which is less falsifiable than this row that replaces it) if 5-row ceiling holds*

**No edit** (existing 5 gates are already falsifiable)

---

## AI Solutions Architect
**File:** `~/.claude/roles/ai-automation/ai-solutions-architect.md`
**JD sources used:** ai-architect.md, solutions-architect.md (404 — skipped)
**JD tiers:** STRONG: 0, GOOD: 2 (1 valid), WEAK: 0

### Required Context
**Add:**
- `- [ ] ADR template and repo path` — *source: ai-architect.md, reason: current Key Priorities reference ADR (architecture decision record) discipline but the template location is not in Required Context*

**No edit** (existing 7 items are already the strongest in the ai-automation set)

### Key Priorities
**Add:**
- `Validate every proposed architecture against build-vs-buy criteria and documented trade-off rationale` — *source: ai-architect.md, reason: JD names "build-vs-buy decisions" as responsibility; current priorities cover architecture drafting but not the decision discipline*

**No edit** (existing 5 priorities cover architecture, contracts, capacity, degradation, ADRs)

### Quality Bar
**Add:**
- `| **Ethical review** | Responsible-AI checklist signed before architecture handoff to implementation |` — *source: ai-architect.md, reason: JD lists ethical compliance as key responsibility; current gates lack the ethics checkpoint; net add — reviewer to retire one existing row (candidate: Reviewability, which is the weakest of the five) if 5-row ceiling holds*

**No edit** (existing 5 gates are already concrete)

---

## AI Trainer / Evaluator
**File:** `~/.claude/roles/ai-automation/ai-trainer-evaluator.md`
**JD sources used:** AI Trainer.md
**JD tiers:** STRONG: 0, GOOD: 1, WEAK: 0

### Required Context
**Add:**
- `- [ ] Adversarial prompt/red-team library` — *source: AI Trainer.md, reason: JD lists "red teaming exercises" as key responsibility; current context lists edge-case inventory but not adversarial sets*

**No edit** (existing 6 items are already specific and cite tools/datasets)

### Key Priorities
**Add:**
- `Run red-team evaluation on every release candidate to surface safety and jailbreak failures before ship` — *source: AI Trainer.md, reason: JD names red teaming; current priorities cover edge cases but not adversarial testing*

**Edit:**
- OLD: `Define quality metrics aligned to product outcomes` → NEW: `Define per-use-case quality rubrics (accuracy, safety, coherence, latency) with scoring guidelines for LLM-as-judge and human annotation` — *reason: JD stresses rubric design and both judge types (current Required Context already names both); names the four dimensions*

### Quality Bar
**Add:**
- `| **Inter-rater agreement** | Human annotator agreement >0.75 Cohen's kappa on gold set |` — *source: AI Trainer.md, reason: JD stresses annotation consistency; adds a numeric threshold absent from current gates; net add — reviewer to retire one existing row (candidate: Dataset hygiene, partly subsumed since agreement is itself a hygiene check) if 5-row ceiling holds*

**No edit** (existing 5 gates cover coverage, reproducibility, baseline, hygiene, reporting)

---

## Automation Engineer
**File:** `~/.claude/roles/ai-automation/automation-engineer.md`
**JD sources used:** QA Automation Engineer.md
**JD tiers:** STRONG: 0, GOOD: 1, WEAK: 0

### Required Context
**Add:**
- `- [ ] CI/CD pipeline access` — *source: QA Automation Engineer.md, reason: JD names Jenkins/GitHub Actions/GitLab CI/Azure DevOps as required platforms; current context covers automation platform (n8n/Zapier) but not the CI/CD integration*

**No edit** (existing 6 items adequately bracket automation-engineer inputs)

### Key Priorities
**Add:**
- `Integrate automation suite into CI/CD so broken workflows block deploy` — *source: QA Automation Engineer.md, reason: JD stresses CI/CD integration; current priorities cover standardization and observability but not deploy-gate wiring*

**No edit** (existing 5 priorities cover inventory, standardization, integrations, dashboards, documentation)

### Quality Bar
**Add:**
- `| **Flake rate** | Workflow false-failure rate <2% across 30 runs |` — *source: QA Automation Engineer.md, reason: QA domain stresses test reliability; adds a numeric reliability threshold specific to automation; net add — reviewer to retire one existing row (candidate: Reliability, subsumed by this more-specific flake-rate gate) if 5-row ceiling holds*

**No edit** (existing 5 gates cover reliability, observability, recovery, security, documentation)

---

## Chief AI Officer
**File:** `~/.claude/roles/ai-automation/chief-ai-officer.md`
**JD sources used:** Chief AI Officer (CAIO).md
**JD tiers:** STRONG: 1, GOOD: 0, WEAK: 0

### Required Context
**No change** — existing 7 items already cite strategy, CTO technical assessment, portfolio inventory, regulatory briefing, market intel, governance artifacts, and talent/budget. JD offered no sharper additions.

### Key Priorities
**Add:**
- `Publish AI literacy program covering fundamentals, prompting, and responsible-use policy for all employees` — *source: Chief AI Officer (CAIO).md, reason: JD Template 1 lists "AI literacy programs to upskill 10,000+ employees"; current priorities cover governance and staffing but not organization-wide enablement*

**Edit:**
- OLD: `Set budget and measure AI ROI across initiatives` → NEW: `Set AI budget with per-initiative ROI targets and quarterly portfolio review against those targets` — *reason: JD stresses ROI measurement with specific metrics; adds the review cadence and target discipline*

### Quality Bar
**Add:**
- `| **Regulatory posture** | EU AI Act, NIST AI RMF, and sector-specific obligations mapped with named owner |` — *source: Chief AI Officer (CAIO).md, reason: JD names regulatory compliance as CAIO responsibility; current gates cover governance generically but not regulatory mapping; net add — reviewer to retire one existing row (candidate: Risk posture, which partly subsumes this but lacks regulatory specifics) if 5-row ceiling holds*

**No edit** (existing 5 gates are already concrete)

---

## Conversational AI Designer
**File:** `~/.claude/roles/ai-automation/conversational-ai-designer.md`
**JD sources used:** Conversational AI Designer.md
**JD tiers:** STRONG: 1, GOOD: 1 (not read; STRONG covered span), WEAK: 0

### Required Context
**Add:**
- `- [ ] Conversation design tool access` — *source: Conversational AI Designer.md, reason: JD must-have: "experience with conversation design tools" (Voiceflow/Botmock/Dialogflow class); current context omits the authoring-tool access*
- `- [ ] Conversation analytics dashboard` — *source: Conversational AI Designer.md, reason: JD lists "conversation analytics dashboards" with intent-recognition accuracy and drop-off metrics as key responsibility; current context lists testing but not telemetry*

**No edit** (existing 5 items cover scope, brand, flows, persona, edge cases)

### Key Priorities
**Add:**
- `Design conversation handoff protocol to human agents for high-stakes or low-confidence turns` — *source: Conversational AI Designer.md, reason: JD Template 2 lists "conversation handoff protocols between AI and human agents"; current priorities cover error recovery but not escalation*

**No edit** (existing 5 priorities cover persona, flows, canonical copy, testing, guidelines)

### Quality Bar
**Add:**
- `| **Intent coverage** | >90% of production utterances map to a defined intent or fallback |` — *source: Conversational AI Designer.md, reason: JD stresses conversation coverage; adds a numeric threshold absent from current gates; net add — reviewer to retire one existing row (candidate: Flow coverage, partly subsumed by this more-falsifiable utterance-level gate) if 5-row ceiling holds*

**Edit:**
- OLD: `| Testing | Usability validated with target users |` → NEW: `| Testing | Usability validated with target users across voice and text channels per supported locale |` — *reason: JD Template 2 calls out multi-channel/multi-locale testing; sharpens single-path anchor*

---

## Prompt Engineer
**File:** `~/.claude/roles/ai-automation/prompt-engineer.md`
**JD sources used:** prompt-engineer.md (role-descriptions-2)
**JD tiers:** STRONG: 1, GOOD: 0, WEAK: 0

### Required Context
**Add:**
- `- [ ] Production prompt-serving logs` — *source: prompt-engineer.md, reason: JD names monitoring prompt performance as core duty; current context names previous attempts but not production telemetry or failure samples*

**No edit** (existing 5 items are already tightly scoped)

### Key Priorities
**Add:**
- `Run A/B tests on prompt variants and promote by measured quality delta with a defined guardrail window` — *source: prompt-engineer.md, reason: JD names performance analysis and refinement; current priorities cover evaluation harness but not promotion discipline*

**No edit** (existing 5 priorities cover library, baselines, eval harness, patterns, model selection)

### Quality Bar
**Add:**
- `| **Rollout safety** | Prompt changes gated by eval harness pass and a 48-hour canary before full traffic |` — *source: prompt-engineer.md, reason: JD stresses refinement and improvement cycle; adds a release-discipline gate absent from current 5 rows; net add — reviewer to retire one existing row (candidate: Evaluation, which partly overlaps with this) if 5-row ceiling holds*

**No edit** (existing 5 gates cover versioning, evaluation, token budget, reuse, documentation)

---
