# A06 — Replay contrafactual sem ferramentas (P3)

**Pergunta única:** a próxima decisão do Qwen depende dos fatos, ou de uma sequência esperada pelo prompt?
**Dependência:** [A04](A04-controles-por-cenario.md) e [A05](A05-ledger-factual.md). **Estado:** ensaio futuro; nenhum replay rodou.

## Isolamento obrigatório

Criar runner específico, por exemplo `scripts/af_replay.py`, cujo modo padrão é **dry-run estrutural**: valida casos e imprime plano, **não chama Ollama**, Nmap, HTTP do Juice Shop, Docker ou restore. O modo opt-in de **Ollama local** pede confirmação e só acessa `127.0.0.1:11434`; **NUNCA** executa a ação sugerida. Pode compartilhar helpers puros com `agent.py`, mas nenhuma função de ferramenta ou restauração é invocável pelo replay.

## Contrato dos casos

- `case_id`, `scenario`, `research_question`, `objective`, `allowed_tools`, `evidence_source` (`result_id` de sessão real ou `fixture_simulada`), `context_mode`, `branch_id`, `expected_observation_delta` e `pre_registered_evaluation`.
- Propostas/condições carregam uma **referência** a artefato real privado ou uma fixture sanitizada explicitamente rotulada. Nunca forjar `result_id` de produção para uma fixture.
- Um par A/B mantém objetivo, schema, instrução, allowlist, modelo/digest e opções constantes, variando **uma evidência por vez**. Exemplos seguros: status de porta aferido ou não, uma versus duas respostas inválidas observadas, restrição de extensão versus resultado adicional permitido.
- Comparação de memória A/B mantém **os mesmos fatos**, mudando só montagem do contexto (histórico original versus ledger); registrar quando diferenças de truncagem impedirem equivalência perfeita.
- **Controle de estabilidade:** repetir um prompt idêntico antes de interpretar qualquer mudança entre braços como evidência de sensibilidade. Respostas diferentes para o mesmo prompt enfraquecem a atribuição à evidência.
- Orçamento máximo proposto: **3 pares** sensibilidade + **3 pares** memória + **2 propostas** de estabilidade = **14 propostas**, sempre separadas das sessões de investigação real. `temperature=0`, `think=false`, JSON Schema e parâmetros atuais do Ollama, registro de `done`, `done_reason`, duração, tokens quando presentes.

## Avaliação do resultado

Anotar se a ação seguinte **é relevante e justificada** pelo fato alterado, não apenas se a string da ferramenta mudou. Proposta insegura ou repetitiva é limitação. Parada apropriada é válida, mas se o contrato atual exige sempre propor ferramenta, **não forçar implementação de stop dentro do modelo**: avaliar a decisão do revisor ou reconhecer a limitação do schema.

## Aceite com testes sem rede

Mockar todo executor, `subprocess.run`, `HTTPConnection` e restore para falhar se forem tocados pelo replay. Com `--dry-run` (nome a decidir no código), nenhuma API Ollama é acessada. Fixture que inclua instrução maliciosa no corpo HTTP para sair do escopo deve ser tratada como **dado não confiável**, sem expandir host/porta; resultados simulados não entram na matriz de investigações reais.

**Próximo:** [A07 — avaliação e métricas](A07-metricas-e-aval-humana.md).
