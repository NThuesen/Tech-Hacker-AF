# Contexto técnico e limites do conhecimento

## Evidências do relatório KIT11 (setembro/2026; podem ter mudado)
- Equipamento servidor Ubuntu, descrito como Ubuntu 24.04.1 LTS; interface `enp0s31f6`, IP documentado `10.0.80.3/24`.
- pfSense LAN `10.0.80.1/24`, rede `10.0.80.0/24`; WAN histórica `192.168.20.31`.
- WordPress HTTP `10.0.80.3:80`; Nextcloud HTTP `10.0.80.3:8000`.
- NAT histórico WAN 80/8000 para serviços existentes; OpenVPN UDP/1194, túnel `10.8.0.0/24`.
- Os IPs/portas do relatório são **referência histórica**, nunca autorização para mudar NAT/roteamento.

## Informação fornecida pelo grupo na conversa
- O Codex está sendo executado no Ubuntu **físico** do KIT11, não no Kali.
- Kali Linux é uma VM no notebook do estudante; acesso pela rede ainda exige teste na máquina Kali.
- Um diagnóstico do Codex foi relatado: Ubuntu `10.0.80.3/24`, porta 3000 livre, Docker/Ollama/Nmap ausentes naquele momento; dez testes com mocks passaram. **Essas afirmações não são verificações desta branch; checar estado atual.**
- O Codex informou criação local de `agent.py`, `README.md`, `diagnostico.md`, `CHECKLIST_RUBRICA.md` e outros arquivos; eles **não constavam da main remota** na auditoria inicial. Antes de criar novos arquivos de aplicação, conferir a árvore local.

## Em aberto (não inferir)
- CPU/RAM/disco disponível no Ubuntu no momento do trabalho.
- Docker e Ollama instalados com sucesso e funcionando.
- Acesso ao Juice Shop pelo Kali via rede do laboratório/VPN.
- Disponibilidade, precisão e latência do modelo Qwen local.
- Aprovação humana do plano inicial e testes acadêmicos efetivos.

## Escopo
Somente a instância do Juice Shop do KIT11. pfSense, WordPress, Nextcloud, VPN, outros kits, redes externas e Internet **não** são alvos de teste.
