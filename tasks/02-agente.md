# Bloco 02 — Agente acadêmico supervisionado

## Objetivo
Validar e corrigir minimamente `agent.py` para cumprir o ciclo de decisão real exigido na AF. O Codex é o desenvolvedor; o Qwen/Ollama é o agente acadêmico.

## Código existente (verificar antes de mudar)
Há `agent.py` com `nmap`, `http_get`, `http_post`, `review()`, `model_call()`, escrita JSONL e 10 testes simulados em `tests/test_agent.py`. Reusar; **não gerar novo framework**.

## Tarefas prioritárias
1. Verificar se o LLM local realmente retorna JSON conforme o contrato atual: `hipotese`, `interpretacao`, `ferramenta`, `parametros`. Se Qwen gerar JSON ruim, tentar instrução/format/schema e fallback de erros com parcimônia.
2. Conduzir ensaios técnicos autorizados: LLM escolhe uma ferramenta, usuário aprova/rejeita/modifica, ferramenta roda ou não, resultado volta ao histórico do LLM; repetir com **resultados diferentes** e comparar próximas ações.
3. Corrigir lacuna importante: após cada resultado, capturar uma interpretação do **resultado recém-coletado** (não somente a interpretação na proposta seguinte). Associá-la ao `step_id` e registrar ação do grupo após essa interpretação; não forçar comandos adicionais em caso de parada.
4. Conferir logs completos: objetivo, horário, ferramentas/argumentos propostos, decisão, parâmetros finais, resultado, interpretação, decisão final humana, erros.
5. Aumentar cobertura de rejeição, modificação, contenção do alvo, logs, resposta malformada, falhas de rede e duas sequências de evidências diferentes. Usar mocks de forma explícita apenas para testes unitários.
6. Confirmar utilidade do POST para autenticação: hoje só aceita corpo como texto JSON, sem cabeçalhos customizados/cookies. Se insuficiente para a investigação escolhida, adicionar **suporte mínimo validado e restrito** a headers/cookies de laboratório, com teste e justificativa; não dar acesso genérico HTTP arbitrário.
7. Não usar manipulação insegura de shell, proxies ou redirects; reduzir exposição de dados sensíveis em logs; limitar chamadas e contexto.
8. Executar teste integrado com Ollama + Juice Shop *após* aprovação do grupo; não antecipar plano humano nem executar ataques definitivos.

## Critérios de aceite
- >=2 ferramentas integradas, >=1 acessa Juice Shop diretamente.
- Ação alterada pelo grupo só executa após segunda aprovação; rejeitada nunca executa.
- Evidência B ≠ evidência A podem provocar propostas diferentes de forma verificável, sem roteiro fixo; se modelo falhar, documentar a limitação em vez de fabricar comportamento.
- Cada execução real tem interpretação vinculada ao resultado e decisão humana auditável.
- Todos os testes unitários passam; teste real registrado separadamente.
- Mudanças mínimas, sem nova UI, multiagente ou framework pesado.

## Saída
Relato em `docs/STATE.md` e `CHECKLIST_RUBRICA.md`, mais próximo bloco. Parar antes do bloco 03.
