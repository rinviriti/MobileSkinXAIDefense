import 'dart:convert';
import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobileskinxai_codec/mobileskinxai_codec.dart';

void main() {
  const manifest = String.fromEnvironment('MSX_PREPROCESS_MANIFEST');
  const library = String.fromEnvironment('MSX_CODEC_LIBRARY');
  test(
    'Native JPEG, EXIF 1-8, resize and JPEG roundtrip match Pillow pixels',
    () {
      final codec = NativeJpegCodec(libraryPath: library);
      final rows = jsonDecode(File(manifest).readAsStringSync()) as List;
      for (final r in rows) {
        final actual = codec.prepareRgb(
          File(r['source'] as String).readAsBytesSync(),
        );
        final expected = File(r['expected'] as String).readAsBytesSync();
        expect(actual, orderedEquals(expected), reason: r['source'] as String);
      }
    },
    skip: manifest.isEmpty || library.isEmpty,
  );
}
