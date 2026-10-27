#!/usr/bin/env python3
"""Agente supervisionado: escopo limitado à instância local do Juice Shop."""
import argparse
import datetime
import http.client
import ipaddress
import json
import os
import socket
import subprocess
import sys
import urllib.error
import urllib.request

MAX_BODY = 16384
MAX_ACTIONS = 20
TIMEOUT = 8
MODEL = 'qwen3:4b-instruct'


def log(path, kind, **fields):
    entry = {'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'evento': kind, **fields}
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def local_ip(value):
    ip = ipaddress.ip_address(value)
    if ip.version != 4 or not (ip.is_private or ip.is_loopback) or ip.is_unspecified:
        raise ValueError('endereço deve ser IPv4 privado local')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((value, 0))
    return value


def validate_proposal(obj):
    if not isinstance(obj, dict) or set(obj) != {'hipotese', 'interpretacao', 'ferramenta', 'parametros'}:
        raise ValueError('JSON exige hipotese, interpretacao, ferramenta e parametros')
    if not all(isinstance(obj[k], str) and len(obj[k]) <= 2000 for k in ('hipotese', 'interpretacao', 'ferramenta')):
        raise ValueError('campos textuais inválidos')
    tool, p = obj['ferramenta'], obj['parametros']
    if tool not in ('nmap', 'http_get', 'http_post') or not isinstance(p, dict):
        raise ValueError('ferramenta ou parâmetros inválidos')
    expected = {'nmap': set(), 'http_get': {'path'}, 'http_post': {'path', 'body'}}[tool]
    if set(p) != expected:
        raise ValueError('parâmetros inválidos')
    if tool != 'nmap':
        path = p['path']
        if not isinstance(path, str) or not path.startswith('/') or path.startswith('//') or len(path) > 1024 or any(ord(c) < 32 or ord(c) > 126 for c in path) or '#' in path:
            raise ValueError('caminho HTTP inválido')
    if tool == 'http_post' and (not isinstance(p['body'], str) or len(p['body'].encode()) > 4096):
        raise ValueError('corpo POST inválido')
    return obj


def execute(action, host, port=3000):
    validate_proposal(action)
    tool, p = action['ferramenta'], action['parametros']
    try:
        if tool == 'nmap':
            result = subprocess.run(['nmap', '-sT', '-Pn', '-n', '-p', str(port), '--max-retries', '1', '--host-timeout', '8s', host], capture_output=True, timeout=TIMEOUT + 2, check=False)
            return {'exit_code': result.returncode, 'stdout': result.stdout[:MAX_BODY].decode('utf-8', 'replace'), 'stderr': result.stderr[:2048].decode('utf-8', 'replace')}
        conn = http.client.HTTPConnection(host, port, timeout=TIMEOUT)
        try:
            body = p.get('body') if tool == 'http_post' else None
            conn.request('POST' if body is not None else 'GET', p['path'], body=body, headers={'Content-Type': 'application/json', 'Connection': 'close'})
            response = conn.getresponse()
            data = response.read(MAX_BODY + 1)
            return {'status': response.status, 'headers': dict(response.getheaders()), 'body': data[:MAX_BODY].decode('utf-8', 'replace'), 'truncated': len(data) > MAX_BODY, 'redirect_followed': False}
        finally:
            conn.close()
    except (OSError, subprocess.TimeoutExpired, http.client.HTTPException) as exc:
        return {'error': str(exc)}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def model_call(objective, history):
    prompt = ('Você é um assistente supervisionado em laboratório local autorizado. Escolha uma única ferramenta conforme o objetivo e evidências; não suponha resultados. '
              'Responda SOMENTE JSON com chaves hipotese, interpretacao, ferramenta, parametros. '
              'Ferramentas: nmap com parametros {}; http_get com {"path":"/"}; http_post com {"path":"/", "body":"JSON em texto"}. '
              'Os caminhos são relativos ao Juice Shop; não há outras ferramentas. A interpretacao deve avaliar as evidências anteriores.\n'
              + json.dumps({'objetivo': objective, 'historico': history[-8:]}, ensure_ascii=False))
    request = urllib.request.Request('http://127.0.0.1:11434/api/generate', data=json.dumps({'model': MODEL, 'prompt': prompt, 'stream': False, 'format': 'json', 'think': False, 'options': {'num_predict': 800}}).encode(), headers={'Content-Type': 'application/json'})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    with opener.open(request, timeout=180) as response:
        result = json.loads(response.read(100000))
    return validate_proposal(json.loads(result['response']))


def review(proposal, input_fn=None):
    input_fn = input_fn or input
    while True:
        choice = input_fn('Aprovar [a], modificar [m], rejeitar [r], encerrar [e]: ').strip().lower()
        if choice == 'a':
            return 'aprovada', proposal
        if choice == 'r':
            return 'rejeitada', None
        if choice == 'e':
            return 'encerrada', None
        if choice == 'm':
            try:
                changed = validate_proposal(json.loads(input_fn('JSON completo da ação modificada: ')))
                print(json.dumps(changed, ensure_ascii=False, indent=2))
                if input_fn('Aprovar esta ação final? [s/N]: ').strip().lower() == 's':
                    return 'modificada_aprovada', changed
                return 'modificada_rejeitada', changed
            except (ValueError, json.JSONDecodeError) as exc:
                print('Modificação inválida:', exc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', required=True, help='IPv4 privado vinculado a este Ubuntu')
    parser.add_argument('--log', default='logs/investigacao.jsonl')
    args = parser.parse_args()
    try:
        host = local_ip(args.ip)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print('Antes de consultar o modelo, preencha e aprove plano_humano.md com o grupo.')
    if input('O plano humano desta investigação foi registrado e aprovado? [s/N]: ').strip().lower() != 's':
        return
    objective = input('Objetivo e hipótese inicial registrados no plano: ').strip()
    if not objective:
        return
    os.makedirs(os.path.dirname(os.path.abspath(args.log)), exist_ok=True)
    log(args.log, 'inicio', objetivo=objective, alvo=host, plano_humano_confirmado=True)
    history = []
    for _ in range(MAX_ACTIONS):
        try:
            proposal = model_call(objective, history)
        except (OSError, ValueError, KeyError, urllib.error.URLError) as exc:
            print('Falha no modelo:', exc)
            log(args.log, 'erro_modelo', erro=str(exc))
            break
        print(json.dumps(proposal, ensure_ascii=False, indent=2))
        log(args.log, 'proposta', proposta=proposal)
        decision, action = review(proposal)
        log(args.log, 'decisao_humana', decisao=decision, acao_final=action)
        if decision == 'encerrada':
            break
        if decision not in ('aprovada', 'modificada_aprovada'):
            history.append({'proposta': proposal, 'decisao': decision})
            continue
        result = execute(action, host)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        log(args.log, 'resultado', acao=action, resultado=result)
        history.append({'proposta': proposal, 'decisao': decision, 'acao': action, 'resultado': result})
    conclusion = input('Decisão final e conclusão humana (ou pendência): ')
    log(args.log, 'conclusao_humana', conclusao=conclusion)

if __name__ == '__main__':
    main()
