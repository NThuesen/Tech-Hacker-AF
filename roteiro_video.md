# Roteiro de gravação — AF Tecnologias Hackers

**Versão para a apresentação final:** fala natural + demonstração real já gravada no KIT11.

**Meta de duração:** aproximadamente **8 min 30 s a 9 min**, incluindo os quatro cortes do terminal (cerca de 1 min 05 s). Limite da AF: 10 minutos. Os horários abaixo são referências de edição, não uma obrigação de falar devagar ou preencher cada segundo.

## Antes de apertar REC

Grave pelo notebook Windows. O KIT11 pode permanecer desligado. Abra o roteiro no celular ou em outra tela que não esteja sendo capturada. Deixe estas quatro abas do navegador abertas, na ordem:

| Aba | Arquivo | Deixe preparado |
|---|---|---|
| 1 | [Relatório final — PDF](docs/RELATORIO_ENTREGA.pdf) | Página 1, com o título e o início do relatório visíveis |
| 2 | [Trilha da INV-01-B](docs/video/EVIDENCIA_INV01B.md) | Início do arquivo, com a hipótese e a tabela dos três passos |
| 3 | [Matriz comparativa](docs/03b/MATRIZ_COMPARATIVA.md) | Início, com as três linhas INV-01, INV-02 e INV-03 |
| 4 | [Checklist da rubrica](CHECKLIST_RUBRICA.md) | Tabela de atendimento à avaliação |

Use zoom suficiente para ler o texto na gravação. Não abra os logs privados nem mostre credenciais. Não é necessário executar nenhum comando.

**Como usar este roteiro:** fale apenas o texto dos blocos **FALA**. As instruções **TELA** são ações de gravação e edição, não fazem parte da narração. Faça uma pausa breve ao trocar de aba. Pode gravar cada trecho separadamente e juntar no editor.

## Visão rápida do vídeo

| Tempo aproximado | Trecho | Tela |
|---|---|---|
| 0:00–0:45 | Introdução e objetivo | Aba 1 — PDF, página 1 |
| 0:45–1:45 | Laboratório e funcionamento | Aba 1 — arquitetura e fluxo |
| 1:45–2:05 | Introdução da demonstração | Aba 1, depois corte para o terminal |
| 2:05–3:10 | Demonstração real já gravada | Quatro vídeos do KIT11, em sequência |
| 3:10–4:00 | O que vimos na demonstração e hipótese da INV-01-B | Aba 2 — início |
| 4:00–5:25 | Investigação completa e decisões | Aba 2 — tabela dos três passos |
| 5:25–6:20 | Testes de login | Aba 3 — linha INV-02 |
| 6:20–7:35 | Teste de recursos e erro da IA | Aba 3 — linha INV-03 e tentativa adicional |
| 7:35–8:40 | Conclusão e limites | Aba 1 — página 5, depois aba 4 |

---

## 1. Introdução — 0:00–0:45

**TELA**
- Abra a **aba 1**, página 1 do relatório.
- Comece com o título e os nomes da equipe visíveis.
- Mantenha a tela parada enquanto apresenta o objetivo.

**FALA**

> Olá, professor. Eu sou Nicholas Thuesen, e esse é o trabalho de Avaliação Final de Tecnologias Hackers que desenvolvi junto com o Alison Araujo.
>
> A ideia do nosso trabalho foi entender até que ponto uma inteligência artificial consegue auxiliar uma investigação de segurança. Mais especificamente, queríamos saber se ela consegue escolher o que testar, interpretar os resultados e usar essas informações para decidir o próximo passo.
>
> Para isso, construímos um agente que roda localmente e fizemos três investigações em um ambiente controlado. Vou começar explicando como montamos esse ambiente, mostrar o agente funcionando e depois comentar os resultados que encontramos.

## 2. Como montamos o laboratório — 0:45–1:45

**TELA**
- Continue na **aba 1**.
- Role até a parte do relatório que descreve a arquitetura do laboratório e o funcionamento do agente.
- Quando falar do modelo, aponte para Qwen/Ollama; quando falar do alvo, aponte para Juice Shop; quando falar de supervisão, aponte para o fluxo de aprovação.
- Se necessário, avance para a página 2. Não abra o terminal ainda.

