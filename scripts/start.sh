#!/bin/sh
set -eu
IP=${1:?Informe o IPv4 privado da interface autorizada}
python3 -c 'import sys; from agent import local_ip; local_ip(sys.argv[1])' "$IP"
if [ -n "$(docker ps -aq -f name='^kit11-juice$')" ]; then echo 'Container kit11-juice já existe; não será alterado.' >&2; exit 1; fi
exec docker run -d --name kit11-juice --restart no --publish "$IP:3000:3000" bkimminich/juice-shop:v17.3.0
