# Defense repository validation — 2026-11-18

## Actually rerun for this independent copy

| Check | Result |
|---|---|
| Original commit/archive | Commit 36044b4f57f1051360b369afe0f7976e4af070f0 verified; original ZIP SHA-256 743ba5cc552008d1e6b68c4df8ca06735a7822f1437d4c146ee39e09ad1f341e; all 1,037 source-file hashes verified against its internal provenance plus one package provenance entry |
| Evaluation integrity | PASS: 48 metric rows reconciled to confusion counts; 161 original evaluation/figure files checked byte-for-byte; ten editable tables; 56 research PNGs present |
| Extra aggregate chart recovery | Three local summary-chart PNGs match original figure-index hashes; CSV/SVG copies also recorded, no dataset files copied |
| Python | All 157 source files parsed; four installer/unit tests pass with genuine model installed locally |
| Controller | 11/11 pass using existing PyTorch environment; tiny synthetic CPU optimizer smoke test only, no research retraining |
| Flutter pub get | PASS, offline existing cache; locked dependencies preserved |
| Flutter analyze | PASS with --no-fatal-infos: zero errors/warnings, six Material import deprecation infos |
| Linux native codec | Clean rebuild PASS from copied source using existing CMake/Ninja/Zig compiler; no compiled binary committed |
| Real-model Flutter suite | 8 passed, 1 skipped optional screenshot capture; real TFLite classifier tests use genuine separately stored FP32 model and four original private development fixtures |
| Expanded preprocessing | PASS: exact Pillow-reference pixels on ten nonclinical generated cases, all eight EXIF orientations, landscape downscale and narrow portrait downscale |
| Source-only Flutter suite | 6 passed, 3 optional integration/capture tests skipped; model temporarily absent, then restored only to ignored local test workspace |
| PyTorch/TFLite parity | Four genuine fixed development fixtures pass original logits/probability tolerances; original PyTorch reference supplied externally, never committed |
| Missing-model behavior | Service raises explicit exception and remains retryable; UI reports model unavailable and disables Analyze; no fake predictions |
| Installation | SHA, size, TFLite signature, class metadata, exact positive install, idempotency, wrong/missing model rejection and existing-file preservation checked |
| Security/publication | Every indexed file inspected completely, type/hash recorded privately; no restricted artifacts, tokens or parameter arrays; detect-secrets indexed-file findings reviewed as provenance hashes/paths, upstream test constants and one historical status string |

Detailed logs are in docs/validation/. Tests initially encountered sandbox socket/cache restrictions and were rerun with approved access. Initial wrong-environment Python imports were rerun in the existing appropriate environments. Neither was a model/research failure.

The new narrow-image regression initially failed. Investigation found Pillow resize pass ordering; geometry.dart now follows vertical-first when height shrink exceeds twice width shrink. After correction all expanded cases and all original genuine TFLite fixture tolerances passed. No reference outputs, original metrics or tolerances were changed.

## Not run / not established

- Real macOS/Xcode iOS native-framework/app build. The old repository's CI failed because libjpeg received an empty CMAKE_SYSTEM_PROCESSOR. The new source explicitly passes ARM64; the iOS correction still requires Mac validation.
- Android SDK/NDK app build, physical iPhone/Android inference, Apple signing, camera/Photos byte behavior, AOT latency/memory and clinical validation.
- New research training, held-out evaluation, calibration, model selection or screenshot regeneration. Existing thesis results and approved figures are retained.
- Source-only CI intentionally skips model/native parity when separate local inputs are unavailable; local genuine parity evidence is retained above.

Fresh root history excludes all datasets and trained weights, including .tflite and .pt. The released ZIP archives committed files only and is extracted with per-file SHA-256 verification. Do not describe this project as a production-ready mobile deployment.
