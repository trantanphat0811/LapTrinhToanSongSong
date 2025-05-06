import random
import threading
import time

# 1. Tạo file "numbers.txt" với 25 triệu số ngẫu nhiên
def generate_numbers_file(filename="numbers.txt", count=25_000_000, max_value=25_000_000, chunk_size=1_000_000):
    """Tạo file chứa số ngẫu nhiên theo từng khối để tránh quá tải bộ nhớ."""
    start_time = time.time()

    with open(filename, "w") as f:
        for _ in range(count // chunk_size):
            numbers = [str(random.randint(1, max_value)) for _ in range(chunk_size)]
            f.write("\n".join(numbers) + "\n")

    end_time = time.time()
    print(f"File {filename} đã được tạo với {count} số ngẫu nhiên.")
    print(f"Thời gian tạo file: {end_time - start_time:.2f} giây\n")

# 2. Merge Sort và Merge Sort song song
def merge_sort(arr):
    """Thuật toán Merge Sort tiêu chuẩn."""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """Hợp nhất hai danh sách đã sắp xếp."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def threaded_merge_sort(arr):
    """Hàm Merge Sort có sử dụng đa luồng."""
    if len(arr) <= 10_000:  # Khi nhỏ, dùng Merge Sort bình thường
        return merge_sort(arr)

    mid = len(arr) // 2
    left_sorted = []
    right_sorted = []

    t1 = threading.Thread(target=lambda: left_sorted.extend(merge_sort(arr[:mid])))
    t2 = threading.Thread(target=lambda: right_sorted.extend(merge_sort(arr[mid:])))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    return merge(left_sorted, right_sorted)

# 3. Đọc dữ liệu từ file theo từng khối
def read_numbers_in_chunks(filename, chunk_size=1_000_000):
    """Đọc dữ liệu từ file theo từng khối để tiết kiệm bộ nhớ."""
    with open(filename, "r") as f:
        while True:
            chunk = f.readlines(chunk_size)
            if not chunk:
                break
            yield list(map(int, chunk))

# 4. Sắp xếp song song và ghi ra file
def sort_numbers_from_file(input_file="numbers.txt", output_file="sorted_numbers.txt"):
    """Đọc dữ liệu từ file theo từng khối, sắp xếp song song và ghi ra file."""
    start_time = time.time()

    sorted_chunks = []
    threads = []

    for chunk in read_numbers_in_chunks(input_file):
        thread = threading.Thread(target=lambda c: sorted_chunks.append(threaded_merge_sort(c)), args=(chunk,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Hợp nhất danh sách đã sắp xếp
    while len(sorted_chunks) > 1:
        chunk1 = sorted_chunks.pop(0)
        chunk2 = sorted_chunks.pop(0)
        sorted_chunks.append(merge(chunk1, chunk2))  # Dùng merge để hợp nhất các khối đã sắp xếp

    sorted_numbers = sorted_chunks[0] if sorted_chunks else []

    # Ghi kết quả vào file
    with open(output_file, "w") as f:
        for num in sorted_numbers:
            f.write(f"{num}\n")
    
    end_time = time.time()
    print(f"Dữ liệu đã được sắp xếp và lưu vào {output_file}.")
    print(f"Thời gian sắp xếp và ghi file: {end_time - start_time:.2f} giây\n")

# Chạy chương trình
if __name__ == "__main__":
    total_start_time = time.time()

    generate_numbers_file()
    sort_numbers_from_file()

    total_end_time = time.time()
    print(f"Tổng thời gian thực thi: {total_end_time - total_start_time:.2f} giây")
