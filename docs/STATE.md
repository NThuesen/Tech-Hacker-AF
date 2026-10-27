# Estado atual e handoff

Atualizado documentalmente em 2026-10-27, **após** o push `codex inicial` na `main` (commit `c0508c72c2ff56e4aaee3320daa5a36463f6323f`). Estes dados refletem leitura do GitHub, **não** execução de comandos no Ubuntu pelo autor desta documentação.

## Código presente em main, verificado no GitHub
- `agent.py`: Python sem dependências externas, API Ollama em loopback, ferramentas `nmap`, `http_get` e `http_post`, confirmação humana, execução restrita ao IP local parametrizado e logs JSONL.
- `tests/test_agent.py`: **10** testes unitários definidos para validação/rejeição, modificação, Nmap delimitado, servidor HTTP simulado, modelo simulado, logs e erros.
- `scripts/start.sh` / `scripts/restore.sh`: Juice Shop `bkimminich/juice-shop:v17.3.0` no IP privado informado, restauração por remoção/criação de container.
- `README.md`, `diagnostico.md`, `PENDENCIAS.md`, `CHECKLIST_RUBRICA.md`, `docs/requisitos.md`, `plano_humano.md`, `relatorio_template.md`, `roteiro_video.md`.
- Os testes e instalações **não** foram executados por esta revisão no KIT11.

## Diagnóstico anterior (registrado pelo Codex em diagnostico.md)
- Ubuntu 24.04.1, Intel i5-14500T, 15 GiB RAM (~11 GiB disponível à época), ~39 GiB livres em /; interface `10.0.80.3/24`.
- Portas 80 e 8000 ocupadas por serviços existentes; 3000/11434 livres à época.
- Docker, Nmap e Ollama **não instalados quando o diagnóstico foi escrito**. Pode ter mudado: revalidar com comandos reais antes de afirmar bloqueio.
- Acesso pelo Kali e ausência de publicação WAN ainda não foram confirmados na evidência examinada.

## Lacunas observadas no código (a investigar no bloco 02)
1. `interpretacao` é produzida na **proposta anterior** à execução; não há evento explícito de interpretação do resultado recém-obtido quando o fluxo acaba. Verificar/implementar evidência vinculada a cada resultado.
2. O histórico é enviado ao LLM, mas os testes simulados verificam principalmente a presença do histórico no prompt; **não comprovam** que o modelo real modifica a decisão frente a evidências diferentes.
3. O POST atual usa corpo JSON e cabeçalho fixo; checar se cobre a investigação de autenticação escolhida sem expandir excessivamente permissões.
4. O estado de restauração, acesso Kali, isolamento da publicação e operação real da API Ollama permanecem por validar.

## Estado dos blocos
| Bloco | Status | Próxima evidência requerida |
|---|---|---|
| 00 — Auditoria/sincronização | PARCIAL | ler árvore local do Ubuntu, confirmar status do Git e rodar testes |
| 01 — Laboratório | NÃO VERIFICADO | Docker, Juice Shop HTTP, Ollama/Qwen, Nmap, restauração, Kali |
| 02 — Agente | PARCIAL | código existe; integração real, interpretação pós-resultado e decisões condicionais pendentes |
| 03 — Investigações | PENDENTE | plano humano e três execuções reais com supervisão |
| 04 — Entrega | PENDENTE | relatório/roteiro existentes são templates; consolidar evidências reais |

## Próxima sessão
Executar `tasks/00-auditoria.md` e confirmar que a branch de documentação foi integrada à `main`. **Não executar investigação definitiva antes de `plano_humano.md` aprovado.**

## Registro de sessão (acrescentar ao executar)
Data/hora e host:
Bloco solicitado:
Arquivos alterados:
Comandos/testes rodados + saídas resumidas:
Evidências (paths, IDs JSONL, capturas; sem segredos):
Decisões humanas recebidas:
Falhas/pendências:
Próximo passo:
