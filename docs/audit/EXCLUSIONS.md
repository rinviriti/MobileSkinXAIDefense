# Defense exclusions
Fresh root Git history. No parent repository history is imported.
All TFLite, PyTorch and other serialized weights are excluded, including the original inference reference.
Raw clinical fixture bytes embedded in golden_cases.dart were removed. Only numeric logits and hashes remain.
Frozen per-image membership checksum records were excluded conservatively; obtain private split manifests separately.
The 56 approved research PNGs and corresponding SVGs remain subject to their artifact licenses. No raw clinical images are distributed.
Original status/provenance reports are retained as historical evidence and can describe binaries no longer distributed here.
Old model-inclusive archive builders are retained as explicitly historical source; use scripts/build_defense_release.py only.
