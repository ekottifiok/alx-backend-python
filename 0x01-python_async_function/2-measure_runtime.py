#!/usr/bin/env python3
"""Measure Runtime"""

from time import time
from asyncio import run
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """measures the time and returns it in float"""
    start_time = time()
    run(wait_n(n, max_delay))
    return (time() - start_time) / n
