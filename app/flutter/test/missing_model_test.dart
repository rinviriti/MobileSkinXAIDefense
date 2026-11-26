import 'dart:typed_data';

import 'package:flutter/services.dart';
import 'package:material_ui/material_ui.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobileskinxai/services/skin_classifier.dart';
import 'package:mobileskinxai/screens/analysis_screen.dart';

class MissingAssets extends CachingAssetBundle {
  @override
  Future<ByteData> load(String key) async => throw FlutterError('Asset absent');
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'Missing model fails explicitly and supports retry without predictions',
    () async {
      final classifier = SkinClassifier(assets: MissingAssets());
      try {
        await expectLater(
          classifier.loadModel(),
          throwsA(isA<ModelNotInstalledException>()),
        );
        await expectLater(
          classifier.loadModel(),
          throwsA(isA<ModelNotInstalledException>()),
        );
      } finally {
        classifier.dispose();
      }
    },
  );
  testWidgets('Review screen shows missing-model state and disables analysis', (
    tester,
  ) async {
    // Force a missing asset even when the genuine model is installed for other tests.
    final messenger =
        TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger;
    messenger.setMockMessageHandler('flutter/assets', (message) async {
      final key = const StringCodec().decodeMessage(message);
      if (key != null && key.endsWith('model_float32.tflite')) return null;
      return null;
    });
    addTearDown(() => messenger.setMockMessageHandler('flutter/assets', null));
    await tester.pumpWidget(
      MaterialApp(
        home: AnalysisScreen(
          imageBytes: Uint8List(0),
          imageName: 'none',
          imageSource: 'test',
        ),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('Model not installed or unavailable'), findsOneWidget);
    final button = tester.widget<FilledButton>(
      find.widgetWithText(FilledButton, 'Analyze image'),
    );
    expect(button.onPressed, isNull);
  });
}
