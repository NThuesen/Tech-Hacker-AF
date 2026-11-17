# A05 — Ledger factual e contexto controlado (P2)

**Pergunta única:** como dar memória confiável ao Qwen 4B sem inventar resultados nem aumentar permissões?
**Dependência:** [A02](A02-inventario-do-codigo.md), [A03](A03-sessao-e-gates.md). **Estado:** contrato para helper determinístico.

## Fonte e projeção dos dados

Ler somente eventos da **sessão atual**: proposta, ação final autorizada, `result_id`, ferramenta, método/caminho, status/porta, `truncated`, hash/limite do corpo, interpretação e avaliação do humano. Não converter frases do Qwen em fatos observados. O ledger é gerado por Python stdlib, não por outro LLM.

**Projeção sugerida (esquema, NÃO dado observado):**

```json
{
  "run_id": "<real quando existir>",
  "result_id": "<real quando existir>",
  "ferramenta": "http_get",
  "recurso": "/rota-permitida",
  "observado": {"status": 200, "truncated": true},
  "alegacao_modelo": "<citação redigida ou ausente>",
  "avaliacao_humana": "<registro exato ou ausente>",
  "nao_testado": ["<somente limitações sustentadas pelo registro>"]
}
```

Os valores acima são **ilustrativos**, não respostas do Juice Shop. Os campos `alegacao_modelo` e `avaliacao_humana` nunca são promovidos para `observado`; `nao_testado` não recebe inferência arbitrária. Preferir guardar referência/hash e tamanhos ao transmitir corpos; limitar contexto a até oito registros recentes e orçamento existente (até 16 KiB total, sem precisar ampliá-lo).

## Dois modos comparáveis

- **A — histórico original:** `agent.recent_history()` como está.
- **B — ledger factual:** mesmo conjunto de fatos, com IDs, truncagem, autoria e estados explicitados. Só afeta a **próxima proposta**: `agent.interpret_result()` continua restrita ao último resultado.
- Registrar `context_mode`, bytes/tokens disponíveis, `result_id` incluídos e registros omitidos por limite. Caso A não contenha fatos que B contém, declarar diferença de **disponibilidade** além da formatação.

## Aceite com fixtures

- Diante de HTML 80117 bytes mas corpo truncado, o ledger marca `truncated=true` e **não** afirma HTML integral.
- Diante de Nmap sem `-sV`, `ppp` é rótulo da tabela, **não** identificação de serviço.
- Após apenas uma tentativa de login, não existe fato “A e B são iguais”. Somente variantes efetivamente realizadas aparecem como observadas.
- Dados sigilosos não são enviados ao modelo nem para CSV; IDs continuam correlacionáveis; byte budget não é excedido; modo legado sem opt-in não muda.

**Próximo:** [A06 — replay controlado](A06-replay-isolado.md).
