"""Fixtures de modo delegado; sem rede, Docker, modelo ou restauração reais."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import af_03b_delegated as delegated


class Delegated03BTests(unittest.TestCase):
    def test_cli_help_imports_without_side_effects(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/af_03b_delegated.py'), '--help'],
                                cwd=ROOT, capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('INV-02-B', result.stdout)

    def test_plan_mismatch_stops_before_restoration(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prior = [{'run_id': 'FIXTURE', 'evento': 'aprovacao_plano_03b',
                      'plan_v2_sha256': 'divergente', 'plan_original_sha256': 'fixture'},
                     {'evento': 'aprovacao_plano', 'plano_sha256': 'fixture'},
                     {'evento': 'portao_rede', 'estado': 'declarado_pelo_grupo'}]
            with patch.object(delegated, 'ROOT', root), \
                 patch.object(delegated, 'PLAN_OLD', root / 'docs/old.md'), \
                 patch.object(delegated, 'PLAN_V2', root / 'docs/v2.md'), \
                 patch.object(delegated, 'sha', return_value='fixture'), \
                 patch.object(delegated, 'load_events', return_value=prior), \
                 patch.object(delegated.subprocess, 'check_output', return_value='fixture-commit'), \
                 patch.object(delegated.subprocess, 'run') as restore, \
                 patch.object(delegated, 'identity') as identity:
                self.assertEqual(delegated.main(['INV-02-B', '--autorizacao', 'FIXTURE']), 1)
                restore.assert_not_called()
                identity.assert_not_called()


if __name__ == '__main__':
    unittest.main()
