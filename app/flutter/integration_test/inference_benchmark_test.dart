// Repeated native preprocessing + FP32 TensorFlow Lite benchmark.
// Requires the four privately installed, checksum-verified golden fixtures.
import 'dart:convert';
import 'dart:io';
import 'dart:math' as math;
import 'dart:typed_data';

import 'package:crypto/crypto.dart';
import 'package:flutter/foundation.dart' show kDebugMode, kProfileMode;
import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:mobileskinxai/services/skin_classifier.dart';

const int _warmupRounds = 5;
const int _measuredRounds = 30;

class _GoldenCase {
  const _GoldenCase(this.name, this.jpeg, this.expectedLogits);

  final String name;
  final Uint8List jpeg;
  final List<double> expectedLogits;
}

class _Metrics {
  final modelMs = <double>[];
  final endToEndMs = <double>[];
  final rssBytes = <int>[];
  double maxLogitError = 0;
}

Future<List<_GoldenCase>> _readVerifiedFixtures() async {
  final entries = jsonDecode(
    await rootBundle.loadString('assets/local_fixtures/cases.json'),
  ) as List<dynamic>;
  expect(entries.length, 4, reason: 'Exactly four frozen reference cases required.');
  final fixtures = <_GoldenCase>[];
  for (final entry in entries) {
    final row = entry as Map<String, dynamic>;
    final name = row['image'] as String;
    final data = await rootBundle.load('assets/local_fixtures/$name.jpg');
    final bytes = data.buffer.asUint8List(data.offsetInBytes, data.lengthInBytes);
    expect(sha256.convert(bytes).toString(), row['sha256'],
        reason: 'Fixture checksum mismatch: $name');
    final expectedLogits = (row['logits'] as List<dynamic>)
        .cast<num>()
        .map((value) => value.toDouble())
        .toList(growable: false);
    expect(expectedLogits.length, 4);
    fixtures.add(_GoldenCase(name, bytes, expectedLogits));
  }
  return fixtures;
}

double _round(double value) => double.parse(value.toStringAsFixed(3));

