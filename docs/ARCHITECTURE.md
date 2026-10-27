# Arquitetura local — validada em ensaios de engenharia

## Fluxo lógico
```text
Notebook pessoal: Kali VM ──(SSH já autorizado, se existir; PENDENTE)──> KIT11

KIT11 físico: Ubuntu 10.0.80.3 (rede existente preservada)
  ├── Docker Rootless: OWASP Juice Shop (único alvo, 127.0.0.1:3000)
  ├── Ollama (API apenas loopback; modelo quantizado local)
  └── Python: agente acadêmico supervisionado
       objetivo -> LLM propõe tool + args -> validação/consentimento humano
                 -> executa ferramenta autorizada -> log -> interpretação do resultado pelo LLM
                 -> decisão humana após interpretação -> nova proposta dependente das evidências ou parada
```

## Limites obrigatórios
- Não alterar regras pfSense/NAT, OpenVPN, WordPress/Nextcloud, nem encaminhar a porta 3000 para a WAN.
- Bind do Juice Shop e alvo do CLI fixos em `127.0.0.1:3000` por autorização atual (ADR-006). Acesso Kali continua pendente; não habilitar SSH nem publicar na interface privada por conveniência.
- Ollama na interface local (`127.0.0.1:11434`) para não expor o LLM na rede. Python conecta por loopback; não é necessário abrir sua API para Kali.
- Instalação do Docker pode alterar regras iptables/nftables; observar rotas e serviços antes/depois. Não modificar firewall sem autorização.
- Não executar Nmap indiscriminado na sub-rede: destino único explicitamente configurado para o Juice Shop; selecionar opções e portas permitidas.
- Python valida host/IP/porta, método, caminhos relativos permitidos, redirects, timeouts, limites de saída e volume. Saída da aplicação pode conter prompt injection.
- A aprovação humana é implementada no agente **independentemente** de permissões administrativas do Codex. Mudança de parâmetros passa por nova validação e autorização.
- Fixar versão de imagem/modelo conforme viável; documentar comandos e mecanismo real de restauração, inclusive estado de usuário/cookies.

## Interface implementada
Entrada: objetivo de investigação + contexto resumido + lista limitada de ferramentas + histórico relevante.
Proposta JSON: `hipotese`, `interpretacao` do histórico, `ferramenta`, `parametros`. JSON Schema auxilia a geração e a validação Python decide a aceitação.
Decisão humana: aprovar, modificar com segunda confirmação, rejeitar ou encerrar, com justificativa ligada à proposta identificada.
Execução: resultado estruturado (status, saída delimitada, erro, duração, timestamps).
Próxima volta: modelo recebe **o resultado real anterior** e pode propor outra ação.
Interpretação separada: `resultado_id`, `interpretacao`, `limitacoes`; ID deve corresponder ao resultado recém-obtido. O grupo decide continuar/encerrar após recebê-la.
Log JSONL privado: `run_id`, `step_id`, `proposal_id`, `execution_id`, `result_id`, `event_id`, objetivo, proposta original, parâmetros finais, decisão, resultado, interpretação e conclusão/continuação. Falha na gravação aborta; o mecanismo não protege contra adulteração pelo próprio proprietário.

Limites e evidências atuais em `docs/ENGENHARIA_BLOCO02.md`. O contexto do modelo usa trechos de corpos extensos, identificando truncamento; logs retêm o resultado limitado com redação de campos sensíveis. O modelo pode produzir inferências semanticamente erradas mesmo com JSON válido.

## Separação das responsabilidades
O grupo decide escopo, hipóteses, aprovações e conclusões. O Codex desenvolve o software. O LLM local propõe ações e interpreta, mas não tem autonomia para executá-las.
