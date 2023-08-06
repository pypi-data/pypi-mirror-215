"""Rate limit module."""
from datetime import datetime, timedelta
from functools import wraps
import logging
import shelve

from . import config

logger = logging.getLogger(__name__)


class OverLimit(Exception):
    """The number of requests exceeds the limit."""
    pass


def check_limit(limit, unit, name='default'):
    """Increment count and compare to limit.

    Args:
        limit: integer for the max number of executions.
        unit: 'SECOND', 'MINUTE', 'HOUR', 'DAY'.
        name: name of the limiter. Default is 'default'.

    Raises:
        OverLimit: number of calls is over the limit.

    Uses a fixed window rate length algorithm:

    1. On the first call, store the datetime stamp and the count (1) in
    the shelf file.
    2. On subsequent calls, check the datetime: if the time window has
    expired, store the new datetime and reset the count to (1).
    3. If the window hasn't expired, increment the count and store it.
    4. If the count is over the limit, raise OverLimit exception.

    If RATE_LIMIT_DB_PATH isn't set, check_limit() exits immediately.

    Example::

        from drakken.rate_limit import check_limit, OverLimit

        try:
            check_limit(limit=12, unit='MINUTE')
        except OverLimit as e:
            s = f'Rate limit exceeded: {limit} per {unit} count: {e}'
            logger.warning(s)
            return None
    """
    path = config.get('RATE_LIMIT_DB_PATH')
    if not path:
        return
    d = shelve.open(path, writeback=True)
    # Initialize dict if empty.
    if name in d:
        d[name]['count'] += 1
    else:
        d[name] = dict(count=1, start_time=datetime.now())
        d.close()
        return
    delta = timedelta(**{unit.lower() + 's': 1})
    # If time expired, reset.
    if datetime.now() > d[name]['start_time'] + delta:
        d[name]['start_time'] = datetime.now()
        d[name]['count'] = 1
    elif d[name]['count'] > limit:
        count = d[name]['count']
        d.close()
        raise OverLimit(count)
    d.close()


def rlimit(limit, unit, name='default'):
    """Rate limit decorator that calls `check_limit()`.

    Args:
        limit: integer for the max number of executions.
        unit: 'SECOND', 'MINUTE', 'HOUR', 'DAY'.
        name: name of the limiter. Default is 'default'.

    If the rate limit is exceeded the decorated function isn't executed.

    Example::

        import drakken.rate_limit as rlimit

        @rlimit.rlimit(limit=3, unit='SECOND')
        def sum(x, y):
            return x + y

        z = sum(4, 3)   # 1
        z = sum(12, 1)  # 2
        z = sum(6, 2)   # 3
        z = sum(9, 5)   # Over limit
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                check_limit(limit, unit, name)
            except OverLimit as e:
                s = f'Rate limit exceeded: {limit} per {unit} count: {e}'
                logger.warning(s)
                return None
            res = function(*args, **kwargs)
            return res
        return wrapper
    return decorator

