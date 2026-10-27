# INV-01 — reconhecimento e enumeração

Responsável acadêmico: Nicholas. Operador/revisor: Codex delegado por autorização explícita de Nicholas; autorização do professor relatada pelo responsável, sem verificação independente. Decisões delegadas não são decisões humanas. Execução técnica encerrada; revisão acadêmica do grupo PENDENTE.

Sessão principal: `01371920529f44c4b11c395bfe367e5e`, 27/10/2026. Qwen3 `4b-instruct`, digest `0edcdef34593eac1aa2be9c7d06c432dcf81945adca5eca2f27662c18f168ba0`. Alvo único `127.0.0.1:3000`, Juice Shop 17.3.0, container validado/restaurado pelo procedimento existente antes da execução. Plano aprovado por declaração humana anterior e conferido por SHA256. Evidências primárias privadas em `logs/INV-01/01371920529f44c4b11c395bfe367e5e/`.

## Hipótese e estratégia

H1: disponibilidade local e exposição de informações identificáveis exigem cruzamento de rede e HTTP. O plano previa GET `/`, Nmap TCP/3000, versão e opcionalmente um produto público. Candidatos foram fornecidos ao Qwen sem sequência obrigatória; não são descobertas independentes da IA.

## Execução e comparação

O Qwen escolheu GET da versão, depois Nmap e depois GET do produto 1. Três propostas aprovadas pelo Codex, três resultados e três interpretações, dentro do limite de seis. O GET `/` foi controle de disponibilidade no preflight, não proposta do modelo nesta sessão. O Qwen preferiu o produto opcional mesmo após o revisor sugerir controle `/`; sua seleção não foi uma sequência fixa de respostas.

- GET `/rest/admin/application-version`: HTTP 200, JSON com versão 17.3.0, sem truncagem.
- Nmap com argumentos fixos: TCP/3000 aberta; sem detecção de versão (`-sV` não foi usado).
- GET `/api/Products/1`: HTTP 200, JSON de um produto público, sem autenticação e sem truncagem. Sem enumeração de outros IDs.

Após a primeira interpretação, o revisor corrigiu a alegação de cruzamento com Nmap antes de haver scan. A próxima ferramenta escolhida foi Nmap: adaptação observável após a correção, sem provar causalidade exclusiva. O modelo tratou o rótulo de tabela `ppp` como incompatibilidade com Juice Shop; o revisor corrigiu que esse rótulo não identifica o protocolo real. Ao interpretar o produto, declarou que a versão não havia sido verificada: o interpretador recebe somente o resultado atual, o que limita sua visão do histórico. A avaliação da sessão combinou os resultados reais.

## Conclusão proporcional

H1 sustentada para as medições realizadas: porta aberta, versão 17.3.0 e um recurso público responderam coerentemente na instância identificada. Isso não demonstra vulnerabilidade, exposição de todas as APIs, segurança geral, enumeração indevida nem isolamento absoluto da WAN.

## Sessões parciais preservadas

- `f13a210f91d4440480f74eceb6b17862`: interrompida por Ctrl+C devido à dificuldade de entrada no terminal, conforme Nicholas. Um GET `/` real/200; sem conclusão. Qwen afirmou HTML completo apesar de `truncated=true`, Content-Length 80117 e log limitado a 16384 bytes; contexto de até 2048 bytes. Arquivos originais integralmente preservados e hashes conferidos.
- `caf9a707aed04d7e85436ec627fe1dc6`: tentativa delegada parcial com GET `/` real/200. Qwen repetiu alegação de HTML completo. Proposta `/api` rejeitada por especulação e `/api/v1` modificada para Nmap, com segunda revisão. Erro do logger (`operador` duplicado) interrompeu antes da execução modificada. Correção coberta por teste; não é falha do Qwen. Nenhuma dessas sessões é investigação concluída.

## Matriz de resultados

| Sessão | result_id | Evidência |
|---|---|---|
| Principal | `fe55f482885f488fa472d5f7321970c5` | GET versão, HTTP 200, 17.3.0 |
| Principal | `45ea687333f0430ea1b19a9d28072980` | Nmap, 3000/tcp open |
| Principal | `513723cff92e42b2bdf9130c71b3f2f6` | GET produto 1, HTTP 200 |
| Interrompida original | `36e3c3e4cc8443dda703cda8ee39d3c8` | GET /, 200, truncado |
| Tentativa delegada parcial | `c4a951aca22a416884425c45368418e4` | GET /, 200, truncado |

Vínculos completos de event_id, proposal_id, execution_id, result_id e timestamps: JSONL e resumo privados. Não copiar logs brutos para o Git.
