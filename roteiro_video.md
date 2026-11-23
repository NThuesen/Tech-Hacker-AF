# Roteiro de gravação — 8 min 15 s

Grave a tela com os documentos já abertos. Use a INV-01-B registrada em 19/11 como demonstração principal. Leia somente os trechos entre aspas. As instruções de tela ficam fora da fala. O tempo inclui pausas breves para apontar as evidências.

Antes de gravar, abra quatro abas nesta ordem: [relatório PDF](docs/RELATORIO_ENTREGA.pdf), [trilha da INV-01-B](docs/video/EVIDENCIA_INV01B.md), [matriz 03B](docs/03b/MATRIZ_COMPARATIVA.md) e [checklist da rubrica](CHECKLIST_RUBRICA.md). Use a visualização Markdown do GitHub ou do editor. Nenhum comando é necessário.

## 0:00–0:55 — Pergunta da AF

**Tela:** página 1 do relatório. Aponte para o título e os três cenários.

> “Olá, eu sou Nicholas Thuesen. Este é o trabalho de Avaliação Final de Tecnologias Hackers, da equipe com Alison Araujo. Investigamos como um modelo de linguagem local pode ajudar a escolher ferramentas e interpretar resultados de segurança. Usamos somente a instância do OWASP Juice Shop do nosso kit. A pergunta foi em quais decisões o modelo ajudou e onde a evidência exigiu revisão. Organizamos o trabalho em três investigações: reconhecimento HTTP, comportamento diante de entradas inválidas no login e tratamento de recursos. Vou mostrar a primeira do início ao fim usando o registro da sessão real de 19 de novembro. A apresentação é uma leitura comentada dessa sessão já encerrada.”

## 0:55–1:50 — Ambiente e ciclo do agente

**Tela:** no relatório, mantenha visíveis a arquitetura e o fluxo. Aponte para Qwen, terminal e Juice Shop.

> “O agente Python e o Ollama rodaram no Ubuntu do KIT11. O modelo foi o Qwen3 4B e a aplicação foi o Juice Shop 17.3.0 em Docker Rootless. O Kali acessou o laboratório pela VPN. Na verificação que relatei, houve HTTP 200 pela VPN e timeout sem VPN. Esse teste vale para o caminho medido. O agente tem Nmap, GET e POST com ferramentas, parâmetros, alvo e tempo limitados. A cada ciclo, o Qwen sugere uma ação. O supervisor vê os parâmetros e pode aprovar, modificar ou rejeitar. Depois da execução, o resultado volta ao modelo para interpretação. O supervisor então decide se a investigação continua. Os identificadores permitem conferir essa ordem depois.”

## 1:50–2:40 — Hipótese e aprovação do plano

**Tela:** abra a trilha INV-01-B. Mostre a hipótese, os eventos de aprovação do plano e a primeira linha da tabela.

> “Na INV-01-B, a hipótese foi que os dados disponíveis por HTTP poderiam confirmar a identidade do serviço, a versão e a origem de um registro de catálogo. O plano já incluía as rotas candidatas e o Nmap como opção. Antes de começar, eu revisei o plano e o adendo no terminal. Os eventos de aprovação guardam as referências das versões usadas. A sequência de ferramentas ainda dependia das propostas do modelo e da minha decisão por ação. O registro confirma a aprovação antes desta sessão. A autoria inicial do plano sem apoio do modelo é uma questão separada e permanece sem comprovação documental suficiente.”

## 2:40–3:55 — Primeira proposta e primeira decisão

**Tela:** primeira linha. Mostre, em ordem, GET, aprovação, HTTP 200 e interpretação. Aponte para o ID da decisão no quadro de vínculos.

> “A primeira proposta do Qwen foi consultar a raiz com GET. Eu aprovei essa ação no terminal. O resultado foi HTTP 200 com HTML do Juice Shop. O corpo estava limitado pelo tamanho máximo registrado, e o Qwen reconheceu o truncamento nessa sessão. A evidência era suficiente para dizer que a interface web respondia. Ainda faltavam dados sobre a versão e sobre o catálogo. Por isso, depois de ler a interpretação, decidi continuar. Esse é um exemplo dos dois momentos de supervisão: a autorização antes da ferramenta e a avaliação depois que o modelo recebeu o resultado. O identificador da decisão e o do resultado permitem localizar os eventos correspondentes no registro privado.”

