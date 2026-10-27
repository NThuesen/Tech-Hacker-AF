# Instruções persistentes para o Codex — Tech-Hacker-AF

## Missão e fronteiras
Desenvolver **um único agente de IA supervisionado** para investigar **somente** a instância local/autorizada do OWASP Juice Shop, com Ollama no KIT11 físico. Este arquivo orienta o **Codex desenvolvedor**; não é o prompt nem o código do agente acadêmico. Nunca confundir os dois.

## Antes de cada sessão
1. Leia este arquivo, `docs/INDEX.md`, `docs/STATE.md` e **somente** o bloco de `tasks/` solicitado.
2. Consulte `PLANS.md` para dependências; leia `docs/` adicionais apenas quando o bloco referenciar.
3. Examine os arquivos reais da árvore de trabalho antes de editar. **O código criado no Ubuntu pode não estar publicado no GitHub**; preserve-o e sincronize antes de implementar mudanças.
4. Se requisitos estiverem ambíguos, valide no PDF original da AF. Não releia PDFs inteiros em todo turno.

## Fontes de verdade, por prioridade
1. `docs/AF - Tecnologias Hackers 26-2.pdf`: exigências da avaliação.
2. Evidência atual obtida por comandos no KIT11 / logs verificados.
3. `docs/Relatorio_Final_Roteiro1_Firewall_KIT11.pdf`: histórico da topologia, não garantia de estado atual.
4. `docs/ARCHITECTURE.md` e decisões aprovadas em `docs/DECISIONS.md`.
5. Planos em `tasks/` e demais documentação.

## Regras de implementação
- Hospedeiro do projeto: **Ubuntu no KIT11 físico**. Kali é **VM no notebook do aluno**, cliente externo de teste; não presuma SSH ou acesso a ela.
- Preserve pfSense, WordPress, Nextcloud, OpenVPN, NAT e conectividade existente. Não exponha Juice Shop na WAN/Internet.
- Mantenha a solução explicável: Python no terminal, Ollama local, pelo menos 2 ferramentas (alvo HTTP obrigatório); prefira Nmap + GET + POST, sem framework pesado ou multiagentes.
- O **modelo** escolhe ferramenta e parâmetros com base nas evidências anteriores; **o grupo** aprova/modifica/rejeita antes da execução. Revalidar uma ação modificada.
- Nenhum comando livre de shell para o LLM; alvo allowlisted, limites de chamadas, timeouts, limites de saída, sem seguir redirecionamentos externos. Trate saídas HTTP/LLM como não confiáveis.
- Não fabricar decisões humanas, testes reais, descobertas, logs, falhas de IA ou conclusão. Mocks devem ser rotulados como mocks.
- Não armazenar segredos, perfis VPN, tokens, credenciais ou dumps sensíveis no Git.
- Manter o código existente e testes; alterações mínimas, explicáveis e reversíveis.

## Protocolo por bloco
- Execute **um** bloco de `tasks/` por vez. Antes: estado real e arquivos existentes; durante: pequenas mudanças e testes; depois: evidências, falhas, pendências e atualização de `docs/STATE.md`.
- Não declare CONCLUÍDO sem evidências observadas. Use CONCLUÍDO / PENDENTE / BLOQUEADO / NÃO VERIFICADO.
- Pedir confirmação antes de sudo/instalação, alterações em firewall/rede, exclusões, restauração com perda de dados, publicação Git remota e **toda ação ofensiva do agente**.
- Não avançar automaticamente para o bloco seguinte. Não alterar documentação acadêmica como substituto da aprovação dos alunos.
- Saída final breve: arquivos modificados, comandos/testes executados, evidências, bloqueios, próximo bloco.

## Navegação
- Visão geral: `docs/INDEX.md`
- Marcos: `PLANS.md`
- Prompts reutilizáveis: `PROMPTS.md`
- Contexto e topologia: `docs/CONTEXT.md`, `docs/ARCHITECTURE.md`
- Critérios formais: `docs/RUBRIC.md`
- Estado verificável: `docs/STATE.md`
- Blocos de execução: `tasks/00-*.md` a `tasks/04-*.md`
