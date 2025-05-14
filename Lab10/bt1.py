from multiprocessing import Pool
import numpy as np

# Hàm tính tổng các phần tử trong một đoạn của mảng
def sum_array(arr):
    return sum(arr)

# Hàm chia mảng thành các phần nhỏ
def split_array(arr, num_parts):
    n = len(arr)
    part_size = n // num_parts
    parts = [arr[i * part_size:(i + 1) * part_size] for i in range(num_parts)]
    # Thêm phần còn lại vào phần cuối nếu mảng không chia hết
    if n % num_parts != 0:
        parts[-1] = arr[(num_parts - 1) * part_size:]
    return parts

# Hàm chính để tính tổng song song
def parallel_sum(arr, num_processes):
    # Chia mảng thành các phần
    parts = split_array(arr, num_processes)

    # Sử dụng Pool để tính tổng song song
    with Pool(processes=num_processes) as pool:
        results = pool.map(sum_array, parts)

    # Tổng hợp kết quả
    total_sum = sum(results)
    return total_sum

# Ví dụ sử dụng
if __name__ == '__main__':
    # Tạo mảng ngẫu nhiên
    arr = np.random.randint(1, 100, size=1000)  # Mảng 1000 phần tử ngẫu nhiên từ 1 đến 99
    num_processes = 4  # Số tiến trình

    # Tính tổng song song
    result = parallel_sum(arr, num_processes)
    print(f"Tong cua mang: {result}")

    # Kiểm tra kết quả
    expected_sum = sum(arr)
    print(f"Kiem tra (tong truc tiep): {expected_sum}")
    print(f"Ket qua co dung khong? {result == expected_sum}")