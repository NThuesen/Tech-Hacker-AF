# Matriz de rastreabilidade — AF Tecnologias Hackers 2026.2

**Fonte normativa:** `docs/AF - Tecnologias Hackers 26-2.pdf` (11 páginas). Esta matriz resume a AF; em caso de dúvida, prevalece o PDF.

| Critério da rubrica (p. 10) | Peso | Como comprovar |
|---|---:|---|
| Laboratório reproduzível | 15% | instalação validada, versões/configuração, HTTP Juice Shop, modelo local, restauração real |
| Agente supervisionado | 20% | >=2 ferramentas, >=1 acessa Juice Shop, LLM escolhe e adapta ferramenta/parâmetros, intervenção humana antes de executar |
| Planejamento e testes | 20% | plano humano **antes do LLM**, hipóteses e evidências pretendidas; três investigações distintas |
| Evidências e interpretação | 20% | trilha de proposta, ferramenta, parâmetros, decisão humana, resposta, interpretação e decisão final |
| Análise crítica da IA | 20% | comparação humano vs. IA, adequações/erros, resposta às evidências, limitação concreta observada, intervenção humana |
| Documentação/apresentação | 5% | instruções reproduzíveis, código, registros, relatório 4–6 páginas, vídeo <=10 min |

## Condições explícitas da AF
- Aplicação: **OWASP Juice Shop local** acessível a partir do Kali; alvo exclusivo da investigação.
- Modelo: LLM **local**, ex. Qwen3 4B quantizado via Ollama.
- No mínimo **duas ferramentas integradas**, uma interagindo diretamente com o Juice Shop; Nmap/curl são exemplos, não obrigatórios.
- O LLM decide próximo passo **com base nos resultados**, não segue sequência predeterminada.
- Grupo pode **autorizar, modificar ou rejeitar**; resultados da ferramenta retornam ao modelo.
- Logs completos consultáveis, mesmo sem transcrever tudo no relatório.
- Restaurar o Juice Shop ao estado conhecido para repetibilidade.
- Primeiro registrar estratégia e hipóteses **sem uso do LLM**; depois documentar sugestões aceitas/modificadas/rejeitadas e justificativas.
- **Três investigações distintas** (sugestões: reconhecimento, autenticação/autorização, entradas/recursos); para cada: hipótese, plano humano, contribuição da IA, execução, intervenção, conclusão/limitação.
- Uma investigação **sem vulnerabilidade confirmada é válida**, desde que as evidências sustentem a conclusão.
- Análise crítica deve ter **ao menos um exemplo real** de limitação, erro ou dificuldade de uso da IA, com diagnóstico e tratamento.
- Entregáveis: laboratório, código, registros, relatório **4–6 páginas** e vídeo **até 10 minutos**, mostrando ao menos uma investigação completa.
- A nota não é baseada na quantidade de vulnerabilidades ou autonomia.

## Não são evidências suficientes
- Resultado de teste com mock = comprovação de serviço real.
- Sugestão do LLM = confirmação de vulnerabilidade.
- Um HTTP 200 isolado = confirmação automática de falha de controle de acesso.
- Captura sem contexto = interpretação.
- Template preenchido por Codex = decisão humana real.

## Portões de qualidade
Cada item requer arquivo de evidência, data/ambiente e responsável pela validação. Marcar NÂO VERIFICADO enquanto não observado; evitar prometer 100% da nota.
