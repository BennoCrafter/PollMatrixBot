import datetime
import asyncio

async def call_at(date: datetime.date, coro, *args):
    """
    Schedule a coroutine to run at a specific date/time
    Args:
        date (datetime): The datetime at which to run the coroutine
        coro (Coroutine): The coroutine function to execute
        *args: Variable length argument list to pass to the coroutine
    """
    now = datetime.datetime.now()
    if date < now:
        return
    await asyncio.sleep((date - now).total_seconds())
    return await coro(*args)
