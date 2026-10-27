# Bloco 03 — comparação e análise crítica

Responsável acadêmico: Nicholas. Operação/revisão por ação: Codex delegado, conforme autorização explícita nesta conversa de 27/10/2026, motivada por dificuldade física no teclado. Nicholas relatou autorização do professor. A autorização humana para delegação é distinta das decisões técnicas do Codex; não foram fabricadas aprovações humanas. A revisão e o aceite acadêmico do grupo/professor permanecem PENDENTES. Bloco 04 não iniciado.

## Planejamento e comportamento observado

| Caso | Plano e variável | Comportamento do Qwen | Resultado técnico |
|---|---|---|---|
| INV-01 | Rede + HTTP; versão; um produto opcional | Versão → Nmap → produto 1; Nmap escolhido após correção do revisor | Porta aberta, versão 17.3.0 e produto público. H1 sustentada no escopo medido |
| INV-02 | Email/rota fixos; variar senha, A×B e C opcional | B (vazia) → A (inválida), fora da ordem do quadro | HTTP 401 e corpos iguais nos dois controles; diferença não observada |
| INV-03 | Referência HTTP, recurso candidato e inexistente; arquivo público opcional condicionado | GET / → /ftp/ → controle inexistente .txt | Listagem pública/200; controle/403 por extensão, sem isolar ausência; H3 parcial |

Os candidatos do plano foram informados ao modelo, sem sequência obrigatória. O Qwen escolheu as ferramentas/parâmetros; o Codex decidiu sobre as propostas reais. Não atribuir ao modelo descoberta independente de rotas previamente fornecidas. Os resumos individuais e a matriz abaixo distinguem fatos, inferências e correções.

## Limitações efetivamente observadas

1. **Truncagem e excesso de confiança:** a sessão original interrompida e a primeira tentativa delegada da INV-01 receberam HTML truncado; o Qwen afirmou HTML completo. O agente limita corpo a 16384 bytes e contexto a até 2048 bytes por saída. `Content-Length: 80117` evidencia a incompletude. O revisor corrigiu, sem preencher conteúdo ausente.
2. **Evidência antecipada:** na INV-01 o Qwen alegou cruzamento com Nmap antes de qualquer scan daquela sessão. Na INV-02 generalizou igualdade de variantes após somente B. A comparação posterior A×B foi feita de fato; seu resultado não torna correta a afirmação antecipada.
3. **Rótulo de serviço:** interpretou `ppp` no scan sem `-sV` como incompatibilidade com Juice Shop. O resultado comprova porta aberta; não identificação de aplicação. HTTP da instância validada sustentou a identificação e a versão.
4. **Descrição divergente dos parâmetros:** na INV-02 declarou variar email, embora o corpo mantivesse email e alterasse senha. O revisor conferiu os parâmetros concretos e corrigiu o relato.
5. **Contexto limitado:** interpretações recebem somente o resultado atual; a proposta seguinte recebe histórico compacto e avaliações do revisor. Isso favorece frases equivocadas sobre o que foi ou não testado na sessão. Senhas redigidas também reduzem o que o modelo vê. Logs primários e decisões distinguem os controles; não se ampliou coleta de credenciais para contornar isso.
6. **Especulação de rotas:** na tentativa delegada parcial da INV-01, `/api` foi rejeitada e `/api/v1` modificada por falta de evidência, antes da execução. No reinício, o objetivo incluiu candidatos do plano para reduzir ambiguidade. Essa alteração deve constar da metodologia.
7. **Falha do código, separada da IA:** duplicação de `operador` no logger interrompeu a primeira tentativa delegada antes da ação modificada. Corrigida e testada; registros mantidos. Não foi apresentada como erro do modelo nem como investigação concluída.

8. **Controle negativo inadequado:** na INV-03, o próprio plano usa arquivo inexistente `.txt`, mas a resposta foi 403 com restrição a `.md`/`.pdf`. O teste mistura extensão e existência; não se concluiu tratamento de ausência. A execução encerrou diante da restrição, sem contorná-la. O Qwen também afirmou ausência de sensibilidade na listagem sem ler os arquivos; o revisor corrigiu e nenhum documento foi baixado.

A mudança de ferramenta após uma correção é adaptação observável, sem experimento causal que isole a influência do revisor de todos os demais fatores. Schema válido e texto plausível não asseguram raciocínio correto.

