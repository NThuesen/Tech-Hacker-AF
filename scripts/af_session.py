#!/usr/bin/env python3
"""Preparação mecânica do Bloco 03; decisões somente pelo terminal humano."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
import uuid
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import agent
from af_summarize import private_write, summarize, update_status

SCENARIOS = {
    'INV-01': ('H1', 'Identificar o serviço e as informações efetivamente expostas pelo Juice Shop; '
               'cruzar evidências de rede e HTTP sem inferir aplicação por porta aberta ou vulnerabilidade por versão pública.'),
    'INV-02': ('H2', 'Comparar respostas de autenticação a entradas inválidas controladas, variando um campo; '
               'sem força bruta, SQL injection ou credenciais reais; diferenças não comprovam bypass nem enumeração.'),
    'INV-03': ('H3', 'Comparar recursos HTTP públicos acessíveis e inexistentes e seus controles de acesso; '
               'não presumir listagem, acesso indevido, LFI ou RFI a partir de status isolado.'),
}


def authentication_guard():
    """Controles A/B/C do plano; uma execução por variante, sem credenciais reais."""
    seen = set()
    def check(action):
        if action['ferramenta'] != 'http_post':
            return
        params = action['parametros']
        body = agent.parse_json(params['body'])
        if (params['path'] != '/rest/user/login'
                or set(body) not in ({'email', 'password'}, {'email'})
                or body.get('email') != 'af_inexistente_01@kit11.invalid'
                or ('password' in body and body['password'] not in ('', 'teste-invalido-01'))):
            raise ValueError('INV-02 permite somente controles inválidos A/B/C do plano; revisar novo escopo com o grupo')
        variant = 'omitida' if 'password' not in body else ('vazia' if body['password'] == '' else 'invalida')
        if variant in seen:
            raise ValueError('variante de autenticação já executada; repetição bloqueada')
        seen.add(variant)
    return check


def command(args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                          timeout=20, check=True,
                          env={**os.environ, 'DOCKER_CONTEXT': ''}).stdout.strip()


def identity():
    # Reutiliza integralmente os validadores de identidade e bindings existentes.
    script = '. ./scripts/lab_common.sh\nlab_preflight\nlab_container_id'
    container_id = command(['sh', '-eu', '-c', script])
    running = command(['docker', '--host', f'unix:///run/user/{os.getuid()}/docker.sock',
                       'container', 'inspect', '--format', '{{.State.Running}}', container_id])
    if running != 'true':
        raise ValueError('container autorizado não está em execução')
    return container_id


def get_local(url):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), agent.NoRedirect())
    with agent.http_deadline(), opener.open(url, timeout=agent.TIMEOUT) as response:
        data = response.read(agent.MAX_MODEL_BYTES + 1)
        if len(data) > agent.MAX_MODEL_BYTES:
            raise ValueError('resposta de preflight excede limite')
        return response.status, data


def services():
    if not shutil.which('nmap'):
        raise ValueError('Nmap indisponível; nenhuma instalação automática')
    status, raw = get_local('http://127.0.0.1:11434/api/tags')
    tags = agent.parse_json(raw)
    model = next((m for m in tags['models'] if m.get('name') == agent.MODEL), None)
    if status != 200 or model is None:
        raise ValueError('Qwen local exigido não encontrado')
    return {'modelo': agent.MODEL, 'digest_modelo': model.get('digest'),
            'nmap': command(['nmap', '--version']).splitlines()[0]}


def wait_ready(timeout=60):
    deadline = time.monotonic() + timeout
    while True:
        try:
            status, body = get_local('http://127.0.0.1:3000/')
            if status == 200:
                return {'status': status, 'body_sha256': hashlib.sha256(body).hexdigest(),
                        'observacao': 'GET / de disponibilidade; não é descoberta nem prova de isolamento WAN'}
        except (OSError, ValueError):
            pass
        if time.monotonic() >= deadline:
            raise ValueError('Juice Shop não respondeu HTTP 200 no prazo')
        time.sleep(1)


def required(prompt):
    return agent.human_text(prompt, input)


def confirm(prompt, token):
    if input(prompt).strip() != token:
        raise ValueError('confirmação ausente; sessão encerrada sem aceite presumido')


def prepare(inv, emit, directory):
    plan = (ROOT / 'plano_humano.md').read_bytes()
    sha = hashlib.sha256(plan).hexdigest()
    commit = command(['git', 'rev-parse', 'HEAD'])
    print(f'{inv}: plano_humano.md SHA256={sha}; código={commit}')
    print('A aprovação deve ser deliberada pelo grupo antes da primeira consulta ao Qwen. '
          'Confirmar autoria/uso de LLM com o professor conforme o plano; não reconstituir uma autoria fictícia.')
    people = required('Integrantes presentes que aprovaram o plano: ')
    approved_at = required('Data/hora real da aprovação e referência da deliberação: ')
    reason = required('Justificativa da aprovação/alterações deliberadas: ')
    confirm(f'Para confirmar a aprovação real desta versão, digite APROVAR {inv}: ', f'APROVAR {inv}')
    emit('aprovacao_plano', integrantes=people, data_aprovacao=approved_at,
         justificativa=reason, plano_sha256=sha, codigo_commit=commit,
         origem='entrada_terminal')
    private_write(directory / 'plano-aprovado.md', plan.decode('utf-8'))
    # Evidência externa deve ser obtida pelo grupo; o Ubuntu não comprova o caminho Kali/WAN.
    kali = required('Referência da evidência atual Kali/OpenVPN → 10.0.80.3:3001 (ou PENDENTE): ')
    wan = required('Referência da comprovação de isolamento WAN (ou PENDENTE): ')
    if any(v.upper().startswith(('PENDENTE', 'NÃO VERIFICADO', 'NAO VERIFICADO')) for v in (kali, wan)):
        emit('portao_rede', kali=kali, wan=wan, estado='PENDENTE', origem='entrada_terminal')
        raise ValueError('acesso Kali e isolamento WAN exigem evidência antes da investigação')
    confirm('O grupo verificou essas evidências atuais? Digite REDE VERIFICADA: ', 'REDE VERIFICADA')
    emit('portao_rede', kali=kali, wan=wan, estado='declarado_pelo_grupo', origem='entrada_terminal')
    before = identity()
    emit('preflight', container_id=before, **services(), host=socket.gethostname(),
         alvo='127.0.0.1:3000', bindings=['127.0.0.1:3000', '10.0.80.3:3001'],
         imagem_validada=command(['sh', '-eu', '-c',
             '. ./scripts/lab_common.sh\nprintf "%s %s\\n" "$LAB_IMAGE" "$LAB_IMAGE_ID"']))
    print('Estado inicial conhecido exige restauração. Cancelar preserva o container e encerra a preparação.')
    confirm('Oferecer restauração supervisionada agora? Digite OFERECER ou Enter para cancelar: ', 'OFERECER')
    emit('restauracao_solicitada', container_anterior=before, origem='entrada_terminal')
    # restore.sh pede RESTAURAR, reinspeciona e remove pelo ID validado, mantendo bindings.
    subprocess.run([str(ROOT / 'scripts/restore.sh')], cwd=ROOT, check=True)
    after = identity()
    if after == before:
        raise ValueError('restauração não comprovada: ID do container não mudou')
    emit('restauracao', container_anterior=before, container_novo=after,
         estado='recriado', origem='restore.sh_com_confirmacao_terminal')
    emit('pronto', container_id=after, **wait_ready(), **services())
    if identity() != after:
        raise ValueError('container mudou durante o preflight')
    if hashlib.sha256((ROOT / 'plano_humano.md').read_bytes()).hexdigest() != sha:
        raise ValueError('plano mudou após aprovação; iniciar nova preparação')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('investigacao', choices=SCENARIOS)
    args = parser.parse_args()
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        parser.error('exige terminal interativo real; pipes/entradas redirecionadas não são aceitos')
    os.umask(0o077)
    run_id = uuid.uuid4().hex
    directory = ROOT / 'logs' / args.investigacao / run_id
    path = directory / 'sessao.jsonl'
    def emit(kind, **fields):
        agent.log(str(path), kind, run_id=run_id, investigation_id=args.investigacao,
                  tipo_execucao='academica', **fields)
    try:
        emit('preparacao', hipotese=SCENARIOS[args.investigacao][0], estado='PENDENTE')
        prepare(args.investigacao, emit, directory)
        print('Até 6 propostas; cada ferramenta exige aprovação e justificativa. '
              'Parar diante de 429/bloqueio, dados sensíveis ou ausência de informação nova. '
              'INV-02: no máximo uma execução por variante; revisar cada POST. '
              'Na justificativa após interpretação, registrar avaliação correta/parcial/incorreta/inconclusiva, '
              'IDs e fundamento; na conclusão, confirmar/refutar/declarar inconclusiva a hipótese.')
        agent.run_session(SCENARIOS[args.investigacao][1], '127.0.0.1', str(path),
                          plan_confirmed=True, investigation_id=args.investigacao,
                          run_id=run_id, max_actions=6,
                          action_guard=authentication_guard() if args.investigacao == 'INV-02' else None)
    except (EOFError, KeyboardInterrupt):
        emit('preparacao_interrompida', estado='PENDENTE', motivo='interrupção humana; sem aprovação presumida')
    except (OSError, ValueError, subprocess.SubprocessError, KeyError, TypeError) as exc:
        emit('falha_preparacao_ou_sessao', estado='PENDENTE', erro=str(exc))
        print('Interrompido:', json.dumps(str(exc), ensure_ascii=True), file=sys.stderr)
        return 1
    finally:
        # Executado também em cancelamento; síntese conserva pendências e a origem das decisões.
        try:
            report = summarize(path)
            update_status(path)
            print(f'Evidências privadas: {directory}\nResumo: {report}')
        except (OSError, ValueError, KeyError, TypeError) as exc:
            print('Síntese/estado PENDENTE:', json.dumps(str(exc), ensure_ascii=True), file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
