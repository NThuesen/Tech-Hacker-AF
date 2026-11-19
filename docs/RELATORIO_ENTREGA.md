# Investigação supervisionada de uma aplicação web vulnerável com modelo de linguagem local

**Tecnologias Hackers — Avaliação Final — 2026.2**
**Equipe informada pelo responsável:** Nicholas Thuesen e Alison Araujo
**Ambiente:** laboratório físico KIT11, Ubuntu, Kali Linux e OWASP Juice Shop
**Versão:** relatório preparado em 19/11/2026 — revisão acadêmica e vídeo pendentes

> As evidências numéricas provêm das sessões registradas. Os JSONL são privados; decisões por ação atribuídas ao Codex delegado permanecem distintas da autorização geral do responsável. A adequação acadêmica da adaptação requer revisão do professor.

## Resumo

Este trabalho investiga o emprego de um modelo de linguagem executado localmente na seleção de ferramentas e na interpretação de evidências de segurança de uma aplicação web deliberadamente vulnerável. O objeto exclusivo de testes foi uma instância do **OWASP Juice Shop 17.3.0**, implantada no servidor físico KIT11. Um agente em Python integrou **Qwen3 4B via Ollama**, Nmap e requisições HTTP GET e POST, com limites técnicos de alvo, recursos e tempo. O planejamento aprovado pelo grupo previu três investigações: reconhecimento de serviços e informações expostas; comparação de respostas de autenticação para entradas inválidas; e avaliação de recursos HTTP públicos e controles de caminho. Nas execuções registradas, a porta TCP/3000 estava aberta, o endpoint de versão informou 17.3.0, duas tentativas inválidas de login produziram a mesma resposta HTTP 401 e uma rota de arquivos exibiu listagem pública. O estudo distingue sistematicamente resposta observada, inferência do modelo e vulnerabilidade demonstrada. Foram identificadas limitações reais de interpretação, inclusive afirmação de completude sobre HTML truncado e conclusões antes de uma segunda medição. A contribuição principal está na **rastreabilidade experimental e na avaliação crítica das decisões**, não na quantidade de falhas encontradas.

**Palavras-chave:** segurança de aplicações web; reconhecimento; autenticação; OWASP Juice Shop; LLM local; evidências; supervisão.

## 1. Introdução e delimitação

Ferramentas de reconhecimento e clientes HTTP permitem observar sistemas, mas o resultado técnico exige interpretação cuidadosa: uma porta aberta não identifica, sozinha, o software executado; HTTP 200 não comprova vulnerabilidade; e respostas de erro semelhantes não atestam segurança integral. Modelos de linguagem podem auxiliar na formulação de hipóteses, seleção de testes e explicação dos resultados, mas também podem produzir conclusões não sustentadas pela saída das ferramentas.

A pergunta orientadora deste trabalho foi: **até que ponto um LLM local consegue propor testes de segurança úteis, reagir às evidências e reconhecer os limites das próprias inferências em um laboratório controlado?** Para responder, foram delineadas três hipóteses e preservados os registros de proposta, ação executada, resultado e interpretação. A disciplina fundamenta o procedimento em reconhecimento e coleta de informações, comunicação TCP/HTTP e análise de logs, credenciais/autenticação e acesso a recursos web, sem extrapolar para ataques não cobertos pelo laboratório.

O escopo foi fixado exclusivamente no Juice Shop do KIT11. Não houve testes ofensivos em WordPress, Nextcloud, pfSense, máquinas de terceiros ou endereços da Internet. A análise não pressupõe que todos os comportamentos observados sejam falhas de segurança.

## 2. Laboratório, agente e método

### 2.1 Arquitetura e isolamento

A aplicação foi executada em um container Docker **Rootless**, com a imagem fixada em `bkimminich/juice-shop:v17.3.0`. A porta interna 3000 foi exposta no próprio Ubuntu em **127.0.0.1:3000**, usada pelo agente, e na interface privada em **10.0.80.3:3001**, usada pelo Kali por OpenVPN. O Ollama com o modelo **`qwen3:4b-instruct`** permaneceu acessível apenas pelo loopback do KIT11 em **127.0.0.1:11434**. Os serviços preexistentes do laboratório não foram alterados durante as três investigações.

