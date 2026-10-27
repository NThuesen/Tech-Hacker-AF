# Diagnóstico do KIT11 — 27/10/2026

- **PASSOU — ambiente e recursos:** Ubuntu 24.04.1 x86_64, host `kit11-OptiPlex-Micro-7020`; `systemd-detect-virt`: `none`; Intel i5-14500T, 20 CPUs lógicas, 15 GiB RAM (11 GiB disponíveis), 39 GiB livres em `/`, Python 3.12.3. Recursos parecem suficientes, sem garantia de desempenho do modelo.
- **PASSOU — inventário de rede e conflitos:** `ip -br addr` mostra `enp0s31f6` em `10.0.80.3/24`; `ip route` mostra rota padrão via `10.0.80.1`. `ss -lnt`: 80 e 8000 em uso, 3000 e 11434 sem listener. Endereço privado atual não comprova ausência de roteamento WAN ou regras do pfSense; não se alterou firewall/NAT. Confirme isolamento e rota antes de publicar.
- **BLOQUEADO — Docker/Juice Shop:** `command -v docker` não retornou caminho; conexão local à 3000 falhou. Não há evidência de execução HTTP real. Instalação administrativa requer aprovação explícita.
- **BLOQUEADO — Ollama/modelo:** `command -v ollama` não retornou caminho e `curl` em 127.0.0.1:11434 falhou. Modelo e chamada Python real não verificados; instalação administrativa requer aprovação explícita.
- **BLOQUEADO — Nmap:** `command -v nmap` não retornou caminho; instalação administrativa requer aprovação explícita.
- **PENDENTE — Kali:** nenhum acesso ao cliente; não se confirmou rota VPN nem HTTP. Execute `scripts/diagnostico_kali.sh IP_ATUAL` no próprio Kali após iniciar o laboratório. Não modificar notebook/VM remotamente.
- **Recomendação:** com autorização administrativa, instalar Docker, Nmap e Ollama conforme documentação oficial, obter modelo e validar os serviços localmente; confirmar que a rede autorizada é privada e não há publicação WAN antes de executar `scripts/start.sh`. Preservar os serviços existentes.
