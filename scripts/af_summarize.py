#!/usr/bin/env python3
"""Síntese determinística privada de JSONL; não consulta LLM nem conclui hipóteses."""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import stat
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import agent

INVESTIGATIONS = {'INV-01', 'INV-02', 'INV-03'}


def plan_candidates(path, inv, events):
    snapshot = path.with_name('plano-aprovado.md')
    if not snapshot.is_file():
        return set(), 'Snapshot do plano ausente; comparação com planejamento indisponível.'
    raw = snapshot.read_bytes()
    approvals = [e for e in events if e['evento'] == 'aprovacao_plano']
    if not approvals or approvals[-1].get('plano_sha256') != hashlib.sha256(raw).hexdigest():
        return set(), 'Hash do snapshot sem aprovação correspondente; comparação indisponível.'
    # Extrair somente a seção deste cenário do snapshot aprovado, não do plano atual.
    section = next((s for s in raw.decode('utf-8').split('\n## ') if inv in s.split('\n', 1)[0]), '')
    candidates = set(re.findall(r'\*\*(/[A-Za-z0-9_./-]*)\*\*', section))
    if 'nmap' in section.lower():
        candidates.add('nmap')
    return candidates, ('Candidatos extraídos da seção do cenário no snapshot aprovado. '
                        'Rotas sem destaque Markdown e mudanças de formato exigem comparação manual.')


def cell(value):
    if not isinstance(value, str):
        value = json.dumps(agent.redact(value), ensure_ascii=False)
    return html.escape(value).replace('|', '&#124;').replace('`', '&#96;').replace('\n', ' ')


def load_events(path):
    events = []
    ids = set()
    with Path(path).open(encoding='utf-8') as stream:
        for number, line in enumerate(stream, 1):
            item = agent.parse_json(line)
            if not isinstance(item, dict) or not all(item.get(k) for k in ('event_id', 'evento', 'run_id')):
                raise ValueError(f'evento incompleto na linha {number}')
            if item['event_id'] in ids:
                raise ValueError('event_id duplicado')
            ids.add(item['event_id'])
            events.append(item)
    if not events or len({e['run_id'] for e in events}) != 1:
        raise ValueError('exige exatamente uma sessão por arquivo')
    return events


def audit(events):
    """Checagem estrutural, sem transformar declaração humana em prova externa."""
    issues = []
    proposals, approvals, results, interpretations = {}, {}, {}, set()
    executions, modifications, confirmations = {}, {}, {}
    for e in events:
        kind, pid = e['evento'], e.get('proposal_id')
        if kind == 'proposta':
            proposals[pid] = e
        elif kind == 'modificacao_validada':
            modifications[pid] = e.get('acao_modificada')
        elif kind == 'confirmacao_modificacao_delegada':
            confirmations[pid] = e.get('acao_final')
        elif kind in ('decisao_humana', 'decisao_delegada'):
            if pid not in proposals:
                issues.append('decisão sem proposta anterior: ' + e['event_id'])
            if kind == 'decisao_delegada':
                if e.get('origem') != 'codex_delegado' or not e.get('justificativa'):
                    issues.append('decisão delegada sem origem/justificativa: ' + e['event_id'])
                if e.get('decisao') == 'modificada_aprovada' and (
                        modifications.get(pid) != e.get('acao_final')
                        or confirmations.get(pid) != e.get('acao_final')):
                    issues.append('modificação delegada sem validação/segunda aprovação: ' + e['event_id'])
            if e.get('decisao') in ('aprovada', 'modificada_aprovada'):
                approvals[pid] = e
        elif kind == 'execucao':
            approval = approvals.get(pid)
            if not approval or approval.get('acao_final') != e.get('acao'):
                issues.append('execução sem autorização correspondente: ' + e['event_id'])
            executions[e.get('execution_id')] = e
        elif kind == 'resultado':
            execution = executions.get(e.get('execution_id'))
            if not execution or any(execution.get(k) != e.get(k) for k in ('proposal_id', 'result_id', 'acao')):
                issues.append('resultado sem execução correspondente: ' + e['event_id'])
            results[e.get('result_id')] = e
        elif kind == 'interpretacao':
            rid = e.get('result_id')
            if rid not in results or e.get('interpretacao', {}).get('resultado_id') != rid:
                issues.append('interpretação sem resultado correspondente: ' + e['event_id'])
            interpretations.add(rid)
    for rid in results.keys() - interpretations:
        issues.append('resultado sem interpretação: ' + str(rid))
    return issues


