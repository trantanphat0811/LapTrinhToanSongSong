import time

def process_item (item):
    print(f"Processing item: {item} (sequential)")
    time.sleep(1) # Simulate processing time 1-sec task
    print (f"Finished processing item: {item} (sequential)")
    return item * 2 # Return the processed item

def main ():
    items= [1,2,3,4,5]
    results= []
    
    for item in items:
        results.append(process_item(item))
        results.append(results)
    print ('all item processed')    
    print (f"Results: {results}")
    
if __name__ == "__main__":
    main()