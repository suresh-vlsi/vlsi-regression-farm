# Windows 11 + Docker Desktop quick start

This guide runs the VLSI Regression Farm locally using Docker Desktop with the WSL 2 backend.

## 1. Prepare the workspace

In PowerShell, extract the project to `D:\AI-Deployment-Lab\vlsi-regression-farm` (adjust the ZIP path to where you saved the downloaded archive):

```powershell
New-Item -ItemType Directory -Force D:\AI-Deployment-Lab | Out-Null
Expand-Archive -LiteralPath "$HOME\Downloads\vlsi-regression-farm.zip" -DestinationPath D:\AI-Deployment-Lab -Force
```

The resulting project directory should be `D:\AI-Deployment-Lab\vlsi-regression-farm`.

## 2. Verify Docker Desktop and WSL integration

In PowerShell:

```powershell
wsl --status
wsl -l -v
```

Confirm the Ubuntu distribution uses WSL version 2. In Docker Desktop, enable **Settings → General → Use the WSL 2 based engine**, then enable Ubuntu under **Settings → Resources → WSL Integration**.

Open Ubuntu and run:

```bash
docker version
docker compose version
```

The client and server sections should both appear in `docker version`.

## 3. Enter the project

In Ubuntu:

```bash
cd /mnt/d/AI-Deployment-Lab/vlsi-regression-farm
ls
```

You should see `docker-compose.yml`, `Makefile`, `docker/`, `controller/`, `runner/`, `rtl/`, `tb/`, and `k8s/`.

## 4. Build the images

```bash
make images
```

This builds, in order:

- `vlsi-eda-base`: Ubuntu plus Icarus Verilog, Verilator, Yosys, Python and Cocotb.
- `vlsi-runner`: the RTL/Cocotb regression worker.
- `vlsi-controller`: the FastAPI regression API.
- `vlsi-dashboard`: the results dashboard.

The first build can take several minutes because the EDA base image installs packages.

## 5. Start the supporting services

```bash
make up
docker compose ps
```

Wait until PostgreSQL is healthy and the controller is running. MinIO exposes its API on port 9000 and its local console on port 9001.

## 6. Check the endpoints

Open these URLs in Windows:

- Dashboard: http://localhost:8080
- Controller health: http://localhost:8000/healthz
- Controller API docs: http://localhost:8000/docs
- MinIO console: http://localhost:9001

The default MinIO credentials in this local development Compose file are `minioadmin` / `minioadmin`. They are for local learning only; replace them before any shared or production deployment.

## 7. Run parallel FIFO seeds

```bash
make run-seeds
```

This starts four runner containers in parallel with seeds 1, 2, 3 and 4. Each runner compiles the FIFO RTL, executes the Cocotb random test, uploads its log to MinIO, and posts its result to the controller.

Refresh http://localhost:8080 to inspect results. You can also query:

```bash
curl http://localhost:8000/summary
```

## 8. Inspect and clean up

```bash
docker compose ps
docker compose logs --tail=100 controller dashboard postgres minio
docker ps -a
```

Stop the services but retain database and artifact data:

```bash
docker compose down
```

Stop services and delete local database/artifact volumes (destructive):

```bash
docker compose down -v
```

Do not run the destructive command unless you intentionally want to erase the local PostgreSQL and MinIO data.

## Notes

- Use Ubuntu/WSL commands from the project directory under `/mnt/d/...`.
- Docker image layers and container storage are managed by Docker Desktop and may still consume space on the Windows system drive. Project source files remain on D:.
- The Compose path is the first milestone. The Kubernetes controller code and manifests are a later milestone; we will set up Kind only after the Compose regression flow works.
