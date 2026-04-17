```json
{
  "role": "mobile-qa-specialist",
  "department": "quality-assurance",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 5,
    "anti_pattern_quality": 8,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "All 6 principles are role-specific and not generic platitudes. 'Touch Is Not Click' and 'Real Devices Over Emulators' are genuinely distinct to mobile QA. The table format is terse though — the 'Meaning' column adds little beyond restating the principle name. 'Device Fragmentation Is Reality' means 'test across real device diversity' but doesn't explain why that matters or what failure looks like. Principles read as labels rather than convictions.",
      "example_rewrite": "| **Device Fragmentation Is Reality** | Android alone has 10,000+ active device models. A layout that works on a Pixel 7 can break on a Samsung Galaxy A14 due to manufacturer skin overrides, custom fonts, and display density differences. Test matrix must include at least one mid-tier Android with a manufacturer skin (Samsung One UI or Xiaomi MIUI) on every release. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff tables name roles correctly but artifacts are vague to the point of being non-actionable. 'Features ready for mobile testing' from QA Lead is not an artifact — it's a status. 'Mobile test results' delivered to QA Lead could mean anything from a Slack message to a 50-page report. No artifact format, file name convention, or tool (e.g., JIRA, TestRail, Notion) is specified. The Receives From table also omits the artifact from UI Designer — it says 'Mobile design specifications' without specifying format (Figma link? PDF? Component spec?).",
      "example_rewrite": "| Receives From | Artifact | Format |\n|---|---|---|\n| QA Lead | Mobile Test Assignment — list of user stories approved for mobile testing with device matrix scope | JIRA sprint board label 'Mobile-QA-Ready' |\n| UI Designer | Mobile Design Specification — annotated Figma frames showing touch target sizes, gesture zones, and breakpoint layouts | Figma share link pinned in #design-handoffs |\n| Mobile Developer | Testable Build — signed IPA (iOS) or APK/AAB (Android) with build number and changelog | Uploaded to BrowserStack App Automate or shared via TestFlight/Firebase |\n\n| Delivers To | Artifact | Format |\n|---|---|---|\n| QA Lead | Mobile Test Report — pass/fail by device, OS version, and scenario with linked bug tickets | TestRail run exported to Notion page in /QA/Mobile-Reports/ |\n| Mobile Developer | Platform Bug Report — reproducible steps, device/OS, screenshot or screen recording attached | JIRA ticket with label 'mobile-platform-specific' |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 8,
      "finding": "Six anti-patterns are present and all are specific to mobile QA — none are generic quality platitudes. 'Assume touch = click' and 'Skip orientation testing' are genuine mobile-specific failure modes. Minor deduction: 'Test only on emulators' and 'Test only flagship devices' are well-known enough in mobile QA that they border on obvious. The 'Instead' column could be more prescriptive — 'Use real devices' doesn't say how many or which ones. For a role file that defines a Device Matrix section, the anti-pattern should cross-reference it.",
      "example_rewrite": "| Don't | Why | Instead |\n|---|---|---|\n| Test only on emulators | Emulators cannot replicate manufacturer skins, actual touch latency, thermal throttling, or real-world storage pressure | Execute final validation on physical devices per the Device Matrix minimum — at least one real mid-tier Android with a manufacturer skin per release cycle |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol is present and correct for a Hybrid role. The AI/Human split is clearly articulated: AI plans and documents, human physically executes. CLI deployment rationale is given. However, the skill files are all marked 'planned development' — an AI agent loading this role has no actual skill content to reference for methodology. The three ALWAYS statements at the end of the Iteration Protocol are good but buried. An AI agent also has no guidance on what to do when a physical device is unavailable — the protocol doesn't handle that fallback state.",
      "example_rewrite": "Add a fallback block to the Iteration Protocol: 'IF physical device unavailable → STOP and notify human operator. Do NOT substitute emulator results for final validation. MAY use BrowserStack live session with human operator controlling the session remotely. Document any emulator-only results as PROVISIONAL — require physical device confirmation before closing ticket.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 9,
      "finding": "The Story Portal appendix is the strongest section in this file. Festival offline use as a PWA requirement is a specific, real constraint. The Wheel Component gesture challenge, WebGL mobile GPU concern, and audio recording permission flow are all Story Portal-specific — none of these would appear in a generic mobile QA template. Device priority table with rationale ('Primary festival attendee device') shows genuine product context. Minor gap: PWA Requirements table shows 'Audio recording offline' as High priority but the workflow section has no specific workflow for testing offline audio recording — the most complex and highest-risk mobile scenario has no step-by-step protocol.",
      "example_rewrite": "Add Workflow 4: Offline Audio Recording (Story Portal): 'TRIGGER: Audio recording feature ready for offline validation. 1. SETUP — Enable airplane mode on target device. Confirm PWA is installed to home screen. 2. RECORD — Open Story Portal PWA in standalone mode. Navigate to story recording flow. Initiate recording. Speak 10+ seconds of audio. Stop recording. Verify recording is saved locally (check storage indicator). 3. SYNC — Re-enable network. Verify upload queue activates. Confirm recording appears in story list with server-confirmed status. 4. EDGE CASES — Test recording interrupted by incoming call. Test storage-full condition. Test battery-low condition during recording. STOP → Document results per device. Report to QA Lead and Mobile Developer.'"
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. Every handoff currently names a role and a vague artifact category but specifies no format, no tool, and no file convention. An AI agent executing this role cannot produce 'Mobile test results' without knowing whether that means a TestRail export, a Notion page, a JIRA label, or a Slack message. Rewrite all handoff rows to include: (1) the specific artifact name, (2) the tool or location it lives in, and (3) the trigger that initiates the handoff — this will make the collaboration section actually executable rather than decorative."
}
```