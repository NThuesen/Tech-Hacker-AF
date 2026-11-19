# KIT11-AF

Agente local supervisionado para o Juice Shop. Leia `diagnostico.md`, `docs/requisitos.md` e `PENDENCIAS.md`. O planejamento original está em `plano_humano.md`. **As três investigações técnicas do Bloco 03 já foram executadas** e possuem resumos em `docs/investigacoes/`; as decisões por ação foram delegadas ao Codex e a adequação acadêmica depende de revisão. O **Bloco 03B v2** está implementado e validado com fixtures; sessões ao vivo continuam pendentes.

## Bloco 03B: operação e estado

Consulte [operação 03B v2](docs/OPERACAO_BLOCO03B_V2.md), [estado verificável](docs/STATE.md) e [notas atômicas](docs/03b/INDEX.md). O replay não executa ferramentas; sessões reais exigem preflight e evidências atuais de rede. O relatório preparado está em [Markdown](docs/RELATORIO_ENTREGA.md) e [PDF de cinco páginas](docs/RELATORIO_ENTREGA.pdf); vídeo e revisão acadêmica seguem pendentes.

**Proposta prioritária v2:** compara decisões do Qwen, histórico e ledger, controles A/B/C e extensão/existência. Nicholas autorizou a implementação e delegou decisões ao Codex; essa delegação não comprova revisão acadêmica individual. O replay local com entradas simuladas foi executado e teve limitações de desenho e excesso do orçamento planejado, registrados em `docs/STATE.md`. Os documentos anteriores seguem como histórico.

- [Plano acadêmico e experimental v2](docs/PLANO_03B_EXCELENCIA_V2.md) — perguntas de pesquisa, dois trilhos separados, segurança e rubrica.
- [Backlog técnico v2 para Codex](tasks/03b-v2-excelencia-implementacao.md) — P0–P5 de programação/fixtures; P6 depende de autorização futura.
- [Handoff Codex v2](docs/HANDOFF_CODEX_03B_EXCELENCIA_V2.md) — contexto histórico e referências para revisão, sem executar ferramentas reais nesta etapa.

A proposta de melhoria é **corrigir o controle negativo da INV-03**, adicionar comparação A/B/C da INV-02 e verificar a seleção condicionada do Qwen na INV-01, com histórico factual e supervisão genuína. **Não executar experimentos, não modificar o plano original e não publicar logs automaticamente** nesta etapa de desenvolvimento.

1. [Plano experimental complementar — 03B](docs/PLANO_REFINAMENTO_BLOCO03B.md) — hipóteses, controles, segurança e matriz da rubrica.
2. [Backlog implementável e testes](tasks/03b-refinamento-experimental.md) — P0–P4, Definition of Done; P5 depende de nova autorização.
3. [Handoff e instrução para Codex](docs/HANDOFF_CODEX_BLOCO03B.md) — ordem de leitura, branch de trabalho, escopo e comando futuro.
4. [Análise das execuções originais](docs/investigacoes/ANALISE_BLOCO03.md) e [matriz de evidências](docs/investigacoes/MATRIZ_EVIDENCIAS.md).

A branch `evidencias/logs-completos-2026-10-27` preserva o snapshot histórico das execuções. Não fazer merge automático dos logs na `main`.

## Preparação

Python 3.10+ usa apenas biblioteca padrão (`requirements.txt`). O ambiente observado e suas limitações estão em `docs/STATE.md`. No KIT11, o Docker Rootless está instalado em `/home/kit11/.local/opt/kit11-docker`. A configuração autorizada publica a porta interna 3000 do Juice Shop em **127.0.0.1:3000 para Ubuntu/agente** e **10.0.80.3:3001 para Kali/OpenVPN**. Ollama permanece apenas em 127.0.0.1:11434. A verificação de isolamento WAN está pendente; não altere pfSense, VPN, NAT ou firewall.

Na raiz, após confirmar que o daemon Rootless e a API Ollama estão ativos:

```sh
export PATH="/home/kit11/.local/opt/kit11-docker:$PATH"
export DOCKER_HOST="unix:///run/user/$(id -u)/docker.sock"
./scripts/start.sh
curl --noproxy '*' --max-time 5 -i http://127.0.0.1:3000/
curl --noproxy '*' --max-time 5 -i http://10.0.80.3:3001/
python3 agent.py --ip 127.0.0.1 --log logs/investigacao1.jsonl
```

Os scripts usam explicitamente o socket Rootless local `/run/user/UID/docker.sock`, verificam o modo Rootless e o digest da imagem local, sem iniciar daemons ou baixar imagens automaticamente. A configuração compartilhada fica em `scripts/lab_common.sh`; os dois bindings são fixos. O argumento legado opcional `127.0.0.1` continua aceito, mas não muda os bindings; outros argumentos de IP são recusados.

O script de início verifica a identidade de um container existente e recusa substituí-lo. Os serviços do usuário estão habilitados, mas `Linger=no`; o container usa `--restart no`, portanto não há garantia de retomada após logout ou reinicialização. A imagem é `bkimminich/juice-shop:v17.3.0`, com digest validado `sha256:123acb31ed8bb05ebb06934a29be83d4e11a46cae937b9ed2bf2bda29d98130a`, sem volumes. Ambos os IPs devem estar vinculados ao Ubuntu.

