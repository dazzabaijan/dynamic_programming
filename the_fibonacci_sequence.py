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
    if n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)
