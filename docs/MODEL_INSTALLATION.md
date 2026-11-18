# Install the genuine model locally

The repository and source ZIP contain no trained weights. Obtain the genuine original FP32 export separately from the project owner through an approved local transfer. No model download URL, model conversion or replacement checkpoint is selected by these scripts.

```bash
python3 scripts/install_model.py /absolute/path/to/model_float32.tflite
```

The script checks size **10,073,864 bytes**, TFLite signature and SHA-256 **8b6e19f3d8d0dd9c3b798a2cf99c0525079b9de4ea2f5d1708dd928a718412f3** against `deployment/ios/MODEL_MANIFEST.json` before writing. It atomically installs to `app/flutter/assets/models/e2_lr_control_v20261118/model_float32.tflite`. Different existing content is preserved and rejected. An identical existing file is accepted. No silent fallback, dummy model, pretrained substitute or random initialization is used for app predictions.

`labels.json` fixes order NV, MEL, BCC, SCC. `preprocessing.json` describes the input contract; `model_metadata.json` and the runtime enforce the checksum and logits contract. Runtime also verifies FP32 tensor shapes `[1,224,224,3]` and `[1,4]`.

The whole asset directory is declared in pubspec, so a source-only checkout still builds its asset bundle. When the model is absent, the review screen reports it and disables Analyze. Preview remains a layout preview without invented probabilities. Fully stop/rebuild the app after installing a model; hot reload alone need not refresh an asset bundle.

The installed file is ignored by Git. Never add it with `git add -f`. `python3 scripts/audit_repository.py` rejects any tracked/staged trained weight. Transfer checksums alongside the separately stored export.
