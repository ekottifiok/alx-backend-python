#!/usr/bin/env python3
"""Task 0: Async Generator
"""
from asyncio import sleep
from random import random
from typing import AsyncIterator


async def async_generator() -> AsyncIterator[float]:
    """
    Write a coroutine called async_generator that takes no arguments.
    """
    for _ in range(10):
        await sleep(1)
        yield random() * 10
