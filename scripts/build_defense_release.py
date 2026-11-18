"""Archive only audited committed source files, never local installs or clinical fixtures."""
from pathlib import Path
import hashlib,json,subprocess,zipfile,tempfile
from audit_repository import main as audit
ROOT=Path(__file__).resolve().parents[1]
def main():
    audit()
    assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT).strip(),'Commit source first'
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    names=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
    out=ROOT/'release_dist';out.mkdir(exist_ok=True)
    target=out/'MobileSkinXAIDefense-v2026.11.18-defense-source.zip'
    assert not target.exists(),'Preserve existing release; choose a new version'
    manifest={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names}
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for n in sorted(names):z.write(ROOT/n,'MobileSkinXAIDefense/'+n)
        z.writestr('MobileSkinXAIDefense/PACKAGE_PROVENANCE.json',json.dumps({'source_commit':commit,'weights_included':False,'raw_datasets_included':False,'sha256':manifest},indent=2))
    with zipfile.ZipFile(target) as z, tempfile.TemporaryDirectory(prefix='defense-extraction-') as d:
        assert z.testzip() is None
        z.extractall(d)
        extracted=Path(d)/'MobileSkinXAIDefense'
        for n,sha in manifest.items():assert hashlib.sha256((extracted/n).read_bytes()).hexdigest()==sha,n
        assert len(list(p for p in extracted.rglob('*') if p.is_file()))==len(names)+1
    sha=hashlib.sha256(target.read_bytes()).hexdigest()
    (out/'SHA256SUMS.txt').write_text(sha+'  '+target.name+'\n')
    print(json.dumps({'archive':str(target),'bytes':target.stat().st_size,'sha256':sha,'files':len(names),'commit':commit,'extraction_verified':True},indent=2))
if __name__=='__main__':main()
