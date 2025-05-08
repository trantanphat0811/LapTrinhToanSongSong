import time
import threading

def process_item(item):
    print(f"Processing item: {item} (Parallel)") 
    time.sleep(1)  # Simulate processing time
    print(f"Finished processing item: {item} (Parallel)")
    return item * 2  # Return the processed item

def main():
    items = [1,2,3,4,5]
    results = [None] * len(items)
    threads = []

    def thread_function(index, item):
        results[index] = process_item(item)

    for i, item in enumerate(items): # Enumerate the items
        thread = threading.Thread(target=thread_function, args=(i, item)) # Create a thread for each item
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print('All items processed')
    print(f"Results: {results}")

if __name__ == "__main__":
    main()