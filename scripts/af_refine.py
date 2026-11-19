#!/usr/bin/env python3
"""Sessão 03B v2 supervisionada; exige terminal e validações reais de preflight."""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import uuid

from af_session import ROOT, SCENARIOS, command, confirm, identity, prepare, required, services
from af_summarize import private_write
from af_03b_controls import ScenarioGuard, factual_context, original_context
from af_delegated import result_guard as legacy_result_guard
import agent

PLAN_OLD = ROOT / 'docs/PLANO_REFINAMENTO_BLOCO03B.md'
PLAN_V2 = ROOT / 'docs/PLANO_03B_EXCELENCIA_V2.md'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_result(result):
    legacy_result_guard(result)
    if isinstance(result.get('status'), int) and 300 <= result['status'] < 400:
        raise ValueError('redirecionamento não seguido; interromper para revisão')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenario', choices=sorted(('INV-01-B', 'INV-02-B', 'INV-03-B')))
    parser.add_argument('--context-mode', choices=('A', 'B'), default='A')
    args = parser.parse_args(argv)
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        parser.error('sessão ao vivo exige terminal humano; nenhuma ferramenta executada')
    os.umask(0o077)
    inv = args.scenario[:-2]
    run_id = uuid.uuid4().hex
    directory = ROOT / 'logs' / '03B' / inv / run_id
    path = directory / 'sessao.jsonl'
    old_sha, plan_sha = sha(PLAN_OLD), sha(PLAN_V2)
    code_commit = command(['git', 'rev-parse', 'HEAD'])
    code_sha = {name: sha(ROOT / name) for name in
                ('agent.py', 'scripts/af_refine.py', 'scripts/af_03b_controls.py',
                 'scripts/af_session.py', 'scripts/af_delegated.py', 'scripts/af_summarize.py',
                 'scripts/lab_common.sh', 'scripts/restore.sh')}
    meta = {'phase': '03B', 'scenario': args.scenario, 'trial_type': 'real',
            'plan_original_sha256': old_sha, 'plan_v2_sha256': plan_sha,
            'code_commit': code_commit, 'context_mode': args.context_mode,
            'origem_decisao': 'entrada_terminal_humana'}
    def emit(kind, **fields):
        agent.log(str(path), kind, run_id=run_id, investigation_id=inv,
                  tipo_execucao='academica', **meta, **fields)
    try:
        emit('preparacao', estado='PENDENTE')
        supervisor = required('Nome e sobrenome do integrante que supervisionará esta sessão no terminal: ')
        if len(supervisor) > 200:
            raise ValueError('nome do supervisor excede limite')
        confirm('O integrante identificado está presente e assume as decisões? Digite ASSUMO: ', 'ASSUMO')
        meta['supervisor'] = supervisor
        emit('supervisor_identificado', origem='entrada_terminal_humana', identidade='autodeclarada')
        print(f'Plano anterior SHA256={old_sha}; plano v2 SHA256={plan_sha}; commit={code_commit}')
        people = required('Integrantes responsáveis pela aprovação desta versão: ')
        date = required('Data e referência verdadeira da decisão: ')
        reason = required('Justificativa/condições da decisão: ')
        confirm('Para confirmar o plano exibido, digite APROVAR 03B: ', 'APROVAR 03B')
        emit('aprovacao_plano_03b', integrantes=people, data_aprovacao=date,
             justificativa=reason, origem='entrada_terminal_humana')
        private_write(directory / 'plano-03b-v2-aprovado.md', PLAN_V2.read_text(encoding='utf-8'))
        private_write(directory / 'plano-03b-anterior.md', PLAN_OLD.read_text(encoding='utf-8'))
        def check_plans():
            if sha(PLAN_OLD) != old_sha or sha(PLAN_V2) != plan_sha:
                raise ValueError('plano alterado depois da aprovação')
            if any(sha(ROOT / name) != digest for name, digest in code_sha.items()):
                raise ValueError('código alterado depois do preflight')
        check_plans()
        emit('codigo_em_uso', sha256=code_sha, observacao='hashes incluem código não commitado')
        model_before_restore = {}
        def before_restore():
            check_plans()
            model_before_restore.update(services())
            if not isinstance(model_before_restore.get('digest_modelo'), str) or not model_before_restore['digest_modelo']:
                raise ValueError('digest do modelo ausente antes da restauração')
        # O fluxo existente exige aprovação do plano histórico, evidências Kali/WAN,
        # identidade Rootless, confirmação separada de restauração e readiness.
        prepare(inv, emit, directory, pre_restore_guard=before_restore)
        expected_id = identity()
        details = services()
        digest = details.get('digest_modelo')
        if not isinstance(digest, str) or not digest or digest != model_before_restore.get('digest_modelo'):
            raise ValueError('digest do modelo ausente ou alterado no preflight')
        meta['model_digest'] = digest
        emit('identidade_03b', container_id=expected_id, **details)
        guard = ScenarioGuard(args.scenario)
        def check(action):
            check_plans()
            if identity() != expected_id:
                raise ValueError('identidade do container mudou')
            if services().get('digest_modelo') != digest:
                raise ValueError('digest do modelo mudou; sessão interrompida')
            return guard.check(action)
        def observe(action, result):
            verified = False
            if (args.scenario == 'INV-03-B' and action['ferramenta'] == 'http_get'
                    and action['parametros']['path'] == '/ftp/'
                    and result.get('status') == 200 and result.get('truncated') is False):
                verified = input('Listagem completa e legível, nomes conferidos (inclusive ausência do candidato .md)? [s/N]: ').strip().lower() == 's'
                emit('revisao_listagem', confirmada=verified, origem='entrada_terminal_humana')
            guard.observe(action, result, listing_verified=verified)
        known = {'INV-01': ['nmap TCP/3000', '/', '/rest/admin/application-version', '/api/Products/1'],
                 'INV-02': ['/rest/user/login A/B/C'],
                 'INV-03': ['/', '/ftp/', '/ftp/arquivo-inexistente-af.txt', '/ftp/arquivo-inexistente-af.md',
                            '/ftp/legal.md ou /ftp/README.md condicionados']}
        emit('candidatos_conhecidos', known_candidates=known[inv], discovered_by_model=[])
        objective = SCENARIOS[inv][1] + ' Candidatos autorizados, sem ordem obrigatória: ' + ', '.join(known[inv]) + '.'
        if inv == 'INV-02':
            objective += (' No único POST permitido, use email af_inexistente_01@kit11.invalid e '
                          'password teste-invalido-01, vazio ou omitido; cada variante no máximo uma vez.')
        agent.run_session(objective, '127.0.0.1', str(path), plan_confirmed=True,
                          investigation_id=inv, run_id=run_id, max_actions=6,
                          action_guard=check, result_guard=safe_result, result_observer=observe,
                          session_metadata=meta,
                          context_provider=factual_context if args.context_mode == 'B' else original_context)
        print(f'Evidências privadas: {directory}')
        return 0
    except (OSError, ValueError, subprocess.SubprocessError, KeyboardInterrupt, EOFError) as exc:
        emit('falha_preparacao_ou_sessao', estado='PENDENTE', erro=str(exc))
        print('Sessão interrompida:', str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
