import csv
from decimal import Decimal
import functools
import fire
import reactivex
from reactivex import operators

def aggregate(step: float, accumulator: tuple[int, int], current: tuple[int, int]):
    previous_steps, current_steps = current
    change_in_steps = abs(current_steps - previous_steps)
    if change_in_steps != 0:
        if previous_steps < current_steps:
            return (accumulator[0], accumulator[1] + change_in_steps)
        else:
            return (accumulator[0] + change_in_steps, accumulator[1])
    return accumulator

def back_test_2(path: str, step: Decimal):
    step = Decimal(str(step))
    with open(path) as csv_file:
        reader = csv.reader(csv_file)
        initial_price = Decimal(next(reader)[1])
        csv_file.seek(0)
        reactivex.from_iterable(reader).pipe(
            operators.map(lambda x: Decimal(x[1])),
            operators.start_with(initial_price),

        )

def back_test(path: str, step: Decimal):
    step = Decimal(str(step))
    with open(path) as csv_file:
        with open(path.replace('.csv', '.out.csv'), 'w') as csv_out:
            writer = csv.writer(csv_out)
            reader = csv.reader(csv_file)
            initial_price = Decimal(next(reader)[1])
            csv_file.seek(0)
            steps = reactivex.of(0.01, 0.03, 0.05, 0.1, 1, 3, 10).pipe(
                operators.map(lambda x: Decimal(str(x))),
                operators.share()
            )
            reactivex.zip(
                steps,
                steps.pipe(
                    operators.flat_map(lambda local_step: reactivex.from_iterable(reader).pipe(
                        operators.map(lambda x: initial_price - Decimal(x[1])),
                        operators.map(lambda x: int(x / local_step)),
                        # operators.distinct_until_changed(),
                        operators.pairwise(),
                        operators.reduce(
                            functools.partial(aggregate, local_step)
                        , (0, 0))
                    )),
                    operators.do_action(on_next=lambda _: csv_file.seek(0)),
                )
            ).pipe(
                operators.map(lambda x: (x, x[0] * Decimal(1/3) * (x[1][0] + x[1][1])))
            ).subscribe(print, print, print)
                
if __name__ == "__main__":
    fire.Fire(back_test)
