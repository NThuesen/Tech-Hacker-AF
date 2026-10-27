"""Fixtures explícitas: sem Docker, Ollama, Nmap ou investigação real."""
import json
import contextlib
import io
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import agent

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import af_session as session
import af_summarize as summary


class AutomationTests(unittest.TestCase):
    def test_pipe_refused_before_lab(self):
        result = subprocess.run([str(ROOT / 'scripts/af_run.sh'), 'INV-01'],
                                input='APROVAR INV-01\n', text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('terminal interativo', result.stderr)

    def test_plan_refused_without_any_lab_call(self):
        events = []
        with tempfile.TemporaryDirectory() as folder, patch.object(session, 'command', return_value='fixture-commit'), \
                patch('builtins.input', side_effect=['Grupo fixture', 'data fixture', 'motivo fixture', '']), \
                patch.object(session, 'identity') as identity:
            with self.assertRaises(ValueError):
                session.prepare('INV-01', lambda kind, **kw: events.append((kind, kw)), Path(folder))
            identity.assert_not_called()
        self.assertFalse(any(kind == 'aprovacao_plano' for kind, _ in events))

    def test_pending_wan_stops_before_docker(self):
        events = []
        with tempfile.TemporaryDirectory() as folder, patch.object(session, 'command', return_value='fixture-commit'), \
                patch('builtins.input', side_effect=['Grupo fixture', 'data fixture', 'motivo fixture',
                    'APROVAR INV-02', 'evidencia Kali fixture', 'PENDENTE']), \
                patch.object(session, 'identity') as identity:
            with self.assertRaises(ValueError):
                session.prepare('INV-02', lambda kind, **kw: events.append((kind, kw)), Path(folder))
            identity.assert_not_called()
        self.assertEqual(events[-1][1]['estado'], 'PENDENTE')

    def test_successful_preparation_fixture_for_all_scenarios(self):
        for inv in session.SCENARIOS:
            with self.subTest(inv=inv), tempfile.TemporaryDirectory() as folder:
                events = []
                answers = ['Grupo fixture', 'data fixture', 'motivo fixture', 'APROVAR ' + inv,
                           'Kali fixture', 'WAN fixture', 'REDE VERIFICADA', 'OFERECER']
                with patch.object(session, 'command', return_value='fixture-commit'), \
                     patch('builtins.input', side_effect=answers), \
                     patch.object(session, 'identity', side_effect=['a' * 64, 'b' * 64, 'b' * 64]), \
                     patch.object(session, 'services', return_value={'modelo': agent.MODEL}), \
                     patch.object(session, 'wait_ready', return_value={'status': 200}), \
                     patch.object(session.subprocess, 'run') as restore:
                    session.prepare(inv, lambda kind, **kw: events.append((kind, kw)), Path(folder))
                    restore.assert_called_once()
                    self.assertEqual(restore.call_args.args[0], [str(ROOT / 'scripts/restore.sh')])
                self.assertEqual([kind for kind, _ in events],
                    ['aprovacao_plano', 'portao_rede', 'preflight', 'restauracao_solicitada', 'restauracao', 'pronto'])
                self.assertEqual((Path(folder) / 'plano-aprovado.md').read_bytes(),
                                 (ROOT / 'plano_humano.md').read_bytes())

    def test_readiness_retries_and_deadline_without_network(self):
        with patch.object(session, 'get_local', side_effect=[OSError('fixture'), (200, b'fixture')]), \
             patch.object(session.time, 'sleep'):
            self.assertEqual(session.wait_ready()['status'], 200)
        with patch.object(session, 'get_local', side_effect=OSError('fixture')), \
             patch.object(session.time, 'monotonic', side_effect=[0, 61]):
            with self.assertRaises(ValueError):
                session.wait_ready()

    def test_services_missing_model_refused(self):
        with patch.object(session.shutil, 'which', return_value='/fixture/nmap'), \
             patch.object(session, 'get_local', return_value=(200, b'{"models":[]}')):
            with self.assertRaises(ValueError):
                session.services()

    def test_authentication_variants_once_and_no_other_credentials(self):
        guard = session.authentication_guard()
        def action(body, path='/rest/user/login'):
            return {'ferramenta': 'http_post', 'parametros': {'path': path, 'body': json.dumps(body)}}
        email = {'email': 'af_inexistente_01@kit11.invalid'}
        for body in ({**email, 'password': 'teste-invalido-01'}, {**email, 'password': ''}, email):
            guard(action(body))
            with self.assertRaises(ValueError):
                guard(action(body))
        for body in ({'email': 'real@example.com', 'password': ''},
                     {**email, 'password': 'payload'}, {**email, 'extra': 'fixture'}):
            with self.assertRaises(ValueError):
                guard(action(body))
        with self.assertRaises(ValueError):
            guard(action(email, '/outra-rota'))

    def test_429_stops_even_if_operator_requests_continue(self):
        proposal = {'hipotese': 'FIXTURE', 'interpretacao': 'MOCK',
                    'ferramenta': 'http_get', 'parametros': {'path': '/'}}
        answers = iter(['a', 'FIXTURE motivo', 'c', 'FIXTURE continuar', 'FIXTURE inconclusiva'])
        with tempfile.TemporaryDirectory() as folder, \
             patch.object(agent, 'model_call', return_value=proposal) as model, \
             patch.object(agent, 'execute', return_value={'status': 429}) as execute, \
             patch.object(agent, 'interpret_result', side_effect=lambda o, a, r, rid: {
                 'resultado_id': rid, 'interpretacao': 'FIXTURE bloqueio', 'limitacoes': 'MOCK'}), \
             contextlib.redirect_stdout(io.StringIO()):
            path = Path(folder) / 'fixture.jsonl'
            agent.run_session('FIXTURE', '127.0.0.1', str(path), input_fn=lambda _: next(answers),
                              plan_confirmed=True, max_actions=3)
            self.assertEqual(model.call_count, 1)
            self.assertEqual(execute.call_count, 1)
            self.assertTrue(any(e['evento'] == 'parada_seguranca' for e in summary.load_events(path)))

    def test_guard_blocks_approved_action_before_execution(self):
        proposal = {'hipotese': 'FIXTURE', 'interpretacao': 'MOCK',
                    'ferramenta': 'http_post', 'parametros': {'path': '/rest/user/login',
                    'body': '{"email":"real@example.com","password":""}'}}
        answers = iter(['a', 'FIXTURE motivo', 'FIXTURE pendência'])
        with tempfile.TemporaryDirectory() as folder, \
             patch.object(agent, 'model_call', return_value=proposal), \
             patch.object(agent, 'execute') as execute, contextlib.redirect_stdout(io.StringIO()):
            path = Path(folder) / 'fixture.jsonl'
            agent.run_session('FIXTURE', '127.0.0.1', str(path), input_fn=lambda _: next(answers),
                plan_confirmed=True, action_guard=session.authentication_guard())
            execute.assert_not_called()
            self.assertTrue(any(e['evento'] == 'acao_bloqueada' for e in summary.load_events(path)))

    def fixture_log(self, folder):
        path = Path(folder) / 'sessao.jsonl'
        plan = (ROOT / 'plano_humano.md').read_bytes()
        summary.private_write(Path(folder) / 'plano-aprovado.md', plan.decode())
        agent.log(str(path), 'aprovacao_plano', run_id='fixture-run', investigation_id='INV-01',
                  tipo_execucao='academica', fixture=True, plano_sha256=hashlib.sha256(plan).hexdigest())
        proposal = {'hipotese': 'FIXTURE H1', 'interpretacao': 'MOCK',
                    'ferramenta': 'http_get', 'parametros': {'path': '/'}}
        interpretation = {'resultado_id': 'fixture-rid', 'interpretacao': 'MOCK resposta',
                          'limitacoes': 'MOCK não comprova vulnerabilidade'}
        # Não alterar o gerador de IDs do logger; interpretação retorna o result_id efetivo.
        with patch.object(agent, 'model_call', return_value=proposal), \
             patch.object(agent, 'execute', return_value={'status': 200}), \
             patch.object(agent, 'interpret_result', side_effect=lambda o, a, r, rid: {**interpretation, 'resultado_id': rid}):
            answers = iter(['a', 'FIXTURE autorização', 'e', 'FIXTURE avaliação inconclusiva', 'FIXTURE conclusão inconclusiva'])
            agent.run_session('FIXTURE MOCK H1', '127.0.0.1', str(path), input_fn=lambda _: next(answers),
                              plan_confirmed=True, investigation_id='INV-01', run_id='fixture-run', max_actions=1)
        return path

    def test_summary_trace_and_fixture_never_updates_status(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.fixture_log(folder)
            events = summary.load_events(path)
            self.assertFalse(summary.audit(events))
            report = summary.summarize(path).read_text()
            self.assertIn('FIXTURE/MOCK', report)
            self.assertIn('candidato previsto', report)
            self.assertIn('FIXTURE conclusão', report)
            for e in events:
                self.assertIn(e['event_id'], report)
            self.assertEqual(os.stat(Path(folder) / 'resumo.md').st_mode & 0o777, 0o600)
            with self.assertRaises(ValueError):
                summary.update_status(path)
            # Alteração posterior do snapshot invalida comparação; não usar plano atual como substituto.
            (Path(folder) / 'plano-aprovado.md').write_text('FIXTURE plano adulterado')
            self.assertIn('Hash do snapshot sem aprovação correspondente', summary.summarize(path).read_text())

    def test_missing_approval_and_interpretation_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            events = summary.load_events(self.fixture_log(folder))
            damaged = [e for e in events if e['evento'] not in ('decisao_humana', 'interpretacao')]
            issues = summary.audit(damaged)
            self.assertTrue(any('autorização' in i for i in issues))
            self.assertTrue(any('sem interpretação' in i for i in issues))

    def test_status_update_is_counts_only_in_temporary_repository(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'docs').mkdir()
            for name in ('CHECKLIST_RUBRICA.md', 'docs/STATE.md'):
                (root / name).write_text('Histórico preservado\n')
            path = root / 'real-format.jsonl'
            # Fixture do formato acadêmico, somente em árvore temporária; não é execução real.
            path.write_text(json.dumps({'event_id': 'fixture-e', 'evento': 'preparacao',
                'run_id': 'fixture-run', 'investigation_id': 'INV-03', 'tipo_execucao': 'academica'}) + '\n')
            with patch.object(summary, 'ROOT', root):
                summary.update_status(path)
                summary.update_status(path)
            content = (root / 'docs/STATE.md').read_text()
            self.assertEqual(content.count('<!-- AF-AUTO-INV-03 -->'), 1)
            self.assertIn('Histórico preservado', content)
            self.assertIn('PENDENTE', content)
            self.assertNotIn('CONCLUÍDO', content)

    def test_summary_refuses_symlink_output_and_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.fixture_log(folder)
            output = Path(folder) / 'resumo.md'
            victim = Path(folder) / 'victim'
            victim.write_text('preservar')
            output.symlink_to(victim)
            with self.assertRaises(ValueError):
                summary.summarize(path)
            self.assertEqual(victim.read_text(), 'preservar')
            line = path.read_text().splitlines()[0]
            path.write_text(line + '\n' + line + '\n')
            with self.assertRaises(ValueError):
                summary.load_events(path)


if __name__ == '__main__':
    unittest.main()
