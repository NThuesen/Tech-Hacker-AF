# Handoff para Codex — Implementação do Bloco 03B

**Estado em 29/10/2026:** somente especificação. Esta mensagem **não autoriza execução real de testes de segurança, restauração destrutiva, publicações de logs ou alterações de rede**. Objetivo: deixar o repositório pronto para uma sessão de programação orientada por evidências.

## Como iniciar, quando Nicholas solicitar a implementação

No Ubuntu KIT11 (quando disponível), a partir de `/home/kit11/Kit11-AF`:

```sh
git status --short
git fetch origin
git pull --ff-only origin main
git switch -c feature/af-bloco03b-refinamento
```

**Parar se a árvore não estiver limpa, `main` divergir, não houver acesso ao repositório ou a branch existir.** Não usar `git reset --hard`, `git clean -fd` nem forçar push. Não alterar a branch de evidências históricas. Se estiver trabalhando em checkout distinto, ajustar somente o caminho local após verificar.

Ler, nesta ordem:
1. `docs/RUBRIC.md` — critérios originais da AF.
2. `plano_humano.md` — planejamento original/histórico (imutável).
3. `docs/PLANO_REFINAMENTO_BLOCO03B.md` — plano complementar e limites.
4. `tasks/03b-refinamento-experimental.md` — backlog, P0–P4 e testes.
5. `docs/investigacoes/ANALISE_BLOCO03.md` e `docs/investigacoes/INV-0N/resumo.md` — falhas e limites observados.
6. `agent.py`, `scripts/af_session.py`, `scripts/af_delegated.py`, `scripts/af_summarize.py`, `scripts/lab_common.sh`, `scripts/restore.sh`, `tests/`.

## Instrução direta para Codex (copiar para a sessão de programação)

> Implemente **somente** o Bloco 03B descrito no repositório, respeitando `docs/PLANO_REFINAMENTO_BLOCO03B.md` e `tasks/03b-refinamento-experimental.md`. Faça mudanças mínimas e reversíveis. Priorize na ordem: (1) escopo/identificação/fluxo humano; (2) INV-03B com o controle inexistente `.md` e prova de ausência na listagem; (3) INV-02B com A/B/C uma vez cada; (4) INV-01B com contexto factual compacto para decisão; (5) logs, comparador, documentação e testes. Preserve o modo antigo, a imagem e os binds Docker Rootless, o plano original/hashes, os JSONL históricos, os limites de acesso e o controle explícito antes de cada ferramenta. Não simule aprovações humanas; testes com respostas simuladas devem estar rotulados como fixtures. Não executar Juice Shop, nmap real, consultas Ollama, restauração, Docker real, Kali, pfSense ou rede nesta rodada de programação. Não instalar dependências nem tocar outros serviços. Execute apenas testes locais simulados, compile/check de sintaxe, documente resultados verdadeiros; commit/push na branch `feature/af-bloco03b-refinamento` depois de validar e verificar arquivos alterados; não faça merge automático e não inicie o Bloco 04. Devolva: arquivos alterados, commits, contagens de testes, limitações, checklist P0–P4 e instruções de operação futura (não executadas).

## Matriz rápida do trabalho

| Ordem | Arquivos prováveis | Entrega técnica |
|---:|---|---|
| 1 | novo `scripts/af_refine.py` ou extensão pequena de `af_session.py` | modo 03B com confirmação do adendo, supervisão humana e `phase/scenario` |
| 2 | guard para INV-03B e respectivos testes | `.md` inexistente permitido apenas sob condições controladas; controle `.txt` comparado e rotas privadas bloqueadas |
| 3 | guarda de INV-02 e testes | A, B, C únicos, email fixo, sem credenciais reais |
| 4 | helper opcional em `agent.py` e testes | histórico factual com IDs para **próxima proposta**, sem dar respostas prontas |
| 5 | sumarização + `docs/OPERACAO_BLOCO03B.md` + testes | log privado, matriz baseline vs. 03B, guia de uso e pendências |

**Não introduzir suíte ampla de ferramentas, varredura de subrede, crawler livre, bypass de extensão, conta real ou gestão de cookies/tokens.**

## Proteções específicas a verificar antes de declarar pronto

- A guarda de **INV-03 original** não deve mudar nem passar a aceitar `.md` sem modo 03B. O código delegado anterior é histórico; não modificar seu papel para forçar conformidade acadêmica.
- O controle de `/ftp/arquivo-inexistente-af.md` só pode ocorrer quando a listagem `/ftp/` da **mesma sessão** foi obtida e analisada. Status do arquivo é hipótese, nunca constante embutida no teste.
- `POST` somente para os três corpos A/B/C permitidos em INV-02B, uma única vez por sessão, com validação antes de qualquer efeito.
- `agent.py` não deve ganhar capacidade de alterar `host`, porta ou executar shell arbitrário. A interpretação de um único resultado pode continuar isolada; o sumário do histórico deve ajudar somente a **proposta subsequente** e indicar fatos registrados, truncagem e IDs.
- Em modo acadêmico, `REDE VERIFICADA` e aprovação do adendo **não podem ser presumidos**, nem a restauração confirmada por pipe automático. Erro de confirmação aborta e gera log de falha sem declarar conclusão.
- Não declarar execução 03B em README, checklist, estado ou relatório antes de um `run_id` real com evidência. Use `PENDENTE`, `IMPLEMENTADO COM FIXTURES` e `NÃO EXECUTADO` conforme o caso.
- O sumário pode comparar sessões antigas por referência a paths/IDs, **nunca reescrever os arquivos antigos**. Não publicar logs brutos na main.
- Registrar data/versão da documentação, alterações de guard, testes PASS/SKIP e limitações no handoff.

## Critérios para solicitar uma nova autorização a Nicholas

Após finalizar código + fixtures, pedir orientação explícita **somente para o que ainda falta**: (a) validar aprovação real do plano complementar, (b) verificar laboratório/rede pós-reinício, (c) autorizar restauração destrutiva apenas do `kit11-juice`, (d) executar INV-03B → INV-02B → INV-01B com supervisão genuína, (e) revisar e exportar evidências para relatório/vídeo. Não solicitar a mesma informação repetidamente se já houver registro válido e atual.

## Resposta final que Codex deve fornecer

Um relatório curto com estado por P0–P4 (PASS/FAIL/PENDENTE), testes e comandos executados, branch/commits, arquivos alterados, garantias de que **nenhuma ação de rede ou container real foi feita**, e procedimento posterior para execuções com consentimento. Em caso de falha de segurança/regressão: **não fazer merge**, explicar bloqueio e deixar evidências do erro.
