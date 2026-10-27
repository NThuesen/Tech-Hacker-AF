# Contexto técnico e limites do conhecimento

## Relatório do KIT11 (setembro/2026; histórico)
- Ubuntu 24.04.1 LTS, interface `enp0s31f6`, IP relatado `10.0.80.3/24`.
- pfSense LAN `10.0.80.1/24`, rede `10.0.80.0/24`; WAN relatada `192.168.20.31`.
- WordPress HTTP `10.0.80.3:80`; Nextcloud HTTP `10.0.80.3:8000`.
- NAT WAN para serviços existentes; OpenVPN UDP/1194, túnel `10.8.0.0/24`.
- Dados anteriores **não provam** estado atual ou autorização para expor novo serviço.

## Contexto atualizado da AF (informação do grupo + repositório)
- Hospedeiro: KIT11 físico, Ubuntu `kit11-OptiPlex-Micro-7020`; o Kali é VM no notebook do estudante, externa ao host de desenvolvimento.
- Diagnóstico do Codex, salvo em `diagnostico.md` em 27/10/2026: Intel i5-14500T, 15 GiB RAM, ~11 GiB disponíveis e 39 GiB livres; porta 3000 livre, Docker/Nmap/Ollama ausentes naquele instante. Revalidar no Ubuntu.
- O repositório privado `NThuesen/Tech-Hacker-AF` recebeu um push do Codex (`codex inicial`); a `main` já contém `agent.py`, dez testes simulados, scripts, README e templates. **Não criar uma segunda aplicação do zero.**
- Arquivos de governança e tarefas ficam em uma branch própria até integração do PR.

## Dúvidas a resolver com evidências atuais
- O Docker, Nmap e Ollama foram instalados depois do diagnóstico?
- Modelo local Qwen e API JSON funcionam? Qual desempenho?
- Juice Shop acessível no Ubuntu e na VM Kali? A publicação permanece privada?
- O ciclo supervisionado retorna resultados reais ao LLM e grava a interpretação pós-execução?
- O grupo aprovou seu planejamento **antes** de qualquer uso do LLM para revisar testes?

## Escopo rígido
Somente a instância local do Juice Shop do KIT11. pfSense, WordPress, Nextcloud, VPN, outros kits, redes externas e Internet não são alvos.
