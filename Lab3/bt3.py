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

# 2. Selection Sort và Selection Sort song song
def selection_sort(arr):
    """Thuật toán Selection Sort tiêu chuẩn."""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def threaded_selection_sort(arr):
    """Selection Sort có sử dụng đa luồng."""
    if len(arr) <= 10_000:  # Khi nhỏ, dùng Selection Sort bình thường
        return selection_sort(arr)

    mid = len(arr) // 2
    left_sorted = []
    right_sorted = []

    t1 = threading.Thread(target=lambda: left_sorted.extend(selection_sort(arr[:mid])))
    t2 = threading.Thread(target=lambda: right_sorted.extend(selection_sort(arr[mid:])))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    return left_sorted + right_sorted

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
        thread = threading.Thread(target=lambda c: sorted_chunks.append(threaded_selection_sort(c)), args=(chunk,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Hợp nhất danh sách đã sắp xếp
    sorted_numbers = []
    for chunk in sorted_chunks:
        sorted_numbers.extend(chunk)
    sorted_numbers.sort()  # Dùng sort() để đảm bảo danh sách đã đúng thứ tự

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
