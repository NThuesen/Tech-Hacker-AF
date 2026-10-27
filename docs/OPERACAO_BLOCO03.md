# Operação supervisionada — Bloco 03

Preparação implementada e testada com fixtures; investigações acadêmicas PENDENTES. Este documento descreve o uso dos scripts, sem aprovar o plano pelo grupo. `plano_humano.md`, `tasks/03-investigacoes.md` e `docs/RUBRIC.md` definem hipóteses, controles e critérios de refutação. A autoria/cronologia do planejamento com apoio de LLM precisa ser discutida honestamente com o professor, conforme o portão do plano.

## Comandos no Ubuntu KIT11

Na raiz `/home/kit11/Kit11-AF`, com Docker Rootless, Ollama e Qwen3 4B já disponíveis no PATH/ambiente existente:

```sh
./scripts/af_run.sh INV-01
```

Depois de concluir/revisar a primeira sessão e quando o grupo decidir iniciar outro cenário, usar separadamente:

```sh
./scripts/af_run.sh INV-02
```

```sh
./scripts/af_run.sh INV-03
```

INV-01 investiga H1 (reconhecimento/enumeração); INV-02, H2 (entradas inválidas na autenticação); INV-03, H3 (recursos existentes/inexistentes). Somente o objetivo é enviado ao modelo. O sumarizador verifica o hash do snapshot aprovado e extrai os caminhos destacados em Markdown da seção do cenário para comparar com propostas. Mudanças de formato/caminhos sem destaque exigem comparação manual; snapshot ausente ou hash divergente tornam a comparação indisponível. Essa tabela não determina a próxima ferramenta do agente.

## Portões e limites

1. O comando exige entrada e saída em terminal; não aceita pipe, arquivo de respostas ou opção de aprovação automática. O grupo informa pessoas, data/referência da deliberação, justificativa e digita `APROVAR INV-01` (ou o ID correspondente). Registra hash do plano, snapshot privado e commit do código. Isso registra declaração humana; não comprova autoria prévia sem LLM.
2. O grupo informa referências verificáveis da evidência atual Kali/OpenVPN → `10.0.80.3:3001` e da comprovação de isolamento WAN. `PENDENTE` ou `NÃO VERIFICADO` interrompem antes de consultar Docker/modelo. `REDE VERIFICADA` registra a declaração do grupo, sem produzir prova de rede automaticamente. O código não consulta WAN, pfSense ou Kali.
3. O preflight reutiliza `lab_common.sh`: Docker Rootless pelo socket local, imagem/digest, identidade, rótulos, ausência de mounts/privilégios e dois bindings exatos; verifica container ativo, Nmap e `/api/tags` do Ollama local contendo `qwen3:4b-instruct`. Não inicia daemons nem instala componentes.
4. `OFERECER` chama `restore.sh`. Ele exige **outra confirmação, `RESTAURAR`**, antes de apagar os dados descartáveis do container validado. Cancelamento encerra a sessão. Registra ID anterior/novo, reinspeciona e espera GET `/` retornar 200 por até aproximadamente 60 s (cada chamada com prazo de 8 s). Readiness é consulta mecânica identificada; não é proposta do Qwen nem descoberta acadêmica. Os bindings permanecem fixos.
5. Antes da primeira consulta ao modelo, o script revalida container e hash do plano. `agent.run_session` preserva propostas dinâmicas, aprovação/modificação/rejeição/encerramento, justificativas e segunda aprovação de modificação validada. Cada ferramenta exige decisão humana real. São no máximo **6 propostas e 12 chamadas ao modelo** por sessão; HTTP/Nmap mantêm os limites existentes.
6. Na INV-02, POST é limitado aos controles A/B/C inválidos do plano em `/rest/user/login`: identificador `af_inexistente_01@kit11.invalid`, senha de laboratório `teste-invalido-01`, vazia ou omitida, uma execução de cada variante por sessão. Outra entrada ou repetição encerra as ferramentas com `acao_bloqueada`, mesmo após aprovação. Esse bloqueio mecânico não aprova nenhuma ação. Conta descartável opcional exige revisão futura explícita do escopo; não está habilitada neste comando.
7. HTTP 429 encerra novas ferramentas após a interpretação/decisão humana; erro de interpretação também encerra o ciclo. O grupo deve encerrar diante de outros sinais de bloqueio, dados sensíveis, falha repetitiva ou ausência de informação útil. As hipóteses não são decididas por código.
8. Após cada interpretação, registrar na justificativa: correta/parcial/incorreta/inconclusiva, fundamento e IDs relevantes. Ao final: hipótese confirmada/refutada/inconclusiva, evidências por result_id, limites e alternativas. Não fabricar erro do Qwen para cumprir rubrica. EOF/Ctrl-C não geram conclusão humana presumida.

