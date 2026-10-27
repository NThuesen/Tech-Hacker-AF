# AF Tecnologias Hackers — Plano de testes e investigações (KIT11)

**Versão:** 1.0 — hipóteses e estratégia H1–H3 preservadas; atualização somente de registro de aprovação  
**Estado:** APROVAÇÃO DO CONTEÚDO DECLARADA PELO GRUPO em comunicação de 27/10/2026; identificação dos presentes, data/hora da deliberação e portão de isolamento WAN ainda pendentes de documentação. **Investigações acadêmicas não executadas.**  
**Data do planejamento:** 27/10/2026  
**Responsáveis e aprovação:** o responsável informou que o grupo já aprovou o planejamento; integrantes e data/hora original da reunião: [a registrar]; referência do conteúdo técnico aprovado: `plano_humano.md` existente no commit `3cdb951`. A declaração não substitui os dados faltantes nem comprova autoria/cronologia pré-LLM.

> **Objetivo:** conduzir três investigações distintas e reprodutíveis exclusivamente contra o OWASP Juice Shop local, empregando conhecimentos de reconhecimento, Nmap, requisições HTTP, autenticação, análise de respostas/logs e acesso a recursos. O Qwen3 4B deve propor ações condicionais; o grupo mantém o controle de cada execução e da interpretação final. Não há obrigação de descobrir vulnerabilidade: há obrigação de testar hipóteses e sustentar conclusões.

## 1. Base técnica e limites

### 1.1 Ambiente planejado

| Elemento | Configuração de referência | Situação de evidência |
|---|---|---|
| Alvo único | OWASP Juice Shop **v17.3.0** no Docker Rootless do Ubuntu KIT11 | HTTP 200 local e restauração registrados no bloco 01 |
| Endereço do agente | **127.0.0.1:3000**, no Ubuntu físico | Já testado localmente; o código restringe host/porta |
| Modelo | Ollama **qwen3:4b-instruct**, API **127.0.0.1:11434** | Resposta real e integração registradas nos blocos 01–02 |
| Ferramentas integradas | **nmap** (somente TCP/3000), **http_get** e **http_post** (caminhos relativos ao Juice Shop) | Implementadas em agent.py; validar novamente antes da AF |
| Supervisão | Aprovar, modificar com segunda aprovação, rejeitar ou encerrar; decisão posterior à interpretação | Implementada; decisões do ensaio de engenharia já registradas |
| Estação cliente | Kali VM do notebook, por OpenVPN do Roteiro 1, alcançando a rede LAN | Usuário confirmou HTTP 200 pela VPN em 10.0.80.3:3001 na sessão anterior; registrar nova evidência antes de cada investigação |
| Outros serviços | WordPress :80, Nextcloud :8000, pfSense, OpenVPN | Fora do escopo; não modificar ou testar ofensivamente |

**Portão de execução acadêmica:** antes das investigações, comprovar novamente acesso do Kali ao Juice Shop e isolamento da WAN. O uso de OpenVPN existente é preferível a implantar SSH. A instância tem os bindings fixos 127.0.0.1:3000 e 10.0.80.3:3001; o agente usa exclusivamente o primeiro. O acesso Kali foi confirmado pelo usuário na sessão anterior, mas não comprova isolamento WAN, que continua PENDENTE. Não alterar esses bindings nem habilitar portas na WAN. O diagnóstico, o reconhecimento histórico do Roteiro 1 e os ensaios do bloco 02 **não substituem** esse teste de conectividade atual.

### 1.2 Escopo autorizado e regras de segurança

- **Permitido:** portas, respostas e recursos da instância Juice Shop do KIT11; métodos GET e POST limitados, Nmap TCP apenas na porta 3000; uso de contas de teste exclusivamente locais, se necessárias.
- **Proibido:** scans de sub-rede/outros kits, WordPress, Nextcloud, pfSense, endpoint WAN, sites externos; negação de serviço, força bruta, ataques com dicionários, shell irrestrito, extração de segredos, persistência, alteração de firewall/NAT sem autorização e leitura de arquivos do SO hospedeiro.
- **Dados:** nunca usar conta pessoal, senha real, dados de usuários ou chaves VPN. Manter logs JSONL privados e fora do Git; conferir manualmente conteúdo livre e capturas antes de anexar evidências.
- **Limites técnicos atuais:** 20 propostas por sessão, até 40 chamadas ao modelo, HTTP com prazo de 8 s, Nmap limitado à porta 3000 e saída truncada. **Limite metodológico mais restrito:** em cada investigação, preferir 3–6 propostas úteis; interromper quando a hipótese puder ser respondida. Não fazer repetição automática de tentativas de login.
- **Identidade do alvo:** confirmar que a instância publicada é o container Juice Shop autorizado antes de iniciar; não confiar apenas no número da porta. Registrar versão/digest, IP e evidência HTTP. A ferramenta HTTP do agente não segue redirecionamentos.

