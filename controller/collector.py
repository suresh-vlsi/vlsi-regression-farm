"""Placeholder: aggregate results per run, group failures by error_signature, merge coverage."""
from collections import Counter
from models import Result, get_session


def failure_clusters(run_id):
    s = get_session()
    rows = s.query(Result).filter(Result.run_id == run_id, Result.status == "fail").all()
    return Counter(r.error_signature for r in rows).most_common()
