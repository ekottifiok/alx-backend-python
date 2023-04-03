#!/usr/bin/env python3
"""Concurrent Coroutine"""

from asyncio import gather
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """returns a list of all the delays in float"""
    return sorted(
        await gather(
            *list(map(lambda _: wait_random(max_delay), range(n)))
        )
    )
