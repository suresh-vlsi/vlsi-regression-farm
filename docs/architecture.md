# Architecture
```
testlist.yaml -> controller (/regressions) -> K8s Jobs (runner image)
runner -> POST /results -> controller -> Postgres -> dashboard
runner -> logs/waveforms -> MinIO
controller /metrics -> Prometheus -> Grafana
```
OpenSTA and SymbiYosys are not in apt; add them to docker/eda-base for the timing/formal stretch goals.
