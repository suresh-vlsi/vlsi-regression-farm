import time
from pathlib import Path

import yaml
from fastapi import FastAPI
from prometheus_client import Counter, Histogram, make_asgi_app
from pydantic import BaseModel
from sqlalchemy import func

from models import Result, get_session

app = FastAPI(title="VLSI regression controller")
app.mount("/metrics", make_asgi_app())
TESTS = Counter("vlsi_tests_total", "Finished tests", ["status"])
DURATION = Histogram("vlsi_test_duration_seconds", "Test duration")


class ResultIn(BaseModel):
    run_id: str
    test: str
    seed: int
    status: str
    passed: int = 0
    failed: int = 0
    duration_s: float = 0
    error_signature: str = ""


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/regressions")
def start_regression(commit: str = ""):
    from k8s_client import create_test_job
    cfg = yaml.safe_load(Path("testlist.yaml").read_text())
    run_id = f"r{int(time.time())}"
    jobs = []
    for t in cfg["tests"]:
        for seed in t["seeds"]:
            jobs.append(create_test_job(run_id, t, seed, cfg.get("defaults", {})))
    return {"run_id": run_id, "jobs_created": len(jobs)}


@app.post("/results")
def post_result(r: ResultIn):
    s = get_session()
    s.add(Result(**r.model_dump()))
    s.commit()
    TESTS.labels(r.status).inc()
    DURATION.observe(r.duration_s)
    return {"ok": True}


@app.get("/summary")
def summary(run_id: str | None = None):
    s = get_session()
    q = s.query(Result.status, func.count()).group_by(Result.status)
    if run_id:
        q = q.filter(Result.run_id == run_id)
    return dict(q.all())
