from __future__ import annotations

import functools
import inspect
from typing import Callable, TypeVar

from absl import logging

R = TypeVar("R")


def log_before(
    func: Callable[[...], R], logger: Callable[[str], None] = logging.debug
) -> Callable[[...], R]:
    """

    Parameters
    ----------
    func
    logger

    Returns
    -------

    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> R:
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments
        func_args_str = ", ".join(map("{0[0]} = {0[1]!r}".format, func_args.items()))
        logger(
            f"Entered {func.__module__}.{func.__qualname__} with args ( {func_args_str} )"
        )
        return func(*args, **kwargs)

    return wrapper


def log_after(
    func: Callable[[...], R], logger: Callable[[str], None] = logging.debug
) -> Callable[[...], R]:
    """
    Log's function's return value.

    Parameters
    ----------
    func:
        Function exit from which must be logged.
    logger:
        Logger to use, default absl.logging.debug

    Returns
    -------

    func:
        Function with the same signature.

    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> R:
        retval = func(*args, **kwargs)
        logger(
            f"Exited {func.__module__}.{func.__qualname__}(...) with value: "
            + repr(retval)
        )
        return retval

    return wrapper
