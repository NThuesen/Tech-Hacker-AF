# Operação do bloco 03B v2

O agente histórico continua disponível pelo procedimento em `OPERACAO_BLOCO03.md`. O modo 03B é separado e opt-in; remover a opção de contexto ou usar o procedimento histórico não altera logs anteriores. Decisões de Codex delegado não são entradas humanas.

## Replay: nenhuma ferramenta de investigação

```sh
python3 scripts/af_replay.py fixtures/03b/replay-simulado.json
```

O comando valida até três pares de sensibilidade, três de memória e um de estabilidade; não consulta Ollama nem executa ferramentas. As evidências no arquivo são **FIXTURE/SIMULADAS**, inclusive o texto hostil. A validação verifica objetivo idêntico, uma diferença estrutural no par de sensibilidade e o mesmo conjunto de valores no par de memória; isso não comprova equivalência semântica. Os pares são pequenos ensaios de engenharia, sem interpretação estatística. Para memória, compare os fatos realmente disponíveis em A e B: quando divergem, não atribua diferença apenas ao formato.

Para consultar o modelo local, obtenha o digest exato de `qwen3:4b-instruct` em `/api/tags`, crie um diretório privado e use:

```sh
mkdir -p -m 700 logs/03B/replay-local
python3 scripts/af_replay.py fixtures/03b/replay-simulado.json --ollama --model-digest DIGEST_EXATO --output logs/03B/replay-local/sessao.jsonl
```

É exigido terminal e confirmação. O replay só acessa o Ollama em `127.0.0.1:11434`, não importa nem chama o executor do agente e nunca executa a proposta. Registra envelope e telemetria no JSONL **privado**; revise seu conteúdo antes de compartilhar. O arquivo de saída precisa ser novo; o programa não acrescenta a sessão a um arquivo existente. A autorização de Nicholas para este projeto permite operação pelo Codex, mas não transforma a digitação do Codex em decisão humana por ferramenta. O schema histórico não representa uma decisão de parar; ela deve ser avaliada separadamente. Temperatura zero não garante respostas idênticas.

O limite de 14 solicitações é compartilhado entre invocações: `logs/03B/replay-orcamento.jsonl` conserva reservas duráveis sob bloqueio de arquivo; cada tentativa consome uma reserva antes da consulta, inclusive se for interrompida. Na primeira utilização, JSONL históricos privados dentro de `logs/03B/` são lidos para incorporar solicitações de replay anteriores. Os registros anteriores conhecidos somam 17 solicitações, então o orçamento existente está esgotado e novas consultas devem ser recusadas. Esta proteção depende da preservação do arquivo de orçamento e dos logs históricos; não é resistente a exclusão ou adulteração deliberada pelo proprietário. Qualquer novo protocolo ou orçamento precisa de decisão humana expressa e rastreável; não apague registros para contornar o limite.

Para `evidence_source.type=real`, informe `artifact` em `logs/`, `sha256` e `result_id` do evento. O programa confere arquivo privado, hash e existência do resultado, mas essa verificação estrutural não comprova que uma interpretação ou um contexto contrafactual representa fielmente o resultado: registre e revise as diferenças do snapshot.

## Sessão 03B ao vivo

```sh
python3 scripts/af_refine.py INV-01-B --context-mode A
python3 scripts/af_refine.py INV-02-B --context-mode B
python3 scripts/af_refine.py INV-03-B --context-mode B
```

Execute uma sessão de cada vez. O processo exige TTY, registro explícito de integrantes/data/referência e hash do plano; reutiliza o preflight histórico, que solicita evidências **atuais** Kali/VPN e WAN, valida identidade Rootless e pede confirmação antes de restaurar. Confere novamente os hashes e a identidade antes de cada ação. `A` preserva o histórico anterior; `B` envia até oito registros factuais, com hashes e tamanhos de saída. Por não enviar o texto bruto das saídas, B pode apresentar menos informação que A; qualquer comparação deve relatar essa diferença. A interpretação de cada resultado continua isolada.

No cenário 02, cada corpo A/B/C é aceito no máximo uma vez; no 03, a resposta `/ftp/` completa deve ser reconhecida como listagem pelo operador antes do controle `.md` ou do positivo condicionado. A confirmação da listagem não demonstra inocuidade de arquivos. Resultados 423/429, erro, possível segredo ou qualquer redirecionamento param a sessão. Não execute enquanto rede, identidade ou disponibilidade não estiverem comprovadas. A ferramenta live atual exige entrada de terminal; não implementa a revisão delegada 03B em canal privado.

O histórico declarou o Juice Shop 17.3.0 no container identificado por `lab_common.sh` e Qwen `qwen3:4b-instruct`. O estado real pode mudar: o preflight deve verificá-lo, não confiar apenas na documentação. Nenhuma configuração de pfSense, NAT ou firewall deve ser alterada por estes comandos.

## Métricas e privacidade

```sh
mkdir -p -m 700 logs/03B/metricas
python3 scripts/af_metrics.py logs/03B/replay-local/sessao.jsonl --output-dir logs/03B/metricas
```

Os arquivos CSV/Markdown e o manifesto SHA256 são privados. O formulário traz uma linha inicial por interpretação, com texto e classe vazios; o avaliador deve dividir alegações, redigir trechos e preencher a avaliação. O formulário de pares começa vazio. Para somar avaliações já realizadas, use `--avaliacoes caminho.csv` e/ou `--avaliacoes-pares caminho.csv` em uma nova exportação: as classificações exigem ID único, justificativa, avaliador e data. A planilha de pares aceita `pertinente` ou `nao_pertinente`. Divergências precisam ser resolvidas e documentadas antes de uma linha consolidada; o programa não decide entre avaliadores. As contagens não determinam vulnerabilidade ou correção semântica. A exportação separa tipo e cenário quando informados; para sessões legadas sem `trial_type`, a origem permanece **NÃO INFORMADA**, não presumida. Arquivos existentes são preservados e causam recusa; use diretório novo por exportação. Não publique os JSONL sem revisão de segredos.

## Estado

**IMPLEMENTADO COM FIXTURES. P6 NÃO AUTORIZADO nesta etapa.** Sessões 03B ao vivo e novos controles HTTP não são comprovados pelo replay, que não usa o Juice Shop. O teste histórico Kali/WAN vale somente para o caminho e a data registrados; é necessária evidência atual antes de nova sessão. As execuções reais de replay feitas anteriormente e suas limitações permanecem no histórico de `STATE.md`, sem serem confundidas com os testes desta etapa.
