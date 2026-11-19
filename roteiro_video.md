# Roteiro de apresentação — duração planejada: 9 min 15 s

**Equipe informada:** Nicholas Thuesen e Alison Araujo. **Estado:** roteiro preparado; gravação, duração medida e revisão continuam pendentes. Os registros das investigações de 27/10 identificam o Codex como revisor delegado; não apresentar essas decisões como entradas humanas por ação.

## 0:00–1:00 — Pergunta e limites

Apresentar o objetivo: investigar como Qwen3 4B local propõe ações e interpreta evidências do Juice Shop, inclusive quando sua interpretação erra. Mostrar o plano de H1–H3 e dizer que somente o Juice Shop local foi alvo. Diferenciar a aprovação geral informada pelo responsável das decisões técnicas delegadas efetivamente registradas.

## 1:00–2:00 — Ambiente e agente

Mostrar diagrama ou README: KIT11 físico, Docker Rootless, Juice Shop 17.3.0, Ollama em loopback, Python, Nmap e HTTP. Explicar limite de porta, parâmetros e tempo; apresentar o ciclo proposta → decisão → execução → resultado → interpretação. Esclarecer que o acesso por Kali/VPN e o timeout sem VPN são evidências históricas dos caminhos testados em 27/10, não prova universal de isolamento.

## 2:00–5:45 — Investigação real INV-02

Mostrar `docs/investigacoes/INV-02/resumo.md`, abrindo os registros privados apenas após revisão de dados sensíveis. Apresentar hipótese e objetivo, email fictício fixo e variável senha. Descrever as propostas B (senha vazia) e A (texto inválido), as decisões do revisor Codex delegado e as execuções realmente registradas no run `1ae38ffd4ed54a308ec9bd16c5017800`. Os resultados `c3a3deedc7924c769c1a4635c1cdf47f` e `e32b00e3c32744fb82587a270a5c80d2` indicam HTTP 401 e corpos iguais de 26 bytes. Mostrar que a interpretação do Qwen antecipou a comparação após apenas B e descreveu erroneamente a variável; explicar a correção delegada e a comparação posterior efetivamente observada. Concluir que não houve diferença nesses dois controles e que isso não comprova segurança geral ou bypass. A variante C não foi executada nessa sessão.

## 5:45–7:00 — Outros casos

Mostrar a matriz: INV-01 confirmou porta aberta, versão HTTP 17.3.0 e produto público; não identificar aplicação pelo rótulo `ppp` nem alegar descoberta independente de rotas fornecidas. INV-03 observou listagem `/ftp/` e 403 para o negativo `.txt`; a extensão e a existência variaram juntas, impedindo concluir como o servidor trata uma ausência `.md`. Nenhum arquivo foi baixado.

## 7:00–8:15 — Limitação da IA e replay

Apresentar o resultado `36e3c3e4cc8443dda703cda8ee39d3c8`: tamanho anunciado 80117 bytes e resposta truncada, mas o Qwen descreveu HTML completo. A sessão original foi interrompida e não tem conclusão final. Se forem usados resultados de replay, informar que as evidências de entrada eram simuladas, que nenhuma proposta foi executada, e citar somente contagens e comparações realmente registradas; temperatura zero não assegura estabilidade.

## 8:15–9:15 — Conclusão e limites

Reforçar a distinção entre saída, interpretação e decisão. A operação delegada não prova intervenção humana individual; a adequação da adaptação ao enunciado precisa ser validada pelo professor. Mostrar fontes e IDs; informar que WAN atual, sessões 03B ao vivo e vídeo final precisam de verificação. Encerrar sem prometer vulnerabilidades não demonstradas.

Antes de gravar, revisar tela, dados pessoais, credenciais e trechos de logs. Após gravar, conferir inteligibilidade, correspondência com evidências e duração real inferior a dez minutos.
