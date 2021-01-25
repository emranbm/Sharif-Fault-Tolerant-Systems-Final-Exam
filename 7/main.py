
from concurrent.futures import ThreadPoolExecutor
from typing import List
from numpy import random
from datetime import datetime

CONCURRENCY_FACTOR = 8
END_TIME = None
MTTF = 100


def main():
    n = int(input("Number of experiments: "))
    global END_TIME
    END_TIME = int(input("Each simulation time: "))
    random.seed((datetime.now() - datetime(2000, 1, 1)).seconds)
    if n % CONCURRENCY_FACTOR != 0:
        print(
            f"Warning: Experiments count should be product of {CONCURRENCY_FACTOR} to be exactly the same as number of performed experiments.")
    futures = []
    for i in range(CONCURRENCY_FACTOR):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(
                experiment_for_n, int(n / CONCURRENCY_FACTOR))
            futures.append(future)

    failure_times = []
    for future in futures:
        failure_times += future.result()

    total_failure_time = sum(a for a in failure_times)
    availability = 1 - total_failure_time / END_TIME
    print(f"Total Failure Time: {total_failure_time}")
    print(f"Failures Count: {len(failure_times)}")
    print(f"Steady Availabilty: {availability}")


def experiment_for_n(n: int) -> int:
    if n < 1:
        raise Exception("Experiments count should be at least 1")

    modules: List[int] = [0, 0, 0, 0]
    failure_times: List[int] = []
    system_last_fail = None
    for _ in range(n):
        for t in range(END_TIME):
            for i, m in enumerate(modules):
                if m == 0:  # ready to start
                    modules[i] = int(random.exponential(scale=MTTF))  # TTF
                elif m < 0:  # repairing
                    modules[i] += 1
                elif m > 0:  # working
                    modules[i] -= 1
                    if m == 0:  # failed
                        modules[i] = - \
                            int(random.uniform(low=0, high=100))  # TTR
            number_of_non_working_modules = sum(m <= 0 for m in modules)
            currently_failed = number_of_non_working_modules > 2
            if system_last_fail:
                if not currently_failed:
                    failure_times.append(t - system_last_fail)
                    system_last_fail = None
            else:
                if currently_failed:
                    system_last_fail = t
    return failure_times


if __name__ == '__main__':
    main()
