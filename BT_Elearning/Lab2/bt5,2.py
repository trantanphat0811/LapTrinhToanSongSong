from multiprocessing import Process, Queue

def binary_search(arr, key, queue):
    arr.sort()  # Đảm bảo mảng đã được sắp xếp
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if key == arr[mid]:
            queue.put(mid)  # Gửi kết quả về tiến trình chính
            return
        elif key < arr[mid]:
            right = mid - 1
        else:
            left = mid + 1
    queue.put(-1)  # Gửi -1 nếu không tìm thấy

if __name__ == '__main__':
    arr = [64, 34, 25, 12, 22, 11, 90]
    key = 25

    queue = Queue()  # Tạo hàng đợi để nhận kết quả
    p = Process(target=binary_search, args=(arr, key, queue))
    p.start()
    p.join()

    # Lấy kết quả từ tiến trình con
    result = queue.get()
    print('Vị trí của phần tử là:', result)
