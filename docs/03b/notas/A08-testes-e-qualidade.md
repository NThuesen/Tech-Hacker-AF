# A08 — Verificação end-to-end de implementação (P5/QA)

**Pergunta única:** como comprovar que o Codex implementou tudo sem executar testes ofensivos reais?
**Dependência:** [A03](A03-sessao-e-gates.md) até [A07](A07-metricas-e-aval-humana.md). **Estado:** lista de aceite ainda não executada.

## Matriz mínima de testes (todos com mocks/fixtures)

| Categoria | Casos indispensáveis | Esperado |
|---|---|---|
| Contratos antigos | `validate_proposal`, `run_session`, Nmap/GET/POST antigos, modo delegado | comportamento original preservado |
| Gates P0 | plano/hash alterado, sem grupo, sem WAN, sem TTY, identidade/container mudou, restore recusada | abortar antes de ferramenta e logar razão |
| Humano P0 | aprovar, rejeitar, modificar/reconfirmar, encerrar, Ctrl+C, log falha | origem correta, nenhuma aprovação implícita |
| Autenticação P1 | A/B/C em qualquer ordem, variante repetida, quarta variante, email/rota diferentes | só três controles válidos no máximo uma vez |
| Recursos P1 | listagem atual completa/ausente, truncada, nome presente; `.txt`, `.md`, positivo público condicional | permitir `.md` somente após pré-requisito; fora da lista bloqueado |
| Factual P2 | truncagem HTML, `ppp` sem `-sV`, comparação antecipada, resultado ausente, bytes altos | ledger não cria observações; cabe no contexto |
| Replay P3 | modo dry-run, teste de conexão Ollama, fixture simulada, 14 propostas, entrada hostil em HTTP | nunca invoca executor; sem LLM real no teste default |
| Métricas P4 | denominador zero, sessão interrompida, métricas por origem, dados sensíveis, CSV humano vazio | `N/A` honesto e sem elevar fixture a fato |
| Operação P5 | README/STATE/checklist, novas flags documentadas, erros de CLI | status correto, comandos executáveis quando autorizados |

## Comandos de verificação (somente após código implementado)

```sh
python3 -m unittest discover -s tests -v
python3 -m py_compile agent.py scripts/*.py
sh -n scripts/af_run.sh scripts/start.sh scripts/restore.sh
git diff --check
```

O Codex deve primeiro inspecionar scripts novos e adequar a lista real de verificação. Não executar `test_engineering_real.py` com opt-in, não chamar Ollama, rede, Docker, nmap ou restauração ao validar P0–P5. A contagem histórica **58 PASS / 3 SKIP** é baseline e não deve ser declarada como execução atual.

## Definition of Done da programação

1. P0–P5 implementados; testes de segurança/regressão e sintaxe aprovados **na execução atual**, com contagens reais e falhas reportadas.
2. Novo modo é opcional e não alterou os controles nem os registros antigos; logs 03B não são criados com status `EXECUTADO` sem sessão real.
3. Replay é incapaz de disparar ferramenta ofensiva por caminho de código acessível; agente real mantém aprovações humanas.
4. Documentação de uso corresponde a flags existentes; comandos de execução real estão marcados **P6 NÃO AUTORIZADO**.
5. Resumo técnico de riscos/limites e mudanças entregue; nenhuma publicação de código feita sem nova autorização.

**Próximo:** [A09 — operação](A09-operacao-e-entregas.md).
