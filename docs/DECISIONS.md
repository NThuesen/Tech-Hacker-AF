# Registro de decisões arquiteturais (ADR leve)

Registre aqui apenas decisões que alterem escopo, segurança, reprodutibilidade ou custo técnico. Não confundir hipótese de projeto com observação.

| ID | Decisão | Estado | Motivo |
|---|---|---|---|
| ADR-001 | Manter Ubuntu físico KIT11 como host de Ollama, agente e Juice Shop; Kali VM externa como cliente de verificação | proposta | minimiza dependência do notebook e atende kit local, condicionado a recursos/rede |
| ADR-002 | Um agente Python supervisionado, sem LangChain/multiagentes | proposta | rubrica cobra ciclo verificável, não autonomia |
| ADR-003 | Expor Juice Shop somente à rede privada autorizada; API Ollama em loopback | proposta | limita superfície e preserva serviços |
| ADR-004 | Fluxo em blocos e trilha de evidências JSONL | proposta | facilita auditoria, avanço incremental e controle de tokens |
| ADR-005 | Não reimplementar código local que ainda não foi enviado ao GitHub | vigente para desenvolvimento | evita perda de trabalho/código duplicado |
| ADR-006 | Docker Rootless e Juice Shop inicialmente em loopback; acesso Kali por SSH apenas se já autorizado | vigente em 2026-10-27 por instrução do usuário | preserva a rede do host; acesso remoto e isolamento da WAN continuam sujeitos a validação |
| ADR-007 | Iniciar exclusivamente o bloco 02 apesar do bloco 01 parcial | exceção controlada autorizada pelo usuário em 2026-10-27 | laboratório local operacional; pendências Kali/WAN permanecem abertas; não autoriza bloco 03 ou mudança de rede |
| ADR-008 | Manter contrato de proposta existente e acrescentar interpretação separada, IDs e logs privados | implementada no bloco 02, 2026-10-27 | cada resultado exige interpretação explícita; saída incorreta ou falha de log interrompe o fluxo; ensaios técnicos são identificados e não substituem o plano acadêmico |
| ADR-009 | Preservar dois bindings Rootless da porta interna 3000: 127.0.0.1:3000 para agente e 10.0.80.3:3001 para Kali/OpenVPN | autorizada pelo usuário e verificada no Ubuntu em 2026-10-27; substitui a limitação inicial da ADR-006 | acesso Kali/VPN confirmado pelo usuário com HTTP 200; isolamento WAN permanece PENDENTE; nenhuma alteração em firewall, NAT, pfSense ou OpenVPN |
| ADR-010 | Restauração exige identidade e bindings conhecidos, reinspeção após confirmação e remoção por ID | implementada em 2026-10-27 | evita apagar container identificado apenas pelo nome; recusa imagem/configuração divergente, mounts ou troca de ID; o daemon deve ser Rootless local |

Ao aceitar uma decisão, registrar data, evidência e responsável. Se o diagnóstico exigir mudança, adicionar ADR-006+ com alternativas avaliadas; não apagar histórico.

## ADR-011 — operação delegada explícita no Bloco 03 (2026-10-27)

Nicholas solicitou adaptação por dificuldade física no teclado e relatou autorização do professor. O Qwen permanece o único agente acadêmico que escolhe ferramentas/parâmetros. O Codex desenvolvedor revisa propostas por um canal de arquivos privados; não foi criado segundo agente no programa nem framework de multiagentes. Revisor delegado e autorização humana são eventos distintos; decisões automáticas não serão atribuídas ao grupo. O modo terminal original permanece disponível.

Critérios e exceção de operação em `docs/OPERACAO_DELEGADA_BLOCO03.md`. Alterações pequenas no ciclo permitem callbacks de revisão e guarda de resultados. Runner independente reaproveita validação/restauração Rootless e aprovação real anterior por hash. Mantém limite de seis propostas, sem sequência fixa; ações modificadas requerem revalidação e segunda decisão delegada. Bloqueios de escopo e erro de identidade interrompem o fluxo. Os resultados técnicos podem ser analisados; aceite acadêmico da delegação e conclusão do grupo continuam pendentes. Não tratar autorização de acessibilidade como prova de decisão humana em cada ação.

## ADR-012 — canal delegado distinto para 03B (2026-11-19)

Nicholas autorizou expressamente decisões do Codex e relatou liberação do professor, ainda sem validação independente. O canal `03B_delegado` registra a origem de cada decisão, requer justificativa individual e confirmação adicional para alteração, mantém guardas e hashes e não converte essas decisões em humanas. O modo humano original continua separado. Restaurações exigiram autorizações específicas. O professor e Nicholas ainda devem revisar a adequação à rubrica; a delegação não comprova intervenção humana em cada ação.