## 3:55–5:15 — Dois novos resultados e conclusão humana

**Tela:** segunda e terceira linhas, depois conclusão. Deixe os resultados e a coluna de intervenções visíveis.

> “O Qwen propôs então consultar o endpoint de versão. Eu aprovei a segunda ação. O resultado HTTP 200 informou a versão 17.3.0. Na proposta seguinte, o modelo mencionou essa versão que já tinha sido observada e sugeriu consultar um produto para verificar os dados do catálogo. Eu aprovei a terceira ação, que também retornou HTTP 200, com um registro de produto em JSON. Depois de revisar a interpretação, decidi encerrar. Para o objetivo de reconhecimento HTTP, tínhamos evidência sobre a interface, a versão e um produto. A seleção foi contextual. Os caminhos já constavam entre os candidatos, por isso a contribuição do modelo foi escolher a próxima medição e interpretar a resposta. O alcance da conclusão é o serviço local e as respostas observadas. Nmap aparece no histórico do projeto, mas esta sessão demonstrada usou apenas GET.”

## 5:15–6:45 — Comparação, resultado negativo e falha da IA

**Tela:** abra a matriz 03B. Aponte para A/B/C, depois para a repetição da INV-03-B e os tamanhos.

> “As duas outras investigações tiveram decisões do Codex por delegação, registradas com essa autoria. No login, a senha inválida, a senha vazia e a senha omitida deram três respostas 401 com o mesmo corpo de 26 bytes. O Qwen repetiu propostas, então o revisor modificou duas e confirmou cada alteração. O resultado negativo vale para aquelas entradas. Em recursos, a listagem respondeu 200. O controle com extensão não permitida retornou 403, de modo que extensão e existência ficaram misturadas. Na repetição, a listagem declarou 11.079 bytes e o cliente registrou 11.025. O modelo chamou a listagem de completa apesar do indicador de truncamento. O revisor comparou os valores e encerrou sem solicitar o controle de extensão permitida. Depois, uma fixture reproduziu a diferença de tamanho em memória e ajudou a melhorar o diagnóstico do cliente. A causa exata na resposta histórica continua indeterminada.”

## 6:45–8:15 — Alcance dos resultados e encerramento

**Tela:** volte ao relatório para a página 5 e depois mostre os itens de supervisão, evidência e análise crítica no checklist.

> “O melhor exemplo de adaptação foi a proposta de verificar um produto depois de observar a versão. No login, o modelo precisou de correção para completar as comparações planejadas. No teste de recursos, confundiu o aspecto da página com a integridade do corpo. Os replays usaram entradas simuladas e não executaram as ações sugeridas. O histórico de replay excedeu o orçamento previsto, o que limita aquela comparação. Na sessão de reconhecimento, eu fiz a supervisão e a conclusão pessoalmente. Nas sessões delegadas, a autorização geral e a autoria das decisões ficaram registradas separadamente, e o enquadramento acadêmico depende do aceite da adaptação. O aprendizado foi comparar os registros de ferramenta, as justificativas e a interpretação do modelo antes de concluir. Os três casos mostram contribuições e limitações diferentes. Encerramos com observações verificáveis sobre o ambiente medido e com o controle de ausência da INV-03-B explicitamente inconclusivo. Obrigado.”

## Plano alternativo

Se Juice Shop, Ollama, VPN ou GitHub estiverem indisponíveis, use o [PDF local](docs/RELATORIO_ENTREGA.pdf) e a [trilha local da INV-01-B](docs/video/EVIDENCIA_INV01B.md) no editor. As páginas 2 e 4 do PDF reproduzem a sequência supervisionada e a comparação das investigações. Na abertura, mantenha a frase sobre a sessão já encerrada. Use os IDs visíveis para identificar a evidência. Para preparar e conferir a gravação, siga o [checklist de uma página](docs/video/CHECKLIST_GRAVACAO.pdf).
