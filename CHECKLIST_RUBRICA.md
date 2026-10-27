# Checklist da rubrica

| Requisito | Estado | Arquivo/evidência |
|---|---|---|
| Diagnóstico do Ubuntu e topologia local | CONCLUÍDO | diagnostico.md; rota Kali e isolamento WAN pendentes |
| Juice Shop local e acesso Kali | BLOQUEADO | scripts/start.sh; Docker ausente, HTTP real e Kali pendentes |
| LLM local e chamada JSON real | BLOQUEADO | agent.py; Ollama/modelo ausentes |
| Agente com escolha dinâmica e ferramentas | PENDENTE | agent.py; testes simulados passam, ciclo real pendente |
| Aprovação, alteração e rejeição | CONCLUÍDO | agent.py; tests/test_agent.py |
| Logs completos e restauração | PENDENTE | agent.py e scripts/restore.sh; validação real pendente |
| Plano humano anterior ao LLM | PENDENTE | plano_humano.md; exige grupo |
| Três investigações e evidências reais | PENDENTE | plano_humano.md, relatorio_template.md; grupo deve executar |
| Comparação e limitação observada | PENDENTE | relatorio_template.md; depende de uso real |
| Código, instruções e testes | CONCLUÍDO | README.md, agent.py, tests/test_agent.py |
| Relatório 4–6 páginas e vídeo até 10 min | PENDENTE | relatorio_template.md, roteiro_video.md; templates apenas |
