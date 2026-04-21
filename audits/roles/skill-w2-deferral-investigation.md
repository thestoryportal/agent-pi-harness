# W2 Playwright-Patterns — Deferral Investigation Notes

**Date:** 2026-04-18
**Deferred at:** Step 4 (CEO Review)
**Failure count:** 2
**Failure protocol:** 2 failures = deferral; sub-agent investigates; findings held for post-run review

---

## Failure Description

`mcp__just-prompt__ceo_and_board` produces a truncated CEO output file (`/tmp/ceo_decision.md`) on both runs. File ends mid-sentence inside the lowest-priority section of the Action Plan.

| Run | Lines | Truncation point |
|-----|-------|-----------------|
| 1 | 169 | "**P2 —" (mid-heading) |
| 2 | 177 | "13. Append claude's checklist additions (T" (mid-item) |

The board member analyses and the majority of the CEO action plan ARE captured. The truncation consistently falls at Priority 4 (lowest-priority checklist items).

---

## Root Cause Hypothesis

The just-prompt tool writes CEO model output to a file with what appears to be a character or token limit on the file write. The CEO model itself likely produces complete output, but the file writing is cut off around 169–177 lines. This is reproducible across two independent runs with the same prompt.

---

## Investigation Tasks for Sub-Agent

1. **Confirm root cause:** Is the truncation happening at the model level (CEO model output is incomplete) or at the file-write level (output is complete but file write is cut off)?
   - Check `/tmp/ceo_prompt.xml` to see if the CEO prompt includes the full board responses
   - Check if the `ceo_decision.md` file size is consistent with a file-write limit

2. **Find the limit:** What is the character/token threshold at which truncation occurs? (Run a minimal test with just-prompt that produces a long output)

3. **Identify a workaround:** Options to investigate:
   - Split the review into two passes (P1/P2 in pass 1, P3/P4 in pass 2) — preamble/context must be included in BOTH passes
   - Use `mcp__just-prompt__prompt_from_file_to_file` directly to the CEO model instead of `ceo_and_board` (bypasses the file-write limitation if it exists in the board wrapper) — preamble must stay
   - Read board member response files in `/tmp/` directly — they persist and contain the full model output even when CEO synthesis is truncated (proven recovery path)
   - NOTE: Do NOT remove the context preamble from the prompt. The board needs context (role, review questions, use case) to produce meaningful review output.

4. **Verify P4 content:** Read the board member response files in `/tmp/` to reconstruct what item 13 (checklist hardening) says, since that content exists in the board responses even if not in the CEO synthesis.

---

## Content State at Deferral

The CEO review produced actionable P1/P2/P3 content. If the tool limitation is resolved, W2 can resume at Step 5 using the captured content below.

### P1 — Runtime-breaking bugs (apply immediately when unblocked)

1. **Remove `>>` shadow DOM combinator.** It was removed in Playwright v1.27 and throws at runtime. Replace example with note that Playwright auto-pierces shadow roots; use `getByRole` or CSS locators directly.

2. **Fix `route.fulfill({ response, json })`.** This pattern silently fails to merge the JSON — only the original response body is used. Correct pattern:
   ```typescript
   await route.fulfill({
     response,
     contentType: 'application/json',
     body: JSON.stringify(json),
   });
   ```

3. **Fix `workers` config.** `workers: process.env.CI ? 1 : undefined` contradicts `fullyParallel: true`. With `fullyParallel: true`, use a percentage: `workers: process.env.CI ? '50%' : undefined` (or remove `workers: 1` entirely and let Playwright manage it).

### P2 — Flakiness/correctness (apply when unblocked)

4. Add `test.step` and `test.describe` organizational guidance.
5. Add `beforeAll` vs `beforeEach` tradeoff discussion.
6. Add `page.unroute()` and context-vs-page route scoping.
7. Clarify `expect.soft()` continuation semantics; clarify difference between `waitForURL` and `expect(page).toHaveURL()`.
8. Soften XPath blanket prohibition: "use only when semantic locators cannot express the query; document why."

### P3 — Coverage expansion (apply when unblocked)

9. Add Visual Regression Testing section (`expect(page).toHaveScreenshot()`).
10. Add `request` fixture section for direct API calls (distinct from `page.route()` mocking).
11. Add File upload/download patterns (`setInputFiles`, `waitForEvent('download')`).
12. Add dialog and popup/multi-tab handling (`page.on('dialog', ...)`, `page.waitForEvent('popup')`).

### P4 — Checklist hardening (RECOVERED from board response files)

13. Append the following checklist items from the `claude-sonnet-4-6` board review (items not already in the 18-item checklist):
    - [ ] `testDir` explicitly set (don't rely on default discovery)
    - [ ] Timeouts set at project level, not overridden ad-hoc in individual tests
    - [ ] No `page.evaluate()` used where locator API would suffice
    - [ ] Custom fixture types exported from a single `test.ts` entry point
    - [ ] Visual snapshot tests have a defined update workflow (`--update-snapshots` in a dedicated CI job)

---

## Investigation Findings (2026-04-18)

**Root cause confirmed:** The truncation is at the **file-write level**, not the model output level. The board member response files in `/tmp/` are ALSO truncated (claude-sonnet-4-6 board response ends at 334 lines, mid-sentence at `` `grep` tags (` ``). This confirms the `just-prompt` tool applies a file-write limit of ~169-335 lines depending on content density.

**P4 recovery:** Board response files were still present in `/tmp/`. P4 item 13 fully recovered by reading `/tmp/playwright-patterns-ceo-review_anthropic_claude-sonnet-4-6.md`.

**W2 status: UNBLOCKED** — all P1/P2/P3/P4 action items are now known. Proceeding to Steps 5-6 without re-running the CEO tool.

**For the infinite workflow spec:** The just-prompt `ceo_and_board` file-write limit is ~170-335 lines. Workaround: split long reviews into two passes (P1/P2 in pass 1, P3/P4 in pass 2), or reduce prompt file size, or use `prompt_from_file_to_file` directly with the CEO model.

---

## Resume Point

**UNBLOCKED** — P4 recovered from board response files.
- Step 1–3: Complete (skill draft at `~/.claude/skills/playwright-patterns.md`)
- Step 4: Complete (CEO action plan fully reconstructed — P1+P2+P3+P4)
- Step 5–6: Applying now

**pocket-pick:** skill-dev-walkthroughs-2026-04-17
