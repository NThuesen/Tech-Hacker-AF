# INV-03 — exposição e acesso a recursos HTTP

Responsável acadêmico: Nicholas. Operador/revisor: Codex delegado por autorização explícita; autorização do professor relatada por Nicholas, sem verificação independente. Decisões delegadas não são humanas. Execução técnica encerrada diante de restrição; revisão acadêmica do grupo PENDENTE.

Sessão: `6e1489236a7b49e1ac57abcfccdc8347`, 27/10/2026. Qwen3 `4b-instruct` local; somente Juice Shop 17.3.0 em `127.0.0.1:3000`. Identidade do container verificada, restauração comprovada antes do cenário e plano conferido por hash. Evidências completas e limitadas conforme o programa em `logs/INV-03/6e1489236a7b49e1ac57abcfccdc8347/`, fora do Git.

## Hipótese e estratégia

H3: verificar se recurso relacionado a arquivos expõe listagem pública e comparar resposta a caminho inexistente, sem confundir acessibilidade com acesso indevido, LFI ou RFI. Plano: referência `/`, candidato `/ftp/`, negativo `/ftp/arquivo-inexistente-af.txt`; um documento público não sensível seria opcional, condicionado a nome observado e aprovação. Risco principal: coletar conteúdo privado; não houve download de documentos.

## Execução e intervenções

O Qwen escolheu três GETs: `/`, `/ftp/`, arquivo inexistente do plano. Três propostas aprovadas, três resultados e interpretações. A ordem coincidiu com os candidatos do plano neste caso; foi escolhida pelo Qwen no ciclo de evidências/revisão, sem respostas fixas no runner.

1. `/`: HTTP 200, título OWASP Juice Shop, Content-Length 80117, corpo truncado no log a 16384 bytes. O revisor registrou a truncagem omitida na limitação do modelo.
2. `/ftp/`: HTTP 200, Content-Length 11078, sem truncagem no log. Título `listing directory /ftp/` e links comprovam listagem pública de nomes via HTTP. O contexto enviado ao modelo foi limitado a prefixo de até 2048 bytes; o revisor conferiu o corpo registrado. Nenhum arquivo listado foi baixado.
3. `/ftp/arquivo-inexistente-af.txt`: HTTP 403, corpo sem truncagem, com mensagem `Only .md and .pdf files are allowed!`. Encerramento diante da restrição, sem tentativa de contornar o bloqueio.

O Qwen declarou que o conteúdo da listagem não era sensível. O revisor corrigiu: nomes podem indicar arquivos privados e não permitem avaliar seu conteúdo. O modelo também chamou o caminho de diretório FTP; nenhum protocolo FTP foi testado, apenas HTTP. Na resposta 403, associou a mensagem à extensão, mas extrapolou para autorização/acesso a arquivo inexistente. O revisor separou essas afirmações.

## Limitação do próprio planejamento

O controle negativo `.txt` mistura duas variáveis: existência e extensão permitida. O 403 observado sustenta uma restrição compatível com o filtro de extensão descrito na mensagem; não comprova o tratamento de ausência nem controle por usuário. Um controle com extensão permitida exigiria novo teste deliberado, que não foi executado após a restrição. Documento opcional também não foi coletado, por desnecessidade e risco de conteúdo privado.

## Conclusão proporcional

H3 parcialmente sustentada: listagem HTTP pública demonstrada. Tratamento de arquivo ausente e controles de todos os documentos permanecem inconclusivos. Não foram demonstrados acesso indevido, ausência de autenticação em todos os arquivos, LFI/RFI ou conteúdo secreto. Um 403 no controle não prova segurança geral. A restrição observada encerrou a execução.

## Matriz de resultados

| Caminho | result_id | Evidência |
|---|---|---|
| `/` | `3fa447a6491141bfa8b20b7390563d19` | HTTP 200, HTML truncado |
| `/ftp/` | `41ee9e9701f34ace8b340e8327aca1ec` | HTTP 200, listagem pública de nomes |
| `/ftp/arquivo-inexistente-af.txt` | `ec76542988d04dafa7e046553aa2640b` | HTTP 403, restrição .md/.pdf |

Timestamps, parâmetros e vínculos completos por event_id/proposal_id/execution_id/result_id estão no JSONL e no resumo privados. Revisão/conclusão acadêmica humana ainda pendente.
