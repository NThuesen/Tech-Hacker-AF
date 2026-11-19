# Matriz comparativa — investigações históricas e 03B

**Estado:** preparada para coleta; as três investigações 03B ainda não foram executadas. Os IDs abaixo correspondem ao Bloco 03 histórico, cujas decisões por ação foram **delegadas ao Codex**, não a decisões humanas das futuras sessões 03B. Fontes primárias permanecem privadas.

| Cenário | Observação histórica | `result_id` histórico | Nova sessão 03B |
|---|---|---|---|
| INV-01 — reconhecimento | HTTP 200 no endpoint de versão, versão 17.3.0; TCP/3000 aberta | `fe55f482885f488fa472d5f7321970c5`; `45ea687333f0430ea1b19a9d28072980` | **PENDENTE:** observações, IDs, supervisor e interpretação |
| INV-02 — autenticação | As variantes de senha vazia e inválida retornaram HTTP 401 e corpos iguais, no escopo testado | `c3a3deedc7924c769c1a4635c1cdf47f`; `e32b00e3c32744fb82587a270a5c80d2` | **PENDENTE:** A/B/C efetivamente propostos, decisões, resultados e IDs; ausência de execução não é resultado |
| INV-03 — recursos | `/ftp/` retornou HTTP 200 com listagem; o controle inexistente `.txt` retornou 403 | `41ee9e9701f34ace8b340e8327aca1ec`; `ec76542988d04dafa7e046553aa2640b` | **PENDENTE:** confirmação de listagem e controle `.md`, se proposto e autorizado, com IDs e limites |

O `.txt` histórico não isolou existência da restrição de extensão. HTTP 200, HTTP 401 idêntico ou HTTP 403, isoladamente, não demonstram vulnerabilidade, bypass ou segurança geral. Uma proposta do modelo é hipótese, não resultado.

Os testes de rede de 19/11 foram **relatados por Nicholas** e estão em [evidências de rede](EVIDENCIAS_REDE_2026-11-19.md); os arquivos primários e capturas atuais de regras ainda não foram disponibilizados ao Codex. Cada futura linha 03B deve conter `run_id`, `proposal_id`, `execution_id`, `result_id`, nome real do supervisor, decisão, observação, interpretação e pendência, sem expor dados sensíveis.
