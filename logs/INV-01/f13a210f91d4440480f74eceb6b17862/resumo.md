# INV-01 — resumo técnico privado

**Registro de sessão; exige revisão humana e dos logs primários.**

run_id: f13a210f91d4440480f74eceb6b17862. Origem: sessao.jsonl.

Hipótese e controles: consultar plano-aprovado.md preservado nesta pasta e sua aprovação por hash no JSONL. A hipótese permanece PENDENTE de análise/conclusão do grupo. Candidatos extraídos da seção do cenário no snapshot aprovado. Rotas sem destaque Markdown e mudanças de formato exigem comparação manual.

## Planejamento × propostas efetivas

Correspondência indica apenas ferramenta/rota candidata do plano; não valida corpo, hipótese, adequação nem obriga sequência. Arquivo adicional da INV-03 requer nome oriundo de evidência real.

| proposal_id / evento | Proposta Qwen e parâmetros | Relação com candidatos do plano |
|---|---|---|
| 123a0fb480ce4f4f80d204665e8ee726 / ee5a55c1a9a84c7593fb701ba71428fb | {&quot;hipotese&quot;: &quot;O serviço Juice Shop está exposto em 127.0.0.1:3000, com possibilidade de exposição de endpoints via HTTP.&quot;, &quot;interpretacao&quot;: &quot;Nenhuma evidência histórica disponível para validação. A hipótese se baseia apenas no alvo fixo e na suposição de exposição de serviço conhecido.&quot;, &quot;ferramenta&quot;: &quot;http_get&quot;, &quot;parametros&quot;: {&quot;path&quot;: &quot;/&quot;}} | candidato previsto; revisar conteúdo |

## Evidências, intervenções e interpretações

Resultado técnico é distinto de inferência do Qwen e conclusão humana. Corpos HTTP e saídas Nmap completos e limitados estão no JSONL privado.

