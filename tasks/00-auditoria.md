# Bloco 00 — Auditoria, sincronização e diagnóstico

## Objetivo
Integrar os arquivos **já criados no Ubuntu**, conferir o repositório Git e o diagnóstico do KIT11. Não reimplementar aplicação existente.

## Entradas
`AGENTS.md`, `docs/STATE.md`, `docs/CONTEXT.md`, `diagnostico.md`, `PENDENCIAS.md`, `README.md`, `agent.py`, `tests/`, `scripts/`; PDFs apenas se houver divergência normativa.

## Tarefas
1. `pwd; git status --short; git branch -vv; git remote -v; git fetch origin`. Confrontar arquivos locais e remoto e **nunca resetar** ou sobrescrever trabalho não commitado.
2. Executar `python3 -m unittest discover -s tests -v`; registrar número e erros reais.
3. Coletar `uname -a`, `free -h`, `df -h /`, `ip -br addr`, `ss -lnt`, `command -v docker nmap ollama`. Não inferir serviço funcionando porque está instalado.
4. Inventariar serviços existentes/portas importantes 80/8000/1194 e impactos potenciais do Docker.
5. Conferir scripts start/restore, validação de alvo e gitignore; identificar perigos/bugs em vez de refatorar tudo.
6. Registrar diferenças para os dados históricos em `docs/STATE.md` e, se necessário, `docs/DECISIONS.md`.

## Critérios de aceite
- Estado local vs. remoto explicitado.
- Testes registrados separando mocks e integrações reais.
- Recursos, portas, serviços existentes e bloqueios registrados com data e comandos.
- Próximos riscos priorizados: serviço inexistente, publicação indevida, falha de autorização, logs insuficientes.
- Nenhuma instalação, scan ou modificação de rede sem permissão.

## Saída
Status, no máximo cinco riscos mais relevantes e se é seguro avançar ao bloco 01. Não avançar automaticamente.
