
import os
import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

from functional_coverage import FIFOCoverage


DEPTH = 16


async def reset(dut, coverage):
    dut.rst_n.value = 0
    dut.wr_en.value = 0
    dut.rd_en.value = 0
    dut.din.value = 0

    for _ in range(3):
        await RisingEdge(dut.clk)

    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    coverage.record_reset()


async def start(dut, coverage):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset(dut, coverage)


async def tick(dut, coverage, wr=0, rd=0, din=0):
    """Drive one cycle and record actual pre-edge FIFO status."""

    full = int(dut.full.value)
    empty = int(dut.empty.value)

    dut.wr_en.value = int(wr)
    dut.rd_en.value = int(rd)
    dut.din.value = int(din)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    coverage.sample(wr, rd, full, empty)

    return full, empty, bool(wr and not full), bool(rd and not empty)


def save_coverage(coverage):
    test_name = os.environ.get("TESTCASE", "unknown")
    seed = os.environ.get("RANDOM_SEED", "1")

    filename = f"/work/tb/coverage/{test_name}_seed_{seed}.json"

    coverage.save(filename)

@cocotb.test()
async def test_reset(dut):
    coverage = FIFOCoverage(DEPTH)
    await start(dut, coverage)

    assert int(dut.empty.value) == 1
    assert int(dut.full.value) == 0

    await tick(dut, coverage)
    save_coverage(coverage)


@cocotb.test()
async def test_basic_write_read(dut):
    coverage = FIFOCoverage(DEPTH)
    await start(dut, coverage)

    data = [0xA1, 0xB2, 0xC3]

    for value in data:
        await tick(dut, coverage, wr=1, din=value)

    for expected in data:
        _, _, _, read_ok = await tick(dut, coverage, rd=1)
        assert read_ok, "FIFO unexpectedly rejected a read"

        assert int(dut.dout.value) == expected

    save_coverage(coverage)


@cocotb.test()
async def test_fill_to_full(dut):
    coverage = FIFOCoverage(DEPTH)
    await start(dut, coverage)

    for i in range(DEPTH):
        await tick(dut, coverage, wr=1, din=i)

    assert int(dut.full.value) == 1

    # Attempt a write while full.
    _, _, write_ok, _ = await tick(
        dut, coverage, wr=1, din=0xAA
    )

    assert not write_ok, "FIFO should reject a write while full"

    save_coverage(coverage)


@cocotb.test()
async def test_random(dut):
    """Constrained-random FIFO test with reproducible seed."""

    coverage = FIFOCoverage(DEPTH)
    await start(dut, coverage)

    seed = int(os.environ.get("RANDOM_SEED", "1"))
    random.seed(seed)

    model = []

    for cycle in range(500):
        wr = random.random() < 0.6
        rd = random.random() < 0.5
        value = random.randrange(256)

        full, empty, write_ok, read_ok = await tick(
            dut, coverage, wr, rd, value
        )

        if write_ok:
            model.append(value)

        if read_ok:
            expected = model.pop(0)
            actual = int(dut.dout.value)

            assert actual == expected, (
                f"cycle {cycle}: got {actual}, expected {expected} "
                f"(seed={seed})"
            )

    save_coverage(coverage)

@cocotb.test()
async def test_read_while_empty(dut):
    coverage = FIFOCoverage(DEPTH)
    await start(dut, coverage)

    # Attempt to read while FIFO is empty.
    _, empty, _, read_ok = await tick(
        dut, coverage, rd=1
    )

    assert empty, "FIFO should be empty"
    assert not read_ok, "FIFO should reject read while empty"

    save_coverage(coverage)
