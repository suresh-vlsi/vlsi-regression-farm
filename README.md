# ⚡ VLSI Regression Farm

### Automated RTL Verification | Regression Orchestration | Functional Coverage Analytics

## 🌐 Project Links

| Resource | Link |
|---|---|
| 🌍 **Live Website** | [VLSI Regression Farm Dashboard](https://suresh-vlsi.github.io/vlsi-regression-farm/) |
| 💻 **GitHub Repository** | [View Source Code](https://github.com/suresh-vlsi/vlsi-regression-farm) |
| 📐 **Architecture** | [System Architecture](docs/architecture.md) |
| 📘 **Setup Guide** | [Windows & Docker Quickstart](docs/windows-docker-quickstart.md) |
| 🔧 **Integration Guide** | [Adding an RTL Design](docs/adding-a-design.md) |

---

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/suresh-vlsi/vlsi-regression-farm)
[![GitHub Pages](https://img.shields.io/badge/Live%20Website-Visit-2563eb?logo=githubpages)](https://suresh-vlsi.github.io/vlsi-regression-farm/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Cocotb](https://img.shields.io/badge/Cocotb-Verification-orange)](https://www.cocotb.org/)

---

**VLSI Regression Farm** is a containerized RTL verification and regression automation platform designed to execute hardware verification workloads, orchestrate simulation jobs, collect regression results, merge functional coverage reports, and visualize verification analytics.

The platform integrates open-source EDA tools, Python-based verification, Docker containers, Kubernetes orchestration, FastAPI services, PostgreSQL analytics, and MinIO artifact storage.

---

## 🎯 Project Objectives

- Automate RTL simulation and regression execution.
- Support scalable, containerized verification workloads.
- Orchestrate regression jobs using Kubernetes.
- Integrate Cocotb-based functional verification.
- Collect and merge functional coverage reports.
- Store verification artifacts using MinIO.
- Track regression campaigns and test results using PostgreSQL.
- Provide a dashboard for verification analytics.
- Establish a foundation for CI/CD-driven RTL verification.

---

## 🏗️ System Architecture

The platform follows a modular architecture that separates RTL verification, regression execution, orchestration, data collection, artifact storage, and visualization.

```text
                   RTL DESIGN
                       |
                       v
                Cocotb Testbench
                       |
                       v
                 Regression Runner
                       |
                       v
              EDA Simulation Engines
              /                  \
        Icarus Verilog          Verilator
              \                  /
                       |
                       v
               Test Result Collector
                       |
                       v
                FastAPI Controller
                       |
              +--------+--------+
              |                 |
              v                 v
         PostgreSQL           MinIO
       Campaign Data      Coverage Artifacts
              |                 |
              +--------+--------+
                       |
                       v
                Analytics Dashboard
```

### Infrastructure Components

| Component | Responsibility |
|---|---|
| Docker | Containerized EDA and application environments |
| Kubernetes | Regression job orchestration |
| FastAPI | Controller and API services |
| PostgreSQL | Campaign and regression analytics |
| MinIO | Coverage and verification artifact storage |
| Python | Automation and result processing |
| GitHub Actions | CI/CD workflows |

---

## 📊 Regression Results

The current recorded FIFO regression campaign produced the following results:

| Metric | Result |
|---|---:|
| Tests Passed | 10 / 10 |
| Pass Rate | 100% |
| Tests Failed | 0 |
| Functional Coverage | 100% |
| Coverage Bins Covered | 10 / 10 |
| Coverage Reports Merged | 4 |

### Functional Coverage

The FIFO verification environment includes the following transaction-level coverage bins:

| Coverage Bin | Description |
|---|---|
| Reset | FIFO reset operation |
| Write Accepted | Successful write transaction |
| Read Accepted | Successful read transaction |
| Empty Observed | FIFO empty condition |
| Full Observed | FIFO full condition |
| Simultaneous Read/Write | Concurrent read and write |
| Write Pointer Wrap | Write pointer wraparound activity |
| Read Pointer Wrap | Read pointer wraparound activity |
| Write Rejected When Full | Write request rejected at full condition |
| Read Rejected When Empty | Read request rejected at empty condition |

**Recorded functional coverage: 10/10 bins (100%).**

The pointer-wrap bins are inferred from accepted operation counts rather than direct observation of internal RTL pointer signals.

> Note: These figures represent recorded validation results, not a continuously running public regression service. The GitHub Pages dashboard currently presents a static snapshot of these results.

---

## 🛠️ Technology Stack

| Domain | Technologies |
|---|---|
| Programming | Python |
| RTL Simulation | Icarus Verilog, Verilator |
| Verification | Cocotb |
| Backend | FastAPI |
| Database | PostgreSQL |
| Object Storage | MinIO |
| Containerization | Docker, Docker Compose |
| Orchestration | Kubernetes, Kind |
| Deployment | Helm, Kustomize |
| CI/CD | GitHub Actions |
| Dashboard | HTML, CSS, JavaScript |

---

## 📁 Repository Structure

```text
vlsi-regression-farm/
│
├── .github/
│   └── workflows/
│       ├── build-images.yml
│       └── regression.yml
│
├── controller/
│   ├── collector.py
│   ├── k8s_client.py
│   ├── main.py
│   └── models.py
│
├── dashboard/
│   ├── app/
│   │   └── main.py
│   └── static/
│
├── docker/
│   ├── controller/
│   ├── dashboard/
│   ├── eda-base/
│   └── runner/
│
├── docs/
│   ├── architecture.md
│   ├── windows-docker-quickstart.md
│   ├── adding-a-design.md
│   └── index.html
│
├── helm/
│   └── vlsi-farm/
│
├── k8s/
│   ├── base/
│   ├── jobs/
│   ├── monitoring/
│   └── overlays/
│
├── results/
│   └── fifo_functional_coverage.json
│
├── rtl/
│   ├── fifo/
│   ├── picorv32/
│   └── uart/
│
├── runner/
│   ├── coverage_merge.py
│   ├── functional_coverage_merge.py
│   ├── run_test.py
│   └── entrypoint.sh
│
├── scripts/
│   ├── kind-setup.sh
│   └── submit_regression.sh
│
├── tb/
│   ├── coverage/
│   ├── functional_coverage.py
│   ├── test_fifo.py
│   └── testlist.yaml
│
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Install the following tools:

- Docker Desktop
- Ubuntu on WSL2 (Windows users)
- Python 3.12
- Git
- kubectl
- Kind
- Helm

### 1. Clone the Repository

```bash
git clone https://github.com/suresh-vlsi/vlsi-regression-farm.git

cd vlsi-regression-farm
```

### 2. Create a Python Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r controller/requirements.txt
pip install minio
```

The EDA tools and Cocotb dependencies are also configured through the project's Docker images.

### 4. Build Docker Images

```bash
docker compose --profile build build
```

### 5. Start the Local Services

```bash
docker compose up -d postgres minio controller dashboard
```

### 6. Access the Local Services

| Service | Local URL |
|---|---|
| Controller API | http://localhost:8001 |
| Controller Health | http://localhost:8001/healthz |
| Dashboard | http://localhost:8080 |
| MinIO Console | http://localhost:9001 |

Local service access depends on your Docker Compose configuration and environment variables.

---

## 🧪 Verification Workflow

The FIFO verification environment uses Cocotb to exercise the RTL design.

Implemented test scenarios include:

- FIFO reset verification
- Basic write and read operations
- FIFO fill-to-full operation
- Randomized transactions
- Read attempts while FIFO is empty

### Run the Cocotb Testbench

```bash
cd tb

make -f Makefile.cocotb
```

### Merge Functional Coverage Reports

From the repository root:

```bash
python runner/functional_coverage_merge.py \
    tb/coverage \
    results/fifo_functional_coverage.json
```

The merger combines individual Cocotb functional coverage reports into a consolidated JSON report and can optionally upload it to MinIO when the required environment variables are configured.

---

## ⚙️ CI/CD Integration

GitHub Actions workflows are included for:

**1. RTL Regression Workflow**

- Triggered by relevant RTL and testbench changes.
- Installs Icarus Verilog and Cocotb.
- Executes the FIFO simulation workflow.

**2. Docker Image Build Workflow**

- Builds the EDA base image.
- Builds the runner and controller images.
- Pushes configured container images to GitHub Container Registry (GHCR).

---

## 🔮 Future Development

Planned enhancements include:

- Public backend hosting and secure API integration.
- Dynamic dashboard updates from regression APIs.
- Multi-design regression support.
- Parallel regression scaling.
- Advanced coverage analytics.
- Regression history and trend visualization.
- Formal verification integration.
- Additional EDA tool integrations.
- Improved monitoring and observability.

---

## 👨‍💻 Author

**Kusumuru Suresh Kumar**

M.Tech, Systems & Control Engineering  
Indian Institute of Technology Bombay

Interested in RTL Design, Digital VLSI, ASIC Verification, Formal Verification, EDA Automation, and Semiconductor Engineering.

- GitHub: [@suresh-vlsi](https://github.com/suresh-vlsi)
- Project: [VLSI Regression Farm](https://github.com/suresh-vlsi/vlsi-regression-farm)
- Live Website: [VLSI Regression Farm Dashboard](https://suresh-vlsi.github.io/vlsi-regression-farm/)

---

## ⭐ Support

If you find this project interesting, consider giving the repository a ⭐ on GitHub.

**Built to explore scalable, automated and data-driven RTL verification.**
