# iOS source integration

See [Mac setup and iPhone validation](../../docs/IOS_DEPLOYMENT_GUIDE.md) and [model installation](../../docs/MODEL_INSTALLATION.md).

The intended model is MobileSkinXAI-Enhanced (LR Control), FP32, 10,073,864 bytes; no weights are distributed. `MODEL_MANIFEST.json` is metadata only.

Preserved: Runner project, iOS 15.0 deployment target, camera/Photo Library usage descriptions, Podfile with frameworks, tflite_flutter 0.12.1 plugin and custom native preprocessing FFI package. The codec is built for ARM64 device and ARM64 simulator, packaged as a dynamic XCFramework and declared in the plugin podspec. iOS FFI resolves msx_decode/msx_roundtrip/msx_free/msx_error from the linked process; linker flags retain these symbols. Intel simulator is not provided by the current script; use Apple Silicon or extend/test an x86_64 simulator slice separately.

`build_ios_codec.sh` now explicitly propagates `CMAKE_SYSTEM_PROCESSOR=arm64` to avoid the prior empty-processor libjpeg CMake failure. This has been inspected and the changed shared CMake/native source rebuilt on Linux; a real iOS build remains unverified. Existing framework output is preserved rather than silently overwritten.

Decode/EXIF/geometry/JPEG roundtrip/normalization are implemented in codec.c, native_codec.dart and geometry.dart. Tensor shapes, label order and single softmax handling are enforced in skin_classifier.dart. No automatic HEIC conversion or on-device Grad-CAM is implemented. Native framework output, Pods, signing credentials and model binaries are ignored and excluded from publication.
