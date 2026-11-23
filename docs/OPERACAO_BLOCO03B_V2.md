# Operação do bloco 03B v2

O agente histórico continua disponível pelo procedimento em `OPERACAO_BLOCO03.md`. O modo 03B é separado e opt-in; remover a opção de contexto ou usar o procedimento histórico não altera logs anteriores. Decisões de Codex delegado não são entradas humanas.

## Replay: nenhuma ferramenta de investigação

```sh
python3 scripts/af_replay.py fixtures/03b/replay-simulado.json
```

O comando valida até três pares de sensibilidade, três de memória e um de estabilidade; não consulta Ollama nem executa ferramentas. As evidências no arquivo são **FIXTURE/SIMULADAS**, inclusive o texto hostil. A validação verifica objetivo idêntico, uma diferença estrutural no par de sensibilidade e o mesmo conjunto de valores no par de memória; isso não comprova equivalência semântica. Os pares são pequenos ensaios de engenharia, sem interpretação estatística. Para memória, compare os fatos realmente disponíveis em A e B: quando divergem, não atribua diferença apenas ao formato. A instrução atual solicita justificativa da escolha; o prompt mudou em relação aos replays históricos e resultados de versões diferentes não constituem comparação controlada direta.

Para consultar o modelo local, obtenha o digest exato de `qwen3:4b-instruct` em `/api/tags`, crie um diretório privado e use:

```sh
mkdir -p -m 700 logs/03B/replay-local
python3 scripts/af_replay.py fixtures/03b/replay-simulado.json --ollama --model-digest DIGEST_EXATO --output logs/03B/replay-local/sessao.jsonl
```

É exigido terminal e confirmação. O replay só acessa o Ollama em `127.0.0.1:11434`, não importa nem chama o executor do agente e nunca executa a proposta. Registra envelope e telemetria no JSONL **privado**; revise seu conteúdo antes de compartilhar. O arquivo de saída precisa ser novo; o programa não acrescenta a sessão a um arquivo existente. A autorização de Nicholas para este projeto permite operação pelo Codex, mas não transforma a digitação do Codex em decisão humana por ferramenta. O schema histórico não representa uma decisão de parar; ela deve ser avaliada separadamente. Temperatura zero não garante respostas idênticas.

O limite de 14 solicitações é compartilhado entre invocações: `logs/03B/replay-orcamento.jsonl` conserva reservas duráveis sob bloqueio de arquivo; cada tentativa consome uma reserva antes da consulta, inclusive se for interrompida. Na primeira utilização, JSONL históricos privados dentro de `logs/03B/` são lidos para incorporar solicitações de replay anteriores. Os registros anteriores conhecidos somam 17 solicitações, então o orçamento existente está esgotado e novas consultas devem ser recusadas. Esta proteção depende da preservação do arquivo de orçamento e dos logs históricos; não é resistente a exclusão ou adulteração deliberada pelo proprietário. Qualquer novo protocolo ou orçamento precisa de decisão humana expressa e rastreável; não apague registros para contornar o limite.

Para `evidence_source.type=real`, informe `artifact` em `logs/`, `sha256` e `result_id` do evento. O programa confere arquivo privado, hash e existência do resultado, mas essa verificação estrutural não comprova que uma interpretação ou um contexto contrafactual representa fielmente o resultado: registre e revise as diferenças do snapshot.

## Sessão 03B ao vivo

**A supervisão é presencial no terminal.** O integrante do grupo informa seu nome e sobrenome reais e digita `ASSUMO` para declarar que está conduzindo a sessão. Esse nome é registrado em cada decisão; Nicholas faz a revisão final e não é automaticamente registrado como supervisor. Não execute por pipe nem forneça respostas automáticas.

Em cada proposta, o programa mostra investigação, objetivo, justificativa fornecida pelo Qwen, ferramenta, argumentos efetivos, riscos e evidências disponíveis. As decisões usam uma tecla, sem Enter: **A** aprova, **M** permite editar a ação, **R** rejeita e **P** pausa. Na pausa, **C** volta à revisão e **E** encerra; continuar a revisão não aprova a ação. Uma modificação exige nova confirmação **A** e passa novamente pelos validadores de escopo. A aprovação simples não exige justificativa digitada; o registro contém `justificativa: null`, não uma explicação inventada. Após o resultado, o supervisor avalia a interpretação e registra sua justificativa ou pendência no fluxo existente.

### Preparação com o supervisor

1. Antes de publicar a aplicação, o grupo verifica as regras WAN/NAT atuais para a porta 3001 e documenta a evidência; não alterar pfSense automaticamente. Verifique também as condições de VPN e o contexto do KIT11.
2. O Docker Rootless deste KIT11 foi instalado fora do PATH padrão. Em um terminal no repositório, ajuste apenas o PATH do processo:

   ```sh
   export PATH="/home/kit11/.local/opt/kit11-docker:$PATH"
   ```

3. Se o container validado estiver parado, o supervisor pode iniciá-lo **manualmente**, somente após verificar as regras de rede. O comando abaixo valida Rootless, imagem e identidade e inicia o ID conferido, sem restaurar dados. A abertura dos bindings `127.0.0.1:3000` e `10.0.80.3:3001` deve ser entendida antes de executá-lo:

   ```sh
   sh -eu -c '. ./scripts/lab_common.sh; lab_preflight; id=$(lab_container_id); lab_docker start "$id"'
   ```

