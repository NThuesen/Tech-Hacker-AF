# Evidências técnicas do bloco 02 — 2026-10-27

Estes ensaios verificam software e integração no KIT11. Não são as três investigações acadêmicas, não aprovam `plano_humano.md` e não comprovam vulnerabilidades. O usuário autorizou os testes técnicos e a exceção de dependência em ADR-007.

## Ambiente e escopo

Python 3.12.3; Ollama 0.40.11 com `qwen3:4b-instruct` (`0edcdef34593`, Q4_K_M, 4B); Juice Shop v17.3.0 em Docker Rootless. Alvos fixos de ferramentas: `127.0.0.1:3000`; API do modelo: `127.0.0.1:11434`. Nenhuma configuração de rede, Docker, SSH ou serviços foi alterada no bloco 02.

## Implementação

O agente preserva as ferramentas `nmap`, `http_get` e `http_post` e o contrato `hipotese`, `interpretacao`, `ferramenta`, `parametros`. O CLI restringe o alvo a loopback. Porta, método, executável e opções de Nmap são definidos pelo código; o modelo escolhe ferramenta, caminho e corpo JSON dentro da validação. Não há comando de shell livre, proxy ou redirecionamento.

Cada ciclo registra solicitação/proposta, decisão e justificativa, ação final, execução, resultado com duração, interpretação separada e decisão após interpretação. `run_id`, `step_id`, `proposal_id`, `execution_id`, `result_id` e `event_id` permitem a ligação entre eventos; a interpretação deve devolver o ID exato do resultado. A última execução também é interpretada antes de encerrar, sem executar uma ferramenta adicional. Não há aprovação automática no CLI.

JSON duplicado, constantes não JSON, ferramentas/argumentos desconhecidos, geração incompleta, envelope inválido, conteúdo excedente e interpretação vinculada a outro resultado são rejeitados. Falha do modelo encerra o ciclo, com pendência explícita; falha de escrita impede a execução seguinte. Uma modificação inválida volta à revisão e uma modificação válida exige segunda aprovação.

HTTP tem prazo total de 8 s no CLI síncrono Linux (inclusive resposta lenta), corpo até 16 KiB, POST objeto JSON UTF-8 até 4 KiB e cabeçalhos de saída restritos. Nmap usa uma porta e timeout de processo de 10 s. API do modelo tem timeout de 180 s, envelope até 100 kB, contexto até 16 kB, últimas oito entradas com remoção das mais antigas e até 40 chamadas por sessão de 20 propostas, sem retry automático. Corpos/saídas maiores que 2048 bytes são resumidos no contexto por prefixo, tamanho e SHA-256; o resultado limitado original permanece no log. O modelo recebe instruções e dados em campos separados, mas prompt injection não tem proteção absoluta: a validação e a supervisão continuam necessárias.

Logs novos são 0600, em diretório do usuário 0700; links, hardlinks, arquivos não regulares e permissões compartilhadas são rejeitados. `logs/` e arquivos `.jsonl` são ignorados pelo Git. A gravação usa append e fsync, mas não garante inviolabilidade contra o proprietário do arquivo. Campos de senha/token/cookies e objetos JSON aninhados são redigidos; texto livre ou JSON truncado ainda pode conter dados sensíveis. O terminal mostra os parâmetros completos das propostas para permitir revisão efetiva; capturas também exigem revisão antes de compartilhar. O diretório local `logs/`, que estava em 0775, foi restringido a 0700 nesta sessão.

## Testes locais com fixtures e mocks explícitos

`python3 -m unittest discover -s tests -v` deixa integrações reais desabilitadas por padrão. As fixtures verificam rejeição sem execução, modificação com segunda aprovação, ação final correta, registro do último resultado, interpretação malformada, IDs, limites, falha de log, interrupção sem conclusão presumida, JSON inválido, UTF-8, redação de segredos, links/permissões e prazo de resposta HTTP lenta. HTTP simulado é servidor de loopback; modelo e Nmap são substituídos nos testes unitários. Essas decisões injetadas não são decisões humanas reais.

Verificação final: 32 testes descobertos, 29 passaram e três integrações opt-in foram ignoradas, em 1,132 s. As três integrações reais foram executadas separadamente conforme os registros abaixo. `git diff --check` passou.

## Ensaios reais automatizados

Com autorização técnica, executar `KIT11_REAL_TESTS=1 python3 -m unittest discover -s tests -p test_engineering_real.py -v`. Exige os serviços já ativos; não instala nem inicia serviços. O gate técnico só executa uma proposta se for Nmap na porta fixa ou GET `/` ou `/rest/admin/application-version`. As coletas A/B usam somente GET público de produto. Os gates são rotulados como automatizados; propostas condicionais são registradas sem execução.

