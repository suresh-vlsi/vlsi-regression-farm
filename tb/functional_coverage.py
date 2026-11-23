"""Transaction-level functional coverage for the FIFO regression."""

import json
import os
from pathlib import Path


class FIFOCoverage:
    def __init__(self, depth=16):
        self.depth = depth

        self.hits = {
            "reset": 0,
            "write_accepted": 0,
            "read_accepted": 0,
            "empty_observed": 0,
            "full_observed": 0,
            "simultaneous_read_write": 0,
            "write_pointer_wrap": 0,
            "read_pointer_wrap": 0,
            "write_rejected_full": 0,
            "read_rejected_empty": 0,
        }

        self.write_count = 0
        self.read_count = 0

    def record_reset(self):
        self.hits["reset"] += 1

    def sample(self, wr_en, rd_en, full, empty):
        """Record one clock cycle using pre-edge FIFO status."""

        if empty:
            self.hits["empty_observed"] += 1

        if full:
            self.hits["full_observed"] += 1

        write_ok = bool(wr_en and not full)
        read_ok = bool(rd_en and not empty)

        if wr_en and full:
            self.hits["write_rejected_full"] += 1

        if rd_en and empty:
            self.hits["read_rejected_empty"] += 1

        if write_ok:
            self.write_count += 1
            self.hits["write_accepted"] += 1

            if self.write_count % self.depth == 0:
                self.hits["write_pointer_wrap"] += 1

        if read_ok:
            self.read_count += 1
            self.hits["read_accepted"] += 1

            if self.read_count % self.depth == 0:
                self.hits["read_pointer_wrap"] += 1

        if write_ok and read_ok:
            self.hits["simultaneous_read_write"] += 1

    def report(self):
        bins = {
            name: {
                "covered": count > 0,
                "hits": count,
            }
            for name, count in self.hits.items()
        }

        covered = sum(item["covered"] for item in bins.values())
        total = len(bins)

        return {
            "design": "fifo",
            "depth": self.depth,
            "coverage_type": "cocotb_functional",
            "covered_bins": covered,
            "total_bins": total,
            "coverage_percent": round(100 * covered / total, 2),
            "bins": bins,
            "accepted_writes": self.write_count,
            "accepted_reads": self.read_count,
            "seed": int(os.environ.get("RANDOM_SEED", "1")),
            "testcase": os.environ.get("TESTCASE", "unknown"),
        }

    def save(self, filename=None):
        filename = filename or os.environ.get(
            "COVERAGE_FILE", "functional_coverage.json"
        )

        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.report(), indent=2))

        print(f"Functional coverage saved: {path}")
        return self.report()
