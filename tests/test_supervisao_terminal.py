"""Terminal de teste local: sem Ollama, Juice Shop ou ferramentas de investigação."""
import os
import pty
import select
import subprocess
import sys
import unittest
from pathlib import Path


class TerminalTest(unittest.TestCase):
    def test_uma_tecla_sem_enter(self):
        master, slave = pty.openpty()
        process = None
        try:
            process = subprocess.Popen(
                [sys.executable, '-c', 'import agent; print("RESULTADO=" + agent.read_key("DECIDA: "), flush=True)'],
                cwd=Path(__file__).resolve().parents[1], stdin=slave, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            os.close(slave)
            slave = None
            ready, _, _ = select.select([process.stdout], [], [], 5)
            self.assertTrue(ready, 'prompt não apareceu no prazo')
            prompt = os.read(process.stdout.fileno(), 128)
            self.assertIn(b'DECIDA:', prompt)
            os.write(master, b'a')  # Sem newline: aprovação é uma tecla.
            out, err = process.communicate(timeout=5)
            self.assertEqual(process.returncode, 0, err.decode(errors='replace'))
            self.assertIn(b'RESULTADO=a', out)
        finally:
            if process is not None and process.poll() is None:
                process.kill()
                process.communicate()
            os.close(master)
            if slave is not None:
                os.close(slave)


if __name__ == '__main__':
    unittest.main()
