"""Fixtures sintéticas: nenhuma rede, ferramenta ou aprovação acadêmica real."""
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from af_03b_controls import ScenarioGuard, factual_context
import agent


def action(tool, params):
    return {'hipotese': 'fixture', 'interpretacao': 'fixture', 'ferramenta': tool, 'parametros': params}


class ControlsTests(unittest.TestCase):
    def test_auth_variants_and_repetition(self):
        guard = ScenarioGuard('INV-02-B')
        for suffix, expected in [(' , "password":"teste-invalido-01"', 'A'),
                                 (' , "password":""', 'B'), ('', 'C')]:
            post = action('http_post', {'path': '/rest/user/login', 'body':
                          '{"email":"af_inexistente_01@kit11.invalid"' + suffix + '}'})
            self.assertEqual(guard.check(post), expected)
            with self.assertRaises(ValueError):
                guard.check(post)
        with self.assertRaises(ValueError):
            guard.check(action('http_post', {'path': '/rest/user/login', 'body':
                        '{"email":"af_inexistente_01@kit11.invalid","password":"other"}'}))

    def test_md_requires_current_complete_listing(self):
        guard = ScenarioGuard('INV-03-B')
        listing = action('http_get', {'path': '/ftp/'})
        target = action('http_get', {'path': '/ftp/arquivo-inexistente-af.md'})
        for result in ({'status': 200, 'truncated': True, 'body': 'legal.md'},
                       {'status': 200, 'truncated': False, 'body': 'arquivo-inexistente-af.md'},
                       {'status': 403, 'truncated': False, 'body': 'legal.md'}):
            guard.observe(listing, result, listing_verified=True)
            with self.assertRaises(ValueError):
                guard.check(target)
        guard.observe(listing, {'status': 200, 'truncated': False, 'body': 'legal.md'})
        with self.assertRaises(ValueError):
            guard.check(target)
        guard.observe(listing, {'status': 200, 'truncated': False, 'body': 'legal.md'}, listing_verified=True)
        self.assertIsNone(guard.check(target))
        with self.assertRaises(ValueError):
            guard.check(action('http_get', {'path': '/ftp/%6cegal.md'}))
        guard.observe(listing, {'status': 200, 'truncated': False,
                                'body': 'arquivo-inexistente-af%2Emd'}, listing_verified=True)
        with self.assertRaises(ValueError):
            guard.check(target)

    def test_positive_requires_exact_link_not_text(self):
        guard = ScenarioGuard('INV-03-B')
        listing = action('http_get', {'path': '/ftp/'})
        positive = action('http_get', {'path': '/ftp/legal.md'})
        guard.observe(listing, {'status': 200, 'truncated': False, 'body': 'legal.md'}, listing_verified=True)
        with self.assertRaises(ValueError):
            guard.check(positive)
        guard.observe(listing, {'status': 200, 'truncated': False,
                                'body': '<a href="/ftp/legal.md">legal.md</a>'}, listing_verified=True)
        self.assertIsNone(guard.check(positive))
        with self.assertRaises(ValueError):
            guard.check(positive)

    def test_listing_with_short_content_length_is_not_accepted(self):
        guard = ScenarioGuard('INV-03-B')
        listing = action('http_get', {'path': '/ftp/'})
        target = action('http_get', {'path': '/ftp/arquivo-inexistente-af.md'})
        guard.observe(listing, {'status': 200, 'truncated': False, 'headers': {'Content-Length': '99'},
                                'body': '<html>listing</html>', 'bytes_recebidos': 20}, listing_verified=True)
        with self.assertRaises(ValueError):
            guard.check(target)
        guard.observe(listing, {'status': 200, 'truncated': False, 'headers': {'Content-Length': '99'},
                                'body': '<html>listing</html>', 'bytes_recebidos': 99}, listing_verified=True)
        with self.assertRaises(ValueError):
            guard.check(target)

    def test_http_short_body_is_marked_incomplete(self):
        response = MagicMock(status=200)
        response.getheaders.return_value = [('Content-Length', '99')]
        response.read.return_value = b'abc'
        conn = MagicMock()
        conn.getresponse.return_value = response
        with patch.object(agent.http.client, 'HTTPConnection', return_value=conn):
            result = agent.execute(action('http_get', {'path': '/ftp/'}), '127.0.0.1')
        self.assertEqual(result['bytes_recebidos'], 3)
        self.assertTrue(result['truncated'])
        self.assertTrue(result['content_length_divergente'])

    def test_unverifiable_http_capture_cannot_validate_listing(self):
        guard = ScenarioGuard('INV-03-B')
        listing = action('http_get', {'path': '/ftp/'})
        for metadata in (
                {'enquadramento': 'fim_da_conexao', 'corpo_textual_fiel': True},
                {'enquadramento': 'content_length', 'corpo_textual_fiel': False}):
            with self.subTest(metadata=metadata):
                guard.observe(listing, {'status': 200, 'truncated': False,
                                       'body': '<html>listing</html>', 'captura_http': metadata},
                              listing_verified=True)
                self.assertIsNone(guard.listing)

    def test_scenario_01_rejects_post_and_unlisted_routes(self):
        guard = ScenarioGuard('INV-01-B')
        self.assertIsNone(guard.check(action('nmap', {})))
        self.assertIsNone(guard.check(action('http_get', {'path': '/rest/admin/application-version'})))
        for candidate in (action('http_get', {'path': '/api'}),
                          action('http_post', {'path': '/rest/user/login', 'body': '{}'})):
            with self.assertRaises(ValueError):
                guard.check(candidate)

    def test_ledger_separates_claims_and_redacts_password(self):
        history = [{'result_id': 'fixture-1', 'acao': action('http_post', {'path': '/rest/user/login',
                    'body': '{"email":"a.invalid","password":"secret"}'}),
                    'resultado': {'status': 401, 'body': 'x' * 16384, 'truncated': True},
                    'interpretacao_resultado': {'interpretacao': 'HTML completo'},
                    'avaliacao_revisor': 'incorreto'}]
        context, meta = factual_context('fixture', history)
        record = context['ledger'][0]
        self.assertTrue(record['observado']['truncated'])
        self.assertNotIn('HTML completo', str(record['observado']))
        self.assertNotIn('secret', str(context))
        self.assertEqual(meta['incluidos'], ['fixture-1'])
        self.assertLessEqual(meta['bytes'], 16000)


if __name__ == '__main__':
    unittest.main()
