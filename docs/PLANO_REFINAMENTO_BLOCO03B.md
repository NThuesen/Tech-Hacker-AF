# Bloco 03B — Plano complementar de refinamento experimental

**Estado: PLANEJADO — nenhuma implementação ou nova execução foi autorizada por este documento.**  
**Projeto:** AF Tecnologias Hackers 2026.2 — KIT11.  
**Versão do plano complementar:** 1.0, 29/10/2026.  
**Relação com o planejamento original:** adendo posterior aos resultados do Bloco 03; **não altera nem substitui** `plano_humano.md`, sua aprovação, suas datas, hipóteses ou hashes.

## 1. Motivação e perguntas

Os três cenários originais foram executados tecnicamente; seus resultados permanecem preservados nos resumos e na branch `evidencias/logs-completos-2026-10-27`. Eles são o **baseline histórico**, não devem ser reescritos, reclassificados ou apresentados como execução do 03B.

Lacunas identificadas:
- **INV-01:** Nmap constatou 3000/tcp aberta, GET revelou v17.3.0 e recurso público; os caminhos candidatos haviam sido informados ao Qwen. Há evidência de seleção de ferramentas, mas pouca evidência de descoberta independente.
- **INV-02:** duas variantes inválidas (A, B) devolveram 401 e mesmo corpo; a variante C (senha omitida) não foi realizada e faltou comparar explicitamente os três controles.
- **INV-03:** listagem de `/ftp/` observada (200), mas o controle inexistente `.txt` devolveu 403 por filtro de extensão. Existência e extensão variaram simultaneamente; não foi possível inferir o tratamento de arquivo inexistente.
- **Análise da IA:** observaram-se extrapolações, interpretação do rótulo `ppp` e alegações de HTML completo embora truncado. A interpretação atual recebe o resultado isolado, enquanto a decisão subsequente usa histórico compacto; é necessário testar se um sumário factual rastreável melhora a consistência **sem fornecer resultados inventados**.

### Objetivo do 03B

Melhorar a **qualidade dos controles**, a relação entre resultados e decisões do modelo e a rastreabilidade da supervisão, sem ampliar o alvo ou adicionar uma plataforma de pentest.

### Hipóteses complementares

- **H1B (condicionamento):** quando recebe objetivo, escopo e histórico factual, o Qwen consegue selecionar ao menos uma ação pertinente condicionada ao resultado anterior; isso será avaliado pelo **motivo demonstrado no log**, não pela simples mudança de ferramenta.
- **H2B (campo omitido):** omitir `password` mantendo todos os demais parâmetros constantes pode ou não produzir resposta diferente das variantes A/B; comparar status, Content-Type, corpo e tratamento do erro, sem inferir bypass.
- **H3B (controle de existência):** usar caminho fictício não listado com extensão permitida `.md`, juntamente com a observação do filtro de extensão para `.txt`, permite separar melhor ausência de recurso de rejeição por extensão. Uma listagem HTTP 200 continua sem provar exposição indevida.

## 2. Regras gerais, ambiente e autoria

- Instância única permitida: **Juice Shop v17.3.0**, identificada por imagem/digest/container validado no KIT11; ferramenta do Qwen acessa somente `127.0.0.1:3000`. O Kali pode validar, separadamente, `10.0.80.3:3001` por VPN, sem novos testes fora do Juice Shop.
- Qwen3 `qwen3:4b-instruct` via Ollama em `127.0.0.1:11434`; ferramentas existentes: `nmap` porta 3000, `http_get`, `http_post`. **Sem novas ferramentas** por padrão.
- Sem alterações em pfSense, OpenVPN, WordPress, Nextcloud, WAN/NAT/firewall, outras máquinas ou outros serviços. Proibidos enumeração massiva, brute force, SQLi, LFI/RFI, downloads de arquivos privados, contas reais e tokens.
- Restauro antes de **cada** cenário mediante identificação prévia de container, comprovação do estado anterior, autorização humana e registro de ID anterior/novo. Nunca remover outro container. Falhas em identidade/rede abortam.
- **Plano complementar submetido ao grupo antes dos novos testes**: inserir nomes reais, data/hora real e versão/commit aprovado; se houver alterações posteriores à aprovação, registrar novo hash e aprovar novamente. Este adendo foi concebido **após** o uso do LLM no Bloco 03; não se apresentar como planejamento original sem LLM.
- Para buscar o requisito mais exigente da rubrica, usar **modo supervisionado por humano por ação** nas sessões do 03B: aprovar, modificar (com segunda confirmação), rejeitar ou encerrar e justificar; interpretar cada resultado e concluir pessoalmente. Codex pode implementar/corrigir o software e preparar a infraestrutura, mas **não pode registrar decisões automatizadas como decisões humanas**. Se houver nova delegação expressa, registrar claramente origem e confirmar com o professor sua equivalência acadêmica; sem aprovação tácita.
- **Sessões novas, novas identidades**: `phase=03B`, `scenario=INV-0N-B`, `run_id` novo; preservar `investigation_id` original somente como chave de compatibilidade, nunca sobrescrever logs existentes. O arquivo `plano_humano.md` aprovado fica imutável; snapshot separado do adendo e seu SHA256.

