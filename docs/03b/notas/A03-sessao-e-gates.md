# A03 — Sessão 03B e portões verificáveis (P0)

**Pergunta única:** como iniciar um 03B válido sem confundir aprovação humana e decisão de código?
**Dependência:** [A01](A01-limites-e-autoria.md), [A02](A02-inventario-do-codigo.md). **Estado:** ainda não implementado.

## Entrada e metadados

- Modo 03B **opt-in**, aceitando somente `INV-01-B`, `INV-02-B`, `INV-03-B`. Para compatibilidade interna, o `investigation_id` antigo segue `INV-01/02/03`, mas adicionar `phase=03B`, `scenario`, `run_id` único.
- Fixar no preflight `plan_original_sha256`, `plan_v2_sha256`, commit de código, digest do modelo, identidade/digest do container, bindings e `origem_decisao`. Guardar logs em `logs/03B/INV-0N/<run_id>/` com permissões 0700/0600. Não deixar logs entrarem no Git.
- Aprovação do plano v2 exige integrantes e deliberação/data reais, hash efetivo e confirmação digitada pelo humano **na sessão live**. Se arquivo aprovado mudou, abortar. Se professor exigir revisão do plano posterior ao LLM, registrar condição real; não preencher com texto padrão.
- Revalidar Kali/VPN e evidência de isolamento WAN **do caminho autorizado**. Se pendente, bloquear operação real; timeout anterior isolado não é garantia de toda a WAN.
- Validar imagem, ID, volumes, bindings, Docker Rootless e serviços antes da restauração. Pedir consentimento separado para perder estado descartável de `kit11-juice`; identidade nova após restauração e HTTP 200 do alvo são evidência de preflight, não ação do Qwen.

## Fluxo por ação

1. Qwen recebe objetivo+histórico observado e emite uma proposta válida.
2. Guardas validam escopo e plano; estudante aprova/modifica/rejeita ou encerra, com motivo não vazio. Ação modificada passa por validação e **segunda confirmação** antes da execução.
3. Registrar autorização durável e IDs **antes** do efeito. Executar uma ferramenta permitida; logar resposta limitada e erro/truncamento.
4. Qwen interpreta o resultado vinculado a `result_id`; humano avalia e decide continuar/parar com justificativa; se continuar, próximo prompt usa evidências anteriores. Máximo seis propostas por investigação.
5. Falha de log, alteração de identidade, redirecionamento externo, segredo, HTTP 423/429, repetição indevida ou risco -> parada segura com evento explícito.

## Critérios de aceite com fixtures

- Plano v2 ausente/alterado/sem aprovação, rede `PENDENTE`, identidade divergente ou restauração não confirmada -> `EXECUÇÃO BLOQUEADA` e nenhuma ferramenta.
- Ação rejeitada, alterada não reconfirmada, truncagem, interrupção Ctrl+C, timeout do Ollama ou falha de gravação preservam auditoria sem inventar conclusão.
- Metadados aparecem em toda sessão 03B; sessão legada mantém contrato anterior; diretórios e arquivos de log têm permissões privadas.

**Próximo:** [A04 — controles dos três cenários](A04-controles-por-cenario.md).
