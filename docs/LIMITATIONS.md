# Limitations

- E2 has labeled PAD exposure. Prior PAD inspection and an exploratory teacher-protocol amendment prevent a clean independent zero-shot claim.
- E1/E2 comparison has one seed, unequal parent budgets and only 7 melanoma / 28 SCC PAD test lesion units. Selected LR Control detects 4/7 MEL and 7/28 SCC; poor minority-class recognition remains.
- Known lesion grouping is not proven biological patient independence when linkage is unavailable. Conditional bootstrap uncertainty does not replace repeated training seeds.
- No clinical safety, validated diagnostic workflow, calibrated probability guarantee or established methodological novelty is claimed.
- All trained weights and private data are excluded. Exact training reproduction requires separate licensed datasets, reviewed private manifests/locks and legitimate initialization/teacher/parent weights. Cloning alone cannot reproduce inference.
- No successful iOS app build or physical phone test was performed here. iOS ARM64 processor propagation is corrected in source, but packaging/linking/signing and physical AOT behavior require Xcode/iPhone validation. Android SDK/NDK build verification is outstanding.
- HEIC/HEIF and on-device Grad-CAM are unsupported. Offline Grad-CAM panels are actual research outputs, not a tested mobile explanation feature.
- Headless UI capture and existing screenshots are not physical-device evidence. Camera/Photos byte behavior, unusual color profiles, real-world robustness, memory and device latency need measurement.
