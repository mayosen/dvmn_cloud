import asyncio
import time


def ftime() -> str:
    return time.strftime("%X")


async def timer(timer_id: str, delay: int):
    for i in range(delay):
        print(f"timer: {timer_id}, iter: {i + 1}")
        await asyncio.sleep(1)


async def main_1():
    """
    Работают последовательно.
    6s
    """

    print(f"started at {ftime()}")

    await timer("first", 2)
    await timer("second", 4)

    print(f"finished at {ftime()}")


async def main_2():
    """
    Работают конкурентно.
    4s
    """
    print(f"started at {ftime()}")

    t1 = timer("first", 2)
    t2 = timer("second", 4)
    await asyncio.gather(t1, t2)

    print(f"finished at {ftime()}")


async def main_3():
    """
    Работают последовательно.
    6s
    """
    print(f"started at {ftime()}")

    await asyncio.create_task(timer("first", 2))
    await asyncio.create_task(timer("second", 4))

    print(f"finished at {ftime()}")


async def main_4():
    """
    Работают конкурентно.
    Но в чем разница с предыдущим примером?
    Тут Task просто сохраняются в переменные
    4s
    """
    print(f"started at {ftime()}")

    t1 = asyncio.create_task(timer("first", 2))
    t2 = asyncio.create_task(timer("second", 4))
    await t1
    await t2

    print(f"finished at {ftime()}")


async def main_5():
    """
    gather работает конкурентно как с корутинами, так и с Task
    4s
    """
    print(f"started at {ftime()}")

    task1 = asyncio.create_task(timer("first", 2))
    task2 = asyncio.create_task(timer("second", 4))
    await asyncio.gather(task1, task2)

    print(f"finished at {ftime()}")


asyncio.run(main_5())