def is_fixture(events):
    return any(e.get('fixture') or e.get('origem') == 'entrada_injetada_teste'
               or e.get('tipo_execucao') != 'academica' for e in events)


def private_write(path, content):
    # Mesmo validador de proprietário/permissões/links dos logs; arquivo de saída não publica dados.
    parent = path.parent
    current = path.absolute()
    while current != current.parent:
        if current.is_symlink():
            raise ValueError('saída não pode usar links simbólicos')
        current = current.parent
    info = parent.stat()
    if info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError('diretório de saída deve ser privado (0700)')
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise ValueError('saída exige arquivo regular privado 0600 sem hardlinks')
        stream.truncate(0)
        stream.write(content)


def summarize(path):
    path = Path(path)
    events = load_events(path)
    inv = events[0].get('investigation_id', 'NÃO IDENTIFICADA')
    issues = audit(events)
    fixture = is_fixture(events)
    candidates, plan_note = plan_candidates(path, inv, events)
    rows = [f'# {cell(inv)} — resumo técnico privado', '',
            '**FIXTURE/MOCK — não é evidência acadêmica.**' if fixture else
            '**Registro de sessão; exige revisão humana e dos logs primários.**', '',
            f'run_id: {cell(events[0]["run_id"])}. Origem: {cell(path.name)}.', '',
            'Hipótese e controles: consultar plano-aprovado.md preservado nesta pasta e sua aprovação por hash no JSONL. '
            'A hipótese permanece PENDENTE de análise/conclusão do grupo. ' + plan_note, '',
            '## Planejamento × propostas efetivas', '',
            'Correspondência indica apenas ferramenta/rota candidata do plano; não valida corpo, hipótese, '
            'adequação nem obriga sequência. Arquivo adicional da INV-03 requer nome oriundo de evidência real.', '',
            '| proposal_id / evento | Proposta Qwen e parâmetros | Relação com candidatos do plano |',
            '|---|---|---|']
    for e in events:
        if e['evento'] == 'proposta':
            p = e['proposta']
            key = 'nmap' if p['ferramenta'] == 'nmap' else p['parametros'].get('path')
            match = ('candidato previsto; revisar conteúdo' if key in candidates else
                     'revisão humana de desvio/justificativa necessária' if candidates else
                     'comparação indisponível; revisar plano/aprovação')
            rows.append(f'| {cell(e.get("proposal_id"))} / {cell(e["event_id"])} | {cell(p)} | {match} |')
    rows += ['', '## Evidências, intervenções e interpretações', '',
             'Resultado técnico é distinto de inferência do Qwen e conclusão humana. '
             'Corpos HTTP e saídas Nmap completos e limitados estão no JSONL privado.', '',
             '| Evento / ID | Conteúdo registrado (origem preservada) |', '|---|---|']
    relevant = {'aprovacao_plano', 'portao_rede', 'preflight', 'restauracao', 'pronto',
                'decisao_humana', 'decisao_delegada', 'conclusao_delegada', 'autorizacao_delegacao',
                'confirmacao_modificacao_delegada', 'modificacao_validada', 'modificacao_invalida', 'resultado',
                'interpretacao', 'decisao_pos_interpretacao', 'conclusao_humana',
                'erro_modelo', 'erro_interpretacao', 'interrompida',
                'acao_bloqueada', 'parada_seguranca',
                'falha_preparacao_ou_sessao', 'preparacao_interrompida'}
    for e in events:
        if e['evento'] not in relevant:
            continue
        content = {k: v for k, v in e.items() if k not in
                   ('timestamp', 'event_id', 'run_id', 'investigation_id', 'tipo_execucao', 'evento')}
        if e['evento'] == 'resultado':
            result = content.get('resultado', {})
            content['resultado'] = {k: v for k, v in result.items() if k not in ('body', 'stdout', 'stderr')}
            content['evidencia_primaria'] = 'corpo/saída no JSONL por result_id; revisar antes de citar'
        rows.append(f'| {cell(e["evento"])} / {cell(e["event_id"])} | {cell(content)} |')
    rows += ['', '## Limitações e conclusão', '',
             'Erros técnicos efetivamente registrados: ' + str(sum(e['evento'] in ('erro_modelo', 'erro_interpretacao') for e in events)) + '.',
             'Inferências incorretas: classificação depende da avaliação humana registrada após interpretação; '
             'não deduzir erro, adaptação útil, vulnerabilidade ou ausência de falhas automaticamente.',
             'Conclusão: consultar conclusao_humana ou conclusao_delegada acima; se ausente, PENDENTE. Decisão Codex não é decisão humana. '
             'A sequência de propostas/intervenções e os resultados permitem ao grupo comparar decisões sucessivas; '
             'causalidade e correção exigem análise humana.', '',
             'Integridade estrutural: ' + ('; '.join(map(cell, issues)) if issues else 'sem lacunas detectadas nos vínculos checados; não atesta autenticidade.'), '',
             '## Matriz de rastreabilidade', '',
             '| Linha JSONL | event_id | Evento / timestamp | proposal_id | execution_id | result_id |', '|---|---|---|---|---|---|']
    for line, e in enumerate(events, 1):
        rows.append('| ' + ' | '.join(cell(v) for v in (line, e['event_id'], e['evento'] + ' / ' + e.get('timestamp', ''), e.get('proposal_id', ''), e.get('execution_id', ''), e.get('result_id', ''))) + ' |')
    rows += ['', 'Para relatório de 4–6 páginas: selecionar fatos sustentados por result_id, separar interpretação '
             'e avaliação humana; usar este resumo como material privado. Para vídeo até 10 minutos: selecionar '
             'uma investigação completa com plano, proposta, decisão real, resultado, interpretação e conclusão. '
             'Capturas, segredos e texto livre exigem revisão antes de compartilhar.', '']
    output = path.with_name('resumo.md')
    private_write(output, '\n'.join(rows))
    return output


