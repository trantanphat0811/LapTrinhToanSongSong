import time
import multiprocessing

def process_item(item):
    print(f"Processing item: {item} (Parallel)") 
    time.sleep(1)  # Simulate processing time
    print(f"Finished processing item: {item} (Parallel)")
    return item * 2  # Return the processed item

def main():
    items = [1, 2, 3, 4, 5]

    with multiprocessing.Pool() as pool:
        results = pool.map(process_item, items)

    print('All items processed')
    print(f"Results: {results}")

if __name__ == "__main__":
    main()