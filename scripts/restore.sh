#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$SCRIPT_DIR/lab_common.sh"
lab_args "$@"
lab_preflight
lab_addresses
container_id=$(lab_container_id)
printf 'Restauração apaga os dados de kit11-juice (%s). Digite RESTAURAR: ' "$container_id"
read -r answer
[ "$answer" = RESTAURAR ] || exit 1
# Reinspecionar após a confirmação e remover pelo ID, nunca somente pelo nome.
current_id=$(lab_container_id)
if [ "$current_id" != "$container_id" ]; then
    echo 'Container mudou durante a confirmação; remoção recusada.' >&2
    exit 1
fi
lab_docker container rm --force "$container_id" >/dev/null
exec "$SCRIPT_DIR/start.sh"