O acesso do Kali pela VPN a `http://10.0.80.3:3001/` foi confirmado pelo usuário com HTTP 200. As verificações executadas pelo Codex nesta sessão partiram do Ubuntu e também retornaram 200 nos dois endpoints; não representam uma nova execução no Kali. Não é necessário habilitar SSH. Para repetir a checagem no próprio Kali conectado à VPN: `curl --noproxy '*' --max-time 5 -i http://10.0.80.3:3001/` ou `./scripts/diagnostico_kali.sh 10.0.80.3`.

Para verificação técnica isolada do modelo, sem investigação: `curl --noproxy '*' http://127.0.0.1:11434/api/generate -d '{"model":"qwen3:4b-instruct","prompt":"Responda JSON com ok true","format":"json","stream":false}'`.

## Operação e limites

Cada ciclo gera uma proposta JSON e solicita aprovação, modificação (com segunda aprovação), rejeição ou encerramento, com justificativa. Após executar, o modelo interpreta explicitamente o resultado; o operador decide continuar ou encerrar. Histórico, resultados e interpretações alimentam a próxima escolha. Não há seleção de ferramenta por roteiro no código.

O CLI aceita somente `--ip 127.0.0.1`. Nmap usa conexão TCP na porta 3000; HTTP aceita caminhos relativos sem proxies nem redirecionamentos. Limites: 20 propostas, até 40 chamadas de modelo, HTTP com prazo total de 8 s, Nmap com timeout de processo de 10 s, POST objeto JSON UTF-8 até 4 KiB e resposta HTTP até 16 KiB. Corpos extensos são reduzidos no contexto do modelo com truncamento explícito. JSON inválido, saída incompleta e falhas de log interrompem a operação. Detalhes em `docs/ENGENHARIA_BLOCO02.md`.

Logs exigem arquivos 0600 em diretório privado 0700, sem links; o CLI exige extensão `.jsonl`, ignorada pelo Git. Se `logs/` já existir com permissões compartilhadas, revise a propriedade e restrinja seu acesso antes de executar. Senhas/tokens em campos reconhecidos são redigidos, mas texto livre pode conter dados sensíveis: use somente dados de laboratório e revise antes de compartilhar. IDs ligam proposta, execução, resultado, interpretação e decisões; o modelo pode interpretar incorretamente mesmo retornando JSON válido.

Para ensaio técnico interativo, use `python3 agent.py --engenharia --ip 127.0.0.1 --log logs/engenharia-interativa.jsonl`. Essa opção identifica engenharia e não afirma aprovação do plano acadêmico; mantém a revisão antes de toda ação. O modo acadêmico continua exigindo a confirmação do plano pelo grupo.

## Restauração

`./scripts/restore.sh` exige digitar `RESTAURAR` e apaga os dados do container reconhecido. Antes de qualquer remoção, verifica nome, ID, digest, referência e rótulos da imagem, ausência de mounts/privilégios extras e os dois bindings esperados. Após a confirmação, reinspeciona e recusa se o ID mudou; remove pelo ID verificado e recria com ambos os endpoints. Divergências ou container ausente encerram a operação sem remoção. Não restaura serviços externos. A restauração real anterior com marcador descartável e os testes atuais com Docker simulado estão separados em `docs/STATE.md`.

## Testes

`python3 -m unittest discover -s tests -v` executa os testes locais com fixtures e mocks explicitamente identificados; as integrações reais são ignoradas por padrão. Com serviços ativos e autorização para as leituras técnicas, `KIT11_REAL_TESTS=1 python3 -m unittest discover -s tests -p test_engineering_real.py -v` consulta Ollama/Qwen, HTTP público local e Nmap reais. O gate automatizado desses testes não é decisão humana e não executa propostas condicionais A/B. Resultados e limitações observados estão em `docs/ENGENHARIA_BLOCO02.md`.

## Bloco 03 — execução supervisionada

A preparação e seus portões estão documentados em [docs/OPERACAO_BLOCO03.md](docs/OPERACAO_BLOCO03.md). Em terminal interativo no Ubuntu KIT11, execute **uma investigação por vez**, após deliberação real do grupo:

```sh
cd /home/kit11/Kit11-AF
./scripts/af_run.sh INV-01
./scripts/af_run.sh INV-02
./scripts/af_run.sh INV-03
```

Cada comando é independente: não executar a lista como lote. O script interrompe sem aprovação explícita do plano, evidências atuais Kali/WAN, restauração confirmada e preflight válido. Antes da execução, o grupo deve registrar evidência WAN com alcance explícito; bind privado não demonstra isolamento absoluto. A preparação inicial usou fixtures; os resultados reais posteriores estão na análise vinculada abaixo.


### Operação delegada autorizada no Bloco 03

Nicholas autorizou operação pelo Codex por dificuldade de entrada no terminal. O modo original acima permanece disponível. O modo delegado é iniciado com `python3 scripts/af_delegated.py INV-01 --autorizacao-nicholas 'referência explícita à autorização'`; exige Codex ativo revisando cada proposta pelo canal privado, sem sequência fixa de aprovações. Decisões delegadas são registradas separadamente das autorizações humanas.

Critérios e comandos em [operação delegada](docs/OPERACAO_DELEGADA_BLOCO03.md). Resultados reais, limitações, resumos individuais e matriz em [análise do Bloco 03](docs/investigacoes/ANALISE_BLOCO03.md). As três execuções técnicas terminaram; revisão acadêmica humana permanece pendente. WAN: bloqueio no caminho testado conforme evidência relatada por Nicholas, sem comprovação de isolamento absoluto. Bloco 04 não iniciado.
