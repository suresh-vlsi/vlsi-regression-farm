# Adding a design
1. Put RTL under `rtl/<name>/`.
2. Write `tb/test_<name>.py` (cocotb).
3. Add an entry to `tb/testlist.yaml` (top, module, sources, seeds).
4. `make images && make regress`.