## 3. Matriz de experimentos, variáveis e decisões

| Experimento | Controle | Variável isolada | Evidência necessária | Interpretação permitida |
|---|---|---|---|---|
| **INV-01B** — confirmação contextual | GET `/` / Nmap e versão, quando justificados | Próxima ação escolhida com base no último resultado, não sequência imposta | proposta, histórico conhecido, justificativa, ação seguinte, resultado | seleção condicional observada, sem alegar descoberta de rotas que já estavam no objetivo |
| **INV-02B** — A/B/C | A = senha inválida fictícia; B = senha vazia; C = senha omitida; email fictício fixo | presença/valor do campo `password`; demais valores invariáveis | POST único por variante, status, tipo, mensagem, diferenças corpo, IDs e tempos | comparação somente das variantes realmente medidas |
| **INV-03B** — controle negativo corrigido | `/ftp/` (listagem); histórico `.txt` bloqueado | novo candidato `/ftp/arquivo-inexistente-af.md` com extensão permitida | ausência do nome na listagem, status/corpo de `.md`, comparação com `.txt` histórico e controles do mesmo estado | distinguir o que seria compatível com ausência vs filtro de extensão; sem presumir comportamento por status |
| **INV-03B opcional** — controle positivo | **somente** `/ftp/legal.md` ou `/ftp/README.md`, se nome estiver **visível na listagem real da sessão** e conteúdo for previamente considerado público/não sensível | existência de recurso com extensão permitida | GET isolado aprovado, tipo/corpo limitado/sem segredos, link observado previamente | recurso HTTP público acessível; nada sobre demais arquivos |

### INV-01B: protocolo de seleção dinâmica

1. Objetivo fornecido ao Qwen: identificar **uma** característica observável da instância e justificar o próximo passo após resultado real; pode informar categorias de ferramentas e limites, **não** uma sequência de rotas.
2. O revisor não antecipa resultados e não diz “rode Nmap em seguida” como comando disfarçado. Uma correção factual pode explicitar “o resultado atual só comprova X; Y não foi observado”; a decisão seguinte permanece do Qwen.
3. Registrar a diferença entre os cenários: (a) com candidatos conhecidos previstos no plano e (b) com objetivo menos prescritivo, dentro de uma **allowlist técnica pequena**. Se Qwen sugerir rota desconhecida, rejeitar com razão técnica e dar a ele nova oportunidade de propor; não liberar requisições arbitrárias.
4. Critério observável: ao menos uma decisão subsequente justificada por um `result_id` ou pela correção do revisor. Se repetir uma ação sem ganho, registrar **limitação** em vez de inventar adaptação.
5. Não realizar novos scans além da porta TCP/3000 nem enumerar IDs de produtos.

### INV-02B: controles invalidos A/B/C

A rota é `POST /rest/user/login`, com identificador **`af_inexistente_01@kit11.invalid`**; as três variantes pré-autorizáveis são:

```json
{"email":"af_inexistente_01@kit11.invalid","password":"teste-invalido-01"}
```

```json
{"email":"af_inexistente_01@kit11.invalid","password":""}
```

```json
{"email":"af_inexistente_01@kit11.invalid"}
```

**No máximo uma tentativa por variante por sessão**, nunca login real nem loop. Registrar A/B como baseline de 27/10, mas se comparar temporalmente A/B/C em igualdade de estado, executar cada variante **uma vez em uma mesma sessão nova**, após restauração. Se o Qwen interromper após duas e o grupo considerar suficiente, registrar C não realizado; não executar C fora da cadeia sem declarar experimento adicional separado. Um controle positivo com conta descartável fica **FORA DO ESCOPO 03B**, pois requer gestão de conta, persistência, consentimento e mudança de guards; somente mediante proposta separada e aprovação formal.

### INV-03B: corrigir controle de ausência e extensão

