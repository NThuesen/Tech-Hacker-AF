"""Controles puros do 03B; não executam ferramentas nem autorizam sessões."""
import hashlib
import html
from html.parser import HTMLParser
import json
from urllib.parse import unquote

import agent

SCENARIOS = {'INV-01-B', 'INV-02-B', 'INV-03-B'}
LOGIN = '/rest/user/login'
EMAIL = 'af_inexistente_01@kit11.invalid'
MISSING_MD = '/ftp/arquivo-inexistente-af.md'
FTP_FILES = {'/ftp/legal.md', '/ftp/README.md'}


class ListingLinks(HTMLParser):
    """Conservador: somente referências exatas em âncoras da listagem."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.names = set()

    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'a':
            return
        for key, value in attrs:
            if key.lower() == 'href' and isinstance(value, str):
                href = value
                for _ in range(3):
                    href = unquote(html.unescape(href))
                if href.startswith('/ftp/'):
                    href = href[len('/ftp/'):]
                if href in {'legal.md', 'README.md', 'arquivo-inexistente-af.md'}:
                    self.names.add(href)


class ScenarioGuard:
    """Estado restrito a uma sessão; chamador deve parar após qualquer bloqueio."""

    def __init__(self, scenario):
        if scenario not in SCENARIOS:
            raise ValueError('cenário 03B inválido')
        self.scenario = scenario
        self.variants = set()
        self.checked_paths = set()
        self.listing = None
        self.listed_names = set()

    def check(self, action):
        agent.validate_proposal(action)
        tool, params = action['ferramenta'], action['parametros']
        path = params.get('path')
        if self.scenario == 'INV-01-B':
            if tool == 'nmap' or (tool == 'http_get' and path in {
                    '/', '/rest/admin/application-version', '/api/Products/1'}):
                return None
        elif self.scenario == 'INV-02-B' and tool == 'http_post' and path == LOGIN:
            body = agent.parse_json(params['body'])
            if body.get('email') == EMAIL:
                if set(body) == {'email'}:
                    variant = 'C'
                elif set(body) == {'email', 'password'} and body['password'] == '':
                    variant = 'B'
                elif set(body) == {'email', 'password'} and body['password'] == 'teste-invalido-01':
                    variant = 'A'
                else:
                    raise ValueError('controle de autenticação inválido')
                if variant in self.variants:
                    raise ValueError('variante repetida')
                self.variants.add(variant)
                return variant
        elif self.scenario == 'INV-03-B' and tool == 'http_get':
            if path in {'/', '/ftp/'}:
                return None
            if path in self.checked_paths:
                raise ValueError('controle de recurso já executado')
            if path == '/ftp/arquivo-inexistente-af.txt':
                self.checked_paths.add(path)
                return None
            if path == MISSING_MD:
                if self.listing is not None and 'arquivo-inexistente-af.md' not in self.listing:
                    self.checked_paths.add(path)
                    return None
                raise ValueError('listagem completa da sessão não comprova ausência do arquivo')
            if path in FTP_FILES and self.listing is not None and path.rsplit('/', 1)[-1] in self.listed_names:
                self.checked_paths.add(path)
                return None
        raise ValueError('ação fora do escopo do cenário 03B')

    def observe(self, action, result, *, listing_verified=False):
        """Registra listagem completa apenas após verificação explícita do operador.

        O chamador deve validar formato e ausência/presença dos nomes; HTTP 200
        sozinho pode ser uma página de erro e não prova que há uma listagem.
        Apenas âncoras exatas permitem o controle positivo.
        """
        if action.get('ferramenta') == 'http_get' and action.get('parametros', {}).get('path') == '/ftp/':
            self.listing = None
            self.listed_names = set()
            body = result.get('body')
            headers = result.get('headers', {})
            declared = next((v for k, v in headers.items() if k.lower() == 'content-length'), None) if isinstance(headers, dict) else None
            expected_bytes = int(declared) if isinstance(declared, str) and declared.isdecimal() else None
            received_bytes = result.get('bytes_recebidos')
            capture = result.get('captura_http')
            if capture is not None and (
                    not isinstance(capture, dict)
                    or capture.get('enquadramento') not in ('content_length', 'chunked')
                    or capture.get('corpo_textual_fiel') is not True):
                return
            if received_bytes is None and isinstance(body, str):
                received_bytes = len(body.encode('utf-8'))
            if (listing_verified is True and result.get('status') == 200 and result.get('truncated') is False
                    and isinstance(body, str) and body.strip()
                    and len(body.encode('utf-8')) == received_bytes
                    and (expected_bytes is None or received_bytes == expected_bytes)):
                # Entidades HTML e URL podem representar nomes sem texto literal.
                normalized = body
                for _ in range(3):
                    normalized = unquote(html.unescape(normalized))
                parser = ListingLinks()
                parser.feed(body)
                self.listing = normalized
                self.listed_names = parser.names


def factual_context(objective, history):
    """Projeta evidências sem promover alegações ou avaliação a fatos observados."""
    if not isinstance(objective, str) or not objective.strip() or len(objective) > 2000:
        raise ValueError('objetivo inválido')
    records = []
    eligible = [h for h in history if isinstance(h, dict) and h.get('result_id') and isinstance(h.get('resultado'), dict)]
    for item in eligible[-8:]:
        result = item['resultado']
        action = item.get('acao', {})
        observed = {k: result[k] for k in ('status', 'truncated', 'redirect_followed', 'exit_code', 'error',
                                           'bytes_recebidos', 'content_length_divergente', 'captura_http') if k in result}
        if isinstance(result.get('headers'), dict):
            observed['headers'] = {k: v for k, v in result['headers'].items()
                                   if k.lower() in ('content-type', 'content-length')}
        if item.get('variant') in ('A', 'B', 'C'):
            observed['variant'] = item['variant']
        for key in ('body', 'stdout', 'stderr'):
            if isinstance(result.get(key), str):
                raw = result[key].encode('utf-8')
                observed[key + '_bytes_disponiveis'] = len(raw)
                observed[key + '_sha256'] = hashlib.sha256(raw).hexdigest()
        records.append({'run_id': item.get('run_id'), 'result_id': item['result_id'], 'acao': agent.redact(action),
                        'observado': observed, 'alegacao_modelo': agent.redact(item.get('interpretacao_resultado')),
                        'avaliacao_revisor': agent.redact(item.get('avaliacao_revisor')),
                        'origem_avaliacao': item.get('origem_avaliacao', 'não informada'),
                        'nao_testado': []})
    context = {'objetivo': objective, 'ledger': records}
    size = lambda: len(json.dumps(context, ensure_ascii=False).encode('utf-8'))
    while records and size() > 12000:
        records.pop(0)
    if size() > agent.MAX_CONTEXT_BYTES:
        raise ValueError('contexto excede o limite')
    return context, {'bytes': size(), 'incluidos': [r['result_id'] for r in records],
                     'omitidos': len(eligible) - len(records),
                     'disponibilidade': 'Ledger inclui hash e tamanho das saídas, não o texto; pode diferir do modo A.'}


def original_context(objective, history):
    context = agent.recent_history(objective, history)
    included = context['historico']
    return context, {'bytes': len(json.dumps(context, ensure_ascii=False).encode('utf-8')),
                     'incluidos': [item['result_id'] for item in included if isinstance(item, dict) and item.get('result_id')],
                     'omitidos': len(history) - len(included), 'disponibilidade': 'Histórico legado compactado.'}
