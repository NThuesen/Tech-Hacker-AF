# A04 — Controles por investigação (P1)

**Pergunta única:** que ações HTTP/Nmap podem ser propostas sem alterar escopo ou confundir variáveis?
**Dependência:** [A03](A03-sessao-e-gates.md). **Estado:** desenho, nenhuma nova requisição realizada.

## INV-01-B — reconhecimento e decisão contextual

- Nmap **somente TCP/3000** no host fixo do agente; GET apenas nos caminhos pequenos já autorizados pelo plano (`/`, `/rest/admin/application-version`, `/api/Products/1`). Não inserir sequência obrigatória na lógica do runner.
- Objetivo neutro descreve hipótese, limites e ferramentas, não determina “faça Nmap agora”. Se o Qwen sugere rota fora da lista, registrar rejeição/bloqueio, sem tentar descobrir automaticamente.
- Registrar quais rotas foram **dadas como candidatas**; não chamar de descoberta independente. Porta aberta com rótulo Nmap `ppp` sem `-sV` não identifica serviço. Version endpoint HTTP 200 comprova somente a versão devolvida no momento.

## INV-02-B — autenticação A/B/C

- Única rota: `POST /rest/user/login`. Único email fictício: `af_inexistente_01@kit11.invalid`.
- **A:** senha textual fictícia `teste-invalido-01`; **B:** senha `""`; **C:** chave `password` ausente. JSON válido; **uma execução por variante por sessão**, nenhuma quarta variante ou repetição. Não usar credenciais reais, brute force, SQLi ou conta positiva.
- Corpo real redigido no log, mas `variant=A|B|C` permanece explícito. Comparar A/B/C no **mesmo estado/sessão** quando autorizado; status, Content-Type, mensagem/corpo, bytes, redirect, truncagem; `Date` volátil não demonstra diferença semântica.
- Se C não for testada, marcar **NÃO EXECUTADA**. Dois HTTP 401 com corpo igual não provam segurança de autenticação.

## INV-03-B — existência versus extensão

- GET liberados: `/`, `/ftp/`, `/ftp/arquivo-inexistente-af.txt`, `/ftp/arquivo-inexistente-af.md`.
- O GET do `.md` só é admissível **após** GET `/ftp/` **na sessão atual**, com listagem completa, legível e nome candidato **ausente**. Se o nome constar ou a listagem estiver truncada, bloquear e solicitar revisão.
- `.txt` histórico retornou 403 por extensão; novo teste `.txt` na mesma sessão é opcional e exige aprovação. Sem evasão, percent-encoding, traversal, download de arquivo privado ou variação arbitrária de nome.
- Positivo opcional **somente** `/ftp/legal.md` ou `/ftp/README.md` quando o nome aparecer de fato na listagem e o grupo concordar que é público/baixo risco. Se houver suspeita de dados sensíveis, **não baixar**.
- Status 200/403/404 do `.md` são **hipóteses**, não resultados predeterminados. Listagem pública de nomes não equivale a dados privados expostos; filtro por extensão não prova autorização de usuário.

## Critérios de aceite

Fixtures de todas as rotas válidas e inválidas; email diferente, variante repetida, quarta senha, método incorreto, listagem incompleta, nome presente e caminho fora da allowlist devem **bloquear antes do executor**. Testar cancelamento sem HTTP real. Nenhum endpoint adicional é permitido por analogia.

**Próximo:** [A05 — ledger e contexto](A05-ledger-factual.md).
