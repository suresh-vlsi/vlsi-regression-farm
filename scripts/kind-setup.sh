#!/usr/bin/env bash
set -euo pipefail
kind create cluster --name vlsi-farm || true
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
make images
for i in vlsi-runner vlsi-controller vlsi-dashboard; do kind load docker-image $i:latest --name vlsi-farm; done
echo "Cluster ready. Next: make deploy"
