
"""Merge Cocotb FIFO functional coverage reports and optionally upload to MinIO."""

import json
import os
import sys
from pathlib import Path
from collections import Counter


def upload_to_minio(output_file):
    endpoint = os.getenv("MINIO_ENDPOINT")
    access_key = os.getenv("MINIO_ACCESS_KEY")
    secret_key = os.getenv("MINIO_SECRET_KEY")

    if not all((endpoint, access_key, secret_key)):
        print("MinIO upload skipped: credentials or endpoint not configured.")
        return

    from minio import Minio
    from minio.error import S3Error

    bucket = os.getenv("MINIO_BUCKET", "artifacts")
    object_name = os.getenv(
        "FUNCTIONAL_COVERAGE_OBJECT",
        "coverage/fifo/latest.json"
    )

    client = Minio(
        endpoint,
        access_key,
        secret_key,
        secure=False
    )

    try:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)

        client.fput_object(
            bucket,
            object_name,
            str(output_file),
            content_type="application/json"
        )

        print(f"MinIO upload successful: {bucket}/{object_name}")

    except S3Error as exc:
        raise RuntimeError(
            f"MinIO upload failed: {exc.code}"
        ) from exc


def merge_coverage(input_dir, output_file):
    input_dir = Path(input_dir)
    output_file = Path(output_file)

    reports = sorted(input_dir.glob("*.json"))

    if not reports:
        raise FileNotFoundError(
            f"No coverage reports found in {input_dir}"
        )

    merged_hits = Counter()
    report_names = []
    design = None
    depth = None

    for report_path in reports:
        with report_path.open() as file:
            report = json.load(file)

        if report.get("coverage_type") != "cocotb_functional":
            raise ValueError(
                f"Unexpected coverage type in {report_path}"
            )

        if design is None:
            design = report["design"]
            depth = report["depth"]
        elif design != report["design"] or depth != report["depth"]:
            raise ValueError("Incompatible design or FIFO depth")

        for bin_name, details in report["bins"].items():
            merged_hits[bin_name] += details["hits"]

        report_names.append(report_path.name)

    bins = {
        name: {
            "covered": hits > 0,
            "hits": hits
        }
        for name, hits in sorted(merged_hits.items())
    }

    total_bins = len(bins)
    covered_bins = sum(item["covered"] for item in bins.values())

    result = {
        "design": design,
        "depth": depth,
        "coverage_type": "cocotb_functional",
        "reports_merged": len(report_names),
        "source_reports": report_names,
        "covered_bins": covered_bins,
        "total_bins": total_bins,
        "coverage_percent": round(
            100 * covered_bins / total_bins, 2
        ) if total_bins else 0,
        "bins": bins
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w") as file:
        json.dump(result, file, indent=2)

    print(f"Reports merged: {len(report_names)}")
    print(f"Coverage: {covered_bins}/{total_bins}")
    print(f"Functional coverage: {result['coverage_percent']}%")
    print(f"Output: {output_file}")

    upload_to_minio(output_file)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python3 functional_coverage_merge.py "
            "<input_dir> <output_file>"
        )
        sys.exit(1)

    merge_coverage(sys.argv[1], sys.argv[2])
