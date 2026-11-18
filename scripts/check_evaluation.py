"""Reconcile frozen aggregate results only; no model evaluation or training."""
from pathlib import Path
import csv, hashlib, json
ROOT=Path(__file__).resolve().parents[1]
def rows(p):
    with (ROOT/p).open(newline='') as f:return list(csv.DictReader(f))
def main():
    cms={};labels=['NV','MEL','BCC','SCC']
    for r in rows('evaluation/source_data/CONFUSION_COUNTS.csv'):
        key=tuple(r[k] for k in ['model','condition','dataset','analysis_level']);a=cms.setdefault(key,[[0]*4 for _ in range(4)])
        a[labels.index(r['true_class'])][labels.index(r['predicted_class'])]=int(r['count'])
    metrics=rows('evaluation/source_data/ALL_SETTING_METRICS.csv')
    for r in metrics:
        a=cms[tuple(r[k] for k in ['model','condition','dataset','analysis_level'])];s=[sum(x) for x in a];p=[sum(a[i][j] for i in range(4)) for j in range(4)]
        rec=[a[j][j]/s[j] for j in range(4)];pre=[a[j][j]/p[j] if p[j] else 0 for j in range(4)];f=[2*x*y/(x+y) if x+y else 0 for x,y in zip(rec,pre)]
        derived={'accuracy':sum(a[j][j] for j in range(4))/sum(s),'macro_f1':sum(f)/4,'balanced_accuracy':sum(rec)/4,'macro_precision':sum(pre)/4,'MEL_recall':rec[1],'SCC_recall':rec[3]}
        for k,v in derived.items():assert abs(v-float(r[k]))<1e-12,(k,r['model'])
        if r['dataset']=='PAD' and r['analysis_level']=='lesion_primary':assert s==[41,7,129,28]
    source=json.loads((ROOT/'docs/audit/SOURCE_ARCHIVE_AUDIT.json').read_text())['copied_original_sha256']
    checked=0
    for name,sha in source.items():
        if name.startswith(('evaluation/','figures/')):
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
            checked+=1
    tables=sorted((ROOT/'evaluation/metrics_tables').glob('Table_*.csv'))
    assert len(tables)==10
    images=list((ROOT/'evaluation').rglob('*.png'))+list((ROOT/'figures').rglob('*.png'))
    assert len(images)==56
    print(json.dumps({'status':'PASS','metric_rows':len(metrics),'immutable_results_and_figures':checked,'editable_tables':len(tables),'research_pngs':len(images)}))
if __name__=='__main__':main()
