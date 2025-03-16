from threading import Thread, Lock, Event

max_elements = 16
max_thread = 4
arr = [1, 5, 7, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34]
key = 16

step = 0
lock = Lock()  # Khóa để đồng bộ hóa
found_event = Event()  # Sự kiện để xác nhận tìm thấy phần tử
found_index = -1  # Lưu vị trí của phần tử

def binary_search():
    global step, found_index
    with lock:
        thread_step = step
        step += 1
    
    left = int(thread_step * (max_elements / max_thread))
    right = int((thread_step + 1) * (max_elements / max_thread)) - 1  # Giảm 1 để tránh lỗi index
    
    while left <= right and not found_event.is_set():
        mid = left + (right - left) // 2
        if arr[mid] == key:
            found_index = mid
            found_event.set()  # Đánh dấu đã tìm thấy
            break
        elif arr[mid] > key:
            right = mid - 1
        else:
            left = mid + 1

if __name__ == '__main__':
    threads = []
    
    # Khởi tạo và chạy các luồng
    for _ in range(max_thread):
        t = Thread(target=binary_search)
        threads.append(t)
        t.start()
    
    # Chờ tất cả các luồng hoàn thành
    for t in threads:
        t.join()
    
    # In kết quả
    if found_event.is_set():
        print(f'Đã tìm thấy phần tử {key} tại vị trí {found_index}')
    else:
        print(f'Không tìm thấy phần tử {key}')
