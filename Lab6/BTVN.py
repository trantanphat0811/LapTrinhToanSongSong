import time

 

def bubble_sort_with_sleep(arr, sleep_time=0.1):
    """
    Sorts a list using the bubble sort algorithm with sleep after each swap,
    and counts the total sleep time.

 

    Args:
        arr: The list to be sorted.
        sleep_time: The time to sleep (in seconds) after each swap.

 

    Returns:
        A tuple containing the sorted list and the total sleep time.
    """
    n = len(arr)
    total_sleep_time = 0
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                print(arr)
                time.sleep(sleep_time)
                total_sleep_time += sleep_time
        if not swapped:
            break
    return arr, total_sleep_time

 

# Example usage
my_list = [64, 34, 25, 12, 22, 11, 90]
print("Initial list: ", my_list)
sorted_list, total_sleep = bubble_sort_with_sleep(my_list, sleep_time=1)  # Reduced sleep time for faster execution.
print("Sorted list:", sorted_list)
print("Total sleep time:", total_sleep, "seconds")

 

# my_list2 = [5, 1, 4, 2, 8, -2, 4, 0]
# sorted_list2, total_sleep2 = bubble_sort_with_sleep(my_list2, sleep_time=1)
# print("Sorted list 2:", sorted_list2)
# print("Total sleep time 2:", total_sleep2, "seconds")