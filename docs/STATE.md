# Estado atual e handoff

Atualizado na criação da estrutura documental (2026-10-27). **Este arquivo não é diagnóstico do Ubuntu**.

## Fatos verificados sobre a branch remota
- `main` no GitHub continha apenas os PDFs da AF e do relatório KIT11 quando a estrutura foi iniciada.
- Código citado em conversas (`agent.py`, README, testes e scripts) **não foi observado na branch remota**. Pode estar apenas no Ubuntu. Verificar `git status`, `git log`, `git remote -v` e comparar `origin/main` antes de tocar no código.
- Não se executaram comandos no Ubuntu nem testes de integração reais nesta operação documental.

## Status dos blocos
| Bloco | Status | Evidência/pendência |
|---|---|---|
| 00 — Auditoria/sincronização | PENDENTE | inspecionar arquivos locais, hardware e resultados reais |
| 01 — Laboratório | NÃO VERIFICADO | Docker, Juice Shop HTTP, Ollama/LLM, rota Kali |
| 02 — Agente | NÃO VERIFICADO | verificar implementação existente e testes condicionais |
| 03 — Investigações | PENDENTE | plano humano e execução supervisionada reais |
| 04 — Entrega | PENDENTE | consolidar somente evidências reais |

## Registro de sessão (acrescentar ao executar)
Data/hora e host:
Bloco solicitado:
Arquivos alterados:
Comandos e testes rodados + resumo real:
Evidências (paths, screenshots, JSONL; sem segredos):
Decisões humanas recebidas:
Problemas não resolvidos:
Próxima ação proposta:

**Regra:** uma resposta do LLM ou um arquivo criado não é prova de funcionamento ou de vulnerabilidade.
