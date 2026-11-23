import os
from kubernetes import client, config

NAMESPACE = os.environ.get("NAMESPACE", "vlsi-farm")


def _load():
    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()


def create_test_job(run_id, test, seed, defaults):
    _load()
    name = f"{run_id}-{test['name']}-{seed}".lower().replace("_", "-")[:52]
    env = {
        "RUN_ID": run_id, "TEST_NAME": test["name"], "TOP": test["top"],
        "MODULE": test["module"], "TESTCASE": test.get("testcase", ""),
        "SOURCES": ",".join(test["sources"]), "SEED": str(seed),
        "SIM": test.get("sim", defaults.get("sim", "icarus")),
        "TIMEOUT_S": str(test.get("timeout_s", defaults.get("timeout_s", 300))),
        "CONTROLLER_URL": os.environ.get("CONTROLLER_URL", "http://controller:8000"),
        "MINIO_ENDPOINT": os.environ.get("MINIO_ENDPOINT", "minio:9000"),
    }
    secret = lambda k: client.V1EnvVar(name=k, value_from=client.V1EnvVarSource(
        secret_key_ref=client.V1SecretKeySelector(name="farm-secrets", key=k)))
    container = client.V1Container(
        name="runner", image=os.environ.get("RUNNER_IMAGE", "vlsi-runner:latest"),
        image_pull_policy="IfNotPresent",
        env=[client.V1EnvVar(name=k, value=v) for k, v in env.items()]
            + [secret("MINIO_ACCESS_KEY"), secret("MINIO_SECRET_KEY")],
        resources=client.V1ResourceRequirements(
            requests={"cpu": "250m", "memory": "256Mi"}, limits={"cpu": "1", "memory": "1Gi"}))
    job = client.V1Job(
        metadata=client.V1ObjectMeta(name=name, labels={"app": "vlsi-test", "run": run_id}),
        spec=client.V1JobSpec(
            backoff_limit=0, ttl_seconds_after_finished=3600, active_deadline_seconds=900,
            template=client.V1PodTemplateSpec(spec=client.V1PodSpec(
                restart_policy="Never", containers=[container]))))
    client.BatchV1Api().create_namespaced_job(NAMESPACE, job)
    return name
