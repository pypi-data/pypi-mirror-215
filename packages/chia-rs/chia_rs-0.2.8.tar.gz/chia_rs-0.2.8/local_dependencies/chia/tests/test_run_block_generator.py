from chia_rs import run_block_generator
from chia_rs import MEMPOOL_MODE
import pytest

def test_run_block_generator_cost() -> None:

    generator = bytes.fromhex(open("generator-tests/block-834768.txt", "r").read().split("\n")[0])
    # the total cost of this generator is 635805370
    err, conds = run_block_generator(generator, [], 635805370, 0)
    assert err is None
    assert conds is not None

    # we exceed the cost limit by 1
    err, conds = run_block_generator(generator, [], 635805370 - 1, 0)
    # BLOCK_COST_EXCEEDS_MAX = 23
    assert err == 23
    assert conds is None

    # the byte cost alone exceeds the limit by 1
    err, conds = run_block_generator(generator, [], len(generator) * 12000 - 1, 0)
    # BLOCK_COST_EXCEEDS_MAX = 23
    assert err == 23
    assert conds is None
