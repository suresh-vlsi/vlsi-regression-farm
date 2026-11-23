FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential git make python3 python3-pip python3-venv \
      iverilog verilator yosys \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    libpython3.12-dev \
    && rm -rf /var/lib/apt/lists/*
# OpenSTA / SymbiYosys are not in apt: add them here for the timing/formal stretch goals.
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir cocotb==1.9.2 pytest pyyaml minio