A conectividade foi verificada a partir do Kali: via VPN, o Juice Shop respondeu **HTTP 200** em `10.0.80.3:3001`. Sem VPN, uma tentativa de conexão à interface WAN do pfSense (`192.168.20.31:3001`, em 27/10/2026, 15:04:05 -03) resultou em **timeout**, HTTP 000 e código 28 do curl. As capturas de regras WAN/NAT não exibiam permissão explícita de encaminhamento dessa porta. Esses fatos sustentam **bloqueio pelo caminho medido**; não constituem prova universal de isolamento diante de todas as possíveis regras, interfaces ou origens.

Scripts de inicialização e restauração validam identidade do container, imagem e bindings antes de operações destrutivas. Os registros das sessões principais informam restauração para estado conhecido antes de cada investigação, além da confirmação HTTP de disponibilidade.

### 2.2 Ferramentas, decisões e trilha de evidências

O agente Python oferece três ferramentas: **Nmap**, restrito a uma varredura TCP da porta 3000 em loopback; **HTTP GET**, limitado a caminhos relativos do Juice Shop; e **HTTP POST**, com corpo JSON e validações. O programa não admite comandos arbitrários de shell escolhidos pelo LLM, não segue redirecionamentos externos e limita ações, duração e tamanho das saídas. A escolha de ferramenta e parâmetros é proposta pelo Qwen com base no objetivo e nas evidências disponíveis.

O planejamento prévio estabeleceu hipóteses, candidatos de rota, controles, critérios de refutação e condições de parada. Os objetivos fornecidos ao modelo incluíram **candidatos já previstos no plano**, mas não impuseram uma sequência obrigatória de ações. Portanto, não é adequado caracterizar essas rotas como descobertas independentes do modelo. O grupo declarou aprovação do planejamento; a documentação final dessa deliberação e a condição formal de elaboração do plano exigem revisão acadêmica.

As execuções principais utilizaram um **procedimento de revisão técnica delegado**, que registrou as avaliações e justificativas antes de executar ações. **As decisões individuais dessas sessões históricas não foram entradas humanas diretas; na INV-01-B posterior, Nicholas decidiu pessoalmente.** A autorização geral do responsável, as avaliações automatizadas e a futura validação acadêmica são registros distintos. A adequação desse procedimento ao requisito original de supervisão humana deve ser ratificada com o professor antes da versão final.

Os arquivos JSONL privados preservam IDs de sessão, proposta, execução e resultado; relatórios públicos apresentam apenas resumos e identificadores. As execuções principais registraram **3 resultados na INV-01, 2 na INV-02 e 3 na INV-03**, todos associados aos cenários respectivos. A sessão inicial interrompida foi preservada, mas não foi contabilizada como uma investigação completa.

## 3. Investigações e evidências

### 3.1 INV-01 — Reconhecimento e enumeração

**Hipótese H1:** a aplicação está acessível na porta prevista e expõe informações públicas identificáveis, mas a confirmação do serviço requer correlacionar evidências TCP e HTTP. O plano previa uma consulta de disponibilidade, observação da porta, versão do Juice Shop e, de forma opcional, um produto público.

Na sessão principal `01371920529f44c4b11c395bfe367e5e`, o Qwen propôs sucessivamente uma consulta de versão, Nmap e consulta de produto. O primeiro GET a `/rest/admin/application-version` retornou **HTTP 200**, com versão **17.3.0** (`result_id=fe55f482885f488fa472d5f7321970c5`). O Nmap observou **3000/tcp open** (`result_id=45ea687333f0430ea1b19a9d28072980`); não foi empregado o parâmetro de detecção de versão `-sV`, de modo que um rótulo de serviço associado à porta não identifica a aplicação. Por fim, `/api/Products/1` respondeu **HTTP 200** com um objeto de produto público (`result_id=513723cff92e42b2bdf9130c71b3f2f6`).

