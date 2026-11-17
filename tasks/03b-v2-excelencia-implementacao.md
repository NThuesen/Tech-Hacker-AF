# Task 03B v2 — Implementação do experimento de decisão e evidência

**Estado:** ESPECIFICAÇÃO NÃO IMPLEMENTADA. **Um único bloco:** ampliação do 03B original, não início de Bloco 04 nem quarto cenário.
**Ler antes:** `AGENTS.md`, `docs/INDEX.md`, `docs/STATE.md`, `PLANS.md`, `docs/AF - Tecnologias Hackers 26-2.pdf`, `plano_humano.md`, `docs/PLANO_REFINAMENTO_BLOCO03B.md`, **`docs/PLANO_03B_EXCELENCIA_V2.md`**, `docs/investigacoes/ANALISE_BLOCO03.md`.
**Baseline de código:** `agent.py`, `scripts/af_session.py`, `scripts/af_delegated.py`, `scripts/af_summarize.py`, `scripts/lab_common.sh`, `scripts/restore.sh` e `tests/` como estão na branch escolhida. Verificar divergência do KIT11 antes de tocar no código.

## Trabalho proposto por prioridade — cada item tem teste de aceite

**Orquestração para o Codex:** a rota principal é [`docs/03b/INDEX.md`](../docs/03b/INDEX.md). Implemente **todos os itens P0–P5** sem deixar integração, testes ou documentação para Nicholas; as notas A01/A02 definem regras/interfaces e A03–A09 definem cada entrega. Use **uma nota por vez**, lendo arquivos de implementação reais. A10/P6 só documenta o que exige autorização humana posterior. Sem branch nova automática ou publicação de código sem confirmação.


### P0. Reconciliação, versionamento e separação de modos

- [ ] Verificar `git status`, upstream, código local mais novo e estado do KIT11; recusar sobrescrita de alterações não publicadas. **Não criar branch automaticamente**; qualquer publicação futura de código exige autorização de Nicholas.
- [ ] Preservar `plano_humano.md`, branch histórica de logs, INV-01/02/03, modo de execução delegado antigo e API atual de `agent.py`; novo modo precisa opt-in inequívoco.
- [ ] Guardar hash do plano 03B anterior e v2 aprovado com nomes/data reais e fazer o preflight validar que não mudou. Nenhuma string `APROVADO` ou data pré-preenchida em produção.
- [ ] Metadados: `phase=03B`, `scenario=INV-0N-B`, `run_id`, `plan_v2_sha256`, `code_commit`, `model_digest`, `origem_decisao`, `trial_type=real|replay_fixture|replay_real_context`.
- [ ] Modo acadêmico não aceita entrada injetada de teste nem revisor Codex como se fosse entrada humana. Injeção só em testes unitários claramente rotulados.

**Aceite:** testes demonstram que execução real sem aprovação/sem WAN validada/sem restauração confirmada aborta; histórico original intocado; origem de decisão correta; regressão anterior PASS.

### P1. Controles experimentais revisados (INV-01B/02B/03B)

- [ ] INV-01B: objetivo neutro, Nmap apenas TCP/3000, GET em rotas pequenas já autorizadas. Não hardcodear próxima ferramenta por resposta; model decides, guard valida. Registrar `known_candidates` separadamente de `discovered_by_model` para não exagerar originalidade.
- [ ] INV-02B: email `.invalid` fixo; senha inválida/vazia/omitida; um POST por variante, nenhuma quarta variante, tentativa repetida ou conta real. Resultado vinculado a `variant` e não à senha visível.
- [ ] INV-03B: permitir somente GET `/`, `/ftp/`, os dois caminhos inexistentes `.txt`/`.md` e positivo público condicionado do plano. Negativo `.md` depende de listagem **não truncada da mesma sessão** e verificação de nome ausente; se nome constar, bloquear e pedir deliberação.
- [ ] Interpretar 403 por extensão, 404/200 ou falha como observação; não inferir status futuro. HTTP 423/429, conteúdo sensível, redirecionamento externo ou falha de identidade exigem parada.

**Aceite:** fixtures A/B/C, listagem ausente/presente/truncada, arquivo proibido e histórico separado; nenhuma rede real. Propostas não permitidas não chegam a `agent.execute`.

### P2. Ledger factual com limites de contexto (não é outro agente)

- [ ] Helper stdlib que extrai até oito registros relevantes de resultados reais, mantendo `result_id`, `action`, resposta essencial, `truncated`, origem e avaliação/revisão humana; nenhuma conclusão de segurança gerada automaticamente.
- [ ] Separar saída da ferramenta, alegação do LLM, comentário do revisor e estado não testado. Não promover versão, rota ou comparação não observada.
- [ ] Opt-in da apresentação compacta ao Qwen **na proposta seguinte**; a interpretação atual continua restrita ao `result_id` da rodada. Mesmos limites existentes (`MAX_CONTEXT_BYTES`, `MAX_BODY`, timeouts); instrumentar bytes usados e eventual eliminação de registros antigos.
- [ ] Disponibilizar versão A (histórico atual) e B (ledger factual) para comparação controlada; o primeiro modo acadêmico histórico permanece padrão.

**Aceite:** testes com HTML 80117 vs truncado, serviço `ppp` sem `-sV`, duas respostas de login ainda não realizadas, avaliação humana verdadeira e histórica. Ledger B não introduz fatos ausentes em A sem marcar diferença de disponibilidade.

