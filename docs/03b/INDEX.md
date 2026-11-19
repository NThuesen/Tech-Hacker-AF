# Bloco 03B v2 — índice operacional de notas atômicas para o Codex

**Estado atual:** P0–P5 implementados com fixtures; detalhes e limites em [operação](../OPERACAO_BLOCO03B_V2.md) e [estado](../STATE.md). As notas abaixo preservam a especificação histórica; P6 não foi executado nesta etapa.

## Objetivo do Codex desenvolvedor

Implementar **integralmente P0–P5**, incluindo programação, testes simulados, documentação operacional, métricas e validação de regressão. O estudante **não precisa conduzir a programação passo a passo**. O Codex deve escolher detalhes mecânicos, executar testes seguros, corrigir defeitos e registrar decisões técnicas; somente pedir autorização quando uma ação mudar permissões, serviços, dados, rede, escopo ou publicar código. **P6 (investigações reais) não faz parte da autorização de programação** e exige supervisão humana por ferramenta.

Há **um único agente acadêmico**: Qwen3 4B local via Ollama. O Codex é o **desenvolvedor**, não uma segunda IA acadêmica nem um substituto das decisões humanas. Não trocar o modelo, adicionar multiagentes ou acessar alvos externos.

## Ordem de leitura econômica (um contexto por vez)

1. Antes de agir: `AGENTS.md` → `docs/STATE.md` → este índice → [A01 — limites](notas/A01-limites-e-autoria.md) → [A02 — código real](notas/A02-inventario-do-codigo.md). Consulte PDF da AF se houver conflito; `plano_humano.md` é histórico imutável.
2. Para cada implementação: leia **somente a nota correspondente**, os arquivos de código que ela cita e seus testes. Não copie todos os documentos para o prompt.
3. Após cada entrega: testes de fixtures, regressão, resumo técnico e próximo passo. Prossiga automaticamente P0→P5, salvo bloqueio real. P6 fica pendente.

| Ordem | Nota atômica | Entrega verificável |
|---:|---|---|
| P0 | [A03 — sessão e gates](notas/A03-sessao-e-gates.md) | modo 03B opt-in, hashes, origem humana, metadados e preflight |
| P1 | [A04 — controles HTTP](notas/A04-controles-por-cenario.md) | três investigações preservadas; A/B/C e `.md` sob guarda |
| P2 | [A05 — ledger factual](notas/A05-ledger-factual.md) | histórico determinístico com IDs, truncagem e origem |
| P3 | [A06 — replay isolado](notas/A06-replay-isolado.md) | comparação controlada sem nenhuma ferramenta ofensiva |
| P4 | [A07 — métricas](notas/A07-metricas-e-aval-humana.md) | métricas com denominadores + formulário humano, sem juiz-LLM |
| P5 | [A08 — verificação](notas/A08-testes-e-qualidade.md) e [A09 — operação](notas/A09-operacao-e-entregas.md) | suíte completa, guia de operação, documentação atualizada |
| Fora do escopo atual | [A10 — gates da execução real](notas/A10-execucao-real-pendente.md) | **somente preparo do protocolo**; nenhuma execução nova |

**A01 e A02 são referências obrigatórias** que governam todas as etapas. Cada nota define um único problema, contrato, aceite e limites; evite repetir parâmetros em outros lugares. A planilha ampla [Plano científico v2](../PLANO_03B_EXCELENCIA_V2.md) estabelece as perguntas de pesquisa; [task P0–P6](../../tasks/03b-v2-excelencia-implementacao.md) é o backlog agregado; este índice é a rota canônica de implementação.

## Contrato de autonomia e término

- O Codex **faz toda a programação P0–P5** e todos os testes **com mocks/fixtures** em Python stdlib. Não espere uma aprovação humana a cada arquivo, teste ou refatoração reversível; documente decisões técnicas relevantes.
- Preserve modos e arquivos originais; mantenha mudanças pequenas, com testes, e pare diante de divergência do checkout KIT11 ou evidência de risco a outros serviços.
- Não criar branch automaticamente; Nicholas prefere `main`. **Documentação já foi publicada na `main`, mas a publicação de código requer autorização própria** conforme `AGENTS.md`.
- Nada de Ollama real, Nmap real, HTTP ao Juice Shop, Docker, Kali, restauração ou rede na fase P0–P5. O replay deve ter modo `dry-run` que não chama sequer Ollama.
- Entregar: arquivos alterados, justificativas, testes PASS/FAIL/SKIP, validação de escopo e segurança, pendências reais e instrução de operação futura. Marcar `IMPLEMENTADO COM FIXTURES`, nunca `INVESTIGAÇÃO EXECUTADA`, enquanto P6 não ocorrer.

## Fonte de verdade e antirrepetição

1. AF original > `AGENTS.md`/aprovação humana > logs reais > plano v2 > estas notas > proposta 03B v1. Em conflito, interromper e reportar.
2. Segurança e autoria: **A01**. Interfaces realmente existentes: **A02**. Validações: **A03/A04**. Formato do ledger: **A05**. Replays: **A06**. Métricas: **A07**. Testes: **A08**. Operação: **A09**. Execução real: **A10**.
3. Evidência não é conclusão: eventos `run_id/result_id` são primários; inferências ficam associadas a avaliações humanas. Mock não é resultado real. A v1 e logs originais não devem ser reescritos.
