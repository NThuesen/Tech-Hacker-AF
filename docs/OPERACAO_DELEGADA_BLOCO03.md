# Bloco 03 — operação delegada ao Codex

Responsável acadêmico: Nicholas. Em 27/10/2026, Nicholas autorizou nesta conversa a operação delegada por dificuldade física no teclado e relatou autorização do professor. A autorização do professor não foi verificada independentemente. A instrução específica desta sessão excepciona a proibição de automação no bloco 03; não altera retroativamente os registros nem demonstra atendimento ao requisito de intervenção humana por ação do PDF.

As decisões são registradas como `decisao_delegada` e `conclusao_delegada`, com operador Codex; nunca como decisões humanas. A autorização humana de Nicholas é registrada separadamente. A avaliação acadêmica desta adaptação e a conclusão final permanecem sujeitas à revisão do grupo/professor. O modo interativo original continua disponível em `scripts/af_run.sh`.

## Execução

```sh
PATH=/home/kit11/.local/opt/kit11-docker:$PATH python3 -u scripts/af_delegated.py INV-01 --autorizacao-nicholas 'Referência à autorização explícita desta conversa'
```

Executar um cenário por vez. O runner reutiliza a aprovação real do plano preservada na sessão interrompida, conferindo SHA256 com o arquivo atual. Reutiliza referências de rede sem alegar novo teste externo. Antes de cada cenário valida Docker Rootless, nome, ID, imagem/digest, rótulos, bindings e ausência de mounts/privilégios; chama o procedimento existente `restore.sh` com a autorização já dada por Nicholas e registra IDs antes/depois e HTTP 200. Não remove outros containers nem modifica bindings/regras de rede.

O Qwen3 4B local escolhe uma proposta por vez usando os resultados e avaliações anteriores, até seis propostas e doze chamadas ao modelo. O Codex lê `revisao-pendente.json` e grava uma resposta privada com o mesmo `request_id`, `operador: Codex`, decisão, ação final e justificativa. O canal aguarda até 30 minutos, sem aceite padrão. Não existe sequência fixa de aprovações. Modificações são validadas e exigem uma segunda revisão da ação final. Logs JSONL e arquivos de revisão permanecem em `logs/`, ignorados pelo Git.

## Critérios definidos antes dos ensaios

- Aprovar somente ações coerentes com a hipótese, evidências prévias e limites do cenário. GET de referência é controle de disponibilidade; status isolado não comprova vulnerabilidade.
- Rejeitar repetição sem nova variável/informação, inferências sem resultado correspondente e ações sem justificativa experimental. A rejeição retorna ao histórico do Qwen, sem escolher sua próxima ferramenta.
- Modificar somente para reduzir risco/escopo ou alinhar um controle ao plano, preservando a proposta original e a segunda aprovação delegada. Não fabricar uma modificação para cumprir a rubrica.
- Nmap somente INV-01, TCP/3000 local, argumentos fixos existentes. GETs limitados aos candidatos públicos do cenário. INV-03 permite apenas um documento não sensível, com nome observado na resposta antes da aprovação; arquivos privados são proibidos.
- POST somente INV-02, `/rest/user/login`, email fictício fixo do plano, senha de teste inválida, vazia ou omitida; uma execução por variante. Sem SQL injection, contas reais ou força bruta.
- Revalidar identidade antes de cada ferramenta. Erro de identificação, rota fora dos limites, erro de ferramenta, HTTP 423/429 ou indicador de segredo interrompe a sessão. Limites de tempo, saída, contexto, redirecionamentos e corpo originais preservados.
- Após cada interpretação, corrigir extrapolações e registrar continuar/encerrar com fundamento. Encerrar por evidência suficiente, ausência de ganho ou limite de propostas. Conclusão delegada não é parecer humano.

## Rede e sessão interrompida

Nicholas reconfirmou nesta conversa: Kali via OpenVPN/tun0 → `10.0.80.3:3001` retornou HTTP 200 em 27/10/2026; Kali sem VPN às 15:04:05 → `192.168.20.31:3001` terminou em timeout, HTTP 000, curl 28, referência `~/af-wan-sem-vpn.txt`; capturas WAN/NAT sem permissão explícita TCP/3001. Esses relatos sustentam bloqueio no caminho testado, não isolamento absoluto. O Codex não acessou o Kali nem refez o teste WAN.

A sessão `f13a210f91d4440480f74eceb6b17862` permanece incompleta e integralmente preservada. Nicholas informou interrupção por Ctrl+C devido à dificuldade de entrada no terminal. Resultado `36e3c3e4cc8443dda703cda8ee39d3c8`: GET `/`, HTTP 200, Content-Length 80117, corpo truncado a 16384 bytes; o contexto do modelo recebe prefixo ainda menor, de até 2048 bytes. O Qwen afirmou “HTML completo” apesar de reconhecer truncagem em limitações: contradição real, sem evidência para a alegação de completude. Nenhuma conclusão humana foi registrada. Hashes dos três arquivos originais foram preservados em manifesto privado separado; nenhum arquivo daquela pasta foi reescrito.

## Limitação de integração observada nesta sessão

A tentativa delegada `caf9a707aed04d7e85436ec627fe1dc6` foi interrompida por erro do código ao registrar segunda aprovação (`operador` duplicado nos argumentos do logger), antes de executar a ação modificada. Contém um GET real, uma rejeição e uma modificação proposta; permanece incompleta. O erro foi corrigido e coberto por teste com os metadados reais do canal. Não é falha de raciocínio do Qwen. Os registros e respostas de revisão foram mantidos. O reinício parte de nova restauração.

O objetivo do runner foi complementado com os candidatos e controles do plano, sem ordem obrigatória. Isso limita especulação de rotas e preserva a escolha dinâmica da ferramenta/parâmetros pelo Qwen. A comparação acadêmica deve explicitar essa informação fornecida ao modelo; não caracterizar rotas do plano como descobertas independentes da IA.
