from typing import Any, Callable, Literal, TypeVar, Generator
from reactivex import observable, disposable, operators
import reactivex
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")

def retry_with_delay(delay_pattern: Generator[float, float, float], reset_after: observable.Observable[Any]) -> Callable[[observable.Observable[T]], observable.Observable[T]]:
    def _retry_with_delay(source: observable.Observable[T]) -> observable.Observable[T]:
        resetter = disposable.SerialDisposable()
        resetter.set_disposable(reactivex.never().subscribe())

        def make_reset_timer():
            logger.debug("Resetting retry delay")

            return reset_after.subscribe(on_completed=lambda: (
                delay_pattern.send(0)
            ))
        
        def on_caught_error(_exc, _src):
            delay = next(delay_pattern)
            logger.debug("Retrying in %s seconds", delay)
            return reactivex.timer(delay).pipe(
                operators.do_action(on_completed=lambda: (
                    resetter.set_disposable(make_reset_timer())
                )),
                operators.ignore_elements()
            )
        
        def cancel_reset(_exc):
            logger.debug("Canceling reset timer")
            resetter.current.dispose()

        return source.pipe(
            operators.do_action(on_error=cancel_reset),
            operators.catch(on_caught_error),
            operators.repeat()
        )
    return _retry_with_delay


def resettable_counter(values: list[float] | Generator[float, float, float], *, infinite_behavior: Literal["loop", "last", "raise"]="raise") -> Generator[float, float, float]:
    def reset():
        if callable(values):
            return values()
        else:
            return iter(values)

    value_iter = reset()
    current_value = next(value_iter)

    while True:
        reset_value = yield current_value
        if reset_value is not None:
            value_iter = reset()
            current_value = None
        else:
            try:
                current_value = next(value_iter)
            except StopIteration as exc:
                if infinite_behavior == "loop":
                    value_iter = reset()
                    current_value = next(value_iter)
                elif infinite_behavior == "last":
                    pass
                else:
                    raise exc

def kraken_delay():
    return resettable_counter([0, 0, 1, 2, 5], infinite_behavior="last")

def luno_delay():
    return resettable_counter([0, 1, 2, 4, 8, 16, 30, 60], infinite_behavior="loop")

def cryptodotcom_delay():
    return resettable_counter([0, 1, 2, 3, 4, 5], infinite_behavior="last")

def huobi_delay():
    return resettable_counter([0, 1, 2, 3, 4, 5], infinite_behavior="last")

def binance_delay():
    return resettable_counter([0, 1, 2, 3, 4, 5], infinite_behavior="last")