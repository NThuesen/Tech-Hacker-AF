#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$SCRIPT_DIR/lab_common.sh"
lab_args "$@"
lab_preflight
lab_addresses
existing=$(lab_docker container ls -aq --filter 'name=^/kit11-juice$')
if [ -n "$existing" ]; then
    lab_container_id >/dev/null
    echo 'Container kit11-juice reconhecido; já existe e não será alterado.' >&2
    exit 1
fi
lab_docker run -d --pull never --name "$LAB_NAME" --restart no \
    --publish 127.0.0.1:3000:3000 \
    --publish 10.0.80.3:3001:3000 "$LAB_IMAGE"
