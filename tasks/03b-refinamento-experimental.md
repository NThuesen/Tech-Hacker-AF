# Task 03B — Implementação mínima do refinamento experimental

**Estado:** BACKLOG PRONTO PARA CODIFICAR; **nenhum código foi alterado por esta task**.  
**Fonte normativa do escopo:** [plano complementar](../docs/PLANO_REFINAMENTO_BLOCO03B.md), [plano original](../plano_humano.md), [rubrica](../docs/RUBRIC.md).  
**Baseline:** `docs/investigacoes/INV-01/02/03/resumo.md`, `docs/investigacoes/ANALISE_BLOCO03.md`, e branch `evidencias/logs-completos-2026-10-27`.

## Resultado esperado

Construir modo **03B** pequeno, reproduzível e supervisionado para complementar as investigações existentes, **sem alterar os logs/interpretações passados, sem ampliar o alvo, sem instalar plataformas novas, sem executar experimentos automaticamente**.

## Inventário de código relevante (conferido em 29/10/2026)

- `agent.py`: `run_session` recebe `reviewer=None` para interação humana no terminal; `recent_history` usa as últimas 8 entradas, com limite de tamanho; `interpret_result` recebe só a ação/resultado corrente; `compact_context` reduz saídas grandes a 2048 bytes de contexto e sinaliza truncagem; `execute` fixa loopback e Nmap TCP/3000; limites incluem 16KiB para resultado HTTP.
- `scripts/af_session.py`: `SCENARIOS` contém somente INV-01/02/03; `authentication_guard()` já restringe A/B/C com email fixo e impede repetição; `prepare` verifica aprovação, rede, identidade de container, modelo, restauração e snapshot do `plano_humano.md`.
- `scripts/af_delegated.py`: canal de decisões automatizadas com identificação distinta e `scope_guard` restritivo: INV-03 contém `/ftp/arquivo-inexistente-af.txt`, `/ftp/legal.md`, `/ftp/README.md`, **não** contém o novo candidato `/ftp/arquivo-inexistente-af.md`. A lista de INV-01 é fechada. Não transformar essas decisões em decisões humanas.
- `scripts/af_summarize.py`: sintetiza eventos e preserva relação de IDs; atualização de checklist pode escrever informação automática de sessões, portanto a implementação do 03B deve rotular seus resumos e evitar sobrescrever os estados históricos.
- `scripts/restore.sh`, `scripts/lab_common.sh`: proteções já existentes de identidade, binding e digest antes de remoção. Reusar, não contornar.
- `tests/`: suíte anterior comunicou 61 testes, 58 PASS e 3 integrações opt-in SKIP. Essa contagem é baseline histórico, **não promete resultado do código novo**.

## P0 — Contrato de escopo, compatibilidade e aprovação

- [ ] Criar abordagem mínima de execução 03B (novo wrapper, por exemplo `scripts/af_refine.py`, ou extensão estritamente isolada da CLI existente); documentar opção escolhida.
- [ ] Não modificar os experimentos originais nem `plano_humano.md` (hash histórico serve para comparar). `docs/PLANO_REFINAMENTO_BLOCO03B.md` deve ser aprovado e seu SHA256 capturado antes da primeira consulta ao modelo.
- [ ] `scenario=INV-01-B|INV-02-B|INV-03-B` e `phase=03B` precisam aparecer **nos metadados das sessões**, mantendo `investigation_id=INV-01|02|03` apenas para compatibilidade com `agent.run_session`. Gerar `run_id` único e salvar exclusivamente em `logs/03B/INV-0N/<run_id>/` com permissões privadas.
- [ ] Aceitar explicitamente **modo supervisionado** para estudo 03B e validar que a decisão antes de executar cada ação tem origem terminal humana e justificativa não vazia. O Codex só poderá escrever fixtures de interação em testes marcados como simulação, nunca simular entrada humana em sessão real. Se preservar modo delegado alternativo, rotular e separar por completo, sem usá-lo como evidência de aprovação humana.
- [ ] Preflight e restauração destrutiva seguem com confirmação humana de identidade e da perda de estado; jamais respostas pré-programadas de aceite para operação real. Código do cenário não altera portas/serviços/roteadores.
- [ ] Garantir que o plan hash do adendo não se perca após snapshot; alterações entre aprovação e execução abortam.

