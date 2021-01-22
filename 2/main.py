
from typing import List, Optional

TASK_DEADLINE = 20

def main():
    n = int(input('Experiments count: '))
    if n < 1:
        raise Exception("Experiments count should be at least 1")
    
    type_a_actual_times: List[int] = []
    type_b_actual_times: List[int] = []
    for i in range(n):
        total_time = get_task_total_time()
        type_a_subtasks = devide_to_subtasks_type_a(total_time)
        type_b_subtasks = devide_to_subtasks_type_b(total_time)
        actual_time_spent_type_a = get_actual_time_spent(type_a_subtasks)
        actual_time_spent_type_b = get_actual_time_spent(type_b_subtasks)
        type_a_actual_times.append(actual_time_spent_type_a)
        type_b_actual_times.append(actual_time_spent_type_b)
    
    type_a_failure_probability = get_failure_probability(type_a_actual_times)
    type_b_failure_probability = get_failure_probability(type_a_actual_times)

    type_a_avg_energy_consumption = get_avg_energy_consumption(type_a_actual_times)
    type_b_avg_energy_consumption = get_avg_energy_consumption(type_b_actual_times)

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

def get_task_total_time() -> int:
    raise NotImplementedError

def devide_to_subtasks_type_a(total_time: int) -> List[int]:
    raise NotImplementedError

def devide_to_subtasks_type_b(total_time: int) -> List[int]:
    raise NotImplementedError

def get_actual_time_spent(subtasks: List[int]) -> int:
    raise NotImplementedError

def get_failure_probability(actual_times: List[int]) -> float:
    failure_count = sum(t <= TASK_DEADLINE for t in actual_times)
    return failure_count / len(actual_times)

def get_avg_energy_consumption(type_a_actual_times) -> float:
    raise NotImplementedError

if __name__ == '__main__':
    main()
