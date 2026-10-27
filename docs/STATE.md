# Estado atual e handoff

Atualizado em 2026-10-27 após auditoria no Ubuntu do KIT11; o registro de sessão abaixo distingue as evidências atuais do histórico documental.

## Código presente em main, verificado no GitHub
- `agent.py`: Python sem dependências externas, API Ollama em loopback, ferramentas `nmap`, `http_get` e `http_post`, confirmação humana, execução restrita ao IP local parametrizado e logs JSONL.
- `tests/test_agent.py`: **10** testes unitários definidos para validação/rejeição, modificação, Nmap delimitado, servidor HTTP simulado, modelo simulado, logs e erros.
- `scripts/start.sh` / `scripts/restore.sh`: Juice Shop `bkimminich/juice-shop:v17.3.0` no IP privado informado, restauração por remoção/criação de container.
- `README.md`, `diagnostico.md`, `PENDENCIAS.md`, `CHECKLIST_RUBRICA.md`, `docs/requisitos.md`, `plano_humano.md`, `relatorio_template.md`, `roteiro_video.md`.
- A auditoria atual executou os testes locais; instalações e integrações reais continuam pendentes.

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
| 00 — Auditoria/sincronização | CONCLUÍDO | auditoria local e comparação com origin registradas abaixo; laboratório real permanece pendente |
| 01 — Laboratório | NÃO VERIFICADO | Docker, Juice Shop HTTP, Ollama/Qwen, Nmap, restauração, Kali |
| 02 — Agente | PARCIAL | código existe; integração real, interpretação pós-resultado e decisões condicionais pendentes |
| 03 — Investigações | PENDENTE | plano humano e três execuções reais com supervisão |
| 04 — Entrega | PENDENTE | relatório/roteiro existentes são templates; consolidar evidências reais |

## Próxima sessão
Com autorização para o bloco 01, planejar a validação do laboratório; instalações administrativas exigem confirmação específica. **Não executar investigação definitiva antes de `plano_humano.md` aprovado.**

## Registro de sessão — 2026-10-27 12:25 -03

- **Host e bloco:** `kit11-OptiPlex-Micro-7020`, bloco 00. Apenas este arquivo foi alterado; código e scripts preservados.
- **Git:** antes desta atualização, `git status --short` estava limpo; `git fetch origin` teve sucesso e `git rev-list --left-right --count HEAD...origin/main` retornou `0 0`. `main` e `origin/main` apontavam para `82735a7` (`docs: estrutura de execução do Codex por blocos`): a documentação já estava integrada. Sem arquivos não rastreados; caches Python ignorados presentes. Nenhum reset ou push.
- **Testes:** `python3 -m unittest discover -s tests -v`: 10 testes passaram. Servidor HTTP em loopback simulado, modelo e Nmap simulados; não constituem integração real com Juice Shop, Ollama, Nmap ou Kali.
- **Ambiente:** `uname -a`, `free -h`, `df -h /`, `ip -br addr`, `ip route`, `ss -lnt`, `ss -lnu`, `python3 --version` e `command -v`: kernel Linux 7.0.0-31, Python 3.12.3, 15 GiB RAM (11 GiB disponíveis), 39 GiB livres em `/`, `enp0s31f6` em `10.0.80.3/24`, rota padrão via `10.0.80.1`. Docker, Nmap e Ollama ausentes do PATH; isso não comprova ausência de toda instalação fora do PATH. Consistente com diagnóstico anterior; desempenho do modelo não verificado.
- **Serviços:** `ss` mostrou TCP 80 e 8000 em `*`, sem listeners TCP em 3000 ou 11434 e sem listener UDP 1194 no Ubuntu. `systemctl is-active` informou apache2, mysql, mariadb e openvpn ativos; nginx, docker e ollama inativos. O processo dono das portas não foi identificado por `ss` sem privilégios; os nomes WordPress/Nextcloud e OpenVPN no pfSense são histórico, não confirmação atual desses serviços ou da VPN externa. Docker pode alterar regras locais ao publicar portas; não se inspecionou nem alterou firewall/NAT.
- **Riscos priorizados:** (1) Docker, Nmap e Ollama indisponíveis no PATH e integrações reais não verificadas; (2) IP privado e publicação vinculada a ele não garantem isolamento WAN, e impacto do Docker nas regras precisa ser avaliado; (3) `local_ip` comprova IPv4 privado/loopback vinculável ao host, não que o serviço na porta 3000 seja o Juice Shop autorizado; `restore.sh` apaga o container chamado `kit11-juice` após confirmação, sem validar sua identidade; (4) interpretação explícita do último resultado e escolha condicionada por evidências reais permanecem pendentes de verificação; (5) logs podem conter corpos/cabeçalhos sensíveis e `.gitignore` cobre somente `logs/*.jsonl`, não caminhos arbitrários passados por `--log`.
- **Decisões humanas:** solicitada exclusivamente a auditoria do bloco 00; nenhuma instalação, ação ofensiva, mudança de rede, restauração ou publicação foi autorizada nesta sessão. Nenhuma dessas ações foi realizada.
- **Próximo passo:** bloco 01 somente após autorização do usuário. Recursos parecem suficientes para iniciar seu planejamento e diagnóstico, sem garantia de desempenho; instalação requer confirmação específica e acesso Kali, isolamento WAN e serviços reais continuam NÃO VERIFICADOS.
