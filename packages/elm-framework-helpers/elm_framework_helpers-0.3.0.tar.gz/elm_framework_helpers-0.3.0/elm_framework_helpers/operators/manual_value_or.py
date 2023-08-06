from reactivex import Observable, operators
import reactivex
from typing import TypeVar, Callable

T = TypeVar("T")

def manual_value_or_operator(source: Observable[T]) -> Callable[[Observable[T]], Observable[T]]:
    """Apply to this to a "manual" observable and provide an alternative source. When the manual observable emits None, the source observable will be used until it completes or the manual observable emits a value.

    Args:
        source (Observable[T]): the alternative source used whenever the manual observable emits None

    Returns:
        Callable[[Observable[T]], Observable[T]]: the operator
    """
    def manual_value_or(manual: Observable[T]):
        shared = manual.pipe(operators.share())
        return shared.pipe(
            operators.flat_map_latest(
                lambda value: reactivex.just(value)
                if value is not None
                else source.pipe(
                    operators.take_until(
                        reactivex.concat(
                            shared.pipe(operators.ignore_elements()),
                            reactivex.just(1),
                        )
                    )
                )
            )
        )
    return manual_value_or