## Alcance da evidência e integridade

Todas as ferramentas das investigações usam `127.0.0.1:3000`. Identidade e bindings do `kit11-juice` são verificados antes da restauração e de cada ação executada. A restauração foi autorizada previamente e o procedimento remove somente o ID validado. Nenhuma mudança de pfSense, firewall/NAT, OpenVPN, WordPress ou Nextcloud foi realizada; não houve teste de sistemas externos.

Nicholas reconfirmou HTTP 200 pelo Kali/OpenVPN em `10.0.80.3:3001`. Sem VPN, em 27/10/2026 às 15:04:05, acesso a `192.168.20.31:3001` resultou em timeout, HTTP 000 e curl 28, referência `~/af-wan-sem-vpn.txt`; capturas WAN/NAT sem permissão explícita TCP/3001. Trata-se de relato/evidência do responsável sobre bloqueio no caminho testado, não comprovação de isolamento absoluto. O Codex não refez esses testes externos.

JSONL, respostas HTTP limitadas, propostas, decisões e interpretações permanecem privados em `logs/`. As sínteses públicas contêm somente informação revisada e IDs; não incluem dumps, tokens, perfis VPN ou credenciais. A sessão original interrompida permaneceu byte a byte preservada, inclusive seu resumo e plano. Verificação estrutural de IDs não é atestado independente de autenticidade nem correção semântica.

## Pendências para o relatório final

- Revisão pelo grupo/professor da adaptação de acessibilidade e sua relação com o requisito de intervenção humana por ação no PDF; manter decisões delegadas identificadas.
- Revisão/conclusão acadêmica por Nicholas/grupo, sem atribuir ao Codex deliberações humanas.
- Selecionar capturas e trechos dos logs privados, revisar dados e relacionar cada alegação ao result_id; preservar arquivos primários completos fora do Git.
- Completar dados originais de autoria/deliberação do plano conforme os registros verdadeiros; não reconstruir uma cronologia fictícia.
- Registrar limites das conclusões: sem bypass demonstrado, sem segurança geral comprovada, sem isolamento WAN absoluto, sem inferência automática de LFI/RFI.
- Continuidade do laboratório após logout/reinicialização segue NÃO VERIFICADA nesta sessão; não integra as conclusões das investigações.
- Relatório e vídeo finais continuam pendentes; nenhum trabalho do Bloco 04 foi iniciado.

## Resumos e matriz

- [INV-01](INV-01/resumo.md): hipótese H1, sessões parciais preservadas e limitações de identificação.
- [INV-02](INV-02/resumo.md): comparação A×B de autenticação e variável efetivamente alterada.
- [INV-03](INV-03/resumo.md): listagem pública e limite do controle negativo.
- [Matriz de evidências](MATRIZ_EVIDENCIAS.md): IDs correlacionados com os JSONL privados.

## Validação e reprodução

`python3 -m unittest discover -s tests -v`: 61 testes descobertos, 58 aprovados e três integrações reais opt-in ignoradas. Os testes usam fixtures/mocks identificados; as três investigações reais descritas acima são evidências distintas. `python3 -m py_compile` nos quatro módulos e `sh -n` nos scripts shell passaram; `git diff --check` sem erros.

Auditoria dos cinco JSONL (original interrompido, tentativa parcial e três principais) sem lacunas nos vínculos checados. Nas principais: INV-01 3 propostas/3 resultados; INV-02 2/2; INV-03 3/3. Cada uma tem restauração com IDs diferentes, interpretações vinculadas, conclusão delegada e limite de chamadas preservado. A tentativa parcial e a principal da INV-01 somam seis propostas novas; a original interrompida tem uma proposta histórica anterior à solicitação atual. Hashes dos três arquivos originais preservados; manifesto privado dos novos artefatos e validação em `logs/`.

A leitura final confirmou identidade do container, Qwen local, IP/rota conhecidos, `ip_forward=0` e Apache/mysql/openvpn ativos. Isso não valida todas as funções de WordPress/Nextcloud/VPN nem constitui auditoria de firewall. O procedimento não modificou esses serviços. [Operação delegada e critérios](../OPERACAO_DELEGADA_BLOCO03.md) documentam comandos, escopo e canal de revisão; o modo supervisionado original segue disponível.
