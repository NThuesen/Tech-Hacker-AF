# INV-02 — autenticação e entradas inválidas

Responsável acadêmico: Nicholas. Operador/revisor: Codex delegado, por autorização explícita de Nicholas; autorização do professor relatada, sem verificação independente. Decisões e conclusão delegadas não são decisões humanas. Execução técnica encerrada; revisão acadêmica do grupo PENDENTE.

Sessão: `1ae38ffd4ed54a308ec9bd16c5017800`, 27/10/2026. Qwen3 `4b-instruct` local; alvo único `127.0.0.1:3000`, Juice Shop 17.3.0 identificado e restaurado antes da investigação. Logs JSONL, revisões, snapshot do plano e síntese privados em `logs/INV-02/1ae38ffd4ed54a308ec9bd16c5017800/`.

## Hipótese e plano

H2: comparar comportamento de entradas inválidas sem inferir bypass ou enumeração. Plano: POST `/rest/user/login`, email fictício fixo, A (texto de senha inválido), B (senha vazia), C opcional (campo omitido), uma vez cada; variar somente um campo. O objetivo fornecido ao modelo incluiu os controles permitidos, sem ordem obrigatória. Nenhuma conta real, SQL injection, força bruta ou login válido.

## Execução e intervenção

O Qwen escolheu B antes de A. Duas propostas aprovadas pelo revisor delegado, duas execuções e duas interpretações; nenhuma variante repetida. Nas duas respostas: HTTP 401, Content-Type `text/html; charset=utf-8`, corpo idêntico `Invalid email or password.`, 26 bytes, sem truncagem nem redirecionamento seguido. Não se afirmou igualdade de todos os cabeçalhos: Date variou.

Após B, o modelo afirmou que as variantes não diferiam antes de testar A ou C. O Codex registrou que havia somente uma observação e solicitou outra variante permitida. A proposta seguinte usou a senha inválida prevista em A, mantendo o identificador. Entretanto, hipótese e interpretação do Qwen descreveram o email como variável; a decisão revisou os parâmetros concretos e corrigiu a descrição. O email foi mantido igual; variou somente a senha.

Os campos de senha são redigidos no JSONL e no contexto do modelo; arquivos de revisão privados preservam os parâmetros de teste. Essa proteção também limita a interpretação do Qwen, razão para identificar explicitamente as variantes nas decisões. Não se tratam de credenciais reais.

## Conclusão proporcional

Não houve diferença observável entre A e B no status, tipo de conteúdo e corpo. A expectativa de respostas diferentes não foi sustentada nesses dois controles. C era opcional e não foi executada porque A×B já respondia à comparação principal. Não há evidência de bypass, enumeração, segurança geral da autenticação ou lógica interna de validação; faltam controle positivo e outros contextos para conclusões mais amplas. O comportamento igual não comprova ausência de vulnerabilidades.

## Matriz de resultados

| Variante | result_id | Resultado |
|---|---|---|
| B — senha vazia | `c3a3deedc7924c769c1a4635c1cdf47f` | HTTP 401, mensagem genérica, 26 bytes |
| A — senha inválida de teste | `e32b00e3c32744fb82587a270a5c80d2` | HTTP 401, mesmo corpo, 26 bytes |

IDs de propostas, decisões, execuções, interpretações e timestamps completos estão no JSONL e no resumo privados. Conclusão técnica pelo Codex; validação acadêmica pelo grupo/professor permanece pendente.