### P3. Replay e avaliação local isolados do executor

- [ ] CLI `scripts/af_replay.py` com **validação offline/dry-run como padrão**. Nenhum `import` nem chamada indireta que execute Nmap, HTTP ao Juice Shop, Docker, restore ou qualquer rede além de Ollama local no modo explicitamente autorizado.
- [ ] Arquivos de casos fora de `logs/` (fixtures) contendo objetivo, instruções, evidência com fonte (`result_id` real ou `simulado=true`), braços A/B, justificativa esperada de escopo e orçamento. **Fixtures sintéticas não podem aparentar logs reais.**
- [ ] Para executar o modelo local mais tarde, opção inequívoca de opt-in, confirmação humana e `model_digest`/config. Parâmetros iguais entre braços (temperatura=0, think=false, num_ctx e num_predict existentes); capturar envelope bruto/redigido, `done`, tokens e tempos Ollama.
- [ ] Até três pares de sensibilidade, três pares de memória e um controle de estabilidade com entrada idêntica repetida (até **14 propostas**). Preservar respostas inclusive se iguais ou incorretas. Propostas do replay **nunca** são executadas em ferramenta. Contemplar parada como decisão legítima se representável sem quebrar contrato histórico; se impossível, medir somente a recomendação e declarar a limitação.

**Aceite:** teste com monkeypatch de `agent.execute`, subprocess, HTTPConnection e restore que falha se chamados durante replay; fixture com instrução de alterar alvo dentro de HTML simuladamente retornado não atravessa a guarda; sem acesso a `11434` nos testes normais; confirmação obrigatória quando replay Ollama estiver habilitado; N/A explícito quando telemetria ausente.

### P4. Avaliação quantitativa sem falsear semântica

- [ ] Parser de eventos e relatório Markdown/CSV para contagens objetivas: propostas/JSON válidos, escopo, decisões, ações e interrupções; segregação `real`, `replay_real_context`, `replay_fixture`.
- [ ] Folha de avaliação humana com uma linha por alegação (`claim_id`, texto, `result_id`, classe 0–3, justificativa, avaliador e data). O software **não** decide se uma conclusão de vulnerabilidade é correta.
- [ ] Métricas apenas com `numerador/denominador`, sem percentuais sem N. Verificação de integridade dos vínculos `proposal_id → execution_id → result_id` e manifesto SHA256 de artefatos privados, sem publicar dumps.
- [ ] Comparar A/B do contexto apenas quando diferenças de conteúdo/snapshot estiverem documentadas; indicar confusão por prompt e sem significância com N reduzido.

**Aceite:** fixtures de denominador zero, sessão interrompida, resultado sem interpretação, duplicação de variante e evidência não disponível; export não publica senha/segredo nem classifica simulado como real.

### P5. Operação documentada, retrocompatibilidade e revisão de segurança

- [ ] Instruções `docs/OPERACAO_BLOCO03B_V2.md` com dois fluxos separados: `replay` (sem ferramenta) e `live` (porta/restauração/human gates). Não inventar comandos antes de confirmar nomes da CLI implementada.
- [ ] README/STATE/CHECKLIST e handoff atualizados **sem declarar testes novos concluídos**. Relatório/vídeo devem continuar históricos até coleta verdadeira de dados 03B.
- [ ] `python3 -m unittest discover -s tests -v`; `python3 -m py_compile` em todos os módulos novos/alterados; `sh -n` nos shells; `git diff --check`; evidenciar PASS/FAIL/SKIP verdadeiros. Foco em semântica e segurança, não no número bruto de testes.
- [ ] Conferir allowlists, falhas de log, permissões privadas e redirecionamento antes de pedir merge. Não instalar novos frameworks nem serviço adicional.

**Aceite:** código + fixtures prontos para revisão e demonstravelmente incapazes de executar ações de laboratório sem os portões; instrução de como reverter opt-in para o modo histórico.

### P6. Execução real, auditoria do grupo e entrega — NÃO AUTORIZADAS NESTA TASK

- [ ] Aprovação escrita/data/hash do adendo v2 pelo grupo, critérios de autoria/revisão aceitos pelo professor se necessário.
- [ ] Comprovação atual do laboratório, identidade, Kali/VPN e isolamento de WAN no escopo. Se WAN seguir pendente, abortar operações reais.
- [ ] Consentimento específico para restauração de `kit11-juice`; uma investigação por vez e com decisão humana antes de cada ferramenta.
- [ ] Autorização distinta antes do **replay com Ollama real** (sem tocar no Juice Shop).
- [ ] Rastrear novas decisões e resultados ao vivo, comparar com logs originais sem sobrescrever, revisão humana de alegações e conclusão.
- [ ] Só após evidências reais: relatório final 4–6 páginas, vídeo até 10 minutos e checklist de submissão.

## Dever de honestidade científica

Não inventar falhas, aprovação humana, adaptações, execução em Kali, resultados numéricos ou sucesso de controles. Um resultado sem mudança entre as condições é relevante; uma hipótese não confirmada é resultado válido. O professor avalia **método, evidência e pensamento crítico**, não volume de ataques.

**Definição de pronto do Codex:** P0–P5 implementados e validados com fixtures, P6 explicitamente PENDENTE; entregar arquivos, testes/contagens reais, desvio da primeira proposta 03B, ameaças à validade e nenhum serviço/rede/container alterado.
