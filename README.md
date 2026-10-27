# KIT11-AF

Agente local supervisionado para o Juice Shop. Leia `diagnostico.md`, `docs/requisitos.md` e `PENDENCIAS.md`. O plano em `plano_humano.md` deve ser preenchido e aprovado pelo grupo antes da primeira consulta ao LLM. Não há experimentos definitivos neste repositório.

## Preparação

Python 3.10+ usa apenas biblioteca padrão (`requirements.txt`); requer Docker, Nmap e Ollama instalados no Ubuntu com autorização administrativa. Nenhuma instalação foi feita. Instale por fontes oficiais conforme política do ambiente; verifique permissões de Docker e consumo de recursos. Baixe `ollama pull qwen3:4b-instruct` e confira `ollama list` (o nome/tag depende do registro disponível); mantenha a API em 127.0.0.1:11434. Confirme com `ip -br addr`, `ip route`, `ss -lnt` e regras existentes que o endereço é da interface privada autorizada, a porta 3000 está livre e não há encaminhamento WAN. Uma vinculação a IP privado sozinha não comprova que outros roteamentos não o alcancem; não altere pfSense, VPN ou NAT.

Na raiz, substitua o IP pelo endereço atual confirmado:

```sh
./scripts/start.sh 10.0.80.3
curl --noproxy '*' --max-time 5 -i http://10.0.80.3:3000/
python3 agent.py --ip 10.0.80.3 --log logs/investigacao1.jsonl
```

O IP deve estar vinculado ao próprio Ubuntu; o agente usa apenas esse IPv4 e TCP/3000. O container fixa `bkimminich/juice-shop:v17.3.0`, não compartilha volumes e é publicado apenas no IP informado. O Docker pode modificar regras locais ao iniciar containers: verifique seu impacto previamente. Não expor a Internet. No Kali, execute localmente uma cópia de `scripts/diagnostico_kali.sh` passando o IP atual; o teste de acesso depende da rota/regras existentes e não foi realizado. A validação do modelo ocorre pelo próprio agente após aprovação do plano. Para verificação técnica isolada sem investigação, teste a API local manualmente, por exemplo `curl --noproxy '*' http://127.0.0.1:11434/api/generate -d '{"model":"qwen3:4b-instruct","prompt":"Responda JSON com ok true","format":"json","stream":false}'`.

## Operação e limites

Cada ciclo gera proposta JSON, mostra-a e solicita aprovação, modificação (seguida de nova aprovação), rejeição ou encerramento. Resultados e decisões anteriores são enviados ao LLM para a próxima escolha; não há roteiro fixo. Nmap usa conexão TCP em uma única porta, HTTP usa apenas caminhos relativos, sem proxies nem redirecionamentos; limite de 20 propostas, timeout 8 s por ferramenta, POST até 4 KiB e resposta até 16 KiB. Dados dos testes, inclusive corpos e cabeçalhos, são registrados: use apenas contas e dados de laboratório e proteja os arquivos de log. JSONL inclui horário UTC e conclusão humana. Limites não substituem supervisão, e o modelo pode interpretar incorretamente evidências.

## Restauração

`./scripts/restore.sh 10.0.80.3` exige digitar `RESTAURAR`, remove somente o container chamado `kit11-juice` e o recria sem volumes; apaga dados e alterações nesse container. Não restaura serviços externos. Ainda precisa de teste real após instalação do Docker. Antes e depois, verifique HTTP e registre as evidências, sem repetir ações definitivas sem autorização do grupo.

## Testes

`python3 -m unittest discover -s tests -v`. São testes locais automatizados, com servidor simulado e modelo simulado; não provam operação real do Docker, Ollama ou Kali. Consulte `relatorio_template.md`, `roteiro_video.md` e `CHECKLIST_RUBRICA.md`.
