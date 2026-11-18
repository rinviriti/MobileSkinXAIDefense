"""Inspect every indexed file, its complete bytes and declared file type before publication."""
from pathlib import Path
import ast, csv, hashlib, io, json, re, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
FORBIDDEN={'.pt','.pth','.ckpt','.safetensors','.h5','.keras','.onnx','.tflite','.npy','.npz','.pkl','.pickle','.joblib','.pb','.bin','.zip','.7z','.gz','.tar','.jpg','.jpeg','.dcm','.dicom'}
SECRETS=[r"gh[pousr]_[A-Za-z0-9]{30,}",r"github_pat_[A-Za-z0-9_]{50,}",r"AKIA[0-9A-Z]{16}",r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",r"PAT_\d+",("jpeg_" + "base64" + r".*:") ]
def inspect(name, raw):
    p=Path(name)
    assert p.suffix.lower() not in FORBIDDEN, f'Restricted artifact: {name}'
    assert not any(x in p.parts for x in ['datasets','raw_data','.private','.venv','Pods','.dart_tool','__pycache__','.aws','.ssh','saved_model','variables']),name
    assert 'dataset' not in p.parts or name.startswith('figures/dataset/'),name
    assert not p.name.startswith('.env') and p.suffix not in ['.pem','.p12','.key','.mobileprovision'],name
    assert not re.search(r'\.data-\d+-of-\d+$',name),name
    assert len(raw)<50*1024**2, f'Unexpected large file: {name}'
    assert raw[4:8]!=b'TFL3' and not raw.startswith((b'\x80\x02',b'\x80\x04',b'\x80\x05',b'\x89HDF',b'PK\x03\x04',b'\x7fELF')),name
    if p.suffix.lower() in ['.png','.ico']:
        assert raw.startswith(b'\x89PNG\r\n\x1a\n') if p.suffix.lower()=='.png' else raw.startswith(b'\x00\x00\x01\x00'),name
        return
    text=raw.decode('utf-8-sig') # reject undeclared executable/model or opaque binary
    for pattern in SECRETS:
        assert not re.search(pattern,text),f'Sensitive content pattern in {name}'
    # No parameter tensors encoded as literal large numeric arrays or serialized base64 weights.
    assert not re.search(r'(?:weights|state_dict|parameters)\s*[:=]\s*\[\s*[-\d]',text,re.I),f'Embedded parameter array: {name}'
    if p.suffix=='.py':ast.parse(text,filename=name)
    if p.suffix=='.json':json.loads(text)
    if p.suffix=='.jsonl':
        for line in text.splitlines():
            if line.strip():json.loads(line)
    if p.suffix=='.ipynb':
        nb=json.loads(text)
        for cell in nb['cells']:
            assert not cell.get('outputs') and not cell.get('attachments'),f'Notebook embedded content: {name}'
    if p.suffix=='.csv':list(csv.reader(io.StringIO(text)))
def main():
    names=subprocess.check_output(['git','ls-files','--cached','-z'],cwd=ROOT).decode().split('\0')
    names=[n for n in names if n]
    assert names,'No staged/indexed files'
    records=[]
    for name in names:
        raw=subprocess.check_output(['git','show',':'+name],cwd=ROOT)
        inspect(name,raw)
        assert not (ROOT/name).is_symlink(),name
        assert raw==(ROOT/name).read_bytes(),f'Unstaged modification: {name}'
        kind=subprocess.check_output(['file','--brief','--mime-type','--',str(ROOT/name)],text=True).strip()
        records.append({'path':name,'bytes':len(raw),'mime_type':kind,'sha256':hashlib.sha256(raw).hexdigest()})
    report={'status':'PASS','files_reviewed':len(records),'scope':'Every complete indexed file read, type inspected, UTF-8/text structures or image signature checked; restricted formats and credential/parameter patterns checked','records':records}
    target=ROOT/'.private/STAGED_FILE_AUDIT.json';target.parent.mkdir(exist_ok=True);target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','files_reviewed':len(records),'private_audit_report':str(target)}))
if __name__=='__main__':main()
