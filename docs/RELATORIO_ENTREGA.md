# Investigação supervisionada com um modelo de linguagem local

**Avaliação Final · Tecnologias Hackers · 2026.2**
**Nicholas Thuesen e Alison Araujo**
Relatório técnico · 23 de novembro de 2026

## 1. Pergunta, escopo e arquitetura

**Pergunta.** Como o Qwen3 4B escolhe ferramentas e interpreta resultados em investigações de segurança no laboratório, e em quais situações o revisor precisa intervir? Foram estudados três casos: reconhecimento, entradas inválidas no login e tratamento de recursos HTTP. O alvo foi exclusivamente a instância local do OWASP Juice Shop 17.3.0 no KIT11.

**Arquitetura.** O KIT11 físico executou Ubuntu, o Juice Shop em Docker Rootless e o Qwen3 4B (`qwen3:4b-instruct`) via Ollama. O agente em Python e o Ollama se comunicam por loopback. O agente consulta o Juice Shop pelo binding local. O Kali em uma VM externa recebe acesso ao laboratório pelo OpenVPN, em um binding privado separado. A imagem da aplicação é fixada e os procedimentos de restauração conferem identidade e configuração antes de apresentar confirmação.

**Fluxo da investigação**

1. O agente informa objetivo, ferramentas permitidas e evidências disponíveis ao Qwen.
2. O modelo propõe ferramenta e parâmetros. O operador aprova, modifica com nova confirmação, rejeita ou pausa.
3. Após autorização e validação de escopo, a ferramenta executa. O resultado retorna ao Qwen.
4. O operador avalia a interpretação, decide continuar ou encerrar e registra uma conclusão. IDs vinculam cada etapa.

**Limites.** As ferramentas integradas são Nmap, HTTP GET e HTTP POST. O modelo propõe dentro de um conjunto limitado de parâmetros e rotas. O executor restringe o alvo local e limita tempo e tamanho das respostas. As ações registradas ficaram no Juice Shop. O laboratório tem procedimento de restauração para um estado conhecido.

**Acesso e isolamento.** Nicholas relatou em 19/11 HTTP 200 via VPN, timeout sem VPN e inspeção visual sem regra WAN ou encaminhamento NAT identificado para a porta do laboratório. O timeout delimita o caminho e o momento testados. Os originais do Kali ainda não estavam disponíveis para conferência no KIT11. O relato não estabelece isolamento WAN absoluto.

<!-- pagebreak -->

## 2. Planejamento e investigação supervisionada

O `plano_humano.md` registrou H1–H3, ferramentas candidatas, variáveis e evidências esperadas antes das investigações acadêmicas. Seu primeiro registro Git é posterior a um ensaio de integração com LLM. O histórico comprova a existência do plano antes das sessões acadêmicas e não comprova elaboração inicial sem LLM, exigida pela AF. A deliberação original permanece sem documentação completa. O adendo 03B é posterior e foi aprovado por Nicholas no terminal, com hash, antes da INV-01-B. Preservamos os planos e seus registros.

**H1 · Reconhecimento.** Confirmar a identidade do serviço por HTTP, examinar a versão anunciada e verificar a disponibilidade de dados de catálogo. Nmap e GET já estavam entre os candidatos. Na sessão histórica de 27/10, o Nmap registrou TCP/3000 aberta (`45ea6873…`), e a versão foi obtida por HTTP (`fe55f482…`). O rótulo de serviço de uma porta, sozinho, não identifica a aplicação.

### INV-01-B · Um ciclo completo em sessão real

| Proposta do Qwen | Intervenção de Nicholas | Resultado e avaliação |
|---|---|---|
| GET da raiz | Aprovou individualmente | HTTP 200, HTML limitado (`bc005ded…`). O Qwen reconheceu o truncamento. Nicholas decidiu continuar para verificar os dados específicos. |
| GET do endpoint de versão | Aprovou individualmente | HTTP 200, versão 17.3.0 (`196ea749…`). O Qwen identificou a versão da resposta. Nicholas decidiu continuar. |
| GET de um produto, após mencionar a versão observada | Aprovou individualmente | HTTP 200, JSON de catálogo (`946ca486…`). Nicholas encerrou após revisar a interpretação. |

