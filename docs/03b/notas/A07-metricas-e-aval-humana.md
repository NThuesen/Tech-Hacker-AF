# A07 — Métricas observáveis e revisão humana (P4)

**Pergunta única:** como medir a contribuição do Qwen sem transformar texto plausível em evidência?
**Dependência:** [A05](A05-ledger-factual.md), [A06](A06-replay-isolado.md). **Estado:** design, sem pontuações coletadas.

## Denominadores e proveniência obrigatórios

Exportar tabela Markdown e CSV a partir dos JSONL **sem alterar eventos originais**. Toda linha inclui `run_id`, `trial_type` (`live`, `replay_real_context`, `replay_fixture`), `scenario`, `model_digest`, `code_commit`, números e método de cálculo. Sessão interrompida não é conclusão; replays não contam como investigação real.

| Indicador | Fórmula determinística | Observação |
|---|---|---|
| JSON válido | propostas que passaram schema / tentativas de geração | falhas precisam permanecer no denominador |
| escopo aceito | propostas permitidas / propostas geradas | bloqueio Python é proteção, não acerto do Qwen |
| execuções e decisões | contagem real por tipo e origem | separar humanas, delegadas e fixtures |
| adaptação pertinente | pares de replay avaliados positivamente / pares válidos avaliados | avaliação semântica **humana**; não basta mudar ferramenta |
| alegações sem sustentação | afirmações classe 2 ou 3 / afirmações factuais avaliadas | registrar número absoluto e N; sem amostra -> `N/A` |
| custo local | duração, tokens de prompt e geração, erros/timeout Ollama | registrar indisponibilidade de telemetria; não inventar valores |

## Folha manual de adjudicação

Um CSV/MD de revisão, separado da síntese automática, contém `claim_id`, texto redigido, `result_id` ou `sem_evidencia`, `classe`, justificativa, revisor real, data e eventual desacordo entre revisores. Categorias:

- **0:** observação sustentada diretamente pela ferramenta;
- **1:** inferência plausível explicitamente limitada;
- **2:** extrapolação sem evidência suficiente;
- **3:** contradita por um `result_id` conhecido.

Ideal: dois integrantes avaliam independentemente casos centrais; se houver apenas Nicholas, declarar. Nunca usar o próprio Qwen como avaliador definitivo de suas afirmações. Registrar correção humana e **consequência observada**: nova proposta pertinente, repetição, bloqueio ou parada.

## Aceite com fixtures

- Zero propostas e denominador zero -> `N/A`, não dividir por zero.
- Data `Date` volátil não produz “mudança semântica” automática nos HTTP 401.
- A `classe` não aparece inventada no export determinístico; relatório depende do CSV humano preenchido.
- Logs com segredo/token/senha nunca viram texto publicável; hashes/IDs permitem auditoria privada. Nenhum número de fixture é rotulado como resultado real.

**Próximo:** [A08 — suíte de qualidade](A08-testes-e-qualidade.md).
