# Human playtesting and readiness

Automated checks can detect crashes, missing resources, invalid saves, and some input/state regressions. They do not establish fun, emotional response, difficulty fairness, fatigue, or market fit. Human feedback is a distinct evidence source, not a box filled by another model.

## A small useful session

Prepare a local build or launch instructions and a short scenario. Ask for permission before sharing private builds or recruiting/contacting testers. For an early pass, one fresh player can expose obvious confusion, but do not generalize their opinion to the market.

Give the player a goal rather than instructions for every control. Observe where they hesitate, misread feedback, fail, retry, or stop. Avoid coaching until needed to unblock the session. Ask afterwards what they thought the goal was, what felt responsive or confusing, and whether they wanted another attempt. Separate verbatim feedback from your interpretation. Obtain consent before recording people or collecting personal data.

Compare relevant evidence before and after: time to first meaningful action, unprompted control discovery, unnecessary menu detours, recoverable vs unrecoverable failures, and willingness to replay. Sample size and learning effects matter. Repeating the same scenario with the same player may measure familiarity rather than improved onboarding.

## A release decision needs broader coverage

Before recommending a release, identify evidence for the actual scope and platform:

- Fresh install/start, shutdown/relaunch, complete core loop, end state, and retry.
- Save/load compatibility, interrupted writes, settings persistence, missing/corrupt data recovery where applicable.
- Supported input devices and rebinding, focus loss, pause behavior, controller disconnect if supported.
- UI readability at supported sizes, contrast and non-color cues, reduced motion/flashing options where relevant, readable subtitles when needed.
- Audio balance, mute/pause behavior, repetitive effects, and licensing/provenance of shipped assets and fonts.
- Target-hardware performance, memory growth over a meaningful session, export correctness, and platform-specific requirements.

Choose checks appropriate to the game. Record untested areas explicitly. A polished vertical slice is not proof that all levels, save paths, localization, storefront requirements, or supported platforms are release-ready.
