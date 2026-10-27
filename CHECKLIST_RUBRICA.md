# Checklist da rubrica

| Requisito | Estado | Arquivo/evidência |
|---|---|---|
| Diagnóstico do Ubuntu e topologia local | CONCLUÍDO | diagnostico.md; rota Kali e isolamento WAN pendentes |
| Juice Shop local e acesso Kali | PARCIAL | Docker Rootless e HTTP real em loopback verificados; Kali/WAN pendentes no bloco 01 |
| LLM local e chamada JSON real | CONCLUÍDO | Ollama/Qwen3 4B real; docs/STATE.md e docs/ENGENHARIA_BLOCO02.md |
| Agente com escolha dinâmica e ferramentas | CONCLUÍDO EM ENGENHARIA | GET e Nmap reais; propostas diferentes após HTTP 200/404 sob objetivo delimitado; tentativa inicial falhou e foi preservada |
| Aprovação, alteração e rejeição | CONCLUÍDO EM ENGENHARIA | rejeição e segunda aprovação testadas com fixtures; modificação, segunda aprovação e rejeição de inferência reais pelo usuário via conversa |
| Logs completos e restauração | CONCLUÍDO EM ENGENHARIA | IDs, interpretação após resultado, decisão posterior e logs privados; restauração de marcador descartável no bloco 01; logs acadêmicos dependem do bloco 03 |
| Plano humano anterior ao LLM | PENDENTE | plano_humano.md; exige grupo |
| Três investigações e evidências reais | PENDENTE | plano_humano.md, relatorio_template.md; grupo deve executar |
| Comparação e limitação observada | PARCIAL | limitações técnicas reais em docs/ENGENHARIA_BLOCO02.md; comparação com plano humano acadêmico ainda pendente |
| Código, instruções e testes | CONCLUÍDO | README.md, agent.py, tests/test_agent.py |
| Relatório 4–6 páginas e vídeo até 10 min | PENDENTE | relatorio_template.md, roteiro_video.md; templates apenas |

O usuário autorizou a exceção ADR-007 para iniciar o bloco 02 com o bloco 01 parcial. Ensaios de engenharia não substituem as investigações, o planejamento humano nem os entregáveis acadêmicos; não representam garantia de nota.
