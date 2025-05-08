import time
import threading

def bubble_sort_with_sleep(arr, sleep_time=0.1):
    """
    Sorts a list using the parallel bubble sort algorithm (Odd-Even Transposition Sort)
    with sleep after each swap, and counts the total sleep time.
    
    
    
    
    
    Args:
        arr: The list to be sorted.
        sleep_time: The time to sleep (in seconds) after each swap.
    
    
    
    
    
    Returns:
        A tuple containing the sorted list and the total sleep time.
    """
    n = len(arr)
    total_sleep_time = 0
    arr = arr.copy()  # Avoid modifying the original list

    print_lock = threading.Lock()
    sleep_lock = threading.Lock()
    
    def swap_if_needed(i, phase_swapped):
        nonlocal total_sleep_time
        if i + 1 < n and arr[i] > arr[i + 1]:
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
            phase_swapped[0] = True
            
            with print_lock:
                print(arr)
            
            time.sleep(sleep_time)
            
            with sleep_lock:
                total_sleep_time += sleep_time
    
    swapped = True
    while swapped:
        swapped = False
        
        odd_swapped = [False]  
        threads = []
        
        for i in range(1, n - 1, 2):
            thread = threading.Thread(target=swap_if_needed, args=(i, odd_swapped))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        even_swapped = [False] 
        threads = []
        
        for i in range(0, n - 1, 2):
            thread = threading.Thread(target=swap_if_needed, args=(i, even_swapped))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        swapped = odd_swapped[0] or even_swapped[0]
    
    return arr, total_sleep_time

# Example usage
if __name__ == "__main__":
    my_list = [64, 34, 25, 12, 22, 11, 90]
    print("Initial list:", my_list)
    sorted_list, total_sleep = bubble_sort_with_sleep(my_list, sleep_time=1) # Reduced sleep time for faster execution.
    print("Sorted list:", sorted_list)
    print("Total sleep time:", total_sleep, "seconds")


# my_list2 = [5, 1, 4, 2, 8, -2, 4, 0]
# sorted_list2, total_sleep2 = bubble_sort_with_sleep(my_list2, sleep_time=1)
# print("Sorted list 2:", sorted_list2)
# print("Total sleep time 2:", total_sleep2, "seconds")