### 1.3 Bases conceituais da disciplina

1. **Reconhecimento ativo e coleta de informações:** identificar serviço e superfícies observáveis, sem extrapolar o significado de uma porta aberta (Aula 4 — Coleta de informações; Reconhecendo Alvo).
2. **Comunicação HTTP/TCP e análise de logs:** comparar métodos, status, cabeçalhos, corpos e anomalias; diferenciar observação de inferência (Aula 3 — Comunicação de dados e Análise de logs).
3. **Autenticação e credenciais:** comparar comportamento diante de entradas controladas, sem força bruta nem coleta de credenciais de terceiros (Aula — credenciais).
4. **Recursos/arquivos e validação de caminhos:** investigar acessibilidade e tratamento de caminhos; **não classificar uma listagem HTTP ou erro como LFI/RFI sem demonstrar as condições técnicas** (Aula — LFI e RFI).

## 2. Método experimental comum

### 2.1 Antes de cada investigação

1. Confirmar autorização do grupo e estado do laboratório, incluindo conexão a partir do Kali e restrição à instância do Juice Shop; registrar data/hora, operador, versão da aplicação, modelo e imagem.
2. Reiniciar/restaurar o **container identificado e autorizado** ao estado conhecido, mediante confirmação explícita do responsável; observar HTTP 200 após a restauração. Registrar ID anterior/novo do container e evidência da restauração. Não apagar containers desconhecidos.
3. Criar identificador do cenário (INV-01, INV-02, INV-03) e arquivo privado distinto, por exemplo **logs/inv-01.jsonl**. Guardar capturas revisadas em pasta local privada de evidências.
4. Registrar antecipadamente: hipótese, variável manipulada, controle, evidência necessária, condição que refuta a hipótese, limite de ações e responsáveis.
5. Informar ao agente **somente o objetivo**, e não um roteiro obrigatório de requisições. As ações listadas abaixo são possibilidades para decisão humana e comparação, não uma sequência fixa imposta ao modelo.

### 2.2 A cada proposta do Qwen

1. Registrar proposta integral, ferramenta, parâmetros, objetivo e justificativa em JSONL, vinculados aos IDs de sessão/proposta.
2. **Antes de executar**, o responsável escolhe: aprovar / modificar / rejeitar / encerrar, e escreve justificativa técnica. Modificação só roda depois de validação e **segunda aprovação**.
3. Somente depois da autorização, executar a ferramenta **contra Juice Shop**, armazenar status/código de retorno, trecho útil da saída, duração e identificador de resultado.
4. Solicitar interpretação do resultado ao Qwen e registrar **o que a resposta comprova, o que não comprova e limitações**. O grupo registra concordância/correção e decide continuar ou encerrar.
5. Se continuar, permitir nova escolha dinâmica da ferramenta/rota pelo modelo a partir da evidência. Para mostrar adaptação, destacar ao menos um ponto em que um resultado ou uma rejeição humana mudou a proposta seguinte.
6. Encerrar com conclusão humana explícita: **confirmada / refutada / inconclusiva**, evidências por ID, hipóteses alternativas e limitações. Não confundir ensaio de engenharia com investigação da AF.

**Critérios gerais de parada:** saída do escopo; sugestão de varredura ampla/força bruta; tentativa de obter dados sensíveis; HTTP 429 ou indicação de bloqueio; falha repetitiva de modelo/ferramenta; ausência de nova informação útil; ou decisão do grupo. Uma rejeição **não** autoriza execução alternativa automática.

## 3. INV-01 — Reconhecimento e enumeração controlada

**Pergunta:** quais serviços e informações a instância Juice Shop expõe a um cliente HTTP não autenticado?

**Hipótese H1:** o serviço local está acessível em TCP/3000 e divulga informações básicas identificáveis, como a versão da aplicação; uma porta aberta, por si só, **não** demonstra produto, aplicação nem vulnerabilidade.

