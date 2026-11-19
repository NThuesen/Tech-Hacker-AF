# Evidências de rede — 03B, 19/11/2026

**Origem:** saídas relatadas por Nicholas na conversa. O Codex não executou os testes no Kali nem teve acesso aos arquivos primários. As informações abaixo são transcrição do relato, não verificação independente dos arquivos.

| Teste | Hora (-03) | Condições relatadas | Resultado relatado |
|---|---|---|---|
| Kali pela VPN | 11:58:27 | Kali `172.16.50.203/24`, `tun0` `10.8.0.2/24`; rota para `10.0.80.3` via `10.8.0.1`, `dev tun0` | Juice Shop HTTP 200; `curl_exit=0` |
| WAN sem VPN | 11:59:17 | Kali `172.16.50.203/24`; `tun0` ausente; rota para `192.168.20.31` via `172.16.50.1`, `dev eth0` | `http://192.168.20.31:3001/`: HTTP 000, timeout após 3000 ms, `curl_exit=28` |

O segundo teste indica **ausência de resposta no caminho, origem e momento relatados**. Não comprova isolamento WAN absoluto, nem verifica todas as regras, interfaces, endereços ou possibilidades de acesso. Uma captura das regras WAN/NAT feita em sessão anterior é histórica e não comprova sua configuração em 19/11.

## Evidências primárias e portões

- **PENDENTE:** receber os arquivos originais dos dois testes e capturas ou referência verificável das regras WAN/NAT atuais. Nicholas informou que os originais existem no Kali; não informou seus caminhos nem os disponibilizou ao KIT11. Ele confirmou que as capturas das regras são anteriores; não foram promovidas a verificação atual. Não foi presumido SSH para a VM Kali.
- A pasta privada `logs/03B/rede-20261119/` foi preparada no KIT11 com acesso `0700` e é ignorada pelo Git. Após transferência pelo grupo, registrar SHA-256 dos arquivos na origem e no destino, comparar os hashes, proteger os artefatos e documentar nomes/data/origem sem publicar seu conteúdo. Até lá, integridade e identidade dos arquivos são **NÃO VERIFICADAS**.
- **PENDENTE:** revisão das regras e do escopo do teste; aprovação real do plano/adendo por hash e supervisor no terminal; confirmação específica de restauração. A aprovação final de Nicholas não substitui uma decisão humana por ferramenta.
- **NÃO INICIADAS:** INV-01-B, INV-02-B e INV-03-B nesta sessão. Não existem resultados 03B novos nem decisões por ação a inserir no relatório.

## Verificação local complementar pelo Codex

Às 12:01:57 -03, o KIT11 mostrou `10.0.80.3/24`, rota padrão via `10.0.80.1`, listeners `127.0.0.1:3000`, `10.0.80.3:3001` e `127.0.0.1:11434`; serviços de usuário Docker Rootless e Ollama ativos. `lab_preflight` e `lab_container_id` validaram a imagem e a configuração do container `8be0a5edf7496ab70740087f2c6912c8b6d386a9755a314592078129d4e9ed11`, em execução. `/api/tags` identificou `qwen3:4b-instruct` digest `0edcdef34593eac1aa2be9c7d06c432dcf81945adca5eca2f27662c18f168ba0`. Apache, MySQL e OpenVPN foram informados ativos por `systemctl`; `ip_forward=0`. Essas leituras não verificam funcionalidade integral dos serviços ou o caminho WAN.
