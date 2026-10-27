# Configuração compartilhada dos scripts; não inicia nem configura o daemon.
LAB_NAME=kit11-juice
LAB_IMAGE=bkimminich/juice-shop:v17.3.0
LAB_IMAGE_ID=sha256:123acb31ed8bb05ebb06934a29be83d4e11a46cae937b9ed2bf2bda29d98130a
LAB_DOCKER_HOST="unix:///run/user/$(id -u)/docker.sock"

lab_args() {
    if [ "$#" -gt 1 ] || [ "${1-127.0.0.1}" != 127.0.0.1 ]; then
        echo 'Uso: script [127.0.0.1]; bindings fixos: 127.0.0.1:3000 e 10.0.80.3:3001.' >&2
        exit 1
    fi
}

lab_docker() {
    DOCKER_CONTEXT= docker --host "$LAB_DOCKER_HOST" "$@"
}

lab_preflight() {
    lab_docker info --format '{{json .SecurityOptions}}' | python3 -c '
import json, sys
if "name=rootless" not in json.load(sys.stdin):
    sys.exit("Operação exige Docker Rootless; nenhuma alteração realizada.")
'
    image_id=$(lab_docker image inspect --format '{{.Id}}' "$LAB_IMAGE")
    if [ "$image_id" != "$LAB_IMAGE_ID" ]; then
        echo 'Imagem local divergente do digest validado; nenhuma alteração realizada.' >&2
        exit 1
    fi
}

lab_addresses() {
    python3 -c '
import socket
for address in ("127.0.0.1", "10.0.80.3"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((address, 0))
'
}

lab_container_id() {
    lab_docker container inspect "$LAB_NAME" | python3 -c '
import json, re, sys
items = json.load(sys.stdin)
if not isinstance(items, list) or len(items) != 1:
    sys.exit("Inspeção de container inválida; remoção recusada.")
c = items[0]
config, host = c.get("Config", {}), c.get("HostConfig", {})
labels = config.get("Labels") or {}
ports = host.get("PortBindings") or {}
expected = {("127.0.0.1", "3000"), ("10.0.80.3", "3001")}
bindings = ports.get("3000/tcp") or []
valid = (
    re.fullmatch(r"[0-9a-f]{64}", c.get("Id", ""))
    and c.get("Name") == "/kit11-juice"
    and c.get("Image") == sys.argv[1]
    and config.get("Image") == "bkimminich/juice-shop:v17.3.0"
    and labels.get("org.opencontainers.image.source") == "https://github.com/juice-shop/juice-shop"
    and labels.get("org.opencontainers.image.version") == "17.3.0"
    and not c.get("Mounts")
    and not host.get("Privileged")
    and host.get("NetworkMode") == "bridge"
    and set(ports) == {"3000/tcp"}
    and len(bindings) == 2
    and {(b.get("HostIp"), b.get("HostPort")) for b in bindings} == expected
)
if not valid:
    sys.exit("Identidade/configuração de kit11-juice divergente; remoção recusada.")
print(c["Id"])
' "$LAB_IMAGE_ID"
}
