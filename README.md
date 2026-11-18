# MobileSkinXAIDefense

Private thesis-defense source project for MobileSkinXAI, created with fresh Git history from verified integration `36044b4f57f1051360b369afe0f7976e4af070f0` and its checksum-verified archive. This is an independent repository. The original project, experiments and GitHub repository are preserved.

**No datasets, patient records, raw clinical fixtures or trained weights are included. Downloading this repository alone cannot perform real inference.** Install the separately transferred genuine FP32 TensorFlow Lite export. Never use a dummy model. The application displays model unavailability and disables analysis when the model cannot load.

## Riti's Mac quick start

```bash
gh repo clone rinviriti/MobileSkinXAIDefense
cd MobileSkinXAIDefense
python3 scripts/install_model.py /absolute/path/to/model_float32.tflite
cd app/flutter
flutter --version
flutter doctor -v
flutter pub get
bash packages/mobileskinxai_codec/build_ios_codec.sh
(cd ios && pod install)
flutter analyze --no-fatal-infos
flutter test
flutter build ios --release --no-codesign
```

Install/configure Flutter, Xcode, CocoaPods and CMake first; follow [the complete Mac/iPhone guide](docs/IOS_DEPLOYMENT_GUIDE.md). Source baseline: Flutter 3.50.0 / Dart 3.12 constraint, locked tflite_flutter 0.12.1, iOS target 15.0. No iOS build or physical iPhone success is claimed. Native codec source is included; its XCFramework must be built on Mac. Use a unique bundle ID and your own Apple signing identity for a phone. No certificates or provisioning profiles are included.

## Contents

- `app/flutter/`: Riti's existing UI, navigation, inference service, iOS/Android/platform projects, codec source and real interpreter tests.
- `training/`, `final_training/`, `research/`, `scripts/`: architecture definitions, six-model configurations, dataset preparation/audits and original research implementations, with their established paths.
- `evaluation/`: genuine aggregate CSV/JSON results, ten editable CSV/Markdown tables, confusion matrices, ROC/PR plots and training curves.
- `figures/`: architecture diagrams, aggregate dataset charts, six approved Grad-CAM panels, a permitted training illustration grid and headless Flutter UI capture. Together with evaluation, 56 research PNGs.
- `deployment/ios/`: exact model installation manifest and native iOS notes; `deployment/verification/`: preprocessing specification and historical parity evidence.
- `tests/`: model-installation integrity tests. `docs/`: defense narrative, methods, limitations, reproducibility and current validation report.

Start with [Defense Guide](docs/DEFENSE_GUIDE.md), [Research Overview](docs/RESEARCH_OVERVIEW.md), [Results](docs/EXPERIMENTAL_RESULTS.md), [Inventory](docs/INVENTORY.md), [Model Installation](docs/MODEL_INSTALLATION.md) and [Validation](docs/VALIDATION_REPORT.md).

## Research boundaries

The deployment candidate remains MobileSkinXAI-Enhanced (LR Control), validation-selected before the final comparison. E2 uses labeled PAD exposure; its PAD results are exploratory adaptation evidence, not independent zero-shot or clinical validation. Preserve the poor SCC recognition and very small melanoma support. No retraining or new research evaluation was performed to create this repository. Controller unit tests contain only a tiny engineering optimizer smoke test, not a research experiment.

Approved clinical-image derivatives retain their original noncommercial/attribution or attribution terms. Raw clinical images and embedded base64 fixtures are excluded. See [artifact rights](docs/ARTIFACT_RIGHTS.md). This project is not production-ready medical software. HEIC and on-device Grad-CAM are unsupported; physical camera/Photos, AOT, latency and signing remain to validate.
