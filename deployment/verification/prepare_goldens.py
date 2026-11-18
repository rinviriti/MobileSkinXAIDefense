"""Verify separately supplied development images; never downloads or distributes images."""
from pathlib import Path
import argparse, hashlib, json, shutil
ROOT=Path(__file__).resolve().parents[2]
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-dir', required=True, type=Path)
    p.add_argument('--output', type=Path, default=ROOT/'.private')
    p.add_argument('--device-assets', action='store_true')
    a=p.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    rows=json.loads((ROOT/'deployment/verification/GOLDEN_REFERENCE.json').read_text())
    result=[]
    for r in rows:
        source=a.source_dir/(r['image']+'.jpg')
        raw=source.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==r['sha256'], 'Fixture mismatch: '+r['image']
        result.append({'image':r['image'],'source':str(source.resolve()),'source_sha256':r['sha256'],'original_logits':r['logits'],'split':'development_validation'})
    (a.output/'golden_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    if a.device_assets:
        dest=ROOT/'app/flutter/assets/local_fixtures';dest.mkdir(exist_ok=True)
        for r in rows:
            shutil.copyfile(a.source_dir/(r['image']+'.jpg'),dest/(r['image']+'.jpg'))
        (dest/'cases.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(a.output/'golden_manifest.json')
if __name__=='__main__':main()
