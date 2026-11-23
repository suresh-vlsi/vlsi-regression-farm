"""Merge Verilator coverage files: python coverage_merge.py out.dat in1.dat in2.dat ...
Requires `verilator_coverage` (shipped with Verilator)."""
import subprocess, sys
out, *ins = sys.argv[1:]
subprocess.run(["verilator_coverage", "-write", out, *ins], check=True)
subprocess.run(["verilator_coverage", "--annotate", "cov_annotated", out], check=True)
