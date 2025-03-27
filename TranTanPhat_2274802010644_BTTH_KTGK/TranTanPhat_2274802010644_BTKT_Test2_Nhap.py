import threading
import random
import time

MAX_DEPTH = 3  
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)

def merge(left, right): 
    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])   
    return merged

def threaded_merge_sort(arr, depth=0):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = []
    right_half = []
    if depth < MAX_DEPTH: 
        left_thread = threading.Thread(target=lambda: left_half.extend(threaded_merge_sort(arr[:mid], depth+1)))
        right_thread = threading.Thread(target=lambda: right_half.extend(threaded_merge_sort(arr[mid:], depth+1)))
        left_thread.start()
        right_thread.start()
        left_thread.join()
        right_thread.join()
    else:
        left_half = merge_sort(arr[:mid])
        right_half = merge_sort(arr[mid:])
    return merge(left_half, right_half)

if __name__ == "__main__":
    random_list = [random.randint(0, 10000) for _ in range(2000)]
    start_time = time.time()
    sorted_seq = merge_sort(random_list)
    sequential_time = time.time() - start_time
    print(f"Thời gian tính toán tuần tự: {sequential_time:.4f} giây")
    start_time = time.time()
    sorted_thread = threaded_merge_sort(random_list)
    threading_time = time.time() - start_time
    print(f"Thời gian tính toán song song: {threading_time:.4f} giây")
    assert sorted_seq == sorted_thread, "Lỗi! Kết quả sắp xếp không giống nhau."
    speedup = sequential_time / threading_time
    print(f"Tốc độ cải thiện: {speedup:.2f}x")
    print(random_list)