1. **Primeira tentativa, falhas preservadas:** `run_id=c44eb79d07ff4bd981079a2cb5aa3432`, `logs/engenharia-c44eb79d07ff4bd981079a2cb5aa3432.jsonl`. Sob um objetivo genérico de catálogo, tanto HTTP 200 (`/api/Products/1`) quanto 404 (`/api/Products/0`) levaram à proposta GET `/api/Products`. A asserção condicional falhou. A interpretação da página inicial também atingiu 180 s; o journal local do Ollama mostrou processamento de cerca de 7 mil tokens. O unittest registrou uma falha e um erro. Isso motivou delimitar o objetivo de engenharia e reduzir o trecho de corpo enviado ao modelo, sem codificar uma tabela de decisões no agente.
2. **Comparação após ajuste, dois testes passaram:** `run_id=1779e55fd5ec4ddcb037542bad92d041`, `logs/engenharia-1779e55fd5ec4ddcb037542bad92d041.jsonl`; 101,552 s no total. Para o mesmo objetivo delimitado (ler um único produto e identificar a versão), a evidência 200 levou à proposta GET `/rest/admin/application-version`; a evidência 404 levou a GET `/api/Products/1`. Resultado A `d9e89318e3324d8ab4925cd7c4d4be3b`, proposta A `130387198e9e4ed69466eb387ec5fcbc`; resultado B `171c666a0ada4e6693bb5473fe164b81`, proposta B `ed310896eb674c76bd5de3f18d97df6c`. A escolha veio do Qwen, sem if/else de seleção no código. Na integração simples, o Qwen escolheu GET da versão, recebeu HTTP 200 e produziu interpretação vinculada; Nmap real, executado como fixture técnica identificada, observou TCP/3000 aberta e também foi interpretado. O rótulo `ppp` exibido pelo Nmap é associação por número de porta, não identificação do protocolo da aplicação.
3. **Regressão do HTML extenso passou:** `run_id=e9d9c24ba7bb46aca9e6fa3d5ca8dc59`, `logs/engenharia-e9d9c24ba7bb46aca9e6fa3d5ca8dc59.jsonl`. Executado isoladamente com `PYTHONPATH=tests KIT11_REAL_TESTS=1 python3 -m unittest test_engineering_real.RealEngineeringTests.test_large_real_http_result_uses_bounded_context -v`; o GET real da raiz retornou 200, o trecho de contexto foi marcado como truncado a 2048 bytes e houve interpretação vinculada. Teste concluído em 22,839 s, sem repetir os demais ensaios.

Esses resultados demonstram adaptação no caso observado, não confiabilidade semântica geral nem garantia de repetição. O modelo ainda generalizou indevidamente a validade de índices positivos a partir de um único 404 e usou expressões excessivamente confiantes. Uma resposta estruturalmente válida não é uma conclusão verificada.

Os JSONL integrais permanecem privados no host e fora do commit. Este documento contém somente o resumo revisado e os identificadores para localização.

## Intervenção humana real via conversa

`logs/engenharia-humana-bloco02.jsonl`, `run_id=0a55a4672c3c40f0b4cb31a36edccae5`. O Qwen havia proposto GET `/api/Products`. O usuário modificou para `/rest/admin/application-version`, com justificativa de limitar a leitura à versão. A ação modificada foi revalidada e o usuário deu uma segunda aprovação explícita. Só então o desenvolvedor chamou a ferramenta e a interpretação do agente, com origem `usuario_chat` nos eventos, sem simular entradas de terminal.

O resultado `733b497e7a4d4774888564db2b64a04b` retornou HTTP 200 e `{"version":"17.3.0"}`. A interpretação recebeu esse ID, mas inferiu indevidamente a existência de uma API de produtos e sugeriu ampliar a leitura. Esse erro foi apresentado ao usuário, que decidiu: **“Encerrar: versão validada; rejeitar as inferências sobre catálogo.”** A decisão posterior e a conclusão foram acrescentadas ao JSONL com origem `usuario_chat`. Nenhuma ferramenta adicional foi executada após essa decisão.

## Pendências acadêmicas

Autenticação real por POST, cookies e investigações ainda dependem do planejamento do grupo; o suporte JSON atual foi mantido sem ampliar cabeçalhos ou acesso. O plano acadêmico, acesso Kali, isolamento WAN e as três investigações permanecem pendentes. O bloco 03 depende de autorização explícita.
