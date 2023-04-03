#!/usr/bin/env python3
"""A basic async syntax"""
from asyncio import sleep
from random import random


async def wait_random(max_delay: int = 10) -> float:
    """waits for a random number of seconds"""
    wait_seconds: float = random() * max_delay
    await sleep(wait_seconds)
    return wait_seconds
