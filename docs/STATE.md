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
| 01 — Laboratório | PARCIAL | laboratório local validado; acesso Kali por conexão já autorizada e isolamento WAN permanecem pendentes |
| 02 — Agente | PARCIAL | código existe; integração real, interpretação pós-resultado e decisões condicionais pendentes |
| 03 — Investigações | PENDENTE | plano humano e três execuções reais com supervisão |
| 04 — Entrega | PENDENTE | relatório/roteiro existentes são templates; consolidar evidências reais |

## Próxima sessão
Bloco 01 autorizado com Docker Rootless e bind em loopback; consultar o registro mais recente para as evidências e pendências. **Não executar investigação definitiva antes de `plano_humano.md` aprovado.**

## Registro de sessão — 2026-10-27 12:25 -03

- **Host e bloco:** `kit11-OptiPlex-Micro-7020`, bloco 00. Apenas este arquivo foi alterado; código e scripts preservados.
- **Git:** antes desta atualização, `git status --short` estava limpo; `git fetch origin` teve sucesso e `git rev-list --left-right --count HEAD...origin/main` retornou `0 0`. `main` e `origin/main` apontavam para `82735a7` (`docs: estrutura de execução do Codex por blocos`): a documentação já estava integrada. Sem arquivos não rastreados; caches Python ignorados presentes. Nenhum reset ou push.
- **Testes:** `python3 -m unittest discover -s tests -v`: 10 testes passaram. Servidor HTTP em loopback simulado, modelo e Nmap simulados; não constituem integração real com Juice Shop, Ollama, Nmap ou Kali.
- **Ambiente:** `uname -a`, `free -h`, `df -h /`, `ip -br addr`, `ip route`, `ss -lnt`, `ss -lnu`, `python3 --version` e `command -v`: kernel Linux 7.0.0-31, Python 3.12.3, 15 GiB RAM (11 GiB disponíveis), 39 GiB livres em `/`, `enp0s31f6` em `10.0.80.3/24`, rota padrão via `10.0.80.1`. Docker, Nmap e Ollama ausentes do PATH; isso não comprova ausência de toda instalação fora do PATH. Consistente com diagnóstico anterior; desempenho do modelo não verificado.
- **Serviços:** `ss` mostrou TCP 80 e 8000 em `*`, sem listeners TCP em 3000 ou 11434 e sem listener UDP 1194 no Ubuntu. `systemctl is-active` informou apache2, mysql, mariadb e openvpn ativos; nginx, docker e ollama inativos. O processo dono das portas não foi identificado por `ss` sem privilégios; os nomes WordPress/Nextcloud e OpenVPN no pfSense são histórico, não confirmação atual desses serviços ou da VPN externa. Docker pode alterar regras locais ao publicar portas; não se inspecionou nem alterou firewall/NAT.
- **Riscos priorizados:** (1) Docker, Nmap e Ollama indisponíveis no PATH e integrações reais não verificadas; (2) IP privado e publicação vinculada a ele não garantem isolamento WAN, e impacto do Docker nas regras precisa ser avaliado; (3) `local_ip` comprova IPv4 privado/loopback vinculável ao host, não que o serviço na porta 3000 seja o Juice Shop autorizado; `restore.sh` apaga o container chamado `kit11-juice` após confirmação, sem validar sua identidade; (4) interpretação explícita do último resultado e escolha condicionada por evidências reais permanecem pendentes de verificação; (5) logs podem conter corpos/cabeçalhos sensíveis e `.gitignore` cobre somente `logs/*.jsonl`, não caminhos arbitrários passados por `--log`.
- **Decisões humanas:** solicitada exclusivamente a auditoria do bloco 00; nenhuma instalação, ação ofensiva, mudança de rede, restauração ou publicação foi autorizada nesta sessão. Nenhuma dessas ações foi realizada.
- **Próximo passo:** bloco 01 somente após autorização do usuário. Recursos parecem suficientes para iniciar seu planejamento e diagnóstico, sem garantia de desempenho; instalação requer confirmação específica e acesso Kali, isolamento WAN e serviços reais continuam NÃO VERIFICADOS.

## Registro de sessão — 2026-10-27 12:29 -03 — bloco 01

