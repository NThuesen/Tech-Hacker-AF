#!/bin/sh
set -eu
IP=${1:?Informe o IPv4 privado da interface autorizada}
python3 -c 'import sys; from agent import local_ip; local_ip(sys.argv[1])' "$IP"
printf 'A restauração apaga os dados do container kit11-juice. Digite RESTAURAR: '
read -r answer
[ "$answer" = RESTAURAR ] || exit 1
if [ -n "$(docker ps -aq -f name='^kit11-juice$')" ]; then docker rm -f kit11-juice >/dev/null; fi
exec ./scripts/start.sh "$IP"
