import random
import time
from concurrent.futures import ThreadPoolExecutor

def generate_random_numbers(size, lower_bound=0, upper_bound=100):
    return random.sample(range(lower_bound, upper_bound + 1), size)

def bubble_sort_with_sleep(arr, sleep_time=5):
    n = len(arr)
    total_sleep_time = 1
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                print(arr)
                time.sleep(sleep_time)
                total_sleep_time += sleep_time
        if not swapped:
            break
    return arr, total_sleep_time

def bubble_sort_step_with_sleep(data, sleep_time=1):
    total_sleep = 0
    for i in range(len(data) - 1):
        if data[i] > data[i + 1]:
            data[i], data[i + 1] = data[i + 1], data[i]
            print(f"Đã đổi chỗ cặp chỉ số: {(i, i + 1)}")
            time.sleep(sleep_time)
            total_sleep += sleep_time
            break  # Chỉ đổi chỗ 1 lần mỗi vòng
    return data, total_sleep

def is_sorted(data):
    return all(data[i] <= data[i + 1] for i in range(len(data) - 1))

def parallel_bubble_sort_with_sleep(data):
    total_sleep_time = 1
    step = 0
    while not is_sorted(data):
        print(f"\nVòng {step + 1}:")
        with ThreadPoolExecutor() as executor:
            future = executor.submit(bubble_sort_step_with_sleep, data)
            data, sleep_time = future.result()
            total_sleep_time += sleep_time
            print(f"Sau vòng {step + 1}: {data}")
        step += 1
    return data, total_sleep_time

def main():
    full_set = generate_random_numbers(100)
    print("Tập hợp ban đầu (100 số):", full_set)

    selected_set = []
    while len(selected_set) < 12:
        number = random.choice(full_set)
        if number not in selected_set:
            selected_set.append(number)
            print(f"Đã chọn số: {number}")
            time.sleep(2)

    print("Tập hợp chọn lọc (12 số):", selected_set)

    # Sequential sort
    sequential_set = selected_set.copy()
    start_time = time.time()
    sorted_sequential, sequential_sleep_time = bubble_sort_with_sleep(sequential_set, sleep_time=1)
    sequential_time = time.time() - start_time
    print("Kết quả sắp xếp tuần tự:", sorted_sequential)
    print("Thời gian sắp xếp tuần tự: {:.6f} giây".format(sequential_time))
    print("Tổng thời gian sleep tuần tự: {:.2f} giây".format(sequential_sleep_time))

    # Parallel sort
    parallel_set = selected_set.copy()
    start_time = time.time()
    sorted_parallel, parallel_sleep_time = parallel_bubble_sort_with_sleep(parallel_set)
    parallel_time = time.time() - start_time
    print("\nKết quả sắp xếp song song:", sorted_parallel)
    print("Thời gian sắp xếp song song: {:.6f} giây".format(parallel_time))
    print("Tổng thời gian sleep song song: {:.2f} giây".format(parallel_sleep_time))

    speedup = sequential_time / parallel_time if parallel_time > 0 else float('inf')
    print("Tốc độ tăng (Speedup): {:.2f}".format(speedup))

if __name__ == "__main__":
    main()