**Conclusão registrada.** Houve evidência de interface HTTP disponível, versão anunciada e produto consultável. Esses resultados sustentam o objetivo de reconhecimento HTTP. A sessão 03B usou apenas GET. A terceira proposta mostra uso de uma observação anterior. Como as rotas eram candidatas do plano e a sessão não teve contrafactual equivalente, essa sequência não mede o efeito causal do histórico na escolha.

**Rastreabilidade.** Sessão `f0e74216eeba4a3780b1eb41c48695ca`. A trilha da INV-01-B no pacote de gravação lista IDs de propostas, decisões, execuções, resultados e escolhas após interpretação. A conclusão humana está no evento `ecf649bfd4a44de3b565e56a15f17722`.

<!-- pagebreak -->

## 3. Autenticação e acesso a recursos

### H2 · Respostas a variações inválidas de senha

**Estratégia.** Manter um único identificador fictício e variar a senha. A é texto inválido, B é senha vazia e C é campo omitido. O histórico de 27/10 testou B e A, nessa ordem, com HTTP 401 e o mesmo corpo.

**INV-02-B.** O Qwen propôs A. Depois repetiu propostas e descreveu de forma incorreta qual variante havia sido enviada. O Codex, revisor delegado, modificou duas propostas para completar B e C e confirmou cada alteração. As três execuções retornaram **HTTP 401**, mesmo tipo de conteúdo e mesmo corpo de 26 bytes. A comparação registrada considera status e corpo, sem atribuir igualdade a todos os cabeçalhos. IDs: `52511329…`, `c7e8f6ea…`, `6f1c957e…`.

**Conclusão.** A diferença esperada entre as três respostas não foi observada com as entradas medidas. A amostra não sustenta inferências sobre bypass, enumeração, outras contas ou segurança geral do login.

### H3 · Listagem HTTP e tratamento de caminho

**Estratégia.** Observar se há listagem de nomes e distinguir efeito da extensão do efeito da ausência. O histórico e a primeira rodada INV-03-B observaram listagem HTTP 200 e 403 no caminho de controle com extensão `.txt`. Como extensão e existência variaram juntas, o 403 deixa em aberto o comportamento diante de uma ausência com extensão permitida.

**Repetição INV-03-B.** Nas duas rodadas de 19/11, a listagem declarou **11.079 bytes** e o corpo registrado teve **11.025** (`ea5956fd…`, `fe4d96fb…`). Na repetição, o contador antes da decodificação também mediu 11.025. O teto local era 16.384 bytes. A causa exata permanece indeterminada. O Qwen afirmou completude apesar do indicador de truncamento e fez referência a uma resposta `.md` que não existia. O Codex comparou os metadados e encerrou a rodada.

**Conclusão.** A listagem de nomes foi observada. O controle `.md` não foi executado e permanece inconclusivo. O caso não estabeleceu acesso indevido a arquivos, inclusão local ou remota de arquivos ou falha geral de autorização. A correção de captura foi validada com fixtures, sem gerar novo resultado do Juice Shop.

<!-- pagebreak -->

## 4. Decisões do modelo, intervenções e qualidade da evidência

| Cenário | O que o plano previa | O que o Qwen fez | O que o operador decidiu |
|---|---|---|---|
| Reconhecimento | Medir interface, versão e catálogo. Nmap era candidato | Propôs três GETs. Referenciou a versão ao propor o produto | Nicholas aprovou cada GET, avaliou resultados e encerrou com o objetivo atingido |
| Autenticação | Comparar respostas mantendo fixo o identificador | Sugeriu A, repetiu propostas e confundiu variantes | Codex modificou e confirmou B/C. Comparou as três respostas reais |
| Recursos | Condicionar o controle `.md` à evidência da listagem | Antecipou uma resposta ausente e chamou a listagem de completa | Codex interrompeu o controle. A diferença entre bytes recebidos e anunciados contrariava a interpretação |

