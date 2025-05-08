import time
import threading

def sort(j, arr, sleep_time, swapped_flag):
    if arr[j] > arr[j + 1]:
        arr[j], arr[j + 1] = arr[j + 1], arr[j]
        swapped_flag[0] = True
        print(arr)
    time.sleep(sleep_time)

def bubble_sort_with_sleep(arr, sleep_time=2.5):
    n = len(arr)
    total_sleep_time = 0
    for i in range(n):
        start_loop_time = time.time()
        swapped_flag = [False]
        threads = []
        for j in range(0, n - i - 1):
            thread = threading.Thread(target=sort, args=(j, arr, sleep_time, swapped_flag))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        total_sleep_time += sleep_time
        end_loop_time = time.time()
        print(f"Vòng lặp {i + 1} (Threading) thực thi trong: {end_loop_time - start_loop_time} giây")
        if not swapped_flag[0]:
            break
    return arr, total_sleep_time

# Example usage
if __name__ == "__main__":
    my_list = [64, 34, 25, 12, 22, 11, 90]
    print("Danh sách ban đầu:", my_list)
    
    # Sắp xếp nổi bọt sử dụng threading
    start_time = time.time()
    sorted_list, total_sleep = bubble_sort_with_sleep(my_list.copy(), sleep_time=2.5) # Reduced sleep time for faster execution.
    end_time = time.time()
    print("Danh sách sau khi sắp xếp (Threading):", sorted_list)
    print("Tổng thời gian ngủ (Threading):", total_sleep, "giây")
    print("Thời gian thực thi (Threading):", end_time - start_time, "giây")