4. Com o container ativo, o integrante no Kali testa o acesso pela VPN em `10.0.80.3:3001` e, separadamente, a porta 3001 no endereço WAN correto sem VPN. Registra horário, comandos, resultados e referências privadas. Um timeout com o container parado não demonstra isolamento. O caminho testado não prova isolamento absoluto; se as condições não forem verificadas, não iniciar as investigações.
5. O supervisor confirma o adendo e o plano histórico com nomes, data, referência e hashes reais. Em seguida, executa uma das sessões abaixo pessoalmente. O preflight solicita evidências atuais e, **separadamente**, a confirmação explícita de restauração; recusar preserva o estado e encerra a preparação.

```sh
python3 scripts/af_refine.py INV-01-B --context-mode A
python3 scripts/af_refine.py INV-02-B --context-mode B
python3 scripts/af_refine.py INV-03-B --context-mode B
```

Execute uma sessão de cada vez, na ordem acima. O processo exige TTY, registro explícito de integrantes/data/referência e hash do plano; reutiliza o preflight histórico, que solicita evidências **atuais** Kali/VPN e WAN, valida identidade Rootless e pede confirmação antes de restaurar. Confere novamente os hashes e a identidade antes de cada ação. `A` preserva o histórico anterior; `B` envia até oito registros factuais, com hashes e tamanhos de saída. Por não enviar o texto bruto das saídas, B pode apresentar menos informação que A; qualquer comparação deve relatar essa diferença. A interpretação de cada resultado continua isolada.

No cenário 02, cada corpo A/B/C é aceito no máximo uma vez; no 03, a resposta `/ftp/` completa deve ser reconhecida como listagem pelo operador antes do controle `.md` ou do positivo condicionado. A confirmação da listagem não demonstra inocuidade de arquivos. Resultados 423/429, erro, possível segredo ou qualquer redirecionamento param a sessão. Não execute enquanto rede, identidade ou disponibilidade não estiverem comprovadas. O modo humano exige entrada de terminal; o canal delegado separado é descrito abaixo.

A captura distingue teto local, tamanho declarado, enquadramento HTTP e fidelidade do corpo textual. Captura ambígua, incompleta ou sem texto fiel não serve para afirmar completude. Veja o [diagnóstico da INV-03-B](03b/DIAGNOSTICO_CAPTURA_HTTP.md).

O histórico declarou o Juice Shop 17.3.0 no container identificado por `lab_common.sh` e Qwen `qwen3:4b-instruct`. O estado real pode mudar: o preflight deve verificá-lo, não confiar apenas na documentação. Nenhuma configuração de pfSense, NAT ou firewall deve ser alterada por estes comandos.

## Métricas e privacidade

```sh
mkdir -p -m 700 logs/03B/metricas
python3 scripts/af_metrics.py logs/03B/replay-local/sessao.jsonl --output-dir logs/03B/metricas
```

Os arquivos CSV/Markdown e o manifesto SHA256 são privados. O formulário traz uma linha inicial por interpretação, com texto e classe vazios; o avaliador deve dividir alegações, redigir trechos e preencher a avaliação. O formulário de pares começa vazio. Para somar avaliações já realizadas, use `--avaliacoes caminho.csv` e/ou `--avaliacoes-pares caminho.csv` em uma nova exportação: as classificações exigem ID único, justificativa, avaliador e data. A planilha de pares aceita `pertinente` ou `nao_pertinente`. Divergências precisam ser resolvidas e documentadas antes de uma linha consolidada; o programa não decide entre avaliadores. As contagens não determinam vulnerabilidade ou correção semântica. A exportação separa tipo e cenário quando informados; para sessões legadas sem `trial_type`, a origem permanece **NÃO INFORMADA**, não presumida. Arquivos existentes são preservados e causam recusa; use diretório novo por exportação. Não publique os JSONL sem revisão de segredos.

## Estado

**SESSÕES LIVE REALIZADAS; CONTROLE .MD E REVISÃO ACADÊMICA PENDENTES.** O usuário solicitou as investigações sob supervisão humana, condicionadas à verificação atual da rede e à confirmação específica de qualquer restauração. As sessões 03B ao vivo estão documentadas na matriz; o replay não usa o Juice Shop e não as comprova. O teste histórico Kali/WAN vale somente para o caminho e a data registrados; é necessária evidência atual antes de nova sessão. As execuções reais de replay feitas anteriormente e suas limitações permanecem no histórico de `STATE.md`, sem serem confundidas com os testes desta etapa.

## Canal delegado 03B, excepcional

`scripts/af_03b_delegated.py` foi usado somente após autorização expressa de Nicholas para cada restauração e para decisões do Codex. A CLI exige autorização textual, valida dependências e registros humanos prévios específicos da sessão, e usa um diretório privado de revisões por proposta; não existe aprovação automática por padrão. O Codex registra justificativa, revalida modificações e identifica a origem `codex_delegado`. Esse canal não representa intervenção humana individual e não substitui revisão acadêmica. Confira as pré-condições atuais, o código e `--help` antes de qualquer reutilização; os vínculos com registros prévios são específicos deste laboratório. Ver resultados e limites na [matriz](03b/MATRIZ_COMPARATIVA.md).
