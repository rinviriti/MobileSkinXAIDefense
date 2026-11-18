"""Install only the explicitly supplied, checksum-verified original FP32 export."""
from pathlib import Path
import argparse, hashlib, json, os, tempfile
ROOT = Path(__file__).resolve().parents[1]
def install(source, root=ROOT):
    m = json.loads((root / 'deployment/ios/MODEL_MANIFEST.json').read_text())
    source = Path(source).expanduser().resolve(strict=True)
    if source.suffix.lower() != '.tflite':
        raise ValueError('Supply the genuine .tflite export; no conversion or fallback exists.')
    raw = source.read_bytes()
    if len(raw) != m['bytes'] or raw[4:8] != b'TFL3' or hashlib.sha256(raw).hexdigest() != m['sha256']:
        raise ValueError('Model checksum, size, or TFLite signature mismatch. No file installed.')
    target = root / m['asset_path']
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if target.read_bytes() != raw:
            raise FileExistsError('Different existing model preserved; inspect it manually.')
        return target
    fd, name = tempfile.mkstemp(prefix='.model-install-', dir=target.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(raw)
        # Atomic non-overwriting publication; fail rather than replacing any existing file.
        os.link(name, target)
    finally:
        Path(name).unlink(missing_ok=True)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == m['sha256']
    return target
if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    args = p.parse_args()
    print(install(args.source))
