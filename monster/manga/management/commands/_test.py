import asyncio
import random
import time
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

async def func1(i):
    await asyncio.sleep(random.random()*10)
    print(f'УРА! {i}')
    return i

async def main():
    coroutines = [example_coroutine(i) for i in range(100)]

    max_concurrent = 16  # Здесь вы можете установить максимальное количество одновременно выполняющихся корутин

    tasks = []
    async for result in async_generator(max_concurrent, coroutines):
        task = asyncio.create_task(func1(result))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    print(results)


if __name__ == "__main__":
    asyncio.run(main())