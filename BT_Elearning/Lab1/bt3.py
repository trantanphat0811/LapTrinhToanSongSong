from multiprocessing import Process, Manager

def bubble_sort(shared_arr):
    for i in range(len(shared_arr)):
        for j in range(len(shared_arr) - 1):
            if shared_arr[j] > shared_arr[j + 1]:
                shared_arr[j], shared_arr[j + 1] = shared_arr[j + 1], shared_arr[j]
    print("Mảng sau khi sắp xếp:", list(shared_arr))

if __name__ == '__main__':
    with Manager() as manager:
        arr = manager.list([64, 34, 25, 12, 22, 11, 90])  # Dùng Manager để tạo danh sách chia sẻ
        p = Process(target=bubble_sort, args=(arr,))
        p.start()
        p.join()
        print("Mảng trong tiến trình chính:", list(arr))
