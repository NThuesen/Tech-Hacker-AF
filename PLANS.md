# Plano de execução — blocos controlados

Este arquivo é a **ordem das entregas**, não um relatório de testes realizados. A execução de cada bloco exige validação do bloco anterior e registro em `docs/STATE.md`.

| Bloco | Trabalho | Dependência | Evidência de conclusão |
|---|---|---|---|
| 00 | Sincronizar trabalho local, inventariar código e validar ambiente KIT11 | acesso ao Ubuntu/repo | árvore conferida, inventário real e testes existentes executados |
| 01 | Instalar/validar laboratório Juice Shop e Ollama | 00 | HTTP local + rede autorizada + chamada de LLM local, sem afetar serviços |
| 02 | Implementar/verificar agente supervisionado | 01 | escolha condicionada às evidências, autorização humana, logs e testes unitários |
| 03 | Três investigações reais e evidências | 02 + plano humano aprovado | três estudos de caso completos, decisões humanas e análise de limitações |
| 04 | Documentação, reprodução e entrega | 03 | README, relatório 4–6 pp., vídeo <=10 min, checklist da rubrica |

## Portões de decisão
- Após 00: a RAM, rede e softwares suportam o projeto? Se não, registrar impedimento e alternativa antes de instalar.
- Após 01: testes mostram Juice Shop e Ollama **reais**? Mocks não substituem.
- Após 02: o LLM propõe próximo passo diferente quando recebe evidência diferente? O grupo pode rejeitar sem execução?
- Antes de 03: o grupo escreveu e aprovou o planejamento **sem LLM**.
- Após 03: as evidências sustentam conclusões, inclusive quando hipótese é refutada?
- Antes de 04: logs e materiais compartilháveis não contêm segredos.

## Política de mudança
Não assumir que um bloco foi concluído porque um arquivo existe. Reexecutar validações relevantes após alterações. Mudanças de arquitetura devem ser justificadas em `docs/DECISIONS.md`; não expandir escopo apenas por estética.
