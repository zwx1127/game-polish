import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from game_polish.cli import create_run, default_config, main
from game_polish.reporting import write_reports

class ReportingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        config = default_config('中文项目')
        config['checks'] = {'test': {'argv': [sys.executable, '-c', 'print("ok")']}}
        self.config = self.root / 'game-polish.json'
        self.config.write_text(json.dumps(config))

    def test_automatic_reports_for_planned_passed_and_failed(self):
        for phase, execute in [('baseline', False), ('baseline', True), ('run', True)]:
            path, manifest = create_run(self.config, phase, execute, None, None)
            for filename in ['report.md', 'report.html']:
                report = (path / filename).read_text()
                self.assertIn('中文项目', report)
                self.assertIn(manifest['status'], report)
                self.assertIn('未验证', report)
        config = json.loads(self.config.read_text())
        config['checks']['test']['argv'][-1] = 'raise SystemExit(2)'
        self.config.write_text(json.dumps(config))
        path, manifest = create_run(self.config, 'run', True, None, None)
        self.assertEqual(manifest['status'], 'failed')
        self.assertIn('failed', (path / 'report.html').read_text())

    def test_refresh_reads_observations_and_does_not_execute(self):
        path, manifest = create_run(self.config, 'run', False, None, None)
        observation = {'hypothesis': '起步跳变', 'changes': ['新增16组对应场'],
                       'evidence': [{'path': 'evidence/paired.mp4', 'description': '左前右后'}],
                       'limitations': ['未验证Forward+'], 'rollback': ['反向补丁'], 'decision': 'reviewed'}
        (path / 'observations.json').write_text(json.dumps(observation))
        before = (path / 'manifest.json').read_bytes()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(['report', str(path)]), 0)
        self.assertEqual(before, (path / 'manifest.json').read_bytes())
        for filename in ['report.html', 'report.md']:
            report = (path / filename).read_text()
            for text in ['起步跳变', '新增16组对应场', 'paired.mp4', '反向补丁', '未验证Forward+']:
                self.assertIn(text, report)
        self.assertFalse(list(path.glob('*.log')))

    def test_html_untrusted_text_escaped(self):
        path, manifest = create_run(self.config, 'run', False, None, None)
        (path / 'observations.json').write_text(json.dumps({'changes': ['<script>alert(1)</script>']}))
        write_reports(path, manifest)
        html = (path / 'report.html').read_text()
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)

    def test_invalid_observations_preserve_reports(self):
        path, manifest = create_run(self.config, 'run', False, None, None)
        previous = (path / 'report.html').read_bytes()
        (path / 'observations.json').write_text('{')
        with self.assertRaises(ValueError):
            write_reports(path, manifest)
        self.assertEqual(previous, (path / 'report.html').read_bytes())

    def test_symlink_report_rejected(self):
        path, manifest = create_run(self.config, 'run', False, None, None)
        (path / 'report.html').unlink()
        target = self.root / 'unrelated.txt'
        target.write_text('unchanged')
        (path / 'report.html').symlink_to(target)
        with self.assertRaises(ValueError):
            write_reports(path, manifest)
        self.assertEqual(target.read_text(), 'unchanged')

    def test_invalid_empty_observations_not_silently_accepted(self):
        path, manifest = create_run(self.config, 'run', False, None, None)
        previous = (path / 'report.html').read_bytes()
        for invalid in [[], False, 0, "", None]:
            (path / 'observations.json').write_text(json.dumps(invalid))
            with self.assertRaises(ValueError):
                write_reports(path, manifest)
            self.assertEqual(previous, (path / 'report.html').read_bytes())

    def test_json_contract_failure_reason_visible(self):
        path, manifest = create_run(self.config, 'run', False, None, None)
        manifest['checks']['test'].update(status='failed', exit_code=0, json_ok=False, error='JSON result must contain ok: true')
        write_reports(path, manifest)
        report = (path / 'report.html').read_text()
        self.assertIn('json_ok=False', report)
        self.assertIn('JSON result must contain ok: true', report)