Não executar investigações enquanto os portões do plano estiverem pendentes. Não há autorização adicional para mudar firewall, NAT, VPN, serviços ou bindings. Acessibilidade por IP privado/VPN não comprova isolamento WAN. O preflight não substitui a verificação externa pelo grupo.

## Evidências e síntese

Cada tentativa recebe `run_id` e diretório privado `logs/INV-0N/<run_id>/`:

- `sessao.jsonl`: preparação, aprovação, estado, restauração e eventos do agente com o mesmo run_id/investigation_id; parâmetros, propostas, justificativas, resultados, duração, interpretação, decisões e IDs.
- `plano-aprovado.md`: snapshot da versão cuja aprovação foi declarada (ausente se cancelado antes disso).
- `resumo.md`: planejamento × propostas reais, intervenções, resultados resumidos, interpretações atribuídas ao Qwen, conclusão atribuída ao grupo, lacunas e matriz de todos os eventos com linhas/IDs do JSONL.

Os arquivos permanecem fora do Git, com diretórios 0700 e arquivos 0600. Campos conhecidos de senha/token são redigidos; texto livre e corpos podem conter segredos. **Privado não equivale a sanitizado**: revisar manualmente trechos e capturas antes de compartilhar. O resumo não inclui corpos HTTP ou saídas Nmap integrais: consultar os result_ids no JSONL para sustentar cada afirmação.

A síntese roda também em cancelamento/erro, quando existir log legível. Para reprocessar uma sessão local, substitua o caminho pelo run_id verdadeiro:

```sh
python3 scripts/af_summarize.py logs/INV-01/SEU_RUN_ID/sessao.jsonl
```

Para atualizar também as contagens de evidências:

```sh
python3 scripts/af_summarize.py logs/INV-01/SEU_RUN_ID/sessao.jsonl --update-status
```

O runner atualiza automaticamente seções delimitadas em `CHECKLIST_RUBRICA.md` e `docs/STATE.md` com ID, contagens e pendência de revisão. Preserva histórico, não promove a CONCLUÍDO, não publica no Git e não comprova autenticidade/correção por mera contagem. A rubrica deve ser validada pelo grupo com os logs e evidências de rede. O sumarizador verifica uma sessão por arquivo, event_ids únicos, autorização/ação antes de execução, resultado e interpretação vinculados; lacunas são reportadas. Fixtures/engenharia são rotuladas e recusadas para atualização acadêmica.

## Relatório e vídeo

Usar `relatorio_template.md` e `roteiro_video.md`, juntamente com os resumos privados revisados. A distribuição sugerida é: 1 página de ambiente/escopo, 1 de plano e método, 2–3 das três investigações com referências por ID e 1 de análise crítica/limitações/reprodução (total 5–6 páginas). Não preencher lacunas com resultados de engenharia ou fixtures.

No vídeo de até 10 minutos, mostrar pelo menos uma investigação completa: contexto/plano (2 min), proposta/decisão (3 min), resultado/interpretação/adaptação (3 min), conclusão e limitação observada (2 min). Selecionar capturas depois das execuções reais, revisar segredos e medir duração. A automação prepara a organização; relatório final, vídeo e aprovações continuam PENDENTES e pertencem ao grupo.

## Validação da preparação

`python3 -m unittest discover -s tests -v` usa fixtures/mocks identificados; integrações reais são opt-in e devem permanecer desabilitadas nesta preparação. Os novos testes simulam aprovação, serviços, Docker e restauração apenas em diretórios temporários; não constituem decisões reais do grupo nem investigações. Nenhuma ação ofensiva, restauração real ou consulta Qwen é necessária para testar os scripts.
