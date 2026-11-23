# VLSI Regression Farm
Cloud-native verification regressions: cocotb + Icarus/Verilator in containers, one Kubernetes Job per test/seed.

## Quick start
```bash
make test-local          # needs iverilog + cocotb (pip install cocotb==1.9.2)
make images && make up   # Compose: postgres, minio, controller, dashboard
make run-seeds           # parallel seeds via the Compose runner
```
Kubernetes (kind):
```bash
make kind && make deploy && make regress
```
Edit `tb/testlist.yaml` to add tests/seeds. See `docs/`.
