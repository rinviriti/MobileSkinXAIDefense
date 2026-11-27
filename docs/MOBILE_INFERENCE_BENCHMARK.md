# MobileSkinXAI iOS inference benchmark

This **opt-in** integration test measures performance of the actual packaged native
preprocessing codec and verified FP32 TensorFlow Lite model. It does not train a
model, repeat accuracy evaluation, or implement Grad-CAM. No trained model or
private image is committed.

## Prerequisites

- Genuine `model_float32.tflite` installed by `scripts/install_model.py`.
- Native ARM64 `MobileSkinXaiCodec.xcframework` built and linked.
- Four development-validation JPEGs verified and installed locally. From the
  repository root:

```bash
python3 deployment/verification/prepare_goldens.py \
  --source-dir "$HOME/Desktop/MobileSkinXAI-Datasets/ISIC2019/images/ISIC_2019_Training_Input" \
  --device-assets
```

Do **not** replace original JPEGs with `rgb224` or `rgb320` preprocessed versions.
Original SHA-256 checksums must match `GOLDEN_REFERENCE.json`.

## Run on Riti's iPhone 18 Pro simulator (exploratory, debug mode)

Previously tested simulator: device ID
`0978F917-23B7-4438-A55C-24228375CE96` (iOS 27.0).

```bash
xcrun simctl list devices booted
# If not already booted, run the following:
xcrun simctl boot 0978F917-23B7-4438-A55C-24228375CE96
xcrun simctl bootstatus 0978F917-23B7-4438-A55C-24228375CE96 -b

cd ~/MobileSkinXAIDefense/app/flutter
flutter pub get
set -o pipefail
flutter test integration_test/inference_benchmark_test.dart \
  -d 0978F917-23B7-4438-A55C-24228375CE96 \
  --dart-define=MSX_BENCHMARK=true \
  --dart-define=MSX_DEVICE_KIND=simulator \
  --dart-define=MSX_DEVICE_NAME=iPhone_18_Pro \
  --reporter expanded 2>&1 | tee "$HOME/Desktop/MSX_Benchmark_iOS27_simulator.log"
```

If the simulator is already booted, skip the `xcrun simctl boot` command.
Do not pass `--profile` for an iOS Simulator; this is a **debug-mode** exploratory
measurement, not physical iPhone performance.

The test emits four `MSX_BENCHMARK_CASE_JSON=` lines (raw samples) and one
`MSX_BENCHMARK_SUMMARY_JSON=` line. A wrong checksum, out-of-tolerance model
output (absolute logit error > 0.001), or inference exception fails the test.

## Export machine-readable evidence

From the repository root, run:

```bash
cd ~/MobileSkinXAIDefense
python3 scripts/summarize_mobile_benchmark.py \
  "$HOME/Desktop/MSX_Benchmark_iOS27_simulator.log" \
  --out-dir "$HOME/Desktop/MobileSkinXAI-Benchmark"
```

Outputs: `benchmark_summary.json`, `benchmark_summary.csv`,
`benchmark_samples.csv`. The parser rejects incomplete runs rather than
silently reporting partial data.

## Measurement protocol

- **Four** checksum-verified ISIC development-validation images, one per
  ground-truth class (NV/MEL/BCC/SCC), loaded into memory before timing.
- **Model load** timed separately.
- **Five** untimed warm-up rounds across all four images (20 predictions).
- **Thirty** timed rounds across all four images (120 predictions), interleaved
  to reduce systematic time-order bias.
- **Model-only time:** measured inside `SkinClassifier.predictBytes` around
  `Interpreter.run`, excluding image preprocessing.
- **End-to-end time:** `predictBytes` wall-clock time after JPEG asset is
  preloaded; includes native JPEG decoding, resizing/padding, JPEG round-trip,
  normalization and inference, but excludes image selection, asset I/O, app
  startup, network and drawing results on the screen.
- Mean, median, **nearest-rank P95**, population standard deviation, minimum
  and maximum are reported for both timings, overall and per image.
- Process resident memory (`ProcessInfo.currentRss`) sampled before model
  load, after load, after warm-up, after completion, and after each measured
  prediction. This is not reliable peak memory: shared mappings and platform
  accounting may affect it.
- Keep exact device, iOS version, build mode and original log alongside the
  exported data; rerun under consistent thermal and power conditions.

## Research interpretation and limitations

- Simulator debug-mode timings are **exploratory**. For mobile deployment
  performance claims, repeat the protocol on a **physical iPhone** running an
  appropriately signed profile/release build and record hardware and thermal
  conditions. Flutter's official profiling guidance recommends profile mode
  on physical devices.
- This measures inference (not UI frame rates, FPS, energy use or battery life).
- The four images verify reference parity and benchmark four known inputs;
  they do not establish clinical sensitivity, cross-dataset generalization or
  reliability of a diagnosis.
- Never report earlier single-sample `134.6 ms` as the new benchmark's mean
  or insert invented results.
- Private JPEGs, trained weights and sensitive research data must remain
  outside GitHub.

See also `integration_test/model_device_test.dart`,
`docs/REPRODUCIBILITY.md`, and `docs/IOS_DEPLOYMENT_GUIDE.md`.
