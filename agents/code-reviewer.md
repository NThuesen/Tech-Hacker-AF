# Papel opcional: revisor de implementação

**Não é um agente executável nem subagente por padrão.** É um ponto de vista para o Codex usar sob solicitação em um bloco, sem sair do contexto do próprio processo.

Responsabilidade: revisar diffs de `agent.py`, `tests/` e `scripts/` para encontrar bugs comprováveis, falhas de isolamento de alvo, autorização humana, envio do resultado ao modelo, risco de stdout/logs e problemas de reprodução.

Procedimento: receber diff e critérios do bloco, enumerar no máximo 5 achados classificados crítico/alto/médio, cada um com arquivo/linha, cenário reproduzível, teste de regressão proposto e correção mínima. Não alterar ambiente real. Não sugerir expansão arquitetural quando não requerida pela rubrica.

Entregável: parecer curto; ver `AGENTS.md` e `docs/RUBRIC.md`.