**Aceite P0:** novos metadados em fixtures, guard de alvo/proposta, IDs únicos, diretórios privados; nenhuma execução com adendo pendente ou confirmação de restauração ausente. Regressões do fluxo original passam.

## P1 — INV-03B, primeira prioridade (controle negativo corrigido)

- [ ] Adicionar **somente no cenário 03B** a allowlist para `GET /`, `GET /ftp/`, `GET /ftp/arquivo-inexistente-af.md` e `GET /ftp/arquivo-inexistente-af.txt` (controle comparativo, quando aprovado). Nenhuma expansão genérica `/ftp/*`.
- [ ] Antes de GET do falso arquivo `.md`, validar/registrar evidência de que o nome não está listado no corpo de `GET /ftp/` **na sessão atual**; se houver truncagem ou impossibilidade de conferir a listagem, suspender o negativo e solicitar revisão humana.
- [ ] Se autorizado um documento positivo, permitir exclusivamente `/ftp/legal.md` ou `/ftp/README.md` **após** presença confirmada na listagem e avaliação humana da natureza pública; sem baixar outros documentos.
- [ ] Cada controle produz resultado e interpretação independentes. `HTTP 403` por extensão não deve bloquear a documentação do resultado **nem** ser contornado; decidir continuar apenas se o humano justificar que o próximo teste continua no escopo. `423/429`, segredo, erro de identidade ou outra parada de segurança **sempre abortam**.
- [ ] Registrar se comparações cruzaram sessões/datas; um `.txt` histórico nunca substitui um controle pareado sob mesmo estado.

**Aceite P1:** teste fixture “listagem /ftp/ contém X, candidato .md ausente” permite a proposta `.md`; fixtures “nome presente”, “listagem truncada” e “arquivo fora da lista” **bloqueiam**; teste fixture `403` registra interpretação cautelosa; teste de resultado não deve presumir `404`.

## P2 — INV-02B, comparação A/B/C

- [ ] Reusar `authentication_guard()` com identificador fixo `af_inexistente_01@kit11.invalid` e rota `/rest/user/login`. Garantir três variantes, uma vez cada, corpo JSON: A senha fictícia inválida; B vazia; C campo `password` omitido.
- [ ] Registrar explicitamente qual variante foi executada (`A/B/C`), **sem registrar senha real** e sem depender de o modelo inferir variantes a partir de valores redigidos. A/B históricos são referências, não controles automaticamente repetidos na mesma sessão.
- [ ] Avaliar status, Content-Type, mensagem, tamanho, redirecionamento e diferenças observáveis, ignorando `Date` volátil em comparações semânticas. Não afirmar que dois 401 provam segurança.
- [ ] Sem conta real, criação de conta, bypass, credential stuffing ou repetição. A conta descartável positiva está fora do 03B atual.

**Aceite P2:** fixture verifica uma ação por A, B e C; bloqueia email diferente, repetição, POST em caminho distinto, credencial real, JSON malformado, qualquer quarta variante; enumera A/B/C sem publicar campos de senha.

## P3 — INV-01B e histórico factual útil

- [ ] Preservar `agent.interpret_result` como **interpretação de um único resultado**. Não falsificar o que esse passo viu. Melhorar **somente o contexto de decisão seguinte**, fornecendo um **resumo factual compacto, determinístico**, extraído dos eventos verdadeiros da sessão.
- [ ] O resumo deve carregar no mínimo: `result_id`, ferramenta, método/caminho, status ou porta, flag de truncamento, distinção “observado vs alegado pelo Qwen” e a avaliação humana prévia; nunca concluir versão/rota sem resultado.
- [ ] Não injetar comandos obrigatórios, endpoints fixos nem conclusão inventada na mensagem do sistema; o Qwen segue escolhendo a próxima ferramenta. Guard de rotas permanece fechado, com rejeição e justificativa para candidatas não autorizadas.
- [ ] Testar regressão de contexto contra os erros históricos: “HTML completo” apesar de `truncated=true`, Nmap `SERVICE=ppp` sem `-sV`, afirmação de comparação com controles não executados.
- [ ] Se o Qwen insistir em proposição inválida, registrar a limitação, interromper por limite ou revisar plano; **não** permitir execução fora de escopo para produzir uma “adaptação”.

