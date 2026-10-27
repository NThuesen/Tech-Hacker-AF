#!/bin/sh
set -u
IP=${1:?Informe o IP atual do Ubuntu}
echo 'Diagnóstico local no Kali; não modifica configuração.'
cat /etc/os-release | head -6
ip -br addr
ip route get "$IP"
command -v nmap || true
curl --noproxy '*' --max-time 5 -sS -o /dev/null -w 'Juice Shop HTTP: %{http_code}\n' "http://$IP:3001/"
