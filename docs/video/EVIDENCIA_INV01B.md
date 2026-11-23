# INV-01-B — demonstração com registros de 19/11/2026

**Tipo de apresentação:** leitura comentada de uma sessão real já encerrada. **Supervisor:** Nicholas Thuesen. **Modelo:** Qwen3 4B local via Ollama. **Alvo:** Juice Shop do KIT11. **Sessão:** `f0e74216eeba4a3780b1eb41c48695ca`.

**Hipótese e plano:** a interface HTTP pode confirmar a identidade do serviço, sua versão e a disponibilidade de dados de catálogo. GET e Nmap eram candidatos no plano. Nicholas confirmou o adendo e o plano antes da execução, com hashes registrados nos eventos `860e9b8a79924757ba7582fadc3a9cd4` e `14513785d3454ec5b3c2ff4c1405be0c`.

| Ordem | Proposta do Qwen | Decisão de Nicholas antes de executar | Resultado da ferramenta | Interpretação do Qwen e ação posterior |
|---|---|---|---|---|
| 1 | GET `/` para verificar o serviço web | Aprovou individualmente | HTTP 200, HTML limitado. Resultado `bc005ded0ee84d6ca164b2259139dbac` | O Qwen reconheceu o truncamento. Nicholas continuou porque ainda faltava medir a versão e o catálogo. |
| 2 | GET `/rest/admin/application-version` para confirmar a versão | Aprovou individualmente | HTTP 200, versão 17.3.0. Resultado `196ea749f7e346fc833626ed96f5a6f7` | O Qwen reconheceu a versão observada. Nicholas continuou com a revisão das propostas. |
| 3 | GET `/api/Products/1` para verificar dados de catálogo. A proposta mencionou a versão observada | Aprovou individualmente | HTTP 200, JSON de um produto. Resultado `946ca4860a744b35b47224e73b24ee53` | O Qwen identificou dados estruturados. Nicholas encerrou: a meta de reconhecimento HTTP foi atingida dentro do escopo. |

**O que a sessão sustenta:** interface disponível, versão exposta e produto consultável no escopo. Nmap aparece no histórico de 27/10; os três passos acima usaram somente HTTP. A sessão não estabeleceu vulnerabilidade ou falha de autorização.

| Passo | ID da proposta | ID da decisão humana | ID da execução | ID da decisão após interpretação |
|---|---|---|---|---|
| 1 | `a1da32d9ca40497abbf8f0c1b26cec55` | `40cb1162dc0a471c9cec93b6bc1ac713` | `0cf34c13e5cb4dddb6f0355d67ddcf88` | `3a46393a74fd4659a36d6327b52af39f` |
| 2 | `8bf4a80c39e04a29ad88d9bcd5ed565e` | `4d42ddc7d46c41bca5ca09277bdae8c1` | `3ba7eab89dc1488db8317e7a27000bb4` | `f30ec637f65b46c7b49949fc57301d32` |
| 3 | `3d00793323d34e28ae743a300a8dfad2` | `602da0b9067a465c8f21ceca40820011` | `daddb4acf4664304a58e59f38b02b944` | `64d11a5c1254427dadc4376eee6b4871` |

Conclusão humana: evento `ecf649bfd4a44de3b565e56a15f17722`. A tabela resume registros reais e omite saídas brutas. O JSONL original da sessão permanece no KIT11 com acesso privado.
