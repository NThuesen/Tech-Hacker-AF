# Índice da documentação e infraestrutura Codex

**Separação:** `AGENTS.md` na raiz = instruções automáticas do **Codex desenvolvedor**. `docs/` = conhecimento e evidência. `tasks/` = blocos de execução. `agents/` = perspectivas opcionais de revisão, **não** subagentes executando automaticamente. `agent.py` = agente acadêmico local integrado ao Ollama.

## Navegação mínima
| Documento | Ler quando |
|---|---|
| `AGENTS.md` | sempre (regras de projeto para Codex) |
| `PLANS.md` | escolher próximo bloco e portões de aceite |
| `PROMPTS.md` | iniciar uma sessão curta sem repetir um mega-prompt |
| `docs/STATE.md` | primeira leitura de cada sessão; estado real vs. pendente |
| `docs/ENGENHARIA_BLOCO02.md` | comandos, IDs e limitações dos ensaios técnicos do agente |
| `docs/investigacoes/ANALISE_BLOCO03.md` | resultados reais INV-01/02/03, limitações e matriz de evidências |
| `docs/OPERACAO_DELEGADA_BLOCO03.md` | modo delegado autorizado por Nicholas, critérios e distinção de decisões |
| `docs/OPERACAO_BLOCO03.md` | comandos INV-01/02/03, portões humanos, síntese privada e rastreabilidade |
| `docs/CONTEXT.md` | consulta de infraestrutura histórica |
| `docs/ARCHITECTURE.md` | mudança de código/topologia |
| `docs/RUBRIC.md` | validação de critérios da AF |
| `docs/DECISIONS.md` | mudanças arquiteturais |
| `docs/requisitos.md` | resumo extraído pelo Codex dos PDFs |
| `tasks/00-auditoria.md` | sincronização e diagnóstico |
| `tasks/01-laboratorio.md` | Docker/Juice Shop/Ollama/Nmap |
| `tasks/02-agente.md` | implementação/validação do agente Python |
| `tasks/03-investigacoes.md` | ensaios reais e decisões humanas |
| `tasks/04-entrega.md` | relatório/vídeo/checklist |
| `agents/code-reviewer.md` | auditoria opcional do código |
| `agents/evidence-auditor.md` | auditoria opcional de rastreabilidade |

## Fontes originais
- `docs/AF - Tecnologias Hackers 26-2.pdf` (avaliação final; fonte normativa).
- `docs/Relatorio_Final_Roteiro1_Firewall_KIT11.pdf` (histórico do kit).

Não duplicar integralmente PDFs no prompt nem transformar resultados simulados em evidências reais.
