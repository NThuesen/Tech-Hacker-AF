# KIT11-AF

Agente local supervisionado para o Juice Shop. Leia `diagnostico.md`, `docs/requisitos.md` e `PENDENCIAS.md`. O plano em `plano_humano.md` deve ser preenchido e aprovado pelo grupo antes da primeira consulta ao LLM. Não há experimentos definitivos neste repositório.

## Preparação

Python 3.10+ usa apenas biblioteca padrão (`requirements.txt`). O ambiente observado e suas limitações estão em `docs/STATE.md`. No KIT11, o Docker Rootless está instalado em `/home/kit11/.local/opt/kit11-docker`. A configuração autorizada publica a porta interna 3000 do Juice Shop em **127.0.0.1:3000 para Ubuntu/agente** e **10.0.80.3:3001 para Kali/OpenVPN**. Ollama permanece apenas em 127.0.0.1:11434. A verificação de isolamento WAN está pendente; não altere pfSense, VPN, NAT ou firewall.

Na raiz, após confirmar que o daemon Rootless e a API Ollama estão ativos:

```sh
export PATH="/home/kit11/.local/opt/kit11-docker:$PATH"
export DOCKER_HOST="unix:///run/user/$(id -u)/docker.sock"
./scripts/start.sh
curl --noproxy '*' --max-time 5 -i http://127.0.0.1:3000/
curl --noproxy '*' --max-time 5 -i http://10.0.80.3:3001/
python3 agent.py --ip 127.0.0.1 --log logs/investigacao1.jsonl
```

Os scripts usam explicitamente o socket Rootless local `/run/user/UID/docker.sock`, verificam o modo Rootless e o digest da imagem local, sem iniciar daemons ou baixar imagens automaticamente. A configuração compartilhada fica em `scripts/lab_common.sh`; os dois bindings são fixos. O argumento legado opcional `127.0.0.1` continua aceito, mas não muda os bindings; outros argumentos de IP são recusados.

O script de início verifica a identidade de um container existente e recusa substituí-lo. Os serviços do usuário estão habilitados, mas `Linger=no`; o container usa `--restart no`, portanto não há garantia de retomada após logout ou reinicialização. A imagem é `bkimminich/juice-shop:v17.3.0`, com digest validado `sha256:123acb31ed8bb05ebb06934a29be83d4e11a46cae937b9ed2bf2bda29d98130a`, sem volumes. Ambos os IPs devem estar vinculados ao Ubuntu.

O acesso do Kali pela VPN a `http://10.0.80.3:3001/` foi confirmado pelo usuário com HTTP 200. As verificações executadas pelo Codex nesta sessão partiram do Ubuntu e também retornaram 200 nos dois endpoints; não representam uma nova execução no Kali. Não é necessário habilitar SSH. Para repetir a checagem no próprio Kali conectado à VPN: `curl --noproxy '*' --max-time 5 -i http://10.0.80.3:3001/` ou `./scripts/diagnostico_kali.sh 10.0.80.3`.

Para verificação técnica isolada do modelo, sem investigação: `curl --noproxy '*' http://127.0.0.1:11434/api/generate -d '{"model":"qwen3:4b-instruct","prompt":"Responda JSON com ok true","format":"json","stream":false}'`.

## Operação e limites

Cada ciclo gera uma proposta JSON e solicita aprovação, modificação (com segunda aprovação), rejeição ou encerramento, com justificativa. Após executar, o modelo interpreta explicitamente o resultado; o operador decide continuar ou encerrar. Histórico, resultados e interpretações alimentam a próxima escolha. Não há seleção de ferramenta por roteiro no código.

O CLI aceita somente `--ip 127.0.0.1`. Nmap usa conexão TCP na porta 3000; HTTP aceita caminhos relativos sem proxies nem redirecionamentos. Limites: 20 propostas, até 40 chamadas de modelo, HTTP com prazo total de 8 s, Nmap com timeout de processo de 10 s, POST objeto JSON UTF-8 até 4 KiB e resposta HTTP até 16 KiB. Corpos extensos são reduzidos no contexto do modelo com truncamento explícito. JSON inválido, saída incompleta e falhas de log interrompem a operação. Detalhes em `docs/ENGENHARIA_BLOCO02.md`.

Logs exigem arquivos 0600 em diretório privado 0700, sem links; o CLI exige extensão `.jsonl`, ignorada pelo Git. Se `logs/` já existir com permissões compartilhadas, revise a propriedade e restrinja seu acesso antes de executar. Senhas/tokens em campos reconhecidos são redigidos, mas texto livre pode conter dados sensíveis: use somente dados de laboratório e revise antes de compartilhar. IDs ligam proposta, execução, resultado, interpretação e decisões; o modelo pode interpretar incorretamente mesmo retornando JSON válido.

Para ensaio técnico interativo, use `python3 agent.py --engenharia --ip 127.0.0.1 --log logs/engenharia-interativa.jsonl`. Essa opção identifica engenharia e não afirma aprovação do plano acadêmico; mantém a revisão antes de toda ação. O modo acadêmico continua exigindo a confirmação do plano pelo grupo.

## Restauração

`./scripts/restore.sh` exige digitar `RESTAURAR` e apaga os dados do container reconhecido. Antes de qualquer remoção, verifica nome, ID, digest, referência e rótulos da imagem, ausência de mounts/privilégios extras e os dois bindings esperados. Após a confirmação, reinspeciona e recusa se o ID mudou; remove pelo ID verificado e recria com ambos os endpoints. Divergências ou container ausente encerram a operação sem remoção. Não restaura serviços externos. A restauração real anterior com marcador descartável e os testes atuais com Docker simulado estão separados em `docs/STATE.md`.

## Testes

`python3 -m unittest discover -s tests -v` executa os testes locais com fixtures e mocks explicitamente identificados; as integrações reais são ignoradas por padrão. Com serviços ativos e autorização para as leituras técnicas, `KIT11_REAL_TESTS=1 python3 -m unittest discover -s tests -p test_engineering_real.py -v` consulta Ollama/Qwen, HTTP público local e Nmap reais. O gate automatizado desses testes não é decisão humana e não executa propostas condicionais A/B. Resultados e limitações observados estão em `docs/ENGENHARIA_BLOCO02.md`.
