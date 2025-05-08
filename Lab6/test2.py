import time
import threading



global swapped
# hàm vòng lặp xử lí j
def sort(j,arr,swapped,sleep_time):
    if arr[j] > arr[j + 1]:
        arr[j], arr[j + 1] = arr[j + 1], arr[j]
        swapped = True
        print(arr)
    time.sleep(sleep_time)
    return arr, swapped,sleep_time

def bubble_sort_with_sleep(arr, sleep_time=0.5):
    n = len(arr)
    total_sleep_time = 0
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            for i in range(n-j-1): #tạo số lượng thread dựa trên số lượng phần từ có index = 0 đến vị trí không swap
                thread = threading.Thread(target=sort,args=(i,arr,swapped,sleep_time))
                thread.start()
            total_sleep_time+=sleep_time
            thread.join()
        if not swapped:
            break
    return arr, total_sleep_time


# Example usage
my_list = [64, 34, 25, 12, 22, 11, 90]
print("Initial list: ", my_list)
sorted_list, total_sleep = bubble_sort_with_sleep(my_list,sleep_time=2)  # Reduced sleep time for faster execution.
print("Sorted list:", sorted_list)
print("Total sleep time:", total_sleep, "seconds")