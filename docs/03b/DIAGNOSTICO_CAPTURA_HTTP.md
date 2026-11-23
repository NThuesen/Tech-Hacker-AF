# INV-03-B — diagnóstico de captura HTTP, 23/11/2026

## Evidência existente

| Registro | Content-Length | Bytes medidos pelo cliente antes da decodificação | Corpo UTF-8 registrado | Sinal histórico |
|---|---:|---:|---:|---|
| 27/10, `41ee9e9701f34ace8b340e8327aca1ec` | 11.078 | Indisponível | 11.024 | `truncated=false` |
| 19/11, `ea5956fd5bba44c2b63252f1cdcc5a81` | 11.079 | Indisponível | 11.025 | `truncated=false` |
| 19/11, `fe4d96fb080c41418344f764c34a0ec6` | 11.079 | 11.025 | 11.025 | `truncated=true` |
| Referência GET da raiz, `4da745f4c0c24bc4a69710f5f693bade` | 80.117 | 16.385 | 16.384 | Limite local atingido |

As três cópias da listagem são ASCII, sem caractere de substituição UTF-8, e terminam em `</html>`. A diferença de 54 bytes se repete. Na última, o contador bruto no cliente coincide com os bytes do texto registrado. O teto de 16 KiB, a decodificação UTF-8, a redação e o registro JSON não explicam essa diferença na última rodada. A comparação é feita com o corpo desserializado, sem contar escapes nem campos do JSONL.

O cabeçalho de tipo registrado indica HTML UTF-8. O código da época filtrava `Content-Encoding` e `Transfer-Encoding` dos logs. A ausência desses campos no registro deixa a codificação HTTP histórica sem confirmação. O cliente recebeu menos bytes do que o cabeçalho anunciado e a leitura retornou normalmente. Sem registro bruto do intercâmbio, não é possível distinguir comprimento informado incorretamente, transformação por componente intermediário ou encerramento antecipado da resposta. O padrão repetido e o fechamento HTML não provam nenhuma dessas causas.

## Correção testada sem alvo real

Uma fixture usa o parser `HTTPResponse` sobre bytes em memória, com Content-Length de 11.079 e corpo de 11.025 bytes terminado em HTML. A leitura limitada devolve todos os 11.025 bytes disponíveis. A implementação anterior a 19/11 classificava a captura só pelo teto local. A versão de 19/11 detectava o déficit, mas usava o mesmo sinal mesmo quando o teto era atingido, como no GET da raiz.

A captura agora expõe bytes lidos e declarados, teto local, divergência verificável de comprimento, leitura interrompida reportada pelo parser, enquadramento e fidelidade do texto. Cabeçalhos de codificação selecionados são preservados. Corpo com codificação de conteúdo não suportada fica sem representação textual. A guarda existente não aceita captura ambígua ou texto sem fidelidade como listagem completa. Não há ampliação de alvo, limites ou ferramentas.

As fixtures cobrem o déficit de 54 bytes, teto local, final de resposta em chunks, cabeçalhos ambíguos, UTF-8 válido e inválido, redação e codificação de conteúdo. Os resultados dessas fixtures demonstram o comportamento do código e não identificam a causa no Juice Shop. A regra HTTP para resposta com comprimento declarado e corpo menor é tratá-la como incompleta. [RFC 9112, seções 6.3 e 8](https://www.rfc-editor.org/rfc/rfc9112.html#section-8).

## Conclusão para a entrega

A listagem de nomes por HTTP foi observada. O 403 de `.txt` continua misturando extensão e existência. Não existe resultado do controle `.md`; o arquivo não foi solicitado. A rubrica original aceita resultados limitados ou inconclusivos. O P6 do adendo permanece parcial e uma revisão acadêmica não deve preencher o resultado ausente. Uma nova rodada seria um experimento adicional, condicionado a autorização específica, preflight atualizado e supervisão por ação. Nenhuma sessão real foi iniciada nesta auditoria.
