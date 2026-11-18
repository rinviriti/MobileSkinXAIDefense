# Reviewed publication handoff

Local branch: feature/mobile-skinxai-final-integration
Commit: 36044b4f57f1051360b369afe0f7976e4af070f0
Worktree: /tmp/mobileskinxai-release-review
Repository: https://github.com/rinviriti/MobileSkinXAI

GitHub Contents/ref creation is blocked by authenticated integration HTTP403; Git CLI lacks credentials. No remote write succeeded. Once secure write access is available, push this branch, create the PR against current main and run all CI. Do not merge until required checks, branch protections and the exact PR head are verified. User authorization for normal squash merge and release already exists; never bypass protections or force push.

The supplied main-branch workflow creates a research prerelease only after integrity, actual Flutter/Linux tests and unsigned iOS/native build succeed. It packages the verified iOS framework. The present LOCAL ZIP has source/model and no prebuilt iOS framework; it is not a GitHub release or physical-device verification. Extracted files and model hashes were verified. See PUBLICATION_STATUS.json and packaged docs/PUBLICATION_BLOCKERS.md.

No source model was retrained, test metric changed or candidate reselected. PAD results remain exploratory. Older notebook outputs already exist in base Git history; publication copies are sanitized without rewriting that history. Original local research files remain untouched.