1. GET `/ftp/`, verificar a listagem real e que `arquivo-inexistente-af.md` **não consta nela**. Se constar, cancelar, escolher outro nome benigno com aprovação e registrar a mudança.
2. GET `/ftp/arquivo-inexistente-af.md` (**candidato**, nunca presumir status).
3. Comparar com o histórico `.txt` de 27/10, explicitando que ocorre em rodada diferente; se necessário e autorizado, um novo GET `.txt` na mesma sessão permite controle pareado. **Não usar bypass de extensão, codificações evasivas, traversal ou leitura fora do escopo.**
4. O HTTP 403 da rodada anterior foi acompanhado por `Only .md and .pdf files are allowed!`; pode indicar filtro de extensão, mas não comprova autorização. Se `.md` também for 403, registrar hipóteses alternativas e não forçar conclusão. HTTP 404, 200 ou 403 exigem interpretação ligada ao corpo recebido.
5. Opcional: um único documento `.md` **comprovadamente público** e explicitamente aprovado pelo grupo, com revisão prévia de risco. Não baixar arquivos que pareçam relatórios, dados pessoais ou segredos.

## 4. Regras de operação, evidência e segurança

**Antes:** estado do KIT11 e versão; internet/WAN fora do alcance; plano original e adendo aprovados; identidade do container e restauração documentadas. **Durante:** até seis propostas e doze consultas ao LLM por cenário; timeout HTTP 8 s, respostas limitadas a 16 KiB, contexto até limite existente; Nmap fixo; decisões antes de ferramentas; uma ação por vez. **Depois:** cada resultado deve ter `result_id` e interpretação, avaliação/revisão, conclusão do responsável e comparação baseline/03B.

**Parar imediatamente** diante de alteração inesperada de alvo, erro de identidade/container, resposta HTTP 423/429, dado sensível, segredo ou conteúdo privado, redirecionamento para fora do alvo, ferramenta indisponível, timeout repetido, rota fora da allowlist, duplicação de teste A/B/C, solicitação de scan amplo ou ausência de ganho informacional.

Exigir no mínimo:
- `event_id`, `run_id`, `phase`, `scenario`, `proposal_id`, `execution_id`, `result_id`, `timestamp` em cada evento aplicável.
- `origem_decisao` verificável (`entrada_terminal_humana` ou `delegada`) e **nunca transformar origem por mudança de rótulo**.
- `experiment_variant` A/B/C, controle de extensão e hash de plano original + adendo; `preflight`, restauração, imagem/modelo e commit do código.
- Estado explícito **observado**, **inferido**, **não testado** para cada afirmação.
- Sínteses novas em `docs/investigacoes/03B/` **somente depois** de execução e revisão, sem sobrescrever `INV-01/02/03`.
- Logs novos em `logs/03B/INV-0N/<run_id>/` privados, sem publicação/merge automático; a branch histórica de logs permanece intacta. Se o relatório de 4–6 páginas citar novos resultados, acrescentar referência cruzada e reduzir conteúdo menos relevante; não declarar resultados antes de medi-los.

## 5. Relação direta com a rubrica

| Peso | O que 03B deve reforçar | Evidência de aceite |
|---:|---|---|
| **15%** laboratório | revalidação das identidades e restauração por cenário | preflight+restauração+HTTP 200 e escopo preservado |
| **20%** agente supervisionado | escolhas realmente condicionais; decisão humana antes da ação | JSONL com sequência causal rastreável e `decisao_humana` genuína |
| **20%** planejamento | adendo explícito, hipóteses e variáveis corrigidas | duas versões com SHA e data, comparação original→refinamento |
| **20%** evidências | A/B/C e controle corrigido, respostas integralmente rastreáveis | tabela por `result_id` e status/corpos, conclusão proporcional |
| **20%** análise crítica | evidência antecipada, contexto parcial, desenho de controle | correção efetivamente registrada e efeito/limites verificados |
| **5%** documentação | atualizar relatório de 4–6 páginas e vídeo <=10min | relatório versionado e vídeo mostrando um ciclo **real** e completo |

**Nenhuma etapa garante nota máxima:** satisfazer a rubrica depende de execução, qualidade da interpretação e avaliação do professor. Resultado negativo e hipótese inconclusiva são válidos.

## 6. Portão de aprovação do adendo — preencher antes de executar

- Responsável/grupo: **[preencher com integrantes verdadeiros]**.
- Data/hora real da aprovação: **[pendente]**.
- Commit e SHA256 do adendo efetivamente aprovado: **[pendente]**.
- Mudanças deliberadas e justificativa: **[pendente]**.
- Autorização para recriar **somente** o container validado do Juice Shop em cada cenário: **[a confirmar em tempo de execução]**.
- Evidência de conectividade/isolamento válida na data da execução: **[a confirmar]**.
- Requisitos de autoria/supervisão humana discutidos com o professor: **[registrar conforme ocorrido]**.

**Próximo passo:** o Codex deve **implementar e testar a infraestrutura em fixtures primeiro**, seguindo `tasks/03b-refinamento-experimental.md`. Execuções reais só após aprovação/portões; os resultados 03B ainda **não existem**.
