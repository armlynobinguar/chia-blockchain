from typing import List

from blspy import G2Element

from chia.types.blockchain_format.program import INFINITE_COST
from chia.types.coin_spend import CoinSpend
from chia.full_node.mempool_check_conditions import get_name_puzzle_conditions
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.spend_bundle import SpendBundle
from chia.full_node.bundle_tools import simple_solution_generator


def compute_coin_hints(cs: CoinSpend) -> List[bytes]:

    bundle = SpendBundle([cs], G2Element())
    generator = simple_solution_generator(bundle)

    npc_result = get_name_puzzle_conditions(
        generator,
        INFINITE_COST,
        cost_per_byte=DEFAULT_CONSTANTS.COST_PER_BYTE,
        mempool_mode=False,
        height=DEFAULT_CONSTANTS.SOFT_FORK_HEIGHT,
    )
    if npc_result.conds is None:
        return []

    h_list = []
    for spend in npc_result.conds.spends:
        for _, _, hint in spend.create_coin:
            if hint != b"":
                h_list.append(hint)

    return h_list
