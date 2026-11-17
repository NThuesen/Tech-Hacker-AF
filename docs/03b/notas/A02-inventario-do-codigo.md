# A02 — Interfaces reais a preservar

**Pergunta única:** onde o Codex deve integrar o 03B sem reescrever o agente?
**Estado:** inventário conferido no histórico do repositório de 17/11/2026; **rever checkout KIT11 antes de editar**.
**Fontes:** `agent.py`, `scripts/af_session.py`, `scripts/af_delegated.py`, `scripts/af_summarize.py`, `scripts/lab_common.sh`, `scripts/restore.sh`, `tests/`.

## Ponto de integração

| Arquivo/símbolo | Contrato existente | O que a v2 pode acrescentar |
|---|---|---|
| `agent.py:validate_proposal()` | JSON estrito com `hipotese`, `interpretacao`, `ferramenta`, `parametros`; apenas nmap/GET/POST | preservar shape e host; não inventar ferramenta nova |
| `agent.py:execute()` | HTTPConnection apenas loopback, Nmap fixo TCP/3000, timeout, limites, sem redirecionamentos | nenhuma mudança de alvo ou execução para replay |
| `agent.py:recent_history()` | últimas oito entradas compactadas; truncagem sinalizada | ledger factual como **opt-in** no contexto da proposta seguinte |
| `agent.py:interpret_result()` | interpretação de um `result_id`, em chamada separada | preservar contrato; não atribuir memória que ela não viu |
| `agent.py:run_session()` | logs JSONL de proposta, decisão, resultado, interpretação; `reviewer` delegado separado | metadados 03B, guardas por cenário, sem quebrar modo antigo |
| `scripts/af_session.py:prepare()` | aprovação do plano, Kali/WAN, identidade, restauração e hashes; TTY real | reaproveitar validadores e integrar hash adicional do adendo |
| `scripts/af_session.py:authentication_guard()` | A/B/C controlados, uma variante por sessão | reaproveitar e registrar `variant` explicitamente |
| `scripts/af_summarize.py` | síntese privada determinística por IDs | exportar nova fase sem sobrescrever sessões antigas |
| `scripts/af_delegated.py` | decisões automatizadas rotuladas como delegadas | preservar, **não** usar como aprovação humana no 03B |
| `tests/` | suíte de mocks/fixtures, 3 integrações reais opt-in históricas | regressão + testes específicos do 03B, sem network default |

## Decisões técnicas delegadas ao Codex

- Pode criar `scripts/af_refine.py`, `scripts/af_replay.py`, helper de ledger e módulo de métricas, ou integrar minimamente em módulos existentes. Escolher a opção **menos invasiva** e registrar trade-offs.
- Python stdlib; sem dependências, frameworks, APIs remotas, vector DB ou mais modelos. Manter `temperature=0`/`think=false`/JSON Schema do Ollama, sem afirmar garantia semântica.
- Separar três modos: **legado**, **03B live supervisionado**, **replay local sem executor**. Não passar callback de revisão delegada para afirmar supervisão real.
- Evitar nomes de funções/flags na documentação operacional até que existam no código. Implementar e testar primeiro, documentar depois.

## Aceite verificável

Um teste de regressão demonstra que uma sessão legada recebe as mesmas rotas, validações e decisões que antes; novos fluxos 03B exigem opt-in. A suíte de tests antiga continua rodando com PASS/FAIL/SKIP honestos. `git diff` não contém alteração inesperada no plano humano, logs históricos ou scripts de rede.

**Próximo:** [A03 — modo 03B e gates](A03-sessao-e-gates.md).
