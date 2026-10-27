# Bloco 01 — Laboratório real e reprodutível

## Objetivo
Fazer a infraestrutura local funcionar no Ubuntu físico KIT11 sem quebrar WordPress, Nextcloud, pfSense ou VPN.

## Pré-condições
Bloco 00 verificado, inventário de hardware documentado e autorização específica para instalação administrativa.

## Passos
1. Verificar conflitos de portas/interfaces, espaço em disco, serviço Docker, permissões, impacto nas regras de rede. Planejar fallback/rollback.
2. Instalar apenas dependências ausentes autorizadas: Docker, Nmap, Ollama, modelo local especificado/alternativa justificada. Não mudar pfSense/roteamento.
3. Conferir `scripts/start.sh` e imagem fixada já existente: `bkimminich/juice-shop:v17.3.0`; verificar se o tag existe; não trocar versão sem registro.
4. Iniciar Juice Shop no IP **privado atual** e porta validada. Obter HTTP real (status, data, URL e resposta resumida).
5. Confirmar serviço Ollama em `127.0.0.1:11434` e fazer chamada Python real ao modelo Qwen local; capturar JSON bruto, parse e latência, sem tratar exemplo como resultado acadêmico.
6. Testar RESTAURAÇÃO em dados descartáveis e registrar antes/depois. Confirmar ausência de impacto em portas 80/8000.
7. Orientar usuário a testar acesso da VM Kali; sem acesso efetivo ao notebook, marcar como PENDENTE (não fingir).
8. Registrar versões, comandos reproduzíveis, evidências e medidas de isolamento em `docs/STATE.md` e `diagnostico.md`.

## Critérios de aceite
- `docker ps` mostra container correto; HTTP local resposta real.
- Ollama retorna uma resposta estruturada válida através de Python e existe modelo local.
- Nmap funciona e testes existentes continuam passando.
- Serviço existente permanece acessível.
- Restauração concluída com confirmação explícita (ou marcada PENDENTE com razão).
- Kali acessa a aplicação **quando testado no Kali**, sem exposição WAN.

## Não fazer
Não instalar no Kali sem solicitação; não publicar Juice Shop em `0.0.0.0` por conveniência, nem abrir NAT WAN, nem coletar tráfego de outros kits. Pare diante de impacto inesperado.
