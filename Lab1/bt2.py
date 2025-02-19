import numpy as np
import time
import dask.array as da

# Tạo mảng NumPy gồm 1,000,000 phần tử ngẫu nhiên
array = np.random.rand(1_000_000)

# 1. Tính tổng các phần tử bằng phương pháp tuần tự (sử dụng vòng lặp for)
start_sequential = time.time()  # Bắt đầu đo thời gian tuần tự
total_sequential = 0
for value in array:
    total_sequential += value  # Cộng dồn từng phần tử
end_sequential = time.time()  # Kết thúc đo thời gian tuần tự

# 2. Tính tổng các phần tử bằng phương pháp song song sử dụng Dask (vòng lặp trên từng chunk)
start_parallel = time.time()  # Bắt đầu đo thời gian song song
dask_array = da.from_array(array, chunks=10_000)  # Chia mảng NumPy thành các chunk nhỏ
chunks = dask_array.to_delayed()  # Chuyển mỗi chunk thành một đối tượng "delayed"
chunk_sums = [chunk.sum() for chunk in chunks]  # Tính tổng từng chunk
total_parallel = sum([chunk.compute() for chunk in chunk_sums])  # Tính tổng các chunk
end_parallel = time.time()  # Kết thúc đo thời gian song song

# Tính thời gian thực thi cho từng phương pháp
time_sequential = end_sequential - start_sequential
time_parallel = end_parallel - start_parallel

# Hiển thị kết quả và so sánh
print("Tổng (tuần tự):", total_sequential)
print("Thời gian (tuần tự): {:.5f} giây".format(time_sequential))
print("Tổng (song song):", total_parallel)
print("Thời gian (song song): {:.5f} giây".format(time_parallel))

# So sánh và xác định phương pháp nhanh hơn
if time_sequential < time_parallel:
    print("Phương pháp nhanh hơn: Tuần tự")
    print("Thời gian nhanh hơn: {:.5f} giây".format(time_parallel - time_sequential))
else:
    print("Phương pháp nhanh hơn: Song song")
    print("Thời gian nhanh hơn: {:.5f} giây".format(time_sequential - time_parallel))
