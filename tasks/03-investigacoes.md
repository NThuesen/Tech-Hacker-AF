# Bloco 03 — Três investigações supervisionadas

## Pré-condição **obrigatória**
`plano_humano.md` foi criado e **aprovado pelo grupo antes de consultar o LLM**. Confirmar pessoas/data e guardar versão inicial assinada ou commitada. Sem aprovação: PARAR; não preencher por conta própria.

## Cenários sugeridos (confirmar com grupo)
1. Reconhecimento/enumeração: porta, serviço, rotas HTTP e hipóteses.
2. Autenticação: entradas controladas, comparar respostas de login sem força bruta.
3. Recursos/documentos: exposição de arquivos e controle de acesso HTTP. **Não confundir arquivo acessível com LFI/RFI**.

## Método para CADA investigação
1. Registrar objetivo, hipótese, risco, ferramentas possíveis, evidência necessária, condição de refutação e limites.
2. Criar estado de partida conhecido; manter evidência da restauração.
3. LLM propõe ferramenta/parâmetros; mostrar justificativa; grupo aprova/modifica/rejeita **ação por ação**.
4. Gravar respostas reais (status, cabeçalhos relevantes, corpo limitado, timestamps), decisão e interpretação do resultado.
5. Escolher próximo teste condicionado à evidência; preservar histórico completo e apontar erros, sugestões repetitivas ou limitações reais.
6. Encerrar com conclusão proporcional à evidência, possíveis alternativas e o que **não** foi demonstrado.
7. Confrontar com plano humano e classificar contribuições da IA (acerto, erro, desnecessário, intervenção).

## Critérios de aceite
- Três casos distintos completos com seis componentes da rubrica: hipótese, plano, contribuição IA, execução, intervenção e conclusão.
- Logs JSONL, screenshots/artefatos e rastreio entre IDs e texto do relatório; nada inventado.
- Ao menos uma rejeição/modificação real quando tecnicamente justificada, **sem criar erro artificial**.
- No mínimo uma dificuldade/limitação real analisada, inclusive se for problema de modelo/integração.
- Não é preciso confirmar vulnerabilidade em todos os casos.

## Regras
Só Juice Shop do KIT11, sem testes em serviços externos ou sistemas dos colegas. Não usar Codex para automatizar aprovação humana.
