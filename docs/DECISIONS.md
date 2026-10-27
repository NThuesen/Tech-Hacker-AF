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

Ao aceitar uma decisão, registrar data, evidência e responsável. Se o diagnóstico exigir mudança, adicionar ADR-006+ com alternativas avaliadas; não apagar histórico.