**FALA**

> Todo o ambiente principal roda em um mini computador Linux, que é o nosso KIT11. Nele temos o Juice Shop, uma aplicação criada justamente para o estudo de segurança, rodando em um container Docker.
>
> Nesse mesmo computador usamos o Ollama para executar o Qwen3, um modelo local de quatro bilhões de parâmetros. Também usamos uma máquina virtual Kali no notebook para verificar o acesso pela VPN. No teste que fiz, consegui acessar pela VPN, mas a tentativa sem VPN deu timeout. Isso vale para o caminho que testamos, não significa que comprovamos isolamento absoluto.
>
> O nosso agente foi desenvolvido em Python e tem três ferramentas disponíveis: Nmap, GET e POST. A parte mais importante é que o modelo não executa essas ferramentas sozinho. Ele propõe uma ação, alguém revisa essa proposta e só depois de uma aprovação ela é executada. O resultado volta para o modelo, que interpreta o que aconteceu, e o revisor decide se vale a pena continuar.

## 3. Introdução da demonstração — 1:45–2:05

**TELA**
- Ainda na aba 1, termine a explicação do fluxo.
- Ao acabar a fala abaixo, corte diretamente para o primeiro vídeo do terminal.

**FALA**

> Para mostrar isso na prática, gravei uma interação curta no próprio KIT11. É um ensaio de engenharia separado das investigações que usamos no relatório.
>
> Nesse exemplo, o objetivo é simplesmente descobrir a versão do Juice Shop por meio de uma consulta HTTP, sem alterar nada na aplicação.

## 4. Inserir os quatro vídeos já gravados — 2:05–3:10

**EDIÇÃO — não precisa gravar a tela novamente.**

Insira os quatro arquivos em ordem cronológica:

1. `Gravação de tela de 2026-11-23 19-42-04.webm`
2. `Gravação de tela de 2026-11-23 19-42-43.webm`
3. `Gravação de tela de 2026-11-23 19-47-27.webm`
4. `Gravação de tela de 2026-11-23 19-47-42.webm`

Confira a continuidade visual na prévia do editor. Preserve a sequência real de proposta, decisão, execução, interpretação e encerramento. Corte somente esperas e trechos redundantes; não reorganize decisões nem esconda limitações. Se faltar alguma tela, não simule uma nova.

Se quiser narrar sobre os cortes, use estas frases **somente quando o trecho correspondente estiver visível**. Não precisa ler tudo: são quatro comentários curtos, opcionais.

- **Proposta na tela:** “Aqui o Qwen escolheu fazer um GET no endpoint de versão.”
- **Aprovação na tela:** “Eu reviso a proposta, aprovo a consulta e explico por que ela faz sentido.”
- **Resultado na tela:** “A ferramenta retornou status 200 e informou a versão 17.3.0. Foram recebidos os vinte bytes declarados na resposta.”
- **Interpretação e encerramento:** “O modelo interpreta esse resultado, mas a versão pública não comprova uma vulnerabilidade. Com o objetivo atingido, podemos encerrar.”

Se preferir, deixe o trecho sem narração adicional e use a explicação do próximo bloco. Identifique-o como **“Demonstração — ensaio de engenharia, 23/11/2026”**. Não apresente esta gravação como parte da investigação de 19/11.

## 5. Da demonstração à primeira investigação — 3:10–4:00

**TELA**
- Volte à gravação do Windows.
- Abra a **aba 2 — Trilha da INV-01-B**.
- Deixe visíveis o cabeçalho da sessão e o parágrafo **Hipótese e plano**.
- Ao dizer “três consultas”, role até o começo da primeira tabela.

**FALA**

