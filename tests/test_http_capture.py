"""Respostas HTTP sintéticas em memória. Nenhum servidor do laboratório é consultado."""
import gzip
from http.client import HTTPResponse
from io import BytesIO
import unittest

import agent


def capture(headers, data):
    packet = b'HTTP/1.1 200 OK\r\n' + headers + b'\r\n\r\n' + data

    class SocketFixture:
        def makefile(self, mode):
            return BytesIO(packet)

    with HTTPResponse(SocketFixture(), method='GET') as response:
        response.begin()
        return agent.capture_http_response(response)


class HttpCaptureTests(unittest.TestCase):
    def test_reproduces_54_byte_deficit_even_with_closing_html(self):
        suffix = b'</body></html>'
        body = b'x' * (11025 - len(suffix)) + suffix
        result = capture(b'Content-Length: 11079', body)
        self.assertEqual(result['bytes_recebidos'], 11025)
        self.assertTrue(result['body'].endswith('</html>'))
        self.assertTrue(result['truncated'])
        self.assertTrue(result['content_length_divergente'])
        self.assertFalse(result['captura_http']['limite_local_atingido'])

    def test_local_cap_does_not_diagnose_short_transport(self):
        body = b'x' * (agent.MAX_BODY + 42)
        result = capture(f'Content-Length: {len(body)}'.encode(), body)
        self.assertEqual(len(result['body']), agent.MAX_BODY)
        self.assertTrue(result['captura_http']['limite_local_atingido'])
        self.assertTrue(result['truncated'])
        self.assertFalse(result['content_length_divergente'])

    def test_chunked_complete_and_missing_terminator(self):
        complete = capture(b'Transfer-Encoding: chunked', b'3\r\nabc\r\n0\r\n\r\n')
        interrupted = capture(b'Transfer-Encoding: chunked', b'3\r\nabc\r\n')
        self.assertEqual(complete['body'], 'abc')
        self.assertFalse(complete['truncated'])
        self.assertEqual(complete['captura_http']['enquadramento'], 'chunked')
        self.assertTrue(interrupted['truncated'])
        self.assertTrue(interrupted['captura_http']['leitura_interrompida'])
        self.assertIn('error', interrupted)
        self.assertEqual(interrupted['body'], '')

    def test_ambiguous_headers_do_not_produce_a_length_verdict(self):
        result = capture(b'Transfer-Encoding: chunked\r\nContent-Length: 12',
                         b'3\r\nabc\r\n0\r\n\r\n')
        self.assertEqual(result['captura_http']['enquadramento'], 'ambiguo')
        self.assertIsNone(result['captura_http']['bytes_declarados'])
        self.assertFalse(result['content_length_divergente'])

    def test_bytes_are_measured_before_decoding_and_redaction(self):
        for body, faithful in (('ação'.encode(), True), (b'\xff', False),
                               (b'{"password":"sentinela"}', False)):
            with self.subTest(faithful=faithful):
                result = capture(f'Content-Length: {len(body)}'.encode(), body)
                self.assertFalse(result['truncated'])
                self.assertEqual(result['bytes_recebidos'], len(body))
                self.assertEqual(result['captura_http']['corpo_textual_fiel'], faithful)
                self.assertNotIn('sentinela', result['body'])

    def test_encoded_payload_is_counted_without_ascribing_text(self):
        data = gzip.compress(b'conteudo sintetico')
        result = capture(f'Content-Length: {len(data)}\r\nContent-Encoding: gzip'.encode(), data)
        self.assertEqual(result['bytes_recebidos'], len(data))
        self.assertEqual(result['headers']['Content-Encoding'], 'gzip')
        self.assertFalse(result['truncated'])
        self.assertEqual(result['body'], '')
        self.assertFalse(result['captura_http']['corpo_textual_fiel'])
