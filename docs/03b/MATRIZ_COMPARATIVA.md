# Matriz comparativa — investigações históricas e 03B

**Estado:** três sessões 03B executadas; INV-03-B inconclusiva quanto ao controle `.md`. No histórico, as decisões foram **delegadas ao Codex**. Na INV-01-B, Nicholas decidiu pessoalmente; nas INV-02-B e INV-03-B, as decisões e conclusões foram **delegadas ao Codex**, conforme autorização informada por Nicholas. Fontes primárias permanecem privadas.

| Cenário | Observação histórica | `result_id` histórico | Nova sessão 03B |
|---|---|---|---|
| INV-01 — reconhecimento | HTTP 200 no endpoint de versão, versão 17.3.0; TCP/3000 aberta | `fe55f482885f488fa472d5f7321970c5`; `45ea687333f0430ea1b19a9d28072980` | Run `f0e74216eeba4a3780b1eb41c48695ca`: supervisor Nicholas aprovou três GETs; `/` 200 truncado (`bc005ded0ee84d6ca164b2259139dbac`), versão 17.3.0/200 (`196ea749f7e346fc833626ed96f5a6f7`), produto público/200 (`946ca4860a744b35b47224e73b24ee53`). Nmap não foi executado nesta sessão. |
| INV-02 — autenticação | As variantes de senha vazia e inválida retornaram HTTP 401 e corpos iguais, no escopo testado | `c3a3deedc7924c769c1a4635c1cdf47f`; `e32b00e3c32744fb82587a270a5c80d2` | Run `fe9737b23e8a4f37bb38b4e0fafd0c98`: A/B/C 401, corpos iguais de 26 bytes (`52511329785c40bcba57957a0adf2bc3`, `c7e8f6eae808423e9888228dd7a430e9`, `6f1c957e63c14694a602acd457805214`). A veio do Qwen; B/C foram modificações delegadas após repetição. |
| INV-03 — recursos | `/ftp/` retornou HTTP 200 com listagem; o controle inexistente `.txt` retornou 403 | `41ee9e9701f34ace8b340e8327aca1ec`; `ec76542988d04dafa7e046553aa2640b` | Run `7c9c7dd8d01640dbb42c7ad6dda644d1`: GET `/ftp/` 200 (`ea5956fd5bba44c2b63252f1cdcc5a81`), mas 11025 bytes registrados frente a Content-Length 11079; completude não comprovada. `.txt` 403 (`fe67f70cf27d43a2a8a35a4f6ae73d39`); `.md` não executado. Decisões delegadas ao Codex. |

O `.txt` histórico não isolou existência da restrição de extensão. HTTP 200, HTTP 401 idêntico ou HTTP 403, isoladamente, não demonstram vulnerabilidade, bypass ou segurança geral. Uma proposta do modelo é hipótese, não resultado.

Os testes de rede de 19/11 e a inspeção visual foram **relatados por Nicholas** e estão em [evidências de rede](EVIDENCIAS_REDE_2026-11-19.md); os arquivos primários e capturas atuais de regras ainda não foram disponibilizados ao Codex. Os JSONL privados contêm `proposal_id`, `execution_id`, decisões e interpretações; checagem estrutural não valida correção semântica. A diferença de tamanho da listagem indica que sua completude não foi comprovada; não se identifica a causa apenas por esse registro.

## Tentativa adicional INV-03-B

Run `4463d8c1bcfb43bba4dc81292e4d20fb`: após restauração adicional autorizada, `/` respondeu 200 com limite de leitura; `/ftp/` respondeu 200 (`fe4d96fb080c41418344f764c34a0ec6`), com 11025 bytes recebidos contra 11079 declarados e `truncated=true`. O Codex encerrou sem executar o controle `.md`: não foi comprovado que a listagem estava completa. Não se estabeleceu a causa da diferença; o Qwen afirmou completude em contradição com o próprio indicador e aludiu a resposta `.md` inexistente. Revisões e conclusão foram delegadas ao Codex. Auditoria estrutural: 29 eventos, nenhuma lacuna.