**Interpretação:** H1 foi sustentada nos limites dessas três observações e da identidade do container validado. Não foram demonstradas vulnerabilidade, enumeração indevida, exposição de todas as APIs ou qualquer comprometimento do serviço. Na análise do ciclo, uma alegação prematura do modelo sobre cruzamento com Nmap foi corrigida antes da medição TCP; posteriormente, o modelo também interpretou o nome convencional `ppp` exibido pelo Nmap como se fosse um diagnóstico de protocolo, extrapolando a saída real.

### 3.2 INV-02 — Comportamento de autenticação perante entradas inválidas

**Hipótese H2:** variações controladas de entradas inválidas poderiam ocasionar respostas de validação ou autenticação distintas; qualquer diferença exigiria evidência suficiente antes de inferir enumeração de usuários ou bypass.

Foi utilizado exclusivamente `POST /rest/user/login`, com identificador fictício fixo `af_inexistente_01@kit11.invalid`. A variável foi o campo de senha: **B**, senha vazia; **A**, texto de teste inválido. Na sessão `1ae38ffd4ed54a308ec9bd16c5017800`, o Qwen escolheu B antes de A. Ambas as execuções retornaram **HTTP 401**, tipo `text/html; charset=utf-8` e o mesmo corpo **`Invalid email or password.`** com 26 bytes, sem truncamento (`result_id=c3a3deedc7924c769c1a4635c1cdf47f` e `e32b00e3c32744fb82587a270a5c80d2`). Isso não significa que todos os cabeçalhos fossem idênticos; o campo `Date` variou.

**Interpretação:** a expectativa de diferença entre A e B **não se confirmou nas respostas medidas**. A observação não demonstra bypass, enumeração de contas nem segurança geral do login. Não foram executadas força bruta, credenciais reais ou a variante opcional com campo omitido. O modelo antecipou uma comparação quando só B havia sido executada e, em outro ponto, descreveu o e-mail como variável, embora os corpos reais mantivessem esse valor fixo. O confronto com os parâmetros registrados permitiu corrigir a narrativa.

### 3.3 INV-03 — Exposição de recursos e tratamento de caminhos

**Hipótese H3:** pode existir listagem pública de recursos relacionados a arquivos, mas sua acessibilidade não prova, isoladamente, exposição indevida, inclusão local/remota de arquivos (LFI/RFI) ou ausência de controles.

Na sessão `6e1489236a7b49e1ac57abcfccdc8347`, o GET de referência a `/` respondeu **HTTP 200**; o HTML foi truncado no log (`result_id=3fa447a6491141bfa8b20b7390563d19`). O GET `/ftp/` também retornou **HTTP 200**, com conteúdo interpretável como **listagem pública de nomes de arquivos**, inicialmente marcado sem truncamento; comparação posterior encontrou 11025 bytes registrados contra 11079 declarados, sem comprovação de completude (`result_id=41ee9e9701f34ace8b340e8327aca1ec`). Não houve download dos arquivos listados. O controle `/ftp/arquivo-inexistente-af.txt` recebeu **HTTP 403**, com mensagem **`Only .md and .pdf files are allowed!`** (`result_id=ec76542988d04dafa7e046553aa2640b`).

**Interpretação:** confirmou-se a presença de listagem HTTP pública; não se comprovou conteúdo sensível, acesso indevido ou LFI/RFI. O controle negativo tem um problema de desenho: utiliza simultaneamente arquivo **inexistente** e extensão **não permitida**. Assim, o 403 é compatível com filtro de extensão e **não isola o efeito da inexistência do arquivo**. Encerrar diante da restrição, sem tentar contorná-la ou acessar documentos potencialmente privados, preservou os limites do experimento. O modelo também extrapolou ao descrever a listagem como não sensível sem examinar os arquivos e ao associar o nome `/ftp/` ao protocolo FTP sem evidência de sessão FTP.

## 4. Discussão crítica: planejamento, IA e limites da evidência

