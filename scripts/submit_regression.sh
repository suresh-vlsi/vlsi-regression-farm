#!/usr/bin/env bash
set -euo pipefail

PORT=18000
LOG=/tmp/vlsi-controller-port-forward.log

kubectl -n vlsi-farm port-forward svc/controller ${PORT}:8000 >"$LOG" 2>&1 &
PF=$!
trap 'kill "$PF" 2>/dev/null || true' EXIT

echo "Waiting for controller..."
READY=0
for i in $(seq 1 20); do
    if curl -fsS "http://localhost:${PORT}/healthz" >/dev/null; then
        READY=1
        break
    fi
    sleep 1
done

if [ "$READY" -ne 1 ]; then
    echo "Controller port-forward failed:"
    cat "$LOG"
    exit 1
fi

COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo none)

echo "Submitting FIFO regression campaign..."
curl --fail-with-body -sS -X POST \
    "http://localhost:${PORT}/regressions?commit=${COMMIT}"

echo
echo "Kubernetes regression jobs:"
kubectl -n vlsi-farm get jobs
