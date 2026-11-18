# Research overview

The study compares four lightweight/backbone configurations and two training variants under source-only E1 and supervised joint-domain E2 conditions. `training/models/factory.py` records the exact timm architecture names. MobileSkinXAI-Enhanced and LR Control share MobileNetV4-Conv-Small inference architecture; enhancement/control concern training rather than extra inference modules.

Source-domain data are ISIC; smartphone target-domain data are PAD-UFES-20. Fixed class order is NV, MEL, BCC, SCC. Original frozen image counts are ISIC 11,632 / 2,835 / 2,703 and PAD 781 / 261 / 261 for train / validation / test. Scoring uses declared lesions, not a claim of universal biological patient independence: 1,421 ISIC test units and 205 fixed PAD test units.

Architecture sources, original execution controllers, configs, aggregate evaluations, learning histories, ten editable tables and approved figures are retained. Original run directories remain stable to preserve imports/provenance. Historical machine paths and external prerequisite locks must be privately reconstructed before any new run. This repository does not grant data redistribution rights or contain the trained networks.

See `evaluation/reports/SIX_MODEL_E1_E2_FINAL_REPORT.md`, `docs/RESULTS_SUMMARY.md`, and `docs/METHODOLOGY.md`. No novelty, clinical safety or external superiority claim is established by packaging this work.