A comparação dos três casos mostra que a escolha dinâmica pode ser **útil, mas não garante avaliação semântica correta**. Na INV-01, após a correção de uma inferência sobre Nmap, a ferramenta seguinte proposta foi justamente Nmap; isso é compatível com adaptação ao histórico, **sem comprovar nexo causal exclusivo**. Na INV-02, a ordem B→A foi diferente da ordem do quadro de planejamento. Na INV-03, a sequência coincidiu com os controles previstos; nesse caso, não se deve alegar criatividade ou descoberta independente das rotas.

A limitação mais clara ocorreu na **primeira sessão interativa da INV-01**, preservada com `run_id=f13a210f91d4440480f74eceb6b17862`. A resposta GET `/` indicava `Content-Length: 80117`, enquanto a ferramenta registrava no máximo 16.384 bytes, marcados por `truncated=true` (`result_id=36e3c3e4cc8443dda703cda8ee39d3c8`). Mesmo assim, a interpretação do Qwen afirmou que havia recebido **HTML completo**, apesar de observar em outro campo que a resposta estava truncada. A contradição revela um problema relevante: o texto de um LLM pode parecer plausível e simultaneamente contrariar metadados do próprio experimento. Essa sessão foi interrompida e **não** possui conclusão humana final; sua evidência foi reaproveitada apenas na análise crítica.

Outras limitações observadas foram (i) antecipar resultados ainda não medidos; (ii) confundir rótulo de porta com identificação de aplicação; (iii) narrar variáveis diferentes das realmente enviadas; (iv) inferir inocuidade de arquivos apenas pelos nomes; e (v) perder parte do contexto porque a interpretação isolada recebe sobretudo o resultado atual. Uma falha de integração no registrador de eventos interrompeu uma tentativa parcial; ela foi corrigida e testada, **sem ser falsamente atribuída ao modelo**. A decisão metodológica foi privilegiar checagem cruzada com saída técnica e interrupção diante de dados insuficientes, preservando os erros para análise posterior.

Como aprendizado experimental, foi essencial separar **hipótese**, **proposta do modelo**, **resultado de ferramenta**, **avaliação intermediária** e **conclusão**. Uma resposta 200 não equivale a acesso indevido, dois 401 não provam segurança e uma restrição 403 não demonstra autorização adequada para todos os recursos. A principal fraqueza metodológica do plano ocorreu no controle negativo da INV-03, que não isolou uma única variável; reconhecer essa limitação é mais sólido que declarar uma vulnerabilidade sem teste adequado.

## 4.1 Replay com evidências simuladas em 19/11/2026

O Qwen local recebeu dois pedidos exploratórios com o mesmo contexto sintético e, em outra execução, sete pares planejados: três de sensibilidade, três de apresentação do histórico e um controle idêntico. Em ambos os casos nenhuma proposta foi executada. A primeira execução produziu duas respostas com a mesma ferramenta e textos diferentes; na série de 14, o controle idêntico produziu respostas iguais. Esses resultados mostram que temperatura zero não garante estabilidade, mas uma repetição não permite estimar frequência nem provar causalidade.

A série de 14 gerou 14 propostas válidas pelo validador básico. Oito foram classificadas fora da lista estática do cenário, porém a lista de ferramentas permitidas não havia sido enviada no contexto ao modelo. Esse defeito do desenho impede interpretar a contagem como taxa justa de desobediência. Os testes usaram fatos simulados, e as condições de memória não demonstram equivalência completa de conteúdo. Uma repetição corrigida foi interrompida antes de receber resposta.

O orçamento proposto era de até 14 pedidos. O Codex realizou duas consultas exploratórias adicionais e iniciou mais uma antes de interrompê-la: **17 solicitações, 16 respostas registradas e uma solicitação sem resposta registrada**. O excesso foi um desvio de execução, registrado sem atribuí-lo ao Qwen. Esse replay não executou ferramentas; as sessões 03B reais posteriores são distintas e descritas a seguir.

## 4.2 Investigações 03B e origem das decisões

