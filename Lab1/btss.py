import time
from dask import delayed, compute
from tqdm import tqdm

# 1. Hàm thực hiện tác vụ (giả lập một công việc tốn thời gian)
def inc(x):

    time.sleep(1)
    return x + 1

# 2. Tạo danh sách các tác vụ (lazy tasks) với cập nhật tiến độ
def create_tasks_with_progress(n_tasks):

    tasks = []
    with tqdm(total=n_tasks, desc="Tạo tác vụ") as pbar:
        for i in range(n_tasks):
            tasks.append(delayed(inc)(i))
            pbar.update(1)  # Cập nhật tiến độ sau mỗi tác vụ được tạo
    return tasks

# 3. Thực hiện tính toán song song với cập nhật tiến độ
def parallel_compute_with_progress(tasks):
 
    with tqdm(total=len(tasks), desc="Tiến độ tính toán") as pbar:
        def progress_callback(future):

            pbar.update(1)

        # Tính toán song song sử dụng Dask
        results = compute(*tasks, scheduler="threads", traverse=False, callback=progress_callback)
    return results

# 4. Chương trình chính
if __name__ == "__main__":
    print("Bắt đầu chương trình...")

    # Số lượng tác vụ
    n_tasks = 60

    # Bắt đầu thời gian thực thi
    start = time.time()

    # Tạo danh sách các tác vụ với tiến độ
    tasks = create_tasks_with_progress(n_tasks)
    results = parallel_compute_with_progress(tasks)
    end = time.time()

    print("Kết quả 5 phần tử đầu tiên:", results[:5])
    print(f"Thời gian thực thi: {end - start:.2f} giây")
