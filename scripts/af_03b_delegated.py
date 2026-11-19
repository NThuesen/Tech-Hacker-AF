#!/usr/bin/env python3
"""03B delegado: Codex revisa cada proposta; não representa decisão humana por ação."""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from af_03b_controls import ScenarioGuard, factual_context
from af_delegated import ReviewChannel
from af_refine import PLAN_OLD, PLAN_V2, safe_result, sha
from af_session import ROOT, SCENARIOS, identity, services, wait_ready
from af_summarize import load_events, private_write
import agent

PRIOR = ROOT / 'logs/03B/INV-01/f0e74216eeba4a3780b1eb41c48695ca/sessao.jsonl'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenario', choices=('INV-02-B', 'INV-03-B'))
    parser.add_argument('--autorizacao', required=True, help='referência à autorização real de delegação e restauração')
    args = parser.parse_args(argv)
    if not args.autorizacao.strip():
        parser.error('referência de autorização vazia')
    os.umask(0o077)
    inv = args.scenario[:-2]
    run_id = uuid.uuid4().hex
    directory = ROOT / 'logs/03B' / inv / run_id
    path = directory / 'sessao.jsonl'
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in (PLAN_OLD, PLAN_V2, ROOT / 'plano_humano.md',
              ROOT / 'agent.py', ROOT / 'scripts/af_03b_controls.py', ROOT / 'scripts/af_03b_delegated.py')}
    meta = {'phase': '03B_delegado', 'scenario': args.scenario, 'trial_type': 'real',
            'plan_v2_sha256': hashes[str(PLAN_V2.relative_to(ROOT))], 'code_commit': commit,
            'origem_decisao': 'codex_delegado', 'responsavel_academico': 'Nicholas',
            'operador': 'Codex', 'modo': 'delegado'}
    def emit(kind, **fields):
        agent.log(str(path), kind, run_id=run_id, investigation_id=inv, tipo_execucao='academica', **meta, **fields)
    try:
        prior = load_events(PRIOR)
        approval = next(e for e in prior if e['evento'] == 'aprovacao_plano_03b')
        original = next(e for e in prior if e['evento'] == 'aprovacao_plano')
        network = next(e for e in prior if e['evento'] == 'portao_rede')
        if (approval.get('plan_v2_sha256') != hashes[str(PLAN_V2.relative_to(ROOT))]
                or approval.get('plan_original_sha256') != hashes[str(PLAN_OLD.relative_to(ROOT))]
                or original.get('plano_sha256') != hashes['plano_humano.md']
                or network.get('estado') != 'declarado_pelo_grupo'):
            raise ValueError('aprovação ou rede anterior não corresponde; sessão cancelada')
        emit('autorizacao_delegacao', referencia=args.autorizacao, origem='instrucao_usuario',
             limitacao='decisões e conclusões do Codex não são decisões humanas por ação')
        emit('aprovacoes_referenciadas', plano_03b_event_id=approval['event_id'],
             plano_original_event_id=original['event_id'], rede_event_id=network['event_id'],
             referencia_run_id=prior[0]['run_id'])
        emit('codigo_em_uso', sha256=hashes)
        private_write(directory / 'plano-03b-v2-aprovado.md', PLAN_V2.read_text(encoding='utf-8'))
        before = identity()
        details = services()
        digest = details.get('digest_modelo')
        if not digest:
            raise ValueError('digest do modelo ausente')
        emit('preflight', container_id=before, **details)
        emit('restauracao_solicitada', container_anterior=before, origem='autorizacao_explicita_usuario')
        subprocess.run([str(ROOT / 'scripts/restore.sh')], input='RESTAURAR\n', text=True,
                       capture_output=True, timeout=90, check=True, cwd=ROOT)
        after = identity()
        if before == after:
            raise ValueError('restauração não comprovada')
        emit('restauracao', container_anterior=before, container_novo=after,
             origem='autorizacao_explicita_usuario')
        emit('pronto', container_id=after, **wait_ready(), **services())
        meta['model_digest'] = digest
        channel = ReviewChannel(directory)
        guard = ScenarioGuard(args.scenario)
        def check(action):
            if any(sha(ROOT / name) != value for name, value in hashes.items()):
                raise ValueError('plano ou código alterado')
            if identity() != after or services().get('digest_modelo') != digest:
                raise ValueError('identidade do container ou modelo alterada')
            return guard.check(action)
        def observe(action, result):
            verified = False
            if (args.scenario == 'INV-03-B' and action['ferramenta'] == 'http_get'
                    and action['parametros']['path'] == '/ftp/' and result.get('status') == 200
                    and result.get('truncated') is False):
                response = channel('validar_listagem', {'acao': action, 'resultado': result})
                verified = response.get('decisao') == 'listagem_completa'
                if not isinstance(response.get('justificativa'), str) or not response['justificativa'].strip():
                    raise ValueError('revisão delegada da listagem exige justificativa')
                emit('revisao_listagem_delegada', confirmada=verified, justificativa=response['justificativa'],
                     request_id=response['request_id'], origem='codex_delegado')
            guard.observe(action, result, listing_verified=verified)
        objective = SCENARIOS[inv][1]
        if inv == 'INV-02':
            objective += (' POST /rest/user/login com email af_inexistente_01@kit11.invalid e '
                          'password teste-invalido-01, vazio ou omitido, uma vez por variante; escolha sem roteiro fixo.')
        else:
            objective += (' Candidatos GET /, /ftp/, /ftp/arquivo-inexistente-af.txt e '
                          '/ftp/arquivo-inexistente-af.md; este último depende de listagem completa e ausência do nome. '
                          'Documentos /ftp/legal.md ou /ftp/README.md apenas se listados e aprovados; sem sequência fixa.')
        # Não usar phase=03B: esse identificador é reservado ao modo humano sem injeção.
        session_meta = {k: v for k, v in meta.items() if k not in ('responsavel_academico', 'operador', 'modo')}
        agent.run_session(objective, '127.0.0.1', str(path), plan_confirmed=True,
                          investigation_id=inv, run_id=run_id, max_actions=6, reviewer=channel,
                          action_guard=check, result_guard=safe_result, result_observer=observe,
                          context_provider=factual_context, session_metadata=session_meta)
        return 0
    except (OSError, ValueError, KeyError, StopIteration, subprocess.SubprocessError, KeyboardInterrupt) as exc:
        emit('falha_preparacao_ou_sessao', estado='PENDENTE', erro=str(exc))
        print('Interrompido:', str(exc), file=sys.stderr)
        return 1
    finally:
        print(f'EVIDENCIAS {directory}', flush=True)


if __name__ == '__main__':
    sys.exit(main())
