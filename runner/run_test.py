"""Runs ONE test+seed. Kubernetes-independent: configured purely via env vars.

Env: RUN_ID, TEST_NAME, TOP, MODULE, TESTCASE, SOURCES (comma sep), SEED, SIM,
     TIMEOUT_S, CONTROLLER_URL (optional), MINIO_ENDPOINT/ACCESS_KEY/SECRET_KEY (optional)
"""
import json, os, subprocess, time, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

E = os.environ.get
ROOT = Path("/work") if Path("/work/tb").exists() else Path(__file__).resolve().parent.parent
TB = ROOT / "tb"


def run():
    seed = E("SEED", "1")
    sim_build = TB / f"sim_build_{E('TEST_NAME')}_{seed}"
    results = TB / f"results_{E('TEST_NAME')}_{seed}.xml"
    sources = " ".join(str(ROOT / s) for s in E("SOURCES", "rtl/fifo/fifo.v").split(","))
    env = dict(os.environ, RANDOM_SEED=seed)
    if E("TESTCASE"):
        env["TESTCASE"] = E("TESTCASE")
    cmd = ["make", "-f", "Makefile.cocotb", f"SIM={E('SIM', 'icarus')}",
           f"TOPLEVEL={E('TOP', 'fifo')}", f"MODULE={E('MODULE', 'test_fifo')}",
           f"VERILOG_SOURCES={sources}", f"SIM_BUILD={sim_build}",
           f"COCOTB_RESULTS_FILE={results}"]
    start = time.time()
    try:
        proc = subprocess.run(cmd, cwd=TB, env=env, capture_output=True, text=True,
                              timeout=int(E("TIMEOUT_S", "300")))
        log, rc = proc.stdout + proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as e:
        log, rc = f"TIMEOUT\n{e.stdout or ''}", 124
    duration = time.time() - start

    passed = failed = 0
    if results.exists():
        for tc in ET.parse(results).getroot().iter("testcase"):
            if tc.find("failure") is not None or tc.find("error") is not None:
                failed += 1
            else:
                passed += 1
    status = "pass" if rc == 0 and failed == 0 and passed > 0 else "fail"
    sig = next((l.strip() for l in log.splitlines() if "AssertionError" in l or "Error" in l), "")
    return {"run_id": E("RUN_ID", "local"), "test": E("TEST_NAME", "adhoc"), "seed": int(seed),
            "status": status, "passed": passed, "failed": failed,
            "duration_s": round(duration, 2), "error_signature": sig[:200]}, log



def upload(result, log):
    if not E("MINIO_ENDPOINT"):
        return

    from minio import Minio
    from minio.error import S3Error

    client = Minio(
        E("MINIO_ENDPOINT"),
        E("MINIO_ACCESS_KEY"),
        E("MINIO_SECRET_KEY"),
        secure=False
    )

    bucket = "artifacts"

    # Create the bucket if it does not exist.
    if not client.bucket_exists(bucket):
        try:
            client.make_bucket(bucket)
        except S3Error as exc:
            # Another parallel runner may have created it first.
            if exc.code not in (
                "BucketAlreadyOwnedByYou",
                "BucketAlreadyExists"
            ):
                raise

    # Upload logs and waveforms.
    prefix = f"{result['run_id']}/{result['test']}_{result['seed']}"

    log_path = Path("/tmp/log.txt")
    log_path.write_text(log)

    client.fput_object(
        bucket,
        f"{prefix}/log.txt",
        str(log_path)
    )

    for pattern in ("*.fst", "*.vcd"):
        for file in TB.rglob(pattern):
            client.fput_object(
                bucket,
                f"{prefix}/{file.name}",
                str(file)
            )


def report(result):
    url = E("CONTROLLER_URL")
    if not url:
        return
    req = urllib.request.Request(url.rstrip("/") + "/results", json.dumps(result).encode(),
                                 {"Content-Type": "application/json"})
    for _ in range(5):
        try:
            urllib.request.urlopen(req, timeout=10); return
        except Exception:
            time.sleep(2)


if __name__ == "__main__":
    result, log = run()
    print(json.dumps(result)); print(log[-2000:])
    try:
        upload(result, log)
    except Exception as e:
        print("artifact upload failed:", e)
    report(result)
    raise SystemExit(0 if result["status"] == "pass" else 1)
