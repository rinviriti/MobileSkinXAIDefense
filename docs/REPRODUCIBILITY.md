# Reproducibility

## Frozen research evidence

No research training or held-out evaluation was repeated for repository creation. Existing numerical results, tables, figures and histories remain unchanged; `scripts/check_evaluation.py` verifies original hashes and reconciles confusion counts. Three aggregate dataset summary charts, previously omitted by a broad ignore rule, were recovered from reviewed local output and checked against the existing figure index.

```bash
python3 scripts/check_evaluation.py
python3 -B -m unittest discover -s tests -v
python3 scripts/audit_repository.py  # requires fresh Git repo with audited files staged/indexed
```

## Private datasets and training

Acquire official ISIC 2019/2020 and PAD-UFES-20 data under publisher terms; see `ARTIFACT_RIGHTS.md` and the historical `DATA_REPRODUCTION.md`. Data download/preprocessing/audit scripts are source code, not a grant to redistribute patient records. Keep datasets and private metadata outside publication. `training/configs/` has six E2 settings; `training/models/factory.py` identifies backbones. Original trainer/controller/architecture implementations are retained under training, scripts, final_training and research to preserve relative imports.

All checkpoints, ImageNet/teacher/parent weights and the frozen per-image membership file are excluded. `restore_private_split.py --local-index <private-index.csv> --frozen-membership <private-frozen-split-checksums.csv>` therefore needs the separately supplied private frozen membership checksum file as well as a licensed local index; it cannot reconstruct the exact split from this source checkout alone. Do not regenerate a split silently or claim a rebased reconstruction is byte-identical. `training/scripts/check_prerequisites.py` intentionally fails without licensed private inputs and approved locks. Use new experiment directories and preserve original run receipts, class mapping and grouping rules. Do not relax original approval guards or reselect checkpoints using test results.

Rebuilding presentation figures from aggregate source data is different from repeating evaluation. Bootstrap CIs require original private grouping/predictions. No seed variation or missing evaluation is invented.

## Local deployment checks

Install the genuine model using `scripts/install_model.py`. Python verification dependencies are recorded in `deployment/verification/requirements.txt` and historical `environment.json`. PyTorch parity requires a separately supplied genuine `student_reference.pt`; no reference weights are included.

```bash
python3 deployment/verification/prepare_goldens.py --source-dir /private/path/to/fixtures
python3 deployment/verification/verify_model.py --reference /private/path/to/student_reference.pt
python3 scripts/prepare_preprocessing_checks.py
cmake -S app/flutter/packages/mobileskinxai_codec/src -B .private/codec -G Ninja
cmake --build .private/codec --target mobileskinxai_codec --parallel 4
cd app/flutter
flutter pub get
flutter analyze --no-fatal-infos
flutter test --no-pub --dart-define=MSX_GOLDEN_MANIFEST=/absolute/repo/.private/golden_manifest.json --dart-define=MSX_CODEC_LIBRARY=/absolute/repo/.private/codec/libmobileskinxai_codec.so --dart-define=MSX_PREPROCESS_MANIFEST=/absolute/repo/.private/preprocess/manifest.json
```

Linux Flutter real interpreter tests also need the legitimate `libtensorflowlite_c-linux.so` runtime expected by tflite_flutter. The previously verified runtime SHA-256 is `4d0de8f2e694102387f85a2c79a91945b547e7e00786f5b57dec4f1ac853cff8`; its original documented upstream source is am15h/tflite_flutter_plugin release v0.5.0. Do not substitute an unverified runtime. Prior host setup put it in Flutter's `bin/cache/artifacts/engine/linux-x64/blobs/`. Native tools are required; macOS uses `.dylib` for host checks. Device checks use the linked iOS framework instead of a host path.

`prepare_preprocessing_checks.py` generates nonclinical geometric JPEG cases covering all eight EXIF orientations and resize/pad cases; it never generates model weights or predictions. Compare exact native/Dart pixels to Pillow. The four optional clinical parity fixtures must be supplied privately with exact hashes; numeric logits are original evidence, not parameters. `--device-assets` installs ignored images locally for the actual device test. Do not commit those assets.

The tiny CPU optimizer loop in controller unit tests checks stopping logic only; it is not a repeated research experiment. Optional screenshot capture is skipped unless font/output definitions are supplied. See `VALIDATION_REPORT.md` for current reruns and environment limitations.

## Resize regression correction

A new nonclinical 25×401 case exposed the prior always-horizontal-first implementation. [Pillow resampling source](https://github.com/python-pillow/Pillow/blob/main/src/libImaging/Resample.c) selects vertical-first when height reduction exceeds twice width reduction. The defense copy now follows that pass ordering; exact-pixel tests cover all eight EXIF orientations and downscaling cases, and the original genuine fixture logits still pass unchanged tolerances. This does not establish universal device parity.
