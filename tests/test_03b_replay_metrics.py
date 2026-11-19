"""Replay e métricas com dados sintéticos; nenhum contato com laboratório."""
import copy
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import af_replay
import af_metrics
import af_refine
import af_03b_controls
import agent


class ReplayMetricsTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((ROOT / 'fixtures/03b/replay-simulado.json').read_text())

    def test_replay_dry_run_has_no_effects(self):
        with patch('agent.execute', side_effect=AssertionError('executor chamado')), \
             patch('subprocess.run', side_effect=AssertionError('subprocess chamado')), \
             patch('http.client.HTTPConnection', side_effect=AssertionError('HTTP chamado')), \
             patch('urllib.request.build_opener', side_effect=AssertionError('rede chamada')):
            self.assertEqual(af_replay.main([str(ROOT / 'fixtures/03b/replay-simulado.json')]), 0)

    def test_invalid_stability_and_fixture_provenance_rejected(self):
        invalid = copy.deepcopy(self.fixture)
        invalid['cases'][0]['branches'][1]['context']['historico'] = []
        with self.assertRaises(ValueError):
            af_replay.validate_cases(invalid)
        invalid = copy.deepcopy(self.fixture)
        invalid['cases'][0]['evidence_source']['result_id'] = 'fabricado'
        with self.assertRaises(ValueError):
            af_replay.validate_cases(invalid)

    def test_counterfactual_pairs_reject_uncontrolled_changes(self):
        sensitivity = next(c for c in self.fixture['cases'] if c['pair_type'] == 'sensibilidade')
        memory = next(c for c in self.fixture['cases'] if c['pair_type'] == 'memoria')
        for case, mutate in ((sensitivity, lambda c: c['branches'][1]['context'].update(objetivo='outro')),
                             (memory, lambda c: c['branches'][1]['context'].update(fato_extra='não observado'))):
            case = copy.deepcopy(case)
            mutate(case)
            with self.assertRaises(ValueError):
                af_replay.validate_cases({'cases': [case]})

    def test_static_scope_is_conservative(self):
        proposal = {'hipotese': 'fixture', 'interpretacao': 'fixture', 'ferramenta': 'http_get',
                    'parametros': {'path': '/ftp/arquivo-inexistente-af.md'}}
        self.assertTrue(af_replay.valid_proposal(proposal))
        self.assertEqual(af_replay.scope_status(proposal, 'INV-03-B', ['http_get']), 'permitida_condicional')
        proposal['parametros']['path'] = '/ftp/segredo'
        self.assertEqual(af_replay.scope_status(proposal, 'INV-03-B', ['http_get']), 'fora_escopo')

    def test_ollama_requires_tty_before_any_network(self):
        with patch('sys.stdin.isatty', return_value=False), patch('af_replay.local_request', side_effect=AssertionError('rede chamada')):
            with self.assertRaises(SystemExit):
                af_replay.main([str(ROOT / 'fixtures/03b/replay-simulado.json'), '--ollama',
                                '--model-digest', 'fixture', '--output', '/tmp/fixture.jsonl'])

    def test_replay_mock_model_never_executes_and_does_not_overwrite(self):
        proposal = {'hipotese': 'FIXTURE', 'interpretacao': 'FIXTURE',
                    'ferramenta': 'nmap', 'parametros': {}}
        envelope = {'done': True, 'done_reason': 'stop', 'response': json.dumps(proposal),
                    'eval_count': 4, 'prompt_eval_count': 8}
        with tempfile.TemporaryDirectory() as td:
            cases = Path(td) / 'cases.json'
            cases.write_text(json.dumps({'cases': [self.fixture['cases'][0]]}))
            output = Path(td) / 'session.jsonl'
            with patch('sys.stdin.isatty', return_value=True), patch('builtins.input', return_value='REPLAY'), \
                 patch.object(af_replay, 'REPLAY_BUDGET_ROOT', Path(td) / 'budget'), \
                 patch.object(af_replay, 'local_request', side_effect=[{'models': [{'name': af_replay.MODEL, 'digest': 'fixture'}]}, envelope, envelope]), \
                 patch('agent.execute', side_effect=AssertionError('executor chamado')), \
                 patch('subprocess.run', side_effect=AssertionError('subprocess chamado')), \
                 patch('http.client.HTTPConnection', side_effect=AssertionError('HTTP chamado')):
                args = [str(cases), '--ollama', '--model-digest', 'fixture', '--output', str(output)]
                self.assertEqual(af_replay.main(args), 0)
                before = output.read_bytes()
                with self.assertRaises(FileExistsError):
                    af_replay.main(args)
                self.assertEqual(output.read_bytes(), before)
            events = [json.loads(line) for line in output.read_text().splitlines()]
            self.assertEqual(sum(e['evento'] == 'proposta' for e in events), 2)
            self.assertTrue(all(e.get('trial_type') == 'replay_fixture' for e in events if e['evento'] == 'proposta'))

    def test_budget_is_shared_between_invocations_and_counts_interrupted_requests(self):
        with tempfile.TemporaryDirectory() as td, patch.object(af_replay, 'REPLAY_BUDGET_ROOT', Path(td) / 'budget'):
            for index in range(14):
                af_replay.replay_budget(proposal_id=f'fixture-{index}')
            with self.assertRaisesRegex(ValueError, 'esgotado'):
                af_replay.replay_budget(required=1)

    def test_budget_migrates_historical_requests_without_modifying_logs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'budget'
            old_dir = root / 'antigo'
            old_dir.mkdir(mode=0o700, parents=True)
            old = old_dir / 'sessao.jsonl'
            old.write_text(''.join(json.dumps({'evento': 'solicitacao_modelo',
                'origem_decisao': 'replay_sem_execucao'}) + '\n' for _ in range(17)))
            old.chmod(0o600)
            before = old.read_bytes()
            with patch.object(af_replay, 'REPLAY_BUDGET_ROOT', root):
                with self.assertRaisesRegex(ValueError, '17/14'):
                    af_replay.replay_budget()
                with patch('sys.stdin.isatty', return_value=True), patch('builtins.input', return_value='REPLAY'), \
                     patch.object(af_replay, 'local_request', side_effect=AssertionError('rede chamada')):
                    with self.assertRaisesRegex(ValueError, '17/14'):
                        af_replay.main([str(ROOT / 'fixtures/03b/replay-simulado.json'), '--ollama',
                                        '--model-digest', 'fixture', '--output', str(root / 'nova.jsonl')])
            self.assertEqual(old.read_bytes(), before)

    def test_zero_denominator_and_fixture_origin(self):
        events = [{'event_id': 'a', 'run_id': 'a' * 32, 'evento': 'inicio',
                   'trial_type': 'replay_fixture', 'scenario': 'INV-01-B'}]
        measured = af_metrics.measure(events)
        self.assertEqual(measured['json_validos_por_tentativa'], 'N/A (0/0)')
        self.assertEqual(measured['trial_type'], 'replay_fixture')
        self.assertIn('N/A', measured['avaliacao_semantica'])

    def test_human_review_metrics_require_provenance_and_unique_ids(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'avaliacoes.csv'
            path.write_text('claim_id,classe,justificativa,avaliador,data\n'
                            'fixture-1,2,FIXTURE motivo,FIXTURE revisor,2026-01-01\n'
                            'fixture-2,0,FIXTURE motivo,FIXTURE revisor,2026-01-01\n')
            self.assertEqual(af_metrics.reviewed_ratio(path, 'classe', {'0', '1', '2', '3'}, {'2', '3'}, 'claim_id'), '1/2')
            with path.open('a') as stream:
                stream.write('fixture-1,3,FIXTURE outro,FIXTURE revisor,2026-01-01\n')
            with self.assertRaises(ValueError):
                af_metrics.reviewed_ratio(path, 'classe', {'0', '1', '2', '3'}, {'2', '3'}, 'claim_id')

    def test_metrics_does_not_export_response_body(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'source.jsonl'
            event = {'event_id': 'a', 'run_id': 'a' * 32, 'evento': 'inicio',
                     'trial_type': 'replay_fixture', 'resultado': {'body': 'senha=exemplo-segredo'}}
            path.write_text(json.dumps(event) + '\n')
            out = Path(td) / 'out'
            out.mkdir(mode=0o700)
            af_metrics.main([str(path), '--output-dir', str(out)])
            for p in out.iterdir():
                self.assertNotIn('exemplo-segredo', p.read_text())

    def test_fixture_cannot_be_promoted_by_grouping(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'source.jsonl'
            events = [{'event_id': '1', 'run_id': 'a' * 32, 'evento': 'inicio', 'fixture': True},
                      {'event_id': '2', 'run_id': 'a' * 32, 'evento': 'proposta',
                       'trial_type': 'real', 'scenario': 'INV-01-B', 'proposal_id': 'fixture'}]
            path.write_text(''.join(json.dumps(event) + '\n' for event in events))
            out = Path(td) / 'out'
            out.mkdir(mode=0o700)
            af_metrics.main([str(path), '--output-dir', str(out)])
            self.assertIn('fixture_de_teste', (out / 'metricas.csv').read_text())
            self.assertIn('FIXTURE/NÃO REAL', (out / 'metricas.md').read_text())

    def test_live_mode_refuses_pipe_before_preparation(self):
        with patch('sys.stdin.isatty', return_value=False), patch('af_refine.prepare', side_effect=AssertionError('preparação chamada')):
            with self.assertRaises(SystemExit):
                af_refine.main(['INV-01-B'])

    def test_03b_rejects_injected_input_or_delegated_reviewer(self):
        meta = {'phase': '03B', 'scenario': 'INV-01-B', 'trial_type': 'real',
                'origem_decisao': 'entrada_terminal_humana'}
        with tempfile.TemporaryDirectory() as td, patch.object(agent, 'execute') as execute, \
             patch('sys.stdin.isatty', return_value=True), patch('sys.stdout.isatty', return_value=True):
            for extra in ({'input_fn': lambda _: 'a'}, {'reviewer': lambda *_: {}}, {}):
                # O último caso também falha porque não forneceu todos os guardas.
                with self.assertRaises(ValueError):
                    agent.run_session('fixture', '127.0.0.1', str(Path(td) / 'fixture.jsonl'),
                                      plan_confirmed=True, investigation_id='INV-01', max_actions=6,
                                      session_metadata=meta, **extra)
            execute.assert_not_called()

    def test_modification_log_failure_aborts_before_confirmation(self):
        proposal = {'hipotese': 'FIXTURE', 'interpretacao': 'FIXTURE',
                    'ferramenta': 'http_get', 'parametros': {'path': '/'}}
        answers = iter(['m', json.dumps(proposal)])
        with self.assertRaisesRegex(ValueError, 'falha de log'):
            agent.review(proposal, lambda _: next(answers),
                         lambda *args, **kwargs: (_ for _ in ()).throw(ValueError('falha de log')),
                         trace_confirmation=True)

    def test_quick_review_pause_does_not_approve_and_rejection_is_explicit(self):
        proposal = {'hipotese': 'FIXTURE', 'interpretacao': 'FIXTURE',
                    'ferramenta': 'http_get', 'parametros': {'path': '/'}}
        events = []
        with patch.object(agent, 'read_key', side_effect=['p', 'c', 'r']):
            decision, action = agent.quick_review(proposal, 'FIXTURE objetivo', 'INV-01-B', [],
                                                  lambda kind, **fields: events.append((kind, fields)))
        self.assertEqual((decision, action), ('rejeitada', None))
        self.assertEqual(events[0][1]['decisao'], 'pausada')
        self.assertIsNone(events[0][1]['justificativa'])

    def test_nmap_review_shows_effective_scope_and_arguments(self):
        proposal = {'hipotese': 'FIXTURE', 'interpretacao': 'FIXTURE motivo',
                    'ferramenta': 'nmap', 'parametros': {}}
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch.object(agent, 'read_key', return_value='r'):
            agent.quick_review(proposal, 'FIXTURE objetivo', 'INV-01-B', [], lambda *_args, **_kwargs: None)
        for text in ('INV-01-B', 'FIXTURE objetivo', 'FIXTURE motivo', '127.0.0.1', '3000', '-sT', '--host-timeout', 'Riscos e limites'):
            self.assertIn(text, output.getvalue())

    def test_03b_without_supervisor_cannot_call_model_or_tool(self):
        meta = {'phase': '03B', 'scenario': 'INV-01-B', 'trial_type': 'real',
                'origem_decisao': 'entrada_terminal_humana'}
        with tempfile.TemporaryDirectory() as td, patch('sys.stdin.isatty', return_value=True), \
             patch('sys.stdout.isatty', return_value=True), patch.object(agent, 'model_call') as model, \
             patch.object(agent, 'execute') as execute:
            with self.assertRaisesRegex(ValueError, 'supervisor'):
                agent.run_session('FIXTURE', '127.0.0.1', str(Path(td) / 'fixture.jsonl'),
                                  plan_confirmed=True, investigation_id='INV-01', max_actions=6,
                                  session_metadata=meta, action_guard=lambda _: None, result_guard=lambda _: None,
                                  result_observer=lambda *_: None, context_provider=af_03b_controls.factual_context)
            model.assert_not_called()
            execute.assert_not_called()

    def test_quick_modification_requires_second_approval(self):
        proposal = {'hipotese': 'FIXTURE', 'interpretacao': 'FIXTURE',
                    'ferramenta': 'http_get', 'parametros': {'path': '/'}}
        changed = {**proposal, 'parametros': {'path': '/api/Products/1'}}
        events = []
        with patch.object(agent, 'read_key', side_effect=['m', 'r']), \
             patch('builtins.input', return_value=json.dumps(changed)):
            decision, _ = agent.quick_review(proposal, 'FIXTURE objetivo', 'INV-01-B', [],
                                             lambda kind, **fields: events.append((kind, fields)))
        self.assertEqual(decision, 'modificada_rejeitada')
        self.assertFalse(any(kind == 'confirmacao_modificacao_humana' for kind, _ in events))
        with patch.object(agent, 'read_key', side_effect=['m', 'a']), \
             patch('builtins.input', return_value=json.dumps(changed)):
            decision, action = agent.quick_review(proposal, 'FIXTURE objetivo', 'INV-01-B', [],
                                                  lambda kind, **fields: events.append((kind, fields)))
        self.assertEqual((decision, action), ('modificada_aprovada', changed))
        self.assertTrue(any(kind == 'confirmacao_modificacao_humana' for kind, _ in events))

    def test_fixture_pause_and_finish_never_executes(self):
        proposal = {'hipotese': 'FIXTURE', 'interpretacao': 'FIXTURE',
                    'ferramenta': 'http_get', 'parametros': {'path': '/'}}
        meta = {'phase': '03B', 'scenario': 'INV-01-B', 'trial_type': 'real',
                'origem_decisao': 'entrada_terminal_humana', 'supervisor': 'FIXTURE Supervisor'}
        with tempfile.TemporaryDirectory() as td, patch('sys.stdin.isatty', return_value=True), \
             patch('sys.stdout.isatty', return_value=True), patch('builtins.input', return_value='FIXTURE pendente'), \
             patch.object(agent, 'read_key', side_effect=['p', 'e']), \
             patch.object(agent, 'model_call', return_value=proposal), patch.object(agent, 'execute') as execute:
            path = Path(td) / 'fixture.jsonl'
            agent.run_session('FIXTURE', '127.0.0.1', str(path), plan_confirmed=True,
                              investigation_id='INV-01', max_actions=6, session_metadata=meta,
                              action_guard=lambda _: None, result_guard=lambda _: None,
                              result_observer=lambda *_: None, context_provider=af_03b_controls.factual_context)
            execute.assert_not_called()
            decisions = [json.loads(line) for line in path.read_text().splitlines()
                         if json.loads(line)['evento'] == 'decisao_humana']
            self.assertEqual([row['decisao'] for row in decisions], ['pausada', 'encerrada'])
            self.assertTrue(all(row['supervisor'] == 'FIXTURE Supervisor' for row in decisions))

    def test_fixture_modified_action_is_revalidated_before_execute(self):
        proposal = {'hipotese': 'FIXTURE', 'interpretacao': 'FIXTURE',
                    'ferramenta': 'http_get', 'parametros': {'path': '/'}}
        changed = {**proposal, 'parametros': {'path': '/fora-do-plano'}}
        guard = af_03b_controls.ScenarioGuard('INV-01-B')
        meta = {'phase': '03B', 'scenario': 'INV-01-B', 'trial_type': 'real',
                'origem_decisao': 'entrada_terminal_humana', 'supervisor': 'FIXTURE Supervisor'}
        with tempfile.TemporaryDirectory() as td, patch('sys.stdin.isatty', return_value=True), \
             patch('sys.stdout.isatty', return_value=True), \
             patch('builtins.input', side_effect=[json.dumps(changed), 'FIXTURE pendente']), \
             patch.object(agent, 'read_key', side_effect=['m', 'a']), \
             patch.object(agent, 'model_call', return_value=proposal), patch.object(agent, 'execute') as execute:
            path = Path(td) / 'fixture.jsonl'
            agent.run_session('FIXTURE', '127.0.0.1', str(path), plan_confirmed=True,
                              investigation_id='INV-01', max_actions=6, session_metadata=meta,
                              action_guard=guard.check, result_guard=lambda _: None,
                              result_observer=lambda *_: None, context_provider=af_03b_controls.factual_context)
            execute.assert_not_called()
            events = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertTrue(any(e['evento'] == 'confirmacao_modificacao_humana' for e in events))
            self.assertTrue(any(e['evento'] == 'acao_bloqueada' for e in events))

    def test_fixture_cycle_links_variants_and_passes_ledger_to_next_proposal(self):
        def post(password):
            return {'hipotese': 'FIXTURE', 'interpretacao': 'FIXTURE', 'ferramenta': 'http_post',
                    'parametros': {'path': '/rest/user/login', 'body': json.dumps({
                        'email': 'af_inexistente_01@kit11.invalid', 'password': password})}}
        guard = af_03b_controls.ScenarioGuard('INV-02-B')
        meta = {'phase': '03B', 'scenario': 'INV-02-B', 'trial_type': 'real',
                'origem_decisao': 'entrada_terminal_humana', 'supervisor': 'FIXTURE Supervisor'}
        answers = ['c', 'FIXTURE avaliação A', 'e', 'FIXTURE avaliação B', 'FIXTURE conclusão']
        with tempfile.TemporaryDirectory() as td, patch('sys.stdin.isatty', return_value=True), \
             patch('sys.stdout.isatty', return_value=True), patch('builtins.input', side_effect=answers), \
             patch.object(agent, 'read_key', side_effect=['a', 'a']), \
             patch.object(agent, 'model_call', side_effect=[post('teste-invalido-01'), post('')]) as model, \
             patch.object(agent, 'execute', return_value={'status': 401, 'truncated': False, 'body': 'fixture'}) as execute, \
             patch.object(agent, 'interpret_result', side_effect=lambda o, a, r, rid: {
                 'resultado_id': rid, 'interpretacao': 'FIXTURE', 'limitacoes': 'FIXTURE'}):
            path = Path(td) / 'fixture.jsonl'
            agent.run_session('FIXTURE', '127.0.0.1', str(path), plan_confirmed=True,
                              investigation_id='INV-02', max_actions=6, session_metadata=meta,
                              action_guard=guard.check, result_guard=lambda _: None,
                              result_observer=guard.observe, context_provider=af_03b_controls.factual_context)
            events = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(execute.call_count, 2)
            self.assertEqual([e['variant'] for e in events if e['evento'] == 'resultado'], ['A', 'B'])
            decisions = [e for e in events if e['evento'] == 'decisao_humana']
            self.assertTrue(all(e['supervisor'] == 'FIXTURE Supervisor' and e['justificativa'] is None for e in decisions))
            ledger = model.call_args_list[1].kwargs['context']['ledger']
            self.assertEqual([record['observado']['variant'] for record in ledger], ['A'])
            self.assertEqual(ledger[0]['origem_avaliacao'], 'entrada_terminal')

    def test_live_result_gate_stops_on_redirect_error_or_block(self):
        for result in ({'status': 302}, {'status': 423}, {'status': 429},
                       {'error': 'timeout'}, {'body': '[REDACTED]'}):
            with self.subTest(result=result), self.assertRaises(ValueError):
                af_refine.safe_result(result)

    def test_live_mode_wires_guards_and_provenance_with_fixtures(self):
        with tempfile.TemporaryDirectory() as td:
            temp_root = Path(td)
            with patch('sys.stdin.isatty', return_value=True), patch('sys.stdout.isatty', return_value=True), \
                 patch('af_refine.ROOT', temp_root), patch('af_refine.command', return_value='f' * 40), \
                 patch('af_refine.sha', return_value='a' * 64), \
                 patch('af_refine.required', side_effect=['FIXTURE Supervisor', 'FIXTURE pessoas', 'FIXTURE data', 'FIXTURE motivo']), \
                 patch('af_refine.confirm'), patch('af_refine.prepare', side_effect=lambda inv, emit, directory, pre_restore_guard: pre_restore_guard()), patch('af_refine.identity', return_value='fixture-id'), \
                 patch('af_refine.services', return_value={'digest_modelo': 'd' * 64}), \
                 patch('agent.run_session') as session:
                self.assertEqual(af_refine.main(['INV-01-B', '--context-mode', 'B']), 0)
                kwargs = session.call_args.kwargs
                self.assertEqual(kwargs['session_metadata']['trial_type'], 'real')
                self.assertEqual(kwargs['session_metadata']['context_mode'], 'B')
                self.assertIs(kwargs['context_provider'], af_refine.factual_context)
                with self.assertRaises(ValueError):
                    kwargs['action_guard']({'hipotese': 'fixture', 'interpretacao': 'fixture',
                                            'ferramenta': 'http_get', 'parametros': {'path': '/proibido'}})

    def test_changed_v2_plan_aborts_before_mock_restoration(self):
        with tempfile.TemporaryDirectory() as td:
            state = {'changed': False}
            def fake_sha(path):
                return 'changed' if path == af_refine.PLAN_V2 and state['changed'] else 'original'
            def fixture_prepare(inv, emit, directory, pre_restore_guard):
                state['changed'] = True
                pre_restore_guard()
                self.fail('restauração simulada não deve ser atingida')
            with patch('sys.stdin.isatty', return_value=True), patch('sys.stdout.isatty', return_value=True), \
                 patch('af_refine.ROOT', Path(td)), patch('af_refine.command', return_value='f' * 40), \
                 patch('af_refine.sha', side_effect=fake_sha), \
                 patch('af_refine.required', side_effect=['FIXTURE Supervisor', 'FIXTURE pessoas', 'FIXTURE data', 'FIXTURE motivo']), \
                 patch('af_refine.confirm'), patch('af_refine.prepare', side_effect=fixture_prepare), \
                 patch('agent.run_session') as session:
                self.assertEqual(af_refine.main(['INV-01-B']), 1)
                session.assert_not_called()


if __name__ == '__main__':
    unittest.main()