**Aceite P3:** fixtures com resultados e IDs preservados; o contexto enviado contém fatos reais úteis e continua dentro do orçamento; propostas novas realmente dependem de saídas observadas, sem uma sequência pré-fixada pelo código; modo original não muda comportamento sem opt-in.

## P4 — Logs, testes, síntese e documentação

- [ ] Criar/estender testes unitários e de integração **simulada**, explicitamente rotulados, para P0–P3; sem consultar o Juice Shop, Ollama, Kali ou usar Docker real nos testes por padrão.
- [ ] Cobrir: autorização real ausente, mudança de hash do plano, logs anteriores intocados, escopo, allowlist, mudança da identidade do container, rollback/cancelamento de restauração, A/B/C não repetidos, extensão e existência não confundidas, truncamento, resultado 403 vs 423/429, redirecionamento, segredos e mudanças de contexto.
- [ ] Rodar `python3 -m unittest discover -s tests -v`, `python3 -m py_compile agent.py scripts/af_session.py scripts/af_delegated.py scripts/af_summarize.py` e `sh -n` para scripts shell alterados; verificar `git diff --check`. Se a suíte exigir interfaces novas, ajustar testes sem enfraquecer asserts de segurança.
- [ ] Criar síntese 03B comparando baseline + controles complementares por `run_id/result_id`, **sem promover conclusões automaticamente**. Atualizar `CHECKLIST_RUBRICA.md` com estado 03B somente após teste/execução reais, usando evidências etiquetadas.
- [ ] Documentar uso novo em `docs/OPERACAO_BLOCO03B.md`: comandos reais somente depois de implementados e testados, confirmação de plano e rede, alterações no desenho experimental, procedimento de cancelamento.
- [ ] Registrar saída de testes, limites e alterações em `docs/STATE.md`; nada de atualizar `docs/RELATORIO_ACADEMICO_RASCUNHO.md` com “resultado 03B” antes de executar e revisar.
- [ ] Commit/push apenas **código e documentação sem segredos** na branch de desenvolvimento criada para a task, com merge sujeito à revisão; jamais merge automático da branch `evidencias/logs-completos-2026-10-27`.

## P5 — Execuções 03B (OUTRO PEDIDO, NÃO AUTORIZADO NESTA TASK)

- [ ] Grupo revisou e aprovou o adendo, assinatura/referência real; evidência recente de conexão e isolamento suficiente no caminho de rede.
- [ ] Responsável concedeu autorização separada para restaurar o container descartável do Juice Shop (destrutivo); nenhum outro serviço será alterado.
- [ ] Em terminal supervisionado, executar **uma sessão por cenário**, com decisões pessoais reais e justificativas; coletar `run_id/result_id` e produzir síntese revisável.
- [ ] Revisar logs, redigir dados sensíveis e comparar o original com 03B; só então preparar capturas/relatório/vídeo.

## Não fazer / guardrails de qualidade

**Não** (1) editar passado, (2) fabricar resultado, aprovação, divergência ou adaptação, (3) tratar “Codex delegado” como “Nicholas aprovou”, (4) usar modelo como testador fora do escopo, (5) tornar `/ftp/` recursivo/arbitrário, (6) incluir vulnerabilidades novas sem plano/consentimento, (7) aumentar limite de propostas apenas para coletar “mais logs”, (8) apagar container sem identidade e consentimento, (9) instalar dependências desnecessárias, (10) alterar WAN/pfSense/WordPress/Nextcloud.

## Definition of Done para a próxima sessão Codex

O Codex só deve declarar **“IMPLEMENTAÇÃO PRONTA PARA REVISÃO”** se:
1. P0–P4 atendidos com testes demonstrados, arquivos e commits citados.
2. Modo antigo segue compatível e testes antigos passam.
3. Todos os novos testes de segurança exigem **aprovação humana real** no caminho acadêmico.
4. Nenhuma execução real do 03B foi feita sem autorização subsequente.
5. Relatório de handoff lista explicitamente o que está completo, pendente, não testado e quais comandos serão usados **após** autorização.

A conclusão **“experimentos concluídos”** exige P5, que não faz parte desta autorização de programação.
