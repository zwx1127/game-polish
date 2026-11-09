# Animation continuity and art consistency

Read when the requested improvement concerns animation, sprites, motion assets or art consistency. A static title image cannot substitute for an animation request.

## Choose an observed discontinuity

Inspect actual atlas frames, animation resources, state transitions and the running character before choosing a fix. Establish the existing palette, silhouette, proportions, sampling, lighting and identity constraints from the project. Distinguish source-pose variation, interpolation artifacts and state-machine jumps: each requires a different intervention. Prefer repairing the demonstrated cause over redrawing an entire cast.

For a bounded animation pass, identify the affected transition and compare continuous frames around it, not only attractive endpoints. Relevant examples include idle→move, stop/resume, interrupted attacks and loops. Check all affected directions and left/right phases, including the join back to the normal loop. Exercise several frame rates and unusually long frames; a modulo phase can hide a full cycle of progress. Preserve distance-driven movement timing unless the task explicitly changes it.

## Preserve identity and the actual asset pipeline

Keep original assets and a source hash manifest. Match the game's established art style rather than introducing an unrelated rendering style. For bitmap creation/editing, use the environment's image-generation guidance when available; do not regenerate each animation frame independently without identity/pose reference control. For code-native or motion-data assets, repair the native representation instead of generating an unrelated bitmap.

Trace which resource the runtime really loads. A changed source atlas or JSON is not integrated if the game still loads an old baked/native resource. Update only the affected generated resource, record the reproducible generation/bake command and versions, and verify the runtime-loaded resource. Do not rebuild the whole asset catalog to fix one character unless dependencies require it.

Retain unchanged source art and unaffected animation data where possible. Check the diff or hashes, not just a claim that a generator preserves them. For a changed asset include its original and candidate bytes or a verified reversible binary patch; a text-only patch cannot restore a binary animation resource.

## Observe a controlled sequence and gameplay

Use the same scene/state, direction, FPS, renderer, resolution and scripted input where supported. First verify that recorded outputs exist and inspect their actual frame count, duration and pixel dimensions (for example with ffprobe when available). A command's requested resolution can differ from the encoded video because project viewport settings override it; do not treat echoed request fields as measured media metadata. A fresh-scene deterministic recording is not a recording of the current daemon state. Disclose any timing/state mismatch rather than presenting arbitrary screenshots as paired frames.

Inspect both the animation review scene, when the project has one, and its real gameplay context. State/resource tests cannot detect every silhouette distortion, mid-transition pop or rendering artifact. Keep full recordings, then create clearly labeled crops, contact sheets or side-by-side clips from those frames. Preserve original time order; label slow motion or resampling, and do not redraw evidence frames.

Use localized pixel-change measures only as diagnostics with the crop, frame indices and interpretation recorded. A lower pixel difference can also mean frozen motion; verify that the intended movement and timing remain. Where feasible, compare unaffected regions and gameplay traces to bound regressions. Neither identical traces nor a few smooth frames prove all-game quality.

## Decision

Keep the change only when the affected continuity improves without unacceptable style/identity drift or gameplay regression. If middle frames remain unconvincing, revise/revert or label the candidate unaccepted. Scope the claim to the tested actor, transitions, directions, renderer and scenario. Retain target-renderer, target-hardware and human feel reviews as open items when not actually performed.
