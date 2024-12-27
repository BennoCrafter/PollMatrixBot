import functools

def once(func):
    """Decorator to ensure the function only runs once."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if not wrapper._called:
            wrapper._called = True
            return await func(*args, **kwargs)
    wrapper._called = False
    return wrapper