| Evento / ID | Conteúdo registrado (origem preservada) |
|---|---|
| aprovacao_plano / ef9b0bd965bc419c85825a2116add234 | {&quot;integrantes&quot;: &quot;Nicholas&quot;, &quot;data_aprovacao&quot;: &quot;15:06&quot;, &quot;justificativa&quot;: &quot;O grupo revisou e aprovou o planejamento das tres investigacoes, considerando as hipoteses, os objetivos, os limites do laboratorio e os criterios de evidencia. A execucao sera supervisionada e restrita ao OWASP Juice Shop do KIT11.&quot;, &quot;plano_sha256&quot;: &quot;2e0de179e41dee61b851344dc1ed819596196b59cabd8d7e5a3a0a621c25f3fb&quot;, &quot;codigo_commit&quot;: &quot;eae8f875166cf2c7d83fce37e35e39fa24986e1c&quot;, &quot;origem&quot;: &quot;entrada_terminal&quot;} |
| portao_rede / 6f35a8655649466d9caa1e667158dce7 | {&quot;kali&quot;: &quot;Kali conectado via OpenVPN (tun0), acesso ao Juice Shop em 10.0.80.3:3001 confirmado com HTTP 200 em 27/10/2026.&quot;, &quot;wan&quot;: &quot;Kali sem VPN em 27/10/2026 15:04:05: acesso a 192.168.20.31:3001 apresentou timeout, HTTP 000 e curl exit 28. Evidencia em ~/af-wan-sem-vpn.txt. Capturas do pfSense WAN e NAT sem permissao explicita TCP/3001. Isolamento confirmado no caminho testado.&quot;, &quot;estado&quot;: &quot;declarado_pelo_grupo&quot;, &quot;origem&quot;: &quot;entrada_terminal&quot;} |
| preflight / 04d7a74df6a846edab2634de9dc21e46 | {&quot;container_id&quot;: &quot;4275d9e2af7f229af38e79fdadc0b35d87f5283d03db96af28a362ce3662b7a6&quot;, &quot;modelo&quot;: &quot;qwen3:4b-instruct&quot;, &quot;digest_modelo&quot;: &quot;0edcdef34593eac1aa2be9c7d06c432dcf81945adca5eca2f27662c18f168ba0&quot;, &quot;nmap&quot;: &quot;Nmap version 7.94SVN ( https://nmap.org )&quot;, &quot;host&quot;: &quot;kit11-OptiPlex-Micro-7020&quot;, &quot;alvo&quot;: &quot;127.0.0.1:3000&quot;, &quot;bindings&quot;: [&quot;127.0.0.1:3000&quot;, &quot;10.0.80.3:3001&quot;], &quot;imagem_validada&quot;: &quot;bkimminich/juice-shop:v17.3.0 sha256:123acb31ed8bb05ebb06934a29be83d4e11a46cae937b9ed2bf2bda29d98130a&quot;} |
| restauracao / 882e49035b574574aab386af683f2e7a | {&quot;container_anterior&quot;: &quot;4275d9e2af7f229af38e79fdadc0b35d87f5283d03db96af28a362ce3662b7a6&quot;, &quot;container_novo&quot;: &quot;882380fb8310a482a8c8cf436ec1b97f89d2f2c8acb4b63fc5480469babd54ac&quot;, &quot;estado&quot;: &quot;recriado&quot;, &quot;origem&quot;: &quot;restore.sh_com_confirmacao_terminal&quot;} |
| pronto / bbd41155c2784c49b1bba918b0aebca9 | {&quot;container_id&quot;: &quot;882380fb8310a482a8c8cf436ec1b97f89d2f2c8acb4b63fc5480469babd54ac&quot;, &quot;status&quot;: 200, &quot;body_sha256&quot;: &quot;486eca89dc36521fb0323bc26024e4e7f5922902d59a702f34c50407531cadd2&quot;, &quot;observacao&quot;: &quot;GET / de disponibilidade; não é descoberta nem prova de isolamento WAN&quot;, &quot;modelo&quot;: &quot;qwen3:4b-instruct&quot;, &quot;digest_modelo&quot;: &quot;0edcdef34593eac1aa2be9c7d06c432dcf81945adca5eca2f27662c18f168ba0&quot;, &quot;nmap&quot;: &quot;Nmap version 7.94SVN ( https://nmap.org )&quot;} |
| decisao_humana / b5290f59d6f14b6da9ffd4cb02b1f2d7 | {&quot;step_id&quot;: 1, &quot;proposal_id&quot;: &quot;123a0fb480ce4f4f80d204665e8ee726&quot;, &quot;decisao&quot;: &quot;aprovada&quot;, &quot;justificativa&quot;: &quot;Aprovada. A requisicao GET / permite verificar a disponibilidade HTTP do Juice Shop sem autenticacao. E uma etapa inicial adequada para H1, mas nao comprova vulnerabilidade.&quot;, &quot;acao_final&quot;: {&quot;hipotese&quot;: &quot;O serviço Juice Shop está exposto em 127.0.0.1:3000, com possibilidade de exposição de endpoints via HTTP.&quot;, &quot;interpretacao&quot;: &quot;Nenhuma evidência histórica disponível para validação. A hipótese se baseia apenas no alvo fixo e na suposição de exposição de serviço conhecido.&quot;, &quot;ferramenta&quot;: &quot;http_get&quot;, &quot;parametros&quot;: {&quot;path&quot;: &quot;/&quot;}}, &quot;origem&quot;: &quot;entrada_terminal&quot;} |
| resultado / 3d11ba46b81142979b1642838b5bb127 | {&quot;step_id&quot;: 1, &quot;proposal_id&quot;: &quot;123a0fb480ce4f4f80d204665e8ee726&quot;, &quot;execution_id&quot;: &quot;6c39c27996de4909b098282544b99d97&quot;, &quot;result_id&quot;: &quot;36e3c3e4cc8443dda703cda8ee39d3c8&quot;, &quot;acao&quot;: {&quot;hipotese&quot;: &quot;O serviço Juice Shop está exposto em 127.0.0.1:3000, com possibilidade de exposição de endpoints via HTTP.&quot;, &quot;interpretacao&quot;: &quot;Nenhuma evidência histórica disponível para validação. A hipótese se baseia apenas no alvo fixo e na suposição de exposição de serviço conhecido.&quot;, &quot;ferramenta&quot;: &quot;http_get&quot;, &quot;parametros&quot;: {&quot;path&quot;: &quot;/&quot;}}, &quot;resultado&quot;: {&quot;status&quot;: 200, &quot;headers&quot;: {&quot;Content-Type&quot;: &quot;text/html; charset=UTF-8&quot;, &quot;Content-Length&quot;: &quot;80117&quot;, &quot;Date&quot;: &quot;Tue, 27 Oct 2026 18:11:00 GMT&quot;}, &quot;truncated&quot;: true, &quot;redirect_followed&quot;: false}, &quot;duracao_s&quot;: 0.004746, &quot;evidencia_primaria&quot;: &quot;corpo/saída no JSONL por result_id; revisar antes de citar&quot;} |
| interpretacao / 4ed8157336d74d529fe4c2eef0044795 | {&quot;step_id&quot;: 1, &quot;proposal_id&quot;: &quot;123a0fb480ce4f4f80d204665e8ee726&quot;, &quot;execution_id&quot;: &quot;6c39c27996de4909b098282544b99d97&quot;, &quot;result_id&quot;: &quot;36e3c3e4cc8443dda703cda8ee39d3c8&quot;, &quot;interpretacao&quot;: {&quot;resultado_id&quot;: &quot;36e3c3e4cc8443dda703cda8ee39d3c8&quot;, &quot;interpretacao&quot;: &quot;O serviço OWASP Juice Shop está ativo em 127.0.0.1:3000, com resposta HTTP 200 e conteúdo HTML completo. A resposta confirma a presença do serviço, com cabeçalhos e corpo de resposta coerentes com a aplicação. Nenhuma evidência de vulnerabilidade ou exposição de endpoints além do índice inicial foi identificada. A hipótese é validada por resposta direta do servidor, sem inferência de versão ou porta aberta.&quot;, &quot;limitacoes&quot;: &quot;O corpo da resposta foi truncado; não foi possível analisar todos os endpoints expostos. A análise se limita ao conteúdo inicial do HTML.&quot;}} |
| interrompida / 836193591e37400f9639a81ac7b49434 | {&quot;step_id&quot;: 1, &quot;proposal_id&quot;: &quot;123a0fb480ce4f4f80d204665e8ee726&quot;, &quot;execution_id&quot;: &quot;6c39c27996de4909b098282544b99d97&quot;, &quot;result_id&quot;: &quot;36e3c3e4cc8443dda703cda8ee39d3c8&quot;, &quot;motivo&quot;: &quot;entrada encerrada; sem decisão/conclusão humana presumida&quot;} |

## Limitações e conclusão

Erros técnicos efetivamente registrados: 0.
Inferências incorretas: classificação depende da avaliação humana registrada após interpretação; não deduzir erro, adaptação útil, vulnerabilidade ou ausência de falhas automaticamente.
Conclusão: consultar conclusao_humana acima; se ausente, PENDENTE. A sequência de propostas/intervenções e os resultados permitem ao grupo comparar decisões sucessivas; causalidade e correção exigem análise humana.

Integridade estrutural: sem lacunas detectadas nos vínculos checados; não atesta autenticidade.

## Matriz de rastreabilidade

| Linha JSONL | event_id | Evento / timestamp | proposal_id | execution_id | result_id |
|---|---|---|---|---|---|
| 1 | 225e6a256b63414eae8d47a997689f9b | preparacao / 2026-10-27T18:06:34.714795+00:00 |  |  |  |
| 2 | ef9b0bd965bc419c85825a2116add234 | aprovacao_plano / 2026-10-27T18:08:53.895495+00:00 |  |  |  |
| 3 | 6f35a8655649466d9caa1e667158dce7 | portao_rede / 2026-10-27T18:09:26.565109+00:00 |  |  |  |
| 4 | 04d7a74df6a846edab2634de9dc21e46 | preflight / 2026-10-27T18:09:26.688381+00:00 |  |  |  |
| 5 | 6f6fedceb2034f60a399bff3c4a6d7a7 | restauracao_solicitada / 2026-10-27T18:09:46.536076+00:00 |  |  |  |
| 6 | 882e49035b574574aab386af683f2e7a | restauracao / 2026-10-27T18:09:57.662993+00:00 |  |  |  |
| 7 | bbd41155c2784c49b1bba918b0aebca9 | pronto / 2026-10-27T18:09:59.741104+00:00 |  |  |  |
| 8 | 02f6ce58318b4cfa940c1889ac8caea4 | inicio / 2026-10-27T18:09:59.840790+00:00 |  |  |  |
| 9 | 2190a55ddc914e66ac5afeb2a0076ca6 | solicitacao_modelo / 2026-10-27T18:09:59.843157+00:00 | 123a0fb480ce4f4f80d204665e8ee726 |  |  |
| 10 | ee5a55c1a9a84c7593fb701ba71428fb | proposta / 2026-10-27T18:10:11.886445+00:00 | 123a0fb480ce4f4f80d204665e8ee726 |  |  |
| 11 | b5290f59d6f14b6da9ffd4cb02b1f2d7 | decisao_humana / 2026-10-27T18:11:00.919756+00:00 | 123a0fb480ce4f4f80d204665e8ee726 |  |  |
| 12 | a2d1017758a54f76bec898851056e45e | execucao / 2026-10-27T18:11:00.924555+00:00 | 123a0fb480ce4f4f80d204665e8ee726 | 6c39c27996de4909b098282544b99d97 | 36e3c3e4cc8443dda703cda8ee39d3c8 |
| 13 | 3d11ba46b81142979b1642838b5bb127 | resultado / 2026-10-27T18:11:00.931613+00:00 | 123a0fb480ce4f4f80d204665e8ee726 | 6c39c27996de4909b098282544b99d97 | 36e3c3e4cc8443dda703cda8ee39d3c8 |
| 14 | e60645e14c4640abaa983385ec6673f2 | solicitacao_modelo / 2026-10-27T18:11:00.933947+00:00 | 123a0fb480ce4f4f80d204665e8ee726 | 6c39c27996de4909b098282544b99d97 | 36e3c3e4cc8443dda703cda8ee39d3c8 |
| 15 | 4ed8157336d74d529fe4c2eef0044795 | interpretacao / 2026-10-27T18:11:29.444541+00:00 | 123a0fb480ce4f4f80d204665e8ee726 | 6c39c27996de4909b098282544b99d97 | 36e3c3e4cc8443dda703cda8ee39d3c8 |
| 16 | 836193591e37400f9639a81ac7b49434 | interrompida / 2026-10-27T18:13:14.244918+00:00 | 123a0fb480ce4f4f80d204665e8ee726 | 6c39c27996de4909b098282544b99d97 | 36e3c3e4cc8443dda703cda8ee39d3c8 |

Para relatório de 4–6 páginas: selecionar fatos sustentados por result_id, separar interpretação e avaliação humana; usar este resumo como material privado. Para vídeo até 10 minutos: selecionar uma investigação completa com plano, proposta, decisão real, resultado, interpretação e conclusão. Capturas, segredos e texto livre exigem revisão antes de compartilhar.