- **Autorização:** usuário autorizou bloco 01, instalações de Docker, Nmap e Ollama, download de Qwen3 4B, testes e commit/push; proibiu alterações em NAT, firewall e rede sem autorização adicional e pediu interrupção diante de risco aos serviços.
- **BLOQUEADO — rede Docker:** documentação oficial de [Docker e iptables](https://docs.docker.com/engine/network/firewall-iptables/) descreve criação de regras para bridge e possível alteração da política de encaminhamento. `scripts/start.sh` usa publicação de porta na rede padrão. Antes de qualquer alteração, `sudo -n iptables -S FORWARD` retornou política `ACCEPT` e `sudo -n sysctl net.ipv4.ip_forward` retornou `0`. Inicializar Docker padrão pode alterar essas condições e afetar conectividade; instalação e execução foram suspensas. Não foram instalados Docker, Nmap ou Ollama nem baixados modelo ou imagem. Não foi feita mudança em firewall, NAT ou rede.
- **Isolamento NÃO VERIFICADO:** a interface permanece `10.0.80.3/24`; vincular a esse IP não comprova ausência de encaminhamento WAN no pfSense. A inspeção ou confirmação da configuração existente precisa ocorrer antes da publicação. Docker em modo host não equivale ao script atual: ignora `--publish` e compartilha a rede do host; não foi usado.
- **Serviços e recursos:** `ss -lntp` identificou Apache nas portas TCP 80 e 8000; `curl --noproxy '*' --max-time 5` para loopback retornou HTTP 200 e 302, respectivamente, antes de instalações. Esses códigos não comprovam todas as funções dos aplicativos. 3000/11434 sem listeners; 39 GiB livres em `/`. `systemctl is-active` registrou apache2, mysql, mariadb e openvpn ativos; Docker e Ollama inativos. Não se verificou a VPN ou pfSense remotamente.
- **Git e testes:** antes desta atualização, árvore limpa em `main` no commit `2bd57fc`, igual a `origin/main` após `git fetch origin` (`0 0`). `python3 -m unittest discover -s tests -v`: 10 testes passaram; servidor HTTP, modelo e Nmap simulados, sem integrações reais.
- **PENDENTE:** instalação e versões reais, tag da imagem, HTTP do Juice Shop, modelo e chamada Python, Nmap, restauração em dados descartáveis e teste no Kali. Nenhuma investigação definitiva foi executada. Próximo passo: avaliar com o responsável uma configuração de Docker que não altere as regras existentes e obter confirmação do isolamento WAN; qualquer mudança de rede exige autorização adicional. Não iniciar o bloco 02.

## Registro de sessão — 2026-10-27 — bloco 01, Docker Rootless

- **Autorização:** usuário autorizou instalar Docker Rootless, Nmap, Ollama e Qwen3 4B, testar o laboratório e restaurar dados descartáveis; vedou mudanças de firewall, NAT, `FORWARD`, `ip_forward`, pfSense e serviços existentes. Publicação inicial somente em loopback; commit/push autorizados.
- **Pré-requisitos e instalação:** o teste genérico `unshare --user --map-root-user true` falhou sob `kernel.apparmor_restrict_unprivileged_userns=1`; o perfil existente `/etc/apparmor.d/rootlesskit` permitiu `rootlesskit --net=slirp4netns --disable-host-loopback true`. Subuid/subgid já tinham 65536 IDs. Simulação APT indicou dez pacotes novos, nenhuma remoção e atualização de `login` e `passwd`; `sudo apt-get install --no-install-recommends uidmap slirp4netns rootlesskit nmap` foi concluído. Docker estático oficial 29.4.2 instalado em `/home/kit11/.local/opt/kit11-docker`, usando `/usr/bin/rootlesskit` 1.1.1 e slirp4netns 1.2.1. `docker info` reportou `rootless`; serviço do usuário ativo, daemon e socket Docker de sistema inativos. Sem alteração de AppArmor ou de `iptables=false`; `Linger=no`, logo a continuidade após logout/reinicialização não foi verificada.
- **Comparação de rede e serviços:** antes e depois, `ip -br addr` e `ip -4 route` mostraram `enp0s31f6` `10.0.80.3/24` e rota via `10.0.80.1`; `iptables -S FORWARD` indicou `ACCEPT`, `net.ipv4.ip_forward=0`, e `nft -nn list ruleset` não listou regras no host. Sem mudanças observadas nessas verificações; pfSense, NAT externo e funcionalidade integral dos serviços não foram inspecionados. Apache/mysql/openvpn ativos; HTTP local 80=200 e 8000=302 antes e depois. Nenhuma modificação de firewall, NAT ou configuração de rede realizada.
- **Juice Shop e restauração:** imagem `bkimminich/juice-shop:v17.3.0`, digest `sha256:123acb31ed8bb05ebb06934a29be83d4e11a46cae937b9ed2bf2bda29d98130a`. `./scripts/start.sh 127.0.0.1` e `docker ps` confirmaram publicação `127.0.0.1:3000->3000/tcp`; HTTP GET local retornou 200. Nmap 7.94SVN, `nmap -sT -Pn -n -p 3000 --max-retries 1 --host-timeout 8s 127.0.0.1`, reportou porta aberta. Um marcador descartável em `/tmp` foi criado no container novo; `./scripts/restore.sh 127.0.0.1` recebeu `RESTAURAR`, recriou-o de `33242a3997be` para `7799fa95df71`, manteve o bind e eliminou o marcador; HTTP retornou 200 depois. Tentativas de executar `touch` e `node` pelo PATH falharam pois a imagem não os fornece nesse PATH; usado `/nodejs/bin/node`. Isso testa a recriação do sistema de arquivos descartável, não todos os possíveis estados da aplicação.
- **Ollama:** binários oficiais instalados em `/home/kit11/.local/opt/kit11-ollama`; serviço de usuário `kit11-ollama.service` configurado com `OLLAMA_HOST=127.0.0.1:11434`. Versão 0.40.11; `ss` confirmou listener apenas em loopback. `ollama list` mostrou `qwen3:4b-instruct`, ID `0edcdef34593`, 2,5 GB. Chamada Python real com `urllib.request` sem proxy à API `/api/generate`, prompt `Responda apenas um objeto JSON com a chave ok e o valor true.`, `format=json`, `stream=false`, `think=false`, `num_predict=64`: resposta abaixo parseada tanto no envelope quanto em `response`, `ok=true`, `done=true`, latência observada de 3,172 s. É teste técnico, não evidência de investigação ou escolha de ferramentas.

```json
{"model":"qwen3:4b-instruct","created_at":"2026-10-27T15:41:20.863470293Z","response":"{\"ok\": true}","done":true,"done_reason":"stop","context":[151644,872,198,1061,618,3235,46667,4443,35543,4718,469,264,97635,5394,384,297,14116,830,13,151645,198,151644,77091,198,4913,562,788,830,92],"total_duration":3157089622,"load_duration":2568678454,"prompt_eval_count":24,"prompt_eval_cached_count":0,"prompt_eval_duration":317464000,"eval_count":6,"eval_duration":267413000}
```
- **Kali PENDENTE:** `systemctl is-active ssh sshd` retornou inativo e `ss` não mostrou TCP/22 no KIT11. Um túnel `ssh -L 127.0.0.1:3000:127.0.0.1:3000` pelo cliente Kali seria possível somente por uma conexão SSH ao host previamente autorizada, disponível e com encaminhamento permitido; nenhuma foi identificada ou configurada, e Kali não foi testado. Loopback do KIT11 não é diretamente acessível pelo Kali.
- **Testes automatizados:** `python3 -m unittest discover -s tests -v`: 10 passaram novamente após instalações; os testes de HTTP/modelo/Nmap usam simulações, distintas das verificações reais acima. Às 12:41 -03, HTTP 80=200, 8000=302 e 3000=200; Apache/mysql/openvpn e serviços de usuário Docker/Ollama ativos; daemon e socket Docker de sistema inativos, 32 GiB livres em `/`. Nenhuma investigação definitiva ou ação do agente acadêmico foi executada.
- **Pendências:** testar o acesso Kali por conexão SSH já autorizada, se existir, e confirmar isolamento WAN; bloco 01 permanece PARCIAL pelos critérios de acesso externo. Os serviços de usuário estão habilitados, mas `Linger=no`; o container foi criado com `--restart no` e não há garantia de retomada após logout ou reinicialização. Não iniciar bloco 02 sem autorização.
