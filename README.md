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

Cada ciclo gera proposta JSON, mostra-a e solicita aprovação, modificação (seguida de nova aprovação), rejeição ou encerramento. Resultados e decisões anteriores são enviados ao LLM para a próxima escolha; não há roteiro fixo. Nmap usa conexão TCP em uma única porta, HTTP usa apenas caminhos relativos, sem proxies nem redirecionamentos; limite de 20 propostas, timeout 8 s por ferramenta, POST até 4 KiB e resposta até 16 KiB. Dados dos testes, inclusive corpos e cabeçalhos, são registrados: use apenas contas e dados de laboratório e proteja os arquivos de log. JSONL inclui horário UTC e conclusão humana. Limites não substituem supervisão, e o modelo pode interpretar incorretamente evidências.

## Restauração

`./scripts/restore.sh 127.0.0.1` exige digitar `RESTAURAR`, remove o container chamado `kit11-juice` e o recria sem volumes; apaga dados e alterações nesse container. Confirme sua identidade antes de executar. Não restaura serviços externos. O teste com marcador descartável está registrado em `docs/STATE.md`.

## Testes

`python3 -m unittest discover -s tests -v`. São testes locais automatizados, com servidor simulado e modelo simulado; não provam operação real do Docker, Ollama ou Kali. Consulte `relatorio_template.md`, `roteiro_video.md` e `CHECKLIST_RUBRICA.md`.
