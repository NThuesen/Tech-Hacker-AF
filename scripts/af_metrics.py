#!/usr/bin/env python3
"""Exportação privada de contagens objetivas; nenhuma classificação semântica automática."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys

from af_summarize import audit, load_events, private_write


def ratio(n, d):
    return f'{n}/{d}' if d else 'N/A (0/0)'


def reviewed_ratio(path, field, accepted, positive, id_field):
    """Conta classificações já feitas e atribuídas; não avalia conteúdo."""
    if path is None:
        return 'N/A (sem avaliações)'
    with path.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    values, seen = [], set()
    for row in rows:
        value = (row.get(field) or '').strip()
        if not value:
            continue
        identifier = (row.get(id_field) or '').strip()
        if (not identifier or identifier in seen or value not in accepted or not (row.get('justificativa') or '').strip()
                or not (row.get('avaliador') or '').strip() or not (row.get('data') or '').strip()):
            raise ValueError('avaliação exige ID único, classe válida, justificativa, avaliador e data')
        seen.add(identifier)
        values.append(value)
    return ratio(sum(value in positive for value in values), len(values))


def integrity_issues(events):
    issues = list(audit(events))
    for kind, key in (('proposta', 'proposal_id'), ('execucao', 'execution_id'), ('resultado', 'result_id')):
        seen = set()
        for event in events:
            if event.get('evento') != kind:
                continue
            identifier = event.get(key)
            if not identifier or identifier in seen:
                issues.append(f'{kind}: identificador ausente ou duplicado')
            if identifier:
                seen.add(identifier)
    return issues


def measure(events):
    if not events:
        raise ValueError('sessão vazia')
    first = events[0]
    proposals = [e for e in events if e.get('evento') == 'proposta']
    requests = [e for e in events if e.get('evento') == 'solicitacao_modelo' and e.get('fase') == 'proposta']
    decisions = [e for e in events if e.get('evento') in ('decisao_humana', 'decisao_delegada')]
    executions = [e for e in events if e.get('evento') == 'execucao']
    results = [e for e in events if e.get('evento') == 'resultado']
    def safe_hash(value):
        return value if isinstance(value, str) and re.fullmatch(r'(?:sha256:)?[0-9a-f]{32,64}', value) else 'N/A'
    trials = {e.get('trial_type') for e in events if e.get('trial_type')}
    trial = next(iter(trials)) if len(trials) == 1 else None
    if any(e.get('fixture') or e.get('origem') in ('entrada_injetada_teste', 'fixture_de_teste') for e in events):
        trial = 'replay_fixture' if trial == 'replay_fixture' else 'fixture_de_teste'
    scenarios = {e.get('scenario', e.get('investigation_id')) for e in events
                 if e.get('scenario', e.get('investigation_id'))}
    scenario = next(iter(scenarios)) if len(scenarios) == 1 else ('MÚLTIPLOS' if scenarios else None)
    model_errors = sum(e.get('evento') == 'erro_modelo' for e in events)
    scope = [e.get('escopo_estatico') for e in proposals]
    scope_available = bool(proposals) and all(s in ('permitida', 'permitida_condicional', 'fora_escopo') for s in scope)
    envelopes = [e.get('envelope', {}) for e in events if e.get('evento') == 'envelope_replay_privado']
    def telemetry(key):
        return sum(e[key] for e in envelopes) if envelopes and all(isinstance(e, dict) and type(e.get(key)) is int for e in envelopes) else 'N/A'
    variants = [e.get('variant') for e in results if e.get('variant') in ('A', 'B', 'C')]
    return {
        'run_id': safe_hash(first['run_id']),
        'trial_type': trial if trial in ('real', 'live', 'replay_real_context', 'replay_fixture', 'fixture_de_teste') else 'NÃO INFORMADO',
        'scenario': scenario if scenario in ('INV-01', 'INV-02', 'INV-03', 'INV-01-B', 'INV-02-B', 'INV-03-B', 'MÚLTIPLOS') else 'NÃO INFORMADO',
        'model_digest': safe_hash(next((e.get('model_digest', e.get('digest_modelo')) for e in events
                                        if e.get('model_digest', e.get('digest_modelo'))), None)),
        'code_commit': safe_hash(next((e.get('code_commit', e.get('codigo_commit')) for e in events
                                       if e.get('code_commit', e.get('codigo_commit'))), None)),
        'json_validos_por_tentativa': ratio(len(proposals), len(requests)),
        'propostas': len(proposals), 'tentativas': len(requests),
        'tentativas_sem_desfecho_registrado': max(0, len(requests) - len(proposals) - model_errors),
        'escopo_aceito_por_propostas': ratio(scope.count('permitida'), len(proposals)) if scope_available else 'N/A (não avaliado em todas as propostas)',
        'escopo_condicional': scope.count('permitida_condicional') if scope_available else 'N/A',
        'decisoes_humanas': sum(e.get('evento') == 'decisao_humana' and e.get('origem') in ('entrada_terminal', 'entrada_terminal_humana') for e in decisions),
        'decisoes_delegadas': sum(e.get('evento') == 'decisao_delegada' for e in decisions),
        'decisoes_fixture': sum(e.get('origem') == 'entrada_injetada_teste' for e in decisions),
        'execucoes': len(executions), 'resultados': len(results),
        'interrupcoes': sum(e.get('evento') in ('interrompida', 'parada_seguranca', 'falha_preparacao_ou_sessao') for e in events),
        'lacunas_estruturais': len(integrity_issues(events)),
        'variantes_repetidas': len(variants) - len(set(variants)),
        'tokens_prompt': telemetry('prompt_eval_count'), 'tokens_gerados': telemetry('eval_count'),
        'duracao_ns': telemetry('total_duration'),
        'avaliacao_semantica': 'N/A (depende de avaliação registrada)',
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('events', type=Path, nargs='+')
    parser.add_argument('--output-dir', type=Path, required=True, help='diretório privado existente, 0700')
    parser.add_argument('--avaliacoes', type=Path, help='CSV privado com alegações avaliadas')
    parser.add_argument('--avaliacoes-pares', type=Path, help='CSV privado com pares avaliados')
    args = parser.parse_args(argv)
    if not args.output_dir.is_dir():
        parser.error('diretório privado deve existir')
    sessions = [load_events(path) for path in args.events]
    unsupported = reviewed_ratio(args.avaliacoes, 'classe', {'0', '1', '2', '3'}, {'2', '3'}, 'claim_id')
    pertinent = reviewed_ratio(args.avaliacoes_pares, 'resultado', {'pertinente', 'nao_pertinente'}, {'pertinente'}, 'case_id')
    rows = []
    for events in sessions:
        fixture_session = any(e.get('fixture') or e.get('origem') in ('entrada_injetada_teste', 'fixture_de_teste')
                              for e in events)
        groups = {(e.get('trial_type'), e.get('scenario', e.get('investigation_id'))) for e in events
                  if e.get('trial_type') and e.get('scenario', e.get('investigation_id'))}
        if not groups:
            rows.append(measure(events))
            continue
        for trial, scenario in sorted(groups):
            selected = [e for e in events if e.get('trial_type') == trial
                        and e.get('scenario', e.get('investigation_id')) == scenario]
            if fixture_session and selected:
                selected[0] = {**selected[0], 'fixture': True}
            rows.append(measure(selected))
    output_names = ('metricas.csv', 'metricas.md', 'avaliacao-alegacoes.csv', 'avaliacao-pares.csv', 'manifesto.json')
    if any((args.output_dir / name).exists() or (args.output_dir / name).is_symlink() for name in output_names):
        raise ValueError('saídas existentes serão preservadas; use diretório vazio')
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    private_write(args.output_dir / 'metricas.csv', out.getvalue())
    lines = ['# Métricas objetivas — revisão necessária', '',
             'Contagens de eventos; não classificam a correção técnica ou semântica.', '',
             '| Sessão | Tipo | Cenário | JSON válido/tentativas | Execuções | Resultados | Lacunas |',
             '|---|---|---|---|---:|---:|---:|']
    if any(row['trial_type'] in ('replay_fixture', 'fixture_de_teste') for row in rows):
        lines.insert(2, '**FIXTURE/NÃO REAL:** linhas assim rotuladas não são investigações reais.')
    for row in rows:
        def cell(key):
            return str(row[key]).replace('|', '&#124;').replace('\n', ' ')
        lines.append('| ' + ' | '.join(cell(k) for k in ('run_id', 'trial_type', 'scenario',
                     'json_validos_por_tentativa', 'execucoes', 'resultados', 'lacunas_estruturais')) + ' |')
    lines += ['', 'Avaliações fornecidas separadamente, agregadas sem atribuição automática a sessões:',
              f'- Alegações classes 2 ou 3 / alegações avaliadas: {unsupported}.',
              f'- Pares pertinentes / pares avaliados: {pertinent}.',
              'Classificação depende dos avaliadores; amostras pequenas não permitem inferência estatística.']
    private_write(args.output_dir / 'metricas.md', '\n'.join(lines) + '\n')
    claims = io.StringIO(newline='')
    claim_writer = csv.writer(claims)
    claim_writer.writerow(['claim_id', 'texto_redigido', 'result_id_ou_sem_evidencia', 'classe', 'justificativa', 'avaliador', 'data', 'desacordo'])
    for events in sessions:
        for event in events:
            if event.get('evento') == 'interpretacao':
                # Uma linha inicial por interpretação, para o revisor dividir em alegações e preencher.
                def identifier(value):
                    return value if isinstance(value, str) and re.fullmatch(r'[0-9a-f]{32}', value) else 'sem_evidencia'
                claim_writer.writerow([identifier(event.get('event_id')), '', identifier(event.get('result_id')), '', '', '', '', ''])
    private_write(args.output_dir / 'avaliacao-alegacoes.csv', claims.getvalue())
    private_write(args.output_dir / 'avaliacao-pares.csv', 'case_id,resultado,justificativa,avaliador,data\n')
    manifest = [{'arquivo': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in args.events]
    private_write(args.output_dir / 'manifesto.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('Métricas e formulário privados gerados; classificação semântica permanece pendente.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as exc:
        print('Métricas interrompidas:', str(exc), file=sys.stderr)
        sys.exit(1)