> Esse exemplo mostra o ciclo básico do agente, mas no trabalho nós queríamos ir além de uma consulta isolada. Por isso, fizemos três investigações com objetivos diferentes.
>
> Vou detalhar primeiro a investigação de reconhecimento, que eu supervisionei pessoalmente no dia 19 de novembro. A nossa hipótese era que, a partir de consultas HTTP, conseguiríamos identificar o serviço, descobrir a versão da aplicação e verificar se havia informações de catálogo disponíveis.
>
> O plano já previa algumas consultas possíveis e o uso de Nmap. Antes da sessão, aprovei o plano no terminal. O que o agente precisava decidir era quais dessas ações executar e em qual ordem. Temos o registro dessa aprovação prévia, embora não tenhamos comprovação suficiente de que a elaboração inicial do plano foi inteiramente sem IA.

## 6. INV-01-B — da hipótese à conclusão — 4:00–5:25

**TELA**
- Continue na **aba 2**. Mostre a tabela que tem as colunas **Ordem**, **Proposta do Qwen**, **Decisão de Nicholas**, **Resultado** e **Interpretação**.
- Ao falar da primeira ação, aponte para a linha **1 — GET /**.
- Na frase “o próximo passo”, desça o cursor para a linha **2 — versão 17.3.0**.
- Na frase “por último”, aponte para a linha **3 — produto**.
- Ao falar de rastreabilidade, role até a tabela de IDs e mostre as colunas de proposta, decisão e execução. Depois deixe a conclusão visível. Não é necessário ler os identificadores.

**FALA**

> Na primeira ação, o Qwen decidiu consultar a página inicial do Juice Shop. Eu aprovei, e a resposta foi HTTP 200, com o HTML da aplicação. Isso confirmou que a interface web estava respondendo.
>
> Só que ainda não sabíamos a versão, e a resposta da página inicial estava truncada pelo limite de captura. O modelo identificou essa limitação, então decidi continuar a investigação.
>
> O próximo passo foi consultar diretamente o endpoint de versão. Dessa vez recebemos um JSON com a versão 17.3.0. Depois de receber esse resultado, o Qwen sugeriu consultar um produto do catálogo, inclusive fazendo referência à versão que já tinha encontrado.
>
> Por último, aprovei essa terceira consulta, que retornou HTTP 200 e os dados de um produto em JSON. Com isso, tínhamos informação suficiente para concluir o reconhecimento HTTP e eu decidi encerrar.
>
> O interessante aqui é que o modelo não apenas sugeriu três ações: ele usou os resultados anteriores para justificar o próximo passo. As rotas já estavam previstas no plano, então o mérito do modelo foi a seleção e a interpretação, e não descobrir esses caminhos do zero.
>
> Cada proposta, aprovação e resultado tem um identificador que permite recuperar a sequência nos logs. A conclusão é limitada ao serviço que testamos. Não encontramos uma vulnerabilidade só por identificar a versão, e o Nmap, embora utilizado no histórico do projeto, não foi executado nessa sessão específica.

## 7. INV-02-B — comportamento do login — 5:25–6:20

**TELA**
- Abra a **aba 3 — Matriz comparativa**.
- Na tabela inicial, encontre **INV-02 — autenticação**.
- Deixe visíveis os resultados A/B/C (HTTP 401, 26 bytes) e a observação sobre as propostas modificadas.

**FALA**

> Na segunda investigação, mudamos o foco para o login. Queríamos ver se diferentes entradas inválidas produziriam comportamentos diferentes.
>
> Testamos três situações: senha incorreta, senha vazia e senha omitida. As três retornaram HTTP 401, com respostas iguais de vinte e seis bytes.
>
>
>
> Um ponto interessante é que o Qwen repetiu propostas no teste de login. O revisor precisou modificar duas delas para completar as três comparações planejadas. Ou seja, o modelo ajudou, mas não conduziu toda a investigação sozinho.
>
> E o resultado foi negativo para aquelas entradas: não observamos um bypass. Isso não significa que o login seja seguro contra qualquer tipo de ataque.

## 8. INV-03-B — quando a IA errou — 6:20–7:35

**TELA**
- Permaneça na **aba 3**.
- Aponte para a linha **INV-03 — recursos**, mostrando o HTTP 200 da listagem e o HTTP 403 do controle `.txt`.
- Depois role até o subtítulo **Tentativa adicional INV-03-B**.
- Deixe visíveis os números **11025** e **11079**, a indicação de truncamento e a informação de que o `.md` não foi executado.
- Ao mencionar a correção, mostre o parágrafo **Auditoria de 23/11** logo abaixo.

**FALA**

> A terceira investigação foi sobre como a aplicação trata o acesso a recursos. E esse acabou sendo o caso mais interessante para avaliar as limitações da IA.
>
> A listagem retornou HTTP 200, enquanto um controle com extensão TXT retornou 403. Mas isso, sozinho, não permitia separar a existência do arquivo da restrição de extensão.
>
> Quando repetimos o teste, percebemos uma inconsistência importante: o servidor declarou onze mil e setenta e nove bytes, mas o cliente recebeu onze mil e vinte e cinco. Mesmo com essa diferença, o Qwen afirmou que a listagem estava completa.
>
> Essa conclusão não era sustentada pelos dados. O revisor identificou o problema e encerrou a sessão sem executar o controle com extensão MD, porque não havia garantia de que a listagem estivesse completa.
>
> Depois, reproduzimos a diferença de tamanho em um teste simulado e melhoramos a forma como o agente identifica capturas incompletas. A causa exata da diferença original não pôde ser determinada.
>
> Preferimos, portanto, manter esse controle como inconclusivo, em vez de apresentar uma conclusão que os nossos testes não conseguiram demonstrar. Para mim, esse é um bom exemplo de por que a supervisão continua importante mesmo quando a resposta da IA parece convincente.

## 9. Conclusão — 7:35–8:40

**TELA**
- Volte à **aba 1 — PDF**, página 5, onde estão as conclusões do relatório.
- Durante a comparação dos três casos, mantenha a conclusão visível.
- Quando mencionar as evidências e limitações, abra a **aba 4 — Checklist da rubrica** e mostre as linhas de supervisão, planejamento e análise crítica.
- Termine com o relatório novamente na tela. Pode voltar à página 1 para finalizar.

**FALA**

> Olhando para as três investigações, a conclusão é que o Qwen consegue ser útil para organizar uma análise de segurança, principalmente na escolha de ferramentas e na interpretação inicial de resultados.
>
> Na primeira investigação, ele usou o contexto para selecionar as próximas consultas. Na segunda, precisou de intervenção para evitar repetições. E na terceira, apresentou uma conclusão que contradizia os dados recebidos.
>
> Também fizemos comparações com entradas simuladas, sem executar ferramentas nessas rodadas, mas o número de consultas do replay ultrapassou o orçamento previsto. Isso limita o alcance daquela comparação.
>
> Nosso principal aprendizado foi que a IA pode ajudar bastante no processo, mas a decisão final não deve depender apenas do que ela afirma. É necessário conferir os resultados, entender as limitações e registrar quem tomou cada decisão.
>
> O código, o relatório e as evidências estão organizados no repositório, com os registros privados preservados. Mantivemos também as pendências acadêmicas e o controle da terceira investigação como inconclusivo, de forma transparente.
>
> E é isso. Obrigado.

---

## Checklist final de gravação e edição

- [ ] Abrir as quatro abas antes de gravar; roteiro fora da tela capturada.
- [ ] Gravar a fala dos blocos 1–3 e 5–9 pelo Windows, com microfone.
- [ ] Inserir os quatro clipes do KIT11 entre os blocos 3 e 5; conferir a ordem.
- [ ] Identificar a demonstração de 23/11 como ensaio de engenharia, distinto da INV-01-B de 19/11.
- [ ] Verificar que as telas acompanham a fala, sem mostrar senhas, tokens ou logs privados.
- [ ] Exportar e conferir áudio, legibilidade e duração final inferior a 10 minutos.
- [ ] Fazer o aceite final da entrega.

**Alternativa offline:** baixe previamente o PDF e a trilha INV-01-B. As páginas 2 e 4 do PDF mostram a sequência supervisionada e a comparação das investigações. Use os quatro clipes locais para a demonstração. Não é necessário iniciar novamente o KIT11, Ollama, Juice Shop ou VPN.

O [checklist PDF anterior](docs/video/CHECKLIST_GRAVACAO.pdf) continua como referência geral; para a ordem das telas, duração e inserção da demonstração gravada, siga este roteiro atualizado.
