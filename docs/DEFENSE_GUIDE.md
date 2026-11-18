# Thesis defense guide

1. Explain the problem and scope: four-class research classification, source/target image differences, offline Flutter inference and attribution of source datasets.
2. Present the frozen audit and split composition (Table 01 and aggregate dataset figures). Distinguish image counts, declared lesions and known patient linkage.
3. Present the six architecture diagrams and E1/E2 methods. Explain shared inference backbones and different training/control budgets.
4. Walk through Tables 03–08: source-only transfer, supervised adaptation, ISIC tradeoffs and exact melanoma/SCC counts. Do not mix historical full-PAD and fixed-PAD populations.
5. Explain the validation-selected LR Control candidate; acknowledge MobileNetV4's higher PAD test point estimate without substituting it retrospectively.
6. Show genuine Grad-CAM as offline research visualization. It is not on-device Flutter Grad-CAM and not a clinical explanation guarantee.
7. Demonstrate Riti's Flutter UI. Without the separately installed real model, demonstrate the clear unavailable state only. With verified weights/native codec, use approved local images and report actual results.
8. Close with limitations: one E1/E2 seed, small melanoma support, poor SCC recognition, teacher amendment, grouping uncertainty, prior PAD exposure and unfinished physical-device validation.

Prepare for questions about unequal parent budgets, why validation selection differs from test ranking, why source-only and E2 target exposure differ, and why Linux parity is insufficient evidence of an iPhone deployment. Source tables, histories and provenance are included for inspection. All trained weights must be transferred separately and remain untracked.
