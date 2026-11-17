# A01 — Limites, autoria e decisões humanas

**Pergunta única:** o que o Codex pode implementar e o que permanece sob autoridade do grupo?
**Estado:** contrato documental, não prova de implementação.
**Fonte:** AF original, `AGENTS.md`, `plano_humano.md`, `docs/DECISIONS.md` (incluindo ADR-011), `docs/PLANO_03B_EXCELENCIA_V2.md`.

## Contrato

- Codex desenvolve **todo P0–P5**: código, fixtures, testes, métricas, documentação e revisão técnica. Nenhuma programação manual de Nicholas é requisito. Codex pode tomar decisões de implementação de baixo risco e registrá-las.
- O programa acadêmico continua sendo **um agente supervisionado**, com Qwen3 4B via Ollama local e apenas `nmap`, `http_get`, `http_post`. O Qwen escolhe ferramenta e parâmetros a partir de resultados; guardas Python aplicam escopo, não roteiro. Nenhum segundo agente LLM.
- **Toda ação ofensiva real** requer decisão verdadeira do grupo por ferramenta (aprovar, modificar com reconfirmação, rejeitar ou encerrar), justificativa e avaliação posterior; automatização/callback Codex não é decisão humana. O Codex pode criar mocks de aprovação **somente nos testes rotulados como mocks**.
- `plano_humano.md`, execuções INV-01/02/03 e logs da branch de evidências são históricos **imutáveis**. O plano 03B v2 nasceu após uso do LLM e precisa aprovação nova do grupo antes de P6; não reconstruir autoria ou cronologia.
- Alvo real do agente apenas `127.0.0.1:3000` no KIT11; Kali/OpenVPN só valida `10.0.80.3:3001` por processo distinto e autorizado. Ollama só `127.0.0.1:11434`. Nunca consultar outro IP, porta, domínio ou equipamento.
- Sem mutações em pfSense/WAN/NAT/firewall/OpenVPN/WordPress/Nextcloud/SSH; sem varreduras fora TCP/3000, bypass, SQLi, brute force, credenciais reais, traversal, LFI/RFI, downloads privados, crawler/fuzzer ou shell livre do LLM.
- Logs privados, sem segredos no Git. Restaurar **somente container verificado**, com confirmação separada e inspeção posterior. WAN ainda tem limite de comprovação e deve ser reavaliada antes de P6.

## Aceite verificável

1. Teste de fixture: proposta fora do host/porta/rota/método permitido é bloqueada **antes de qualquer efeito**.
2. Teste: não há caminho de código acadêmico real que execute ferramenta sem decisão originada de terminal humano com justificativa; modificação exige segunda confirmação.
3. Logs diferenciam `entrada_terminal_humana`, `codex_delegado`, `fixture_de_teste` e `replay_sem_execucao`, sem renomear autoria.
4. P0–P5 não iniciam Docker, Ollama real, rede ou testes reais; P6 exige autorização posterior.

**Próxima leitura:** [A02](A02-inventario-do-codigo.md); para gate específico [A03](A03-sessao-e-gates.md).
