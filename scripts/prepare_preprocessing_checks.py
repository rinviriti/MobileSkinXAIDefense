"""Generate nonclinical geometric test images and Pillow reference pixels locally."""
from pathlib import Path
import sys,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'deployment/verification'))
from preprocess_reference import raw_to_prepared_rgb
out=ROOT/'.private/preprocess';out.mkdir(parents=True,exist_ok=True)
rows=[]
for width,height,orientation in [(37,29,o) for o in range(1,9)]+[(511,311,1),(25,401,1)]:
    y,x=np.indices((height,width));a=np.stack([(x*7+y*3)%256,(y*11+x*5)%256,(x*13+y*17)%256],axis=-1).astype('uint8')
    im=Image.fromarray(a);exif=Image.Exif();exif[274]=orientation
    src=out/f'{width}_{height}_{orientation}.jpg';im.save(src,quality=97,subsampling=0,exif=exif)
    expected=out/(src.stem+'.rgb');expected.write_bytes(raw_to_prepared_rgb(src).tobytes())
    rows.append({'source':str(src),'expected':str(expected)})
(out/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n');print(out/'manifest.json')
