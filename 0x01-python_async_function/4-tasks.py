#!/usr/bin/env python3
"""Concurrent Coroutine"""

from asyncio import gather
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    returns a list of all the delays in float by
    executing task_wait_random n times
    """
    return sorted(
        await gather(
            *list(map(lambda _: task_wait_random(max_delay), range(n)))
        )
    )
