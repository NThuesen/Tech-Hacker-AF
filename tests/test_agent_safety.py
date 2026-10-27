"""Testes de engenharia com fixtures/mocks explícitos; não são decisões humanas reais."""
import contextlib
import io
import json
import os
import stat
import tempfile
import http.server
import threading
import time
import unittest
from unittest.mock import patch

import agent
from test_agent import action


class SafetyTests(unittest.TestCase):
    def test_strict_json_and_body(self):
        for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                agent.parse_json(text)
        for body in ('[]', 'null', '{invalid', '{"x":1,"x":2}'):
            with self.subTest(body=body), self.assertRaises(ValueError):
                agent.validate_proposal(action('http_post', {'path': '/', 'body': body}))

    def test_paths_and_targets_fail_before_io(self):
        for path in ('/%0d%0aX:y', '/%2fexample.com', '/a\\b', '/?token=segredo'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                agent.validate_proposal(action(params={'path': path}))
        with patch('agent.http.client.HTTPConnection') as connection:
            for host in ('8.8.8.8', 'localhost', '10.0.80.3', '127.0.0.2', '-oX'):
                with self.subTest(host=host), self.assertRaises(ValueError):
                    agent.execute(action(), host)
            connection.assert_not_called()

    def test_private_logs_redact_and_reject_links(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, 'events.jsonl')
            agent.log(path, 'teste', body='{"password":"sentinela","ok":true}', token='sentinela')
            self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o600)
            with open(path) as stream:
                raw = stream.read()
            self.assertNotIn('sentinela', raw)
            self.assertIn('[REDACTED]', raw)
            os.symlink(path, os.path.join(directory, 'link'))
            with self.assertRaises(ValueError):
                agent.log(os.path.join(directory, 'link'), 'teste')
            os.link(path, os.path.join(directory, 'hardlink'))
            with self.assertRaises(ValueError):
                agent.log(path, 'teste')

    def test_permissive_existing_log_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, 'unsafe')
            with open(path, 'w'):
                pass
            os.chmod(path, 0o644)
            with self.assertRaises(ValueError):
                agent.log(path, 'teste')

    def test_shared_log_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            os.chmod(directory, 0o755)
            with self.assertRaises(ValueError):
                agent.log(os.path.join(directory, 'events.jsonl'), 'teste')

    def model_response(self, envelope):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *_): pass
            def read(self, n): return envelope
        return Response()

    def test_malformed_model_envelopes(self):
        values = [b'[]', b'{invalid', b'{"done":true,"response":null}',
                  json.dumps({'done': False, 'response': json.dumps(action())}).encode(),
                  json.dumps({'done': True, 'done_reason': 'length', 'response': json.dumps(action())}).encode(),
                  json.dumps({'done': True, 'response': '{"x":1,"x":2}'}).encode(),
                  b'x' * (agent.MAX_MODEL_BYTES + 1)]
        for value in values:
            with self.subTest(value=value[:60]), patch('agent.urllib.request.build_opener') as opener:
                opener.return_value.open.return_value = self.model_response(value)
                with self.assertRaises(ValueError):
                    agent.model_call('teste técnico', [])

    def test_interpretation_must_match_result(self):
        with patch('agent.model_request', return_value={
                'resultado_id': 'outro', 'interpretacao': 'texto', 'limitacoes': 'texto'}):
            with self.assertRaises(ValueError):
                agent.interpret_result('teste', action(), {'status': 200}, 'resultado-correto')

    def test_history_is_bounded_and_keeps_latest(self):
        history = [{'resultado': str(n) + 'x' * 12000} for n in range(20)]
        context = agent.recent_history('teste', history)
        self.assertLess(len(json.dumps(context).encode()), 32001)
        self.assertEqual(context['historico'][-1], history[-1])

    def test_large_http_evidence_is_marked_and_not_silently_dropped(self):
        raw = {'resultado': {'status': 200, 'body': 'x' * 16000}}
        context = agent.recent_history('teste', [raw])
        result = context['historico'][-1]['resultado']
        self.assertEqual(result['status'], 200)
        self.assertEqual(len(result['body']), 2048)
        self.assertTrue(result['body_contexto']['truncado'])
        self.assertEqual(raw['resultado']['body'], 'x' * 16000)

    def run_fixture(self, answers, interpretation_error=False):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, 'events.jsonl')
            result = {'status': 200, 'body': 'fixture HTTP, não Juice Shop real'}
            def interpret(objective, act, response, result_id):
                if interpretation_error:
                    raise ValueError('fixture de saída inválida')
                return {'resultado_id': result_id, 'interpretacao': 'fixture', 'limitacoes': 'mock'}
            replies = iter(answers)
            with patch('agent.model_call', return_value=action()), patch('agent.execute', return_value=result) as execute, \
                    patch('agent.interpret_result', side_effect=interpret) as interpretation, \
                    contextlib.redirect_stdout(io.StringIO()):
                agent.run_session('fixture unitária', '127.0.0.1', path,
                                  lambda _: next(replies), engineering=True)
            with open(path) as stream:
                rows = [json.loads(line) for line in stream]
            return rows, execute.call_count, interpretation.call_count

    def test_last_result_is_interpreted_before_stop(self):
        rows, executions, interpretations = self.run_fixture(['a', 'teste', 'e', 'fim', 'fixture concluída'])
        self.assertEqual((executions, interpretations), (1, 1))
        result = next(row for row in rows if row['evento'] == 'resultado')
        interpretation = next(row for row in rows if row['evento'] == 'interpretacao')
        decision = next(row for row in rows if row['evento'] == 'decisao_pos_interpretacao')
        for key in ('run_id', 'step_id', 'proposal_id', 'execution_id', 'result_id'):
            self.assertEqual(result[key], interpretation[key])
            self.assertEqual(result[key], decision[key])
        self.assertEqual(interpretation['interpretacao']['resultado_id'], result['result_id'])
        self.assertEqual(decision['origem'], 'entrada_injetada_teste')
        self.assertEqual(len({row['event_id'] for row in rows}), len(rows))

    def test_bad_interpretation_stops_next_execution(self):
        rows, executions, _ = self.run_fixture(['a', 'teste', 'pendência simulada'], interpretation_error=True)
        self.assertEqual(executions, 1)
        self.assertTrue(any(row['evento'] == 'erro_interpretacao' for row in rows))
        self.assertFalse(any(row['evento'] == 'interpretacao' for row in rows))

    def test_modified_rejected_never_executes(self):
        changed = action(params={'path': '/fixture'})
        rows, executions, interpretations = self.run_fixture([
            'm', json.dumps(changed), 'n', 'não autorizar fixture', 'e', 'encerrar', 'fim'])
        self.assertEqual((executions, interpretations), (0, 0))
        self.assertTrue(any(row.get('decisao') == 'modificada_rejeitada' for row in rows))

    def test_modified_approved_executes_only_final_action(self):
        changed = action(params={'path': '/fixture-final'})
        rows, executions, interpretations = self.run_fixture([
            'm', json.dumps(changed), 's', 'aprovação simulada da fixture', 'e', 'fim', 'fim'])
        self.assertEqual((executions, interpretations), (1, 1))
        execution = next(row for row in rows if row['evento'] == 'execucao')
        self.assertEqual(execution['acao'], changed)
        self.assertTrue(any(row.get('decisao') == 'modificada_aprovada' for row in rows))

    def test_slow_http_has_total_deadline(self):
        class SlowHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-Length', '100')
                self.end_headers()
                try:
                    for _ in range(100):
                        self.wfile.write(b'x')
                        self.wfile.flush()
                        time.sleep(0.03)
                except (BrokenPipeError, ConnectionResetError):
                    pass
            def log_message(self, *_): pass
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), SlowHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            start = time.monotonic()
            with patch.object(agent, 'TIMEOUT', 0.15):
                result = agent.execute(action(), '127.0.0.1', server.server_port)
            self.assertIn('prazo total HTTP', result['error'])
            self.assertLess(time.monotonic() - start, 1)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_invalid_modification_requires_valid_review(self):
        replies = iter(['m', '{invalid', 'r'])
        with contextlib.redirect_stdout(io.StringIO()):
            decision, _ = agent.review(action(), lambda _: next(replies))
        self.assertEqual(decision, 'rejeitada')

    def test_log_failure_prevents_tool_execution(self):
        def failing_log(path, kind, **fields):
            if kind == 'decisao_humana':
                raise OSError('fixture disco indisponível')
        replies = iter(['a', 'fixture'])
        with patch('agent.log', side_effect=failing_log), patch('agent.model_call', return_value=action()), \
                patch('agent.execute') as execute, contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(OSError):
                agent.run_session('fixture', '127.0.0.1', 'ignorado', lambda _: next(replies), engineering=True)
            execute.assert_not_called()

    def test_eof_does_not_fabricate_decision(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, 'events.jsonl')
            with patch('agent.model_call', return_value=action()), patch('agent.execute') as execute, \
                    contextlib.redirect_stdout(io.StringIO()):
                agent.run_session('fixture', '127.0.0.1', path,
                                  lambda _: (_ for _ in ()).throw(EOFError()), engineering=True)
            execute.assert_not_called()
            with open(path) as stream:
                rows = [json.loads(line) for line in stream]
            self.assertEqual(rows[-1]['evento'], 'interrompida')
            self.assertFalse(any(row['evento'] == 'conclusao_humana' for row in rows))

    def test_academic_mode_requires_explicit_plan_confirmation(self):
        with patch('agent.model_call') as model:
            with self.assertRaises(ValueError):
                agent.run_session('fixture', '127.0.0.1', 'ignorado.jsonl')
            model.assert_not_called()

    def test_proposal_budget_limits_rejections(self):
        replies = iter(['r', 'fixture', 'r', 'fixture', 'fim'])
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(agent, 'MAX_ACTIONS', 2), patch('agent.model_call', return_value=action()) as model, \
                    patch('agent.execute') as execute, contextlib.redirect_stdout(io.StringIO()):
                agent.run_session('fixture', '127.0.0.1', os.path.join(directory, 'events.jsonl'),
                                  lambda _: next(replies), engineering=True)
            self.assertEqual(model.call_count, 2)
            execute.assert_not_called()


if __name__ == '__main__':
    unittest.main()
