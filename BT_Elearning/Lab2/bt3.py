from multiprocessing import Process
def bubble_sort(arr):   
    for i in range(len(arr)):
        for j in range(len(arr) - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    print("Mảng sau khi sắp xếp:", arr)
if __name__ == '__main__':
    p= Process(target=bubble_sort, args=([64, 34, 25, 12, 22, 11, 90],))
    p.start()
    p.join()