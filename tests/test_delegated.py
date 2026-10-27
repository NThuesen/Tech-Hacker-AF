"""Fixtures explícitas para delegação; não são investigações reais."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import agent
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import af_delegated as delegated
import af_summarize as summary


class DelegatedTests(unittest.TestCase):
    proposal = {'hipotese': 'FIXTURE', 'interpretacao': 'MOCK',
                'ferramenta': 'http_get', 'parametros': {'path': '/'}}

    def test_delegated_decision_is_not_human_and_review_reaches_next_model_call(self):
        answers = iter([{'decisao': 'aprovada', 'acao_final': self.proposal, 'justificativa': 'FIXTURE controle'},
                        {'decisao': 'c', 'justificativa': 'FIXTURE corrigir inferência'},
                        {'decisao': 'rejeitada', 'justificativa': 'FIXTURE repetição'},
                        {'conclusao': 'FIXTURE inconclusiva'}])
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()), \
             patch.object(agent, 'model_call', return_value=self.proposal) as model, \
             patch.object(agent, 'execute', return_value={'status': 200}) as execute, \
             patch.object(agent, 'interpret_result', side_effect=lambda o,a,r,rid: {
                 'resultado_id': rid, 'interpretacao': 'FIXTURE', 'limitacoes': 'MOCK'}):
            path = Path(folder) / 'sessao.jsonl'
            agent.run_session('FIXTURE', '127.0.0.1', str(path), plan_confirmed=True,
                              max_actions=2, reviewer=lambda phase,payload: next(answers))
            events = summary.load_events(path)
            self.assertFalse(summary.audit(events))
            self.assertFalse(any(e['evento'] in ('decisao_humana','conclusao_humana') for e in events))
            self.assertEqual(execute.call_count, 1)
            self.assertIn('avaliacao_revisor', model.call_args.args[1][0])

    def test_wrong_approval_cannot_execute(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()), \
             patch.object(agent, 'model_call', return_value=self.proposal), \
             patch.object(agent, 'execute') as execute:
            with self.assertRaises(ValueError):
                agent.run_session('FIXTURE', '127.0.0.1', str(Path(folder)/'sessao.jsonl'),
                    plan_confirmed=True, reviewer=lambda *args: {
                        'decisao':'aprovada', 'acao_final':None, 'justificativa':'FIXTURE'})
            execute.assert_not_called()

    def test_modified_action_requires_matching_second_approval(self):
        changed = {**self.proposal, 'parametros': {'path':'/rest/admin/application-version'}}
        answers = iter([{'decisao':'modificada_aprovada', 'acao_final':changed, 'justificativa':'FIXTURE'},
                        {'decisao':'aprovada', 'acao_final':self.proposal, 'justificativa':'MOCK divergente'}])
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()), \
             patch.object(agent, 'model_call', return_value=self.proposal), \
             patch.object(agent, 'execute') as execute:
            with self.assertRaises(ValueError):
                agent.run_session('FIXTURE', '127.0.0.1', str(Path(folder)/'sessao.jsonl'),
                    plan_confirmed=True, reviewer=lambda *args: next(answers))
            execute.assert_not_called()

    def test_sensitive_response_never_reaches_model_interpretation(self):
        answers = iter([{'decisao':'aprovada', 'acao_final':self.proposal, 'justificativa':'FIXTURE'},
                        {'conclusao':'FIXTURE interrupção por possível segredo'}])
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()), \
             patch.object(agent, 'model_call', return_value=self.proposal), \
             patch.object(agent, 'execute', return_value={'body':'{"token":"fixture-sensitive"}'}), \
             patch.object(agent, 'interpret_result') as interpretation:
            path = Path(folder)/'sessao.jsonl'
            agent.run_session('FIXTURE', '127.0.0.1', str(path), plan_confirmed=True,
                reviewer=lambda *args: next(answers), result_guard=delegated.result_guard)
            interpretation.assert_not_called()
            self.assertTrue(any(e['evento']=='parada_seguranca' for e in summary.load_events(path)))

    def test_modified_action_executes_after_second_review_with_channel_metadata(self):
        changed = {**self.proposal, 'ferramenta':'nmap', 'parametros':{}}
        answers = iter([{'decisao':'modificada_aprovada','acao_final':changed,'justificativa':'FIXTURE'},
                        {'decisao':'aprovada','acao_final':changed,'justificativa':'FIXTURE segunda',
                         'operador':'Codex','request_id':'fixture-request'},
                        {'decisao':'e','justificativa':'FIXTURE encerrar'},
                        {'conclusao':'FIXTURE inconclusiva'}])
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()), \
             patch.object(agent, 'model_call', return_value=self.proposal), \
             patch.object(agent, 'execute', return_value={'exit_code':0}) as execute, \
             patch.object(agent, 'interpret_result', side_effect=lambda o,a,r,rid: {
                 'resultado_id':rid,'interpretacao':'FIXTURE','limitacoes':'MOCK'}):
            path = Path(folder)/'sessao.jsonl'
            agent.run_session('FIXTURE', '127.0.0.1', str(path), plan_confirmed=True,
                              reviewer=lambda *args: next(answers))
            execute.assert_called_once_with(changed, '127.0.0.1')
            events = summary.load_events(path)
            self.assertFalse(summary.audit(events))
            damaged = [e for e in events if e['evento']!='confirmacao_modificacao_delegada']
            self.assertTrue(any('segunda aprovação' in i for i in summary.audit(damaged)))

    def test_scope_and_identity_guards(self):
        with patch.object(delegated, 'identity', return_value='fixture-id'):
            guard = delegated.scope_guard('INV-03', 'fixture-id')
            guard(self.proposal)
            for path in ('/ftp/acquisitions.md', '/../etc/passwd', '/rest/user/login', '//external'):
                with self.assertRaises(ValueError):
                    guard({**self.proposal, 'parametros': {'path':path}})
        with patch.object(delegated, 'identity', return_value='changed'):
            with self.assertRaises(ValueError):
                delegated.scope_guard('INV-01', 'fixture-id')(self.proposal)

    def test_sensitive_or_blocked_result_stops(self):
        for result in ({'status':429}, {'error':'FIXTURE'}, {'body':'{"token":"secret-value"}'},
                       {'body':'-----BEGIN RSA PRIVATE KEY-----'}, {'body':'{"token":"[REDACTED]"}'}):
            with self.assertRaises(ValueError):
                delegated.result_guard(result)
        delegated.result_guard({'status':401,'body':'Invalid email or password.'})

    def test_channel_no_default_approval_and_wrong_request_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                delegated.ReviewChannel(Path(folder), timeout=0)('proposta', {})
            class FakeTime:
                def __init__(self): self.called = False
                def __call__(self, seconds):
                    request = json.loads((Path(folder)/'revisao-pendente.json').read_text())
                    summary.private_write(Path(folder)/(request['request_id']+'.decisao.json'),
                                          json.dumps({'request_id':'wrong','operador':'Codex'}))
            with patch.object(delegated.time, 'sleep', side_effect=FakeTime()):
                with self.assertRaises(ValueError):
                    delegated.ReviewChannel(Path(folder), timeout=1)('proposta', {})


if __name__ == '__main__':
    unittest.main()
