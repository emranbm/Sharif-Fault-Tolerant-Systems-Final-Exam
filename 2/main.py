
from typing import List, Tuple
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

TASK_WCET = 10
TASK_BCET = 1
TASK_DEADLINE = 20
ENERGY_CONSUMPTION_PER_MS = 100
ONE_MS_TASK_FAILURE_PROBABILITY = pow(10, -4)

CONCURRENCY_NUMBER = 8


def main():
    n = int(input('Experiments count: '))
    random.seed(datetime.now())
    if n < 1:
        raise Exception("Experiments count should be at least 1")

    type_a_actual_times: List[int] = []
    type_b_actual_times: List[int] = []

    if n % CONCURRENCY_NUMBER != 0:
        print(
            f"Warning: Experiments count should be product of {CONCURRENCY_NUMBER} to be exactly the same as number of performed experiments.")

    futures = []
    for i in range(CONCURRENCY_NUMBER):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(
                experiment_for_n, int(n / CONCURRENCY_NUMBER))
            futures.append(future)

    for future in futures:
        result = future.result()
        type_a_actual_times = type_a_actual_times + result[0]
        type_b_actual_times = type_b_actual_times + result[1]

    type_a_failure_probability = get_failure_probability(type_a_actual_times)
    type_b_failure_probability = get_failure_probability(type_a_actual_times)

    type_a_avg_energy_consumption = get_avg_energy_consumption(
        type_a_actual_times)
    type_b_avg_energy_consumption = get_avg_energy_consumption(
        type_b_actual_times)

    print(f"""
Type A:
Failure Probability: {type_a_failure_probability}
Average Energy Consumption: {type_a_avg_energy_consumption}
""")
    print(f"""
Type B:
Failure Probability: {type_b_failure_probability}
Average Energy Consumption: {type_b_avg_energy_consumption}
""")


def experiment_for_n(n: int) -> Tuple[List[int], List[int]]:
    if n < 1:
        raise Exception("Experiments count should be at least 1")

    type_a_actual_times: List[int] = []
    type_b_actual_times: List[int] = []
    last_percent_completed = 0
    for i in range(n):
        percent_completed = int(i/n*100)
        if percent_completed > last_percent_completed:
            # print(f"{percent_completed}%  -  {i} out of {n} experiments done.\n")
            last_percent_completed = percent_completed
        task_time = get_task_time()
        type_a_subtasks = devide_to_subtasks_type_a(task_time)
        type_b_subtasks = devide_to_subtasks_type_b(task_time)
        actual_time_spent_type_a = get_actual_time_spent(type_a_subtasks)
        actual_time_spent_type_b = get_actual_time_spent(type_b_subtasks)
        type_a_actual_times.append(actual_time_spent_type_a)
        type_b_actual_times.append(actual_time_spent_type_b)

    return type_a_actual_times, type_b_actual_times


def get_task_time() -> int:
    return random.randint(TASK_BCET, TASK_WCET)


def devide_to_subtasks_type_a(task_time: int) -> List[int]:
    return _devide_to_subtasks_by_segments(task_time, [2, 2, 2, 2, 2])


def devide_to_subtasks_type_b(task_time: int) -> List[int]:
    return _devide_to_subtasks_by_segments(task_time, [1, 1.5, 2, 2.5, 3])


def _devide_to_subtasks_by_segments(task_time: int, segments: List[int]) -> List[int]:
    assert sum(
        s for s in segments) == TASK_WCET, f"Sum segments is not equal to WCET ({TASK_WCET})"
    remained_time = task_time
    subtasks = []
    for s in segments:
        if remained_time >= s:
            subtasks.append(s)
            remained_time -= s
        else:
            subtasks.append(remained_time)
            remained_time = 0
            break
    assert remained_time == 0, f"Unexpected remained time: {remained_time} (total: {task_time})"
    return subtasks


def get_actual_time_spent(subtasks: List[int]) -> int:
    actual_time_spent = 0
    for subtask in subtasks:
        actual_time_spent += subtask  # Do it for the first time
        while is_subtask_failed(subtask) and actual_time_spent <= TASK_DEADLINE:
            actual_time_spent += subtask  # Do it again
        if actual_time_spent > TASK_DEADLINE:
            break
    return actual_time_spent


def is_subtask_failed(subtask: int) -> bool:
    # Probability of failure: subtask * failure_prob
    rand_num = random.randint(1, int(1 / ONE_MS_TASK_FAILURE_PROBABILITY))
    if rand_num <= subtask:
        return True
    else:
        return False


def get_failure_probability(actual_times: List[int]) -> float:
    failure_count = sum(t > TASK_DEADLINE for t in actual_times)
    return failure_count / len(actual_times)


def get_avg_energy_consumption(actual_times) -> float:
    total_time = sum(t for t in actual_times)
    total_energy = total_time * ENERGY_CONSUMPTION_PER_MS
    return total_energy / len(actual_times)


if __name__ == '__main__':
    main()
