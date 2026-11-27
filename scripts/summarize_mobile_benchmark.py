"""Convert a MobileSkinXAI iOS benchmark console log to JSON/CSV evidence.

No clinical images, source checkpoints or model weights are read or uploaded.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

CASE_MARKER = 'MSX_BENCHMARK_CASE_JSON='
SUMMARY_MARKER = 'MSX_BENCHMARK_SUMMARY_JSON='


def extract(log: str) -> tuple[dict, list[dict]]:
    summary = None
    cases = []
    for line in log.splitlines():
        if CASE_MARKER in line:
            cases.append(json.loads(line.split(CASE_MARKER, 1)[1].strip()))
        if SUMMARY_MARKER in line:
            summary = json.loads(line.split(SUMMARY_MARKER, 1)[1].strip())
    if summary is None:
        raise ValueError('No complete benchmark summary found in log. '
                         'Check for test failure or truncated output.')
    if summary.get('total_measurements') != 120:
        raise ValueError('Expected 120 measurements from four images x 30 runs.')
    if len(summary.get('cases', [])) != 4:
        raise ValueError('Benchmark summary must contain four verified cases.')
    if len(cases) != 4:
        raise ValueError(f'Expected four sample traces, got {len(cases)}.')
    for case in cases:
        if any(len(case.get(key, [])) != 30 for key in
               ('model_samples_ms', 'end_to_end_samples_ms', 'rss_samples_bytes')):
            raise ValueError('Missing or incomplete sample data in log.')
    return summary, cases


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log_file', type=Path, help='Captured flutter test log')
    parser.add_argument('--out-dir', type=Path, required=True,
                        help='Directory for benchmark report and CSV evidence')
    args = parser.parse_args()
    summary, cases = extract(args.log_file.read_text(encoding='utf-8'))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / 'benchmark_summary.json').write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    columns = ['image', 'n', 'model_mean_ms', 'model_median_ms', 'model_p95_ms',
               'model_stddev_ms', 'model_min_ms', 'model_max_ms',
               'end_to_end_mean_ms', 'end_to_end_median_ms',
               'end_to_end_p95_ms', 'end_to_end_stddev_ms',
               'end_to_end_min_ms', 'end_to_end_max_ms', 'max_abs_logit_error']
    with (args.out_dir / 'benchmark_summary.csv').open(
            'w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for row in [*summary['cases'], {
                'image': 'ALL', 'model': summary['model'],
                'end_to_end': summary['end_to_end'], 'max_abs_logit_error': ''}]:
            model, full = row['model'], row['end_to_end']
            writer.writerow({
                'image': row['image'], 'n': model['n'],
                'model_mean_ms': model['mean_ms'],
                'model_median_ms': model['median_ms'],
                'model_p95_ms': model['p95_ms'],
                'model_stddev_ms': model['stddev_ms'],
                'model_min_ms': model['min_ms'],
                'model_max_ms': model['max_ms'],
                'end_to_end_mean_ms': full['mean_ms'],
                'end_to_end_median_ms': full['median_ms'],
                'end_to_end_p95_ms': full['p95_ms'],
                'end_to_end_stddev_ms': full['stddev_ms'],
                'end_to_end_min_ms': full['min_ms'],
                'end_to_end_max_ms': full['max_ms'],
                'max_abs_logit_error': row['max_abs_logit_error'],
            })

    with (args.out_dir / 'benchmark_samples.csv').open(
            'w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['image', 'run', 'model_ms', 'end_to_end_ms', 'rss_bytes'])
        for case in cases:
            for i, (model, full, rss) in enumerate(zip(
                    case['model_samples_ms'],
                    case['end_to_end_samples_ms'],
                    case['rss_samples_bytes']), 1):
                writer.writerow([case['image'], i, model, full, rss])

    print(f'Saved {args.out_dir / "benchmark_summary.json"}')
    print(f'Saved {args.out_dir / "benchmark_summary.csv"}')
    print(f'Saved {args.out_dir / "benchmark_samples.csv"}')
    print(f'Build mode: {summary["build_mode"]}, device: {summary["device_name"]}')
    print(f'120 measured predictions; model mean {summary["model"]["mean_ms"]} ms, '
          f'P95 {summary["model"]["p95_ms"]} ms')


if __name__ == '__main__':
    main()
