"""Fixtures de Docker: nunca criam/removem containers reais nem alteram a rede."""
import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
IMAGE_ID = 'sha256:123acb31ed8bb05ebb06934a29be83d4e11a46cae937b9ed2bf2bda29d98130a'
CONTAINER = {
    'Id': 'a' * 64, 'Name': '/kit11-juice', 'Image': IMAGE_ID,
    'Config': {'Image': 'bkimminich/juice-shop:v17.3.0', 'Labels': {
        'org.opencontainers.image.source': 'https://github.com/juice-shop/juice-shop',
        'org.opencontainers.image.version': '17.3.0'}},
    'HostConfig': {'NetworkMode': 'bridge', 'Privileged': False, 'PortBindings': {
        '3000/tcp': [{'HostIp': '127.0.0.1', 'HostPort': '3000'},
                     {'HostIp': '10.0.80.3', 'HostPort': '3001'}]}}, 'Mounts': []}

FAKE_DOCKER = '''#!/usr/bin/python3
import json, os, sys
from pathlib import Path
path = Path(os.environ['KIT11_DOCKER_FIXTURE'])
state = json.loads(path.read_text())
args = sys.argv[1:]
if args[:2] != ['--host', 'unix:///run/user/' + str(os.getuid()) + '/docker.sock']:
    sys.exit('Fixture exige socket Rootless explícito')
if os.environ.get('DOCKER_CONTEXT') != '':
    sys.exit('Fixture exige neutralização do contexto externo')
args = args[2:]
state.setdefault('calls', []).append(args)
path.write_text(json.dumps(state))
if args[0] == 'info':
    if state.get('daemon_error'): sys.exit('Fixture daemon indisponível')
    print(json.dumps(['name=rootless'] if state.get('rootless', True) else ['name=seccomp']))
elif args[:2] == ['image', 'inspect']:
    print(state.get('image_id', state['container']['Image']))
elif args[:2] == ['container', 'ls']:
    if state.get('exists', True): print(state['container']['Id'])
elif args[:2] == ['container', 'inspect']:
    if not state.get('exists', True): sys.exit('Fixture container ausente')
    state['inspections'] = state.get('inspections', 0) + 1
    if state.get('replace_after_inspect') and state['inspections'] > 1:
        state['container']['Id'] = 'b' * 64
    path.write_text(json.dumps(state))
    print(json.dumps([state['container']]))
elif args[:2] == ['container', 'rm']:
    if args != ['container', 'rm', '--force', state['container']['Id']]:
        sys.exit('Fixture recusa remoção sem ID exato')
    state['exists'] = False
    path.write_text(json.dumps(state))
elif args[0] == 'run':
    state['exists'] = True
    path.write_text(json.dumps(state))
    print('c' * 64)
else:
    sys.exit('Comando inesperado na fixture: ' + repr(args))
'''


class LabScriptTests(unittest.TestCase):
    def run_script(self, script, state=None, answer='', arguments=()):
        fixture = {'container': copy.deepcopy(CONTAINER), 'exists': True,
                   'image_id': IMAGE_ID, **(state or {})}
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            state_path = directory / 'state.json'
            state_path.write_text(json.dumps(fixture))
            fake = directory / 'docker'
            fake.write_text(FAKE_DOCKER)
            fake.chmod(0o755)
            # Apenas a existência do IP é simulada para rodar fora do KIT11.
            # Os validadores JSON/identidade executam Python real.
            python = directory / 'python3'
            python.write_text('#!/bin/sh\ncase "$2" in *"for address in"*) exit 0;; esac\nexec /usr/bin/python3 "$@"\n')
            python.chmod(0o755)
            env = {**os.environ, 'PATH': str(directory) + ':' + os.environ['PATH'],
                   'KIT11_DOCKER_FIXTURE': str(state_path),
                   'DOCKER_CONTEXT': 'fixture-contexto-externo', 'DOCKER_HOST': 'unix:///var/run/docker.sock'}
            result = subprocess.run([str(ROOT / 'scripts' / script), *arguments], input=answer,
                                    text=True, capture_output=True, cwd=directory, env=env, timeout=5)
            state = json.loads(state_path.read_text())
        return result, state

    def assert_no_mutation(self, state):
        self.assertFalse(any(call[0] == 'run' or call[:2] == ['container', 'rm']
                             for call in state.get('calls', [])))

    def assert_bindings(self, call):
        published = [call[n + 1] for n, value in enumerate(call) if value == '--publish']
        self.assertEqual(published, ['127.0.0.1:3000:3000', '10.0.80.3:3001:3000'])
        self.assertIn('never', call)

    def test_start_uses_two_fixed_bindings_and_rootless_socket(self):
        result, state = self.run_script('start.sh', {'exists': False})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_bindings(next(call for call in state['calls'] if call[0] == 'run'))

    def test_start_preserves_existing_container(self):
        result, state = self.run_script('start.sh')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('reconhecido', result.stderr)
        self.assert_no_mutation(state)

    def test_restore_recreates_only_verified_id_with_same_bindings(self):
        result, state = self.run_script('restore.sh', answer='RESTAURAR\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        removal = next(call for call in state['calls'] if call[:2] == ['container', 'rm'])
        self.assertEqual(removal[-1], CONTAINER['Id'])
        self.assertEqual(state['inspections'], 2)
        self.assert_bindings(next(call for call in state['calls'] if call[0] == 'run'))

    def test_restore_refuses_wrong_identity_or_bindings(self):
        cases = []
        for key, value in [('Name', '/wordpress'), ('Image', 'sha256:' + '0' * 64),
                           ('Mounts', [{'Source': '/dados'}])]:
            item = copy.deepcopy(CONTAINER)
            item[key] = value
            cases.append(item)
        item = copy.deepcopy(CONTAINER)
        item['Config']['Image'] = 'wordpress:latest'
        cases.append(item)
        item = copy.deepcopy(CONTAINER)
        item['HostConfig']['PortBindings']['3000/tcp'][1]['HostIp'] = '0.0.0.0'
        cases.append(item)
        for item in cases:
            with self.subTest(container=item):
                result, state = self.run_script('restore.sh', {'container': item}, 'RESTAURAR\n')
                self.assertNotEqual(result.returncode, 0)
                self.assert_no_mutation(state)

    def test_restore_cancelled_never_removes(self):
        result, state = self.run_script('restore.sh', answer='cancelar\n')
        self.assertNotEqual(result.returncode, 0)
        self.assert_no_mutation(state)

    def test_replaced_container_during_confirmation_is_not_removed(self):
        result, state = self.run_script('restore.sh', {'replace_after_inspect': True}, 'RESTAURAR\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('mudou', result.stderr)
        self.assert_no_mutation(state)

    def test_rootful_daemon_and_missing_container_are_refused(self):
        for fixture in ({'rootless': False}, {'daemon_error': True}, {'exists': False},
                        {'image_id': 'sha256:' + '0' * 64}):
            with self.subTest(fixture=fixture):
                result, state = self.run_script('restore.sh', fixture, 'RESTAURAR\n')
                self.assertNotEqual(result.returncode, 0)
                self.assert_no_mutation(state)

    def test_arbitrary_bind_argument_is_refused_before_docker(self):
        for script in ('start.sh', 'restore.sh'):
            result, state = self.run_script(script, arguments=('0.0.0.0',))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(state.get('calls', []), [])


if __name__ == '__main__':
    unittest.main()
