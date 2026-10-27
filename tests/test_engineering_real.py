"""Opt-in: Ollama/Qwen, HTTP Juice Shop e Nmap REAIS; sem mocks.

Somente engenharia autorizada. O gate automatizado NÃO representa decisão humana.
Nenhuma proposta fora da lista de consultas técnicas é executada.
"""
import json
import os
import time
import unittest
import uuid

import agent


def fixture_action(path):
    return {'hipotese': 'A rota pública indicada pode responder a uma leitura GET',
            'interpretacao': 'Coleta técnica controlada, sem inferência acadêmica',
            'ferramenta': 'http_get', 'parametros': {'path': path}}


@unittest.skipUnless(os.environ.get('KIT11_REAL_TESTS') == '1', 'integração real opt-in')
class RealEngineeringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.run_id = uuid.uuid4().hex
        cls.path = 'logs/engenharia-' + cls.run_id + '.jsonl'
        agent.log(cls.path, 'inicio_engenharia', run_id=cls.run_id,
                  tipo_execucao='engenharia_automatizada', modelo=agent.MODEL,
                  supervisao='gate técnico automatizado; não é decisão humana')
        print('\nEVIDENCIA_REAL:', cls.path, flush=True)

    def emit(self, event, **fields):
        agent.log(self.path, event, run_id=self.run_id,
                  tipo_execucao='engenharia_automatizada', **fields)

    def collect(self, action, step_id):
        refs = dict(step_id=step_id, execution_id=uuid.uuid4().hex, result_id=uuid.uuid4().hex)
        self.emit('gate_tecnico', **refs, acao=action, origem='fixture_de_engenharia')
        started = time.monotonic()
        result = agent.execute(action, '127.0.0.1')
        self.emit('resultado', **refs, acao=action, resultado=result,
                  duracao_s=round(time.monotonic() - started, 6))
        self.assertNotIn('error', result)
        return refs, result

    def test_model_proposal_execution_and_interpretation(self):
        objective = ('Ensaio técnico autorizado: verificar somente a disponibilidade HTTP pública local. '
                     'Escolha uma leitura GET / ou /rest/admin/application-version, ou nmap na porta fixa. '
                     'Não acessar autenticação nem elaborar plano acadêmico.')
        proposal_id = uuid.uuid4().hex
        started = time.monotonic()
        proposal = agent.model_call(objective, [])
        self.emit('proposta', step_id='smoke', proposal_id=proposal_id, proposta=proposal,
                  duracao_s=round(time.monotonic() - started, 6))
        safe = (proposal['ferramenta'] == 'nmap' or
                (proposal['ferramenta'] == 'http_get' and
                 proposal['parametros']['path'] in ('/', '/rest/admin/application-version')))
        self.emit('gate_tecnico', proposal_id=proposal_id, autorizado=safe,
                  origem='allowlist de engenharia; não humano')
        self.assertTrue(safe, 'proposta válida mas fora do ensaio técnico: não executada')
        refs, result = self.collect(proposal, 'smoke')
        interpretation = agent.interpret_result(objective, proposal, result, refs['result_id'])
        self.emit('interpretacao', **refs, proposal_id=proposal_id, interpretacao=interpretation)
        self.assertEqual(interpretation['resultado_id'], refs['result_id'])
        # Segunda ferramenta real, fixa pela fixture e identificada como tal.
        other = fixture_action('/') if proposal['ferramenta'] == 'nmap' else {
            'hipotese': 'A porta TCP local 3000 pode estar aberta', 'interpretacao': 'Engenharia', 'ferramenta': 'nmap', 'parametros': {}}
        refs, result = self.collect(other, 'segunda-ferramenta')
        interpretation = agent.interpret_result(objective, other, result, refs['result_id'])
        self.emit('interpretacao', **refs, interpretacao=interpretation)

    def test_different_real_evidence_changes_next_proposal(self):
        objective = ('Ensaio de engenharia: confirmar leitura pública de um único produto e identificação '
                     'da versão da aplicação. Avalie o que já foi observado e proponha a próxima '
                     'medição útil sem repetir medições já satisfeitas. O ensaio permite apenas '
                     'GET /api/Products/1, GET /rest/admin/application-version ou nmap na porta fixa. '
                     'Não listar todo o catálogo, testar autenticação, escrever dados ou planejar investigação acadêmica.')
        proposals = []
        for label, path, expected_status in (
                ('A', '/api/Products/1', 200), ('B', '/api/Products/0', 404)):
            action = fixture_action(path)
            refs, result = self.collect(action, label)
            self.assertEqual(result.get('status'), expected_status)
            interpretation = agent.interpret_result(objective, action, result, refs['result_id'])
            self.emit('interpretacao', **refs, interpretacao=interpretation)
            history = [{**refs, 'acao': action, 'resultado': result,
                        'interpretacao_resultado': interpretation,
                        'origem': 'fixture técnica real; sem decisão humana'}]
            proposal = agent.model_call(objective, history)
            self.emit('proposta_condicional', **refs, proposal_id=uuid.uuid4().hex,
                      proposta=proposal, executada=False)
            proposals.append(proposal)
        signatures = [(p['ferramenta'], p['parametros']) for p in proposals]
        self.emit('comparacao_condicional', assinaturas=signatures,
                  diferentes=signatures[0] != signatures[1])
        print('COMPARACAO_REAL:', json.dumps(signatures, ensure_ascii=True), flush=True)
        self.assertNotEqual(signatures[0], signatures[1],
                            'modelo não adaptou ferramenta/parâmetros neste ensaio; registrar limitação')

    def test_large_real_http_result_uses_bounded_context(self):
        action = fixture_action('/')
        refs, result = self.collect(action, 'html-extenso')
        self.assertEqual(result.get('status'), 200)
        compact = agent.compact_context(result)
        self.assertLessEqual(len(compact['body'].encode()), 2048)
        self.assertTrue(compact['body_contexto']['truncado'])
        interpretation = agent.interpret_result(
            'Ensaio de engenharia: descrever apenas o status, formato e limites da leitura HTTP da página inicial.',
            action, result, refs['result_id'])
        self.emit('interpretacao', **refs, interpretacao=interpretation)
        self.assertEqual(interpretation['resultado_id'], refs['result_id'])

    @classmethod
    def tearDownClass(cls):
        agent.log(cls.path, 'fim_engenharia', run_id=cls.run_id,
                  tipo_execucao='engenharia_automatizada', conclusao_humana=None)


if __name__ == '__main__':
    unittest.main()
