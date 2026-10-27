# Prompts curtos para o Codex

Execute na raiz deste repositório (`~/Kit11-AF`, se for o caminho no Ubuntu). **Não envie novamente o prompt monolítico da AF.** O `AGENTS.md` fornece as regras persistentes.

## 1. Sincronização e orientação (primeira sessão)
> Leia AGENTS.md, docs/INDEX.md, docs/STATE.md e tasks/00-auditoria.md. Verifique git status, arquivos locais e divergência com origin/main. Preserve trabalho não publicado. Execute apenas o bloco 00, valide o que puder e atualize docs/STATE.md. Não instale nem altere serviços sem minha autorização.

## 2. Executar um bloco (trocar NN)
> Siga AGENTS.md. Leia docs/STATE.md e somente tasks/NN-ARQUIVO.md e referências estritamente necessárias. Faça um preflight de leitura, implemente apenas este bloco, rode seus critérios de aceite e registre evidências/pendências em docs/STATE.md. Pare no final do bloco.

## 3. Revisão crítica
> Audite o bloco atual contra docs/RUBRIC.md e AGENTS.md. Dê prioridade a problemas reproduzíveis e riscos reais. Não invente resultados nem reescreva partes saudáveis. Corrija apenas o que for necessário com testes.

## 4. Handoff econômico
> Atualize docs/STATE.md com decisões, evidências, falhas e próximo passo. Responda em até 12 linhas: concluído, testes executados, bloqueios e próxima ação humana. Não repita conteúdos dos PDFs.

## Exemplo após sincronizar o repositório
> Execute o bloco 01 de tasks/01-laboratorio.md, respeitando os portões de autorização. Não avance ao bloco 02.

O processo é **sequencial**; a pasta `agents/` fornece perspectivas de revisão sob demanda, não autoriza múltiplos agentes executando testes em paralelo.