**Plano de comparação:**
- **Controle de disponibilidade:** GET **/**. Espera-se uma resposta HTTP da aplicação, mas não se presume o status nem o conteúdo.
- **Observação de rede:** Nmap, limitado por código a **127.0.0.1:3000**. Comparar resultado da porta com a resposta HTTP para evitar inferir o software apenas pelo rótulo de serviço do Nmap.
- **Candidato a confirmação de versão:** GET **/rest/admin/application-version** (já utilizado em ensaio de engenharia; repetir somente se proposto/aprovado). Ler o corpo e identificar exatamente o que informa.
- **Opcional, se surgir justificativa:** um único recurso público do catálogo, como **/api/Products/1**, para verificar se a sugestão sobre produtos é sustentada por nova resposta, sem enumeração massiva.

**Variáveis e evidências:** ferramenta/rota escolhida, porta observada, status HTTP, corpo relevante, eventual campo de versão, versão efetivamente retornada e limites da resposta; IDs de proposta, aprovação, resultado e interpretação.

**Critério de confirmação/refutação:** H1 somente é sustentada quando **Nmap e HTTP reais** forem coerentes e o corpo efetivamente fornecer a informação alegada. Se Nmap indicar porta aberta, mas HTTP não identificar Juice Shop, **não** inferir aplicação. Se a rota da versão falhar, não presumir versão ou exposição.

**Ponto de supervisão:** rejeitar conclusões do Qwen sobre outras APIs sem resposta correspondente. O erro de extrapolação da versão para catálogo observado no bloco 02 pode servir **como comparação crítica histórica**, mas não substitui um registro real de INV-01.

**Saída pretendida:** matriz curta “fato observado / inferência do modelo / decisão do grupo”, com pelo menos um controle positivo, uma verificação cruzada e um limite reconhecido. **Não** alegar vulnerabilidade apenas porque a versão é pública.

## 4. INV-02 — Autenticação e tratamento de entradas controladas

**Pergunta:** a aplicação responde de maneira consistente a tentativas inválidas de autenticação e a campos ausentes, sem divulgar informações indevidas?

**Hipótese H2:** dois erros de entrada controlados podem produzir respostas diferentes de validação ou autenticação; diferenças observadas exigem interpretação cautelosa e **não** demonstram, isoladamente, enumeração de usuários ou bypass.

**Endpoint candidato a verificar:** POST **/rest/user/login**. A rota é hipótese operacional a confirmar na própria instância, não uma descoberta já realizada na AF. O agente atual aceita apenas JSON de texto no corpo; não gerencia cookies ou cabeçalhos arbitrários.

**Comparações planejadas (no máximo uma execução por variante, com aprovação independente):**

| Controle/variante | Exemplo de corpo JSON de laboratório | O que comparar |
|---|---|---|
| A — credencial certamente não cadastrada | {"email":"af_inexistente_01@kit11.invalid","password":"teste-invalido-01"} | status e mensagem genérica de falha |
| B — mesmo identificador, campo de senha vazio | {"email":"af_inexistente_01@kit11.invalid","password":""} | validação de entrada, status, formato e informação exposta |
| C — opcional e condicionado | objeto JSON omitindo o campo de senha, ou conta de teste descartável criada **pelo grupo**, se houver justificativa | separar comportamento de validação de login válido; não usar credenciais reais |

**Controles metodológicos:** manter rota, método, origem, versão e instante conhecidos; variar **um campo de cada vez**. Em caso de redirecionamento, registrar 3xx sem segui-lo. O grupo deve revisar o corpo do POST antes de autorizá-lo. Não repetir credenciais em loop, não fazer SQL injection improvisada nem testes contra contas de terceiros.

**Evidências mínimas:** requisição aprovada com corpo de teste revisado, status, campos não sensíveis de resposta, duração, semelhanças/diferenças A×B, proposta e interpretação do Qwen. Redigir valores de senha nos logs compartilháveis; o agente já tenta ocultar campos sensíveis, mas a revisão humana continua indispensável.

**Decisão condicional sugerida:** se a rota não existir (404), interromper a hipótese sobre essa rota e documentar a dificuldade; se for 4xx por entrada inválida, comparar com o segundo controle; se houver 429/bloqueio, parar; se a aplicação responder algo inesperado, não afirmar bypass sem controle de autenticação adequado.

**Conclusões possíveis:** “respostas iguais para os controles testados”, “validação e autenticação apresentam diferenças observáveis” ou “inconclusivo por ausência de rota/controle positivo”. **Não** afirmar segurança geral da autenticação nem enumeração de usuários só por mudança de status.

