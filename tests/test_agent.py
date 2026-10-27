import contextlib
import http.server
import json
import io
import os
import tempfile
import threading
import unittest
from unittest.mock import patch
import agent


def action(tool='http_get', params=None):
    return {'hipotese': 'teste', 'interpretacao': 'sem evidência', 'ferramenta': tool, 'parametros': params if params is not None else {'path': '/'}}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302 if self.path == '/redirect' else 200)
        self.send_header('Location', 'http://example.com/')
        self.end_headers()
        self.wfile.write(b'x' * (agent.MAX_BODY + 10))
    def do_POST(self):
        self.send_response(201)
        self.end_headers()
        self.wfile.write(self.rfile.read(int(self.headers['Content-Length'])))
    def log_message(self, *_): pass


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.HTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()
    def test_get_limit_and_redirect(self):
        r = agent.execute(action(params={'path': '/redirect'}), '127.0.0.1', self.server.server_port)
        self.assertEqual(r['status'], 302); self.assertFalse(r['redirect_followed']); self.assertTrue(r['truncated'])
    def test_post(self):
        r = agent.execute(action('http_post', {'path': '/', 'body': '{"x":1}'}), '127.0.0.1', self.server.server_port)
        self.assertEqual((r['status'], r['body']), (201, '{"x":1}'))
    def test_validation(self):
        for a in [action(params={'path': '//example.com'}), action(params={'path': '/\r\nX: y'}), action('http_post', {'path': '/', 'body': 'x'*4097}), action('shell', {}), {}]:
            with self.assertRaises(ValueError): agent.validate_proposal(a)
        with self.assertRaises(ValueError): agent.local_ip('8.8.8.8')
    def test_nmap_command_limited(self):
        with patch('agent.subprocess.run') as run:
            run.return_value = type('R', (), {'returncode':0, 'stdout':b'ok', 'stderr':b''})()
            agent.execute(action('nmap', {}), '127.0.0.1')
            self.assertEqual(run.call_args.args[0][-2:], ['8s', '127.0.0.1'])
            self.assertIn('3000', run.call_args.args[0]); self.assertNotIn('shell', run.call_args.kwargs)
    def test_rejection(self):
        decision, result = agent.review(action(), lambda _: 'r')
        self.assertEqual(decision, 'rejeitada'); self.assertIsNone(result)
    def test_modification_requires_approval(self):
        changed = action(params={'path': '/novo'})
        answers = iter(['m', json.dumps(changed), 'n'])
        decision, result = agent.review(action(), lambda _: next(answers))
        self.assertEqual(decision, 'modificada_rejeitada'); self.assertEqual(result, changed)
        answers = iter(['m', json.dumps(changed), 's'])
        self.assertEqual(agent.review(action(), lambda _: next(answers))[0], 'modificada_aprovada')
    def test_network_error(self):
        s = __import__('socket').socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
        self.assertIn('error', agent.execute(action(), '127.0.0.1', port))
    def test_model_history_and_invalid(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, n): return json.dumps({'response': json.dumps(action())}).encode()
        with patch('agent.urllib.request.build_opener') as opener:
            opener.return_value.open.return_value = Response()
            agent.model_call('objetivo', [{'resultado': 'evidencia anterior'}])
            request = opener.return_value.open.call_args.args[0]
            self.assertIn('evidencia anterior', json.loads(request.data)['prompt'])
        with patch('agent.urllib.request.build_opener') as opener:
            opener.return_value.open.return_value = Response()
            with patch.object(Response, 'read', return_value=b'{invalid'):
                with self.assertRaises(ValueError): agent.model_call('x', [])
    def test_log_jsonl(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, 'log')
            agent.log(path, 'proposta', proposta=action()); agent.log(path, 'fim')
            with open(path) as f: rows = [json.loads(line) for line in f]
            self.assertEqual([r['evento'] for r in rows], ['proposta', 'fim']); self.assertIn('timestamp', rows[0])
    def test_main_rejection_never_executes(self):
        answers = iter(['s', 'objetivo', 'r', 'e', 'conclusao'])
        with tempfile.TemporaryDirectory() as d, patch('sys.argv', ['agent.py', '--ip', '127.0.0.1', '--log', os.path.join(d, 'log')]), patch('builtins.input', side_effect=lambda _: next(answers)), patch('agent.model_call', return_value=action()), patch('agent.execute') as execute, contextlib.redirect_stdout(io.StringIO()):
            agent.main(); execute.assert_not_called()

if __name__ == '__main__': unittest.main()
