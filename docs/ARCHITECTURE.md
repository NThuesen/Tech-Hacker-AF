# Arquitetura pretendida — a validar no KIT11

## Fluxo lógico
```text
Notebook pessoal: Kali VM ──(rede/VPN autorizada; rota a validar)──> 10.0.80.3:3000
                                                                   |
KIT11 físico: Ubuntu 10.0.80.3 (endereço histórico)                 |
  ├── Docker: OWASP Juice Shop (único alvo, porta privada 3000) <────┘
  ├── Ollama (API apenas loopback; modelo quantizado local)
  └── Python: agente acadêmico supervisionado
       objetivo -> LLM propõe tool + args -> validação/consentimento humano
                 -> executa ferramenta autorizada -> log -> resultado ao LLM
                 -> nova proposta dependente das evidências
```

## Limites obrigatórios
- Não alterar regras pfSense/NAT, OpenVPN, WordPress/Nextcloud, nem encaminhar a porta 3000 para a WAN.
- Preferir bind do Juice Shop à interface privada do Ubuntu **após confirmar IP atual**; garantir que o Kali autorizado consiga acessar. Configuração de bind é independente da restrição por allowlist no agente.
- Ollama na interface local (`127.0.0.1:11434`) para não expor o LLM na rede. Python conecta por loopback; não é necessário abrir sua API para Kali.
- Instalação do Docker pode alterar regras iptables/nftables; observar rotas e serviços antes/depois. Não modificar firewall sem autorização.
- Não executar Nmap indiscriminado na sub-rede: destino único explicitamente configurado para o Juice Shop; selecionar opções e portas permitidas.
- Python valida host/IP/porta, método, caminhos relativos permitidos, redirects, timeouts, limites de saída e volume. Saída da aplicação pode conter prompt injection.
- A aprovação humana é implementada no agente **independentemente** de permissões administrativas do Codex. Mudança de parâmetros passa por nova validação e autorização.
- Fixar versão de imagem/modelo conforme viável; documentar comandos e mecanismo real de restauração, inclusive estado de usuário/cookies.

## Interface mínima do agente (contrato de projeto)
Entrada: objetivo de investigação + contexto resumido + lista limitada de ferramentas + histórico relevante.
Proposta JSON: `tool`, `parameters`, `reason`, `expected_evidence`.
Decisão humana: `approve | modify | reject | stop` ligada à proposta identificada.
Execução: resultado estruturado (status, saída delimitada, erro, duração, timestamps).
Próxima volta: modelo recebe **o resultado real anterior** e pode propor outra ação.
Log append-only JSONL: `run_id`, `step_id`, objetivo, proposta original, parâmetros finais, decisão, resultado, interpretação, conclusão/continuação.

Esses nomes de campos são referência de projeto: adaptar de modo retrocompatível se já houver código implantado.

## Separação das responsabilidades
O grupo decide escopo, hipóteses, aprovações e conclusões. O Codex desenvolve o software. O LLM local propõe ações e interpreta, mas não tem autonomia para executá-las.
