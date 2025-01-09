import functools

def once(func):
    """Decorator to ensure the function only runs once."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if not wrapper._called: # type: ignore
            wrapper._called = True # type: ignore
            return await func(*args, **kwargs)
    wrapper._called = False # type: ignore
    return wrapper