**Limite explícito:** testar **autorização entre usuários** exigiria autenticação, gestão de sessão e novas evidências. Não ampliar o agente para cookies/tokens sem necessidade e aprovação; H2 avalia o **tratamento de autenticação/entrada**, que já é um cenário distinto e previsto na AF.

## 5. INV-03 — Exposição e acesso a recursos da aplicação

**Pergunta:** a instância oferece recursos HTTP públicos com controles previsíveis para caminhos existentes e inexistentes?

**Hipótese H3:** um caminho relacionado a documentos/arquivos pode expor uma listagem ou recurso publicamente; isso requer validação pelo conteúdo e pelo contexto de acesso. Um HTTP 200, uma listagem ou um 404 **não** prova automaticamente acesso indevido, LFI ou RFI.

**Alvo candidato:** GET **/ftp/**, a confirmar pela resposta real da versão instalada. Se não existir ou não retornar conteúdo útil, o grupo poderá escolher **uma** rota de recurso indicada por evidência do próprio Juice Shop, permanecendo na mesma aplicação.

**Comparações planejadas:**
1. **Controle de referência:** GET **/**, para confirmar que a aplicação responde.
2. **Recurso candidato:** GET **/ftp/**, registrar status, tipo de conteúdo e se há links ou nomes de recursos. Não supor listagem.
3. **Controle negativo:** GET **/ftp/arquivo-inexistente-af.txt**, para comparar tratamento de arquivo ausente.
4. **Opcional condicionado à evidência:** GET de **um único arquivo não sensível**, escolhido dentre os nomes retornados pela aplicação, com aprovação explícita do grupo. Não coletar relatórios privados, credenciais, tokens nem dados pessoais.

**Variáveis e evidências:** caminho real vs. inexistente, status, tipo de conteúdo, tamanho aproximado, corpo limitado, nomes/links observados, sem autenticação, e diferença de tratamento. Registrar a origem de qualquer nome de arquivo: **não inventar caminhos** sugeridos pelo modelo.

**Ramificações possíveis:** se /ftp/ retornar 200, verificar se a resposta é listagem ou página HTML genérica; se retornar 401/403, reconhecer controle de acesso naquele caminho (sem generalizar); se retornar 404, refutar hipótese específica e encerrar ou revisar caminho com base em evidência; se um arquivo público for legível, discutir se a exposição é esperada ou sensível segundo seu **conteúdo e função**.

**Limites:** não executar payloads para ler /etc/passwd, /etc/shadow, arquivos do host, segredos ou URL remota. O conceito de LFI/RFI estudado em aula pode informar a interpretação, mas **não** usar esses rótulos sem demonstrar inclusão indevida controlada por entrada. Nenhuma tentativa fora da instância Juice Shop.

**Conclusão esperada como formato, não como resultado:** “na versão X e no estado Y, o caminho Z respondeu com [status/conteúdo], logo demonstramos [fato específico]; não demonstramos [autorização indevida/LFI/etc.]”.

## 6. Como comparar o planejamento com o agente

Para **cada** INV-0N, criar um registro de comparação:

| Questão de avaliação | Informação a preencher com a execução real |
|---|---|
| Hipótese e estratégia prévia | H1/H2/H3; controle escolhido e evidência esperada |
| Primeira proposta do Qwen | ferramenta, rota, parâmetros, justificativa, proposal_id |
| Decisão do grupo | aprovada / modificada / rejeitada + motivo |
| Evidência produzida | status/saída, result_id, timestamp, duração, arquivo de log |
| Interpretação do Qwen | frase verificável + limite mencionado; interpretação vinculada ao result_id |
| Avaliação do grupo | correta / parcialmente correta / incorreta / não conclusiva; fundamento |
| Adaptação do agente | qual resultado levou a qual nova proposta, com IDs; ou por que não ocorreu |
| Conclusão humana | confirmada / refutada / inconclusiva, sem afirmações além da evidência |
| Limitação da IA | omissão, inferência não suportada, repetição, atraso, erro técnico ou nenhuma observada |
| Aprendizado técnico | o que Nmap/HTTP/logs permitiram e o que não permitiram concluir |

**Exemplo de controle crítico já observado, apenas como engenharia anterior:** um GET de versão retornou {"version":"17.3.0"} e o modelo inferiu uma API de produtos sem prova nessa resposta; o grupo rejeitou a extrapolação. Identificar o registro como **ENGENHARIA, não INV-01**, citando docs/ENGENHARIA_BLOCO02.md e o run_id original. Nas investigações acadêmicas, buscar e registrar limitações **realmente encontradas**, sem fabricar erro, rejeição ou vulnerabilidade.

