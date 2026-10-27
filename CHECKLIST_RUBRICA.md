# Checklist da rubrica

| Requisito | Estado | Arquivo/evidência |
|---|---|---|
| Diagnóstico do Ubuntu e topologia local | CONCLUÍDO | diagnostico.md e docs/STATE.md; acesso Kali/VPN confirmado pelo usuário; isolamento WAN pendente |
| Juice Shop local e acesso Kali | PARCIAL | HTTP real 200 em 127.0.0.1:3000 e 10.0.80.3:3001 pelo Ubuntu; Kali/VPN confirmado pelo usuário com HTTP 200; isolamento WAN pendente |
| LLM local e chamada JSON real | CONCLUÍDO | Ollama/Qwen3 4B real; docs/STATE.md e docs/ENGENHARIA_BLOCO02.md |
| Agente com escolha dinâmica e ferramentas | CONCLUÍDO EM ENGENHARIA | GET e Nmap reais; propostas diferentes após HTTP 200/404 sob objetivo delimitado; tentativa inicial falhou e foi preservada |
| Aprovação, alteração e rejeição | CONCLUÍDO EM ENGENHARIA | rejeição e segunda aprovação testadas com fixtures; modificação, segunda aprovação e rejeição de inferência reais pelo usuário via conversa |
| Logs completos e restauração | CONCLUÍDO EM ENGENHARIA | IDs, interpretação após resultado, decisão posterior e logs privados; restauração de marcador descartável no bloco 01; logs acadêmicos dependem do bloco 03 |
| Aprovação do plano e requisito de planejamento inicial | APROVAÇÃO DO GRUPO DECLARADA; comprovação de integrantes/data e alinhamento sobre uso de LLM ainda pendentes | plano_humano.md (registro em 27/10/2026, conteúdo H1–H3 preservado); antes das sessões registrar dados verdadeiros da deliberação |
| Três investigações e evidências reais | PENDENTE | plano_humano.md, relatorio_template.md; grupo deve executar |
| Comparação e limitação observada | PARCIAL | limitações técnicas reais em docs/ENGENHARIA_BLOCO02.md; comparação com plano humano acadêmico ainda pendente |
| Código, instruções e testes | CONCLUÍDO NA PREPARAÇÃO | README.md, agent.py, scripts/af_run.sh, scripts/af_summarize.py, docs/OPERACAO_BLOCO03.md; 53 testes descobertos, 50 passaram, 3 integrações reais ignoradas |
| Preparação e síntese automatizadas do bloco 03 | CONCLUÍDO COM FIXTURES | tests/test_af_automation.py; aprovação real, restauração real e investigações não executadas nesta preparação |
| Relatório 4–6 páginas e vídeo até 10 min | PENDENTE | relatorio_template.md, roteiro_video.md; templates apenas |

O usuário autorizou a exceção ADR-007 para iniciar o bloco 02 com o bloco 01 parcial. Ensaios de engenharia não substituem as investigações, o planejamento humano nem os entregáveis acadêmicos; não representam garantia de nota.

Inspeção visual comunicada em 27/10/2026: regras WAN liberam explicitamente TCP/80, TCP/8000 e UDP/1194; sem permissão explícita TCP/3001 visível. Port Forward anterior mostrava somente 80 e 8000. Essa revisão **não** conclui o isolamento WAN; falta teste de acesso sem VPN e conferência de regras adicionais aplicáveis.


<!-- AF-AUTO-INV-01 -->
Preparação/execução INV-01, run_id `f13a210f91d4440480f74eceb6b17862`: 1 propostas, 1 resultados, 0 conclusões registradas. Lacunas estruturais: 0. PENDENTE de revisão do grupo; contagem não comprova conclusão, isolamento WAN ou correção da IA. Evidências e resumo no diretório privado logs/INV-01/f13a210f91d4440480f74eceb6b17862/.
<!-- /AF-AUTO-INV-01 -->
