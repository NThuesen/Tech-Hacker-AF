# Índice da documentação

A documentação é dividida para economizar contexto. **Codex lê automaticamente `AGENTS.md` na raiz.** Os demais arquivos devem ser abertos conforme o bloco em execução.

| Arquivo | Responsabilidade |
|---|---|
| `AGENTS.md` | regras permanentes e limites de segurança |
| `PLANS.md` | ordem dos blocos e critérios de avanço |
| `PROMPTS.md` | comandos curtos para iniciar/continuar o Codex |
| `docs/CONTEXT.md` | fatos confirmados e contexto histórico |
| `docs/ARCHITECTURE.md` | arquitetura-alvo e fronteiras |
| `docs/RUBRIC.md` | matriz de rastreabilidade à AF |
| `docs/DECISIONS.md` | escolhas arquiteturais e suas razões |
| `docs/STATE.md` | realizado vs. pendente com evidência |
| `tasks/00-auditoria.md` | inventário + integração do código existente |
| `tasks/01-laboratorio.md` | componentes reais e rede |
| `tasks/02-agente.md` | ciclo de decisão supervisionado |
| `tasks/03-investigacoes.md` | protocolo das três investigações |
| `tasks/04-entrega.md` | relatório, apresentação e reprodução |
| `agents/` | papéis de revisão técnica opcionais (não runtime) |

**Duas IAs distintas:** Codex é o **assistente de desenvolvimento**; Qwen/Ollama é o **agente acadêmico local**, cujo comportamento e supervisão serão avaliados.

**Fontes originais no repositório:** `docs/AF - Tecnologias Hackers 26-2.pdf` e `docs/Relatorio_Final_Roteiro1_Firewall_KIT11.pdf`.

**Regra de manutenção:** uma informação pertence a um único arquivo-fonte; outros documentos devem linká-lo, não copiá-lo.
