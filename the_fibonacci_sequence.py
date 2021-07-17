from functools import lru_cache
import inspect


def stack_depth():
    return len(inspect.getouterframes(inspect.currentframe())) - 1


def fibonacci_1(n: int) -> int:
    """
    Brute force approach, O(2^n) exponential time

    Args:
        n: the n-th Fibonacci number 
    """
    print("{indent}fibonacci({n}) called".format(
        indent=" " * stack_depth(), n=n))

    if n <= 2:
        return 1
    return fibonacci_1(n - 1) + fibonacci_1(n - 2)


fibonacci_1(6)

fibonacci_cache = {}
def fibonacci_2(n: int) -> int:
    """
    Top down approach, O(n) linear time. Uses a global variable

    Args:
        n: the n-th Fibonacci number
    """

    if n <= 2:
        return 1
    if n not in fibonacci_cache:
        fibonacci_cache[n] = fibonacci_2(n - 1) + fibonacci_2(n - 2)

    return fibonacci_cache[n]


def fibonacci_3(n: int) -> int:
    """
    Top down approach. Uses a 'cache' attribute to avoid global variable in order
    to improve code readability. 
    """
    if n <= 2:
        return 1
    if not hasattr(fibonacci_3, 'cache'):
        fibonacci_3.cache = {}
    if n not in fibonacci_3.cache:
        fibonacci_3.cache[n] = fibonacci_3(n - 1) + fibonacci_3(n - 2)

    return fibonacci_3.cache[n]


def cached(f):
    """
    A custom decorator that performs caching .
    """
    cache = {}

    def worker(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return worker


@cached
def fibonacci(n):
    if n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


@lru_cache(maxsize=None)
def fibonacci(n):
    """
    Use the Least Recently Used caching by Python instead
    By default it's limited to 128 entries, with least-recently
    used entries evicted when limit is hit.
    Passing maxsize=None to lru_cache ensures that there
    is no memory limit and all values are cached.
    """
    if n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci(n):
    """
    Bottom-up approach, O(n) time and space complexity.
    Computes iteratively from smaller numbers.
    In practice performance is better than recursive method
    due to the lack of overhead in extra function calls.
    """

    series = [1, 1]
    while len(series) < n:
        series.append(series[-1] + series[-2])
    return series[-1]


def fibonacci(n):
    """
    Bottom-up approach 2, O(n) time but O(1) space complexity
    Only stores the last two number instead of the entire sequence
    Starts from the smallest subproblem (the first two numbers
    in the sequence), then expands the solution to reach the original
    problem (the n-th number in the sequence).
    """
    previous = 1
    current = 1
    for i in range(n - 2):
        next = current + previous
        previous, current = current, next
    return current
