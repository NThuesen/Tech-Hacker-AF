# A09 — Documentação operacional e handoff completo (P5)

**Pergunta única:** como o próximo Codex e o grupo reproduzem o software sem confundir código pronto com experimento feito?
**Dependência:** [A08](A08-testes-e-qualidade.md). **Estado:** tarefa futura do Codex, não pronta.

## Entregáveis de documentação do Codex

- Criar `docs/OPERACAO_BLOCO03B_V2.md` **somente depois de implementar as flags**; incluir comandos reais do replay `dry-run`, como ativar opt-in do Ollama local com aprovação, e fluxo live com todos os portões humanos. Não inventar flags.
- Atualizar README, `docs/INDEX.md`, `docs/STATE.md`, `CHECKLIST_RUBRICA.md` e handoff com estados factuais: `IMPLEMENTADO COM FIXTURES` versus `NÃO EXECUTADO`. Separar logs privados de artefatos publicáveis, preservando branch histórica de evidência.
- Documentar: modelo/digest, Python/OS, versão da imagem, porta/host fixos, limites e erros da CLI, critério de parada, preservação de dados e como desfazer a opção 03B.
- Registro de decisões técnicas: arquivo novo versus extensão existente, formato do ledger, separação do replay e alternativas consideradas. Não é necessário redigir diariamente mega-relatórios; notas atômicas devem ficar atualizadas e links funcionando.
- Exports sintéticos com marca d'água textual **FIXTURE/NÃO REAL** e logs de produção fora do Git. Campos humanos de avaliação ficam vazios até preenchimento verdadeiro.
- Preparar matriz de evidências que aceita run/result IDs futuros e roteiro de relatório de 4–6 páginas / vídeo até 10 minutos. **Não preencher resultados futuros**.

## Handoff final do Codex (padrão)

1. **Implementado:** lista P0–P5, arquivos, interfaces/flags reais.
2. **Testado:** comandos realizados, PASS/FAIL/SKIP, fixtures relevantes, link para diff.
3. **Segurança:** provas de que não houve rede real/teste ofensivo/restauração; regressões e proteções.
4. **Pendente:** P6, aprovação de plano, revisão WAN, restauração autorizada, sessões humanas, métricas reais, relatório/vídeo.
5. **Próximo passo para Nicholas:** comandos previstos após autorização, em uma investigação por vez.

## Critério de aceite

Outro integrante consegue localizar cada nota pelo índice, reproduzir testes simulados, distinguir modo legado/03B/replay e entender exatamente o que precisa de Nicholas para P6. Documentos não se contradizem nem afirmam trabalho não executado.

**Próximo:** [A10 — execução real permanece bloqueada](A10-execucao-real-pendente.md).