def update_status(path):
    events = load_events(path)
    if is_fixture(events):
        raise ValueError('fixtures/engenharia não podem atualizar estado acadêmico')
    inv = events[0].get('investigation_id')
    if inv not in INVESTIGATIONS:
        raise ValueError('investigação não identificada')
    # Nunca promover a CONCLUÍDO automaticamente. Sem conclusões privadas na documentação pública.
    counts = {kind: sum(e['evento'] == kind for e in events)
              for kind in ('proposta', 'resultado', 'conclusao_humana')}
    note = (f'Preparação/execução {inv}, run_id `{events[0]["run_id"]}`: '
            f'{counts["proposta"]} propostas, {counts["resultado"]} resultados, '
            f'{counts["conclusao_humana"]} conclusões registradas. '
            f'Lacunas estruturais: {len(audit(events))}. '
            'PENDENTE de revisão do grupo; contagem não comprova conclusão, isolamento WAN ou correção da IA. '
            'Evidências e resumo no diretório privado logs/' + inv + '/' + events[0]['run_id'] + '/.')
    for target in ('CHECKLIST_RUBRICA.md', 'docs/STATE.md'):
        file = ROOT / target
        start, end = f'<!-- AF-AUTO-{inv} -->', f'<!-- /AF-AUTO-{inv} -->'
        content = file.read_text()
        block = start + '\n' + note + '\n' + end
        if start in content and end in content:
            a, b = content.index(start), content.index(end) + len(end)
            content = content[:a] + block + content[b:]
        else:
            content += '\n\n' + block + '\n'
        file.write_text(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('jsonl', type=Path)
    parser.add_argument('--update-status', action='store_true', help='atualiza contagens, sempre PENDENTE de revisão')
    args = parser.parse_args()
    os.umask(0o077)
    try:
        print(summarize(args.jsonl))
        if args.update_status:
            update_status(args.jsonl)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, 'Síntese interrompida: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
