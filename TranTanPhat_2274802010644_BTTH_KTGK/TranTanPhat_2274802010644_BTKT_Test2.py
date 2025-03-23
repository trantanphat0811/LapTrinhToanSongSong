import threading
import random
import time

MAX_DEPTH = 3  # Giới hạn độ sâu của threading để tránh quá tải CPU

def merge_sort(arr):
    """Thuật toán Merge Sort tuần tự"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)

def merge(left, right):
    """Gộp hai danh sách đã sắp xếp thành một danh sách"""
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
    """Merge Sort song song với threading, kiểm soát số cấp độ song song"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = []
    right_half = []

    if depth < MAX_DEPTH:
        # Tạo hai luồng mới để sắp xếp hai nửa của danh sách
        left_thread = threading.Thread(target=lambda: left_half.extend(threaded_merge_sort(arr[:mid], depth+1)))
        right_thread = threading.Thread(target=lambda: right_half.extend(threaded_merge_sort(arr[mid:], depth+1)))

        left_thread.start()
        right_thread.start()

        left_thread.join()
        right_thread.join()
    else:
        # Nếu đạt đến độ sâu tối đa, sử dụng thuật toán tuần tự
        left_half = merge_sort(arr[:mid])
        right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)

if __name__ == "__main__":
    # Tạo danh sách ngẫu nhiên gồm 2000 phần tử
    random_list = [random.randint(0, 10000) for _ in range(2000)]

    # Đo thời gian chạy của Merge Sort tuần tự
    start_time = time.time()
    sorted_seq = merge_sort(random_list)
    sequential_time = time.time() - start_time
    print(f"Thời gian Merge Sort tuần tự: {sequential_time:.4f} giây")

    # Đo thời gian chạy của Merge Sort song song (threading)
    start_time = time.time()
    sorted_thread = threaded_merge_sort(random_list)
    threading_time = time.time() - start_time
    print(f"Thời gian Merge Sort song song: {threading_time:.4f} giây")
    
   
    assert sorted_seq == sorted_thread, "Lỗi! Kết quả sắp xếp không giống nhau."

   
    speedup = sequential_time / threading_time
    print(f"Tốc độ cải thiện: {speedup:.2f}x")
    print(random_list)