// P95 uses nearest-rank: ceil(0.95 * sampleCount).
Map<String, Object> _summary(List<double> values) {
  if (values.isEmpty) throw StateError('Cannot summarize empty benchmark data.');
  final sorted = [...values]..sort();
  final n = sorted.length;
  final mean = values.reduce((a, b) => a + b) / n;
  final variance = values
          .map((value) => (value - mean) * (value - mean))
          .reduce((a, b) => a + b) /
      n;
  final p95Index = (0.95 * n).ceil() - 1;
  return <String, Object>{
    'n': n,
    'mean_ms': _round(mean),
    'median_ms': _round(n.isOdd
        ? sorted[n ~/ 2]
        : (sorted[n ~/ 2 - 1] + sorted[n ~/ 2]) / 2),
    'p95_ms': _round(sorted[p95Index]),
    'stddev_ms': _round(math.sqrt(variance)),
    'min_ms': _round(sorted.first),
    'max_ms': _round(sorted.last),
  };
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('MobileSkinXAI repeated on-device inference performance',
      (tester) async {
    final fixtures = await _readVerifiedFixtures();
    final data = <String, _Metrics>{
      for (final fixture in fixtures) fixture.name: _Metrics(),
    };
    final classifier = SkinClassifier();
    final rssBeforeLoad = ProcessInfo.currentRss;
    final modelLoadTimer = Stopwatch()..start();
    try {
      await classifier.loadModel();
      modelLoadTimer.stop();
      final rssAfterLoad = ProcessInfo.currentRss;

      // Warm all four fixture paths and amortize isolate/runtime initialization.
      for (var round = 0; round < _warmupRounds; round++) {
        for (final fixture in fixtures) {
          await classifier.predictBytes(fixture.jpeg);
        }
      }
      final rssAfterWarmup = ProcessInfo.currentRss;

      // Interleave images across rounds to reduce systematic time-order bias.
      for (var round = 0; round < _measuredRounds; round++) {
        for (final fixture in fixtures) {
          final elapsed = Stopwatch()..start();
          final prediction = await classifier.predictBytes(fixture.jpeg);
          elapsed.stop();
          final result = data[fixture.name]!;
          result.endToEndMs.add(elapsed.elapsedMicroseconds / 1000);
          result.modelMs.add(prediction.inferenceTimeMs);
          result.rssBytes.add(ProcessInfo.currentRss);

          // Verify the result outside the timed interval, not just its latency.
          for (var classIndex = 0; classIndex < 4; classIndex++) {
            final difference = (prediction.logits[classIndex] -
                    fixture.expectedLogits[classIndex])
                .abs();
            result.maxLogitError = math.max(result.maxLogitError, difference);
            expect(difference, lessThanOrEqualTo(0.001),
                reason: '${fixture.name}: logit drift on run ${round + 1}, '
                    'class ${SkinClassifier.classCodes[classIndex]}');
          }
          final bestReference = fixture.expectedLogits.indexOf(
            fixture.expectedLogits.reduce(math.max),
          );
          expect(prediction.label, SkinClassifier.labels[bestReference]);
        }
      }

      final allModelMs = <double>[];
      final allEndToEndMs = <double>[];
      final allRss = <int>[];
      final caseSummaries = <Map<String, Object>>[];
      for (final fixture in fixtures) {
        final metrics = data[fixture.name]!;
        allModelMs.addAll(metrics.modelMs);
        allEndToEndMs.addAll(metrics.endToEndMs);
        allRss.addAll(metrics.rssBytes);
        final caseReport = <String, Object>{
          'image': fixture.name,
          'model': _summary(metrics.modelMs),
          'end_to_end': _summary(metrics.endToEndMs),
          'max_abs_logit_error': _round(metrics.maxLogitError),
          'model_samples_ms': metrics.modelMs.map(_round).toList(),
          'end_to_end_samples_ms': metrics.endToEndMs.map(_round).toList(),
          'rss_samples_bytes': metrics.rssBytes,
        };
        caseSummaries.add(caseReport);
        // ignore: avoid_print
        print('MSX_BENCHMARK_CASE_JSON=${jsonEncode(caseReport)}');
      }
      final rssAfterBenchmark = ProcessInfo.currentRss;
      final report = <String, Object>{
        'schema_version': 1,
        'runtime': Platform.operatingSystem,
        'runtime_version': Platform.operatingSystemVersion,
        'build_mode': kDebugMode ? 'debug' : (kProfileMode ? 'profile' : 'release'),
        'device_kind': const String.fromEnvironment('MSX_DEVICE_KIND',
            defaultValue: 'unspecified'),
        'device_name': const String.fromEnvironment('MSX_DEVICE_NAME',
            defaultValue: 'unspecified'),
        'model_version': 'E2 LR Control Float32 v20261118',
        'input': 'Four fixed, checksum-verified ISIC development-validation JPEGs',
        'warmup_rounds': _warmupRounds,
        'measured_rounds': _measuredRounds,
        'total_measurements': allModelMs.length,
        'model_load_ms': _round(modelLoadTimer.elapsedMicroseconds / 1000),
        'model': _summary(allModelMs),
        'end_to_end': _summary(allEndToEndMs),
        'memory': <String, Object>{
          'rss_before_model_bytes': rssBeforeLoad,
          'rss_after_model_load_bytes': rssAfterLoad,
          'rss_after_warmup_bytes': rssAfterWarmup,
          'rss_after_benchmark_bytes': rssAfterBenchmark,
          'max_sampled_rss_bytes': allRss.reduce(math.max),
        },
        'cases': caseSummaries.map((caseReport) => <String, Object>{
          'image': caseReport['image']!,
          'model': caseReport['model']!,
          'end_to_end': caseReport['end_to_end']!,
          'max_abs_logit_error': caseReport['max_abs_logit_error']!,
        }).toList(),
        'notes': 'Model time is TFLite Interpreter.run only. End-to-end time '
            'includes native preprocessing + inference, but excludes UI, '
            'gallery selection and image-asset loading. RSS is sampled process '
            'resident memory, not a true peak-memory measurement. Simulator '
            'debug results are exploratory, not physical-device benchmarks.',
      };
      IntegrationTestWidgetsFlutterBinding.instance.reportData = report;
      // ignore: avoid_print
      print('MSX_BENCHMARK_SUMMARY_JSON=${jsonEncode(report)}');
    } finally {
      classifier.dispose();
    }
  }, skip: !const bool.fromEnvironment('MSX_BENCHMARK'));
}