## 7. Padrão de evidências e reprodutibilidade

Para cada investigação, preservar em local privado:
- **INV-0N/01-preflight:** data, host, versão Juice Shop, ID/digest do container, modelo, conectividade Kali verificada, estado das portas relevantes, restauração.
- **INV-0N/02-execucao:** arquivo JSONL completo (run_id e step_ids), requisições executadas/rejeitadas, respostas e interpretações vinculadas.
- **INV-0N/03-analise:** matriz do item 6 e 1–3 capturas selecionadas, com credenciais/tokens/cookies omitidos.
- **INV-0N/04-conclusao:** decisão do grupo, evidência primária por result_id, interpretação prudente, condição de repetição/refutação e limitações.

**Qualidade da prova:** evidência direta ≠ interpretação ≠ hipótese. Status 200 prova resposta, não acesso indevido; 401/403 não provam segurança total; “open” no Nmap prova a condição da porta no instante observado, não o tipo exato da aplicação. Problemas de modelo e de rede são resultados quando documentados com rigor.

**Reprodução:** registrar comando de início, confirmação do container correto, estado inicial, sequência **de decisões efetivamente ocorrida** e restauração entre cenários. Não copiar uma lista de passos sugeridos para fingir que o LLM os escolheu. Testes do bloco 02 não são automaticamente resultados dos três cenários.

## 8. Critérios de aceite e vínculo com a rubrica

| Critério AF | Peso | Evidência pretendida |
|---|---:|---|
| Laboratório reproduzível | 15% | Docker Rootless + HTTP real + Ollama/Qwen local + restauração, acesso Kali atual e checagem WAN |
| Agente supervisionado | 20% | propostas dinâmicas com escolhas Nmap/GET/POST; parâmetros e autorizações/rejeições registradas; interpretação por resultado |
| Planejamento e qualidade dos testes | 20% | H1–H3 distintas, controles, variáveis, evidências-alvo e critérios de refutação; grupo delibera e aprova a versão antes da execução acadêmica |
| Evidências e interpretação | 20% | três logs JSONL reais, IDs interligados, matrizes por cenário, resultados verificáveis |
| Análise crítica da IA | 20% | contrastes entre plano e propostas, decisões humanas justificadas, adaptação condicionada a evidências, erro/limitação concreta com tratamento |
| Documentação e apresentação | 5% | relatório de **4–6 páginas**, vídeo de **até 10 minutos** com **uma investigação completa** e referência cruzada às evidências |

O objetivo é **cobrir todos os critérios**, não garantir nota. Se uma hipótese não for confirmada, a conclusão fundamentada continua válida.

### Portão acadêmico / validação do grupo

- [x] **Aprovação do conteúdo declarada pelo grupo**, conforme informação comunicada pelo responsável em 27/10/2026. O conteúdo técnico H1–H3 não foi alterado neste registro.
- [ ] Identificar integrantes que participaram, data/hora original da deliberação, eventuais alterações e referência verificável da aprovação.
- [ ] Confirmar com o professor, quando aplicável, o tratamento da exigência de planejamento inicial sem LLM; **não atribuir falsamente autoria ou cronologia**.
- [x] Acesso Kali/OpenVPN → Juice Shop `10.0.80.3:3001` observado com HTTP 200, conforme resultado fornecido pelo grupo.
- [ ] Comprovar o isolamento WAN: as capturas das regras WAN/NAT não mostram liberação/encaminhamento de TCP/3001, mas ainda falta teste negativo pelo caminho externo **sem VPN** e conferência de outras regras aplicáveis.
- [ ] Antes de cada investigação, registrar revisão/aprovação da versão no terminal (nomes, data e justificativa), manter logs privados e confirmar restauração apenas do container autorizado.

**Aprovação comunicada não equivale a execução liberada:** o portão de rede permanece PENDENTE, e os dados da deliberação devem ser registrados fielmente.

**Aprovação do grupo:** SIM, segundo declaração do responsável comunicada em 27/10/2026.  
**Data/hora real da deliberação:** [não informada; preencher com dado verdadeiro]  
**Integrantes presentes:** [não informados; preencher com nomes verdadeiros]  
**Versão de referência do conteúdo aprovado:** `plano_humano.md` presente no commit `3cdb951` (a edição atual não altera H1–H3).  
**Alterações deliberadas e justificativas:** [não informadas; não presumir ausência]  
**Evidência complementar de aprovação/ata:** [pendente, se disponível]
