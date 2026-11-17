# Handoff — Bloco 03B v2 (excelência acadêmica)

**Estado:** prompt de programação futuro. Não equivale a autorização de testes reais, restauração, instalação, alteração de rede ou publicação. A v2 ainda depende de aprovação pelo grupo.

## Entrada canônica: notas atômicas (17/11/2026)

**Ler primeiro [`docs/03b/INDEX.md`](03b/INDEX.md)**. Esse índice distribui toda a programação **P0–P5** entre A01–A09 e mantém A10/P6 somente como portões humanos futuros. O Codex deve executar **todo o desenvolvimento** e a verificação com fixtures, sem aguardar Nicholas para escolhas técnicas triviais. Leia apenas a nota da fase corrente, seus arquivos de código e testes; não precisa carregar todos os textos de uma vez. As notas são contratos executáveis de aceite, enquanto este handoff é um atalho. Nenhuma branch nova deve ser criada por padrão.

> **Prompt curto preferencial:** Leia `AGENTS.md`, `docs/STATE.md` e `docs/03b/INDEX.md`. Implemente completamente P0–P5 das notas atômicas A01–A09, incluindo código, testes simulados e documentação, corrigindo erros de regressão. Não execute P6, rede/LLM reais, restauração ou ações de ferramenta. Preserve logs/modos antigos e decisões humanas. Mostre o resultado dos testes e solicite autorização específica antes de publicar código.

## Ler em sequência

1. `AGENTS.md`, `docs/INDEX.md`, `docs/STATE.md`, `PLANS.md`.
2. `docs/AF - Tecnologias Hackers 26-2.pdf` e `plano_humano.md` (fonte normativa e plano humano original; não editar).
3. `docs/PLANO_REFINAMENTO_BLOCO03B.md` (histórico v1), `docs/PLANO_03B_EXCELENCIA_V2.md` (nova proposta) e `tasks/03b-v2-excelencia-implementacao.md` (P0–P6).
4. `docs/investigacoes/ANALISE_BLOCO03.md`, matriz de evidências, três resumos; código em `agent.py`, `scripts/` e `tests/`.

## Prompt de implementação — copiar somente após aprovação do escopo de programação

> Atue como desenvolvedor do único agente acadêmico do KIT11 e implemente **somente P0–P5 de `tasks/03b-v2-excelencia-implementacao.md`**, seguindo `docs/PLANO_03B_EXCELENCIA_V2.md`. Não inicie P6. Não altere `plano_humano.md`, as três investigações originais, a branch de logs nem o modo supervisionado existente. Verifique se o Ubuntu contém código local ainda não publicado antes de editar. Implemente incrementos pequenos, Python stdlib, testes com fixtures e nenhuma dependência nova: 03B opt-in, guards A/B/C e `.md` condicionado à listagem atual, ledger factual de IDs, replay contrafactual **isolado de qualquer executor de ferramenta**, export de métricas objetivas e folha humana de avaliação. Preserve a seleção do Qwen com base em evidências — sem roteiro fixo —, aprovações humanas por ferramenta e todas as proteções atuais. Nunca transforme decisão Codex delegada em intervenção humana. Não execute Ollama real, Juice Shop, Nmap, Docker, Kali, restauração nem teste WAN nesta rodada; nenhum commit/push sem autorização específica de Nicholas. Execute apenas unittest, py_compile, análise estática e testes de mocks; entregue diagnóstico, diffs, PASS/FAIL/SKIP e recomendações antes de solicitar autorização de experimentos. Regras locais e acadêmicas são superiores a este prompt.

## Como demonstrar avanço de verdade

- **Código:** três cenários reais preservados; gates e regressões testados; replay impossibilitado de chamar ferramentas; IDs e hashes íntegros.
- **Evidência:** as condições comparativas são pré-registradas e rotuladas; estatísticas contêm N; LLM não arbitra suas próprias conclusões.
- **Qualidade:** um exemplo causal claro por investigação vale mais que múltiplos requests sem pergunta científica; quando houver erro ou resultado idêntico, explicar isso.
- **Entrega:** relatório 4–6 páginas e vídeo <=10 minutos dependem de execuções e revisão reais, jamais de fixtures.

**Confirmações futuras, separadas:** (1) publicação de documentação/branch; (2) autorização de programação P0–P5; (3) aprovação do plano v2; (4) permissão de replay ao Ollama; (5) permissão de restaurar e investigar Juice Shop no laboratório; (6) aceite acadêmico final.
