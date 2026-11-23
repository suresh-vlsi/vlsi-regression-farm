ARG BASE=vlsi-eda-base:latest
FROM ${BASE}
WORKDIR /work
COPY rtl/ /work/rtl/
COPY tb/ /work/tb/
COPY runner/ /work/runner/
RUN useradd -m runner && chown -R runner /work
USER runner
ENTRYPOINT ["/work/runner/entrypoint.sh"]
