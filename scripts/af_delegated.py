#!/usr/bin/env python3
"""Operação delegada explícita: Qwen propõe; Codex revisa via arquivos privados."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid

from af_session import ROOT, SCENARIOS, authentication_guard, identity, services, wait_ready
from af_summarize import private_write, summarize, load_events
import agent


class ReviewChannel:
    """Sem aceite padrão; IDs vinculam cada resposta a uma solicitação única."""
    def __init__(self, directory, timeout=1800):
        self.directory, self.timeout = directory, timeout

    def __call__(self, phase, payload):
        request_id = uuid.uuid4().hex
        request = {'request_id': request_id, 'fase': phase, **payload}
        raw = json.dumps(request, ensure_ascii=False)
        private_write(self.directory / (request_id + '.solicitacao.json'), raw)
        private_write(self.directory / 'revisao-pendente.json', raw)
        response_path = self.directory / (request_id + '.decisao.json')
        print(f'REVISAO {phase} {request_id}', flush=True)
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            if response_path.exists():
                if response_path.is_symlink() or response_path.stat().st_mode & 0o077:
                    raise ValueError('decisão deve ser arquivo privado sem symlink')
                if response_path.stat().st_size > 16000:
                    raise ValueError('decisão excede limite')
                response = agent.parse_json(response_path.read_text())
                if response.get('request_id') != request_id or response.get('operador') != 'Codex':
                    raise ValueError('decisão sem vínculo/origem Codex')
                return response
            time.sleep(0.25)
        raise ValueError('prazo de revisão expirado; nenhuma aprovação presumida')


def scope_guard(inv, expected_id):
    auth = authentication_guard()
    def check(action):
        if identity() != expected_id:
            raise ValueError('identidade do container mudou; interromper')
        agent.validate_proposal(action)
        tool, p = action['ferramenta'], action['parametros']
        if tool == 'http_post':
            if inv != 'INV-02':
                raise ValueError('POST restrito à INV-02')
            auth(action)
        elif tool == 'nmap':
            if inv != 'INV-01':
                raise ValueError('Nmap restrito à INV-01')
        else:
            allowed = {'INV-01': {'/', '/rest/admin/application-version', '/api/Products/1'},
                       'INV-02': {'/'},
                       'INV-03': {'/', '/ftp/', '/ftp/arquivo-inexistente-af.txt',
                                  '/ftp/legal.md', '/ftp/README.md'}}
            if p['path'] not in allowed[inv]:
                raise ValueError('rota não prevista nos limites delegados; interromper para revisão de escopo')
    return check


def result_guard(result):
    if result.get('error') or result.get('status') in (423, 429) or result.get('exit_code', 0) != 0:
        raise ValueError('erro de ferramenta ou bloqueio; interromper')
    body = result.get('body', '')
    if '[REDACTED]' in body or re.search(
            r'-----BEGIN .*PRIVATE KEY|eyJ[A-Za-z0-9_-]{20,}\.|"(?:token|secret|access_token)"\s*:\s*"[^"\[]+', body):
        raise ValueError('possível dado sensível; interromper sem enviar ao modelo')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('investigacao', choices=SCENARIOS)
    parser.add_argument('--autorizacao-nicholas', required=True,
                        help='referência à autorização explícita, sem alegar aprovação humana por ação')
    args = parser.parse_args()
    os.umask(0o077)
    inv, run_id = args.investigacao, uuid.uuid4().hex
    directory = ROOT / 'logs' / inv / run_id
    path = directory / 'sessao.jsonl'
    def emit(kind, **fields):
        agent.log(str(path), kind, run_id=run_id, investigation_id=inv, tipo_execucao='academica',
                  responsavel_academico='Nicholas', operador='Codex', modo='delegado', **fields)
    try:
        emit('autorizacao_delegacao', referencia=args.autorizacao_nicholas,
             origem='instrucao_explicita_usuario',
             professor='autorização relatada por Nicholas; não verificada independentemente',
             decisao_por_acao='Codex delegado, não humana')
        # Reutiliza registro real anterior sem reescrever sua aprovação ou simular nova entrada.
        prior_path = ROOT / 'logs/INV-01/f13a210f91d4440480f74eceb6b17862/sessao.jsonl'
        prior = load_events(prior_path)
        approval = next(e for e in prior if e['evento'] == 'aprovacao_plano')
        network = next(e for e in prior if e['evento'] == 'portao_rede')
        plan = (ROOT / 'plano_humano.md').read_bytes()
        sha = hashlib.sha256(plan).hexdigest()
        if sha != approval['plano_sha256']:
            raise ValueError('plano mudou desde aprovação real; interromper')
        emit('aprovacao_plano', plano_sha256=sha, referencia_event_id=approval['event_id'],
             referencia_run_id=approval['run_id'], origem='reuso_declaracao_humana_registrada',
             integrantes='Nicholas', data_aprovacao=approval['data_aprovacao'])
        private_write(directory / 'plano-aprovado.md', plan.decode())
        emit('portao_rede', referencia_event_id=network['event_id'], kali=network['kali'],
             wan=network['wan'], estado='evidencia_anterior_declarada_pelo_grupo',
             limite='bloqueio no caminho testado; não comprova isolamento absoluto; sem novo teste externo')
        before = identity()
        emit('preflight', container_id=before, **services(), alvo='127.0.0.1:3000',
             codigo_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
             codigo_sha256={name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                            for name in ('agent.py', 'scripts/af_delegated.py', 'scripts/af_session.py')})
        emit('restauracao_solicitada', container_anterior=before, origem='autorizacao_explicita_nicholas')
        restored = subprocess.run([str(ROOT / 'scripts/restore.sh')], input='RESTAURAR\n',
                                  text=True, capture_output=True, timeout=60, check=True)
        after = identity()
        if after == before:
            raise ValueError('restauração não comprovada')
        emit('restauracao', container_anterior=before, container_novo=after,
             estado='recriado', saida=restored.stdout)
        emit('pronto', container_id=after, **wait_ready(), **services())
        print(f'SESSAO {directory}', flush=True)
        objective = SCENARIOS[inv][1]
        if inv == 'INV-01':
            objective += (' H1 exige cruzamento de rede e HTTP e verificação da informação exposta. '
                          'Candidatos autorizados, sem ordem obrigatória: nmap TCP/3000, GET /, '
                          '/rest/admin/application-version, /api/Products/1. Evitar rotas especulativas.')
        if inv == 'INV-02':
            objective += (' Controles autorizados: email af_inexistente_01@kit11.invalid fixo; '
                          'password teste-invalido-01, vazio ou omitido, uma vez cada; '
                          'candidato /rest/user/login. Escolha dinamicamente a comparação.')
        if inv == 'INV-03':
            objective += (' Candidatos sem sequência obrigatória: GET /, /ftp/, '
                          '/ftp/arquivo-inexistente-af.txt. Um documento público não sensível é opcional '
                          'somente com nome obtido de evidência anterior. Não baixar arquivos privados.')
        agent.run_session(objective, '127.0.0.1', str(path), plan_confirmed=True,
                          investigation_id=inv, run_id=run_id, max_actions=6,
                          reviewer=ReviewChannel(directory), action_guard=scope_guard(inv, after),
                          result_guard=result_guard)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError, KeyboardInterrupt) as exc:
        emit('falha_preparacao_ou_sessao', estado='PENDENTE', erro=str(exc))
        return 1
    finally:
        print(f'EVIDENCIAS {directory}', flush=True)
        if path.exists():
            summarize(path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
