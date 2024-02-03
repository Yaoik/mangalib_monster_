import asyncio
import random
from typing import Coroutine

async def async_generator(max_concurrent:int, coroutines:list[Coroutine]):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def execute_with_semaphore(coroutine):
        async with semaphore:
            return await coroutine

    for coroutine in asyncio.as_completed([execute_with_semaphore(c) for c in coroutines]):
        yield await coroutine
        
async def example_coroutine(name):
    time = random.random()
    await asyncio.sleep(time) # Якобы работа функции
    print(f"Coroutine {name} completed after {time} seconds")
    return f"Result from {name}"

async def main():
    coroutines = [example_coroutine(i) for i in range(1000)]

    max_concurrent = 16  # Здесь вы можете установить максимальное количество одновременно выполняющихся корутин

    async for result in async_generator(max_concurrent, coroutines):
        print(f"Received result: {result}")

if __name__ == "__main__":
    asyncio.run(main())