Em 19/11, Nicholas aprovou pessoalmente os três GETs da INV-01-B: raiz, versão 17.3.0 e produto público responderam 200. Nas demais sessões, a pedido dele, o Codex revisou e justificou cada proposta como delegado; Nicholas relatou que o professor permitiu a adaptação, ainda não verificada independentemente. Na INV-02-B, controles A/B/C retornaram 401 com corpos iguais de 26 bytes; B/C foram alterações do Codex após repetição pelo modelo. Não se demonstrou bypass ou segurança geral.

Duas tentativas da INV-03-B observaram listagem `/ftp/` HTTP 200 com 11025 bytes contra Content-Length 11079; a completude não foi comprovada. Na primeira, `.txt` retornou 403, misturando extensão e existência; o controle `.md` não foi executado. Na repetição, o modelo afirmou completude apesar do indicador de truncamento e mencionou resposta `.md` não observada. A causa da diferença de bytes não foi estabelecida. Restaurações foram especificamente autorizadas. Logs e IDs constam da matriz privada/pública resumida do projeto.

Nicholas relatou também em 19/11 VPN HTTP 200, WAN sem VPN timeout e inspeção visual sem regra WAN/NAT para 3001; Codex não executou esses testes nem viu as telas. As fontes originais e hashes continuam pendentes; o timeout limita-se ao caminho testado.

## 5. Reprodutibilidade, limitações e conclusão

O laboratório utiliza um alvo único, versões fixadas, restauração controlada e registros correlacionados por IDs. Há documentação de 61 testes de software descobertos, dos quais **58 foram aprovados e 3 integrações opt-in foram ignoradas** na suíte registrada; esses testes não devem ser confundidos com as três execuções reais do Qwen e do Juice Shop. Para reproduzir os cenários é necessário validar novamente o estado do KIT11, as versões, os bindings do container e o modelo local; consultar `plano_humano.md`; reiniciar o Juice Shop por procedimento verificado; e preservar um registro separado por investigação. Os resultados brutos podem ser recuperados pelos `run_id` e `result_id` na matriz do projeto, sem publicar credenciais ou corpos sensíveis.

**Conclusão:** dentro dos limites testados, a abordagem integrou propostas dinâmicas do Qwen3 4B e evidências de Nmap/HTTP para sustentar H1, refutar a expectativa de diferença entre duas variantes inválidas em H2 e sustentar apenas parcialmente H3. A contribuição mais significativa foi identificar, a partir de registros auditáveis, pontos em que a interpretação produzida pela IA ultrapassou aquilo que as ferramentas realmente haviam demonstrado. Nenhum bypass, LFI/RFI, comprometimento ou falha generalizada de autenticação foi comprovado.

**Limitações e pendências para submissão:** validar os logs primários e selecionar capturas redigidas; completar nomes dos integrantes e data exata da aprovação; explicitar e obter aceite formal para a modalidade de revisão por ação usada nas novas sessões, pois ela **não constitui intervenção humana pontual**; avaliar eventual implicação da origem do planejamento para a rubrica; confirmar escopo do teste de isolamento WAN; revisar a diagramação do PDF e preparar o vídeo de até dez minutos. O relatório não deve ser entregue como se esses portões estivessem resolvidos.

## Fontes do projeto e evidências

1. **Enunciado e rubrica:** `docs/AF - Tecnologias Hackers 26-2.pdf`; síntese: `docs/RUBRIC.md`.
2. **Planejamento:** `plano_humano.md`, hipóteses H1–H3, controles e limites.
3. **Arquitetura/engenharia:** `README.md`, `agent.py`, `docs/STATE.md`, `docs/ENGENHARIA_BLOCO02.md`.
4. **Sessões técnicas:** `docs/investigacoes/INV-01/resumo.md`, `INV-02/resumo.md`, `INV-03/resumo.md`.
5. **Análise comparativa:** `docs/investigacoes/ANALISE_BLOCO03.md` e `docs/investigacoes/MATRIZ_EVIDENCIAS.md`.
6. **Fonte primária:** `logs/INV-01/<run_id>/sessao.jsonl`, `logs/INV-02/<run_id>/sessao.jsonl`, `logs/INV-03/<run_id>/sessao.jsonl`, preservados **somente no servidor**, com acesso privado.
