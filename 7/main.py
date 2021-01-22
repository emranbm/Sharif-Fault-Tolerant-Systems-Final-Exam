
from concurrent.futures import ThreadPoolExecutor
from typing import List
from numpy import random
from datetime import datetime

CONCURRENCY_NUMBER = 8
END_TIME = 10_000
MTTF = 100


def main():
    n = int(input("Number of experiments: "))
    random.seed((datetime.now() - datetime(2000, 1, 1)).seconds)
    if n % CONCURRENCY_NUMBER != 0:
        print(
            f"Warning: Experiments count should be product of {CONCURRENCY_NUMBER} to be exactly the same as number of performed experiments.")
    futures = []
    for i in range(CONCURRENCY_NUMBER):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(
                experiment_for_n, int(n / CONCURRENCY_NUMBER))
            futures.append(future)

    failure_times = []
    for future in futures:
        failure_times += future.result()

    availability_sum = sum(a for a in failure_times)
    availability = availability_sum / CONCURRENCY_NUMBER
    print(f"Steady Availabilty: {availability_sum}")


def experiment_for_n(n: int) -> int:
    if n < 1:
        raise Exception("Experiments count should be at least 1")

    modules: List[int] = [0, 0, 0, 0]
    failure_times: List[int] = []
    for _ in range(n):
        for i in range(END_TIME):
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
            if number_of_non_working_modules > 2:
                # failure happend!
                failure_times.append(i)
                break
    return failure_times


if __name__ == '__main__':
    main()
