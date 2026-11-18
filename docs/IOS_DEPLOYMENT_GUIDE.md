# Riti's Mac and physical iPhone guide

## Tools and checkout

Use a Mac with full Xcode. This source was analyzed/tested using Flutter 3.50.0 and Dart 3.12-compatible dependencies; start with that version, preserve pubspec.lock, and validate any later upgrade. Check `flutter --version` and `flutter doctor -v`. Install Flutter using its official macOS installation guide and put its bin directory on PATH. Open Xcode once and install its platform components.

```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -license accept
xcodebuild -runFirstLaunch
# If using Homebrew:
brew install cocoapods cmake ninja
pod --version
cmake --version
flutter doctor -v
gh auth login
gh repo clone rinviriti/MobileSkinXAIDefense
cd MobileSkinXAIDefense
```

The repository is private; your GitHub account must be granted access. A separately downloaded private release ZIP may be extracted instead. Do not place source files inside an old research run.

## Model, native framework and app

Receive the genuine FP32 file separately. Run from repository root:

```bash
python3 scripts/install_model.py /absolute/path/to/model_float32.tflite
cd app/flutter
flutter pub get
bash packages/mobileskinxai_codec/build_ios_codec.sh
(cd ios && pod install)
flutter analyze --no-fatal-infos
flutter test
flutter build ios --release --no-codesign
```

Codec build must succeed before pod install. The script builds ARM64 iphoneos and ARM64 iphonesimulator slices then creates `packages/mobileskinxai_codec/ios/Frameworks/MobileSkinXaiCodec.xcframework`. It refuses to replace an existing framework; preserve/version that output before a clean rebuild. Minimum target is iOS 15.0 in Podfile, Runner and native framework. Open `ios/Runner.xcworkspace`, not just the project. Pod resolution/framework linkage and tflite_flutter interpreter availability must be verified on this Mac; no macOS/Xcode success is preclaimed.

A plain `flutter test` runs available source tests and skips optional real-model/native fixture tests unless configured. For Linux-style host parity, follow `REPRODUCIBILITY.md`. macOS host parity requires a locally built `.dylib` and the TFLite host runtime; the iOS packaged-runtime test below is the device check.

## Physical iPhone and signing

1. In Xcode Runner Signing & Capabilities, select your Apple development team and a unique bundle identifier. Connect/unlock the iPhone, trust the Mac and enable Developer Mode if requested. Use `flutter devices` to verify detection.
2. Apple signing requires a valid development identity and provisioning profile managed on your Mac. A personal team may support limited development use; distribution/TestFlight requires the appropriate Apple Developer Program membership and signing. Never commit certificates, keys or profiles.
3. Run `flutter run -d <device-id>` for UI verification. Then test `flutter run --release -d <device-id>` to exercise release/AOT behavior. Unsigned build success is not permission to install on a phone.
4. Confirm model is installed, correct labels, real interpreter execution and no fake fallback. Record app/model commit/hash, iOS/device version, framework build and actual latency. Predictions are uncalibrated research scores, not diagnoses.
5. Exercise camera and Photos permissions (allow/deny), original JPEG, supported 8-bit PNG, malformed/oversized images and orientation 1–8. HEIC must fail clearly; do not silently change preprocessing. Verify Photos/camera APIs preserve intended bytes and do not introduce unrecorded conversions.
6. Check navigation, Back/cancellation, repeated analysis, memory, lifecycle and missing/corrupt model behavior in a separate no-model build. Confirm model absence disables analysis without invented classification.

## Actual packaged codec/interpreter parity

Privately obtain the four fixed development-validation fixtures identified by hash in `deployment/verification/GOLDEN_REFERENCE.json`, under their source license. No raw images are supplied by this repository.

```bash
# From repository root, source folder filenames must match GOLDEN_REFERENCE.json:
python3 deployment/verification/prepare_goldens.py --source-dir /private/path/to/fixtures --device-assets
cd app/flutter
flutter test integration_test/model_device_test.dart -d <device-id> --dart-define=MSX_DEVICE_FIXTURES=true
```

This invokes the real packaged native codec and interpreter. It compares logits and probabilities against genuine reference outputs without retuning tolerances; stores actual device results in integration-test reportData. Retain logs/screenshots privately. Only report device validation after this succeeds on the physical phone. The ordinary tests alone do not establish camera parity, clinical utility or production readiness.