**Erro concreto e correção.** Na repetição de recursos, o HTML terminava com o fechamento esperado e ainda assim havia déficit de 54 bytes. Uma fixture reproduziu esse fenômeno com o parser HTTP em memória. A captura passou a separar limite local, divergência de comprimento, enquadramento e fidelidade do texto. O histórico não reteve os cabeçalhos de codificação necessários nem a resposta bruta. As medições não atribuem a diferença ao servidor, intermediário ou transporte.

**Autoria.** Nicholas supervisionou pessoalmente a INV-01-B. As duas outras investigações 03B tiveram revisões e conclusões registradas como delegadas ao Codex. Nicholas relatou anuência do professor para a adaptação, sem comprovação independente. A rubrica original pede supervisão do grupo na execução. A conformidade das sessões delegadas continua sujeita ao aceite acadêmico.

**Replay.** O Qwen local recebeu entradas simuladas e suas propostas não foram executadas. Foram feitas 17 solicitações para um orçamento de 14, com 16 respostas registradas. O contexto de uma série omitiu a lista de ferramentas, e os formatos comparados não garantiam equivalência de informação. O replay não permite medir uma taxa justa de desvio nem estabelecer superioridade de um formato. O orçamento compartilhado bloqueia novas consultas sob o protocolo existente.

<!-- pagebreak -->

## 5. Conclusão, rastreabilidade e entrega

O Qwen foi útil na escolha de medições HTTP coerentes com o objetivo da INV-01-B e na leitura de status e estruturas. Na INV-02-B, as alterações do revisor foram necessárias para testar todas as variantes. Na INV-03-B, a interpretação do modelo conflitava com os metadados e foi interrompida. A contribuição observada dependeu de escopo restrito e conferência da sequência proposta, autorização, resultado e interpretação. O projeto documentou três cenários distintos e nenhum deles demonstrou exploração bem-sucedida.

**Evidências consultáveis.** As matrizes do projeto associam os IDs abreviados deste relatório aos IDs completos e aos JSONL originais. A auditoria local de 23/11 percorreu 12 arquivos e 320 eventos, verificou vínculos de 20 execuções e comparou 10 snapshots de planos aos hashes registrados. A tentativa histórica interrompida permanece identificada. O manifesto privado fixa os hashes observados na auditoria. Ele não autentica retrospectivamente os eventos nem certifica as interpretações.

**Reprodução.** O README e a operação 03B descrevem requisitos, procedimentos e limites do laboratório. Os testes automatizados exercitam a lógica, a captura HTTP em memória e os controles do agente. Seus resultados não substituem as sessões reais. A continuidade do laboratório após reinicialização não foi verificada nesta auditoria.

**Pendências acadêmicas.** A origem pré-LLM do plano e o aceite da supervisão delegada exigem revisão. A evidência primária do Kali permanece indisponível ao auditor. A investigação de recursos fica limitada à observação da listagem e ao 403 de `.txt`. O controle `.md` permanece aberto no adendo P6. O pacote de gravação mostra a investigação humana completa sem depender da disponibilidade dos serviços. Gravação e aceite final cabem a Nicholas.

### Fontes para conferência

- Enunciado: `docs/AF - Tecnologias Hackers 26-2.pdf`, seções 1–8.
- Metodologia: `plano_humano.md`, `docs/PLANO_03B_EXCELENCIA_V2.md` e `docs/OPERACAO_BLOCO03B_V2.md`.
- Evidências: `docs/03b/MATRIZ_COMPARATIVA.md`, `docs/investigacoes/MATRIZ_EVIDENCIAS.md` e `docs/video/EVIDENCIA_INV01B.md`.
- Diagnóstico: `docs/03b/DIAGNOSTICO_CAPTURA_HTTP.md` e RFC 9112, seções 6.3 e 8.
- Critérios: `CHECKLIST_RUBRICA.md`. Evidências primárias mantidas sob acesso privado no KIT11.
