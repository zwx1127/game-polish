# Design boundaries

## Why a skill plus a small CLI

The host dot already provides conversation, reasoning, delegation, a computer, and user approvals. Reimplementing those capabilities would add deployment, credential, cost, and maintenance burdens without proving that the game gets better. This project instead supplies reusable task guidance and deterministic evidence records.

The separation is deliberate:

- **Dot:** understands intent, selects experiments, reviews evidence, and communicates decisions.
- **Computer and gdx:** edit the project using existing access controls; gdx owns Godot control, interaction, and captures. Missing control capabilities belong in scoped gdx improvements, not a duplicate game-polish controller.
- **CLI:** validates local configuration, records bounded commands, and makes results inspectable.
- **Human player:** supplies evidence about comprehension, feel, fatigue, and enjoyment.

A structured report can help prevent forgotten checks. It cannot prove that captured media was honestly interpreted, that a player is representative, or that the game is commercially viable.

## Explicit non-goals

This initial package does not provide a new multi-agent platform, remote service, standalone continuous autonomous runner, metered model API integration, asset marketplace, automated publishing, generalized game-playing model, or universal quality score. It does not provide an OS sandbox. It does not promise commercial-quality output from an arbitrary prototype.

Godot is the practical first workflow, not a requirement to migrate existing games. Other engines can use explicit local checks and the same evidence loop, but engine-specific support must be tested before being claimed. A cross-engine shell command interface is not proof of cross-engine gameplay support.

## Cost uncertainty

Separate three things: assistant plan/usage limits, cloud-computer runtime/availability, and explicit external spend such as assets or services. The package cannot infer any of these prices from tool success. Record exposed usage and elapsed time; leave unexposed costs unknown. Do not present a per-game or per-pass dollar estimate as established without measured runs and current pricing.

Prefer a fixed experiment cap and checkpoints over an open-ended “keep polishing until great” objective. A budget buys attempts and evidence, not a guarantee of player satisfaction.

## Open-source boundary

The repository's software license covers its own code and documentation, subject to that license's terms. It does not confer rights to third-party games, art, fonts, music, trademarks, or generated assets. Keep private game content and captures out of public commits unless sharing is authorized. An open-source-ready local repository is not a published repository.

## Evidence needed before stronger claims

Validate the workflow on a real, authorized game: preserve the baseline, apply a small change, run automated checks, inspect actual captures, and ask a fresh player to try it. Repeat across different failure modes and at least the intended target hardware. Publish limitations alongside results only when publication is approved. Until then, describe this as an initial toolkit, not a demonstrated automated commercial-polish system.
