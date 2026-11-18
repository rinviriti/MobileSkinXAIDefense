"""Fail-closed installation tests; no dummy model or weights are created."""
from pathlib import Path
import importlib.util,json,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('install_model',ROOT/'scripts/install_model.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class InstallerTests(unittest.TestCase):
    def test_rejects_nonmodel_without_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'deployment/ios').mkdir(parents=True)
            (r/'deployment/ios/MODEL_MANIFEST.json').write_bytes((ROOT/'deployment/ios/MODEL_MANIFEST.json').read_bytes())
            source=r/'invalid.tflite';source.write_text('Not a model; reject this file.')
            with self.assertRaises(ValueError):mod.install(source,r)
            self.assertFalse((r/'app').exists())
    def test_missing_source_rejected(self):
        with self.assertRaises(FileNotFoundError):mod.install(ROOT/'.private/no-such-model.tflite')
    def test_manifest_matches_dart_and_metadata(self):
        m=json.loads((ROOT/'deployment/ios/MODEL_MANIFEST.json').read_text())
        dart=(ROOT/'app/flutter/lib/services/skin_classifier.dart').read_text()
        meta=json.loads((ROOT/'app/flutter/assets/models/e2_lr_control_v20261118/model_metadata.json').read_text())
        self.assertIn(m['sha256'],dart);self.assertEqual(meta['tflite_sha256'],m['sha256'])
        self.assertEqual(m['classes'],['NV','MEL','BCC','SCC'])
        self.assertEqual(json.loads((ROOT/'app/flutter/assets/models/e2_lr_control_v20261118/labels.json').read_text()),m['classes'])
        prep=json.loads((ROOT/'app/flutter/assets/models/e2_lr_control_v20261118/preprocessing.json').read_text())
        self.assertEqual(prep['classes'],m['classes']);self.assertEqual(prep['input_shape'],m['input_shape'])
    def test_verified_local_model_install_and_existing_file_protection(self):
        source=ROOT/'app/flutter/assets/models/e2_lr_control_v20261118/model_float32.tflite'
        if not source.is_file():
            self.skipTest('Genuine model installed only for local integration validation')
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'deployment/ios').mkdir(parents=True)
            (r/'deployment/ios/MODEL_MANIFEST.json').write_bytes((ROOT/'deployment/ios/MODEL_MANIFEST.json').read_bytes())
            target=mod.install(source,r)
            self.assertEqual(target.read_bytes(),source.read_bytes())
            self.assertEqual(mod.install(source,r),target)
            target.write_text('Preserve this invalid existing local file; reject replacement.')
            with self.assertRaises(FileExistsError):mod.install(source,r)
            self.assertTrue(target.read_text().startswith('Preserve'))
if __name__=='__main__':unittest.main()
