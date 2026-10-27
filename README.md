# KIT11-AF

Agente local supervisionado para o Juice Shop. Leia `diagnostico.md`, `docs/requisitos.md` e `PENDENCIAS.md`. O plano em `plano_humano.md` deve ser preenchido e aprovado pelo grupo antes da primeira consulta ao LLM. Não há experimentos definitivos neste repositório.

## Preparação

Python 3.10+ usa apenas biblioteca padrão (`requirements.txt`). O ambiente observado e suas limitações estão em `docs/STATE.md`. No KIT11, o Docker Rootless está instalado em `/home/kit11/.local/opt/kit11-docker`; use seu contexto `rootless` e mantenha a API Ollama em 127.0.0.1:11434. O usuário autorizou inicialmente apenas Juice Shop em loopback: não publique em outro IP sem autorização e sem verificar o isolamento WAN. Não altere pfSense, VPN, NAT ou firewall.

Na raiz, após confirmar que o daemon Rootless e a API Ollama estão ativos:

```sh
export PATH="/home/kit11/.local/opt/kit11-docker:$PATH"
export DOCKER_HOST="unix:///run/user/$(id -u)/docker.sock"
./scripts/start.sh 127.0.0.1
curl --noproxy '*' --max-time 5 -i http://127.0.0.1:3000/
python3 agent.py --ip 127.0.0.1 --log logs/investigacao1.jsonl
```

O script de início recusa substituir um container existente. Se o `kit11-juice` já existe, confira-o com `docker ps -a` antes de decidir como retomá-lo. Os serviços do usuário estão habilitados, mas `Linger=no`; o container usa `--restart no`, portanto não há garantia de retomada após logout ou reinicialização.

O IP deve estar vinculado ao próprio Ubuntu; o agente usa apenas esse IPv4 e TCP/3000. O container fixa `bkimminich/juice-shop:v17.3.0`, não compartilha volumes e é publicado apenas no IP informado. O teste a partir do Kali permanece pendente: loopback não é diretamente acessível pela rede; um túnel SSH exige conexão previamente autorizada e ainda não verificada. Para verificação técnica isolada sem investigação, teste a API local manualmente, por exemplo `curl --noproxy '*' http://127.0.0.1:11434/api/generate -d '{"model":"qwen3:4b-instruct","prompt":"Responda JSON com ok true","format":"json","stream":false}'`.

Se houver uma conexão SSH já autorizada até o KIT11 com encaminhamento permitido, no Kali pode-se usar `ssh -N -L 127.0.0.1:3000:127.0.0.1:3000 USUARIO@HOST_AUTORIZADO` e acessar `http://127.0.0.1:3000/` no próprio Kali. Substitua os campos pela conexão conhecida; ela não foi identificada nem testada nesta sessão. Não habilite SSH ou altere regras para criá-la sem autorização.

## Operação e limites

Cada ciclo gera uma proposta JSON e solicita aprovação, modificação (com segunda aprovação), rejeição ou encerramento, com justificativa. Após executar, o modelo interpreta explicitamente o resultado; o operador decide continuar ou encerrar. Histórico, resultados e interpretações alimentam a próxima escolha. Não há seleção de ferramenta por roteiro no código.

O CLI aceita somente `--ip 127.0.0.1`. Nmap usa conexão TCP na porta 3000; HTTP aceita caminhos relativos sem proxies nem redirecionamentos. Limites: 20 propostas, até 40 chamadas de modelo, HTTP com prazo total de 8 s, Nmap com timeout de processo de 10 s, POST objeto JSON UTF-8 até 4 KiB e resposta HTTP até 16 KiB. Corpos extensos são reduzidos no contexto do modelo com truncamento explícito. JSON inválido, saída incompleta e falhas de log interrompem a operação. Detalhes em `docs/ENGENHARIA_BLOCO02.md`.

Logs exigem arquivos 0600 em diretório privado 0700, sem links; o CLI exige extensão `.jsonl`, ignorada pelo Git. Se `logs/` já existir com permissões compartilhadas, revise a propriedade e restrinja seu acesso antes de executar. Senhas/tokens em campos reconhecidos são redigidos, mas texto livre pode conter dados sensíveis: use somente dados de laboratório e revise antes de compartilhar. IDs ligam proposta, execução, resultado, interpretação e decisões; o modelo pode interpretar incorretamente mesmo retornando JSON válido.

Para ensaio técnico interativo, use `python3 agent.py --engenharia --ip 127.0.0.1 --log logs/engenharia-interativa.jsonl`. Essa opção identifica engenharia e não afirma aprovação do plano acadêmico; mantém a revisão antes de toda ação. O modo acadêmico continua exigindo a confirmação do plano pelo grupo.

## Restauração

`./scripts/restore.sh 127.0.0.1` exige digitar `RESTAURAR`, remove o container chamado `kit11-juice` e o recria sem volumes; apaga dados e alterações nesse container. Confirme sua identidade antes de executar. Não restaura serviços externos. O teste com marcador descartável está registrado em `docs/STATE.md`.

## Testes

`python3 -m unittest discover -s tests -v` executa os testes locais com fixtures e mocks explicitamente identificados; as integrações reais são ignoradas por padrão. Com serviços ativos e autorização para as leituras técnicas, `KIT11_REAL_TESTS=1 python3 -m unittest discover -s tests -p test_engineering_real.py -v` consulta Ollama/Qwen, HTTP público local e Nmap reais. O gate automatizado desses testes não é decisão humana e não executa propostas condicionais A/B. Resultados e limitações observados estão em `docs/ENGENHARIA_BLOCO02.md`.
